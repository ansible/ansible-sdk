# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

import asyncio

from functools import partial, wraps
from types import ModuleType


# hacky threadpool proxy wrapper around modules, adapted from http://zderadicka.eu/asyncio-proxy-for-blocking-functions/
class AsyncProxy(object):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __getattr__(self, name):
        attrval = getattr(self._wrapped, name)

        # wrap submodules
        if isinstance(attrval, ModuleType):
            return AsyncProxy(attrval)

        # just return anything that's not a callable
        if not callable(attrval):
            return attrval

        # FIXME: cache these?
        return self.get_wrapped(attrval)

    @classmethod
    def get_wrapped(cls, thing):
        # FIXME: cache these?
        @wraps(thing)
        async def _inner(*args, **kwargs):
            loop = kwargs.pop('loop', asyncio.get_running_loop())
            executor = kwargs.get('executor', None)
            f = partial(thing, *args, **kwargs)
            return await loop.run_in_executor(executor, f)

        return _inner
