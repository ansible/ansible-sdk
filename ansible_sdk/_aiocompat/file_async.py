# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

import asyncio
from typing import Any, Dict, Optional


class AsyncFile:
    def __init__(self, file_path: str, mode: str = "r", **kwargs: Optional[Dict[str, Any]]):
        self.file_path = file_path
        self.mode = mode
        self.kwargs = kwargs
        self.file = None

    async def __aenter__(self):
        self.file = await asyncio.to_thread(
            open, self.file_path, mode=self.mode, **self.kwargs
        )
        return self.file

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
