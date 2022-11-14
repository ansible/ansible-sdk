import asyncio


from ansible_sdk.executors import AnsibleSubprocessJobExecutor, AnsibleSubprocessJobOptions
from example_common import run_one_stdout


async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()

    await run_one_stdout(executor, executor_options, playbook='vault.yml')


if __name__ == '__main__':
    asyncio.run(main())
