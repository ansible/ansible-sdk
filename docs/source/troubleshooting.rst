.. _sdk_troubleshooting:

Troubleshooting
===============

Ensure Python is >=3.8.

.. code-block:: bash

    $ python --version

Encountered: ``ModuleNotFoundError: No module named 'ansible_runner'``

Ansible SDK requires Ansible Runner to execute content.

#. Check that Ansible Runner is installed in your virtual environment.

  $ pip list | grep ansible_runner

#. Install Ansible Runner if necessary.

  $ pip install ansible-runner

Encountered: ``ValueError: private_data_dir path is either invalid or does not exist``

Change to the ``examples`` directory.