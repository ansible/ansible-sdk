from ansible_sdk.executors.common.desired_capabilities import DesiredCapabilities


class SubProcessOptions:
    def __init__(self) -> None:
        super().__init__()

    @property
    def default_capabilities(self) -> dict:
        return DesiredCapabilities.SUBPROCESS.copy()