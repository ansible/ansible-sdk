from __future__ import annotations

import asyncio


class _JobStatusIterator:
    def __init__(self, parent: AnsibleJobStatus):
        self._parent = parent
        self._current = 0

    def __iter__(self) -> _JobStatusIterator:
        return self

    async def __next__(self) -> AnsibleJobStatusEvent:
        while True:
            if len(self.parent._events) <= self.current:
                await asyncio.wait([self.parent._newevent, self.parent.stream_task], return_when=asyncio.FIRST_COMPLETED)

            if self.parent._stream_task.done():
                self.parent._stream_task.result()

                raise StopIteration()

            evt = self._events[self._current]
            self._current += 1
            if evt:
                return evt


class AnsibleJobStatus:
    def __init__(self):
        self._events = []
        self._events_appended = asyncio.Event()
        self._stream_task = None

    async def add_event(self, evt: AnsibleJobStatusEvent):
        self._events.append(evt)
        self._events_appended.set()
        self._events_appended.clear()

    def stream_task_result(self):
        await self._stream_task

        return self._stream_task.result()

    def drop_event(self, evt: AnsibleJobStatusEvent):
        self._events[self._events.index(evt)] = None

    @property
    def events(self):
        return _JobStatusIterator(self)

