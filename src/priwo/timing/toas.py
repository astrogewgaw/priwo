"""
R/W time-of-arrivals (TOAs) from multiple formats.

As described in https://tempo.sourceforge.net/ref_man_sections/toa.txt,
TOAs are entered, one per line, in one of four formats: 'Princeton',
'Parkes', 'Interchange TOA (ITOA)', or 'TEMPO2' format. TOAs in Princeton,
Parkes and TEMPO2 formats are assumed to be referenced in an observatory
time scale (see TIME SCALES, below). TOAs in ITOA format are assumed to be
referenced to UTC.  TOAs are reported as MJD, except that TOAs reported
using the Princeton format may also be MJD-39126 (also called '1966 day
number'). Use of the latter is discouraged.

One-character observatory codes correspond to lines in the observatory
coordinate file for '1' through '9' and 'a' through 'z'. Code '0' indicates
the geocenter. Code '@' indicates the solar system barycenter (for which
neither geometric nor clock corrections are applied). The two-character
observatory codes used in the ITOA format are given in the observatory
coordinate file. In TEMPO2 format either the one-character or two-character
codes can be used.

Princeton Format

  columns     item
    1-1     Observatory (one-character code)
    2-2     must be blank
    16-24   Observing frequency (MHz)
    25-44   TOA (decimal point must be in column 30 or column 31)
    45-53   TOA uncertainty (microseconds)
    69-78   DM correction (pc cm^-3)

Parkes Format

  columns     item
    1-1     must be blank
    26-34   Observing frequency (MHz)
    35-55   TOA (decimal point must be in column 42)
    56-63   Phase offset (fraction of P0, added to TOA)
    64-71   TOA uncertainty (microseconds)
    80-80   Observatory (one-character code)

ITOA Format

  columns     item
    1-2     ignored, but must not be blank (often PSRNAME goes here)
   10-28    TOA (decimal point must be in column 15)
   29-34    TOA uncertainty (microseconds)
   35-45    Observing frequency (MHz)
   46-55    DM correction (pc cm^-3)
   58-59    Observatory (two-letter code)

TEMPO2 Format

  This format uses whitespace-separated fields rather than fixed column
  locations for the contents.  To use this format, the first line of
  each TOA file must contain the command 'FORMAT 1'.

  field       item
    1       Name of profile data file
    2       Observing frequency (MHz)
    3       TOA
    4       TOA uncertainty (microseconds)
    5       Observatory (one- or two-character code)
    6+      Optional flags
"""

from pathlib import Path
from typing import Literal, TextIO


def readtoas(
    fn: str | Path | TextIO,
    fmt: Literal["tempo2", "princeton"],
) -> list[dict]:
    """
    Read in TOAs.

    Parameters
    ----------
    fn : str or pathlib.Path or TextIO
        Path to a TOA (``*.tim``) file, or a text file object to read from.
    fmt : {"tempo2", "princeton"}
        Format of the TOAs. See the module docstring for a description of
        each format.

    Returns
    -------
    list of dict
        One dictionary per TOA, in the order they appear. The keys are:

        - ``toamjdi``: Integer part of the TOA (MJD), as an int.
        - ``toamjdf``: Fractional part of the TOA (days), as a float. The two
          parts are kept separate to preserve precision.
        - ``toaerr``: TOA uncertainty (microseconds).
        - ``freq``: Observing frequency (MHz).
        - ``dm``: DM correction (pc cm^-3), or ``0.0`` if not given.
        - ``obs``: Observatory code.
        - ``name``: Name of the profile data file (for TEMPO2 TOAs), or the
          contents of columns 3 to 15 (for Princeton TOAs).
        - ``flags``: Dictionary of flags (for TEMPO2 TOAs), with the leading
          ``-`` removed from each flag name. The ``-dm`` flag is moved to
          ``dm``. Always empty for Princeton TOAs.

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a readable file object.
    ValueError
        If `fmt` is not a recognised format, or if a TEMPO2 TOA has fewer
        than five fields.

    See Also
    --------
    writetoas : Write out TOAs.

    Notes
    -----
    Every line in the file is parsed as a TOA, so the file should not
    contain any commands (such as ``FORMAT 1``), comments, or blank lines.

    Examples
    --------
    >>> from priwo.timing import readtoas
    >>> toas = readtoas("test.tim", fmt="tempo2")
    >>> mjds = [toa["toamjdi"] + toa["toamjdf"] for toa in toas]
    """

    def read(f: TextIO, fmt: Literal["tempo2", "princeton"]) -> list[dict]:
        toas = []
        for line in f:
            match fmt:
                case "tempo2":
                    tokens = line.split()
                    if len(tokens) < 5:
                        raise ValueError(f"NOT A VALID TEMPO2 TOA: {line!r}. ABORT.")
                    name = tokens[0]
                    freq = float(tokens[1])
                    toamjdi, toamjdf = tokens[2].strip().split(".")
                    toamjdi, toamjdf = int(toamjdi), float("0." + toamjdf)
                    toaerr = float(tokens[3])
                    obs = tokens[4]

                    i = 0
                    rest = tokens[5:]
                    flags: dict[str, str] = {}
                    while i < len(rest):
                        if rest[i].startswith("-") and i + 1 < len(rest):
                            flags[rest[i][1:]] = rest[i + 1]
                            i += 2
                        else:
                            i += 1
                    dm = float(flags.pop("dm")) if "dm" in flags else 0.0
                case "princeton":
                    line = line.rstrip("\n")
                    obs = line[0]
                    name = line[2:15]
                    freq = float(line[16:24])
                    toamjdi, toamjdf = line[25:44].strip().split(".")
                    toamjdi, toamjdf = int(toamjdi), float("0." + toamjdf)
                    toaerr = float(line[45:53])
                    dm = line[53:].strip()
                    dm = float(dm) if dm else 0.0
                    flags = {}
                case _:
                    raise ValueError("UNRECOGNISED TOA FORMAT. ABORT.")
            toas.append(
                {
                    "toamjdi": toamjdi,
                    "toamjdf": toamjdf,
                    "toaerr": toaerr,
                    "freq": freq,
                    "dm": dm,
                    "obs": obs,
                    "name": name,
                    "flags": flags,
                }
            )
        return toas

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "r") as f:
            return read(f, fmt=fmt)
    elif hasattr(fn, "read"):
        return read(fn, fmt=fmt)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


def writetoas(
    toas: list[dict],
    fn: str | Path | TextIO,
    fmt: Literal["tempo2", "princeton"],
) -> None:
    """
    Write out TOAs.

    Parameters
    ----------
    toas : list of dict
        One dictionary per TOA, with the same keys as those returned by
        `readtoas`: ``toamjdi``, ``toamjdf``, ``toaerr``, ``freq``, ``dm``,
        ``obs``, ``name``, and ``flags``. A ``dm`` of ``0.0`` is not written.
    fn : str or pathlib.Path or TextIO
        Path to the output file, or a text file object to write to. If a
        path is given, the file is created, or overwritten if it exists.
    fmt : {"tempo2", "princeton"}
        Format of the TOAs. See the module docstring for a description of
        each format.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If `fn` is neither a path nor a writable file object.
    ValueError
        If `fmt` is not a recognised format.
    KeyError
        If any TOA is missing a required key.

    See Also
    --------
    readtoas : Read in TOAs.

    Notes
    -----
    TOAs are written with 13 decimal places in the fractional day. No
    ``FORMAT 1`` line is written for TEMPO2 TOAs.

    Examples
    --------
    >>> from priwo.timing import readtoas, writetoas
    >>> toas = readtoas("test.tim", fmt="tempo2")
    >>> writetoas(toas, "copy.tim", fmt="tempo2")
    """

    def write(toas: list[dict], f: TextIO, fmt: Literal["tempo2", "princeton"]) -> None:
        for toa in toas:
            dm = toa["dm"]
            obs = toa["obs"]
            name = toa["name"]
            freq = toa["freq"]
            flags = toa["flags"]
            toaerr = toa["toaerr"]
            toamjdi = toa["toamjdi"]
            toamjdf = toa["toamjdf"]
            match fmt:
                case "tempo2":
                    f.write(
                        f"{name} {freq:f} {f'{int(toamjdi):5d}' + f'{toamjdf:.13f}'[1:]} {toaerr:.2f} {obs}"
                        + (f"{flags} -dm {dm:.4f}".strip() if dm != 0.0 else "")
                        + "\n"
                    )
                case "princeton":
                    f.write(
                        f"{obs} {name:>13s} {freq:8.3f} {f'{int(toamjdi):5d}' + f'{toamjdf:.13f}'[1:]} {toaerr:8.2f}"
                        + (f"{'':14}{dm:9.4f}" if dm != 0.0 else "")
                        + "\n"
                    )
                case _:
                    raise ValueError("UNRECOGNISED TOA FORMAT. ABORT.")

    if isinstance(fn, (str, Path)):
        fn = Path(fn)
        with open(fn, "w+") as f:
            write(toas, f, fmt=fmt)
    elif hasattr(fn, "write"):
        write(toas, fn, fmt=fmt)
    else:
        msg = f"EXPECTED PATH OR TEXT FILE OBJECT, GOT {type(fn).__name__}. ABORT."
        raise TypeError(msg)


__all__ = ["readtoas", "writetoas"]
