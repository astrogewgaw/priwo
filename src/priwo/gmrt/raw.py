from pathlib import Path

import numpy as np

from priwo.gmrt.ahdr import readgmrtahdr, writegmrtahdr
from priwo.gmrt.hdr import readgmrthdr, writegmrthdr
from priwo.typing import BinaryFile


def readgmrt(fn: str | Path | BinaryFile) -> tuple[dict, np.ndarray]:
    def read(f: BinaryFile) -> tuple[dict, np.ndarray]:
        meta = readgmrthdr(str(f.name) + ".hdr")
        nbits = meta["nbits"]
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
        )
        if nbits in [1, 2, 4]:
            pass
        data = data.reshape(-1, meta["nf"]).T
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


def writegmrt(meta: dict, data: np.ndarray, fn: str | Path | BinaryFile) -> None:
    def write(meta: dict, data: np.ndarray, f: BinaryFile) -> None:
        writegmrthdr(meta, str(f.name) + ".hdr")
        f.write(data.T.tobytes())

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            write(meta, data, f)
    elif isinstance(fn, BinaryFile):
        write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def readgmrt2(fn: str | Path | BinaryFile) -> tuple[dict, np.ndarray]:
    def read(f: BinaryFile) -> tuple[dict, np.ndarray]:
        meta = readgmrtahdr(str(f.name) + ".ahdr")
        nbits = meta["nbits"]
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
        )
        if nbits in [1, 2, 4]:
            pass
        data = data.reshape(-1, meta["nf"]).T
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


def writegmrt2(meta: dict, data: np.ndarray, fn: str | Path | BinaryFile) -> None:
    def write(meta: dict, data: np.ndarray, f: BinaryFile) -> None:
        writegmrtahdr(meta, str(f.name) + ".ahdr")
        f.write(data.T.tobytes())

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            write(meta, data, f)
    elif isinstance(fn, BinaryFile):
        write(meta, data, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)
