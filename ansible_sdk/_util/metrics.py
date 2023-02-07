# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

import os
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
        }

        if not status_obj._job_def.metrics_output_path:
            return

        async for ev in status_obj.events:
            if ev.get("event") == "playbook_on_start":
                metrics_data["started"] = datetime.strptime(
                    ev.get("created"), "%Y-%m-%dT%H:%M:%S.%f"
                )
            if ev.get("event") == "playbook_on_task_start":
                metrics_data["task_counter"] += 1
            if ev.get("event") == "playbook_on_stats":
                csv_filename = os.path.join(
                    status_obj._job_def.metrics_output_path,
                    "job_%s.csv" % ev["runner_ident"],
                )
                fh = open(csv_filename, "w+")
                headers = [x.name for x in dataclasses.fields(AnsiblePlaybookStats)]
                writer = CSVAsync(fh, headers, restval="NULL")
                await writer.writeheader_async()
                end_time = datetime.strptime(ev.get("created"), "%Y-%m-%dT%H:%M:%S.%f")

                await writer.writerow_async(
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
                        "task_duration": metrics_data.get("started") - end_time,
                    }
                )
                fh.close()
            print(ev)

            status_obj.drop_event(ev)
