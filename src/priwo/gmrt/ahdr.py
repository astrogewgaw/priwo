from pathlib import Path
from typing import TextIO

import numpy as np


def readgmrtahdr(fn: str | Path | TextIO) -> dict:
    def read(f: TextIO) -> dict:
        def str2bool(s: str) -> bool:
            return {"ON": True, "OFF": False}.get(s, False)

        def str2nulldbl(s: str) -> float | None:
            return None if s == "NA" else float(s)

        def str2list(s: str) -> list[str]:
            return list(s.split())

        def str2mask(s: str) -> list[bool]:
            return [int(x) == 1 for x in np.binary_repr(int(s, 0))]

        meta = {}
        extras = []
        for line in f:
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
                    "Frequency Ch.1  (Hz)": ("fh", float),
                    "Channel width (Hz)": ("df", float),
                    "Sampling time  (uSec)": ("dt", float),
                    "Antenna mask pol1": ("maskX", str2mask),
                    "Antennas pol1": ("antX", str2list),
                    "Antenna mask pol2": ("maskY", str2mask),
                    "Antennas pol2": ("antY", str2list),
                    "Beam mode": ("beammode", str),
                    "No. of stokes": ("npol", int),
                    "Num bits/sample": ("nbits", int),
                    "De-Disperion DM": ("dm", str2nulldbl),
                    "PFB": ("pfb", str2bool),
                    "PFB number of taps": ("pfbtaps", str2nulldbl),
                    "WALSH": ("walsh", str2bool),
                    "Broad-band RFI Filter": ("rfifilter", str2bool),
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

        meta["f0"] *= 1e-6
        meta["df"] *= 1e-6
        meta["dt"] *= 1e-6
        if meta["df"] < 0:
            meta["fh"] = meta["f0"]
            meta["df"] = abs(meta["df"])
            meta["bw"] = meta["nf"] * meta["df"]
            meta["fl"] = meta["fh"] - meta["bw"] + (0.5 * meta["df"])
        else:
            meta["fl"] = meta["f0"]
            meta["bw"] = meta["nf"] * meta["df"]
            meta["fh"] = meta["fl"] + meta["bw"] - (0.5 * meta["df"])

        meta["istdatetime"] = " ".join([meta["istdate"], meta["isttime"][:-3]])

        return meta

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return read(f)
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writegmrtahdr(meta: dict, fn: str | Path | TextIO) -> None:
    raise NotImplementedError

    def write(meta: dict, f: TextIO) -> None:
        pass

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "w+") as f:
            write(meta, f)
    elif hasattr(fn, "write"):
        write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)
