"""
R/W SIGPROC time series (*.tim) files.
"""

import numbits
import numpy as np
from priwo.sigproc.hdr import readhdr


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
            # fmt: off
            1:    np.uint8,
            2:    np.uint8,
            4:    np.uint8,
            8:    np.uint8,
            16:   np.uint16,
            32:   np.float32,
            None: np.float32,
            # fmt: on
        }[nbits],
    )
    if nbits in [1, 2, 4]:
        data = numbits.unpack(data, nbits=nbits)
    return {"meta": meta, "data": data}


def writetim(tim, f):

    """
    Write out a SIGPROC time series (*.tim) file.
    """

    pass
