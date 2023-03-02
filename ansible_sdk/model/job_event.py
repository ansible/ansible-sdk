# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)
from __future__ import annotations

import typing as t

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass
class AnsibleJobEvent(Mapping):
    """
    Container object for various Ansible events.

    :param name: name of the event type
    :param raw_event_data: dictionary of the raw event data
    :param stdout: display text output associated with this event (if any)
    """
    name: str
    raw_event_data: dict[str, t.Any]

    # static no-op impls to keep type-checking happy; we'll patch these during construction
    # FIXME: these shouldn't be necessary to truly implement
    def __getitem__(self, item):
        return self.raw_event_data.__getitem__(item)

    def __iter__(self):
        return self.raw_event_data.__iter__()

    def __len__(self):
        return self.raw_event_data.__len__()

    # def __post_init__(self):
    #     # patch event dict mapping impl methods directly through
    #     self.__getitem__ = self.raw_event_data.__getitem__
    #     self.__iter__ = self.raw_event_data.__iter__
    #     self.__len__ = self.raw_event_data.__len__
