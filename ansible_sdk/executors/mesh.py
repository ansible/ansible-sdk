# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

import asyncio
import io
import os
import socket
import typing as t

from .._aiocompat.receptorctl_async import ReceptorControlAsync
from .._aiocompat.runner_async import asyncio_write_payload_and_close
from ..executors.base import AnsibleJobExecutorBase, AnsibleJobExecutorOptionsBase
from .. import AnsibleJobDef, AnsibleJobStatus
from .._util import dataclass_compat as dataclasses


@dataclasses.dataclass(kw_only=True, frozen=True)
class AnsibleMeshJobOptions(AnsibleJobExecutorOptionsBase):
    control_socket_url: str
    target_node: t.Optional[str] = None
    # FIXME: TBD how we want to represent EE execution to the mesh executor; probably want
    #  an assumption of a higher-level config than just hacking runner CLI args, but it's totally up to how
    #  the receptor config is set up. The following kinda sucks and is almost certainly not the "right" thing.
    container_runtime_exe: t.Optional[str] = None
    container_image_ref: t.Optional[str] = None


class AnsibleMeshJobExecutor(AnsibleJobExecutorBase):
    def __init__(self):
        self._running_job_info: dict[AnsibleJobStatus, _MeshJobInfo] = {}

    def _get_runner_args(self, job_def: AnsibleJobDef, options: AnsibleMeshJobOptions):
        args = {
            'private_data_dir': job_def.data_dir,
            'playbook': job_def.playbook,
        }

        if options.container_runtime_exe and options.container_image_ref:
            args['container_image'] = options.container_image_ref
            args['process_isolation'] = True
            args['process_isolation_executable'] = options.container_runtime_exe

        return args

    async def _stream_events(self, reader: asyncio.StreamReader, status_obj: AnsibleJobStatus) -> None:
        try:
            await super()._stream_events(reader, status_obj)
        finally:
            # FIXME: refetch status to get final exitcode

            # try to release work unit from mesh
            unit_id = self._running_job_info[status_obj].unit_id
            try:
                async with ReceptorControlAsync.create_ctx(status_obj._executor_options.control_socket_url) as rc:
                    await rc.simple_command_async(f'work force-release {unit_id}')
            except Exception as ex:
                # FIXME: log and propagate to status object
                pass

    async def submit_job(self, job_def: AnsibleJobDef, options: AnsibleMeshJobOptions) -> AnsibleJobStatus:
        loop = asyncio.get_running_loop()
        fds = os.pipe()
        with os.fdopen(fds[0], 'rb') as payload_reader, os.fdopen(fds[1], 'wb') as payload_writer:
            # FIXME: come up with a less brittle way to manage the pipe lifetime
            # start payload creation first by explicitly creating a task; this will start feeding our pipe now
            payload_builder = asyncio.create_task(asyncio_write_payload_and_close(payload_writer=payload_writer, **self._get_runner_args(job_def, options)))

            async with ReceptorControlAsync.create_ctx(options.control_socket_url) as rc:
                work_submission = await rc.submit_work_async('ansible-runner', payload=payload_reader, node=options.target_node)
                work_unit_id: str = work_submission['unitid']

                # FIXME: it's poor form to fire-and-forget in case there's a failure on the payload builder (which could theoretically result
                #  in a truncated or forever-blocked work submission), but we can't await before submission starts, since a large
                #  payload can't be completely written before consumption begins. Look into things like aiozipstream and a lighter-weight
                #  file-like that would allow for a more asyncio-native solution. Also think through how we'd recover a failure at this
                #  point, since the work has already been submitted with a potentially bad payload.
                await payload_builder

        result_socket: socket.socket
        sockfile: io.FileIO

        # BUG: setting return_sockfile False fails in receptorctl (access to misnamed instance attr trying to close the sockfile)
        async with ReceptorControlAsync.create_ctx(options.control_socket_url) as rc:
            result_socket, sockfile = await rc.get_work_results_async(work_unit_id, return_socket=True, return_sockfile=True)

        # mimic what the client would do if return_sockfile weren't broken
        sockfile.close()

        # set the socket to a nonblocking mode (zero timeout) so we can await data from it
        result_socket.setblocking(False)

        status_obj = AnsibleJobStatus(job_def)
        status_obj._executor_options = options
        self._running_job_info[status_obj] = _MeshJobInfo(unit_id=work_unit_id)

        # FIXME: small line-length limit is problematic with large stdout and zip payloads;
        #  the latter can be handled with an explicit chunked read + copy to disk until separator or
        #  firehose directly into a future aiozipstream. For now, it's just all getting pulled into memory.
        reader = asyncio.StreamReader(limit=2 ** 32, loop=loop)
        protocol = asyncio.StreamReaderProtocol(reader, loop=loop)

        await loop.connect_accepted_socket(lambda: protocol, result_socket)

        status_obj._stream_task = loop.create_task(self._stream_events(reader, status_obj))
        return status_obj


@dataclasses.dataclass
class _MeshJobInfo:
    unit_id: str
