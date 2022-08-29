import pytest

from dataclasses import fields
from ansible_sdk.model.job_def import AnsibleJob


class TestAnsibleJob:
    def test_basic(self):
        data_dir = "/tmp/private_data_dir"
        playbook_path = "pb.yml"
        ansible_job = AnsibleJob(data_dir, playbook_path)

        assert len(fields(ansible_job)) == 3
        assert ansible_job.data_dir == data_dir
        assert ansible_job.playbook == playbook_path

    def test_missing_datadir(self):
        playbook_path = "pb.yml"
        with pytest.raises(TypeError) as excinfo:
            AnsibleJob(playbook=playbook_path)

        assert "data_dir" in str(excinfo.value)
