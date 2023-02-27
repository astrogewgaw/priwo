from ward import test
from ward import fixture
from pathlib import Path
from tempfile import NamedTemporaryFile
from priwo.presto.inf import readinf, writeinf


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


def check(f):
    assert readinf(f) == dict(
        analyst="Space Sheriff Gavan",
        barycentered=True,
        beamdiam=981.0,
        breaks=False,
        bw=400.0,
        cfreq=1182.1953125,
        chanwidth=0.390625,
        dec="-00:00:01.0000",
        dm=42.42,
        emband="Radio",
        filename="fake_presto_radio",
        instrument="Multibeam",
        mjd=59000.0,
        nchannels=1024,
        notes="Input filterbank samples have 2 bits.",
        nsamples=16,
        object="Pulsar",
        observer="Kenji Oba",
        onoffs=[],
        ra="00:00:01.0000",
        samptime=6.4e-05,
        telescope="Parkes",
    )


def check_breaks(f):
    assert readinf(f) == dict(
        analyst="Space Sheriff Gavan",
        barycentered=True,
        beamdiam=981.0,
        breaks=True,
        bw=400.0,
        cfreq=1182.1953125,
        chanwidth=0.390625,
        dec="-00:00:01.0000",
        dm=42.42,
        emband="Radio",
        filename="fake_presto_radio_breaks",
        instrument="Multibeam",
        mjd=59000.0,
        nchannels=1024,
        notes="Input filterbank samples have 2 bits.",
        nsamples=16,
        object="Pulsar",
        observer="Kenji Oba",
        onoffs=[[0, 14], [15, 15]],
        ra="00:00:01.0000",
        samptime=6.4e-05,
        telescope="Parkes",
    )


def check_xray(f):
    assert readinf(f) == dict(
        analyst="Space Sheriff Gavan",
        barycentered=True,
        bpE=5.0,
        breaks=False,
        cE=1.0,
        dec="-00:00:01.0000",
        emband="X-ray",
        filename="fake_presto_xray",
        fov=3.0,
        instrument="HRC-S",
        mjd=59000.0,
        notes="Full ms-resolution analysis",
        nsamples=16,
        object="Pulsar",
        observer="Kenji Oba",
        onoffs=[],
        ra="00:00:01.0000",
        samptime=6.4e-05,
        telescope="Chandra",
    )


@test(f"{str(readinf.__doc__).strip()}, for radio data.")
def _(f=data().joinpath("test_radio.inf")):
    check(f)


@test(f"{str(readinf.__doc__).strip()}, for radio data, but with breaks.")
def _(f=data().joinpath("test_radio_breaks.inf")):
    check_breaks(f)


@test(f"{str(readinf.__doc__).strip()} for xray data.")
def _(f=data().joinpath("test_xray.inf")):
    check_xray(f)


@test(f"{str(writeinf.__doc__).strip()}, for radio data.")
def _(f=data().joinpath("test_radio.inf")):
    with NamedTemporaryFile(suffix=".inf") as fp:
        writeinf(readinf(f), fp.name)
        check(fp.name)


@test(f"{str(writeinf.__doc__).strip()}, for radio data, but with breaks.")
def _(f=data().joinpath("test_radio_breaks.inf")):
    with NamedTemporaryFile(suffix=".inf") as fp:
        writeinf(readinf(f), fp.name)
        check_breaks(fp.name)


@test(f"{str(writeinf.__doc__).strip()}, for xray data.")
def _(f=data().joinpath("test_xray.inf")):
    with NamedTemporaryFile(suffix=".inf") as fp:
        writeinf(readinf(f), fp.name)
        check_xray(fp.name)
