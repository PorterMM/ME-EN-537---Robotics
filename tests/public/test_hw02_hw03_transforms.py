"""Limited public checks for HW02-HW03 transformation conventions."""

import numpy as np
from numpy.testing import assert_allclose

from byu_robomanip import transforms


def test_hw02_rotation_and_inverse_have_expected_structure():
    rotation = transforms.rotz(np.pi / 3.0)

    assert rotation.shape == (3, 3)
    assert_allclose(rotation.T @ rotation, np.eye(3), atol=1e-10)
    assert_allclose(transforms.rot_inv(rotation) @ rotation, np.eye(3), atol=1e-10)


def test_hw03_homogeneous_transform_has_expected_structure():
    transform = transforms.se3(
        transforms.rotx(0.2),
        np.array([0.3, -0.1, 0.7]),
    )

    assert transform.shape == (4, 4)
    assert_allclose(transform[3, :], [0.0, 0.0, 0.0, 1.0], atol=1e-12)
    assert_allclose(transforms.inv(transform) @ transform, np.eye(4), atol=1e-10)
