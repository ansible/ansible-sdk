.. _running_ansible_jobs:

*****************************
Running local automation jobs
*****************************

Ansible jobs execute playbooks against an inventory.
Ansible SDK provides the following objects to invoke Ansible jobs directly from your project:

* ``AnsibleJobDef`` defines jobs.
* ``JobExecutor`` runs jobs.

*Before you begin:*

* Install Ansible SDK and required software.

Run the example automation job with Ansible SDK, do the following:

#. Open a terminal and change to the ``examples`` directory.
#. Open the ``example_subprocess_job.py`` file with any editor.

   .. code-block:: python
       
      #Imports Ansible SDK modules.
      from ansible_sdk import AnsibleJobDef
      from ansible_sdk.executors import AnsibleSubprocessJobExecutor

      ...

      #Declares the job executor to use.
      executor = AnsibleSubprocessJobExecutor()

      #Configures the job definition.
      jobdef = AnsibleJobDef('datadir', 'pb.yml')
      #Runs the job with the executor.
      job_status = await executor.submit_job(jobdef) 

#. Run the example program as follows:

   .. code-block:: bash

      $ python example_subprocess_job.py

The ``example_subprocess_job.py`` program has a ``main()`` function executes the ``examples/datadir/project/pb.yml`` playbook.
You can verify the job is successful when Ansible SDK prints the following to stdout:

   .. code-block:: bash

      directly awaiting the job status...
      job done? True
      event count: 36
      all done, exiting