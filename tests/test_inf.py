from priwo import readinf


def test_radio_inf(datadir):
    assert readinf(str(datadir / "test_radio.inf")) == {
        "name": "fake_presto_radio",
        "telescope": "Parkes",
        "bary": 1,
        "object": "Pulsar",
        "observer": "Kenji Oba",
        "instrument": "Multibeam",
        "mjd": (59000, 0.0),
        "ra": (0, 0, 1.0),
        "dec": (0, 0, -1.0),
        "N": 16.0,
        "dt": 6.4e-05,
        "numonoff": 1,
        "onoff": [(0.0, 15.0)],
        "band": "Radio",
        "dm": 42.42,
        "fov": 981.0,
        "freq": 1182.1953125,
        "num_chan": 1024,
        "freqband": 400.0,
        "chan_wid": 0.390625,
        "analyzer": "Space Sheriff Gavan",
        "notes": "Input filterbank samples have 2 bits.\n",
    }


def test_radio_breaks_inf(datadir):
    assert readinf(str(datadir / "test_radio_breaks.inf")) == {
        "name": "fake_presto_radio_breaks",
        "telescope": "Parkes",
        "bary": 1,
        "object": "Pulsar",
        "observer": "Kenji Oba",
        "instrument": "Multibeam",
        "mjd": (59000, 0.0),
        "ra": (0, 0, 1.0),
        "dec": (0, 0, -1.0),
        "N": 16.0,
        "dt": 6.4e-05,
        "numonoff": 2,
        "onoff": [(0.0, 14.0), (15.0, 15.0)],
        "band": "Radio",
        "dm": 42.42,
        "fov": 981.0,
        "freq": 1182.1953125,
        "num_chan": 1024,
        "freqband": 400.0,
        "chan_wid": 0.390625,
        "analyzer": "Space Sheriff Gavan",
        "notes": "Input filterbank samples have 2 bits.\n",
    }


def test_xray_inf(datadir):
    assert readinf(str(datadir / "test_xray.inf")) == {
        "name": "fake_presto_xray",
        "telescope": "Chandra",
        "bary": 1,
        "object": "Pulsar",
        "observer": "Kenji Oba",
        "instrument": "HRC-S",
        "mjd": (59000, 0.0),
        "ra": (0, 0, 1.0),
        "dec": (0, 0, -1.0),
        "N": 16.0,
        "dt": 6.4e-05,
        "numonoff": 1,
        "onoff": [(0.0, 15.0)],
        "band": "X-ray",
        "fov": 3.0,
        "energy": 1.0,
        "energyband": 5.0,
        "analyzer": "Space Sheriff Gavan",
        "notes": "Full ms-resolution analysis\n",
    }
