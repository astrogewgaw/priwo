"""
R/W SIGPROC time series (*.tim) files.
"""

from pathlib import Path
from typing import cast

import numpy as np
from numpy.typing import NDArray

from priwo.bits import pack, unpack
from priwo.sigproc.hdr import readhdr, writehdr
from priwo.typing import BinaryFile


def readtim(fn: str | Path | BinaryFile) -> tuple[dict, np.ndarray]:
    """
    Read in a SIGPROC time series (*.tim) file.
    """

    def read(f: BinaryFile) -> tuple[dict, np.ndarray]:
        meta = readhdr(f)
        nbits = meta["nbits"]
        endian = meta["endian"]
        dtype = np.dtype(
            {
                1: np.uint8,
                2: np.uint8,
                4: np.uint8,
                32: np.float32,
                64: np.float64,
                8: np.int8 if meta.get("signed", False) else np.uint8,
                16: np.int16 if meta.get("signed", False) else np.uint16,
            }[nbits]
        )
        data = np.fromfile(f, dtype=dtype.newbyteorder(endian))
        return meta, unpack(
            cast(NDArray[np.uint8], data),
            nbits=nbits,
            parallel=True,
            bitorder="little",
        ) if nbits in [1, 2, 4] else data

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif isinstance(fn, BinaryFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writetim(meta: dict, data: np.ndarray, fn: str | Path | BinaryFile) -> None:
    """
    Write out a SIGPROC time series (*.tim) file.
    """

    def write(meta: dict, data: np.ndarray, f: BinaryFile) -> None:
        if data.size == 0:
            raise ValueError("NO DATA TO WRITE. ABORT.")
        if data.ndim != 1:
            raise ValueError("DATA OF WRONG SHAPE. ABORT.")
        if (nf := meta.get("nchans", 1)) != 1:
            raise ValueError(f"METADATA HAS WRONG NUMBER OF CHANNELS (= {nf}). ABORT.")

        nbits = meta["nbits"]
        endian = meta["endian"]
        if (
            data.dtype.newbyteorder("=")
            != (
                {
                    1: np.uint8,
                    2: np.uint8,
                    4: np.uint8,
                    32: np.float32,
                    64: np.float64,
                    8: np.int8 if meta.get("signed", False) else np.uint8,
                    16: np.int16 if meta.get("signed", False) else np.uint16,
                }[nbits]
            )
        ):
            raise TypeError("DATA OF WRONG TYPE. ABORT.")
        writehdr(meta, f)
        f.write(
            (
                pack(
                    cast(NDArray[np.uint8], data),
                    nbits=nbits,
                    parallel=True,
                    bitorder="little",
                )
                if nbits in [1, 2, 4]
                else data.astype(data.dtype.newbyteorder(endian), copy=False)
            ).tobytes()
        )

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(meta, data, f)
    elif isinstance(fn, BinaryFile):
        return write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readtim", "writetim"]
