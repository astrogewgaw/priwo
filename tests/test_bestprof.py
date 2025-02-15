from priwo import readbestprof


def test_bestprof(datadir):
    meta, _ = readbestprof(str(datadir / "test.bestprof"))
    assert meta == {
        "filenm": "J1646-2142_500_200_512_2.15jul2k19.raw0.fil",
        "candnm": "PSR_1646-2142",
        "telescope": "GMRT",
        "tepoch": 58679.6856653963,
        "bepoch": None,
        "dt": 1.024e-05,
        "N": 263664000.0,
        "data_avg": 11042.9913182359,
        "data_std": 246.537468521724,
        "proflen": 128,
        "prof_avg": 22747152667.3743,
        "prof_std": 353837.098935206,
        "redchi": 106.001,
        "chi_prob": 0.0,
        "chi_sig": 112.9,
        "bestdm": 29.741,
        "topo": {
            "p": 5.85347537656615,
            "pd": -0.0,
            "pdd": 0.0,
            "p_err": 5.16e-08,
            "pd_err": 1.48e-13,
            "pdd_err": 3.55e-16,
        },
        "bary": {
            "p": None,
            "pd": None,
            "pdd": None,
            "p_err": None,
            "pd_err": None,
            "pdd_err": None,
        },
        "orb": {"p": None, "x": None, "e": None, "w": None, "t": None},
    }
