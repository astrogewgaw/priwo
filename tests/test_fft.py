import numpy as np

from ward import test
from ward import fixture
from pathlib import Path
from priwo.presto import readfft
from priwo.presto import writefft
from tempfile import NamedTemporaryFile


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


@fixture
def array():
    return np.asarray(
        [
            120.0,
            -8.0,
            -7.9999995,
            40.218716,
            -8.0,
            19.31371,
            -8.0,
            11.972846,
            -8.0,
            8.0,
            -8.0,
            5.3454294,
            -8.0,
            3.3137085,
            -8.0,
            1.5912989,
        ],
        dtype=np.float32,
    )


def check(f):
    assert np.allclose(readfft(f)["data"], array())


@test(f"{str(readfft.__doc__).strip()}")
def _(f=data().joinpath("test.fft")):
    check(f)


@test(f"{str(writefft.__doc__).strip()}")
def _(f=data().joinpath("test.fft")):
    with NamedTemporaryFile(suffix=".fft") as fp:
        writefft(readfft(f), fp.name)
        check(fp.name)
