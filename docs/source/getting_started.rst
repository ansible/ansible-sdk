.. _getting_started:


Getting Started With Ansible SDK
================================

The ``Ansible SDK`` package provides a low-level interface to Ansible.

It is responsible for:

* Providing access to all operations
* Marshaling all parameters for a particular operation in the correct format
* Receiving the response and returning the data in native Python data structures


Using Ansible SDK
-----------------

The first step in using Ansible SDK is to create a ``JobExecutor`` object.
``JobExecutor`` objects then allow you to execute Ansible Jobs::

    from ansible_sdk.executors import AnsibleSubprocessJobExecutor

    executor = AnsibleSubprocessJobExecutor()
    
Once you have that executor object created, you can execute Ansible Job using Ansible Job Definition::

    from ansible_sdk import AnsibleJobDef
    ...
    jobdef = AnsibleJobDef('datadir', 'pb.yml')
    job_status = await executor.submit_job(jobdef)

Please see ``examples`` directory for more information.