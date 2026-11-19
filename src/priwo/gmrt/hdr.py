import re
from pathlib import Path
from typing import TextIO


def readgmrthdr(fn: str | Path | TextIO) -> dict:
    def read(f: TextIO) -> dict:
        def str2pol(s: str) -> int:
            return 1 if s == "Total I" else 4

        def str2list(s: str) -> list[float]:
            return [float(_.strip()) for _ in s.split(",")]

        meta = {}
        for line in f:
            if line.startswith("#"):
                continue
            key, val = re.split(r"\s+:\s+", line)
            key = key.strip()
            val = val.strip()
            try:
                name, conv = {
                    "Site": ("site", str),
                    "Observer": ("observer", str),
                    "Proposal": ("proposal", str),
                    "Array Mode": ("beammode", str),
                    "Observing Mode": ("obsmode", str),
                    "Date": ("istdate", str),
                    "Num Antennas": ("nant", int),
                    "Antenna List": ("antlist", str),
                    "Num Channels": ("nf", int),
                    "Channel width": ("df", float),
                    "Frequency Ch.1": ("f0", float),
                    "Num bits/sample": ("nbits", int),
                    "MJD": ("mjdi", float),
                    "UTC": ("isttime", str),
                    "Source": ("source", str),
                    "Coordinates": ("coords", str),
                    "Obs. Length": ("obslen", int),
                    "Bad Channels": ("badchans", str),
                    "Bit shift value": ("bitshift", int),
                    "Sampling Time": ("dt", float),
                    "Polarizations": ("npol", str2pol),
                    "Drift Rate": ("driftrates", str2list),
                }[key]
                meta[name] = conv(val)
            except KeyError:
                pass
        if len(meta) == 0:
            raise ValueError("FAILED TO READ HEADER. ABORT.")
        for name in ["f0", "df", "nf", "dt", "nbits"]:
            if name not in meta:
                raise ValueError(f"{name} NOT IN METADATA. ABORT.")

        ra, dec = meta["coords"].split(",")
        rah, ram, ras = ra.strip().split(":")
        decd, decm, decs = dec.strip().split(":")
        ra = meta["ra"] = f"{rah}h{ram}m{ras}s"
        dec = meta["dec"] = f"{decd}d{decm}m{decs}s"
        meta["coords"] = f"{ra} {dec}"

        meta["dt"] = meta["dt"] * 1e6
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


def writegmrthdr(meta: dict, fn: str | Path) -> None:
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
