"""
R/W SIGPROC headers.
"""

import math
import struct
from pathlib import Path

from priwo.typing import BinaryFile

telids: dict[str, int] = {
    "Fake": 0,
    "Arecibo": 1,
    "ARECIBO 305m": 1,
    "Ooty": 2,
    "Nancay": 3,
    "Parkes": 4,
    "Jodrell": 5,
    "GBT": 6,
    "GMRT": 7,
    "Effelsberg": 8,
    "ATA": 9,
    "SRT": 10,
    "LOFAR": 11,
    "VLA": 12,
    "CHIME": 20,
    "FAST": 21,
    "MWA": 30,
    "NC": 40,
    "NGNC": 41,
    "MeerKAT": 64,
    "KAT-7": 65,
}
id2tel: dict[int, str] = {v: k for k, v in telids.items()}

macids: dict[str, int] = {
    "FAKE": 0,
    "PSPM": 1,
    "WAPP": 2,
    "AOFTM": 3,
    "BCPM1": 4,
    "BPP": 4,
    "OOTY": 5,
    "SCAMP": 6,
    "GMRTFB": 7,
    "PULSAR2000": 8,
    "PARSPEC": 9,
    "BPSR": 10,
    "COBALT": 11,
    "GMRTNEW": 14,
    "BG/P": 11,
    "PDEV": 12,
    "CHIME+PSR": 20,
    "MWA-VCS": 30,
    "MWAX-VCS": 31,
    "MWAX-RTB": 32,
    "ADU": 40,
    "iTPM": 41,
    "KAT": 64,
    "KAT-DC2": 65,
}
id2mac: dict[int, str] = {v: k for k, v in macids.items()}

hdrmap: dict[str, str] = {
    "filename": "s",
    "telescope_id": "i",
    "telescope": "s",
    "machine_id": "i",
    "machine": "s",
    "data_type": "i",
    "rawdatafile": "s",
    "source_name": "s",
    "barycentric": "i",
    "pulsarcentric": "i",
    "az_start": "d",
    "za_start": "d",
    "src_raj": "d",
    "src_dej": "d",
    "tstart": "d",
    "tsamp": "d",
    "nbits": "i",
    "nsamples": "i",
    "fch1": "d",
    "foff": "d",
    "fchannel": "d",
    "nchans": "i",
    "nifs": "i",
    "refdm": "d",
    "flux": "d",
    "period": "d",
    "nbeams": "i",
    "ibeam": "i",
    "hdrlen": "i",
    "pb": "d",
    "ecc": "d",
    "asini": "d",
    "orig_hdrlen": "i",
    "new_hdrlen": "i",
    "sampsize": "i",
    "bandwidth": "d",
    "fbottom": "d",
    "ftop": "d",
    "obs_date": "s",
    "obs_time": "s",
    "signed": "b",
    "accel": "d",
}


ENDFLAG: str = "HEADER_END"
STARTFLAG: str = "HEADER_START"
RADTODEG: float = float("57.295779513082320876798154814105170332405472466564")
ARCSECTORAD: float = float("4.8481368110953599358991410235794797595635330237270e-6")


def readhdr(fn: str | Path | BinaryFile) -> dict:
    """
    Read in a SIGPROC header.
    """

    def read(f: BinaryFile) -> dict:
        def chkread(N: int) -> bytes:
            data = f.read(N)
            if len(data) != N:
                raise ValueError("UNEXPECTED END OF SIGPROC HDR. ABORT.")
            return data

        meta = {}
        f.seek(0)
        for swp in ["<", ">"]:
            if (size := struct.unpack(swp + "i", chkread(4))[0]) == len(STARTFLAG):
                key = chkread(size).decode("utf-8")
                if key == STARTFLAG:
                    break
            else:
                f.seek(0)
        else:
            raise ValueError("NOT A VALID SIGPROC HDR. ABORT.")
        while True:
            size = struct.unpack(f"{swp}i", chkread(4))[0]
            key = chkread(size).decode("utf-8")
            if key == ENDFLAG:
                break
            try:
                fmt = hdrmap[key]
            except KeyError:
                raise ValueError("INVALID KEY IN SIGPROC HDR. ABORT.") from None
            val = {
                "d": lambda f: struct.unpack(f"{swp}d", chkread(8))[0],
                "i": lambda f: struct.unpack(f"{swp}i", chkread(4))[0],
                "b": lambda f: struct.unpack(f"{swp}b", chkread(1))[0],
                "s": lambda f: chkread(struct.unpack(f"{swp}i", chkread(4))[0]).decode(
                    "utf-8"
                ),
            }[fmt](f)
            meta[key] = val
        meta["endian"] = {">": "big", "<": "little"}[swp]
        meta["size"] = f.tell()

        if (dec := meta.get("src_dej", None)) is not None:
            dec = float(dec)
            sign = 1.0
            if dec < 0:
                sign = -1.0
            xx = math.fabs(dec)
            dd = math.floor(xx / 10000.0)
            mm = math.floor((xx - dd * 10000.0) / 100.0)
            ss = xx - dd * 10000.0 - mm * 100.0
            meta["decdms"] = f"{sign * dd:.0f}d{mm:.0f}m{ss:.10f}s"
            meta["decrad"] = sign * ARCSECTORAD * (60.0 * (60.0 * dd + mm) + ss)
            meta["decdeg"] = meta["decrad"] * RADTODEG

        if (ra := meta.get("src_raj", None)) is not None:
            ra = float(ra)
            xx = math.fabs(ra)
            dd = math.floor(xx / 10000.0)
            mm = math.floor((xx - dd * 10000.0) / 100.0)
            ss = xx - dd * 10000.0 - mm * 100.0
            meta["rahms"] = f"{dd:.0f}h{mm:.0f}m{ss:.10f}s"
            meta["rarad"] = 15.0 * ARCSECTORAD * (60.0 * (60.0 * dd + mm) + ss)
            meta["radeg"] = meta["rarad"] * RADTODEG

        return meta

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif isinstance(fn, BinaryFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writehdr(meta: dict, fn: str | Path | BinaryFile) -> None:
    """
    Write out a SIGPROC header.
    """

    def write(meta: dict, f: BinaryFile) -> None:
        swp = {"big": ">", "little": "<"}[meta.get("endian", "little")]
        data = struct.pack(f"{swp}i", len(STARTFLAG)) + STARTFLAG.encode("utf-8")
        for key, val in meta.items():
            if key in {
                "size",
                "rahms",
                "rarad",
                "radeg",
                "decdms",
                "decrad",
                "decdeg",
                "endian",
            }:
                continue
            try:
                fmt = hdrmap[key]
            except KeyError:
                raise ValueError("INVALID KEY FOR SIGPROC HDR. ABORT.") from None
            data = data + struct.pack(f"{swp}i", len(key)) + key.encode("utf-8")
            data = data + {
                "d": lambda x: struct.pack(f"{swp}d", x),
                "i": lambda x: struct.pack(f"{swp}i", x),
                "b": lambda x: struct.pack(f"{swp}b", x),
                "s": lambda x: struct.pack(f"{swp}i", len(y := x.encode("utf-8"))) + y,
            }[fmt](val)
        data = data + struct.pack(f"{swp}i", len(ENDFLAG)) + ENDFLAG.encode("utf-8")
        f.write(data)

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(meta, f)
    elif isinstance(fn, BinaryFile):
        return write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readhdr", "writehdr"]
