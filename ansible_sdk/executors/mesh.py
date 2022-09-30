from __future__ import annotations

import asyncio
import io
import os
import socket
import types

from ansible_sdk._aiocompat.receptorctl_async import ReceptorControlAsync
from ansible_sdk._aiocompat.runner_async import asyncio_write_payload_and_close
from ansible_sdk.executors import AnsibleBaseJobExecutor
from ansible_sdk.executors.subprocess import get_runner_args
from ansible_sdk import AnsibleJobDef, AnsibleJobStatus


class AnsibleMeshJobExecutor(AnsibleBaseJobExecutor):
    def __init__(self, local_socket_path: str, node: types.Optional[str] = None):
        # DECISION: define mesh access props only on init?
        self._socketpath = local_socket_path
        self._node = node

    async def submit_job(self, job_def: AnsibleJobDef) -> AnsibleJobStatus:
        loop = asyncio.get_running_loop()
        fds = os.pipe()
        with os.fdopen(fds[0], 'rb') as payload_reader, os.fdopen(fds[1], 'wb') as payload_writer:
            # FIXME: come up with a less brittle way to manage the pipe lifetime
            # start payload creation first by explicitly creating a task; this will start feeding our pipe now
            payload_builder = asyncio.create_task(asyncio_write_payload_and_close(payload_writer=payload_writer, **get_runner_args(job_def)))

            async with ReceptorControlAsync.create_ctx(self._socketpath) as rc:
                print('submitting work')
                work_submission = await rc.submit_work_async('ansible-runner', payload=payload_reader, node=self._node)
                print('work submitted')

                # FIXME: it's poor form to fire-and-forget in case there's a failure on the payload builder (which could theoretically result
                #  in a truncated or forever-blocked work submission), but we can't await before submission starts, since a large
                #  payload can't be completely written before consumption begins. Look into things like aiozipstream and a lighter-weight
                #  file-like that would allow for a more asyncio-native solution. Also think through how we'd recover a failure at this
                #  point, since the work has already been submitted with a potentially bad payload.
                await payload_builder
                print('payload builder completed ok')

        work_unit_id = work_submission['unitid']

        result_socket: socket.socket
        sockfile: io.FileIO

        # BUG: setting return_sockfile False fails in receptorctl (access to misnamed instance attr trying to close the sockfile)
        async with ReceptorControlAsync.create_ctx(self._socketpath) as rc:
            print('getting results')
            result_socket, sockfile = await rc.get_work_results_async(work_unit_id, return_socket=True, return_sockfile=True)
            print('got results')

        # mimic what the client would do if return_sockfile weren't broken
        sockfile.close()

        # set the socket to a nonblocking mode (zero timeout) so we can await data from it
        result_socket.setblocking(False)

        # FIXME: small line-length limit is problematic with large stdout and zip payloads;
        #  the latter can be handled with an explicit chunked read + copy to disk until separator or
        #  firehose directly into a future aiozipstream. For now, it's just all getting pulled into memory.
        reader = asyncio.StreamReader(limit=2 ** 32, loop=loop)
        protocol = asyncio.StreamReaderProtocol(reader, loop=loop)

        await loop.connect_accepted_socket(lambda: protocol, result_socket)

        status_obj = AnsibleJobStatus()
        status_obj._stream_task = loop.create_task(self._stream_events(reader, status_obj))
        return status_obj
