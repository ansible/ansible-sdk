# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

import os
import uuid

from datetime import datetime

import ansible_sdk._util.dataclass_compat as dataclasses
from ansible_sdk.model.job_status import AnsibleJobStatus
from ansible_sdk._aiocompat.csv_async import CSVAsync


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsiblePlaybookStats:
    job_id: str
    job_type: str
    started: str
    finished: str
    job_state: str
    hosts_ok: str
    hosts_changed: str
    hosts_skipped: str
    hosts_failed: str
    hosts_unreachable: str
    task_count: str
    task_duration: str


class MetricsCalc:
    def __init__(self):
        pass

    async def collect_metrics(self, status_obj: AnsibleJobStatus):
        metrics_data = {
            "task_counter": 0,
            "task_data": {},
            "role_data": {},
        }

        if not status_obj._job_def.metrics_output_path:
            return

        # Create job.csv
        job_id = uuid.uuid4()
        job_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path,
            "job_%s.csv" % job_id,
        )
        job_csv_fh = open(job_csv_filename, "w+")
        headers = [x.name for x in dataclasses.fields(AnsiblePlaybookStats)]
        job_csv_writer = CSVAsync(job_csv_fh, headers, restval="NULL")
        await job_csv_writer.writeheader_async()

        # Create modules.csv
        module_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path,
            "modules_%s.csv" % job_id,
        )
        module_csv_fh = open(module_csv_filename, "w+")
        headers = ["job_id", "module_fqcn", "role_fqcn", "task_count", "task_duration"]
        module_csv_writer = CSVAsync(module_csv_fh, headers, restval="NULL")
        await module_csv_writer.writeheader_async()

        async for ev in status_obj.events:
            end_time = datetime.strptime(ev.get("created"), "%Y-%m-%dT%H:%M:%S.%f")
            if ev.get("event") == "playbook_on_start":
                metrics_data["started"] = datetime.strptime(
                    ev.get("created"), "%Y-%m-%dT%H:%M:%S.%f"
                )
            if ev.get("event") == "playbook_on_task_start":
                metrics_data["task_counter"] += 1
                # Update the count of task
                resolved_task_name = ev["event_data"]["resolved_action"]
                if resolved_task_name in metrics_data["task_data"]:
                    metrics_data["task_data"][resolved_task_name] += 1
                else:
                    metrics_data["task_data"][resolved_task_name] = 1

                # Update the count of role
                resolved_role_name = ev["event_data"].get("role")
                if resolved_role_name:
                    if resolved_role_name in metrics_data["role_data"]:
                        metrics_data["role_data"][resolved_role_name] += 1
                    else:
                        metrics_data["role_data"][resolved_role_name] = 1

            if ev.get("event") == "playbook_on_stats":
                # Write module metrics data
                for task in metrics_data["task_data"]:
                    await module_csv_writer.writerow_async(
                        {
                            "job_id": ev["runner_ident"],
                            "module_fqcn": task,
                            "role_fqcn": "",
                            "task_count": metrics_data["task_data"][task],
                            "task_duration": "",
                        }
                    )

                # Write job metrics data
                await job_csv_writer.writerow_async(
                    {
                        "job_id": ev["runner_ident"],
                        "job_type": "local",
                        "started": metrics_data.get("started"),
                        "finished": end_time,
                        "job_state": "",
                        "hosts_ok": len(ev["event_data"]["ok"]),
                        "hosts_changed": len(ev["event_data"]["changed"]),
                        "hosts_skipped": len(ev["event_data"]["skipped"]),
                        "hosts_failed": len(ev["event_data"]["failures"]),
                        "hosts_unreachable": len(ev["event_data"]["failures"]),
                        "task_count": metrics_data["task_counter"],
                        "task_duration": end_time - metrics_data.get("started"),
                    }
                )

            status_obj.drop_event(ev)

        module_csv_fh.close()
        job_csv_fh.close()
