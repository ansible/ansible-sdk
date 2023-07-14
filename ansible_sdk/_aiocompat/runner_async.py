# Copyright: Ansible Project
# Apache License 2.0 (see LICENSE or https://www.apache.org/licenses/LICENSE-2.0)

from ansible_runner.interface import run as _run

from .proxy import AsyncProxy


def _write_payload_and_close(payload_writer, **kwargs):
    try:
        _run(streamer='transmit', _output=payload_writer, **kwargs)
    finally:
        # directly chain completion of the payload write with closing the pipe to avoid logical deadlock with reader
        payload_writer.close()


asyncio_write_payload_and_close = AsyncProxy.get_wrapped(_write_payload_and_close)
