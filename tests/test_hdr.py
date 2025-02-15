from priwo import readhdr


def test_hdr(datadir):
    assert readhdr(str(datadir / "test.fil")) == {
        "rawdatafile": "./small.fil",
        "source_name": "src1",
        "machine_id": 0,
        "machine": "FAKE",
        "telescope_id": 6,
        "telescope": "GBT",
        "src_raj": 122637.6361,
        "src_dej": 135752.112,
        "az_start": -1.0,
        "za_start": -1.0,
        "datatype": 0,
        "fch1": 1465.0,
        "foff": -1.0,
        "nchans": 336,
        "nbeams": 1,
        "ibeam": 0,
        "nbits": 8,
        "tstart": 58682.620316710374,
        "tsamp": 0.00126646875,
        "nifs": 1,
        "sumifs": 1,
        "hdrlen": 389,
    }
