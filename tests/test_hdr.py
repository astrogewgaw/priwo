from ward import test
from ward import fixture
from pathlib import Path
from priwo import readhdr


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    assert readhdr(f) == dict(
        az_start=-1.0,
        barycentric=False,
        data_type=0,
        endian="little",
        fch1=1465.0,
        foff=-1.0,
        ibeam=0,
        machine_id=0,
        nbeams=1,
        nbits=8,
        nchans=336,
        nifs=1,
        nsamples=10,
        pulsarcentric=False,
        rawdatafile="./small.fil",
        source_name="src1",
        src_dej=135752.112,
        src_raj=122637.6361,
        telescope_id=6,
        tsamp=0.00126646875,
        tstart=58682.620316710374,
        za_start=-1.0,
    )


@test(f"{str(readhdr.__doc__).strip()}")
def _(f=data().joinpath("test.fil")):
    check(f)
