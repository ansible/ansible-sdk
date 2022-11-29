import asyncio


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout


async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()
    job_options = {
        'playbook': 'pb.yml',
        'ident': 'sample_dir'
    }

    await run_one_stdout(executor, executor_options, job_options)


if __name__ == '__main__':
    asyncio.run(main())
