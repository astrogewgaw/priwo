import numpy as np

from pathlib import Path
from typing import Dict, Optional
from priwo.meta import read_inf, write_inf


def read_dat(f: str) -> Dict:

    """"""

    dat: Dict = {}

    inf = Path(f).with_suffix(".inf")
    if not inf.exists():
        raise OSError("No corresponding *.inf file found. Exiting...")
    dat["inf"] = str(inf)
    dat.update(read_inf(dat["inf"]))

    with open(f, "rb") as fobj:
        data = np.fromfile(
            fobj,
            dtype="float32",
        )
    dat["data"] = data

    return dat


def write_dat(
    dat: Dict,
    f: Optional[str] = None,
) -> None:

    """"""

    data = dat.pop("data")
    inf = dat["fname"]
    if not f:
        f = str(Path(inf).with_suffix(".dat"))
    write_inf(dat, inf)
    with open(f, "wb+") as fobj:
        data.tofile(fobj)
