from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AnsibleJobEvent:
    # FIXME: decide on our deserialized event shape/hierarchy
    #  Thoughts:
    #  * always make the original raw dict available
    #  * drop extra fields (?), since they'll always be available from --^
    #  * probably 1:1 dataclasses with core callback events

    pass
