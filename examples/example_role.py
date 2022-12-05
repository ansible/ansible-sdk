import asyncio
import os


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout


async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    job_options = {
        'role': 'hello_world',
        'roles_path': os.getcwd() + "/roles",
    }
    await run_one_stdout(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
