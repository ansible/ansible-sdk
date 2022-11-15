# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

import asyncio
import functools
import os
import tempfile
import typing as t

from ansible_runner import interface as async_runner

from .._aiocompat.proxy import AsyncProxy
from .._aiocompat.runner_async import asyncio_write_payload_and_close
from ..executors.base import AnsibleJobExecutorBase, AnsibleJobExecutorOptionsBase
from .._util import dataclass_compat as dataclasses
from .. import AnsibleJobDef, AnsibleJobStatus

# wrap these modules in an AsyncProxy so they're asyncio-friendly
async_runner = AsyncProxy(async_runner)


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsibleSubprocessJobOptions(AnsibleJobExecutorOptionsBase):
    """
    Job Options for AnsibleSubprocessJobExecutor
    """


class AnsibleSubprocessJobExecutor(AnsibleJobExecutorBase):
    """
    Basic Subprocess Job Executor
    """
    def _get_runner_args(self, job_def: AnsibleJobDef, options: AnsibleSubprocessJobOptions) -> dict[str, t.Any]:
        args = {
            'private_data_dir': job_def.data_dir,
            'playbook': job_def.playbook,
            'artifacts_handler': None,
            'extravars': job_def.extra_vars,
            'verbosity': job_def.verbosity,
            'limit': job_def.limit,
        }

        return args

    def _is_cancelled(self, job_status: AnsibleJobStatus) -> bool:
        return job_status._stream_task.cancelled()

    async def submit_job(self, job_def: AnsibleJobDef, options: AnsibleSubprocessJobOptions) -> AnsibleJobStatus:
        loop = asyncio.get_running_loop()

        fds = os.pipe()
        # FIXME: deterministic cleanup (need to offload/chain with the end of the runner invocation; can't be sure when we can close otherwise)
        payload_reader = os.fdopen(fds[0], 'rb')
        payload_writer = os.fdopen(fds[1], 'wb')

        result_fds = os.pipe()
        # FIXME: deterministic cleanup
        results_reader = os.fdopen(result_fds[0], 'rb')
        results_writer = os.fdopen(result_fds[1], 'wb')

        # FIXME: come up with a less brittle way to manage the pipe lifetime
        # start payload creation first by explicitly creating a task; this will start feeding our pipe now
        payload_builder = asyncio.create_task(asyncio_write_payload_and_close(payload_writer=payload_writer, **self._get_runner_args(job_def, options)))

        # print('starting worker')
        runner_args = self._get_runner_args(job_def, options)

        # FIXME: this prevents pollution of the original datadir for local runs and returned artifacts;
        runner_args['private_data_dir'] = tempfile.mkdtemp()

        status_obj = AnsibleJobStatus(job_def)

        cancel_partial = functools.partial(self._is_cancelled, status_obj)

        # by using run_async, we can await
        runner_status = await asyncio.create_task(async_runner.run_async(
            streamer='worker',
            _input=payload_reader,
            _output=results_writer,
            cancel_callback=cancel_partial,
            **runner_args))
        # print('worker running')

        # FIXME: it's poor form to fire-and-forget in case there's a failure on the payload builder (which could theoretically result
        #  in a truncated or forever-blocked work submission), but we can't await before submission starts, since a large
        #  payload can't be completely written before consumption begins. Look into things like aiozipstream and a lighter-weight
        #  file-like that would allow for a more asyncio-native solution. Also think through how we'd recover a failure at this
        #  point, since the work has already been submitted with a potentially bad payload.
        # print('awaiting payload builder')
        await payload_builder
        # print('payload builder completed ok')

        # FIXME: small line-length limit is problematic with large stdout and zip payloads;
        #  the latter can be handled with an explicit chunked read + copy to disk until separator or
        #  firehose directly into a future aiozipstream. For now, it's just all getting pulled into memory.
        reader = asyncio.StreamReader(limit=2 ** 32, loop=loop)
        protocol = asyncio.StreamReaderProtocol(reader, loop=loop)

        await loop.connect_read_pipe(lambda: protocol, results_reader)

        status_obj._runner_thread = runner_status[0]  # set before starting the event streamer task, as it may use it
        status_obj._runner_status = runner_status[1]  # set before starting the event streamer task, as it may use it
        status_obj._executor_options = options
        status_obj._stream_task = loop.create_task(self._stream_events(reader, status_obj))
        return status_obj

    async def _stream_events(self, reader: asyncio.StreamReader, status_obj: AnsibleJobStatus) -> None:
        try:
            await super()._stream_events(reader=reader, status_obj=status_obj)
        finally:
            # force-close the runner IO streams to prevent blocked write deadlock on runner thread in cancel/error cases
            # (this should cause runner to error out writing to those streams instead of blocking forever)
            try:
                status_obj._runner_status._input.close()
            except Exception:
                pass
            try:
                status_obj._runner_status._output.close()
            except Exception:
                pass

        # we only want to do this part if we're not being cancelled
        status_obj._runner_thread.join(3)
        if status_obj._runner_thread.is_alive():
            # FIXME: warning/error?
            pass

        if status_obj._runner_status.rc != 0:
            # FIXME: better error
            raise Exception(f'job failed with exit code {status_obj._runner_status.rc}')


@dataclasses.dataclass(frozen=True, kw_only=True)
class _AnsibleContainerJobOptions(AnsibleJobExecutorOptionsBase):
    container_image_ref: str


OptionsT = t.TypeVar("OptionsT", bound=_AnsibleContainerJobOptions)


class _AnsibleContainerJobExecutorBase(AnsibleSubprocessJobExecutor, t.Generic[OptionsT]):
    _container_runtime_exe: str

    def _get_runner_args(self, job_def: AnsibleJobDef, options: _AnsibleContainerJobOptions):
        args = super()._get_runner_args(job_def, AnsibleSubprocessJobOptions())

        args['container_image'] = options.container_image_ref
        args['process_isolation'] = True
        args['process_isolation_executable'] = self._container_runtime_exe

        return args

    async def submit_job(self, job_def: AnsibleJobDef, options: OptionsT) -> AnsibleJobStatus:
        return await super().submit_job(job_def, options)


class AnsibleDockerJobOptions(_AnsibleContainerJobOptions):
    """
    Job Options for AnsibleDockerJobExecutor

    :param container_image_ref: Docker-style image reference, eg ``quay.io/ansible/ansible-runner:latest``
    """


class AnsibleDockerJobExecutor(_AnsibleContainerJobExecutorBase[AnsibleDockerJobOptions]):
    _container_runtime_exe = 'docker'


class AnsiblePodmanJobOptions(_AnsibleContainerJobOptions):
    """
    Job Options for AnsiblePodmanJobExecutor

    :param container_image_ref: Docker-style image reference, eg ``quay.io/ansible/ansible-runner:latest``
    """


class AnsiblePodmanJobExecutor(_AnsibleContainerJobExecutorBase[AnsiblePodmanJobOptions]):
    _container_runtime_exe = 'podman'
