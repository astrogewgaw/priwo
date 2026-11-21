"""
Type aliases used across priwo.
"""

import io

BinaryFile = io.BufferedReader | io.BufferedWriter | io.BufferedRandom | io.FileIO
TextFile = io.TextIOWrapper

__all__ = ["BinaryFile", "TextFile"]
