# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from __future__ import annotations

import typing as t
from .._util.dataclass_compat import field, dataclass, _DataclassReplaceMixin


@dataclass(frozen=True, kw_only=True)
class AnsibleJobDef(_DataclassReplaceMixin):
    """
    Common Ansible job definition values

    :param data_dir: path to a directory structure containing the Ansible project content and inventory.
    :param playbook: relative path or FQCN of a playbook to run under ``data_dir``
    :param inventory: relative path to inventory file(s) or directory under ``data_dir``, analogue to Ansible's ``-i`` option
    :param extra_vars: dictionary of variables for highest precedence level, analogue to Ansible's ``-e`` option
    :param env_vars: Environment variables to be used when running Ansible.
    :param verbosity: None for default verbosity or 1-5, equivalent to Ansible's ``-v`` options
    :param limit: Matches Ansible's ``--limit`` parameter to further constrain the inventory to be used
    :param ident: The run identifier for this invocation of Runner. Will be used to create and name
                  the artifact directory holding the results of the invocation.
    :param forks: Control Ansible parallel concurrency
    :param module: The module that will be invoked in ad-hoc mode by runner when executing Ansible.
    :param module_args: The module arguments that will be supplied to ad-hoc mode.
    :param host_pattern: The host pattern to match when running in ad-hoc mode.
    :param timeout: The timeout value in seconds that will be passed to ``subprocess`` invocation while executing
                    command. It the timeout is triggered it will force cancel the execution.
    :param role: Name of the role to execute.
    :param roles_path: Directory or list of directories to assign to ANSIBLE_ROLES_PATH
    :param metrics_output_path: A path to directory to collect metrics
    """
    # currently analogue to runner's private_data_dir; do we want to construct this ourselves?
    data_dir: str
    # relative path to playbook in data_dir or FQCN
    playbook: str
    limit: str | None = None
    ident: str | None = None
    forks: int | None = None
    module: str | None = None
    module_args: str | None = None
    host_pattern: str | None = None
    inventory: str | list[str] | None = None  # FUTURE: high-level inventory types?
    env_vars: dict[str, t.Any] = field(default_factory=dict)
    extra_vars: dict[str, t.Any] = field(default_factory=dict)
    verbosity: int | None = None  # None or 1-5
    timeout: int | None = None
    role: str | None = None
    roles_path: str | list[str] | None = None
    metrics_output_path: str | None = None
