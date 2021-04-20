"""
R/W *.spec files.
"""

import numpy as np

from typing import Dict, Tuple
from priwo.meta import read_sigproc, write_sigproc


bitstodtypes = {
    8: "<u1",
    16: "<u2",
    32: "<f4",
}


def read_spec(f: str) -> Dict:

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


def write_spec(
    spec: Dict,
    f: str,
) -> None:

    """"""

    data = spec.pop("data")
    write_sigproc(spec, f)
    with open(f, "ab") as fobj:
        data.tofile(fobj)
