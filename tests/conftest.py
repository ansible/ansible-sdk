import pytest
import shutil

from pathlib import Path


@pytest.fixture
def datadir(tmp_path):
    """ Yield a path to a copy of the data directory """
    source = Path(__file__).parent / 'data'
    dest = tmp_path / 'data'
    shutil.copytree(source, dest)
    yield dest
    shutil.rmtree(dest, ignore_errors=True)
