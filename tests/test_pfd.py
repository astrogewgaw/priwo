from ward import test
from ward import fixture
from pathlib import Path
from priwo import readpfd


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    meta, _ = readpfd(f)

    for _ in [
        "dms",
        "pdots",
        "stats",
        "periods",
    ]:
        meta.pop(_)

    assert meta == dict(
        bary_p=0.0,
        bary_pd=0.0,
        bary_pdd=0.0,
        bary_power=0.0,
        bepoch=0.0,
        bestdm=29.741,
        candname="PSR_1646-2142",
        dec="-21:42:08.9063",
        df=0.390625,
        dmstep=1,
        dt=1.024e-05,
        endian="little",
        f0=300.0,
        filename="J1646-2142_500_200_512_2.15jul2k19.raw0.fil",
        fold_p=170.8386788476822,
        fold_pd=0.0,
        fold_pdd=0.0,
        fold_power=6.9527192090977e-310,
        nbin=128,
        nchan=512,
        ndmfact=1,
        ndms=257,
        npart=60,
        npdots=201,
        nperiods=201,
        npfact=1,
        nsub=128,
        orb_e=0.0,
        orb_p=0.0,
        orb_pd=0.0,
        orb_t=0.0,
        orb_w=0.0,
        orb_wd=0.0,
        orb_x=0.0,
        pdstep=2,
        pgdev="J1646-2142_500_200_512_2.15jul2k19.raw0.new_freq_PSR_1646-2142.pfd.ps/CPS",
        pstep=1,
        ra="16:46:18.1250",
        t0=0.0,
        telescope="GMRT",
        tepoch=58679.6856653963,
        tn=1.0,
        topo_p=0.005853475376566149,
        topo_pd=-0.0,
        topo_pdd=0.0,
        topo_power=0.0,
        vavg=0.0,
    )


@test(f"{str(readpfd.__doc__).strip()}")
def _(f=data().joinpath("test.pfd")):
    check(f)
