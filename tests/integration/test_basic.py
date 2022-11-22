import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions


async def main(job_options={}):
    executor = AnsibleSubprocessJobExecutor()
    example_dir = job_options.get('datadir')
    playbook = job_options.get('playbook')

    jobdef = AnsibleJobDef(data_dir=example_dir, playbook=playbook)

    job_status = await executor.submit_job(jobdef, AnsibleSubprocessJobOptions())

    # consume events and accumulate stdout replica
    stdout = ''

    # consume events as they arrive
    eventcount = 0
    async for ev in job_status.events:
        eventcount += 1
        print(f'*** consumed event {ev}')

    print(f'event enumeration completed, total {eventcount}')

    print(f'stdout results: {stdout}')

    # directly await the job object
    print('*** directly awaiting the job status...')
    await job_status

    print(f'event count: {len(job_status._events)}')

    print('all done, exiting')


def test_basic(datadir):
    example_dir = str(datadir / 'basic')
    job_options = {
        'datadir': example_dir,
        'playbook': 'pb.yml',
    }
    asyncio.run(main(job_options))


def test_limit(datadir):
    example_dir = str(datadir / 'basic')
    job_options = {
        'datadir': example_dir,
        'playbook': 'pb.yml',
        'limit': 'h1',
    }
    asyncio.run(main(job_options))


def test_ident(datadir):
    example_dir = str(datadir / 'basic')
    job_options = {
        'datadir': example_dir,
        'playbook': 'pb.yml',
        'ident': 'sample_dir',
    }
    asyncio.run(main(job_options))
