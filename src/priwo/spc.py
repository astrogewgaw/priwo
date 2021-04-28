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

    spec: Dict = {}
    spec.update(read_sigproc(f))

    with open(f, "rb") as fobj:
        fobj.seek(spec["size"])
        nbits = spec.get("nbits", None)
        if nbits:
            dtype = bitstodtypes[nbits]
            data = np.fromfile(
                fobj,
                dtype=dtype,
            ).astype(np.float32)
        else:
            data = np.fromfile(fobj, dtype=np.float32)
    spec["data"] = data

    return spec


def write_spc(
    spec: Dict,
    f: Union[str, Path],
) -> None:

    """"""

    cspec = spec.copy()

    data = cspec.pop("data")
    write_sigproc(cspec, f)
    with open(f, "ab") as fobj:
        nbits = cspec.get("nbits", None)
        if nbits is not None:
            dtype = bitstodtypes[nbits]
            data.astype(dtype=dtype).tofile(fobj)
        else:
            data.astype(dtype=np.float32).tofile(fobj)
