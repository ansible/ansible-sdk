import asyncio
from tempfile import mkdtemp


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout, run_one_events, run_many


async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    temp_data_dir = mkdtemp()

    job_options = {
        'datadir': temp_data_dir,
        'module': 'debug',
        'module_args': 'msg="Hello From Ansible SDK"',
        'host_pattern': 'localhost',
    }

    await run_one_stdout(executor, executor_options, job_options=job_options)
    await run_one_events(executor, executor_options, job_options=job_options)
    await run_many(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
