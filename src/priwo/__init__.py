from typing import Dict, Callable

from .inf import read_inf, write_inf
from .dat import read_dat, write_dat
from .tim import read_tim, write_tim
from .fft import read_fft, write_fft
from .pfd import read_pfd, write_pfd
from .spc import read_spc, write_spc
from .sigproc import read_sigproc, write_sigproc
from .psrfits import read_psrfits, write_psrfits
from .polycos import read_polycos, write_polycos
from .bestprof import read_bestprof, write_bestprof


exts: Dict[str, Callable] = {
    ".inf": read_inf,
    ".dat": read_dat,
    ".tim": read_tim,
    ".fft": read_fft,
    ".spc": read_spc,
    ".pfd": read_pfd,
    ".fil": read_sigproc,
    ".bestprof": read_bestprof,
}


__all__ = [
    "read_inf",
    "write_inf",
    "read_dat",
    "write_dat",
    "read_tim",
    "write_tim",
    "read_fft",
    "write_fft",
    "read_pfd",
    "write_pfd",
    "read_spc",
    "write_spc",
    "read_sigproc",
    "write_sigproc",
    "read_psrfits",
    "write_psrfits",
    "read_polycos",
    "write_polycos",
    "read_bestprof",
    "write_bestprof",
]

from ._version import get_versions  # type: ignore

__version__ = get_versions()["version"]
del get_versions