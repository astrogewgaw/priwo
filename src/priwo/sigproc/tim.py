"""
R/W SIGPROC time series (*.tim) files.
"""

import pabo as pb
from priwo.sigproc.hdr import readhdr
from priwo.sigproc.hdr import writehdr


def readtim(f):
    """
    Read in a SIGPROC time series (*.tim) file.
    """

    meta = readhdr(f)
    size = meta["size"]
    nbits = meta.get("nbits", 8)
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
    return meta, data


def writetim(meta, data, f):
    """
    Write out a SIGPROC time series (*.tim) file.
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
        ).build(data, fp)
