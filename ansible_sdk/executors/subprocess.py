from __future__ import annotations

import asyncio
import os
import tempfile
import typing as t

from ansible_runner import interface as async_runner

from ansible_sdk._aiocompat.proxy import AsyncProxy
from ansible_sdk._aiocompat.runner_async import asyncio_write_payload_and_close
from ansible_sdk.executors import AnsibleBaseJobExecutor
from ansible_sdk import AnsibleJobDef, AnsibleJobStatus


# wrap these modules in an AsyncProxy so they're asyncio-friendly
async_runner = AsyncProxy(async_runner)


class AnsibleSubprocessJobExecutor(AnsibleBaseJobExecutor):
    # FIXME: define process control props only on init, no-args init and pass to submit_job, or ?
    def __init__(self):
        pass

    def _get_runner_args(self, job_def: AnsibleJobDef) -> dict[str, t.Any]:
        args = {
            'private_data_dir': job_def.data_dir,
            'playbook': job_def.playbook,
        }

        return args

    async def submit_job(self, job_def: AnsibleJobDef) -> AnsibleJobStatus:
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
        payload_builder = asyncio.create_task(asyncio_write_payload_and_close(payload_writer=payload_writer, **self._get_runner_args(job_def)))

        # print('starting worker')
        runner_args = self._get_runner_args(job_def)

        # FIXME: this prevents pollution of the original datadir for local runs and returned artifacts;
        runner_args['private_data_dir'] = tempfile.mkdtemp()

        # by using run_async, we can await
        await asyncio.create_task(async_runner.run_async(streamer='worker', _input=payload_reader, _output=results_writer, **runner_args))
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

        status_obj = AnsibleJobStatus()

        status_obj._event_streamer = loop.create_task(self._stream_events(reader, status_obj))

        return status_obj


class _AnsibleContainerJobExecutorBase(AnsibleSubprocessJobExecutor):
    _container_runtime_exe: str
    def __init__(self, image_ref: str):
        super().__init__()
        self._container_image_ref = image_ref

    def _get_runner_args(self, job_def: AnsibleJobDef):
        args = super()._get_runner_args(job_def)

        args['container_image'] = self._container_image_ref
        args['process_isolation'] = True
        args['process_isolation_executable'] = self._container_runtime_exe

        return args


# FIXME: define container control props only on init, no-args init and pass to submit_job, or ?
class AnsibleDockerJobExecutor(_AnsibleContainerJobExecutorBase):
    _container_runtime_exe = 'docker'

# FIXME: define container control props only on init, no-args init and pass to submit_job, or ?
class AnsiblePodmanJobExecutor(_AnsibleContainerJobExecutorBase):
    _container_runtime_exe = 'podman'
