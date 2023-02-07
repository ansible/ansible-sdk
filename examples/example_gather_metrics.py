import asyncio

from ansible_sdk import AnsibleJobDef
from ansible_sdk.executors import (
    AnsibleSubprocessJobExecutor,
    AnsibleSubprocessJobOptions,
)


async def run_one_events(executor, executor_options, job_options={}):
    """
    Run a single playbook job with several hosts using the specified executor and options, and dump the raw event
    output to the display as it arrives
    """
    playbook = job_options.get("playbook", None)
    datadir = job_options.get("datadir", "datadir")
    limit = job_options.get("limit", None)
    ident = job_options.get("ident", None)
    forks = job_options.get("forks", None)
    module = job_options.get("module", None)
    module_args = job_options.get("module_args", None)
    host_pattern = job_options.get("host_pattern", None)
    timeout = job_options.get("timeout", None)
    metrics_output_path = job_options.get("metrics_output_path", "")

    try:
        job_def = AnsibleJobDef(
            data_dir=datadir,
            playbook=playbook,
            limit=limit,
            ident=ident,
            forks=forks,
            module=module,
            module_args=module_args,
            host_pattern=host_pattern,
            timeout=timeout,
            metrics_output_path=metrics_output_path,
        )

        job_status = await executor.submit_job(job_def, executor_options)

        # directly await the job object
        print("*** directly awaiting the job status...")
        await job_status
    finally:
        print("all done, exiting")


async def main():
    executor = AnsibleSubprocessJobExecutor()
    executor_options = AnsibleSubprocessJobOptions()
    job_options = {
        "playbook": "pb.yml",
        "metrics_output_path": "metrics_output_path"
    }

    await run_one_events(executor, executor_options, job_options=job_options)


if __name__ == "__main__":
    asyncio.run(main())
