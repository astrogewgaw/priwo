"""
R/W PRESTO infodata (*.inf) files.
"""

import re
from collections.abc import Callable
from pathlib import Path
from typing import TextIO

infkeys: dict[str, tuple[str, Callable]] = {
    "Data file name without suffix": ("filename", str),
    "Telescope used": ("telescope", str),
    "Instrument used": ("instrument", str),
    "Object being observed": ("object", str),
    "J2000 Right Ascension (hh:mm:ss.ssss)": ("ra", str),
    "J2000 Declination     (dd:mm:ss.ssss)": ("dec", str),
    "Data observed by": ("observer", str),
    "Epoch of observation (MJD)": ("mjd", float),
    "Barycentered?           (1=yes, 0=no)": ("barycentered", bool),
    "Barycentered?           (1 yes, 0 no)": ("barycentered", bool),
    "Number of bins in the time series": ("nsamples", int),
    "Width of each time series bin (sec)": ("samptime", float),
    "Any breaks in the data? (1=yes, 0=no)": ("breaks", bool),
    "Any breaks in the data? (1 yes, 0 no)": ("breaks", bool),
    "Type of observation (EM band)": ("emband", str),
    "Beam diameter (arcsec)": ("beamdiam", float),
    "Dispersion measure (cm-3 pc)": ("dm", float),
    "Central freq of low channel (MHz)": ("cfreq", float),
    "Total bandwidth (MHz)": ("bw", float),
    "Number of channels": ("nchannels", int),
    "Channel bandwidth (MHz)": ("chanwidth", float),
    "Field-of-view diameter (arcsec)": ("fov", float),
    "Central energy (kev)": ("cE", float),
    "Energy bandpass (kev)": ("bpE", float),
    "Photometric filter used": ("filter", str),
    "Central wavelength (nm)": ("cwaveln", float),
    "Bandpass (nm)": ("bandpass", float),
    "Data analyzed by": ("analyst", str),
}


def readinf(fn: str | Path | TextIO) -> dict:
    """
    Read in a PRESTO infodata (*.inf) file.

    Parameters
    ----------
    fn : str or pathlib.Path or TextIO
        Path to a ``*.inf`` file, or a text file object to read from.

    Returns
    -------
    dict
        The metadata as key-value pairs. Each descriptive label in the file
        is mapped to a short key (for example, ``"Epoch of observation
        (MJD)"`` becomes ``mjd``) as listed in ``infkeys``, and its value is
        converted to the corresponding type (``str``, ``int``, ``float``, or
        ``bool``). Two more keys are always present:

        - ``onoffs``: A list of ``[on, off]`` bin pairs, one per on/off pair
          in the file. Empty if the data has no breaks.
        - ``notes``: The additional notes at the end of the file, as a single
          string with one note per line.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.

    See Also
    --------
    writeinf : Write out a PRESTO infodata (*.inf) file.

    Notes
    -----
    Which keys are present depends on the observation: radio observations
    include keys such as ``cfreq``, ``bw``, ``nchannels``, and
    ``chanwidth``, while X-ray observations include keys such as ``fov``,
    ``cE``, and ``bpE``.

    Examples
    --------
    >>> from priwo.presto import readinf
    >>> meta = readinf("test.inf")
    >>> mjd, dm = meta["mjd"], meta["dm"]
    """

    def read(f: TextIO) -> dict:
        meta = {}
        notes = []
        onoffs = []
        regex = re.compile(r"^\s+(?P<key>.+?)\s+=\s+(?P<val>.+?)\s+$", re.MULTILINE)
        for line in f:
            if matched := regex.search(line):
                groups = matched.groupdict()
                try:
                    name, conv = infkeys[groups["key"]]
                    meta[name] = conv(groups["val"])
                except KeyError:
                    onoffs.append([int(_) for _ in groups["val"].split(",")])
            else:
                notes.append(line)
        meta["onoffs"] = onoffs

        notes = notes[1:]
        notes = [note.strip() for note in notes]
        notes = [note for note in notes if note]
        notes = "\n".join(notes)
        meta["notes"] = notes

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


def writeinf(meta: dict, fn: str | Path | TextIO) -> None:
    """
    Write out a PRESTO infodata (*.inf) file.

    Parameters
    ----------
    meta : dict
        The metadata as key-value pairs, with the same keys as those returned
        by `readinf`. Keys are written in the order they appear in `meta`,
        with boolean values written as ``1`` or ``0``. The ``breaks``,
        ``onoffs``, and ``notes`` keys are required. If ``breaks`` is true,
        the on/off bin pairs in ``onoffs`` are written as well.
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
        If `meta` contains a key that is not in ``infkeys``, or is missing
        any of the required keys.

    See Also
    --------
    readinf : Read in a PRESTO infodata (*.inf) file.

    Notes
    -----
    The on/off bin pairs are inserted after the first 12 lines, which is
    where PRESTO places them, so `meta` should list its keys in the same
    order as `readinf` returns them.

    Examples
    --------
    >>> from priwo.presto import readinf, writeinf
    >>> meta = readinf("test.inf")
    >>> with open("copy.inf", "w") as f:
    ...     writeinf(meta, f)
    """

    def write(meta: dict, f: TextIO) -> None:
        lines = []
        inv = {name: desc for (desc, (name, _)) in infkeys.items()}
        for key, val in meta.items():
            if key in ["notes", "onoffs"]:
                continue
            lines.append(
                f" {inv[key]:<37s}  = { {True: '1', False: '0'}.get(val, val)!s:s}"
            )
        if meta["breaks"]:
            lines[12:12] = [
                f"{f'On/Off bin pair #{i + 1:>3}':<37s}  =  {onoff[0]:<11d}, {onoff[1]:d}"
                for i, onoff in enumerate(meta["onoffs"])
            ]
        f.write("\n".join(lines))
        f.write("\n Any additional notes:\n")
        f.writelines(f"    {note}\n" for note in meta["notes"].split("\n"))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return write(meta, f)
    elif hasattr(fn, "write"):
        return write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readinf", "writeinf"]
