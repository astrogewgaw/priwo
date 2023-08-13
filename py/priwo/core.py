from priwo._internals import (
    _parsehdr,
    _parsefil,
    _parsetim,
)


def readhdr(f):
    with open(f, "rb") as f:
        meta = _parsehdr(f.read())
    meta = {k: v for k, v in meta.items() if v}
    return meta


def readtim(f):
    with open(f, "rb") as f:
        meta, data = _parsetim(f.read())
    meta = {k: v for k, v in meta.items() if v}
    return meta, data


def readfil(f):
    with open(f, "rb") as f:
        meta, data = _parsefil(f.read())
    meta = {k: v for k, v in meta.items() if v}
    return meta, data
