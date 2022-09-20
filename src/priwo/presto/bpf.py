"""
R/W *.bestprof files.
"""

import re
import numpy as np

one = lambda _: _[0]
only = lambda _: _[0] if len(_) == 1 else _
strings = lambda _: None if str(_) == "N/A" else str(_)


def numeral(_):
    matched = re.findall(REGEXPS["numeral"], _)
    return (
        {1: float(one(matched))}.get(
            len(matched),
            [float(_) for _ in matched],
        )
        if matched
        else None
    )


# fmt: off
REGEXPS = {
    "separator": re.compile(r"\s+[=<>]\s+"),
    "header":    re.compile(r"^#.*", re.MULTILINE),
    "profile":   re.compile(r"^\s+\d+\s+(.+)$", re.MULTILINE),
    "numeral":   re.compile(r"[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?"),
}
# fmt: on

# fmt: off
BPFMAP = {
    "filename":     strings,
    "candidate":    strings,
    "telescope":    strings,
    "topo_epoch":   numeral,
    "bary_epoch":   numeral,
    "tsamp":        numeral,
    "nsamp":        numeral,
    "data_avg":     numeral,
    "data_std":     numeral,
    "prof_bins":    numeral,
    "prof_avg":     numeral,
    "prof_std":     numeral,
    "red_chi_sqr":  numeral,
    "noise_sigma":  numeral,
    "dm":           numeral,
    "p_topo":       numeral,
    "pd_topo":      numeral,
    "pdd_topo":     numeral,
    "p_bary":       numeral,
    "pd_bary":      numeral,
    "pdd_bary":     numeral,
    "p_orb":        numeral,
    "asini_by_c":   numeral,
    "eccentricity": numeral,
    "w":            numeral,
    "t_peri":       numeral,
}
# fmt: on


def readbpf(f):

    """
    Read in an *.bestprof file.
    """

    bpf = {}
    meta = {}

    with open(f, "r") as fp:
        lines = fp.read()

    profile = np.asarray(re.findall(REGEXPS["profile"], lines), dtype=np.float32)
    header = re.findall(REGEXPS["header"], lines)
    header = header[:-1]

    for key, val in {
        name: only([validator(_) for _ in string.strip().split("+/-")])
        for (name, validator), string in zip(
            BPFMAP.items(),
            [re.split(REGEXPS["separator"], line)[-1] for line in header],
        )
    }.items():
        if isinstance(val, list):
            meta[key] = val[0]
            meta["".join([key, "_err"])] = val[1]
        else:
            meta[key] = val

    bpf["meta"] = meta
    bpf["data"] = profile

    return bpf
