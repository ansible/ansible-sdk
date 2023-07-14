# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

from csv import DictWriter

from .proxy import AsyncProxy


class CSVAsync(DictWriter):
    async def writeheader_async(self):
        return await AsyncProxy.get_wrapped(self.writeheader)()

    async def writerow_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.writerow)(*args, **kwargs)

    async def writerows_async(self, *args, **kwargs):
        return await AsyncProxy.get_wrapped(self.writerows)(*args, **kwargs)
