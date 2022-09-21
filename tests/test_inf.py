from ward import test
from ward import fixture
from pathlib import Path
from priwo.presto.inf import readinf


@fixture
def data():
    return Path(__file__).parent.joinpath("data")


@test("Read in a *.inf file, for radio data.")
def _(f=data().joinpath("test_fake_presto_radio.inf")):
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


@test("Read in a *.inf file, for radio data, but with breaks.")
def _(f=data().joinpath("test_fake_presto_radio_breaks.inf")):
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


@test("Read in a *.inf file, for xray data.")
def _(f=data().joinpath("test_fake_presto_xray.inf")):
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
