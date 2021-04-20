"""
R/W *.fft files.
"""

import numpy as np

from pathlib import Path
from typing import Dict, Tuple, Optional
from priwo.meta import read_inf, write_inf


def read_fft(f: str) -> Dict:

    """"""

    fft: Dict = {}

    inf = Path(f).with_suffix(".inf")
    if not inf.exists():
        msg = "No corresponding *.inf file found. Exiting..."
        raise OSError(msg)
    fft["inf"] = str(inf)
    fft.update(read_inf(fft["inf"]))

    with open(f, "rb") as fobj:
        data = np.fromfile(
            fobj,
            dtype="float32",
        )
    fft["data"] = data

    return fft


def write_fft(
    fft: Dict,
    f: Optional[str] = None,
) -> None:

    """"""

    data = fft.pop("data")

    inf = fft["inf"]
    if not f:
        f = str(Path(inf).with_suffix(".dat"))
    write_inf(fft, inf)

    with open(f, "wb+") as fobj:
        data.tofile(fobj)
