.. _running_mesh_jobs:

****************************
Running automation mesh jobs
****************************

Automation mesh is a scalable cluster of Receptor nodes that execute Ansible playbooks.
Ansible SDK lets you invoke jobs directly on nodes in the automation mesh.

Prerequisites
=============

* Install Ansible SDK and required software.
* Install Ansible `Receptor <https://github.com/ansible/receptor>`_.

Setting up a local automation mesh
==================================

Create a locally running cluster of Receptor nodes with configuration files in the ``examples/receptor_config`` directory:

#. Open your ``/etc/hosts`` file for editing.
#. Add the following entries to your ``hosts`` file:

   .. code-block::

      127.0.0.1 foo.example.com
      127.0.0.1 bar.example.com
      127.0.0.1 baz.example.com

#. Open a terminal and start the first Receptor node.
   
   a. Activate your virtual environment for Ansible SDK.

      .. code-block:: bash

         $ source env/bin/activate

   b. Start a node with the ``foo.yml`` configuration.

      .. code-block:: bash

         $ receptor --config foo.yml

#. Open a new terminal and start the second Receptor node.
   
   a. Activate your virtual environment for Ansible SDK.
   b. Start a node with the ``bar.yml`` configuration.

      .. code-block:: bash

         $ receptor --config bar.yml

#. Open a new terminal and start the third Receptor node.
   
   a. Activate your virtual environment for Ansible SDK.
   b. Start a node with the ``baz.yml`` configuration.

      .. code-block:: bash

         $ receptor --config baz.yml

#. Verify that the automation mesh is running.
    
   .. code-block:: bash

      $ receptorctl --socket /tmp/bar.sock status

Invoking automation mesh jobs
=============================

Use Ansible SDK to run a playbook on automation mesh as follows:

#. Open a terminal and change to the ``examples`` directory.
#. Run the following command:

   .. code-block:: bash

      $ python example_mesh_job.py 

The ``example_mesh_job.py`` program has a ``main()`` function that connects to the Receptor nodes and runs the ``examples/datadir/project/pb.yml`` playbook.
You can verify the job is successful when Ansible SDK prints the following to stdout:

.. code-block:: bash

   submitting work
   work submitted
   payload builder completed ok
   getting results
   got results
   waiting for jobs
   job done: True, has <x> events

Troubleshooting
===============

If you encounter issues with this scenario, troubleshoot as follows:

- Check your Ansible SDK installation. See :ref:`install_ansible_sdk`.
- Ensure you installed Ansible and Ansible Runner.
- Ensure Receptor is installed correctly.
- Ensure ``receptorctl`` is installed correctly.
- Ensure your ``/etc/hosts`` file contains entries for each local Receptor node.
- Ensure you run each Receptor node in a separate terminal in the Ansible SDK virtual environment.
