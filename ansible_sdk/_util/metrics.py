# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

import asyncio
import os
import tarfile

from datetime import datetime
from hashlib import sha256

import ansible_sdk._util.dataclass_compat as dataclasses
from ansible_sdk.model.job_status import AnsibleJobStatus
from ansible_sdk._aiocompat.csv_async import CSVAsync
from ansible_sdk._aiocompat.file_async import AsyncFile


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsibleJobStats:
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


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsibleModuleStats:
    job_id: str
    module_fqcn: str
    role_fqcn: str
    task_count: int
    task_duration: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsibleCollectionStats:
    job_id: str
    collection_fqcn: str
    collection_version: str
    task_count: int
    task_duration: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsibleRoleStats:
    job_id: str
    role_fqcn: str
    collection_version: str
    task_count: int
    task_duration: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class AnsiblePlaybookStats:
    job_id: str
    event_id: str
    event_data: str


@dataclasses.dataclass(frozen=False, kw_only=True)
class MetricsData:
    started: datetime = dataclasses.field(default_factory=datetime.now)
    task_counter: int = 0
    task_data: dict = dataclasses.field(default_factory=dict)
    role_data: dict = dataclasses.field(default_factory=dict)
    collection_data: dict = dataclasses.field(default_factory=dict)


class MetricsCalc:
    def __init__(self):
        pass

    async def create_tarfile_async(self, file_paths, tarfile_path):
        with tarfile.open(tarfile_path, "w:gz") as tar:
            for file_path in file_paths:
                tar.add(file_path, arcname=os.path.basename(file_path))
                os.remove(file_path)

    def encrypt_hostname_data(self, event_data):
        enc_dict = {}
        enc_key = [
            'changed', 'dark', 'failures',
            'ignored', 'ok', 'processed',
            'rescued', 'skipped'
        ]

        def encrypt_keys(d):
            enc_d = {}
            for key, value in d.items():
                dk = sha256(key.encode())
                enc_d[dk.hexdigest()] = value
            return enc_d

        for key, value in event_data.items():
            if key in enc_key:
                enc_dict[key] = encrypt_keys(value)
            else:
                enc_dict[key] = value
        return enc_dict

    async def collect_metrics(self, status_obj: AnsibleJobStatus):
        metrics_data = MetricsData()
        job_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path, "jobs.csv"
        )
        module_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path,
            "modules.csv",
        )
        collection_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path, "collections.csv"
        )
        roles_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path, "roles.csv"
        )
        pb_stats_csv_filename = os.path.join(
            status_obj._job_def.metrics_output_path, "playbook_on_stats.csv"
        )

        job_headers = [x.name for x in dataclasses.fields(AnsibleJobStats)]
        module_headers = [x.name for x in dataclasses.fields(AnsibleModuleStats)]
        collection_headers = [
            x.name for x in dataclasses.fields(AnsibleCollectionStats)
        ]
        role_headers = [x.name for x in dataclasses.fields(AnsibleRoleStats)]
        pb_stats_headers = [x.name for x in dataclasses.fields(AnsiblePlaybookStats)]

        async with (
            AsyncFile(job_csv_filename, "w") as job_csv_fh,
            AsyncFile(collection_csv_filename, "w") as collection_csv_fh,
            AsyncFile(roles_csv_filename, "w") as role_csv_fh,
            AsyncFile(module_csv_filename, "w") as module_csv_fh,
            AsyncFile(pb_stats_csv_filename, "w") as pb_stats_csv_fh,
        ):
            job_csv_writer = CSVAsync(job_csv_fh, job_headers, restval="NULL")
            await job_csv_writer.writeheader_async()
            module_csv_writer = CSVAsync(module_csv_fh, module_headers, restval="NULL")
            await module_csv_writer.writeheader_async()
            collection_csv_writer = CSVAsync(
                collection_csv_fh, collection_headers, restval="NULL"
            )
            await collection_csv_writer.writeheader_async()
            role_csv_writer = CSVAsync(role_csv_fh, role_headers, restval="NULL")
            await role_csv_writer.writeheader_async()
            pb_stats_csv_writer = CSVAsync(pb_stats_csv_fh, pb_stats_headers, restval="NULL")
            await pb_stats_csv_writer.writeheader_async()

            async for ev in status_obj.events:
                runner_ident = ev.get("runner_ident")
                end_time = datetime.fromisoformat(ev.get("created"))
                if ev.get("event") == "playbook_on_start":
                    metrics_data.started = datetime.fromisoformat(ev.get("created"))
                if ev.get("event") == "playbook_on_task_start":
                    metrics_data.task_counter += 1
                    # Update the count of task
                    resolved_task_name = ev["event_data"].get("resolved_action")
                    collection_name = resolved_task_name.rsplit(".", 1)[0]

                    # Update the count of collections
                    metrics_data.collection_data[collection_name] = (
                        metrics_data.collection_data.get(collection_name, 0) + 1
                    )

                    # Update the count of tasks
                    metrics_data.task_data[resolved_task_name] = (
                        metrics_data.task_data.get(resolved_task_name, 0) + 1
                    )

                    # Update the count of roles
                    if resolved_role_name := ev["event_data"].get("role"):
                        # Role name is not always populated
                        metrics_data.role_data[resolved_role_name] = (
                            metrics_data.role_data.get(resolved_role_name, 0) + 1
                        )

                if ev.get("event") == "playbook_on_stats":
                    # Write playbook on stats data
                    await pb_stats_csv_writer.writerow_async(
                        {
                            "job_id": runner_ident,
                            "event_id": ev.get("uuid"),
                            "event_data": self.encrypt_hostname_data(ev.get("event_data")),
                        }
                    )

                    # Write module metrics data
                    for task, task_count in metrics_data.task_data.items():
                        await module_csv_writer.writerow_async(
                            {
                                "job_id": runner_ident,
                                "module_fqcn": task,
                                "role_fqcn": "",
                                "task_count": task_count,
                                "task_duration": "",
                            }
                        )

                    # Write job metrics data
                    await job_csv_writer.writerow_async(
                        {
                            "job_id": runner_ident,
                            "job_type": "local",
                            "started": metrics_data.started,
                            "finished": end_time,
                            "job_state": "",
                            "hosts_ok": len(ev["event_data"].get("ok")),
                            "hosts_changed": len(ev["event_data"].get("changed")),
                            "hosts_skipped": len(ev["event_data"].get("skipped")),
                            "hosts_failed": len(ev["event_data"].get("failures")),
                            "hosts_unreachable": len(ev["event_data"].get("failures")),
                            "task_count": metrics_data.task_counter,
                            "task_duration": end_time - metrics_data.started,
                        }
                    )

                    # Write collection metrics data
                    for collection, collection_count in metrics_data.collection_data.items():
                        await collection_csv_writer.writerow_async(
                            {
                                "job_id": runner_ident,
                                "collection_fqcn": collection,
                                "collection_version": "",
                                "task_count": collection_count,
                                "task_duration": "",
                            }
                        )

                    # Write role metrics data
                    for role, role_count in metrics_data.role_data.items():
                        await role_csv_writer.writerow_async(
                            {
                                "job_id": runner_ident,
                                "role_fqcn": role,
                                "collection_version": "",
                                "task_count": role_count,
                                "task_duration": "",
                            }
                        )

        # Create a tar file for further consumption
        _end_time = datetime.strftime(end_time, "%Y_%m_%d_%H_%M_%S")
        metrics_tar_filepath = os.path.join(
            status_obj._job_def.metrics_output_path,
            f"{_end_time}_{runner_ident}_job_data.tar.gz"
        )

        datafiles = [
            job_csv_filename,
            module_csv_filename,
            collection_csv_filename,
            roles_csv_filename,
            pb_stats_csv_filename,
        ]

        await asyncio.to_thread(self.create_tarfile_async, datafiles, metrics_tar_filepath)
