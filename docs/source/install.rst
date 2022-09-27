.. _install_ansible_sdk:

Installing Ansible SDK
======================

Ansible SDK requires Python >= 3.8. Currently, it can be installed via source tree

From source
-----------

Check out the source code from `github <https://github.com/ansible/ansible-sdk>`_::

  $ git clone git://github.com/ansible/ansible-sdk

Or download from the `releases page <https://github.com/ansible/ansible-sdk/releases>`_

Create a virtual environment using Python3 and activate it::

  $ virtualenv env
  $ source env/bin/activate

Install Ansible SDK using pip::

  $ cd ansible-sdk
  $ pip install -e .

Building the RPM
----------------

TBD

