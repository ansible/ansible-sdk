.. _install_ansible_sdk:

Installing Ansible SDK
======================

Ansible SDK requires the following software:

* Python version 3.8 or later
* `Ansible <https://docs.ansible.com/ansible-core/devel/#>`_
* `Ansible Runner <https://ansible-runner.readthedocs.io/en/stable/>`_
* `Receptorctl <https://receptor.readthedocs.io/en/latest/index.html#installation>`_

Ansible SDK is currently available from source at `github <https://github.com/ansible/ansible-sdk>`_::

    $ git clone git://github.com/ansible/ansible-sdk

Releases will be available for download from the `releases page <https://github.com/ansible/ansible-sdk/releases>`_

To `pip` install Ansible SDK:

#. Open a terminal in the ``ansible-sdk`` directory.
#. Create and activate a Python3 virtual environment.

   .. code-block:: bash

       $ virtualenv env
       $ source env/bin/activate

#. Install the required Python packages in your virtual environment.

   .. code-block:: bash

       $ pip install ansible-core
       $ pip install ansible-runner
       $ pip install receptorctl

#. Install Ansible SDK.

   .. code-block:: bash

       $ pip install -e .
