"""
R/W PRESTO best pulse profile (*.bestprof) files.
"""

import re
from pathlib import Path
from typing import TextIO

import numpy as np


def readbpf(fn: str | Path | TextIO) -> tuple[dict, np.ndarray]:
    """
    Read in a PRESTO best pulse profile (*.bestprof) file.

    The header lines (those beginning with ``#``) are parsed into a dictionary
    of metadata, and the profile data that follow are parsed into an array.

    Parameters
    ----------
    fn : str or pathlib.Path or TextIO
        Path to a ``*.bestprof`` file, or a text file object to read from.

    Returns
    -------
    meta : dict
        The header parameters as key-value pairs. Numerical values are parsed
        as floats, and string values (``filename``, ``candidate``, and
        ``telescope``) are kept as strings. Header values that are not
        available (such as ``"N/A"``) are set to ``None``. For parameters that
        come with an uncertainty, the uncertainty is stored under a separate
        key with an ``_err`` suffix (for example, ``ptopo`` and ``ptopo_err``).
        The keys are:

        - ``filename``, ``candidate``, ``telescope``: Input file, candidate
          name, and telescope.
        - ``tepoch``, ``bepoch``: Topocentric and barycentric epochs (MJD).
        - ``tsamp``: Sampling time.
        - ``nsamp``: Number of samples folded.
        - ``datamean``, ``datastdv``: Mean and standard deviation of the data.
        - ``nbins``: Number of bins in the profile.
        - ``profmean``, ``profstdv``: Mean and standard deviation of the
          profile.
        - ``redchisqr``: Reduced chi-squared of the profile.
        - ``sigma``: Significance of the profile (in units of sigma).
        - ``dm``: Best dispersion measure (pc cm^-3).
        - ``ptopo``, ``pdtopo``, ``pddtopo``: Topocentric period (ms), and its
          first (s/s) and second (s/s^2) derivatives.
        - ``pbary``, ``pdbary``, ``pddbary``: Barycentric period (ms), and its
          first (s/s) and second (s/s^2) derivatives.
        - ``porb``: Orbital period (s).
        - ``asinibyc``: Projected semi-major axis (lt-s).
        - ``eccentricity``: Orbital eccentricity.
        - ``w``: Longitude of periastron (rad).
        - ``tperi``: Epoch of periastron passage.
    data : numpy.ndarray
        The best pulse profile, as a 1D array of floats with one value per
        phase bin.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.
    KeyError
        If the header contains a keyword that is not recognised.

    See Also
    --------
    writebpf : Write out a PRESTO best pulse profile (*.bestprof) file.

    Examples
    --------
    >>> from priwo.presto import readbpf
    >>> meta, profile = readbpf("test.bestprof")
    >>> dm, nbins = meta["dm"], meta["nbins"]
    """

    def read(f: TextIO) -> tuple[dict, np.ndarray]:
        def numerals(s: str) -> float | list[float] | None:
            regex = re.compile(r"[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?")
            numbers = regex.findall(s)
            if len(numbers) == 0:
                return None
            numbers = list(map(float, numbers))
            return numbers[0] if len(numbers) == 1 else numbers

        bpfkeys = {
            "Input file": ("filename", str),
            "Candidate": ("candidate", str),
            "Telescope": ("telescope", str),
            "Epoch_topo": ("tepoch", numerals),
            "Epoch_bary": ("bepoch", numerals),
            "T_sample": ("tsamp", numerals),
            "Data Folded": ("nsamp", numerals),
            "Data Avg": ("datamean", numerals),
            "Data StdDev": ("datastdv", numerals),
            "Profile Bins": ("nbins", numerals),
            "Profile Avg": ("profmean", numerals),
            "Profile StdDev": ("profstdv", numerals),
            "Reduced chi-sqr": ("redchisqr", numerals),
            "Prob(Noise)": ("sigma", numerals),
            "Best DM": ("dm", numerals),
            "P_topo (ms)": ("ptopo", numerals),
            "P'_topo (s/s)": ("pdtopo", numerals),
            "P''_topo (s/s^2)": ("pddtopo", numerals),
            "P_bary (ms)": ("pbary", numerals),
            "P'_bary (s/s)": ("pdbary", numerals),
            "P''_bary (s/s^2)": ("pddbary", numerals),
            "P_orb (s)": ("porb", numerals),
            "asin(i)/c (s)": ("asinibyc", numerals),
            "eccentricity": ("eccentricity", numerals),
            "w (rad)": ("w", numerals),
            "T_peri": ("tperi", numerals),
        }

        meta = {}
        lines = f.read()
        hdr = re.findall(r"^#.*", lines, re.MULTILINE)[:-1]
        for hdrln in hdr:
            key, val = re.split(r"\s+[=<>]\s+", hdrln)
            key = key[2:]
            name, x = bpfkeys[key]
            val = x(val)
            if isinstance(val, list):
                if name == "sigma":
                    meta[name] = val[-1]
                else:
                    val, err = val
                    meta[name] = val
                    meta[f"{name}_err"] = err
            else:
                meta[name] = val
        data = map(float, re.findall(r"^\s+\d+\s+(.+)$", lines, re.MULTILINE))
        data = np.asarray(list(data))
        return meta, data

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return read(f)
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writebpf(meta: dict, data: np.ndarray, fn: str | Path | TextIO) -> None:
    """
    Write out a PRESTO best pulse profile (*.bestprof) file.

    Parameters
    ----------
    meta : dict
        The header parameters as key-value pairs, with the same keys as those
        returned by `readbpf`. Values set to ``None`` are written as ``"N/A"``,
        and uncertainties stored under keys with an ``_err`` suffix are written
        alongside their parameters as ``"<value> +/- <error>"``.
    data : numpy.ndarray
        The best pulse profile, as a 1D array with one value per phase bin.
        Each value is written on its own line, preceded by its bin index.
    fn : str or pathlib.Path or TextIO
        Path to the output file, or a text file object to write to.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a writable file object.
    KeyError
        If `meta` is missing any of the keys required to write the header.

    See Also
    --------
    readbpf : Read in a PRESTO best pulse profile (*.bestprof) file.

    Examples
    --------
    >>> from priwo.presto import readbpf, writebpf
    >>> meta, profile = readbpf("test.bestprof")
    >>> with open("copy.bestprof", "w") as f:
    ...     writebpf(meta, profile, f)
    """

    def write(meta: dict, data: np.ndarray, f: TextIO) -> None:
        strings = {}
        for key, val in meta.items():
            err = meta.get(f"{key}_err", None)
            val = f"{val!s}" if val is not None else "N/A"
            val = val.rstrip("0").rstrip(".") if isinstance(val, float) else val
            strings[key] = f"{val:17} +/- {err}" if err is not None else f"{val}"
        f.write(
            "\n".join(
                [
                    f"# Input file       =  {strings['filename']}",
                    f"# Candidate        =  {strings['candidate']}",
                    f"# Telescope        =  {strings['telescope']}",
                    f"# Epoch_topo       =  {strings['tepoch']}",
                    f"# Epoch_bary       =  {strings['bepoch']}",
                    f"# T_sample         =  {strings['tsamp']}",
                    f"# Data Folded      =  {strings['nsamp']}",
                    f"# Data Avg         =  {strings['datamean']}",
                    f"# Data StdDev      =  {strings['datastdv']}",
                    f"# Profile Bins     =  {strings['nbins']}",
                    f"# Profile Avg      =  {strings['profmean']}",
                    f"# Profile StdDev   =  {strings['profstdv']}",
                    f"# Reduced chi-sqr  =  {strings['redchisqr']}",
                    f"# Prob(Noise)      <  0   (~{strings['sigma']} sigma)",
                    f"# Best DM          =  {strings['dm']}",
                    f"# P_topo (ms)      =  {strings['ptopo']}",
                    f"# P'_topo (s/s)    =  {strings['pdtopo']}",
                    f"# P''_topo (s/s^2) =  {strings['pddtopo']}",
                    f"# P_bary (ms)      =  {strings['pbary']}",
                    f"# P'_bary (s/s)    =  {strings['pdbary']}",
                    f"# P''_bary (s/s^2) =  {strings['pddbary']}",
                    f"# P_orb (s)        =  {strings['porb']}",
                    f"# asin(i)/c (s)    =  {strings['asinibyc']}",
                    f"# eccentricity     =  {strings['eccentricity']}",
                    f"# w (rad)          =  {strings['w']}",
                    f"# T_peri           =  {strings['tperi']}",
                    "######################################################",
                ]
            )
        )
        f.write("\n")
        f.writelines(f"{i:>4}  {value:e}\n" for i, value in enumerate(data))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return write(meta, data, f)
    elif hasattr(fn, "write"):
        return write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readbpf", "writebpf"]
