from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnsibleJobStatusEvent:
    """
    Container object for various Ansible events.

    :param event: name of the event type
    :param event_data: dictionary of the raw event data
    :param stdout: display text output associated with this event (if any)
    """
    uuid: str
    parent_uuid: str
    counter: int
    stdout: str
    start_line: int
    end_line: int
    event: str
    event_data: dict
    pid: int
    created: str
