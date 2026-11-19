"""
R/W PRESTO power spectrum (*.fft) files.
"""

from pathlib import Path
from typing import BinaryIO

import numpy as np

from priwo.presto.inf import readinf, writeinf


def readfft(fn: str | Path | BinaryIO) -> tuple[dict, np.ndarray]:
    """
    Read in a PRESTO FFT (*.fft) file.

    The metadata is read from the accompanying infodata (``*.inf``) file,
    which must exist in the same directory and share the same base name.

    Parameters
    ----------
    fn : str or pathlib.Path or BinaryIO
        Path to a ``*.fft`` file, or a binary file object to read from. A
        file object must have a ``name`` attribute, which is used to locate
        the ``*.inf`` file.

    Returns
    -------
    meta : dict
        The metadata read from the ``*.inf`` file. See `readinf` for details.
    data : numpy.ndarray
        The Fourier transform, as a 1D array of ``complex64`` amplitudes.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.
    FileNotFoundError
        If the accompanying ``*.inf`` file does not exist.

    See Also
    --------
    writefft : Write out a PRESTO FFT (*.fft) file.
    readinf : Read in a PRESTO infodata (*.inf) file.

    Examples
    --------
    >>> import numpy as np
    >>> from priwo.presto import readfft
    >>> meta, data = readfft("test.fft")
    >>> powers = np.abs(data) ** 2
    """

    def read(f: BinaryIO) -> tuple[dict, np.ndarray]:
        inffn = Path(f.name).with_suffix(".inf")
        meta = readinf(inffn)
        data = np.fromfile(f, dtype=np.complex64)
        return meta, data

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writefft(meta: dict, data: np.ndarray, fn: str | Path | BinaryIO):
    """
    Write out a PRESTO FFT (*.fft) file.

    The metadata is written to an accompanying infodata (``*.inf``) file in
    the same directory, with the same base name as the ``*.fft`` file.

    Parameters
    ----------
    meta : dict
        The metadata to write to the ``*.inf`` file. See `writeinf` for
        details.
    data : numpy.ndarray
        The Fourier transform to write. It is written as raw bytes, so it
        should be a 1D array of ``complex64`` amplitudes for PRESTO to read
        it correctly.
    fn : str or pathlib.Path or BinaryIO
        Path to the output file, or a binary file object to write to. A file
        object must have a ``name`` attribute, which is used to name the
        ``*.inf`` file. If a path is given, the file is created, or
        overwritten if it exists.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a writable file object.

    See Also
    --------
    readfft : Read in a PRESTO FFT (*.fft) file.
    writeinf : Write out a PRESTO infodata (*.inf) file.

    Examples
    --------
    >>> from priwo.presto import readfft, writefft
    >>> meta, data = readfft("test.fft")
    >>> writefft(meta, data, "copy.fft")
    """

    def write(meta: dict, data: np.ndarray, f: BinaryIO):
        inffn = Path(f.name).with_suffix(".inf")
        writeinf(meta, inffn)
        data.tofile(f)

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(meta, data, f)
    elif hasattr(fn, "write"):
        return write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readfft", "writefft"]
