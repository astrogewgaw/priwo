"""
R/W *.inf files.
"""

import re

from pathlib import Path

from typing import (
    Any,
    List,
    Dict,
    Tuple,
    Union,
)


def tobool(s: str) -> bool:
    return int(s) != 0


def tostr(b: Any) -> str:
    if isinstance(b, bool):
        return {
            True: "1",
            False: "0",
        }[b]
    else:
        return str(b)


def onoff(p: str) -> Tuple[int, int]:
    a, b = p.split(",")
    return int(a), int(b)


getmap = {
    "Data file name without suffix": ("bsname", str),
    "Telescope used": ("telescope", str),
    "Instrument used": ("instrument", str),
    "Object being observed": ("object", str),
    "J2000 Right Ascension (hh:mm:ss.ssss)": ("rastr", str),
    "J2000 Declination     (dd:mm:ss.ssss)": ("decstr", str),
    "Data observed by": ("observer", str),
    "Epoch of observation (MJD)": ("mjd", float),
    "Barycentered?           (1=yes, 0=no)": ("bary", tobool),
    "Barycentered?           (1 yes, 0 no)": ("bary", tobool),
    "Number of bins in the time series": ("nsamp", int),
    "Width of each time series bin (sec)": ("tsamp", float),
    "Any breaks in the data? (1=yes, 0=no)": ("breaks", tobool),
    "Any breaks in the data? (1 yes, 0 no)": ("breaks", tobool),
    "Type of observation (EM band)": ("emband", str),
    "Beam diameter (arcsec)": ("bdiam", float),
    "Dispersion measure (cm-3 pc)": ("dm", float),
    "Central freq of low channel (MHz)": ("cfreq", float),
    "Total bandwidth (MHz)": ("bw", float),
    "Number of channels": ("nchan", int),
    "Channel bandwidth (MHz)": ("chanwid", float),
    "Field-of-view diameter (arcsec)": ("fov", float),
    "Central energy (kev)": ("cE", float),
    "Energy bandpass (kev)": ("bpE", float),
    "Photometric filter used": ("filter", str),
    "Field-of-view diameter (arcsec)": ("fov", float),
    "Central wavelength (nm)": ("cwaveln", float),
    "Bandpass (nm)": ("bandpass", float),
    "Data analyzed by": ("analyst", str),
}

putmap = {nvar: dvar for dvar, (nvar, tvar) in getmap.items()}


def read_inf(f: Union[str, Path]) -> Dict:

    """ """

    inf: Dict = {}

    regex = re.compile(
        r"""
        ^               # Beginning of string.
        \s+             # Trailing whitespace, if any.
        (?P<descp>.+?)  # Capture description.
        \s+=\s+         # Separator.
        (?P<value>.+?)  # Capture value.
        \s+             # Trailing whitespace, if any.
        $               # End of line.
        """,
        re.MULTILINE | re.VERBOSE,
    )

    extras: List[str] = []
    onoffs: List[Tuple[int, int]] = []

    with open(f, "r") as fobj:
        for line in fobj:
            match = re.search(regex, line)
            if match:
                mdict = match.groupdict()
                descp = mdict["descp"]
                value = mdict["value"]
                try:
                    (nvar, tvar) = getmap[descp]
                    inf[nvar] = tvar(value)  # type: ignore
                except KeyError:
                    onoffs.append(onoff(value))
            else:
                extras.append(line)
    extras = extras[1:]
    extras = [extra.strip() for extra in extras]
    extras = [extra for extra in extras if extra]
    inf["notes"] = extras
    inf["onoffs"] = onoffs
    return inf


def write_inf(
    inf: Dict[str, Any],
    f: Union[str, Path],
) -> None:

    """ """

    notes = inf.pop("notes")
    onoffs = inf.pop("onoffs")

    template = " {descp:<37s}  =  {value:s}"

    lines = [
        template.format(
            descp=putmap[key],
            value=tostr(value),
        )
        for key, value in inf.items()
    ]

    if inf["breaks"]:
        extras = [
            template.format(
                descp="On/Off bin pair #{npair:>3}".format(npair=i + 1),
                value="{:<11d}, {:d}".format(*onoff),
            )
            for i, onoff in enumerate(onoffs)
        ]
        lines[12:12] = extras

    with open(f, "w+") as fobj:
        fobj.write("\n".join(lines))
        fobj.write("\n")
        fobj.write(" Any additional notes:")
        fobj.write("\n")
        [fobj.write("    {note}\n".format(note=note)) for note in notes]
