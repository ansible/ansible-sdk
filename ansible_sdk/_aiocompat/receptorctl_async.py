# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations
from .proxy import AsyncProxy
from collections.abc import Iterator
from contextlib import asynccontextmanager
from receptorctl import ReceptorControl


class ReceptorControlAsync(ReceptorControl):
    # since the sync init can block on reading config, need an async-friendly factory method to background creation
    @classmethod
    async def create(cls, *args, **kwargs) -> ReceptorControlAsync:
        return await AsyncProxy.get_wrapped(ReceptorControlAsync)(*args, **kwargs)

    @classmethod
    @asynccontextmanager
    async def create_ctx(cls, *args, **kwargs) -> Iterator[ReceptorControlAsync]:
        rca = await ReceptorControlAsync.create(*args, **kwargs)
        try:
            yield rca
        finally:
            await rca.close_async()

    # FIXME: we can probably hack up a proxy for this pattern pretty cleanly too, but this works for now

    async def connect_async(self):
        return await AsyncProxy.get_wrapped(self.connect)()

    async def close_async(self):
        return await AsyncProxy.get_wrapped(self.close)()

    async def submit_work_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.submit_work)(*args, **kwargs)

    async def get_work_results_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.get_work_results)(*args, **kwargs)

    async def simple_command_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.simple_command)(*args, **kwargs)
