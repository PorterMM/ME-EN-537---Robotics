"""Limited public checks for numerical kinematics interfaces."""

import numpy as np
from numpy.testing import assert_allclose

from byu_robomanip.kinematics import SerialArm


def test_hw04_zero_configuration_matches_course_frame_convention():
    arm = SerialArm(
        [
            [0.0, 0.0, 0.4, 0.0],
            [0.0, 0.0, 0.4, 0.0],
            [0.0, 0.0, 0.4, 0.0],
        ]
    )

    transform = arm.fk(np.zeros(3))

    assert transform.shape == (4, 4)
    assert_allclose(transform[:3, 3], [1.2, 0.0, 0.0], atol=1e-12)


def test_hw05_jacobian_has_one_column_per_joint():
    arm = SerialArm(
        [
            [0.0, 0.0, 0.3, 0.0],
            [0.0, 0.0, 0.2, 0.0],
        ]
    )

    jacobian = arm.jacob([0.2, -0.1])

    assert jacobian.shape == (6, arm.n)
    assert np.all(np.isfinite(jacobian))
