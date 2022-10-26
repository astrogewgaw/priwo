"""
R/W TEMPO polynomial ephemerides (*.polycos) files.
"""

import re
import numpy as np

one = lambda _: _[0]
pad = lambda _, N: (_ + [None] * N)[:N]
fx = lambda _, __: __(_) if _ is not None else _

# fmt: off
TEMPLATES = {
    "name":    "{:<10s}",
    "date":    "{:>10s}",
    "utc":     "{:>11s}",
    "tmid":    "{:>20.11f}",
    "dm":      "{:>21.6f}",
    "doppler": "{:>7.3f}",
    "rms":     "{:>7.3f}\n",
    "refphz":  "{:>20.6f}",
    "reff0":   "{:^20.12f}",
    "obsno":   "{:^5d}",
    "span":    "{:^5.0f}",
    "ncoeff":  "{:^4d}",
    "freq":    "{:^21.3f}",
    "binphz":  "{:^4.0f}\n",
}
# fmt: on


def readpolycos(f):

    """
    Read in a TEMPO polynomial ephemerides (*.polycos) file.
    """

    polycos = []
    with open(f, "r") as fp:
        while True:
            line = fp.readline()
            if line == "":
                break

            (
                utc,
                tmid,
                dm,
                doppler,
                rms,
            ) = pad(re.findall(r"[+-]?[0-9]+[.][0-9]+", line), 5)
            name = one(re.findall(r"[A-Z]?[0-9]{4}[+-][0-9]{2,4}", line))
            date = one(re.findall(r"[0-9]{2}[-][A-Za-z]{3}[-][0-9]{2}", line))

            line = fp.readline()
            (
                refphz,
                reff0,
                obsno,
                span,
                ncoeff,
                freq,
                binphz,
            ) = pad(re.findall(r"[0-9]+[.]*[0-9]*", line), 7)

            polycos.append(
                {
                    "meta": {
                        # fmt: off
                        "name":    str(name),
                        "date":    str(date),
                        "utc":     str(utc),
                        "tmid":    fx(tmid,    float),
                        "dm":      fx(dm,      float),
                        "doppler": fx(doppler, float),
                        "rms":     fx(rms,     float),
                        "refphz":  fx(refphz,  float),
                        "reff0":   fx(reff0,   float),
                        "obsno":   fx(obsno,   int),
                        "span":    fx(span,    float),
                        "ncoeff":  fx(ncoeff,  int),
                        "freq":    fx(freq,    float),
                        "binphz":  fx(binphz,  float),
                        # fmt: on
                    },
                    "data": np.asarray(
                        [
                            [
                                float(re.sub(r"[dD]", "e", _)) if _ else None
                                for _ in re.findall(
                                    r"[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eEdD][+\-]?\d+)?",
                                    fp.readline(),
                                )
                            ]
                            for _ in range(int(ncoeff) // 3)
                        ]
                    ).flatten(),
                }
            )
        return polycos


def writepolycos(polycos, f):

    """
    Write out a TEMPO polynomial ephemerides (*.polycos) file.
    """

    with open(f, "w+") as fp:
        for polyco in polycos:
            fp.write(
                "".join(
                    list(
                        [
                            TEMPLATES[_].format(__)
                            if __ is not None
                            else TEMPLATES[_].replace("f", "s").format("")
                            for _, __ in polyco["meta"].items()
                        ]
                    )
                )
            )
            fp.write(
                (
                    "{:>25.16E}{:>25.16E}{:>25.16E}\n" * (polyco["meta"]["ncoeff"] // 3)
                ).format(*list(polyco["data"]))
            )
