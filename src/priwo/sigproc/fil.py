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
        ).parse_stream(fp)

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

    meta = fil["meta"]
    data = fil["data"]
    size = meta["size"]
    nbits = meta.get("nbits", 8)

    writehdr(meta, f)
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
        ).build_stream(data.T, fp)
