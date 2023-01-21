"""
R/W PRESTO folded data (*.pfd) files.
"""

import pabo as pb
import numpy as np


# fmt: off
Position = pb.Spec(
    fields=dict(
        power = pb.Float(8) / "Power normalized with local power.",
        p     = pb.Float(8) / "r if rzw search, r_startfft if bin search.",
        pd    = pb.Float(8) / "z if rzw search, r_freqmod if bin search.",
        pdd   = pb.Float(8) / "w if rzw search, numfftbins if bin search.",
    )
)
# fmt: on


# fmt: off
PFD = pb.Spec(
    fields=dict(
        ndms      = pb.Int(4) / "Number of trial DMs.",
        nperiods  = pb.Int(4) / "Number of trial periods.",
        npdots    = pb.Int(4) / "Number of trial period derivatives.",
        nsub      = pb.Int(4) / "Number of frequency subbands folded.",
        npart     = pb.Int(4) / "Number of folds in time over integration.",
        nbin      = pb.Int(4) / "Number of bins per profile.",
        nchan     = pb.Int(4) / "Number of channels for radio data.",
        pstep     = pb.Int(4) / "Minimum period stepsize in profile phase bins.",
        pdstep    = pb.Int(4) / "Minimum p-dot stepsize in profile phase bins.",
        dmstep    = pb.Int(4) / "Minimum DM stepsize in profile phase bins.",
        ndmfact   = pb.Int(4) / "2 * ndmfact * proflen + 1 DMs to search.",
        npfact    = pb.Int(4) / "2 * npfact * proflen + 1 periods and p-dots to search.",
        filename  = pb.PascalString(pb.Int(4), "utf8") / "Filename of the folded data.",
        candname  = pb.PascalString(pb.Int(4), "utf8") / "String describing the candidate.",
        telescope = pb.PascalString(pb.Int(4), "utf8") / "Telescope where observation took place.",
        pgdev     = pb.PascalString(pb.Int(4), "utf8") / "PGPLOT device to use.",
        ra        = pb.PaddedString(16, "utf8") / "J2000 RA  string in format hh:mm:ss.ssss.",
        dec       = pb.PaddedString(16, "utf8") / "J2000 DEC string in format dd:mm:ss.ssss.",
        dt        = pb.Float(8) / "Sampling interval of the data.",
        T0        = pb.Float(8) / "Fraction of observation file to start folding.",
        Tn        = pb.Float(8) / "Fraction of observation file to stop folding.",
        tepoch    = pb.Float(8) / "Topocentric eopch of data in MJD.",
        bepoch    = pb.Float(8) / "Barycentric eopch of data in MJD.",
        vavg      = pb.Float(8) / "Average topocentric velocity.",
        f0        = pb.Float(8) / "Center of low frequency radio channel.",
        df        = pb.Float(8) / "Width of each radio channel in MHz.",
        bestdm    = pb.Float(8) / "Best DM.",
        topo      = Position / "Best topocentric p, pd, and pdd.",
        bary      = Position / "Best barycentric p, pd, and pdd.",
        fold      = Position / "f, fd, and fdd used to fold the initial data.",
        orb=pb.Spec(
            fields=dict(
                p  = pb.Float(8) / "Orbital period (s).",
                e  = pb.Float(8) / "Orbital eccentricity.",
                x  = pb.Float(8) / "Projected semi-major axis (lt-sec).",
                w  = pb.Float(8) / "Longitude of periapsis (deg).",
                t  = pb.Float(8) / "Time since last periastron passage (s).",
                pd = pb.Float(8) / "Orbital period derivative (s/yr).",
                wd = pb.Float(8) / "Advance of longitude of periapsis (deg/yr).",
            )
        ) / "Barycentric orbital parameters used in folds.",
    )
)
# fmt: on


def readpfd(f):

    """
    Read in a PRESTO folded data (*.pfd) file.
    """

    pfd = {}
    with open(f, "rb") as fp:
        meta = PFD.parse(fp)
        for key, shape in {
            "dms": meta["ndms"],
            "periods": meta["nperiods"],
            "pdots": meta["npdots"],
            "profs": (meta["npart"], meta["nsub"], meta["nbin"]),
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

    with open(f, "wb+") as fp:
        PFD.build(pfd["meta"], fp)
        for key in ["dms", "periods", "pdots"]:
            pfd["meta"][key].tofile(fp)
        pfd["data"].tofile(fp)
        pfd["meta"]["stats"].tofile(fp)
