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
            # print(f'decoded json, got keys {data.keys()}')

            # print(f'got a line of length {len(line)}')

            if 'event' in data:
                # print(f'appending event of type {data["event"]}')
                status_obj._add_event(data)
            elif 'zipfile' in data:
                # print(f'zipfile coming, {data["zipfile"]} bytes expected')
                zf = await reader.readline()
                # FIXME: handle returned artifacts
                # print(f'received {len(zf)} raw bytes (and discarded)')

                # FIXME: is this a bug?
                if b'{"eof": true}' in zf:
                    # print('eof was embedded in zip line, done with stream_events')
                    break
            elif 'eof' in data:
                # print('got eof, done with stream_events')
                break
            elif 'status' in data:
                # FIXME: propagate to status object
                # print(f'got status blob: {line[0:100]} ... ')
                pass
            else:
                # print('\n\n*** unexpected data... ***\n\n')
                pass
