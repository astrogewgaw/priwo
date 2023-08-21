from priwo._internals import (
    _parsehdr,
    _parsefil,
    _parsetim,
    _parsepfd,
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
    meta = {k: v for k, v in meta.items() if v is not None}
    return meta, data


def readfil(f):
    """
    Read in a SIGPROC filterbank (*.fil) file.
    """
    with open(f, "rb") as f:
        meta, data = _parsefil(f.read())
    meta = {k: v for k, v in meta.items() if v is not None}
    return meta, data


def readpfd(f):
    """
    Read in a PRESTO folded data (*.pfd) file.
    """
    with open(f, "rb") as f:
        meta, data = _parsepfd(f.read())
    meta = {k: v for k, v in meta.items() if v is not None}
    return meta, data
