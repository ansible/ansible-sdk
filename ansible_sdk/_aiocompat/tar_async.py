# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations
from .proxy import AsyncProxy
from tarfile import TarFile


class TarFileAsync(TarFile):
    async def __aenter__(self, *args, **kwargs):
        return super().__enter__(*args, **kwargs)

    async def __aexit__(self, *args, **kwargs):
        return super().__exit__(*args, **kwargs)

    async def open_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.open)(*args, **kwargs)

    async def add_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.add)(*args, **kwargs)
