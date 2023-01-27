import numpy as np

from ward import test
from ward import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile
from priwo.sigproc.tim import readtim, writetim


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
    assert np.allclose(readtim(f)["data"], array())


for label, fname in [
    ("Signed 8-bit integer data", "test_ui8.tim"),
    ("Unsigned 8-bit integer data", "test_i8.tim"),
    ("32-bit floating point data", "test_f32.tim"),
]:

    @test(f"{str(readtim.__doc__).strip()} ({label}).")
    def _(f=data().joinpath(f"{fname}")):
        check(f)

    @test(f"{str(writetim.__doc__).strip()} ({label}).")
    def _(f=data().joinpath(f"{fname}")):
        with NamedTemporaryFile(suffix=".tim") as fp:
            writetim(readtim(f), fp.name)
            check(fp.name)
