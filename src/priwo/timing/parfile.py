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
from typing import TextIO


def readpar(fn: str | Path | TextIO) -> dict:
    """
    Read in a TEMPO/TEMPO2 pulsar ephemerides (*.par) file.

    Lines beginning with ``#`` and blank lines are skipped, and Fortran-style
    exponents (such as ``1.0D-12``) are converted to Python-style exponents
    before parsing.

    Parameters
    ----------
    fn : str or pathlib.Path or TextIO
        Path to a ``*.par`` file, or a text file object to read from.

    Returns
    -------
    dict
        The ephemeris parameters as key-value pairs, keyed by their names in
        the file (such as ``F0`` or ``PSRJ``). Values are parsed as follows:

        - String parameters (``FILE``, ``PSR``, ``PSRJ``, ``RAJ``, ``DECJ``,
          ``EPHEM``, ``CLK``, and ``BINARY``) are kept as strings.
        - Recognised numerical parameters, including numbered ones (such as
          ``F1``, ``FB0``, ``FD1``, or ``DMX_0001``), are parsed as floats.
          Values that cannot be parsed are skipped.
        - Uncertainties are stored under a separate key with an ``_ERR``
          suffix (for example, ``F0_ERR``).
        - ``JUMP`` lines are stored under ``JUMP_<flag value>`` (and
          ``JUMP_<flag value>_ERR`` for their uncertainties).
        - ``BETA`` and ``LAMBDA``, if present, are also copied to ``ELAT``
          and ``ELONG``.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.

    See Also
    --------
    writepar : Write out a TEMPO/TEMPO2 pulsar ephemerides (*.par) file.

    Notes
    -----
    Parameters that are not recognised are skipped, and fit flags (``0`` or
    ``1`` after a value) are not stored.

    Examples
    --------
    >>> from priwo.timing import readpar
    >>> par = readpar("test.par")
    >>> f0, f0err = par["F0"], par["F0_ERR"]
    """

    def read(f: TextIO) -> dict:
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
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writepar(meta: dict, fn: str | Path | TextIO) -> None:
    """
    Write out a TEMPO/TEMPO2 pulsar ephemerides (*.par) file.

    Each key-value pair in `meta` is written on its own line, with the key
    left-aligned in a 20-character column and the value right-aligned in a
    19-character column.

    Parameters
    ----------
    meta : dict
        The ephemeris parameters as key-value pairs, keyed by their names in
        the par file (such as ``F0`` or ``PSRJ``).
    fn : str or pathlib.Path or TextIO
        Path to the output file, or a text file object to write to. If a
        path is given, the file is created, or overwritten if it exists.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a writable file object.

    See Also
    --------
    readpar : Read in a TEMPO/TEMPO2 pulsar ephemerides (*.par) file.

    Notes
    -----
    Keys with an ``_ERR`` suffix, as returned by `readpar`, are written as
    separate lines rather than next to their parameters, and no fit flags
    are written.

    Examples
    --------
    >>> from priwo.timing import writepar
    >>> writepar({"PSRJ": "J0000+0000", "F0": 1.0, "DM": 10.0}, "test.par")
    """

    def write(meta: dict, f: TextIO) -> None:
        f.write("\n".join([f"{key:20} {val:>19}" for key, val in meta.items()]))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "w+") as f:
            write(meta, f)
    elif hasattr(fn, "write"):
        write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readpar", "writepar"]
