from ward import test
from ward import fixture
from pathlib import Path
from priwo.others import readpolycos
from priwo.others import writepolycos
from tempfile import NamedTemporaryFile


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    assert readpolycos(f)[0]["meta"] == dict(
        name="1646-2142",
        date="14-JUL-19",
        utc="50000.00",
        tmid=58678.2083333333,
        dm=29.741,
        doppler=0.605,
        rms=-6.064,
        refphz=30728623742.9709,
        reff0=170.849389109675,
        obsno=27,
        span=60.0,
        ncoeff=12,
        freq=399.805,
        binphz=105.0,
    )


@test(f"{str(readpolycos.__doc__).strip()}")
def _(f=data().joinpath("test.polycos")):
    check(f)


@test(f"{str(writepolycos.__doc__).strip()}")
def _(f=data().joinpath("test.polycos")):
    with NamedTemporaryFile(suffix=".polycos") as fp:
        writepolycos(readpolycos(f), fp.name)
        check(fp.name)
