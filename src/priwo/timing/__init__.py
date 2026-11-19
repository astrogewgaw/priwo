"""
R/W data formats used by timing packages like TEMPO/TEMPO2.
"""

from priwo.timing.parfile import readpar, writepar
from priwo.timing.polycos import readpolycos, writepolycos
from priwo.timing.residuals import readresiduals, writeresiduals
from priwo.timing.toas import readtoas, writetoas

__all__ = [
    "readpar",
    "readpolycos",
    "readresiduals",
    "readtoas",
    "writepar",
    "writepolycos",
    "writeresiduals",
    "writetoas",
]
