import tempfile

from typing import Dict
from pathlib import Path

from priwo.meta import (
    read_inf,
    write_inf,
    read_sigproc,
    write_sigproc,
)


datadir = Path(__file__).parent.joinpath("data")


class TestInf(object):

    """"""

    def check_base(self, inf: Dict) -> None:

        """"""

        assert inf["object"] == "Pulsar"
        assert inf["rastr"] == "00:00:01.0000"
        assert inf["decstr"] == "-00:00:01.0000"
        assert inf["observer"] == "Kenji Oba"
        assert inf["mjd"] == 59000.0
        assert inf["bary"] == True
        assert inf["nsamp"] == 16
        assert inf["tsamp"] == 6.4e-05
        assert inf["analyst"] == "Space Sheriff Gavan"

    def check_radio(self, inf: Dict) -> None:

        """"""

        assert inf["emband"] == "Radio"
        assert inf["bdiam"] == 981.0
        assert inf["dm"] == 42.42
        assert inf["cfreq"] == 1182.1953125
        assert inf["bw"] == 400.0
        assert inf["nchan"] == 1024
        assert inf["chanwid"] == 0.390625
        assert inf["notes"] == ["Input filterbank samples have 2 bits."]

    def check_xray(self, inf: Dict) -> None:

        """"""

        assert inf["emband"] == "X-ray"
        assert inf["fov"] == 3.0
        assert inf["cE"] == 1.0
        assert inf["bpE"] == 5.0
        assert inf["notes"] == ["Full ms-resolution analysis"]
        assert inf["onoffs"] == []

    def test_radio(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_presto_radio.inf")
        inf = read_inf(f)

        assert inf["bsname"] == "fake_presto_radio"
        assert inf["telescope"] == "Parkes"
        assert inf["instrument"] == "Multibeam"
        assert inf["breaks"] == False
        assert inf["onoffs"] == []
        self.check_base(inf)
        self.check_radio(inf)

    def test_radio_breaks(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_presto_radio_breaks.inf")
        inf = read_inf(f)

        assert inf["bsname"] == "fake_presto_radio_breaks"
        assert inf["telescope"] == "Parkes"
        assert inf["instrument"] == "Multibeam"
        assert inf["breaks"] == True
        assert inf["onoffs"] == [(0, 14), (15, 15)]
        self.check_base(inf)
        self.check_radio(inf)

    def test_xray(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_presto_xray.inf")
        inf = read_inf(f)

        assert inf["bsname"] == "fake_presto_xray"
        assert inf["telescope"] == "Chandra"
        assert inf["instrument"] == "HRC-S"
        assert inf["breaks"] == False
        self.check_base(inf)
        self.check_xray(inf)

    def test_write(self) -> None:

        """"""

        with tempfile.NamedTemporaryFile(suffix=".inf") as obj:
            tf = Path(obj.name)
            f = datadir.joinpath("test_fake_presto_radio.inf")
            inf = read_inf(f)
            write_inf(inf, tf)
            test = read_inf(tf)
            assert test["bsname"] == "fake_presto_radio"
            assert test["telescope"] == "Parkes"
            assert test["instrument"] == "Multibeam"
            assert test["breaks"] == False
            assert test["onoffs"] == []
            self.check_base(test)
            self.check_radio(test)


class TestHdr(object):

    """"""

    def check_data(self, inf: Dict) -> None:

        """"""

        assert inf["source_name"] == "Pulsar"
        assert inf["telescope_id"] == 4
        assert inf["machine_id"] == 10
        assert inf["src_raj"] == 63642.23
        assert inf["src_dej"] == -454405.0
        assert inf["az_start"] == 0.0
        assert inf["za_start"] == 0.0
        assert inf["data_type"] == 2
        assert inf["refdm"] == 26.31
        assert inf["fch1"] == 1581.8046875
        assert inf["barycentric"] == 0
        assert inf["nchans"] == 1
        assert inf["nbits"] == 32
        assert inf["tstart"] == 56771.1303125
        assert inf["tsamp"] == 6.4e-05
        assert inf["nifs"] == 1
        assert inf["raj"] == 6.611730555555556
        assert inf["decj"] == -45.734722222222224
        assert inf["size"] == 314

    def test_read(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_sigproc_float32.tim")
        sig = read_sigproc(f)
        self.check_data(sig)

    def test_write(self) -> None:

        """"""

        with tempfile.NamedTemporaryFile(suffix=".tim") as obj:
            tf = Path(obj.name)
            f = datadir.joinpath("test_fake_sigproc_float32.tim")
            tim = read_sigproc(f)
            write_sigproc(tim, tf)
            test = read_sigproc(tf)
            self.check_data(test)
