import numpy as np

from pathlib import Path
from deepdiff import DeepDiff
from priwo import read_fft, write_fft
from tempfile import NamedTemporaryFile


fname = "test_fake_presto_radio.fft"
fdata = np.asarray(
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


def test_fft(datadir):

    """ """

    data = read_fft(datadir.joinpath(fname))["data"]
    assert DeepDiff(fdata, data) == {}


def test_write_fft(datadir):

    """ """

    with NamedTemporaryFile(suffix=".fft") as tfobj:
        write_fft(
            read_fft(datadir.joinpath(fname)),
            Path(tfobj.name),
        )
        data = read_fft(tfobj.name)["data"]
        assert DeepDiff(fdata, data) == {}
