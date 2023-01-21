"""
"""

import pabo as pb


def readguppi(f):
    meta = {}
    with open(f, "rb") as fp:
        while True:
            line = pb.PaddedString(80)
            parsed = line.parse_stream(fp)
            parsed = parsed.strip()
            if parsed == "END":
                break
            key, val = parsed.split("=")
            val = val.replace("'", "")
            val = val.strip()
            key = key.strip()
            meta[key] = val
    return meta


def writeguppi():
    pass
