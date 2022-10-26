"""
R/W pulsar data formats used by the SIGPROC package.
"""

from priwo.sigproc.hdr import readhdr
from priwo.sigproc.tim import readtim
from priwo.sigproc.fil import readfil
from priwo.sigproc.hdr import writehdr
from priwo.sigproc.tim import writetim
from priwo.sigproc.fil import writefil

__all__ = [
    "readhdr",
    "readtim",
    "readfil",
    "writehdr",
    "writetim",
    "writefil",
]
