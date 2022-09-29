
import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import AnsibleMeshJobExecutor


async def main():
    executor = AnsibleMeshJobExecutor('/tmp/bar.sock', 'baz')
    jobdef = AnsibleJobDef('datadir', 'pb.yml')

    jobs = [await executor.submit_job(jobdef) for j in range(0, 5)]

    print('waiting for jobs')
    done, _ = await asyncio.wait(jobs)

    for j in jobs:
       print(f'job done: {j.done}, has {len(j._events)} events')


if __name__ == '__main__':
    asyncio.run(main())
