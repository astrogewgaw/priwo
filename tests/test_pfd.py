import numpy as np

from ward import test
from ward import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile
from priwo.presto.pfd import readpfd, writepfd


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    meta = readpfd(f)["meta"]
    for _ in [
        "dms",
        "pdots",
        "stats",
        "periods",
    ]:
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
        ra="16:46:18.1250",
        dec="-21:42:08.9063",
        dt=1.024e-05,
        T0=0.0,
        Tn=1.0,
        tepoch=58679.6856653963,
        bepoch=0.0,
        vavg=0.0,
        f0=300.0,
        df=0.390625,
        bestdm=29.741,
        topo=dict(
            power=0.0,
            p=0.005853475376566149,
            pd=-0.0,
            pdd=0.0,
        ),
        bary=dict(
            power=0.0,
            p=0.0,
            pd=0.0,
            pdd=0.0,
        ),
        fold=dict(
            power=6.9527192090977e-310,
            p=170.8386788476822,
            pd=0.0,
            pdd=0.0,
        ),
        orb=dict(
            p=0.0,
            e=0.0,
            x=0.0,
            w=0.0,
            t=0.0,
            pd=0.0,
            wd=0.0,
        ),
    )


@test(f"{str(readpfd.__doc__).strip()}")
def _(f=data().joinpath("test.pfd")):
    check(f)


@test(f"{str(writepfd.__doc__).strip()}")
def _(f=data().joinpath("test.pfd")):
    with NamedTemporaryFile(suffix=".pfd") as fp:
        writepfd(readpfd(f), fp.name)
        check(fp.name)
