"""
R/W TEMPO polynomial ephemerides (*.polycos) files.

As described in http://tempo.sourceforge.net/ref_man_sections/tz-polyco.txt,
the polynomial ephemerides file written by the TEMPO program has the following
format:

Line  Columns     Item
----  -------   -----------------------------------
  1      1-10   Pulsar Name
        11-19   Date (dd-mmm-yy)
        20-31   UTC (hhmmss.ss)
        32-51   TMID (MJD)
        52-72   DM
        74-79   Doppler shift due to earth motion (10^-4)
        80-86   Log_10 of fit rms residual in periods
  2      1-20   Reference Phase (RPHASE)
        21-38   Reference rotation frequency (F0)
        39-43   Observatory number (see note ** below)
        44-49   Data span (minutes)
        50-54   Number of coefficients
        55-75   Observing frequency (MHz)
        76-80   Binary phase
  3*     1-25   Coefficient 1 (COEFF(1))
        26-50   Coefficient 2 (COEFF(2))
        51-75   Coefficient 3 (COEFF(3))

* Subsequent lines have three coefficients each, up to NCOEFF

The pulse phase and frequency at time T are then calculated as:

       DT = (T-TMID) * 1440
    PHASE = (RPHASE
             + DT*60*F0
             + COEFF(1)
             + DT*COEFF(2)
             + DT^2*COEFF(3)
             + ....)
 FREQ(Hz) = (F0 + (1/60) * (COEFF(2)
                            + 2*DT*COEFF(3)
                            + 3*DT^2*COEFF(4)
                            + ....))

** Observatory numbers are integers based on the observatory code.
"""

from itertools import islice
from pathlib import Path

import numpy as np

from priwo.typing import TextFile


def readpolycos(fn: str | Path | TextFile) -> list[tuple[dict, np.ndarray]]:
    """
    Read in a TEMPO polynomial ephemerides (*.polycos) file.
    """

    def read(f: TextFile) -> list[tuple[dict, np.ndarray]]:
        polycos = []
        for line in f:
            meta = {}

            psr, date, utc, tmid_str, dm, *rest = line.split()
            tmidi, _, tmidf = tmid_str.partition(".")

            meta["psr"] = psr
            meta["date"] = date
            meta["utc"] = utc
            meta["tmidi"] = float(tmidi)
            meta["tmidf"] = float("0." + tmidf)
            meta["tmid"] = meta["tmidi"] + meta["tmidf"]
            meta["dm"] = float(dm)

            if len(rest) == 2:
                doppler, log10rms = rest
            else:
                doppler, _, log10rms = rest[-1].rpartition("-")
                log10rms = "-" + log10rms
            meta["doppler"] = float(doppler) * 1e-4
            meta["log10rms"] = float(log10rms)

            fields = next(f).split()
            meta["refphz"] = float(fields[0])
            meta["f0"] = float(fields[1])
            meta["obs"] = int(fields[2])
            meta["dataspan"] = int(fields[3])
            meta["ncoeff"] = int(fields[4])
            meta["obsfreq"] = float(fields[5])
            meta["binphz"] = float(fields[6]) if len(fields) == 7 else None

            coeffs = np.array(
                [
                    float(coeff.replace("D", "E"))
                    for line in islice(f, -(-meta["ncoeff"] // 3))
                    for coeff in line.split()
                ],
                dtype=np.float64,
            )
            polycos.append((meta, coeffs))
        return polycos

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return read(f)
    elif isinstance(fn, TextFile):
        return read(fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writepolycos(
    polycos: list[tuple[dict, np.ndarray]],
    fn: str | Path | TextFile,
) -> None:
    """
    Write out a TEMPO polynomial ephemerides (*.polycos) file.
    """

    def write(polycos: list[tuple[dict, np.ndarray]], f: TextFile) -> None:
        templates: dict[str, str] = {
            "psr": "{:<10s}",
            "date": "{:>10s}",
            "utc": "{:>11s}",
            "tmid": "{:>20.11f}",
            "dm": "{:>21.6f}",
            "doppler": "{:>7.3f}",
            "log10rms": "{:>7.3f}\n",
            "refphz": "{:>20.6f}",
            "f0": "{:^20.12f}",
            "obs": "{:^5d}",
            "dataspan": "{:^5.0f}",
            "ncoeff": "{:^4d}",
            "obsfreq": "{:^21.3f}",
            "binphz": "{:^4.0f}\n",
        }

        coefftemplate: str = "{:>25.16E}{:>25.16E}{:>25.16E}\n"

        for polyco in polycos:
            lines = []
            meta, coeffs = polyco
            for key, val in meta.items():
                if key not in ["tmidi", "tmidf"]:
                    val = val * 1e4 if key == "doppler" else val
                    if val is not None:
                        lines.append(templates[key].format(val))
                    else:
                        lines.append(templates[key].replace("f", "s").format(""))
            f.write("".join(lines))
            f.write((coefftemplate * (meta["ncoeff"] // 3)).format(*list(coeffs)))

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "w+") as f:
            write(polycos, f)
    elif isinstance(fn, TextFile):
        write(polycos, fn)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readpolycos", "writepolycos"]
