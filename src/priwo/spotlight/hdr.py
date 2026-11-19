from pathlib import Path

import numpy as np


def readspotlighthdr(fn: str | Path) -> dict:
    def str2nullint(s: str) -> int | None:
        return None if s == "NA" else int(s)

    def str2nulldbl(s: str) -> float | None:
        return None if s == "NA" else float(s)

    def str2list(s: str) -> list[str]:
        return list(s.split())

    def str2mask(s: str) -> list[bool]:
        return [int(x) == 1 for x in np.binary_repr(int(s, 0))]

    meta = {}
    extras = []
    with open(fn, "r") as lines:
        for line in lines:
            if line.startswith(("#", " ")):
                extras.append(line)
                continue
            key, val = line.split("=")
            key = key.strip()
            val = val.strip()
            try:
                name, conv = {
                    "Header file": ("fname", str),
                    "Beam ID": ("beamid", int),
                    "Host ID": ("hostid", int),
                    "Host name": ("hostname", str),
                    "GTAC code": ("gtaccode", str),
                    "Observer": ("observer", str),
                    "GTAC title": ("gtactitle", str),
                    "Source": ("source", str),
                    "Source RA (Rad)": ("ra", float),
                    "Source DEC (Rad)": ("dec", float),
                    "Channels": ("nf", int),
                    "Bandwidth (MHz)": ("bw", float),
                    "Channel width (Hz)": ("df", float),
                    "Frequency Ch. 0  (Hz)": ("f0", float),
                    "Sampling time  (uSec)": ("dt", float),
                    "Antennas pol1": ("antX", str2list),
                    "Antennas pol2": ("antY", str2list),
                    "Antenna mask pol1": ("maskX", str2mask),
                    "Antenna mask pol2": ("maskY", str2mask),
                    "Beam mode": ("beammode", str),
                    "No. of stokes": ("npol", int),
                    "Num bits/sample": ("nbits", int),
                    "De-Disperion DM": ("dm", str2nulldbl),
                    "Total No. of Beams": ("nbeams", str2nullint),
                    "No. of PC Baselines": ("nbaselines", str2nullint),
                    "Total No. of Beams/host": ("nbeamsperhost", str2nullint),
                    "Date": ("istdate", str),
                    "IST Time": ("isttime", str),
                }[key]
                meta[name] = conv(val)
            except KeyError:
                pass
    if len(meta) == 0:
        raise ValueError("FAILED TO READ HEADER. ABORT.")
    for name in ["f0", "df", "nf", "dt", "nbits"]:
        if name not in meta:
            raise ValueError(f"{name} NOT IN METADATA. ABORT.")
    if meta.get("istdate", None) is None:
        raise ValueError("DATE FIELD MISSING. FILE CORRUPTED. ABORT.")
    if meta.get("isttime", None) is None:
        raise ValueError("IST TIME FIELD MISSING. FILE CORRUPTED. ABORT.")
    if meta.get("nbeams", None) is None:
        raise ValueError("NBEAMS FIELD MISSING. FILE CORRUPTED. ABORT.")

    if meta["df"] < 0:
        meta["fh"] = meta["f0"]
        meta["df"] = abs(meta["df"])
        meta["bw"] = meta["nf"] * meta["df"]
        meta["fl"] = meta["fh"] - meta["bw"] + (0.5 * meta["df"])
    else:
        meta["fl"] = meta["f0"]
        meta["bw"] = meta["nf"] * meta["df"]
        meta["fh"] = meta["fl"] + meta["bw"] - (0.5 * meta["df"])

    coords = {}
    for extra in extras[2:]:
        ra, dec, bmidx, bmsubidx = [float(_) for _ in extra.split()]
        coords = {"ra": ra, "dec": dec, "bmidx": bmidx, "bmsubidx": bmsubidx}
    meta["coords"] = coords

    meta["istdatetime"] = " ".join([meta["istdate"], meta["isttime"][:-3]])

    return meta


def writespotlighthdr(meta: dict, fn: str | Path) -> None:
    raise NotImplementedError
