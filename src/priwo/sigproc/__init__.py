"""
R/W pulsar data from formats used by the SIGPROC package.
"""

from priwo.sigproc.fil import readfil, writefil
from priwo.sigproc.hdr import readhdr, writehdr
from priwo.sigproc.tim import readtim, writetim

__all__ = [
    "readfil",
    "readhdr",
    "readtim",
    "writefil",
    "writehdr",
    "writetim",
]
