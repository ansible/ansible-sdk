from ansible_sdk.model.job_def import AnsibleJobDef


class TestAnsibleJobDef:
    def test_required(self):
        job_def = AnsibleJobDef(
            data_dir='sample_data_dir',
            playbook='pb.yml',
        )

        assert job_def.data_dir == "sample_data_dir"
        assert job_def.playbook == "pb.yml"

    def test_envvars(self):
        job_def = AnsibleJobDef(
            data_dir='sample_data_dir',
            playbook='pb.yml',
            env_vars={
                "SAMPLE_VAR": 42,
            }
        )

        assert job_def.data_dir == "sample_data_dir"
        assert job_def.playbook == "pb.yml"
        assert job_def.env_vars.get("SAMPLE_VAR") == 42
