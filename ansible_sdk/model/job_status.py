from __future__ import annotations

import asyncio

from collections.abc import AsyncIterator

from ansible_sdk import AnsibleJobEvent


class AnsibleJobStatus:
    def __init__(self):
        self._events = []
        self._complete = False
        self._event_streamer = None
        self._newevent = asyncio.Event()  # fired when a new event arrives to signal awaiting generators to proceed
        self._done = asyncio.Event()  # fired when the job is complete

    @property
    async def events(self) -> AsyncIterator[AnsibleJobEvent]:
        # HACK: this approach is ass, we can do better
        index = 0
        while True:
            # yield any events we haven't yet
            for ev in self._events[index:]:
                index += 1
                yield ev

            if self.done:
                return

            # chill, let either done or newevent wake us up
            await asyncio.wait([self._newevent.wait(), self._done.wait()], return_when=asyncio.FIRST_COMPLETED)

    def __await__(self):
        # make the job object itself awaitable for completion
        return self._done.wait().__await__()

    @property
    def done(self) -> bool:
        return self._done.is_set()
