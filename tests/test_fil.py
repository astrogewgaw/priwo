import numpy as np
from priwo import readfil


def test_1bit_fil(datadir):
    _, data = readfil(str(datadir / "test_1bit.fil"))
    data = np.asarray(data)
    assert np.allclose(
        data[64, 100:110],
        np.asarray(
            [
                1,
                0,
                0,
                1,
                1,
                0,
                0,
                1,
                1,
                0,
            ],
            dtype=np.uint8,
        ),
    )


def test_2bit_fil(datadir):
    _, data = readfil(str(datadir / "test_2bit.fil"))
    data = np.asarray(data)
    assert np.allclose(
        data[64, 100:110],
        np.asarray(
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
            dtype=np.uint8,
        ),
    )


def test_4bit_fil(datadir):
    _, data = readfil(str(datadir / "test_4bit.fil"))
    data = np.asarray(data)
    assert np.allclose(
        data[64, 100:110],
        np.asarray(
            [
                6,
                5,
                9,
                5,
                5,
                12,
                10,
                4,
                8,
                7,
            ],
            dtype=np.uint8,
        ),
    )


def test_8bit_fil(datadir):
    _, data = readfil(str(datadir / "test_8bit.fil"))
    data = np.asarray(data)
    assert np.allclose(
        data[64, 100:110],
        np.asarray(
            [
                121,
                94,
                94,
                124,
                151,
                118,
                132,
                74,
                112,
                65,
            ],
            dtype=np.uint8,
        ),
    )


def test_32bit_fil(datadir):
    _, data = readfil(str(datadir / "test_32bit.fil"))
    data = np.asarray(data)
    assert np.allclose(
        data[64, 100:110],
        np.asarray(
            [
                1.166237,
                -0.84468514,
                0.874816,
                1.4028563,
                -0.98618776,
                -0.80890864,
                -1.6307002,
                1.1306021,
                0.50498164,
                -1.6316832,
            ],
            dtype=np.float32,
        ),
    )
