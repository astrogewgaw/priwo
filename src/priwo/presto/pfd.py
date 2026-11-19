"""
R/W PRESTO folded data (*.pfd) files.
"""

import struct
from pathlib import Path
from typing import BinaryIO

import numpy as np


def readpfd(fn: str | Path | BinaryIO) -> dict:
    """
    Read in a PRESTO folded data (*.pfd) file.

    The byte order of the file is detected automatically: the first five
    integers are read as little-endian, and if any of them is implausibly
    large (greater than 100000 in magnitude), the file is read as big-endian.

    Parameters
    ----------
    fn : str or pathlib.Path or BinaryIO
        Path to a ``*.pfd`` file, or a binary file object to read from.

    Returns
    -------
    dict
        The contents of the file as key-value pairs. The keys are:

        - ``ndms``, ``nperiods``, ``npdots``: Number of trial DMs, periods,
          and period derivatives.
        - ``nsub``, ``npart``: Number of frequency subbands and time
          subintegrations folded.
        - ``nbins``: Number of bins per profile.
        - ``nprofs``: Number of profiles (``nsub * npart``).
        - ``nchan``: Number of channels in the radio data.
        - ``pstep``, ``pdstep``, ``dmstep``: Minimum period, period
          derivative, and DM step sizes, in profile phase bins.
        - ``ndmfact``, ``npfact``: Factors setting the number of trial DMs
          (``2 * ndmfact * nbins + 1``) and trial periods and period
          derivatives (``2 * npfact * nbins + 1``) to search.
        - ``filename``, ``candname``, ``telescope``, ``pgdev``: Name of the
          folded file, candidate name, telescope, and PGPLOT device.
        - ``ra``, ``dec``: J2000 right ascension (``hh:mm:ss.ssss``) and
          declination (``dd:mm:ss.ssss``), as bytes.
        - ``tsamp``: Sampling time (s).
        - ``startT``, ``endT``: Fractions of the observation at which folding
          started and stopped.
        - ``tepoch``, ``bepoch``: Topocentric and barycentric epochs (MJD).
        - ``avgvoverc``: Average topocentric velocity (as a fraction of c).
        - ``lofreq``: Centre frequency of the lowest channel (MHz).
        - ``chanwid``: Width of each channel (MHz).
        - ``bestdm``: Best DM (pc cm^-3).
        - ``topo``, ``bary``: Dictionaries with the best topocentric and
          barycentric ``power``, period (``p``), and its first (``pd``) and
          second (``pdd``) derivatives.
        - ``fold``: Dictionary with the ``power``, frequency (``f``, ``fd``,
          ``fdd``), and period (``p``, ``pd``, ``pdd``) and their
          derivatives used to fold the data.
        - ``orbital``: Dictionary with the barycentric orbital parameters
          used to fold the data: period (``p``, s), eccentricity (``e``),
          projected semi-major axis (``x``, lt-s), longitude of periastron
          (``w``, deg), time since last periastron passage (``t``, s),
          orbital period derivative (``pd``, s/yr), and advance of
          periastron (``wd``, deg/yr).
        - ``dms``, ``periods``, ``pdots``: Trial DMs, periods, and period
          derivatives, as 1D arrays of ``float64``.
        - ``profs``: Folded profiles, as an array of ``float64`` with shape
          ``(npart, nsub, nbins)``.
        - ``endian``: Byte order of the file (``"little"`` or ``"big"``).

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.

    See Also
    --------
    writepfd : Write out a PRESTO folded data (*.pfd) file.

    Examples
    --------
    >>> from priwo.presto import readpfd
    >>> pfd = readpfd("test.pfd")
    >>> profile = pfd["profs"].sum(axis=(0, 1))
    """

    def read(f: BinaryIO) -> dict:
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

        ra = (data := f.read(16))[: data.find(b"\0")]
        dec = (data := f.read(16))[: data.find(b"\0")]
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

        foldp = 1.0 / foldf
        foldpd = -foldfd / (foldf * foldf)
        foldpdd = (
            0.0
            if foldfdd == 0.0
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

        dms = np.asarray(f.read(ndms * 8), dtype=swp + "f8")
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
            "endian": {">": "big", "<": "little"}[swp],
        }

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writepfd(pfd: dict, fn: str | Path | BinaryIO) -> None:
    """
    Write out a PRESTO folded data (*.pfd) file.

    Parameters
    ----------
    pfd : dict
        The contents of the file as key-value pairs. Along with the scalar
        and string keys returned by `readpfd`, the following keys are
        required:

        - ``topopow``, ``topop``, ``topopd``, ``topopdd``: Best topocentric
          power, period, and its first and second derivatives.
        - ``barypow``, ``baryp``, ``barypd``, ``barypdd``: Best barycentric
          power, period, and its first and second derivatives.
        - ``foldpow``, ``foldf``, ``foldfd``, ``foldfdd``: Power, frequency,
          and its first and second derivatives used to fold the data.
        - ``orbp``, ``orbe``, ``orbx``, ``orbw``, ``orbt``, ``orbpd``,
          ``orbwd``: Barycentric orbital parameters used to fold the data.
        - ``dms``, ``periods``, ``pdots``, ``profs``, ``stats``: Trial DMs,
          periods, and period derivatives, folded profiles, and profile
          statistics, as arrays.

        The value of ``endian`` (``"little"`` or ``"big"``) sets the byte
        order of the written file.
    fn : str or pathlib.Path or BinaryIO
        Path to the output file, or a binary file object to write to. If a
        path is given, the file is created, or overwritten if it exists.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a writable file object.
    KeyError
        If `pfd` is missing any of the required keys, or if ``endian`` is not
        ``"little"`` or ``"big"``.

    See Also
    --------
    readpfd : Read in a PRESTO folded data (*.pfd) file.

    Notes
    -----
    The topocentric, barycentric, fold, and orbital parameters are taken
    from flat keys (such as ``topop``), not from the nested dictionaries
    (such as ``pfd["topo"]["p"]``) returned by `readpfd`. Arrays are written
    as raw bytes, so they should already have the byte order set by
    ``endian``.
    """

    def write(pfd: dict, f: BinaryIO) -> None:
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
            f.write(struct.pack(swp + "i", len(val)))
            f.write(val.encode("utf-8"))

        for key in ["ra", "dec"]:
            val = pfd[key]
            pad = 16 - len(val)
            f.write(val.encode("utf-8") + "\x00" * pad)

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

        f.write(struct.pack(swp + "f" * 2, pfd["topopow"], 0.0))
        f.write(struct.pack(swp + "d" * 3, pfd["topop"], pfd["topopd"], pfd["topopdd"]))

        f.write(struct.pack(swp + "f" * 2, pfd["barypow"], 0.0))
        f.write(struct.pack(swp + "d" * 3, pfd["baryp"], pfd["barypd"], pfd["barypdd"]))

        f.write(struct.pack(swp + "f" * 2, pfd["foldpow"], 0.0))
        f.write(struct.pack(swp + "d" * 3, pfd["foldf"], pfd["foldfd"], pfd["foldfdd"]))

        f.write(
            struct.pack(
                swp + "d" * 7,
                pfd["orbp"],
                pfd["orbe"],
                pfd["orbx"],
                pfd["orbw"],
                pfd["orbt"],
                pfd["orbpd"],
                pfd["orbwd"],
            )
        )

        f.write(pfd["dms"].tobytes())
        f.write(pfd["periods"].tobytes())
        f.write(pfd["pdots"].tobytes())
        f.write(pfd["profs"].tobytes())
        f.write(pfd["stats"].tobytes())

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(pfd, f)
    elif hasattr(fn, "write"):
        return write(pfd, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readpfd", "writepfd"]
