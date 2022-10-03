from __future__ import annotations

import asyncio
from .job_event import AnsibleJobStatusEvent


class _JobStatusIterator:
    def __init__(self, parent: AnsibleJobStatus):
        self._parent = parent
        self._current = 0

    def __aiter__(self) -> _JobStatusIterator:
        return self

    async def __anext__(self) -> AnsibleJobStatusEvent:
        while True:
            if len(self._parent._events) <= self._current:
                await asyncio.wait([asyncio.create_task(self._parent._events_appended.wait()), self._parent._stream_task], return_when=asyncio.FIRST_COMPLETED)

            if self._parent._stream_task.done():
                # Reraises exception of the stream task if there is any.
                self._parent._stream_task.result()

                raise StopAsyncIteration()

            evt = self._parent._events[self._current]
            self._current += 1
            if evt:
                return evt


class AnsibleJobStatus:
    def __init__(self):
        self._events = []
        self._events_appended = asyncio.Event()
        self._stream_task = None
        self._executor_options = None

    async def add_event(self, evt: AnsibleJobStatusEvent):
        self._events.append(evt)
        self._events_appended.set()
        self._events_appended.clear()

    @property
    async def stream_task_result(self):
        await self._stream_task

        return self._stream_task.result()

    def drop_event(self, evt: AnsibleJobStatusEvent):
        self._events[self._events.index(evt)] = None
        # FIXME: await self._event_streamer here as well to propagate any exceptions?

    @property
    def events(self):
        return _JobStatusIterator(self)
