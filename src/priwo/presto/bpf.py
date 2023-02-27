"""
R/W PRESTO best pulse profile (*.bestprof) files.
"""

import re
import numpy as np


only = lambda _: _[0] if len(_) == 1 else _
strings = lambda _: None if str(_) == "N/A" else str(_)
numex = re.compile(r"[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?")
numeral = (
    lambda _: only(
        list(
            map(
                float,
                re.findall(numex, _),
            )
        )
    )
    if re.search(numex, _)
    else None
)


def readbpf(f):
    """
    Read in a PRESTO best pulse profile (*.bestprof) file.
    """

    meta = {}
    with open(f, "r") as fp:
        lines = fp.read()
        header = re.findall(r"^#.*", lines, re.M)[:-1]
        for key, val in {
            name: only([validator(_) for _ in string.strip().split("+/-")])
            for (name, validator), string in zip(
                {
                    # fmt: off
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
                    # fmt: on
                }.items(),
                [re.split(r"\s+[=<>]\s+", line)[-1] for line in header],
            )
        }.items():
            if isinstance(val, list):
                if key == "noise_sigma":
                    meta[key] = val[-1]
                else:
                    meta[key] = val[0]
                    meta["".join([key, "_err"])] = val[1]
            else:
                meta[key] = val
        data = np.asarray(re.findall(r"^\s+\d+\s+(.+)$", lines, re.M), dtype=np.float32)
    return meta, data


def writebpf(meta, data, f):
    """
    Write out a PRESTO best pulse profile (*.bestprof) file.
    """

    copy = {}
    for key, val in meta.items():
        val = val if val is not None else "N/A"
        error = meta.get("".join([key, "_err"]), None)
        val = f"{val!s}".rstrip("0").rstrip(".") if isinstance(val, float) else val
        copy[key] = f"{val:17} +/- {error}" if error is not None else f"{val}"

    with open(f, "w+") as fp:
        fp.write(
            "\n".join(
                [
                    f"# Input file       =  {copy['filename']}",
                    f"# Candidate        =  {copy['candidate']}",
                    f"# Telescope        =  {copy['telescope']}",
                    f"# Epoch_topo       =  {copy['topo_epoch']}",
                    f"# Epoch_bary       =  {copy['bary_epoch']}",
                    f"# T_sample         =  {copy['tsamp']}",
                    f"# Data Folded      =  {copy['nsamp']}",
                    f"# Data Avg         =  {copy['data_avg']}",
                    f"# Data StdDev      =  {copy['data_std']}",
                    f"# Profile Bins     =  {copy['prof_bins']}",
                    f"# Profile Avg      =  {copy['prof_avg']}",
                    f"# Profile StdDev   =  {copy['prof_std']}",
                    f"# Reduced chi-sqr  =  {copy['red_chi_sqr']}",
                    f"# Prob(Noise)      <  0   (~{copy['noise_sigma']} sigma)",
                    f"# Best DM          =  {copy['dm']}",
                    f"# P_topo (ms)      =  {copy['p_topo']}",
                    f"# P'_topo (s/s)    =  {copy['pd_topo']}",
                    f"# P''_topo (s/s^2) =  {copy['pdd_topo']}",
                    f"# P_bary (ms)      =  {copy['p_bary']}",
                    f"# P'_bary (s/s)    =  {copy['pd_bary']}",
                    f"# P''_bary (s/s^2) =  {copy['pdd_bary']}",
                    f"# P_orb (s)        =  {copy['p_orb']}",
                    f"# asin(i)/c (s)    =  {copy['asini_by_c']}",
                    f"# eccentricity     =  {copy['eccentricity']}",
                    f"# w (rad)          =  {copy['w']}",
                    f"# T_peri           =  {copy['t_peri']}",
                    "######################################################",
                ]
            )
        )
        fp.write("\n")
        for i, value in enumerate(data):
            fp.write(f"{i:>4}  {value:e}\n")
