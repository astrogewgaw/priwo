"""
R/W TEMPO timing residuals.

As described in https://tempo.sourceforge.net/ref_man_sections/output.txt,
timing residuals are usually written to a resid2.tmp file in a binary format.
Each record contains eight real*8 values:
  --TOA (MJD, referenced to solar system barycenter)
  --Postfit residual (pulse phase, from 0 to 1)
  --Postfit residual (seconds)
  --Orbital phase (where applicable)
  --Observing frequency (in barycenter frame)
  --Weight of point in the fit
  --Timing uncertainty (according to input file)
  --Prefit residual (pulse phase)
"""

import struct
from pathlib import Path
from typing import BinaryIO

import numpy as np


def readresiduals(fn: str | Path | BinaryIO) -> dict:
    """
    Read in TEMPO timing residuals.

    The residuals are read from a binary file (usually ``resid2.tmp``) made
    of Fortran unformatted records. The byte order and the size of the
    record markers (4 or 8 bytes) are detected automatically.

    Parameters
    ----------
    fn : str or pathlib.Path or BinaryIO
        Path to a residuals file, or a seekable binary file object to read
        from.

    Returns
    -------
    dict
        The residuals as key-value pairs. Each array has one value per TOA.
        The keys are:

        - ``endian``: Byte order of the file (``"little"`` or ``"big"``).
        - ``ntoas``: Number of TOAs.
        - ``barytoas``: Barycentric TOAs (MJD).
        - ``prefitphz``, ``postfitphz``: Prefit and postfit residuals (pulse
          phase).
        - ``prefittime``, ``postfittime``: Prefit and postfit residuals (s).
        - ``uncertainty``: TOA uncertainties (s).
        - ``orbitphz``: Orbital phases. Only present if not all zero.
        - ``baryfreq``: Barycentric observing frequencies (MHz). Only present
          if not all zero.
        - ``weight``: Weights of the TOAs in the fit. Only present if not all
          zero.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.
    ValueError
        If the size of the file is not a multiple of the record size, or the
        record size does not match the expected record layout.

    See Also
    --------
    writeresiduals : Write out TEMPO timing residuals.

    Notes
    -----
    The prefit residuals in seconds are not stored in the file. They are
    derived by scaling the prefit residuals in phase by the ratio of the
    postfit residuals in seconds to those in phase.

    Examples
    --------
    >>> from priwo.timing import readresiduals
    >>> res = readresiduals("resid2.tmp")
    >>> toas, resids = res["barytoas"], res["postfittime"]
    """

    def read(f: BinaryIO) -> dict:
        res = {}
        swp = "<"
        data = f.read(8)
        tint32 = struct.unpack(f"{swp}i", data[:4])[0]
        tint64 = struct.unpack(f"{swp}q", data)[0]
        if (tint32 > 100 or tint32 < 0) and (tint64 > 100 or tint64 < 0):
            swp = ">"
            tint32 = struct.unpack(f"{swp}i", data[:4])[0]
            tint64 = struct.unpack(f"{swp}q", data)[0]
        if tint32 < 100 and tint32 > 0:
            marktype = "i"
            reclen = tint32 + 2 * 4
        else:
            marktype = "q"
            reclen = tint64 + 2 * 8
        rectype = swp + marktype + 9 * "d" + marktype

        f.seek(0, 2)
        filelen = f.tell()
        if filelen % reclen or not (reclen == struct.calcsize(rectype)):
            raise ValueError("INCORRECT RECORD SIZE. ABORT.")
        f.seek(0, 0)

        res["endian"] = {">": "big", "<": "little"}[swp]

        ntoas = filelen // reclen
        res["ntoas"] = ntoas
        res["barytoas"] = np.zeros(ntoas, f"{swp}d")
        res["postfitphz"] = np.zeros(ntoas, f"{swp}d")
        res["postfittime"] = np.zeros(ntoas, f"{swp}d")
        res["orbitphz"] = np.zeros(ntoas, f"{swp}d")
        res["baryfreq"] = np.zeros(ntoas, f"{swp}d")
        res["weight"] = np.zeros(ntoas, f"{swp}d")
        res["uncertainty"] = np.zeros(ntoas, f"{swp}d")
        res["prefitphz"] = np.zeros(ntoas, f"{swp}d")

        for ii in range(ntoas):
            rec = struct.unpack(rectype, f.read(reclen))
            (
                res["barytoas"][ii],
                res["postfitphz"][ii],
                res["postfittime"][ii],
                res["orbitphz"][ii],
                res["baryfreq"][ii],
                res["weight"][ii],
                res["uncertainty"][ii],
                res["prefitphz"][ii],
            ) = (rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8])

        for key in ["orbitphz", "baryfreq", "weight"]:
            if not np.any(res[key]):
                res.pop(key)
        res["prefittime"] = res["postfittime"] / res["postfitphz"] * res["prefitphz"]
        res["uncertainty"] = res["uncertainty"] * 1.0e-6
        return res

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "rb") as f:
            return read(f)
    elif hasattr(fn, "read"):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writeresiduals(res: dict, fn: str | Path | BinaryIO) -> None:
    """
    Write out TEMPO timing residuals.

    Parameters
    ----------
    res : dict
        The residuals as key-value pairs, with the same keys as those
        returned by `readresiduals`.
    fn : str or pathlib.Path or BinaryIO
        Path to the output file, or a binary file object to write to.

    Returns
    -------
    None

    Raises
    ------
    NotImplementedError
        Always. Writing TEMPO timing residuals is not supported yet.

    See Also
    --------
    readresiduals : Read in TEMPO timing residuals.
    """
    raise NotImplementedError

    def write(res: dict, f: BinaryIO) -> None:
        pass

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "wb+") as f:
            write(res, f)
    elif hasattr(fn, "write"):
        write(res, fn)
    else:
        msg = f"EXPECTED PATH OR BINARY FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readresiduals", "writeresiduals"]
