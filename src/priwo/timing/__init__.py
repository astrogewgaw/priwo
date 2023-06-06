"""
R/W pulsar data from formats used by timing packages, like TEMPO/TEMPO2.
"""

from priwo.timing.polycos import readpolycos, writepolycos

__all__ = [
    "readpolycos",
    "writepolycos",
]
