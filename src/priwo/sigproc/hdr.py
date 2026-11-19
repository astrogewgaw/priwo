"""
R/W SIGPROC headers.
"""

import math
import struct
from pathlib import Path
from typing import BinaryIO

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

RADTODEG: float = float("57.295779513082320876798154814105170332405472466564")
ARCSECTORAD: float = float("4.8481368110953599358991410235794797595635330237270e-6")


def readhdr(fn: str | Path | BinaryIO) -> dict:
    """
    Read in a SIGPROC header.

    The byte order of the header is detected automatically: the header is
    first parsed as little-endian, and if the ``HEADER_START`` keyword is not
    found, it is parsed again as big-endian.

    Parameters
    ----------
    fn : str or pathlib.Path or BinaryIO
        Path to a SIGPROC file (such as a filterbank or time series file), or
        a binary file object positioned at the start of the header.

    Returns
    -------
    dict
        The header parameters as key-value pairs. Along with the parameters
        stored in the header, the following derived keys are also added:

        - ``endian``: Byte order of the header (``"little"`` or ``"big"``).
        - ``size``: Size of the header in bytes.
        - ``telescope``: Name of the telescope, if ``telescope_id`` is present.
        - ``machine``: Name of the backend, if ``machine_id`` is present.
        - ``rahms``, ``rarad``, ``radeg``: Right ascension as a ``"HHhMMmSS.Ss"``
          string, in radians, and in degrees, if ``src_raj`` is present.
        - ``decdms``, ``decrad``, ``decdeg``: Declination as a ``"DDdMMmSS.Ss"``
          string, in radians, and in degrees, if ``src_dej`` is present.

    Raises
    ------
    ValueError
        If the file does not begin with a valid ``HEADER_START`` keyword in
        either byte order.
    KeyError
        If the header contains a keyword that is not in ``hdrmap``.

    See Also
    --------
    writehdr : Write out a SIGPROC header.

    Examples
    --------
    >>> from priwo.sigproc.hdr import readhdr
    >>> meta = readhdr("test.fil")
    >>> nchans, tsamp = meta["nchans"], meta["tsamp"]
    """

    def read(f: BinaryIO) -> dict:
        meta = {}
        swp = "<"
        key = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")
        if key != "HEADER_START":
            swp = ">"
            key = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")
            if key != "HEADER_START":
                raise ValueError("NOT A VALID SIGPROC HDR. ABORT.")
        while True:
            key = f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode("utf-8")
            if key == "HEADER_END":
                break
            val = {
                "flag": None,
                "d": lambda f: struct.unpack(f"{swp}d", f.read(8))[0],
                "i": lambda f: struct.unpack(f"{swp}i", f.read(4))[0],
                "b": lambda f: struct.unpack(f"{swp}b", f.read(1))[0],
                "s": lambda f: f.read(struct.unpack(f"{swp}i", f.read(4))[0]).decode(
                    "utf-8"
                ),
            }[hdrmap[key]](f)
            meta[key] = val
        meta["endian"] = {">": "big", "<": "little"}[swp]
        meta["size"] = f.tell()

        if (macid := meta.get("machine_id", None)) is not None:
            meta["machine"] = meta.get("machine", id2mac[macid])
        if (telid := meta.get("telescope_id", None)) is not None:
            meta["telescope"] = meta.get("telescope", id2tel[telid])

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
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writehdr(meta: dict, fn: str | Path | BinaryIO) -> None:
    """
    Write out a SIGPROC header.

    Parameters
    ----------
    meta : dict
        The header parameters as key-value pairs. Every key must be a valid
        SIGPROC keyword listed in ``hdrmap``, except for the derived keys added
        by `readhdr` (``size``, ``endian``, ``rahms``, ``rarad``, ``radeg``,
        ``decdms``, ``decrad`` and ``decdeg``), which are skipped. The value of
        ``endian`` (``"little"`` or ``"big"``, defaulting to ``"little"``)
        sets the byte order of the written header.
    fn : str or pathlib.Path or BinaryIO
        Path to the output file, or a binary file object to write to. If a
        path is given, the file is created, or overwritten if it exists.

    Returns
    -------
    None

    Raises
    ------
    KeyError
        If `meta` contains a key that is neither a valid SIGPROC keyword nor
        one of the skipped derived keys, or if ``endian`` is not ``"little"``
        or ``"big"``.
    struct.error
        If a value cannot be packed into the type its keyword requires.

    See Also
    --------
    readhdr : Read in a SIGPROC header.

    Notes
    -----
    Only the header is written; the data that follows it is not. Keys are
    written in the order they appear in `meta`.

    Examples
    --------
    >>> from priwo.sigproc.hdr import readhdr, writehdr
    >>> meta = readhdr("test.fil")
    >>> writehdr(meta, "copy.hdr")
    """

    def write(meta: dict, f: BinaryIO) -> None:
        key = "HEADER_START"
        swp = {"big": ">", "little": "<"}[meta.get("endian", "little")]
        f.write(struct.pack(f"{swp}i", len(key)) + key.encode("utf-8"))
        for key, val in meta.items():
            if key in [
                "size",
                "rahms",
                "rarad",
                "radeg",
                "decdms",
                "decrad",
                "decdeg",
                "endian",
            ]:
                continue
            f.write(struct.pack(f"{swp}i", len(key)) + key.encode("utf-8"))
            f.write(
                {
                    "flag": None,
                    "d": lambda x: struct.pack(f"{swp}d", x),
                    "i": lambda x: struct.pack(f"{swp}i", x),
                    "b": lambda x: struct.pack(f"{swp}b", x),
                    "s": lambda x: struct.pack(f"{swp}i", len(x)) + x.encode("utf-8"),
                }[hdrmap[key]](val)
            )
        key = "HEADER_END"
        f.write(struct.pack(f"{swp}i", len(key)) + key.encode("utf-8"))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            return write(meta, f)
    elif hasattr(fn, "write"):
        return write(meta, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readhdr", "writehdr"]
