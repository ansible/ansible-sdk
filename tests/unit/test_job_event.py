from datetime import datetime

from ansible_sdk.model.job_event import BaseEvent


class TestBaseEvent:

    def test_basic(self):
        ts = datetime(2022, 12, 31, 7, 59, 30, 1234).isoformat()
        event = BaseEvent(event="theEvent", uuid="theUUID", counter=1,
                          stdout="theStdout", start_line=0, end_line=10,
                          runner_ident="theIdent", created=ts)

        assert event.event == "theEvent"
        assert event.uuid == "theUUID"
        assert event.counter == 1
        assert event.stdout == "theStdout"
        assert event.start_line == 0
        assert event.end_line == 10
        assert event.runner_ident == "theIdent"
        assert event.created == datetime.fromisoformat(ts)

        # Test setting new created timestamp
        new_ts = datetime(2000, 1, 17, 14, 00, 13, 5678).isoformat()
        event.created = new_ts
        assert event.created == datetime.fromisoformat(new_ts)
