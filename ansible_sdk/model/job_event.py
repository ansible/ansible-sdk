from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnsibleJobStatusEvent:
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
