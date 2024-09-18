import re
import numpy as np


def _bpf(fn):
    with open(fn, "r") as f:
        lines = f.readlines()

    fields = {}
    for line in lines:
        if line.startswith("#"):
            cleaned = line.strip()
            cleaned = cleaned.replace("#", "")
            if len(cleaned) > 0:
                key, string = list(map(str.strip, re.split(r"[=<]", cleaned)))
                fields[key] = string

    meta = {}
    for key, string in fields.items():
        varname, vartype = {
            "Input file": ("filenm", str),
            "Candidate": ("candnm", str),
            "Telescope": ("telescope", str),
            "Epoch_topo": ("tepoch", float),
            "Epoch_bary": ("bepoch", float),
            "T_sample": ("dt", float),
            "Data Folded": ("N", float),
            "Data Avg": ("data_avg", float),
            "Data StdDev": ("data_std", float),
            "Profile Bins": ("proflen", int),
            "Profile Avg": ("prof_avg", float),
            "Profile StdDev": ("prof_std", float),
            "Reduced chi-sqr": ("redchi", float),
            "Prob(Noise)": (None, None),
            "Best DM": ("bestdm", float),
            "P_topo (ms)": ("p_topo", float),
            "P'_topo (s/s)": ("pd_topo", float),
            "P''_topo (s/s^2)": ("pdd_topo", float),
            "P_bary (ms)": ("p_bary", float),
            "P'_bary (s/s)": ("pd_bary", float),
            "P''_bary (s/s^2)": ("pdd_bary", float),
            "P_orb (s)": ("orb_p", float),
            "asin(i)/c (s)": ("orb_x", float),
            "eccentricity": ("orb_e", float),
            "w (rad)": ("orb_w", float),
            "T_peri": ("orb_t", float),
        }[key]

        if key != "Prob(Noise)":
            if key in [
                "P_topo (ms)",
                "P'_topo (s/s)",
                "P''_topo (s/s^2)",
                "P_bary (ms)",
                "P'_bary (s/s)",
                "P''_bary (s/s^2)",
            ]:
                meta[varname], meta["".join([varname, "_err"])] = None, None
                if string != "N/A":
                    values = string.split("+/-")
                    value, error = list(map(vartype, values))
                    meta[varname], meta["".join([varname, "_err"])] = value, error
            else:
                meta[varname] = None
                if string != "N/A":
                    meta[varname] = vartype(string)
        else:
            regex = re.compile(r"[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?")
            if (matches := re.findall(regex, string)) is not None:
                meta["chi_prob"], meta["chi_sig"] = list(map(float, matches))

    meta["topo"] = {
        "p": meta.pop("p_topo"),
        "pd": meta.pop("pd_topo"),
        "pdd": meta.pop("pdd_topo"),
        "p_err": meta.pop("p_topo_err"),
        "pd_err": meta.pop("pd_topo_err"),
        "pdd_err": meta.pop("pdd_topo_err"),
    }

    meta["bary"] = {
        "p": meta.pop("p_bary"),
        "pd": meta.pop("pd_bary"),
        "pdd": meta.pop("pdd_bary"),
        "p_err": meta.pop("p_bary_err"),
        "pd_err": meta.pop("pd_bary_err"),
        "pdd_err": meta.pop("pdd_bary_err"),
    }

    meta["orb"] = {
        "p": meta.pop("orb_p"),
        "x": meta.pop("orb_x"),
        "e": meta.pop("orb_e"),
        "w": meta.pop("orb_w"),
        "t": meta.pop("orb_t"),
    }

    data = [float(_) for _ in re.findall(r"^\s+\d+\s+(.+)$", "".join(lines), re.M)]
    data = np.asarray(data)
    return meta, data
