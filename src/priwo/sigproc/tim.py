"""
R/W SIGPROC time series (*.tim) files.
"""

import numbits
import numpy as np
from priwo.sigproc.hdr import readhdr
from priwo.sigproc.hdr import writehdr


def readtim(f):

    """
    Read in a SIGPROC time series (*.tim) file.
    """

    meta = readhdr(f)
    nbits = meta.get("nbits", None)

    data = np.fromfile(
        f,
        offset=meta["size"],
        dtype={
            1: np.uint8,
            2: np.uint8,
            4: np.uint8,
            8: np.uint8,
            16: np.uint16,
            32: np.float32,
            None: np.float32,
        }[nbits],
    )
    if nbits in [1, 2, 4]:
        data = numbits.unpack(data, nbits=nbits)
    return {"meta": meta, "data": data}


def writetim(tim, f):

    """
    Write out a SIGPROC time series (*.tim) file.
    """

    meta = tim["meta"]
    data = tim["data"]
    size = meta["size"]
    nbits = meta.get("nbits", None)

    writehdr(meta, f)
    with open(f, "a") as fp:
        fp.seek(size)
        (numbits.pack(data, nbits=nbits) if nbits in [1, 2, 4] else data).tofile(fp)
