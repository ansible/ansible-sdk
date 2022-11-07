# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

import typing as t
from .._util.dataclass_compat import field, dataclass, _DataclassReplaceMixin


@dataclass(frozen=True, kw_only=True)
class AnsibleJobDef(_DataclassReplaceMixin):
    """Common Ansible job definition values"""
    # currently analogue to runner's private_data_dir; do we want to construct this ourselves?
    data_dir: str
    """Path to a directory structure containing the Ansible project content and inventory."""
    # relative path to playbook in data_dir or FQCN
    playbook: str
    """Relative path or FQCN of a playbook to run under ``data_dir``"""
    inventory: t.Optional[t.Union[str, list[str]]] = None  # FUTURE: high-level inventory types?
    """Relative path to inventory file(s) or directory under ``data_dir``, analogue to Ansible's ``-i`` option"""
    extra_vars: dict[str, t.Any] = field(default_factory=dict)
    """Dictionary of variables for highest precedence level, analogue to Ansible's ``-e`` option"""
    verbosity: t.Optional[int] = None  # None or 1-5
    """None for default verbosity or 1-5, equivalent to Ansible's ``-v`` options"""
