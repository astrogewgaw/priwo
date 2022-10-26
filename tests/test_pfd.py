import numpy as np

from ward import test
from ward import fixture
from pathlib import Path
from priwo.presto import readpfd
from priwo.presto import writepfd
from tempfile import NamedTemporaryFile


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    meta = readpfd(f)["meta"]
    for _ in ["dms", "pdots", "stats", "periods"]:
        meta.pop(_)
    assert meta == dict(
        ndms=257,
        nperiods=201,
        npdots=201,
        nsub=128,
        npart=60,
        nbin=128,
        nchan=512,
        pstep=1,
        pdstep=2,
        dmstep=1,
        ndmfact=1,
        npfact=1,
        filename="J1646-2142_500_200_512_2.15jul2k19.raw0.fil",
        candname="PSR_1646-2142",
        telescope="GMRT",
        pgdev="J1646-2142_500_200_512_2.15jul2k19.raw0.new_freq_PSR_1646-2142.pfd.ps/CPS",
        rastr="16:46:18.1250",
        decstr="-21:42:08.9063",
        tsamp=1.024e-05,
        startT=0.0,
        endT=1.0,
        tepoch=58679.6856653963,
        bepoch=0.0,
        avgoverc=0.0,
        lofreq=300.0,
        chanwidth=0.390625,
        bestdm=29.741,
        topopow=0.0,
        _t=0.0,
        topop1=0.005853475376566149,
        topop2=-0.0,
        topop3=0.0,
        barypow=0.0,
        _b=0.0,
        baryp1=0.0,
        baryp2=0.0,
        baryp3=0.0,
        foldpow=0.0,
        _f=4.591354418360263e-41,
        foldp1=170.8386788476822,
        foldp2=0.0,
        foldp3=0.0,
        orbp=0.0,
        orbe=0.0,
        orbx=0.0,
        orbw=0.0,
        orbt=0.0,
        orbpd=0.0,
        orbwd=0.0,
    )


@test(f"{str(readpfd.__doc__).strip()}")
def _(f=data().joinpath("test.pfd")):
    check(f)


@test(f"{str(writepfd.__doc__).strip()}")
def _(f=data().joinpath("test.pfd")):
    with NamedTemporaryFile(suffix=".pfd") as fp:
        writepfd(readpfd(f), fp.name)
        check(fp.name)
