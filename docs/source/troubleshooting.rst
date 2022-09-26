.. _sdk_troubleshooting:

Troubleshooting
===============

Resolve common issues with Ansible SDK setup and usage.

Ensure your Python version is >=3.8 before you start any other troubleshooting steps.

.. code-block:: bash

    $ python --version

**Encountered:** ``ModuleNotFoundError: No module named 'ansible_runner'``

Resolution:

#. Check that Ansible Runner is installed in your virtual environment.

   .. code-block:: bash
        
      $ pip list | grep ansible_runner

#. Install Ansible Runner if necessary.

   .. code-block:: bash
    
      $ pip install ansible-runner

**Encountered:** ``ValueError: private_data_dir path is either invalid or does not exist``

Resolution:

* Change to the ``examples`` directory if you are running one of the Ansible SDK quickstart examples.
  The quickstart examples use the contents of the ``datadir`` folder, which maps to the ``private_data_dir`` path.

* Ensure the ``private_data_dir`` directory contains all the artifacts and metadata for your jobs.
  Ansible Runner requires you to put all playbooks, inventory files, and so on in the ``private_data_dir`` directory.
  This is the directory that you specify in your Ansible job definition with the ``AnsibleJobDef('datadir', 'pb.yml')`` object.