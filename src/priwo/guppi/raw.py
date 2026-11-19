from pathlib import Path

import numpy as np


def readguppi(fn: str | Path) -> list[tuple[dict, np.ndarray]]:
    guppi = []
    fn = Path(fn)
    fsize = fn.stat().st_size
    with open(fn, "rb") as f:
        while True:
            ii = f.tell()
            if ii + 80 > fsize:
                break
            meta = {}
            while True:
                try:
                    line = f.read(80).decode("utf-8").strip()
                    if line.startswith("END"):
                        break
                    key, val = line.split("=")
                    key, val = key.strip(), val.strip()
                    if "'" in val:
                        val = str(val.strip("'").strip())
                    elif "." in val or "e" in val:
                        val = float(val)
                    else:
                        val = int(val)
                    meta[key] = val
                except UnicodeDecodeError:
                    raise ValueError("FILE NOT VALID GUPPI FILE. ABORT.")
                except ValueError:
                    raise ValueError(f"ERROR WHILE READIN BLK {ii}. ABORT.")
            nn = f.tell()
            if "DIRECTIO" in meta and int(meta["DIRECTIO"]) == 1 and nn % 512:
                nn += 512 - nn % 512
            f.seek(nn)

            npol = int(meta["NPOL"])
            nf = int(meta["OBSNCHAN"])
            nbits = int(meta["NBITS"])
            nt = int(int(meta["BLOCSIZE"]) / (nf * npol * (nbits / 8)))

            data = np.fromfile(f, count=meta["BLOCSIZE"], dtype=np.int8)
            data = data.reshape((nf, nt, npol))
            re = data[..., 0:2]
            im = data[..., 2:4]
            data = re + 1j * im
            guppi.append((meta, data))
    return guppi


def writeguppi(guppi: list[tuple[dict, np.ndarray]], fn: str | Path) -> None:
    raise NotImplementedError


__all__ = ["readguppi", "writeguppi"]
