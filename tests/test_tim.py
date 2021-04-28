import numpy as np

from pathlib import Path
from deepdiff import DeepDiff
from priwo import read_tim, write_tim
from tempfile import NamedTemporaryFile


fnames = [
    "test_fake_sigproc_float32.tim",
    "test_fake_sigproc_int8.tim",
    "test_fake_sigproc_uint8.tim",
]

fdata = np.asarray(
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


def test_read_tim(datadir):

    """
    Test reading in a `*.tim` file.
    """

    for fname in fnames:
        data = read_tim(datadir.joinpath(fname))["data"]
        assert DeepDiff(fdata, data) == {}


def test_write_tim(datadir):

    """
    Test writing out a `*.tim` file.
    """

    for fname in fnames:
        with NamedTemporaryFile(suffix=".tim") as tfobj:
            write_tim(
                read_tim(datadir.joinpath(fname)),
                Path(tfobj.name),
            )
            data = read_tim(tfobj.name)["data"]
            assert DeepDiff(fdata, data) == {}
