from __future__ import annotations

import typing
from dataclasses import dataclass


@dataclass
class AnsibleJob:
    """Ansible Job Object Type mappings

    Attributes:
        data_dir (str): Maps to runner's private_data_dir
        playbook (str): Relative path to playbook in data_dir directory
        inventory (optional): An optional inventory object, defaults to None
    """
    data_dir: str
    # relative path to playbook in data_dir or FQCN
    playbook: str
    inventory: typing.Optional[typing.Union[str, list[str]]] = None  # FUTURE: high-level inventory types?
