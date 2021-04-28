"""
R/W *.spc files.
"""

import numpy as np

from pathlib import Path
from typing import Dict, Union
from .sigproc import read_sigproc, write_sigproc


bitstodtypes = {
    8: "<u1",
    16: "<u2",
    32: "<f4",
}


def read_spc(f: Union[str, Path]) -> Dict:

    """"""

    spc: Dict = {}
    spc.update(read_sigproc(f))

    with open(f, "rb") as fobj:
        fobj.seek(spc["size"])
        nbits = spc.get("nbits", None)
        if nbits:
            dtype = bitstodtypes[nbits]
            data = np.fromfile(
                fobj,
                dtype=dtype,
            ).astype(np.float32)
        else:
            data = np.fromfile(fobj, dtype=np.float32)
    spc["data"] = data

    return spc


def write_spc(
    spc: Dict,
    f: Union[str, Path],
) -> None:

    """"""

    cspc = spc.copy()

    data = cspc.pop("data")
    write_sigproc(cspc, f)
    with open(f, "ab") as fobj:
        nbits = cspc.get("nbits", None)
        if nbits is not None:
            dtype = bitstodtypes[nbits]
            data.astype(dtype=dtype).tofile(fobj)
        else:
            data.astype(dtype=np.float32).tofile(fobj)
