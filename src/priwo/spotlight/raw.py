from pathlib import Path

import numpy as np


def readspotlight(fn: str | Path) -> tuple[dict, np.ndarray]:
    raise NotImplementedError


def writespotlight(meta: dict, data: np.ndarray, fn: str | Path) -> None:
    raise NotImplementedError
