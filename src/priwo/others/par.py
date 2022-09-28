"""
R/W TEMPO parameter (*.par) files.
"""

import re
import shlex


pad = lambda _, N: (_ + [None] * N)[:N]
boolean = lambda _: {"1": True, "0": False}.get(_, False)


def readpar(f):

    """
    Read in a TEMPO parameters (*.par) file.
    """

    with open(f, "r") as fp:
        lines = [
            _
            for _ in [
                shlex.split(
                    line,
                    posix=True,
                    comments=True,
                )
                for line in fp.readlines()
            ]
            if _
        ]

    data = {}
    for line in lines:
        if line[0] not in [
            "JUMP",
            "ECORR",
            "DMJUMP",
            "DMEFAC",
            "T2EFAC",
            "T2EQUAD",
        ]:
            (
                key,
                value,
                fit,
                error,
            ) = pad(line, 4)

            data.update(
                {
                    key: value,
                    "_".join([key, "ERR"]): error,
                    "_".join([key, "FIT"]): boolean(fit),
                }
            )
        else:
            (
                key,
                flag,
                ref,
                value,
                fit,
                error,
            ) = pad(line, 6)

            data.update(
                {
                    "_".join([key, ref]): value,
                    "_".join([key, ref, "FLAG"]): flag,
                    "_".join([key, ref, "ERR"]): error,
                    "_".join([key, ref, "FIT"]): boolean(fit),
                }
            )
    return data


def writepar(par, f):

    """
    Write out a TEMPO parameters (*.par) file.
    """

    pass
