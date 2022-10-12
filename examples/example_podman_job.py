
import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsiblePodmanJobExecutor, AnsiblePodmanJobOptions


async def main():
    executor = AnsiblePodmanJobExecutor()
    jobdef = AnsibleJobDef(data_dir='datadir', playbook='pb.yml')
    options = AnsiblePodmanJobOptions(container_image_ref='quay.io/ansible/ansible-runner:devel')

    job_status = await executor.submit_job(jobdef, options)

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

    #print(f'job done? {job_status.done}')
    print(f'event count: {len(job_status._events)}')

    print('all done, exiting')

if __name__ == '__main__':
    asyncio.run(main())
