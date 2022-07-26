from __future__ import annotations

import typing
from dataclasses import dataclass


@dataclass
class AnsibleJobDef:
    # currently analogue to runner's private_data_dir; do we want to construct this ourselves?
    data_dir: str
    # relative path to playbook in data_dir or FQCN
    playbook: str
    inventory: typing.Optional[typing.Union[str, list[str]]] = None  # FUTURE: high-level inventory types?
