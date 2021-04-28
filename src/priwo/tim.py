import numpy as np

from pathlib import Path
from typing import Dict, Union
from .sigproc import read_sigproc, write_sigproc


bitstodtypes = {
    8: "<u1",
    16: "<u2",
    32: "<f4",
}


def read_tim(f: Union[str, Path]) -> Dict:

    """"""

    tim: Dict = {}
    tim.update(read_sigproc(f))

    with open(f, "rb") as fobj:
        fobj.seek(tim["size"])
        nbits = tim.get("nbits", None)
        if nbits is not None:
            dtype = bitstodtypes[nbits]
            data = np.fromfile(
                fobj,
                dtype=dtype,
            ).astype(np.float32)
        else:
            data = np.fromfile(fobj, dtype=np.float32)
    tim["data"] = data

    return tim


def write_tim(
    tim: Dict,
    f: Union[str, Path],
) -> None:

    """"""

    ctim = tim.copy()

    data = ctim.pop("data")
    write_sigproc(ctim, f)

    with open(f, "ab") as fobj:
        nbits = ctim.get("nbits", None)
        if nbits is not None:
            dtype = bitstodtypes[nbits]
            data.astype(dtype=dtype).tofile(fobj)
        else:
            data.astype(dtype=np.float32).tofile(fobj)
