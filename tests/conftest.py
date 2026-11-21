from pathlib import Path

import pytest


@pytest.fixture(scope="package")
def datadir():
    return Path(__file__).parent / "data"
