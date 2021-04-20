import numpy as np

from typing import Dict
from priwo.meta import read_sigproc, write_sigproc


bitstodtypes = {
    8: "<u1",
    16: "<u2",
    32: "<f4",
}


def read_tim(f: str) -> Dict:

    """"""

    tim: Dict = {}
    tim.update(read_sigproc(f))

    with open(f, "rb") as fobj:
        fobj.seek(tim["size"])
        nbits = tim.get("nbits", None)
        if nbits:
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
    f: str,
) -> None:

    """"""

    data = tim.pop("data")
    write_sigproc(tim, f)
    with open(f, "ab") as fobj:
        data.tofile(fobj)
