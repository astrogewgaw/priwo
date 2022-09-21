"""
R/W *.inf files.
"""

import re

boolean = lambda _: int(_) != 0
splits = lambda _: [int(__) for __ in _.split(",")]
string = lambda _: {True: "1", False: "0"}.get(_, str(_))

# fmt: off
INFMAP = {
    "Data file name without suffix":         ("filename",     str),
    "Telescope used":                        ("telescope",    str),
    "Instrument used":                       ("instrument",   str),
    "Object being observed":                 ("object",       str),
    "J2000 Right Ascension (hh:mm:ss.ssss)": ("ra",           str),
    "J2000 Declination     (dd:mm:ss.ssss)": ("dec",          str),
    "Data observed by":                      ("observer",     str),
    "Epoch of observation (MJD)":            ("mjd",          float),
    "Barycentered?           (1=yes, 0=no)": ("barycentered", boolean),
    "Barycentered?           (1 yes, 0 no)": ("barycentered", boolean),
    "Number of bins in the time series":     ("nsamples",     int),
    "Width of each time series bin (sec)":   ("samptime",     float),
    "Any breaks in the data? (1=yes, 0=no)": ("breaks",       boolean),
    "Any breaks in the data? (1 yes, 0 no)": ("breaks",       boolean),
    "Type of observation (EM band)":         ("emband",       str),
    "Beam diameter (arcsec)":                ("beamdiam",     float),
    "Dispersion measure (cm-3 pc)":          ("dm",           float),
    "Central freq of low channel (MHz)":     ("cfreq",        float),
    "Total bandwidth (MHz)":                 ("bw",           float),
    "Number of channels":                    ("nchannels",    int),
    "Channel bandwidth (MHz)":               ("chanwidth",    float),
    "Field-of-view diameter (arcsec)":       ("fov",          float),
    "Central energy (kev)":                  ("cE",           float),
    "Energy bandpass (kev)":                 ("bpE",          float),
    "Photometric filter used":               ("filter",       str),
    "Central wavelength (nm)":               ("cwaveln",      float),
    "Bandpass (nm)":                         ("bandpass",     float),
    "Data analyzed by":                      ("analyst",      str),
}
# fmt: on


def readinf(f):

    """
    Read in an *.inf file.
    """

    meta = {}

    regex = re.compile(
        r"""
        ^               # Beginning of string.
        \s+             # Trailing whitespace, if any.
        (?P<key>.+?)    # Capture key.
        \s+=\s+         # Separator.
        (?P<val>.+?)    # Capture value.
        \s+             # Trailing whitespace, if any.
        $               # End of line.
        """,
        re.MULTILINE | re.VERBOSE,
    )

    notes = []
    onoffs = []
    with open(f, "r") as lines:
        for line in lines:
            matched = re.search(regex, line)
            if matched:
                groups = matched.groupdict()
                key = groups["key"]
                val = groups["val"]
                try:
                    nameof, typeof = INFMAP[key]
                    meta[nameof] = typeof(val)
                except KeyError:
                    onoffs.append(splits(val))
            else:
                notes.append(line)
    notes = notes[1:]
    notes = [note.strip() for note in notes]
    notes = [note for note in notes if note]
    notes = " ".join(notes)
    meta["onoffs"] = onoffs
    meta["notes"] = notes
    return meta


def writeinf(meta, f):

    """
    Write out an *.inf file.
    """

    notes = meta.pop("notes")
    onoffs = meta.pop("onoffs")
    frame = " {key:<37s}  =  {val:s}"
    lines = [frame.format(key={name: key for key, (name, _) in INFMAP.items()})]

    if meta["breaks"]:
        lines[12:12] = [
            frame.format(
                val="{:<11d}, {:d}".format(*onoff),
                key="On/Off bin pair #{npair:>3}".format(npair=i + 1),
            )
            for i, onoff in enumerate(onoffs)
        ]

    with open(f, "w+") as fp:
        fp.write("\n".join(lines))
        fp.write("\n Any additional notes:\n")
        for note in notes:
            fp.write("    {note}\n".format(note=note))
