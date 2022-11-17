import asyncio

from ansible_sdk.executors import AnsiblePodmanJobExecutor, AnsiblePodmanJobOptions
from example_common import run_one_stdout, run_one_events, run_many


async def main():
    executor = AnsiblePodmanJobExecutor()
    executor_options = AnsiblePodmanJobOptions(container_image_ref='quay.io/ansible/ansible-runner:devel')
    job_options = {
        'limit': 1
    }

    await run_one_stdout(executor, executor_options, job_options=job_options)
    await run_one_events(executor, executor_options, job_options=job_options)
    await run_many(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
