************************************
Executing Mesh Job using Ansible SDK
************************************

.. contents::
   :local:

Introduction
============

This guide will show you how to utilize Ansible SDK to invoke jobs using `Receptor <https://github.com/ansible/receptor>`_.

Scenario requirements
=====================

* Software

    * `Receptor <https://github.com/ansible/receptor>`_

    * `Receptorctl <https://receptor.readthedocs.io/en/latest/index.html#installation>`_

* Hardware

    * N/A

* Access / Credentials

    * N/A


Caveats
=======

- N/A

Example description
===================

In order to run this example, we are assuming that you have only one machine running Ansible, Ansible Runner and Receptor

* Start three nodes using the configuration files found in ``examples/receptor_config`` directory.
  Use individual terminals for each nodes

.. code-block:: bash

    # (from the first terminal)
    $ receptor --config foo.yml 
    
.. code-block:: bash

    # (from the second terminal)
    $ receptor --config bar.yml 
    
.. code-block:: bash

    # (from the third terminal)
    $ receptor --config baz.yml 

* Check if all the nodes are up and running using ``receptorctl`` command - 
    
.. code-block:: bash

    # (from the fourth terminal)
    $ receptorctl --socket /tmp/bar.sock status

* Let us invoke ``examples/example_mesh_job.py`` - 

.. code-block:: bash

    # (from the fifth terminal)
    $ python example_mesh_job.py 

What to expect
--------------

Ansible SDK will use underlying receptor to invoke job and present the output to the stdout

Troubleshooting
---------------

If your something fails:

- Check if receptor is installed correctly
- Check if receptorctl is installed correctly
- Check if Ansible SDK is installed correctly 
