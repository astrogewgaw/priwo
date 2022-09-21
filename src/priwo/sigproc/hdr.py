import pabo

# fmt: off
START = pabo.Const(pabo.PascalString(pabo.Int(4), "utf8"), "HEADER_START")
END   = pabo.Const(pabo.PascalString(pabo.Int(4), "utf8"), "HEADER_END")
# fmt: on

# fmt: off
HDRKEYS = {
    "filename":      pabo.PascalString(pabo.Int(4), "utf8"),
    "telescope_id":  pabo.Int(4),
    "telescope":     pabo.PascalString(pabo.Int(4), "utf8"),
    "machine_id":    pabo.Int(4),
    "data_type":     pabo.Int(4),
    "rawdatafile":   pabo.PascalString(pabo.Int(4), "utf8"),
    "source_name":   pabo.PascalString(pabo.Int(4), "utf8"),
    "barycentric":   pabo.Int(4),
    "pulsarcentric": pabo.Int(4),
    "az_start":      pabo.Float(8),
    "za_start":      pabo.Float(8),
    "src_raj":       pabo.Float(8),
    "src_dej":       pabo.Float(8),
    "tstart":        pabo.Float(8),
    "tsamp":         pabo.Float(8),
    "nbits":         pabo.Int(4),
    "nsamples":      pabo.Int(4),
    "fch1":          pabo.Float(8),
    "foff":          pabo.Float(8),
    "fchannel":      pabo.Float(8),
    "nchans":        pabo.Int(4),
    "nifs":          pabo.Int(4),
    "refdm":         pabo.Float(8),
    "flux":          pabo.Float(8),
    "period":        pabo.Float(8),
    "nbeams":        pabo.Int(4),
    "ibeam":         pabo.Int(4),
    "hdrlen":        pabo.Int(4),
    "pb":            pabo.Float(8),
    "ecc":           pabo.Float(8),
    "asini":         pabo.Float(8),
    "orig_hdrlen":   pabo.Int(4),
    "new_hdrlen":    pabo.Int(4),
    "sampsize":      pabo.Int(4),
    "bandwidth":     pabo.Float(8),
    "fbottom":       pabo.Float(8),
    "ftop":          pabo.Float(8),
    "obs_date":      pabo.PascalString(pabo.Int(4), "utf8"),
    "obs_time":      pabo.PascalString(pabo.Int(4), "utf8"),
    "signed":        pabo.Int(1),
    "accel":         pabo.Float(8),
}
# fmt: on


def readhdr(f):

    """
    Read in a SIGPROC header.
    """

    meta = {}
    with open(f, "rb") as fp:
        START.parse_stream(fp)
        while True:
            key = pabo.PascalString(pabo.Int(4), "utf8").parse_stream(fp)
            if key == "HEADER_END":
                break
            meta[key] = HDRKEYS[key].parse_stream(fp)
    return meta


def writehdr(meta, f):

    """
    Write out a SIGPROC header.
    """

    with open(f, "wb+") as fp:
        START.build_stream("HEADER_START", fp)
        for key, val in meta.items():
            HDRKEYS[key].build_stream(val, fp)
        END.build_stream("HEADER_END", fp)
