import asyncio

from ansible_sdk.executors import AnsibleMeshJobExecutor, AnsibleMeshJobOptions
from example_common import run_one_stdout


async def main():
    executor = AnsibleMeshJobExecutor()
    job_options = {
        'playbook': 'extravars.yml',
        'extra_vars': { 'greeting': 'hello world' },
    }
    executor_options = AnsibleMeshJobOptions(
        control_socket_url='unix:///tmp/foo.sock',
        target_node='baz',
        # uncomment the following lines to run in an execution environment via podman (podman must be available on the target node)
        # container_image_ref='quay.io/ansible/ansible-runner:devel',
        # container_runtime_exe='podman',
    )

    await run_one_stdout(executor, executor_options, job_options=job_options)


if __name__ == '__main__':
    asyncio.run(main())
