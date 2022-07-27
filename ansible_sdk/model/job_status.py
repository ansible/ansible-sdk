from __future__ import annotations

import asyncio

from collections.abc import AsyncIterator

from ansible_sdk import AnsibleJobEvent
from ansible_sdk.model.job_event import (
    VerboseEvent,
    PlaybookOnPlayStartEvent,
    PlaybookOnStartEvent,
    PlaybookOnTaskStartEvent,
    PlaybookOnStats,
)
from ansible_sdk.model.job_event import (
    RunnerOnAsyncOKEvent,
    RunnerOnAsyncPollEvent,
    RunnerOnOKEvent,
    RunnerOnStartEvent,
)


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
                if ev["event"] == "verbose":
                    yield VerboseEvent(**ev)
                elif ev["event"] == "playbook_on_start":
                    yield PlaybookOnStartEvent(**ev)
                elif ev["event"] == "playbook_on_play_start":
                    yield PlaybookOnPlayStartEvent(**ev)
                elif ev["event"] == "playbook_on_task_start":
                    yield PlaybookOnTaskStartEvent(**ev)
                elif ev["event"] == "runner_on_start":
                    yield RunnerOnStartEvent(**ev)
                elif ev["event"] == "runner_on_ok":
                    yield RunnerOnOKEvent(**ev)
                elif ev["event"] == "runner_on_async_poll":
                    yield RunnerOnAsyncPollEvent(**ev)
                elif ev["event"] == "runner_on_async_ok":
                    yield RunnerOnAsyncOKEvent(**ev)
                elif ev["event"] == "playbook_on_stats":
                    yield PlaybookOnStats(**ev)
                else:
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

