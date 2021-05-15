"""
R/W PFD files.
"""

import numpy as np

from pathlib import Path
from typing import Dict, Union

from construct import (
    this,
    Struct,
    Int32ul,
    Int32ub,
    Float32l,
    Float32b,
    Float64l,
    Float64b,
    Computed,
    PascalString,
    PaddedString,
)


def pfdstruct(endian: str) -> Struct:

    """ """

    (Int32u, Float32, Float64) = {
        "big": (
            Int32ub,
            Float32b,
            Float64b,
        ),
        "little": (
            Int32ul,
            Float32l,
            Float64l,
        ),
    }[endian]

    return Struct(
        "numdms" / Int32u,
        "numperiods" / Int32u,
        "numpdots" / Int32u,
        "nsub" / Int32u,
        "npart" / Int32u,
        "proflen" / Int32u,
        "numchan" / Int32u,
        "pstep" / Int32u,
        "pdstep" / Int32u,
        "dmstep" / Int32u,
        "ndmfact" / Int32u,
        "npfact" / Int32u,
        "filename" / PascalString(Int32u, "utf8"),
        "candname" / PascalString(Int32u, "utf8"),
        "telescope" / PascalString(Int32u, "utf8"),
        "pgdev" / PascalString(Int32u, "utf8"),
        "rastr" / PaddedString(16, "utf8"),
        "decstr" / PaddedString(16, "utf8"),
        "tsamp" / Float64,
        "startT" / Float64,
        "endT" / Float64,
        "tepoch" / Float64,
        "bepoch" / Float64,
        "avgoverc" / Float64,
        "lofreq" / Float64,
        "chanwidth" / Float64,
        "bestdm" / Float64,
        "topopow" / Float32,
        "_t" / Float32,
        "topop1" / Float64,
        "topop2" / Float64,
        "topop3" / Float64,
        "barypow" / Float32,
        "_b" / Float32,
        "baryp1" / Float64,
        "baryp2" / Float64,
        "baryp3" / Float64,
        "foldpow" / Float32,
        "_f" / Float32,
        "foldp1" / Float64,
        "foldp2" / Float64,
        "foldp3" / Float64,
        "orbp" / Float64,
        "orbe" / Float64,
        "orbx" / Float64,
        "orbw" / Float64,
        "orbt" / Float64,
        "orbpd" / Float64,
        "orbwd" / Float64,
        "dms" / Float64[this.numdms],
        "periods" / Float64[this.numperiods],
        "pdots" / Float64[this.numpdots],
        "profs" / Float64[this.proflen][this.nsub][this.npart],
        "stats" / Float64[7][this.nsub][this.npart],
        "numprofs" / Computed(this.nsub * this.npart),
    )


def read_pfd(
    f: Union[str, Path],
    endian: str = "little",
) -> Dict:

    if Path(f).exists():
        d = pfdstruct(endian).parse_file(f)
        d = dict(d)
        d.pop("_io")

        keys = [
            "dms",
            "pdots",
            "profs",
            "stats",
            "periods",
        ]

        for key in keys:
            d[key] = np.asarray(d[key])

        return d
    else:
        raise OSError("File not found.")


def write_pfd(
    d: Dict,
    f: Union[str, Path],
    endian: str = "little",
) -> None:

    """ """

    pfdstruct(endian).build_file(d, f)
