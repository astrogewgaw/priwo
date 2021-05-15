# type: ignore

from ._version import version

from .core import (
    chunks,
    max_size,
    available_formats,
)

from .inf import read_inf, write_inf
from .dat import read_dat, write_dat
from .tim import read_tim, write_tim
from .fft import read_fft, write_fft
from .pfd import read_pfd, write_pfd
from .spc import read_spc, write_spc
from .sigproc import read_sigproc, write_sigproc
from .polycos import read_polycos, write_polycos
from .bestprof import read_bestprof, write_bestprof


PRIWO_EXTS = {
    ".inf": read_inf,
    ".dat": read_dat,
    ".tim": read_tim,
    ".fft": read_fft,
    ".spc": read_spc,
    ".pfd": read_pfd,
    ".fil": read_sigproc,
    ".polycos": read_polycos,
    ".bestprof": read_bestprof,
}


__all__ = [
    "chunks",
    "version",
    "max_size",
    "available_formats",
]

__all__.extend(
    [
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
        "read_polycos",
        "write_polycos",
        "read_bestprof",
        "write_bestprof",
    ]
)