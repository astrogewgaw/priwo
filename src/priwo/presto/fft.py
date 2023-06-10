"""
R/W PRESTO FFT (*.fft) files.
"""

import pabo as pb
from pathlib import Path
from priwo.presto.inf import readinf
from priwo.presto.inf import writeinf


def readfft(f):
    """
    Read in a PRESTO FFT (*.fft) file.
    """

    return (readinf(Path(f).with_suffix(".inf")), pb.Array(pb.Float(4)).parse(f))


def writefft(meta, data, f):
    """
    Write out a PRESTO FFT (*.fft) file.
    """

    writeinf(meta, Path(f).with_suffix(".inf"))
    pb.Array(pb.Float(4)).build(data, f)
