from typing import Annotated

import numpy
from numpy.typing import NDArray

def unpack(
    x: Annotated[NDArray[numpy.uint8], {"order": "C"}],
    nbits: int,
    bitorder: str = "big",
    parallel: bool = False,
) -> Annotated[NDArray[numpy.uint8], {"order": "C"}]: ...
def pack(
    x: Annotated[NDArray[numpy.uint8], {"order": "C"}],
    nbits: int,
    bitorder: str = "big",
    parallel: bool = False,
) -> Annotated[NDArray[numpy.uint8], {"order": "C"}]: ...
