from ward import test
from ward import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile
from priwo.presto.bpf import readbpf, writebpf


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    assert readbpf(f)["meta"] == dict(
        asini_by_c=None,
        bary_epoch=None,
        candidate="PSR_1646-2142",
        data_avg=11042.9913182359,
        data_std=246.537468521724,
        dm=29.741,
        eccentricity=None,
        filename="J1646-2142_500_200_512_2.15jul2k19.raw0.fil",
        noise_sigma=112.9,
        nsamp=263664000.0,
        p_bary=None,
        p_orb=None,
        p_topo=5.85347537656615,
        p_topo_err=5.16e-08,
        pd_bary=None,
        pd_topo=-0.0,
        pd_topo_err=1.48e-13,
        pdd_bary=None,
        pdd_topo=0.0,
        pdd_topo_err=3.55e-16,
        prof_avg=22747152667.3743,
        prof_bins=128.0,
        prof_std=353837.098935206,
        red_chi_sqr=106.001,
        telescope="GMRT",
        topo_epoch=58679.6856653963,
        t_peri=None,
        tsamp=1.024e-05,
        w=None,
    )


@test(f"{str(readbpf.__doc__).strip()}")
def _(f=data().joinpath("test.bestprof")):
    check(f)


@test(f"{str(writebpf.__doc__).strip()}")
def _(f=data().joinpath("test.bestprof")):
    with NamedTemporaryFile(suffix=".bestprof") as fp:
        writebpf(readbpf(f), fp.name)
        check(fp.name)
