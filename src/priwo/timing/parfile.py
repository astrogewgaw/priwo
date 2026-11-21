"""
R/W TEMPO/TEMPO2 pulsar ephemerides (*.par) files.

The following are the parameters that are accepted in a
par file when trying to determine a pulsar ephemeris.

 PEPOCH   Epoch of period/frequency parameters and position (MJD)
 F0       Pulsar rotation frequency (s-2)
 F        Alternative for F0
 F1       Pulsar rotation frequency derivative (s^-2)
 F2       Pulsar rotation frequency second derivative
 P0       Pulsar period (s).
 P        Alternative for P0
 P1       Pulsar period derivative (10^-15).
 DM       Dispersion measure (pc cm^-3)
 DM1      Dispersion measure time derivative (pc cm^-3 / yr)
 A1       Projected pulsar semi-major axis of 1st orbit
 E        Eccentricity of 1st orbit
 T0       Epoch of periastron passage of 1st orbit (MJD)
 TASC     Epoch of ascending node passage (MJD)
 PB       Period of 1st orbit (days)
 OM       Longitude of periastron passage, 2st orbit (deg)
 EPS1     First Laplace parameter [eccentricity times sin(omega)]
 EPS2     Second Laplace parameter [eccentricity times cos(omega)]
 EPS1DOT  Time derivative of EPS1
 EPS2DOT  Time derivative of EPS2
 OMDOT    Rate of periastron advance (deg/yr)
 PBDOT    Rate of change of orbital period (10^-12)
 XDOT     Rate of change of projected semi-major axis (-12)
 EDOT     Rate of change of eccentricity (-12)

 The following are _not_ currently implemented:
 F3, F4, F5,...  Higher order frequency derivative terms
 OM2DOT   Second time derivative of angle of periastron (rad/s^2)
 X2DOT    Second time derivative of projected semi-major axis (1/s)
"""

import re
from pathlib import Path

from priwo.typing import TextFile


def readpar(fn: str | Path | TextFile) -> dict:
    """
    Read in a TEMPO/TEMPO2 pulsar ephemerides (*.par) file.
    """

    def read(f: TextFile) -> dict:
        meta = {}
        for line in f:
            if line.startswith("#"):
                continue
            line = line.replace("D-", "E-")
            line = line.replace("D+", "E+")
            fields = line.split()
            if len(fields) == 0:
                continue

            key = fields[0]
            if key in ["FILE", "PSR", "PSRJ", "RAJ", "DECJ", "EPHEM", "CLK", "BINARY"]:
                val = fields[1]
                meta[key] = val
            elif key in [
                "PEPOCH",
                "POSEPOCH",
                "DM001",
                "DM002",
                "DM003",
                "DM004",
                "DM",
                "START",
                "FINISH",
                "NTOA",
                "TRES",
                "TZRMJD",
                "TZRFRQ",
                "TZRSITE",
                "NITS",
                "A1",
                "XDOT",
                "E",
                "ECC",
                "EDOT",
                "T0",
                "PB",
                "PBDOT",
                "OM",
                "OMDOT",
                "EPS1",
                "EPS2",
                "EPS1DOT",
                "EPS2DOT",
                "TASC",
                "LAMBDA",
                "BETA",
                "RA_RAD",
                "DEC_RAD",
                "GAMMA",
                "SINI",
                "M2",
                "MTOT",
                "XPBDOT",
                "ELAT",
                "ELONG",
                "PMLAMBDA",
                "PMBETA",
                "PX",
                "PMRA",
                "PMDEC",
                "PB_2",
                "A1_2",
                "E_2",
                "T0_2",
                "OM_2",
            ]:
                try:
                    val = float(fields[1])
                    meta[key] = val
                except ValueError:
                    pass
            elif (match1 := re.search(r"(\D+)(\d+)$", key)) is not None:
                match = match1
                if (match2 := re.search(r"(\D+\d+_)(\d+)$", key)) is not None:
                    match = match2
                if match.group(1) in [
                    "F",
                    "P",
                    "FB",
                    "FD",
                    "DMX_",
                    "DMXEP_",
                    "DMXR1_",
                    "DMXR2_",
                    "DMXF1_",
                    "DMXF2_",
                ]:
                    try:
                        val = float(fields[1])
                        meta[key] = val
                    except ValueError:
                        pass

            if len(fields) == 3 and fields[2] not in ["0", "1"]:
                meta[f"{key}_ERR"] = float(fields[2])
            if len(fields) == 4:
                meta[f"{key}_ERR"] = float(fields[3])

            if (b := meta.get("BETA", None)) is not None:
                meta["ELAT"] = b
            if (l := meta.get("LAMBDA", None)) is not None:
                meta["ELONG"] = l

            if key == "JUMP":
                if (flag := fields[3]) not in ["0", "1"]:
                    meta[f"{key}_{fields[2]}"] = float(flag)
                if len(fields) == 5:
                    if (flag := fields[4]) not in ["0", "1"]:
                        meta[f"{key}_{fields[2]}_ERR"] = float(flag)
                elif len(fields) == 6:
                    meta[f"{key}_{fields[2]}_ERR"] = float(fields[5])
        return meta

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return read(f)
    elif isinstance(fn, TextFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writepar(meta: dict, fn: str | Path | TextFile) -> None:
    """
    Write out a TEMPO/TEMPO2 pulsar ephemerides (*.par) file.
    """

    def write(meta: dict, f: TextFile) -> None:
        f.write("\n".join([f"{key:20} {val:>19}" for key, val in meta.items()]))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "w+") as f:
            write(meta, f)
    elif isinstance(fn, TextFile):
        write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readpar", "writepar"]
