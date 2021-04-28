"""
R/W *.bestprof files.
"""

import re
import numpy as np

from typing import Any, Dict, Tuple
from schema import Or, Use, Schema  # type: ignore


def string_regex(val: Any) -> Any:
    val = str(val)
    if val == "N/A":
        return None
    else:
        return val


def numeric_regex(str: str) -> Any:
    numeric_regex = re.compile(
        """
        [+-]                # Match a `+` or a `-`.
        ?                   # Match between 0 and 1 of the preceding token.
        (?:0|[1-9]\d*)      # Match a single 0, or any non-zero numeric value.
        (?:\.\d*)           # Match zero or more numeric values after a decimal point.
        ?                   # Match between 0 and 1 of the preceding token.
        (?:[eE][+\-]?\d+)   # Match one or more numeric values after an exponent
                            # (indicated by `e` or `E`). The values may be preceded
                            # by a `+` or `-` sign too.
        ?                   # Match between 0 and 1 of the preceding token.
        """,
        re.X,
    )
    nums = re.findall(numeric_regex, str)
    if nums:
        if len(nums) == 1:
            return nums[0]
        else:
            return nums
    else:
        return None


bestprof_map = {
    "fname": string_regex,
    "candname": string_regex,
    "telescope": string_regex,
    "eptopo": numeric_regex,
    "epbary": numeric_regex,
    "tsamp": numeric_regex,
    "nsamp": numeric_regex,
    "davg": numeric_regex,
    "dstd": numeric_regex,
    "nbins": numeric_regex,
    "profavg": numeric_regex,
    "profstd": numeric_regex,
    "chisqr": numeric_regex,
    "nsigma": numeric_regex,
    "dm": numeric_regex,
    "ptopo": numeric_regex,
    "pdtopo": numeric_regex,
    "pddtopo": numeric_regex,
    "pbary": numeric_regex,
    "pdbary": numeric_regex,
    "pddbary": numeric_regex,
    "porb": numeric_regex,
    "asinc": numeric_regex,
    "eccen": numeric_regex,
    "wrad": numeric_regex,
    "tperi": numeric_regex,
}


bestprof_schema = Schema(
    {
        key: Or(
            None,
            Use(value),
        )
        for key, value in bestprof_map.items()
    }
)


bestprof_template = (
    "# Input file       =  {fname}\n"
    "# Candidate        =  {candname}\n"
    "# Telescope        =  {telescope}\n"
    "# Epoch_topo       =  {eptopo}\n"
    "# Epoch_bary       =  {epbary}\n"
    "# T_sample         =  {tsamp}\n"
    "# Data Folded      =  {nsamp}\n"
    "# Data Avg         =  {davg}\n"
    "# Data StdDev      =  {dstd}\n"
    "# Profile Bins     =  {nbins}\n"
    "# Profile Avg      =  {profavg}\n"
    "# Profile StdDev   =  {profstd}\n"
    "# Reduced chi-sqr  =  {chisqr}\n"
    "# Prob(Noise)      <  0   (~{nsigma} sigma)\n"
    "# Best DM          =  {dm}\n"
    "# P_topo (ms)      =  {ptopo}\n"
    "# P'_topo (s/s)    =  {pdtopo}\n"
    "# P''_topo (s/s^2) =  {pddtopo}\n"
    "# P_bary (ms)      =  {pbary}\n"
    "# P'_bary (s/s)    =  {pdbary}\n"
    "# P''_bary (s/s^2) =  {pddbary}\n"
    "# P_orb (s)        =  {porb}\n"
    "# asin(i)/c (s)    =  {asinc}\n"
    "# eccentricity     =  {eccen}\n"
    "# w (rad)          =  {wrad}\n"
    "# T_peri           =  {tperi}\n"
    "######################################################\n"
)


error_template = "{value:16} +/- {error}"


def meta_clean(m: Dict) -> Dict:

    """"""

    d = {}

    for key, val in m.items():
        if isinstance(val, list):
            suffix = "_err"
            err = "".join([key, suffix])
            d[key] = val[0]
            d[err] = val[1]
        else:
            d[key] = val
    return d


def meta_dirty(m: Dict) -> Dict:

    """"""

    d = {}

    for key, value in m.items():

        if value:
            d[key] = value
        else:
            d[key] = "N/A"

        suffix = "_err"
        errkey = "".join([key, suffix])
        error = m.get(errkey, None)

        if error:
            d[key] = error_template.format(
                value=value,
                error=error,
            )

    return d


def read_bestprof(f: str) -> Tuple:

    """"""

    m: Dict[str, Any] = {}

    metex = re.compile(r"^#.*", re.M)
    sepex = re.compile(r"\s+[=<>]\s+")
    numeric_regex = re.compile(r"\d+\.\d+")
    datex = re.compile(r"^\s+\d+\s+(.+)$", re.M)

    with open(f, "r") as fobj:
        lines = fobj.read()

    meta = re.findall(metex, lines)
    data = re.findall(datex, lines)

    meta = meta[:-1]

    keys = bestprof_map.keys()
    values = [re.split(sepex, field)[-1] for field in meta]
    m = {key: value for (key, value) in zip(keys, values)}
    m = bestprof_schema.validate(m)
    m["nsigma"] = m["nsigma"][-1]
    m = meta_clean(m)

    d = np.asarray(data, dtype=np.float32)

    return m, d


def write_bestprof(
    m: Dict,
    d: np.ndarray,
    f: str,
) -> None:

    """"""

    m = meta_dirty(m)

    text = bestprof_template.format(
        fname=m["fname"],
        candname=m["candname"],
        telescope=m["telescope"],
        eptopo=m["eptopo"],
        epbary=m["epbary"],
        tsamp=m["tsamp"],
        nsamp=m["nsamp"],
        davg=m["davg"],
        dstd=m["dstd"],
        nbins=m["nbins"],
        profavg=m["profavg"],
        profstd=m["profstd"],
        chisqr=m["chisqr"],
        nsigma=m["nsigma"],
        dm=m["dm"],
        ptopo=m["ptopo"],
        pdtopo=m["pdtopo"],
        pddtopo=m["pddtopo"],
        pbary=m["pbary"],
        pdbary=m["pdbary"],
        pddbary=m["pddbary"],
        porb=m["porb"],
        asinc=m["asinc"],
        eccen=m["eccen"],
        wrad=m["wrad"],
        tperi=m["tperi"],
    )

    with open(f, "w+") as fobj:
        fobj.write(text)
        for ind, point in enumerate(d):
            fobj.write(
                "{ind:>5}  {point}\n".format(
                    ind=ind,
                    point=point,
                )
            )
