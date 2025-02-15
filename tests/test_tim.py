import numpy as np
from priwo import readtim


def test_tim(datadir):
    for fn in [
        "test_i8.tim",
        "test_ui8.tim",
        "test_f32.tim",
    ]:
        _, data = readtim(str(datadir / fn))
        assert np.allclose(
            data,
            np.asarray(
                [
                    0.0,
                    1.0,
                    2.0,
                    3.0,
                    4.0,
                    5.0,
                    6.0,
                    7.0,
                    8.0,
                    9.0,
                    10.0,
                    11.0,
                    12.0,
                    13.0,
                    14.0,
                    15.0,
                ],
                dtype=np.float32,
            ),
        )
