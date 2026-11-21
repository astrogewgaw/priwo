"""
R/W PRESTO infodata (*.inf) files.
"""

import re
from collections.abc import Callable
from pathlib import Path

from priwo.typing import TextFile

infkeys: dict[str, tuple[str, Callable]] = {
    "Data file name without suffix": ("filename", str),
    "Telescope used": ("telescope", str),
    "Instrument used": ("instrument", str),
    "Object being observed": ("object", str),
    "J2000 Right Ascension (hh:mm:ss.ssss)": ("ra", str),
    "J2000 Declination     (dd:mm:ss.ssss)": ("dec", str),
    "Data observed by": ("observer", str),
    "Epoch of observation (MJD)": ("mjd", float),
    "Barycentered?           (1=yes, 0=no)": ("barycentered", lambda x: int(x) == 1),
    "Barycentered?           (1 yes, 0 no)": ("barycentered", lambda x: int(x) == 1),
    "Number of bins in the time series": ("nsamples", int),
    "Width of each time series bin (sec)": ("samptime", float),
    "Any breaks in the data? (1=yes, 0=no)": ("breaks", lambda x: int(x) == 1),
    "Any breaks in the data? (1 yes, 0 no)": ("breaks", lambda x: int(x) == 1),
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


def readinf(fn: str | Path | TextFile) -> dict:
    """
    Read in a PRESTO infodata (*.inf) file.
    """

    def read(f: TextFile) -> dict:
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
    elif isinstance(fn, TextFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writeinf(meta: dict, fn: str | Path | TextFile) -> None:
    """
    Write out a PRESTO infodata (*.inf) file.
    """

    def write(meta: dict, f: TextFile) -> None:
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
                f"{f' On/Off bin pair #{i + 1:>3}':<37s}  =  {onoff[0]:<11d}, {onoff[1]:d}"
                for i, onoff in enumerate(meta["onoffs"])
            ]
        f.write("\n".join(lines))
        f.write("\n Any additional notes:\n")
        f.writelines(f"    {note}\n" for note in meta["notes"].split("\n"))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "w+") as f:
            return write(meta, f)
    elif isinstance(fn, TextFile):
        return write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readinf", "writeinf"]
