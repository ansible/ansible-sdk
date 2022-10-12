
import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions


async def run_one_stdout():
    try:
        executor = AnsibleSubprocessJobExecutor()
        jobdef = AnsibleJobDef(data_dir='datadir', playbook='pb.yml')

        job_status = await executor.submit_job(jobdef, AnsibleSubprocessJobOptions())

        async for line in job_status.stdout_lines:
            print(line)

        # directly await the job object
        print('*** directly awaiting the job status...')
        await job_status
    finally:
        print('all done, exiting')


async def run_one_events():
    try:
        executor = AnsibleSubprocessJobExecutor()
        jobdef = AnsibleJobDef(data_dir='datadir', playbook='pb.yml')

        job_status = await executor.submit_job(jobdef, AnsibleSubprocessJobOptions())

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


async def run_many():
    try:
        executor = AnsibleSubprocessJobExecutor()
        jobdef = AnsibleJobDef(data_dir='datadir', playbook='pb.yml', verbosity=2)

        num_jobs = 5

        print(f'starting {num_jobs} jobs...')

        import dataclasses

        job_statuses = [await executor.submit_job(jobdef.replace(extra_vars=dict(extra_var_value=f'job_{i}')), AnsibleSubprocessJobOptions()) for i in range(0, num_jobs)]

        async def dumpy(job_status):
            async for ev in job_status.events:
                print(f'got event from job {job_status._job_def.extra_vars["extra_var_value"]}: {ev}')

                # manually drop event after consumption
                job_status.drop_event(ev)

        dumpers = [asyncio.create_task(dumpy(s)) for s in job_statuses]

        print(f'waiting for jobs to complete...')
        await asyncio.gather(*job_statuses)

        print('final event dump (should be empty since we dropped all events)')
        for j in job_statuses:
            async for ev in j.events:
                print(f'got event {ev}')

    finally:
        print('all done, exiting')


async def main():
    await run_one_stdout()
    await run_one_events()
    await run_many()


if __name__ == '__main__':
    asyncio.run(main())


