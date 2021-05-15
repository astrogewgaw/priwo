from pathlib import Path
from pytest import fixture


@fixture(scope="module")
def datadir():

    """ """

    return Path(__file__).parent.joinpath("data")
