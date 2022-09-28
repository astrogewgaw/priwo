"""
R/W SIGPROC filterbank (*.fil) files.
"""

import numbits
import numpy as np

from priwo.sigproc.hdr import readhdr
from priwo.sigproc.hdr import writehdr


def readfil(f):

    """
    Read in a SIGPROC filterbank (*.fil) file.
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

    try:
        nchan = meta.get("nchans", -1)
        nsamp = meta.get("nsamples", -1)
        data = data.reshape(nsamp, nchan)
        data = data.T
    except:
        pass
    return {"meta": meta, "data": data}


def writefil(fil, f):

    """
    Write out a SIGPROC filterbank (*.fil) file.
    """

    pass
