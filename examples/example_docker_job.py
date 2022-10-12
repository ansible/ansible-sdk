import asyncio

from ansible_sdk.executors import AnsibleDockerJobExecutor, AnsibleDockerJobOptions
from example_common import run_one_stdout, run_one_events, run_many


async def main():
    executor = AnsibleDockerJobExecutor()
    executor_options = AnsibleDockerJobOptions(container_image_ref='quay.io/ansible/ansible-runner:devel')

    await run_one_stdout(executor, executor_options)
    await run_one_events(executor, executor_options)
    await run_many(executor, executor_options)


if __name__ == '__main__':
    asyncio.run(main())
