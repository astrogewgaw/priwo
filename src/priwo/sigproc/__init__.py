"""
R/W pulsar data from formats used by the SIGPROC package.
"""

from priwo.sigproc.hdr import readhdr, writehdr
from priwo.sigproc.tim import readtim, writetim
from priwo.sigproc.fil import readfil, writefil

__all__ = [
    "readhdr",
    "readtim",
    "readfil",
    "writehdr",
    "writetim",
    "writefil",
]
