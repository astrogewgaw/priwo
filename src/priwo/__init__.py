from .core import unpack

from .inf import read_inf, write_inf
from .dat import read_dat, write_dat
from .tim import read_tim, write_tim
from .fft import read_fft, write_fft
from .pfd import read_pfd, write_pfd
from .spc import read_spc, write_spc
from .sigproc import read_sigproc, write_sigproc
from .psrfits import read_psrfits, write_psrfits
from .bestprof import read_bestprof, write_bestprof


__all__ = ["unpack"]

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
        "read_psrfits",
        "write_psrfits",
        "read_bestprof",
        "write_bestprof",
    ]
)

from ._version import get_versions  # type: ignore

__version__ = get_versions()["version"]
del get_versions