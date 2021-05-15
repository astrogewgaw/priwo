from pathlib import Path
from deepdiff import DeepDiff
from tempfile import NamedTemporaryFile
from priwo import read_sigproc, write_sigproc


reads = {
    "test_fake_sigproc_float32.tim": {
        "source_name": "Pulsar",
        "telescope_id": 4,
        "machine_id": 10,
        "src_raj": 63642.23,
        "src_dej": -454405.0,
        "az_start": 0.0,
        "za_start": 0.0,
        "data_type": 2,
        "refdm": 26.31,
        "fch1": 1581.8046875,
        "barycentric": 0,
        "nchans": 1,
        "nbits": 32,
        "tstart": 56771.1303125,
        "tsamp": 6.4e-05,
        "nifs": 1,
        "raj": 6.611730555555556,
        "decj": -45.734722222222224,
        "size": 314,
    },
    "test_fake_sigproc_int8.tim": {
        "source_name": "SomePulsar",
        "telescope_id": 0,
        "machine_id": 0,
        "src_raj": 202130.73299999998,
        "src_dej": 402646.04000000004,
        "az_start": 0.0,
        "za_start": 0.0,
        "signed": 1,
        "data_type": 2,
        "refdm": 187.5503692626953,
        "fch1": 1732.0,
        "barycentric": 0,
        "nchans": 1,
        "nbits": 8,
        "tstart": 58900.14229166666,
        "tsamp": 6.4e-05,
        "nifs": 1,
        "raj": 20.358536944444438,
        "decj": 40.44612222222223,
        "size": 329,
    },
    "test_fake_sigproc_uint8.tim": {
        "source_name": "SomePulsar",
        "telescope_id": 0,
        "machine_id": 0,
        "src_raj": 202130.73299999998,
        "src_dej": 402646.04000000004,
        "az_start": 0.0,
        "za_start": 0.0,
        "signed": 0,
        "data_type": 2,
        "refdm": 187.5503692626953,
        "fch1": 1732.0,
        "barycentric": 0,
        "nchans": 1,
        "nbits": 8,
        "tstart": 58900.14229166666,
        "tsamp": 6.4e-05,
        "nifs": 1,
        "raj": 20.358536944444438,
        "decj": 40.44612222222223,
        "size": 329,
    },
}


def test_read_sigproc(datadir):

    """
    Test reading in a SIGPPROC header.
    """

    for fname, fdata in reads.items():
        sigproc = read_sigproc(datadir.joinpath(fname))
        assert DeepDiff(fdata, sigproc) == {}


def test_write_sigproc(datadir):

    """
    Test writing out a SIGPROC header.
    """

    for fname, fdata in reads.items():
        with NamedTemporaryFile(suffix=".tim") as tfobj:
            write_sigproc(
                read_sigproc(datadir.joinpath(fname)),
                Path(tfobj.name),
            )
            sigproc = read_sigproc(tfobj.name)
            assert DeepDiff(fdata, sigproc) == {}
