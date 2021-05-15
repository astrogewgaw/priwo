import numpy as np

from pathlib import Path
from deepdiff import DeepDiff
from tempfile import NamedTemporaryFile
from priwo import read_polycos, write_polycos


fname = "test_PSR_J1646-2142.polycos"
fdata = {
    "psrname": "1646-2142",
    "date": "14-JUL-19",
    "utc": "50000.00",
    "tmid": 58678.2083333333,
    "dm": 29.741,
    "doppler": 0.605,
    "log10rms": -6.064,
    "ref_phase": 30728623742.9709,
    "ref_rot": 170.849389109675,
    "obs_code": 27,
    "data_span": 60.0,
    "num_coeff": 12,
    "obs_freq": 399.805,
    "bin_phz": None,
}


def test_read_polycos(datadir):

    """
    Test reading in a `*.polycos` file.
    """

    polycos = read_polycos(datadir.joinpath(fname))
    assert np.allclose(
        polycos[0].pop("coeffs"),
        np.load(datadir.joinpath("coeffs.npy")),
        equal_nan=True,
    )
    assert DeepDiff(fdata, polycos[0]) == {}


def test_write_polycos(datadir):

    """
    Test writing out a `*.polycos` file.
    """

    with NamedTemporaryFile(suffix=".polycos") as tfobj:
        write_polycos(read_polycos(datadir.joinpath(fname)), Path(tfobj.name))
        polycos = read_polycos(tfobj.name)
        assert np.allclose(
            polycos[0].pop("coeffs"),
            np.load(datadir.joinpath("coeffs.npy")),
            equal_nan=True,
        )
        assert DeepDiff(fdata, polycos[0]) == {}
