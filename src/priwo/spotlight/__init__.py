"""
R/W SPOTLIGHT raw data.
"""

from priwo.spotlight.hdr import readspotlighthdr, writespotlighthdr
from priwo.spotlight.raw import readspotlight, writespotlight

__all__ = [
    "readspotlight",
    "readspotlighthdr",
    "writespotlight",
    "writespotlighthdr",
]
