# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

import abc
import asyncio
import json as async_json

from ansible_sdk import AnsibleJobStatus, AnsibleJobDef
from ansible_sdk._aiocompat.proxy import AsyncProxy


# wrap these modules in an AsyncProxy so they're asyncio-friendly
async_json = AsyncProxy(async_json)


class AnsibleJobExecutorOptionsBase:
    pass


class AnsibleJobExecutorBase(abc.ABC):
    @abc.abstractmethod
    async def submit_job(self, job_def: AnsibleJobDef, options: AnsibleJobExecutorOptionsBase) -> AnsibleJobStatus:
        pass

    async def _stream_events(self, reader: asyncio.StreamReader, status_obj: AnsibleJobStatus) -> None:
        while True:
            line = await reader.readline()

            if not line:
                raise Exception('empty line received; unexpected EOF')

            data = await async_json.loads(line)

            if 'event' in data:
                status_obj._add_event(data)
            elif 'zipfile' in data:
                zf = await reader.readline()
                # FIXME: handle returned artifacts
                # FIXME: is this a bug?
                if b'{"eof": true}' in zf:
                    break
            elif 'eof' in data:
                break
            elif 'status' in data:
                # FIXME: propagate to status object
                pass
            else:
                pass
