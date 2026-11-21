"""
R/W PRESTO power spectrum (*.fft) files.
"""

from pathlib import Path

import numpy as np

from priwo.presto.inf import readinf, writeinf
from priwo.typing import BinaryFile


def readfft(fn: str | Path | BinaryFile) -> tuple[dict, np.ndarray]:
    """
    Read in a PRESTO FFT (*.fft) file.
    """

    def read(f: BinaryFile) -> tuple[dict, np.ndarray]:
        inffn = Path(f.name).with_suffix(".inf")
        meta = readinf(inffn)
        data = np.fromfile(f, dtype=np.complex64)
        return meta, data

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif isinstance(fn, BinaryFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writefft(meta: dict, data: np.ndarray, fn: str | Path | BinaryFile):
    """
    Write out a PRESTO FFT (*.fft) file.
    """

    def write(meta: dict, data: np.ndarray, f: BinaryFile):
        inffn = Path(f.name).with_suffix(".inf")
        writeinf(meta, inffn)
        data.tofile(f)

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(meta, data, f)
    elif isinstance(fn, BinaryFile):
        return write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readfft", "writefft"]
