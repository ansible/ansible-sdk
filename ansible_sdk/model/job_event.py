from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class AnsibleJobEvent:
    # FIXME: decide on our deserialized event shape/hierarchy
    #  Thoughts:
    #  * always make the original raw dict available
    #  * drop extra fields (?), since they'll always be available from --^
    #  * probably 1:1 dataclasses with core callback events

    pass


@dataclass
class BaseEvent:
    event: str
    uuid: str
    counter: int
    stdout: str
    start_line: int
    end_line: int
    runner_ident: str
    created: datetime
    _created: str = field(init=False, repr=False)

    @property
    def created(self) -> datetime:
        return self._created

    @created.setter
    def created(self, value: str) -> None:
        self._created = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")


@dataclass
class VerboseEvent(BaseEvent):
    pass


@dataclass
class PlaybookOnStartEvent(BaseEvent):
    pid: int = 0
    event_data: BaseEventData = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = BaseEventData(**value)


@dataclass
class PlaybookOnPlayStartEvent(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: PlayEventData = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = PlayEventData(**value)


@dataclass
class PlaybookOnTaskStartEvent(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: dict = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = TaskEventData(**value)


@dataclass
class RunnerOnStartEvent(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: dict = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = RunnerOnStartEventData(**value)


@dataclass
class RunnerOnOKEvent(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: dict = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = RunnerOnOKEventData(**value)


@dataclass
class RunnerOnAsyncPollEvent(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: dict = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = RunnerOnAsyncPollEventData(**value)


@dataclass
class RunnerOnAsyncOKEvent(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: dict = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = RunnerOnAsyncOKEventData(**value)


@dataclass
class PlaybookOnStats(BaseEvent):
    pid: int = 0
    parent_uuid: str = ""
    event_data: dict = field(default_factory=dict)
    _event_data: str = field(init=False, repr=False)

    @property
    def event_data(self):
        return self._event_data

    @event_data.setter
    def event_data(self, value: dict) -> None:
        self._event_data = PlaybookOnStatsEventData(**value)


@dataclass
class BaseEventData:
    playbook: str
    playbook_uuid: str
    uuid: str


@dataclass
class PlayEventData(BaseEventData):
    play: str = ""
    play_uuid: str = ""
    play_pattern: str = ""
    name: str = ""
    pattern: str = ""


@dataclass
class TaskEventData(BaseEventData):
    play: str = ""
    play_uuid: str = ""
    play_pattern: str = ""
    name: str = ""
    task: str = ""
    task_uuid: str = ""
    task_action: str = ""
    task_args: str = ""
    task_path: str = ""
    is_conditional: bool = False
    resolved_action: str = ""


@dataclass
class RunnerOnStartEventData(BaseEventData):
    play: str = ""
    play_uuid: str = ""
    play_pattern: str = ""
    name: str = ""
    task: str = ""
    task_uuid: str = ""
    task_action: str = ""
    task_args: str = ""
    task_path: str = ""
    host: str = ""
    resolved_action: str = ""


@dataclass
class RunnerOnOKEventData(BaseEventData):
    play: str = ""
    play_uuid: str = ""
    play_pattern: str = ""
    name: str = ""
    task: str = ""
    task_uuid: str = ""
    task_action: str = ""
    task_args: str = ""
    task_path: str = ""
    host: str = ""
    remote_addr: str = ""
    res: dict = field(default_factory=dict)
    start: str = ""
    end: str = ""
    duration: str = ""
    event_loop: str = ""
    resolved_action: str = ""


@dataclass
class RunnerOnAsyncPollEventData(BaseEventData):
    play: str = ""
    play_uuid: str = ""
    play_pattern: str = ""
    name: str = ""
    task: str = ""
    task_uuid: str = ""
    task_action: str = ""
    task_args: str = ""
    task_path: str = ""
    host: str = ""
    res: dict = field(default_factory=dict)
    jid: str = ""


@dataclass
class RunnerOnAsyncOKEventData(BaseEventData):
    play: str = ""
    play_uuid: str = ""
    play_pattern: str = ""
    name: str = ""
    task: str = ""
    task_uuid: str = ""
    task_action: str = ""
    task_args: str = ""
    task_path: str = ""
    host: str = ""
    res: dict = field(default_factory=dict)
    jid: str = ""


@dataclass
class PlaybookOnStatsEventData(BaseEventData):
    changed: dict = field(default_factory=dict)
    dark: dict = field(default_factory=dict)
    failures: dict = field(default_factory=dict)
    ignored: dict = field(default_factory=dict)
    ok: dict = field(default_factory=dict)
    processed: dict = field(default_factory=dict)
    rescued: dict = field(default_factory=dict)
    skipped: dict = field(default_factory=dict)
    artifact_data: dict = field(default_factory=dict)
    uuid: str = ""
