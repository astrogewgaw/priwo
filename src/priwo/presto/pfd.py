"""
R/W PRESTO folded data (*.pfd) files.
"""

import pabo
import numpy as np

# fmt: off
class PFD(pabo.Struct):

    """
    Specification for PRESTO folded data (*.pfd) files.
    """

    ndms      = pabo.Int(4)
    nperiods  = pabo.Int(4)
    npdots    = pabo.Int(4)
    nsub      = pabo.Int(4)
    npart     = pabo.Int(4)
    nbin      = pabo.Int(4)
    nchan     = pabo.Int(4)
    pstep     = pabo.Int(4)
    pdstep    = pabo.Int(4)
    dmstep    = pabo.Int(4)
    ndmfact   = pabo.Int(4)
    npfact    = pabo.Int(4)
    filename  = pabo.PascalString(pabo.Int(4), "utf8")
    candname  = pabo.PascalString(pabo.Int(4), "utf8")
    telescope = pabo.PascalString(pabo.Int(4), "utf8")
    pgdev     = pabo.PascalString(pabo.Int(4), "utf8")
    rastr     = pabo.String(16, "utf8")
    decstr    = pabo.String(16, "utf8")
    tsamp     = pabo.Float(8)
    startT    = pabo.Float(8)
    endT      = pabo.Float(8)
    tepoch    = pabo.Float(8)
    bepoch    = pabo.Float(8)
    avgoverc  = pabo.Float(8)
    lofreq    = pabo.Float(8)
    chanwidth = pabo.Float(8)
    bestdm    = pabo.Float(8)
    topopow   = pabo.Float(4)
    _t        = pabo.Float(4)
    topop1    = pabo.Float(8)
    topop2    = pabo.Float(8)
    topop3    = pabo.Float(8)
    barypow   = pabo.Float(4)
    _b        = pabo.Float(4)
    baryp1    = pabo.Float(8)
    baryp2    = pabo.Float(8)
    baryp3    = pabo.Float(8)
    foldpow   = pabo.Float(4)
    _f        = pabo.Float(4)
    foldp1    = pabo.Float(8)
    foldp2    = pabo.Float(8)
    foldp3    = pabo.Float(8)
    orbp      = pabo.Float(8)
    orbe      = pabo.Float(8)
    orbx      = pabo.Float(8)
    orbw      = pabo.Float(8)
    orbt      = pabo.Float(8)
    orbpd     = pabo.Float(8)
    orbwd     = pabo.Float(8)
# fmt: on


def readpfd(f):

    """
    Read in a PRESTO folded data (*.pfd) file.
    """

    pfd = {}
    with open(f, "rb") as fp:
        meta = PFD().parse_stream(fp)
        for key, shape in {
            "dms": meta["ndms"],
            "periods": meta["nperiods"],
            "pdots": meta["npdots"],
            "profs": (meta["nsub"], meta["npart"], meta["nbin"]),
            "stats": (7, meta["nsub"], meta["npart"]),
        }.items():
            meta[key] = np.fromfile(
                fp,
                dtype=np.float64,
                count=np.prod(shape),
            ).reshape(shape)
    data = meta.pop("profs", None)

    pfd["meta"] = meta
    pfd["data"] = data

    return pfd


def writepfd(pfd, f):

    """
    Write out a PRESTO folded data (*.pfd) file.
    """

    pass
