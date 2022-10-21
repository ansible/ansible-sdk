Ansible SDK for Python
======================

The Ansible SDK provides lightweight Python library for dispatching and live-monitoring
Ansible tasks, roles, and playbooks from the product or project.

Dispatching of jobs can be local to the machine you are running your python application from or over Ansible Mesh using the receptor integrations.

# Demo App to show how you can use the SDK in real use case - https://github.com/ansible/ansible_sdk_demo


## Releases and maintenance

TBD

## Ansible version compatibility

TBD

## Installation

You can follow the installation guide specified in [`docs`](https://github.com/ansible/ansible-sdk/tree/main/docs/source/install.rst).

### Required Python libraries and SDKs

The Ansible-SDK depends on Python 3.8+, Ansible Core, Ansible Runner and other third party libraries:

* [`ansible-core`](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* [`asyncio`](https://docs.python.org/3/library/asyncio.html)
* [`ansible-runner`](https://ansible-runner.readthedocs.io/en/stable/install/)
* [`receptorctl`](https://receptor.readthedocs.io/en/latest/#installation)


## Testing and Development

Red Hat Enterprise Linux - Install Ansible-SDK and dependecies directly on/into a RHEL Virtual machine.
MacOS - Install PODMAN using BREW, and pull the RHEL8 image, ssh to that and follow the RHEL instructions above.

## Communication

TBD

## License

TBD

See [LICENSE](LICENSE.md) to see the full text.
