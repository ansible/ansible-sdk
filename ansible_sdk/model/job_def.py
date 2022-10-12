from __future__ import annotations

import typing as t
from .._util.dataclass_compat import field, dataclass, _DataclassReplaceMixin


@dataclass(frozen=True, kw_only=True)
class AnsibleJobDef(_DataclassReplaceMixin):
    # currently analogue to runner's private_data_dir; do we want to construct this ourselves?
    data_dir: str
    # relative path to playbook in data_dir or FQCN
    playbook: str
    inventory: t.Optional[t.Union[str, list[str]]] = None  # FUTURE: high-level inventory types?
    extra_vars: dict[str, t.Any] = field(default_factory=dict)
    verbosity: t.Optional[int] = None  # None or 1-5
