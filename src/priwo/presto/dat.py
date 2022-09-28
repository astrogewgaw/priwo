"""
R/W PRESTO time series (*.dat) files.
"""

import numpy as np
from pathlib import Path
from priwo.presto.inf import readinf
from priwo.presto.inf import writeinf


def readdat(f):

    """
    Read in a PRESTO time series (*.dat) file.
    """

    meta = readinf(Path(f).with_suffix(".inf"))
    data = np.fromfile(f, dtype=np.float32)
    return {"meta": meta, "data": data}


def writedat(dat, f):

    """
    Write out a PRESTO time series (*.dat) file.
    """

    writeinf(dat["meta"], Path(f).with_suffix(".inf"))
    dat["data"].tofile(f)
