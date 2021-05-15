import numpy as np

from pathlib import Path
from deepdiff import DeepDiff
from priwo import read_pfd, write_pfd
from tempfile import NamedTemporaryFile

fname = "test_PSR_J1646-2142.pfd"

fdata = {
    "numdms": 257,
    "numperiods": 201,
    "numpdots": 201,
    "nsub": 128,
    "npart": 60,
    "proflen": 128,
    "numchan": 512,
    "pstep": 1,
    "pdstep": 2,
    "dmstep": 1,
    "ndmfact": 1,
    "npfact": 1,
    "filename": "J1646-2142_500_200_512_2.15jul2k19.raw0.fil",
    "candname": "PSR_1646-2142",
    "telescope": "GMRT",
    "pgdev": "J1646-2142_500_200_512_2.15jul2k19.raw0.new_freq_PSR_1646-2142.pfd.ps/CPS",
    "rastr": "16:46:18.1250",
    "decstr": "-21:42:08.9063",
    "tsamp": 1.024e-05,
    "startT": 0.0,
    "endT": 1.0,
    "tepoch": 58679.6856653963,
    "bepoch": 0.0,
    "avgoverc": 0.0,
    "lofreq": 300.0,
    "chanwidth": 0.390625,
    "bestdm": 29.741,
    "topopow": 0.0,
    "_t": 0.0,
    "topop1": 0.005853475376566149,
    "topop2": -0.0,
    "topop3": 0.0,
    "barypow": 0.0,
    "_b": 0.0,
    "baryp1": 0.0,
    "baryp2": 0.0,
    "baryp3": 0.0,
    "foldpow": 0.0,
    "_f": 4.591354418360263e-41,
    "foldp1": 170.8386788476822,
    "foldp2": 0.0,
    "foldp3": 0.0,
    "orbp": 0.0,
    "orbe": 0.0,
    "orbx": 0.0,
    "orbw": 0.0,
    "orbt": 0.0,
    "orbpd": 0.0,
    "orbwd": 0.0,
    "numprofs": 7680,
}

farrs = {
    "dms": "dms.npy",
    "profs": "profs.npy",
    "pdots": "pdots.npy",
    "stats": "stats.npy",
    "periods": "periods.npy",
}


def test_read_pfd(datadir):

    """
    Test reading in a `*.pfd` file.
    """

    pfd = read_pfd(datadir.joinpath(fname))
    for key, farr in farrs.items():
        assert np.allclose(
            pfd.pop(key),
            np.load(datadir.joinpath(farr)),
            equal_nan=True,
        )
    assert DeepDiff(fdata, pfd) == {}


def test_write_pfd(datadir):

    """ """

    with NamedTemporaryFile(suffix=".dat") as tfobj:
        write_pfd(
            read_pfd(datadir.joinpath(fname)),
            Path(tfobj.name),
        )
        pfd = read_pfd(tfobj.name)
        for key, farr in farrs.items():
            assert np.allclose(
                pfd.pop(key),
                np.load(datadir.joinpath(farr)),
                equal_nan=True,
            )
        assert DeepDiff(fdata, pfd) == {}
