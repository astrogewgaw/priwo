"""
R/W SIGPROC headers.
"""

import pabo as pb

# fmt: off
START = pb.Const("HEADER_START", pb.PascalString(pb.Int(4), "utf8"))
END   = pb.Const("HEADER_END", pb.PascalString(pb.Int(4), "utf8"))
# fmt: on

# fmt: off
HDRKEYS = {
    "filename":      pb.PascalString(pb.Int(4), "utf8"),
    "telescope_id":  pb.Int(4),
    "telescope":     pb.PascalString(pb.Int(4), "utf8"),
    "machine_id":    pb.Int(4),
    "data_type":     pb.Int(4),
    "rawdatafile":   pb.PascalString(pb.Int(4), "utf8"),
    "source_name":   pb.PascalString(pb.Int(4), "utf8"),
    "barycentric":   pb.Int(4),
    "pulsarcentric": pb.Int(4),
    "az_start":      pb.Float(8),
    "za_start":      pb.Float(8),
    "src_raj":       pb.Float(8),
    "src_dej":       pb.Float(8),
    "tstart":        pb.Float(8),
    "tsamp":         pb.Float(8),
    "nbits":         pb.Int(4),
    "nsamples":      pb.Int(4),
    "fch1":          pb.Float(8),
    "foff":          pb.Float(8),
    "fchannel":      pb.Float(8),
    "nchans":        pb.Int(4),
    "nifs":          pb.Int(4),
    "refdm":         pb.Float(8),
    "flux":          pb.Float(8),
    "period":        pb.Float(8),
    "nbeams":        pb.Int(4),
    "ibeam":         pb.Int(4),
    "hdrlen":        pb.Int(4),
    "pb":            pb.Float(8),
    "ecc":           pb.Float(8),
    "asini":         pb.Float(8),
    "orig_hdrlen":   pb.Int(4),
    "new_hdrlen":    pb.Int(4),
    "sampsize":      pb.Int(4),
    "bandwidth":     pb.Float(8),
    "fbottom":       pb.Float(8),
    "ftop":          pb.Float(8),
    "obs_date":      pb.PascalString(pb.Int(4), "utf8"),
    "obs_time":      pb.PascalString(pb.Int(4), "utf8"),
    "signed":        pb.Int(1),
    "accel":         pb.Float(8),
}
# fmt: on


def float2coord(x: float):
    dd = int(x / 1e4)
    mm = int((x - dd * 1e4) / 1e2)
    ss = x - dd * 1e4 - mm * 1e2
    return ":".join(map(str, [dd, mm, ss]))


def coord2float(x: str):
    dd, mm, ss = list(map(float, x.split(":")))
    return dd * 1e4 + mm * 1e2 + ss


def readhdr(f):
    """
    Read in a SIGPROC header.
    """

    meta = {}
    with open(f, "rb") as fp:
        START.parse(fp)
        while True:
            key = pb.PascalString(pb.Int(4), "utf8").parse(fp)
            if key == "HEADER_END":
                break
            meta[key] = HDRKEYS[key].parse(fp)
        meta["size"] = fp.tell()
    ra = meta.get("src_raj", None)
    dec = meta.get("src_dej", None)
    if ra is not None:
        meta["src_raj"] = float2coord(ra)
    if dec is not None:
        meta["src_dej"] = float2coord(dec)
    return meta


def writehdr(meta, f):
    """
    Write out a SIGPROC header.
    """

    with open(f, "wb+") as fp:
        START.build(fp)
        for key, val in meta.items():
            if key != "size":
                pb.PascalString(pb.Int(4), "utf8").build(key, fp)
                val = coord2float(val) if key in ["src_raj", "src_dej"] else val
                HDRKEYS[key].build(val, fp)
        END.build(fp)
