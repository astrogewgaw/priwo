"""
R/W *.polycos files.

The polynomial ephemerides file written by the TEMPO program has
the following format:

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

(This description was taken from http://tempo.sourceforge.net/ref_man_sections/tz-polyco.txt)
"""


import numpy as np

from pathlib import Path
from typing import List, Dict, Union


string = lambda _: str(_).strip()
integer = lambda _: int(_) if string(_) else None
numeric = lambda _: float(_) if string(_) else None


polyco_template = {
    "psrname": "{:<10s}",
    "date": "{:>10s}",
    "utc": "{:>11s}",
    "tmid": "{:>20.11f}",
    "dm": "{:>21.6f}",
    "doppler": "{:>7.3f}",
    "log10rms": "{:>7.3f}\n",
    "ref_phase": "{:>20.6f}",
    "ref_rot": "{:^20.12f}",
    "obs_code": "{:^5d}",
    "data_span": "{:^5.0f}",
    "num_coeff": "{:^4d}",
    "obs_freq": "{:^21.3f}",
    "bin_phz": "{:^4.0f}\n",
}

coeff_template = lambda num_coeff: "{:>25.16E}{:>25.16E}{:>25.16E}\n" * num_coeff


def read_polycos(f: Union[str, Path]) -> List[Dict]:

    """"""

    with open(f, "r") as fobj:

        polycos = []

        while True:

            # Read in the following parameters:
            #   1. Pulsar Name
            #   2. Date (dd-mmm-yy)
            #   3. UTC (hhmmss.ss)
            #   4. TMID (MJD)
            #   5. DM
            #   6. Doppler shift due to earth motion (10^-4)
            #   7. Log_10 of fit rms residual in periods

            line = fobj.readline()

            if line == "":
                break

            polyco = {
                "psrname": string(line[:10]),
                "date": string(line[10:20]),
                "utc": string(line[20:32]),
                "tmid": numeric(line[32:52]),
                "dm": numeric(line[52:73]),
                "doppler": numeric(line[73:79]),
                "log10rms": numeric(line[79:86]),
            }

            # Read in the following parameters:
            #   1. Reference Phase (RPHASE)
            #   2. Reference rotation frequency (F0)
            #   3. Observatory number (see note ** below)
            #   4. Data span (minutes)
            #   5. Number of coefficients
            #   6. Observing frequency (MHz)
            #   7. Binary phase

            line = fobj.readline()
            polyco.update(
                {
                    "ref_phase": numeric(line[:20]),
                    "ref_rot": numeric(line[20:39]),
                    "obs_code": integer(line[39:44]),
                    "data_span": numeric(line[44:50]),
                    "num_coeff": integer(line[50:55]),
                    "obs_freq": numeric(line[55:76]),
                    "bin_phz": numeric(line[76:80]),
                }
            )

            # Read in the coefficients.

            num_coeff = polyco["num_coeff"]

            coeffs = []
            for _ in range(num_coeff // 3):  # type: ignore
                line = fobj.readline()
                coeffs.extend(
                    [
                        numeric(_.replace("D", "E"))
                        for _ in [
                            line[:25],
                            line[25:51],
                            line[51:76],
                        ]
                    ]
                )
            polyco["coeffs"] = np.asarray(
                coeffs,
                dtype=np.float64,
            )  # type: ignore
            polycos.append(polyco)

    return polycos


def write_polycos(
    polycos: List[Dict],
    f: Union[str, Path],
) -> None:

    """"""

    with open(f, "w+") as fobj:
        for polyco in polycos:

            p = polyco.copy()
            pt = polyco_template.copy()

            coeffs = p.pop("coeffs")
            num_coeff = p["num_coeff"]
            for key, val in p.items():
                if val is None:
                    p[key] = ""
                    pt[key] = pt[key].replace("f", "s")
            fobj.write("".join(pt.values()).format(*p.values()))
            fobj.write(coeff_template(num_coeff // 3).format(*list(coeffs)))
