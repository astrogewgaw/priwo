import numpy as np

from ward import test
from ward import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile
from priwo.sigproc.fil import readfil, writefil


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f, array):
    assert np.allclose(readfil(f)["data"][64, 100:110], array)


for n, array in {
    1: np.asarray([1, 1, 0, 0, 0, 0, 0, 0, 1, 1], dtype=np.uint8),
    2: np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8),
    4: np.asarray([7, 4, 3, 11, 6, 10, 10, 9, 6, 7], dtype=np.uint8),
    8: np.asarray([121, 94, 94, 124, 151, 118, 132, 74, 112, 65], dtype=np.uint8),
    32: np.asarray(
        [
            1.166237,
            -0.84468514,
            0.874816,
            1.4028563,
            -0.98618776,
            -0.80890864,
            -1.6307002,
            1.1306021,
            0.50498164,
            -1.6316832,
        ],
        dtype=np.float32,
    ),
}.items():

    @test(f"{str(readfil.__doc__).strip()} ({n}-bit data).")
    def _(f=data().joinpath(f"test_{n}bit.fil"), array=array):
        check(f, array)

    @test(f"{str(writefil.__doc__).strip()} ({n}-bit data).")
    def _(f=data().joinpath(f"test_{n}bit.fil"), array=array):
        with NamedTemporaryFile(suffix=".fil") as fp:
            writefil(readfil(f), fp.name)
            check(fp.name, array)
