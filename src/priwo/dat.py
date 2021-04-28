import numpy as np

from pathlib import Path
from typing import Any, Dict, Union
from .inf import read_inf, write_inf


def read_dat(f: Union[str, Path]) -> Dict:

    """"""

    dat: Dict = {}

    inf = Path(f).with_suffix(".inf")
    if not inf.exists():
        raise OSError(
            """
            No corresponding *.inf file found.
            Exiting...
            """.replace(
                "\n",
                " ",
            ).strip()
        )
    dat.update(read_inf(inf))

    with open(f, "rb") as fobj:
        data = np.fromfile(
            fobj,
            dtype="float32",
        )
    dat["data"] = data

    return dat


def write_dat(
    dat: Dict[str, Any],
    f: Union[str, Path],
) -> None:

    """"""

    cdat = dat.copy()

    data = cdat.pop("data")
    write_inf(
        cdat,
        str(Path(f).with_suffix(".inf")),
    )
    with open(f, "wb+") as fobj:
        data.tofile(fobj)
