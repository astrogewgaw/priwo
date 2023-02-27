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

    return (readinf(Path(f).with_suffix(".inf")), np.fromfile(f, dtype=np.float32))


def writedat(meta, data, f):
    """
    Write out a PRESTO time series (*.dat) file.
    """

    writeinf(meta, Path(f).with_suffix(".inf"))
    data.tofile(f)
