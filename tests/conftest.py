from pathlib import Path

import pytest


@pytest.fixture
def datadir(scope="package"):
    return Path(__file__).parent / "data"
