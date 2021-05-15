"""
R/W SIGPROC metadata.
"""

import numpy as np

from pathlib import Path
from typing import Any, Dict, Union

from construct import (
    this,
    Const,
    Switch,
    Struct,
    Int8ul,
    Int8ub,
    Int32ul,
    Int32ub,
    Float64l,
    Float64b,
    Container,
    PascalString,
)


telescope_ids = {
    "Fake": 0,
    "Arecibo": 1,
    "ARECIBO 305m": 1,
    "Ooty": 2,
    "Nancay": 3,
    "Parkes": 4,
    "Jodrell": 5,
    "GBT": 6,
    "GMRT": 7,
    "Effelsberg": 8,
    "ATA": 9,
    "SRT": 10,
    "LOFAR": 11,
    "VLA": 12,
    "CHIME": 20,
    "FAST": 21,
    "MeerKAT": 64,
    "KAT-7": 65,
}

ids_telescopes = dict(
    zip(
        telescope_ids.values(),
        telescope_ids.keys(),
    )
)

machine_ids = {
    "FAKE": 0,
    "PSPM": 1,
    "Wapp": 2,
    "WAPP": 2,
    "AOFTM": 3,
    "BCPM1": 4,
    "BPP": 4,
    "OOTY": 5,
    "SCAMP": 6,
    "GBT Pulsar Spigot": 7,
    "SPIGOT": 7,
    "BG/P": 11,
    "PDEV": 12,
    "CHIME+PSR": 20,
    "KAT": 64,
    "KAT-DC2": 65,
}

id_machines = dict(
    zip(
        machine_ids.values(),
        machine_ids.keys(),
    )
)

datatypes = {
    1: "Filterbank file",
    2: "Timeseries file",
}


def sigproc_keys(endian: str) -> Dict[str, Struct]:

    """"""

    (Int8u, Int32u, Float64) = {
        "big": (Int8ub, Int32ub, Float64b),
        "little": (Int8ul, Int32ul, Float64l),
    }[endian]

    return {
        "filename": PascalString(Int32u, "utf8"),
        "telescope_id": Int32u,
        "telescope": PascalString(Int32u, "utf8"),
        "machine_id": Int32u,
        "data_type": Int32u,
        "rawdatafile": PascalString(Int32u, "utf8"),
        "source_name": PascalString(Int32u, "utf8"),
        "barycentric": Int32u,
        "pulsarcentric": Int32u,
        "az_start": Float64,
        "za_start": Float64,
        "src_raj": Float64,
        "src_dej": Float64,
        "tstart": Float64,
        "tsamp": Float64,
        "nbits": Int32u,
        "nsamples": Int32u,
        "fch1": Float64,
        "foff": Float64,
        "fchannel": Float64,
        "nchans": Int32u,
        "nifs": Int32u,
        "refdm": Float64,
        "flux": Float64,
        "period": Float64,
        "nbeams": Int32u,
        "ibeam": Int32u,
        "hdrlen": Int32u,
        "pb": Float64,
        "ecc": Float64,
        "asini": Float64,
        "orig_hdrlen": Int32u,
        "new_hdrlen": Int32u,
        "sampsize": Int32u,
        "bandwidth": Float64,
        "fbottom": Float64,
        "ftop": Float64,
        "obs_date": PascalString(Int32u, "utf8"),
        "obs_time": PascalString(Int32u, "utf8"),
        "signed": Int8u,
        "accel": Float64,
    }


def keystruct(endian: str) -> Struct:

    """"""

    return Struct(
        "key"
        / PascalString(
            {
                "big": Int32ub,
                "little": Int32ul,
            }[endian],
            "utf8",
        ),
        "value"
        / Switch(
            this.key,
            sigproc_keys(endian),
        ),
    )


def start_flag(endian: str) -> Struct:

    """"""

    return Const(
        "HEADER_START",
        PascalString(
            {
                "big": Int32ub,
                "little": Int32ul,
            }[endian],
            "utf8",
        ),
    )


def end_flag(endian: str) -> Struct:

    """"""

    return Const(
        "HEADER_END",
        PascalString(
            {
                "big": Int32ub,
                "little": Int32ul,
            }[endian],
            "utf8",
        ),
    )


def float_coord(f: float) -> float:

    """"""

    sign = np.sign(f)
    x = abs(f)
    hh, x = divmod(x, 10000.0)
    mm, ss = divmod(x, 100.0)
    return float(sign * (hh + mm / 60.0 + ss / 3600.0))


def read_sigproc(
    f: Union[str, Path],
    endian: str = "little",
) -> Dict[str, Any]:

    """"""

    sig: Dict = {}

    cons = []
    with open(f, "rb") as fobj:
        start_flag(endian).parse_stream(fobj)
        while True:
            con = keystruct(endian).parse_stream(fobj)
            if con.key == "HEADER_END":
                break
            cons.append(con)
        size = fobj.tell()
    sig = {con.key: con.value for con in cons}

    try:
        sig["raj"] = float_coord(sig["src_raj"])
        sig["decj"] = float_coord(sig["src_dej"])
    except KeyError:
        pass

    sig["size"] = size

    return sig


def write_sigproc(
    sig: Dict[str, Any],
    f: Union[str, Path],
    endian: str = "little",
) -> None:

    """"""

    sig.pop("raj")
    sig.pop("decj")
    sig.pop("size")

    with open(f, "wb+") as fobj:
        start_flag(endian).build_stream(None, fobj)
        for key, val in sig.items():
            if key in sigproc_keys(endian).keys():
                con = Container()
                con["key"] = key
                con["value"] = val
                keystruct(endian).build_stream(con, fobj)
        end_flag(endian).build_stream(None, fobj)
