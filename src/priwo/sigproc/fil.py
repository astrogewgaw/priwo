"""
R/W SIGPROC filterbank (*.fil) files.
"""

import pabo as pb

from priwo.sigproc.hdr import readhdr
from priwo.sigproc.hdr import writehdr


def readfil(f):
    """
    Read in a SIGPROC filterbank (*.fil) file.
    """

    meta = readhdr(f)
    size = meta["size"]
    nbits = meta.get("nbits", None)
    with open(f, "rb") as fp:
        fp.seek(size)
        data = pb.Array(
            {
                1: pb.Int(1),
                2: pb.Int(1),
                4: pb.Int(1),
                8: pb.Int(1),
                16: pb.Int(2),
                32: pb.Float(4),
                64: pb.Float(8),
                None: pb.Float(4),
            }[nbits],
            packing=(nbits if nbits in [1, 2, 4] else None),
        ).parse(fp)
    data = data.reshape(-1, meta["nchans"])
    data = data.T
    return meta, data


def writefil(meta, data, f):
    """
    Write out a SIGPROC filterbank (*.fil) file.
    """

    writehdr(meta, f)
    size = meta["size"]
    nbits = meta.get("nbits", None)
    with open(f, "ab") as fp:
        fp.seek(size)
        pb.Array(
            {
                1: pb.Int(1),
                2: pb.Int(1),
                4: pb.Int(1),
                8: pb.Int(1),
                16: pb.Int(2),
                32: pb.Float(4),
                64: pb.Float(8),
                None: pb.Float(4),
            }[nbits],
            packing=(nbits if nbits in [1, 2, 4] else None),
        ).build(data.T, fp)
