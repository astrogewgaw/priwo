"""
I/O for common pulsar data formats.
"""

from beartype.claw import beartype_this_package

beartype_this_package()

from priwo.presto import (
    readbpf,
    readdat,
    readfft,
    readinf,
    readpfd,
    writebpf,
    writedat,
    writefft,
    writeinf,
    writepfd,
)
from priwo.sigproc import readfil, readhdr, readtim, writefil, writehdr, writetim

__all__ = [
    "readbpf",
    "readdat",
    "readfft",
    "readfil",
    "readhdr",
    "readinf",
    "readpfd",
    "readtim",
    "writebpf",
    "writedat",
    "writefft",
    "writefil",
    "writehdr",
    "writeinf",
    "writepfd",
    "writetim",
]
