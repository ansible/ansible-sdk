# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

import asyncio
from ansible_sdk.model.job_status import AnsibleJobStatus

class MetricsCalc:
    def __init__(self):
        pass

    async def collect_metrics(self, status_obj: AnsibleJobStatus):
        async for ev in status_obj.events:
            print(ev)
            status_obj.drop_event(ev)
