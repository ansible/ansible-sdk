# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnsibleJobStatusEvent:
    """Container object for various Ansible events."""
    uuid: str
    parent_uuid: str
    counter: int
    stdout: str
    """Display text output associated with this event (if any)"""
    start_line: int
    end_line: int
    event: str
    """Name of the event type"""
    event_data: dict
    """Dictionary of the raw event data"""
    pid: int
    created: str
