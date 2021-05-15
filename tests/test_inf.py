from pathlib import Path
from deepdiff import DeepDiff
from priwo import read_inf, write_inf
from tempfile import NamedTemporaryFile


reads = {
    "test_fake_presto_radio.inf": {
        "bsname": "fake_presto_radio",
        "telescope": "Parkes",
        "instrument": "Multibeam",
        "object": "Pulsar",
        "rastr": "00:00:01.0000",
        "decstr": "-00:00:01.0000",
        "observer": "Kenji Oba",
        "mjd": 59000.0,
        "bary": True,
        "nsamp": 16,
        "tsamp": 6.4e-05,
        "breaks": False,
        "emband": "Radio",
        "bdiam": 981.0,
        "dm": 42.42,
        "cfreq": 1182.1953125,
        "bw": 400.0,
        "nchan": 1024,
        "chanwid": 0.390625,
        "analyst": "Space Sheriff Gavan",
        "notes": ["Input filterbank samples have 2 bits."],
        "onoffs": [],
    },
    "test_fake_presto_radio_breaks.inf": {
        "bsname": "fake_presto_radio_breaks",
        "telescope": "Parkes",
        "instrument": "Multibeam",
        "object": "Pulsar",
        "rastr": "00:00:01.0000",
        "decstr": "-00:00:01.0000",
        "observer": "Kenji Oba",
        "mjd": 59000.0,
        "bary": True,
        "nsamp": 16,
        "tsamp": 6.4e-05,
        "breaks": True,
        "emband": "Radio",
        "bdiam": 981.0,
        "dm": 42.42,
        "cfreq": 1182.1953125,
        "bw": 400.0,
        "nchan": 1024,
        "chanwid": 0.390625,
        "analyst": "Space Sheriff Gavan",
        "notes": ["Input filterbank samples have 2 bits."],
        "onoffs": [(0, 14), (15, 15)],
    },
    "test_fake_presto_xray.inf": {
        "bsname": "fake_presto_xray",
        "telescope": "Chandra",
        "instrument": "HRC-S",
        "object": "Pulsar",
        "rastr": "00:00:01.0000",
        "decstr": "-00:00:01.0000",
        "observer": "Kenji Oba",
        "mjd": 59000.0,
        "bary": True,
        "nsamp": 16,
        "tsamp": 6.4e-05,
        "breaks": False,
        "emband": "X-ray",
        "fov": 3.0,
        "cE": 1.0,
        "bpE": 5.0,
        "analyst": "Space Sheriff Gavan",
        "notes": ["Full ms-resolution analysis"],
        "onoffs": [],
    },
}


def test_read_inf(datadir):

    """
    Test reading in a `*.inf` file.
    """

    for fname, fdata in reads.items():
        inf = read_inf(datadir.joinpath(fname))
        assert DeepDiff(fdata, inf) == {}


def test_write_inf(datadir):

    """
    Test writing out a `*.inf` file.
    """

    for fname, fdata in reads.items():
        with NamedTemporaryFile(suffix=".inf") as tfobj:
            write_inf(
                read_inf(datadir.joinpath(fname)),
                Path(tfobj.name),
            )
            inf = read_inf(tfobj.name)
            assert DeepDiff(fdata, inf) == {}
