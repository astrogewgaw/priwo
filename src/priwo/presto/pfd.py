"""
R/W PRESTO folded data (*.pfd) files.
"""

import struct
from pathlib import Path

import numpy as np

from priwo.typing import BinaryFile


def readpfd(fn: str | Path | BinaryFile) -> dict:
    """
    Read in a PRESTO folded data (*.pfd) file.
    """

    def read(f: BinaryFile) -> dict:
        swp = "<"
        data = f.read(5 * 4)
        if np.fabs(np.asarray(struct.unpack(swp + "i" * 5, data))).max() > 100000:
            swp = ">"

        (
            ndms,
            nperiods,
            npdots,
            nsub,
            npart,
        ) = struct.unpack(swp + "i" * 5, data)

        nprofs = nsub * npart

        (
            nbins,
            nchan,
            pstep,
            pdstep,
            dmstep,
            ndmfact,
            npfact,
        ) = struct.unpack(swp + "i" * 7, f.read(4 * 7))

        filename = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")
        candname = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")
        telescope = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")
        pgdev = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")

        ra = f.read(16).split(b"\0", 1)[0].decode("utf-8")
        dec = f.read(16).split(b"\0", 1)[0].decode("utf-8")
        (
            tsamp,
            startT,
            endT,
            tepoch,
            bepoch,
            avgvoverc,
            lofreq,
            chanwid,
            bestdm,
        ) = struct.unpack(swp + "d" * 9, f.read(9 * 8))

        topopow, _ = struct.unpack(swp + "f" * 2, f.read(2 * 4))
        topop, topopd, topopdd = struct.unpack(swp + "d" * 3, f.read(3 * 8))

        barypow, _ = struct.unpack(swp + "f" * 2, f.read(2 * 4))
        baryp, barypd, barypdd = struct.unpack(swp + "d" * 3, f.read(3 * 8))

        foldpow, _ = struct.unpack(swp + "f" * 2, f.read(2 * 4))
        foldf, foldfd, foldfdd = struct.unpack(swp + "d" * 3, f.read(3 * 8))

        foldp = 0.0 if foldf == 0.0 else 1.0 / foldf
        foldpd = 0.0 if foldf == 0.0 else -foldfd / (foldf * foldf)
        foldpdd = (
            0.0
            if foldf == 0.0
            else 2.0 * foldfd * foldfd / (foldf**3.0) - foldfdd / (foldf * foldf)
        )

        (
            orbp,
            orbe,
            orbx,
            orbw,
            orbt,
            orbpd,
            orbwd,
        ) = struct.unpack(swp + "d" * 7, f.read(7 * 8))

        dms = np.frombuffer(f.read(ndms * 8), dtype=swp + "f8")
        periods = np.frombuffer(f.read(nperiods * 8), dtype=swp + "f8")
        pdots = np.frombuffer(f.read(npdots * 8), dtype=swp + "f8")
        profs = np.frombuffer(f.read(nprofs * nbins * 8), dtype=swp + "f8")
        profs = profs.reshape((npart, nsub, nbins))

        stats = np.frombuffer(f.read(nprofs * 7 * 8), dtype=swp + "f8")
        stats = stats.reshape((npart, nsub, 7))

        return {
            "ndms": ndms,  # Number of trial DMs.
            "nperiods": nperiods,  # Number of trial periods.
            "npdots": npdots,  # Number of trial period derivatives.
            "nsub": nsub,  # "Number of frequency subbands folded.
            "npart": npart,  # Number of folds in time over integration.
            "nbins": nbins,  # Number of bins per profile.
            "nprofs": nprofs,  # Number of profiles.
            "nchan": nchan,  # "Number of channels for radio data.
            "pstep": pstep,  # Minimum period stepsize in profile phase bins.
            "pdstep": pdstep,  # Minimum p-dot stepsize in profile phase bins.
            "dmstep": dmstep,  # Minimum DM stepsize in profile phase bins.
            "ndmfact": ndmfact,  # 2 * ndmfact * nbin + 1 DMs to search.
            "npfact": npfact,  # 2 * npfact * nbin + 1 periods and p-dots to search.
            "filename": filename,  # Filename of the folded data.
            "candname": candname,  # String describing the candidate.
            "telescope": telescope,  # Telescope where observation took place.
            "pgdev": pgdev,  # PGPLOT device to use.
            "ra": ra,  # J2000 RA  string in format hh:mm:ss.ssss.
            "dec": dec,  # J2000 DEC string in format dd:mm:ss.ssss.
            "tsamp": tsamp,  # Sampling interval of the data.
            "startT": startT,  # Fraction of observation file to start folding.
            "endT": endT,  # Fraction of observation file to stop folding.
            "tepoch": tepoch,  # Topocentric eopch of data in MJD.
            "bepoch": bepoch,  # Barycentric eopch of data in MJD.
            "avgvoverc": avgvoverc,  # Average topocentric velocity.
            "lofreq": lofreq,  # Center of low frequency radio channel.
            "chanwid": chanwid,  # Width of each radio channel in MHz.
            "bestdm": bestdm,  # Best DM.
            "topo": {  # Best topocentric p, pd, and pdd.
                "power": topopow,
                "p": topop,
                "pd": topopd,
                "pdd": topopdd,
            },
            "bary": {  # Best barycentric p, pd, and pdd.
                "power": barypow,
                "p": baryp,
                "pd": barypd,
                "pdd": barypdd,
            },
            "fold": {  # f/p, fd/pd, and fdd/pdd used to fold the initial data.
                "power": foldpow,
                "f": foldf,
                "p": foldp,
                "fd": foldfd,
                "pd": foldpd,
                "fdd": foldfdd,
                "pdd": foldpdd,
            },
            "orbital": {  # Barycentric orbital parameters used in folds.
                "p": orbp,  # Orbital period (s).
                "e": orbe,  # Orbital eccentricity.
                "x": orbx,  # Projected semi-major axis (lt-sec).
                "w": orbw,  # Longitude of periapsis (deg).
                "t": orbt,  # Time since last periastron passage (s).
                "pd": orbpd,  # Orbital period derivative (s/yr).
                "wd": orbwd,  # Advance of longitude of periapsis (deg/yr).
            },
            "dms": dms,
            "periods": periods,
            "pdots": pdots,
            "profs": profs,
            "stats": stats,
            "endian": {">": "big", "<": "little"}[swp],
        }

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif isinstance(fn, BinaryFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writepfd(pfd: dict, fn: str | Path | BinaryFile) -> None:
    """
    Write out a PRESTO folded data (*.pfd) file.
    """

    def write(pfd: dict, f: BinaryFile) -> None:
        swp = {"big": ">", "little": "<"}[pfd["endian"]]
        f.write(
            struct.pack(
                swp + "i" * 12,
                pfd["ndms"],
                pfd["nperiods"],
                pfd["npdots"],
                pfd["nsub"],
                pfd["npart"],
                pfd["nbins"],
                pfd["nchan"],
                pfd["pstep"],
                pfd["pdstep"],
                pfd["dmstep"],
                pfd["ndmfact"],
                pfd["npfact"],
            )
        )

        for key in ["filename", "candname", "telescope", "pgdev"]:
            val = pfd[key]
            val = val.encode("utf-8")
            f.write(struct.pack(swp + "i", len(val)))
            f.write(val)

        for key in ["ra", "dec"]:
            val = pfd[key]
            val = val.encode("utf-8")
            pad = 16 - len(val)
            if pad < 0:
                raise ValueError(f"{key.upper()} LONGER THAN 16 BYTES. ABORT.")
            f.write(val + b"\x00" * pad)

        f.write(
            struct.pack(
                swp + "d" * 9,
                pfd["tsamp"],
                pfd["startT"],
                pfd["endT"],
                pfd["tepoch"],
                pfd["bepoch"],
                pfd["avgvoverc"],
                pfd["lofreq"],
                pfd["chanwid"],
                pfd["bestdm"],
            )
        )

        f.write(struct.pack(swp + "f" * 2, pfd["topo"]["power"], 0.0))
        f.write(
            struct.pack(
                swp + "d" * 3,
                pfd["topo"]["p"],
                pfd["topo"]["pd"],
                pfd["topo"]["pdd"],
            )
        )

        f.write(struct.pack(swp + "f" * 2, pfd["bary"]["power"], 0.0))
        f.write(
            struct.pack(
                swp + "d" * 3,
                pfd["bary"]["p"],
                pfd["bary"]["pd"],
                pfd["bary"]["pdd"],
            )
        )

        f.write(struct.pack(swp + "f" * 2, pfd["fold"]["power"], 0.0))
        f.write(
            struct.pack(
                swp + "d" * 3,
                pfd["fold"]["f"],
                pfd["fold"]["fd"],
                pfd["fold"]["fdd"],
            )
        )

        f.write(
            struct.pack(
                swp + "d" * 7,
                pfd["orbital"]["p"],
                pfd["orbital"]["e"],
                pfd["orbital"]["x"],
                pfd["orbital"]["w"],
                pfd["orbital"]["t"],
                pfd["orbital"]["pd"],
                pfd["orbital"]["wd"],
            )
        )

        f.write(pfd["dms"].astype(swp + "f8").tobytes())
        f.write(pfd["periods"].astype(swp + "f8").tobytes())
        f.write(pfd["pdots"].astype(swp + "f8").tobytes())
        f.write(pfd["profs"].astype(swp + "f8").tobytes())
        f.write(pfd["stats"].astype(swp + "f8").tobytes())

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(pfd, f)
    elif isinstance(fn, BinaryFile):
        return write(pfd, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readpfd", "writepfd"]
