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

    return (readinf(Path(f).with_suffix(".inf")), np.fromfile(f, dtype=np.float32))


def writefft(meta, data, f):
    """
    Write out a PRESTO FFT (*.fft) file.
    """

    writeinf(meta, Path(f).with_suffix(".inf"))
    data.tofile(f)
