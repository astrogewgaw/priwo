import numpy as np

from priwo._internals import (
    _parsehdr,
    _parsefil,
)


def readhdr(f):
    with open(f, "rb") as f:
        meta = _parsehdr(f.read())
    meta = {k: v for k, v in meta.items() if v}
    return meta


def readfil(f):
    with open(f, "rb") as f:
        meta, data = _parsefil(f.read())
    meta = {k: v for k, v in meta.items() if v}
    return meta, data
