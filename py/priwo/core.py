from priwo._internals import (
    _parsehdr,
    _parsefil,
    _parsetim,
)


def readhdr(f):
    """
    Read in a SIGPROC header.
    """
    with open(f, "rb") as f:
        meta = _parsehdr(f.read())
    meta = {k: v for k, v in meta.items() if v is not None}
    return meta


def readtim(f):
    """
    Read in a SIGPROC time series (*.tim) file.
    """
    with open(f, "rb") as f:
        meta, data = _parsetim(f.read())
    data = data[0]
    meta = {k: v for k, v in meta.items() if v is not None}
    return meta, data


def readfil(f):
    """
    Read in a SIGPROC filterbank (*.fil) file.
    """
    with open(f, "rb") as f:
        meta, data = _parsefil(f.read())
    data = data[0]
    meta = {k: v for k, v in meta.items() if v is not None}
    return meta, data
