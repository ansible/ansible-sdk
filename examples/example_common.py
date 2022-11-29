import asyncio

from ansible_sdk import AnsibleJobDef


async def run_one_stdout(executor, executor_options, job_options={}):
    """
    Run a single playbook job with several hosts and echo the display output as it arrives
    """
    playbook = job_options.get('playbook', None)
    datadir = job_options.get('datadir', 'datadir')
    limit = job_options.get('limit', None)
    ident = job_options.get('ident', None)
    forks = job_options.get('forks', None)
    module = job_options.get('module', None)
    module_args = job_options.get('module_args', None)
    host_pattern = job_options.get('host_pattern', None)

    try:
        job_def = AnsibleJobDef(
            data_dir=datadir,
            playbook=playbook,
            limit=limit,
            ident=ident,
            forks=forks,
            module=module,
            module_args=module_args,
            host_pattern=host_pattern
        )
        job_status = await executor.submit_job(job_def, executor_options)

        async for line in job_status.stdout_lines:
            print(line)

        # directly await the job object
        print('*** directly awaiting the job status...')
        await job_status
    finally:
        print('all done, exiting')


async def run_one_events(executor, executor_options, job_options={}):
    """
    Run a single playbook job with several hosts using the specified executor and options, and dump the raw event
    output to the display as it arrives
    """
    playbook = job_options.get('playbook', None)
    datadir = job_options.get('datadir', 'datadir')
    limit = job_options.get('limit', None)
    ident = job_options.get('ident', None)
    forks = job_options.get('forks', None)
    module = job_options.get('module', None)
    module_args = job_options.get('module_args', None)
    host_pattern = job_options.get('host_pattern', None)

    try:
        job_def = AnsibleJobDef(
            data_dir=datadir,
            playbook=playbook,
            limit=limit,
            ident=ident,
            forks=forks,
            module=module,
            module_args=module_args,
            host_pattern=host_pattern,
        )
        job_status = await executor.submit_job(job_def, executor_options)

        eventcount = 0
        async for ev in job_status.events:
            eventcount += 1
            print(f'*** consumed event {ev}')

        print(f'event enumeration completed, total {eventcount}')

        # directly await the job object
        print('*** directly awaiting the job status...')
        await job_status
    finally:
        print('all done, exiting')


async def run_many(executor, executor_options, job_options={}):
    """
    Run five concurrent jobs (with slightly different definitions) against several hosts and dump the raw event
    output to the display as it arrives (interleaving output between the jobs).
    """
    playbook = job_options.get('playbook', None)
    datadir = job_options.get('datadir', 'datadir')
    limit = job_options.get('limit', None)
    ident = job_options.get('ident', None)
    forks = job_options.get('forks', None)
    module = job_options.get('module', None)
    module_args = job_options.get('module_args', None)
    host_pattern = job_options.get('host_pattern', None)

    try:
        job_def = AnsibleJobDef(
            data_dir=datadir,
            playbook=playbook,
            limit=limit,
            ident=ident,
            forks=forks,
            module=module,
            module_args=module_args,
            host_pattern=host_pattern,
        )

        num_jobs = 5

        print(f'starting {num_jobs} jobs...')

        # start all the jobs now
        job_statuses = [
            await executor.submit_job(
            job_def.replace(extra_vars=dict(extra_var_value=f'job_{i}')), executor_options) for i in range(0, num_jobs)
        ]

        async def dump_events(job_status):
            async for ev in job_status.events:
                print(f'got event from job {job_status._job_def.extra_vars["extra_var_value"]}: {ev}')

                # manually drop event after consumption
                job_status.drop_event(ev)

        # start one dumper per job to interleave the event output from all running jobs as the events arrive
        dumpers = [asyncio.create_task(dump_events(s)) for s in job_statuses]

        # FIXME: should probably await these?

        print(f'waiting for jobs to complete...')
        await asyncio.gather(*job_statuses)

        # dump remaining events (shouldn't be any since we dropped them all after displaying them)
        print('final event dump (should be none)')
        for j in job_statuses:
            async for ev in j.events:
                print(f'got event {ev}')

    finally:
        print('all done, exiting')

