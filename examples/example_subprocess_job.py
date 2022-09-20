
import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions


async def main():
    executor = AnsibleSubprocessJobExecutor()
    jobdef = AnsibleJobDef('datadir', 'pb.yml')

    job_status = await executor.submit_job(jobdef, AnsibleSubprocessJobOptions())

    # consume events and accumulate stdout replica
    stdout = ''

    # consume events as they arrive
    eventcount = 0
    async for ev in job_status.events:
        eventcount += 1
        print(f'*** consumed event {ev}')
        # if 'stdout' in ev:
        #    new_data = ev['stdout']
        #    if not new_data:
        #        continue
        #    if new_data[0] == '\n':
        #        new_data = new_data[1:]
        #    eol = '\n' if not new_data[:-1] == '\n' else ''
        #    stdout += f"{ev['stdout']}{eol}"

    print(f'event enumeration completed, total {eventcount}')

    print(f'stdout results: {stdout}')

    # directly await the job object
    print('*** directly awaiting the job status...')
    job_status.stream_task_result

    print(f'job done? {job_status.done}')
    print(f'event count: {job_status.event_count}')

    print('all done, exiting')

if __name__ == '__main__':
    asyncio.run(main())
