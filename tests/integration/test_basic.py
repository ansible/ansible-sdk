import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions


async def main(job_options={}):
    executor = AnsibleSubprocessJobExecutor()
    example_dir = job_options.get('datadir')
    playbook = job_options.get('playbook')

    jobdef = AnsibleJobDef(data_dir=example_dir, playbook=playbook)

    job_status = await executor.submit_job(jobdef, AnsibleSubprocessJobOptions())

    # consume events as they arrive
    eventcount = 0
    async for ev in job_status.events:
        eventcount += 1

    # directly await the job object
    await job_status


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
