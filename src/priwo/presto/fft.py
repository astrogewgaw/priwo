"""
R/W PRESTO FFT (*.fft) files.
"""

import numpy as np
from pathlib import Path
from priwo.presto.inf import readinf
from priwo.presto.inf import writeinf


def readfft(f):

    """
    Read in a PRESTO FFT (*.fft) file.
    """

    meta = readinf(Path(f).with_suffix(".inf"))
    data = np.fromfile(f, dtype=np.float32)
    return {"meta": meta, "data": data}


def writefft(fft, f):

    """
    Write out a PRESTO FFT (*.fft) file.
    """

    writeinf(fft["meta"], Path(f).with_suffix(".inf"))
    fft["data"].tofile(f)
