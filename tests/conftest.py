import pytest
from pathlib import Path


@pytest.fixture
def datadir(scope="package"):
    return Path(__file__).parent / "data"
