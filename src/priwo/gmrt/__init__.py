"""
R/W GMRT raw data.
"""

from priwo.gmrt.ahdr import readgmrtahdr, writegmrtahdr
from priwo.gmrt.hdr import readgmrthdr, writegmrthdr
from priwo.gmrt.raw import readgmrt, readgmrt2, writegmrt, writegmrt2

__all__ = [
    "readgmrt",
    "readgmrt2",
    "readgmrtahdr",
    "readgmrthdr",
    "writegmrt",
    "writegmrt2",
    "writegmrtahdr",
    "writegmrthdr",
]
