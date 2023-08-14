from ward import test
from ward import fixture
from pathlib import Path
from priwo import readhdr


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    assert readhdr(f) == dict(
        rawdatafile="./small.fil",
        source_name="src1",
        machine_id=0,
        barycentric=False,
        pulsarcentric=False,
        telescope_id=6,
        src_raj=122637.6361,
        src_dej=135752.112,
        az_start=-1.0,
        za_start=-1.0,
        data_type=0,
        fch1=1465.0,
        foff=-1.0,
        nchans=336,
        nbeams=1,
        ibeam=0,
        nbits=8,
        tstart=58682.620316710374,
        tsamp=0.00126646875,
        nifs=1,
    )


@test(f"{str(readhdr.__doc__).strip()}")
def _(f=data().joinpath("test.fil")):
    check(f)
