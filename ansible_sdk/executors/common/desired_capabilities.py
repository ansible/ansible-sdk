"""
The Desired Capabilities implementation.
"""


class DesiredCapabilities:
    """
    Set of default supported desired capabilities.
    Use this as a starting point for creating a desired capabilities object for
    executors.
    Usage Example::
        
        from ansible_sdk.executors import AnsiblePodmanJobExecutor

        # Create a desired capabilities object as a starting point.
        capabilities = DesiredCapabilities.PODMAN.copy()
        capabilities['image_ref'] = "quay.io/ansible/ansible-runner"
        capabilities['version'] = "devel"

        executor = AnsiblePodmanJobExecutor(options=capabilities)
    """

    PODMAN = {
        "image_ref": "quay.io/ansible/ansible-runner",
        "version": "devel"
    }

    SUBPROCESS = {
        
    }
