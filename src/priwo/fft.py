"""
R/W *.fft files.
"""

import numpy as np

from pathlib import Path
from typing import Dict, Union
from .inf import read_inf, write_inf


def read_fft(f: str) -> Dict:

    """"""

    fft: Dict = {}

    inf = Path(f).with_suffix(".inf")
    if not inf.exists():
        msg = "No corresponding *.inf file found. Exiting..."
        raise OSError(msg)
    fft.update(read_inf(inf))

    with open(f, "rb") as fobj:
        data = np.fromfile(
            fobj,
            dtype="float32",
        )
    fft["data"] = data

    return fft


def write_fft(
    fft: Dict,
    f: Union[str, Path],
) -> None:

    """"""

    cfft = fft.copy()

    data = cfft.pop("data")

    write_inf(
        cfft,
        Path(f).with_suffix(".inf"),
    )

    with open(f, "wb+") as fobj:
        data.tofile(fobj)
