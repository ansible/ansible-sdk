from datetime import datetime

from ansible_sdk.model.job_event import AnsibleJobStatusEvent


class TestAnsibleJobStatusEvent:
    def test_status(self):
        ts = datetime(2022, 12, 31, 7, 59, 30, 1234).isoformat()
        data = {"yes": "maybe"}
        event = AnsibleJobStatusEvent(uuid="theUUID", parent_uuid="theParentUUID", counter=1,
                                      stdout="theStdout", start_line=0, end_line=10,
                                      event="theEvent", event_data=data, pid=42, created=ts)
        assert event.uuid == "theUUID"
        assert event.parent_uuid == "theParentUUID"
        assert event.counter == 1
        assert event.stdout == "theStdout"
        assert event.start_line == 0
        assert event.end_line == 10
        assert event.event == "theEvent"
        assert event.event_data == data
        assert event.pid == 42
        assert event.created == ts

        # Test setting new created timestamp
        new_ts = datetime(2000, 1, 17, 14, 00, 13, 5678).isoformat()
        event.created = new_ts
        assert event.created == new_ts
