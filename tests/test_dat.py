import numpy as np

from ward import test
from ward import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile
from priwo.presto.dat import readdat, writedat


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


@fixture
def array():
    return np.asarray(
        [
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
        ],
        dtype=np.float32,
    )


def check(f):
    assert np.allclose(readdat(f)["data"], array())


@test(f"{str(readdat.__doc__).strip()}")
def _(f=data().joinpath("test.dat")):
    check(f)


@test(f"{str(writedat.__doc__).strip()}")
def _(f=data().joinpath("test.dat")):
    with NamedTemporaryFile(suffix=".bestprof") as fp:
        writedat(readdat(f), fp.name)
        check(fp.name)
