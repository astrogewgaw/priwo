"""
R/W SIGPROC time series (*.tim) files.
"""

from pathlib import Path
from typing import BinaryIO, cast

import numpy as np
from numpy.typing import NDArray

from priwo.bits import pack, unpack
from priwo.sigproc.hdr import readhdr, writehdr


def readtim(fn: str | Path | BinaryIO) -> tuple[dict, np.ndarray]:
    """
    Read in a SIGPROC time series (*.tim) file.

    Parameters
    ----------
    fn : str or pathlib.Path or BinaryIO
        Path to a ``*.tim`` file, or a binary file object positioned at the
        start of the header.

    Returns
    -------
    meta : dict
        The header parameters as key-value pairs. See `readhdr` for details.
    data : numpy.ndarray
        The time series, as a 1D array. Data with 1, 2, 4, or 8 bits per
        sample is returned as ``uint8``, with 1-, 2-, and 4-bit samples
        unpacked to one sample per byte. Data with 16, 32, or 64 bits per
        sample is returned as ``uint16``, ``float32``, or ``float64``
        respectively.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.
    ValueError
        If the file does not begin with a valid SIGPROC header.
    KeyError
        If ``nbits`` in the header is not one of 1, 2, 4, 8, 16, 32, or 64.

    See Also
    --------
    writetim : Write out a SIGPROC time series (*.tim) file.
    readhdr : Read in a SIGPROC header.

    Notes
    -----
    The ``signed`` header keyword is not taken into account: 8-bit data is
    always read as unsigned.

    Examples
    --------
    >>> from priwo.sigproc import readtim
    >>> meta, data = readtim("test_f32.tim")
    >>> tsamp = meta["tsamp"]
    """

    def read(f: BinaryIO) -> tuple[dict, np.ndarray]:
        meta = readhdr(f)
        skip = meta["size"]
        nbits = meta["nbits"]
        endian = meta["endian"]
        data = np.fromfile(
            f,
            dtype={
                1: np.uint8,
                2: np.uint8,
                4: np.uint8,
                8: np.uint8,
                16: np.uint16,
                32: np.float32,
                64: np.float64,
            }[nbits],
            offset=skip,
        )
        if nbits in [1, 2, 4]:
            data = unpack(
                cast(NDArray[np.uint8], data),
                nbits=nbits,
                parallel=True,
                bitorder=endian,
            )
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


def writetim(meta: dict, data: np.ndarray, fn: str | Path | BinaryIO) -> None:
    """
    Write out a SIGPROC time series (*.tim) file.

    Parameters
    ----------
    meta : dict
        The header parameters as key-value pairs. See `writehdr` for details.
        The ``nbits`` and ``endian`` keys are required.
    data : numpy.ndarray
        The time series, as a 1D array. It is written as raw bytes, so its
        dtype should match ``nbits``. For 1-, 2-, and 4-bit data, it should
        be a ``uint8`` array with one sample per byte, which is packed before
        being written.
    fn : str or pathlib.Path or BinaryIO
        Path to the output file, or a binary file object to write to. If a
        path is given, the file is created, or overwritten if it exists.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a writable file object.
    KeyError
        If `meta` is missing ``nbits`` or ``endian``, or contains a key that
        is not a valid SIGPROC keyword.

    See Also
    --------
    readtim : Read in a SIGPROC time series (*.tim) file.
    writehdr : Write out a SIGPROC header.

    Examples
    --------
    >>> from priwo.sigproc import readtim, writetim
    >>> meta, data = readtim("test_f32.tim")
    >>> writetim(meta, data, "copy.tim")
    """

    def write(meta: dict, data: np.ndarray, f: BinaryIO) -> None:
        writehdr(meta, f)
        nbits = meta["nbits"]
        endian = meta["endian"]
        if nbits in [1, 2, 4]:
            data = pack(
                cast(NDArray[np.uint8], data),
                nbits=nbits,
                parallel=True,
                bitorder=endian,
            )
        f.write(data.tobytes())

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(meta, data, f)
    elif hasattr(fn, "write"):
        return write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readtim", "writetim"]
