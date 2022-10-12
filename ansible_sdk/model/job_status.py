from __future__ import annotations

import asyncio
import typing as t

from .job_event import AnsibleJobStatusEvent
from .job_def import AnsibleJobDef


# FIXME: make kw_only+frozen dataclass, expose dataclasses.replace for mutated copies, expose a place for private mutable data
class AnsibleJobStatus:
    """
    Status object for monitoring running/completed jobs.
    """
    def __init__(self, job_def: AnsibleJobDef):
        self._events = []
        self._events_appended = asyncio.Event()
        self._stream_task = None
        self._executor_options = None
        self._runner_status = None  # stash the runner status object here and consult it on completion for errors, etc
        self._job_def = job_def

    def _add_event(self, evt: AnsibleJobStatusEvent):
        self._events.append(evt)
        # pulse the appended event to awaken any blocked iterators
        self._events_appended.set()
        self._events_appended.clear()

    def drop_event(self, evt: AnsibleJobStatusEvent):
        """
        Request discard of event data that is no longer needed.

        :param evt: The returned event object to be discarded
        """
        self._events[self._events.index(evt)] = None

    @property
    async def events(self) -> t.AsyncIterator[AnsibleJobStatusEvent]:
        """
        Async iterator to enumerate events from this job. Events are yielded live while the job is running; the
        iterator will not complete until the job has completed or failed. In cases of job failure or cancellation,
        the iterator will raise an exception with the appropriate detail.

        :return: a live iterator of ``AnsibleJobStatusEvent`` data for this job
        """
        cur_ev_idx = 0
        streaming_complete = False

        while True:
            if cur_ev_idx >= len(self._events):
                if streaming_complete:
                    return
                # ran out of events, but more are probably coming...
                new_events_waiter = asyncio.create_task(self._events_appended.wait())
                done, pending = await asyncio.wait([new_events_waiter, self._stream_task], return_when=asyncio.FIRST_COMPLETED)
                if new_events_waiter in done:  # new events have been appended, just continue iteration...
                    continue
                if self._stream_task in done:
                    self._stream_task.result()  # this will raise an error to the caller if the stream task failed
                    streaming_complete = True
                    continue  # yield remaining events, if any, then exit

            ev = self._events[cur_ev_idx]
            cur_ev_idx += 1
            if ev:
                yield ev

    @property
    async def stdout_lines(self) -> t.AsyncIterator[str]:
        """
        Async iterator to enumerate lines of display output text from this job. Text lines are yielded live while the
        job is running; the iterator will not complete until the job has completed or failed. In cases of job failure or
        cancellation, the iterator will raise an exception with the appropriate detail.

        :return: an iterator of lines of display output text from the Ansible job
        """
        async for ev in self.events:
            # normalize some runner oddities
            if 'stdout' in ev:
                new_data = ev['stdout']
                if not new_data:
                    continue
                if new_data[0] == '\n':
                    new_data = new_data[1:]
                yield new_data

    def cancel(self):
        """
        Request cancellation of a running job by the executor. On successful cancellation, ``CancelledError`` will be on
        raised on running iterators and on any awaiters of this job object.
        """
        # currently using the stream task's cancel state as the runner callback cancellation callback "answer"
        if self._stream_task and not self._stream_task.cancelled():
            self._stream_task.cancel()
        if self._runner_status:
            self._runner_status._input.close()
            self._runner_status._output.close()

    def __await__(self):
        """
        Await completion of this job (eg, ``await job_status_obj``)
        """
        yield from self._stream_task
        self._stream_task.result()
