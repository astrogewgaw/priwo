"""
Core functionalities.
"""

import numpy as np

from construct import (
    bytes2bits,
    BitsInteger,
    GreedyRange,
)


packed = [1, 2, 4]


def greedybits(nbits: int):

    """
    Construct for unpacking 1, 2, and 4-bit data.
    """

    return GreedyRange(BitsInteger(nbits))


def unpack(
    raw: bytes,
    nbits: int,
) -> np.ndarray:

    """
    Unpack 1, 2 and 4-bit data.
    """

    if nbits in packed:
        data = greedybits(nbits).parse(bytes2bits(raw))
    return np.asarray(
        data,
        dtype=np.uint8,
    )