from datetime import datetime

from ansible_sdk.model.job_event import AnsibleJobEvent


class TestAnsibleJobEvent:
    def test_status(self):
        data = {"yes": "maybe"}
        event = AnsibleJobEvent(name="theEvent", raw_event_data=data)
        assert event.name == "theEvent"
        assert event.raw_event_data == data
        assert event['yes'] == 'maybe'  # direct indexing should pass through to raw_event_data
