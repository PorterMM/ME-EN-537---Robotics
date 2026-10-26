from itertools import product

import numpy as np
import pytest
from numpy.testing import assert_allclose

from byu_robomanip import transforms as tr
from byu_robomanip.kinematics import SerialArm, dh2A


@pytest.mark.parametrize("pitch", [0.147, np.pi / 2, -np.pi / 2, np.pi / 2 - 1e-10])
def test_rpy_round_trip(pitch):
    R = tr.rotz(1.041) @ tr.roty(pitch) @ tr.rotx(0.5299)
    roll, recovered_pitch, yaw = tr.R2rpy(R)
    assert_allclose(tr.rotz(yaw) @ tr.roty(recovered_pitch) @ tr.rotx(roll), R, atol=1e-12)


@pytest.mark.parametrize("angle", [0.0, 1e-10, 0.7, np.pi - 1e-10, np.pi, -np.pi, 4.0])
@pytest.mark.parametrize("axis", [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, -2, 3]])
def test_axis_and_quaternion_round_trips(angle, axis):
    R = tr.axis2R(angle, axis)
    recovered = tr.R2axis(R)
    q = tr.R2quat(R)
    assert_allclose(tr.axis2R(recovered[0], recovered[1:]), R, atol=1e-12)
    assert_allclose(tr.quat2R(q), R, atol=1e-12)
    assert_allclose(tr.quat2R(-7 * q), R, atol=1e-12)
    assert_allclose(R.T @ R, np.eye(3), atol=1e-12)
    assert_allclose(np.linalg.det(R), 1, atol=1e-12)
    assert_allclose(np.linalg.norm(q), 1, atol=1e-12)
    assert q[0] >= 0


@pytest.mark.parametrize("order", ["".join(p) for p in product("xyz", repeat=3) if p[0] != p[1] and p[1] != p[2]])
def test_intrinsic_euler_orders(order):
    from scipy.spatial.transform import Rotation

    assert_allclose(tr.euler2R(0.3, -0.7, 1.2, order),
                    Rotation.from_euler(order.upper(), [0.3, -0.7, 1.2]).as_matrix(), atol=1e-12)


@pytest.mark.parametrize("order", ["xxx", "xxy", "xyy", "abc", "xy", "xyzz", None])
def test_invalid_euler_order(order):
    with pytest.raises(ValueError):
        tr.euler2R(0, 0, 0, order)


@pytest.mark.parametrize("q", [[0, 0, 0, 0], [np.nan, 0, 0, 1], [np.inf, 1, 0, 0], [1, 0, 0]])
def test_invalid_quaternion(q):
    with pytest.raises(ValueError):
        tr.quat2R(q)


@pytest.mark.parametrize("jt", ["r", "p"])
def test_dh_offsets(jt):
    theta, d, a, alpha, q = 0.2, 0.3, 0.4, -0.6, 0.7
    actual = dh2A([theta, d, a, alpha], jt)(q)
    expected = (tr.se3(tr.rotz(theta + (q if jt == "r" else 0)))
                @ tr.se3(p=[0, 0, d + (q if jt == "p" else 0)])
                @ tr.se3(p=[a, 0, 0]) @ tr.se3(tr.rotx(alpha)))
    assert_allclose(actual, expected, atol=1e-12)


def make_arm():
    return SerialArm(
        [[0.2, 0.1, 0.4, 0.6], [-0.3, 0.2, 0.3, -0.5], [0.1, 0, 0.2, 0.4]],
        jt=["r", "p", "r"],
        base=tr.se3(tr.roty(0.7), [0.2, -0.3, 0.4]),
        tip=tr.se3(tr.rotx(-0.4), [0.1, 0.2, -0.1]),
    )


def test_fk_frame_ranges_and_offsets():
    arm = make_arm()
    q = [0.3, 0.2, -0.1]
    full = arm.fk(q)
    assert_allclose(arm.fk(q, base=True, tip=True), arm.base @ full @ arm.tip)
    assert_allclose(arm.fk(q, index=1) @ arm.fk(q, index=[1, 3]), full)
    assert_allclose(arm.fk(q, index=[1, 2], base=True, tip=True), arm.transforms[1](q[1]))
    assert_allclose(arm.fk(q, index=[2, 2]), np.eye(4))
    assert_allclose(arm.fk(q, index=0, base=True), arm.base)
    assert_allclose(arm.fk(q, index=[3, 3], tip=True), arm.tip)
    with pytest.raises(AssertionError):
        arm.fk(q, index=[2, 1])


@pytest.mark.parametrize("index,base,tip", list(product(range(4), [False, True], [False, True])))
def test_jacobian_against_finite_differences(index, base, tip):
    arm = make_arm()
    q = np.array([0.3, 0.2, -0.1])
    J = arm.jacob(q, index=index, base=base, tip=tip)
    expected = np.zeros_like(J)
    R = arm.fk(q, index=index, base=base, tip=tip)[:3, :3]
    for i in range(arm.n):
        dq = np.eye(arm.n)[i] * 1e-6
        plus = arm.fk(q + dq, index=index, base=base, tip=tip)
        minus = arm.fk(q - dq, index=index, base=base, tip=tip)
        derivative = (plus - minus) / 2e-6
        expected[:3, i] = derivative[:3, 3]
        S = derivative[:3, :3] @ R.T
        expected[3:, i] = [S[2, 1], S[0, 2], S[1, 0]]
    assert_allclose(J, expected, atol=1e-9)


def test_published_hw05_jacobians():
    arm = SerialArm([[0, 0, 0.2, np.pi/2], [0, 0, 0.2, -np.pi/2],
                     [0, 0, 0.1, np.pi/2], [0, 0, 0, 0]], jt=["r", "r", "r", "p"])
    assert_allclose(arm.jacob([0, 0, 0, 0]),
                    [[0, 0, 0, 0], [0.5, 0, 0.1, -1], [0, 0.3, 0, 0],
                     [0, 0, 0, 0], [0, -1, 0, 0], [1, 0, 1, 0]], atol=1e-12)
    assert_allclose(arm.jacob([np.pi/4, np.pi/4, np.pi/4, 0.1]),
                    [[-0.3121, -0.1707, -0.1, 0.8536], [0.3121, -0.1707, 0.1, -0.1464],
                     [0, 0.2414, 0, 0.5], [0, 0.7071, -0.5, 0],
                     [0, -0.7071, -0.5, 0], [1, 0, 0.7071, 0]], atol=5e-5)


@pytest.mark.parametrize("method", ["J_T", "pinv"])
def test_ik_reachable_target_and_input_preservation(method):
    arm = SerialArm([[0, 0, 0.7, 0], [0, 0, 0.5, 0]])
    q0 = np.array([[0.2], [0.4]])
    initial = q0.copy()
    target = arm.fk([0.7, 0.8])[:3, 3].reshape(3, 1)
    original_target = target.copy()
    q, error, iters, converged = arm.ik_position(target, q0, method, K=np.eye(3), max_iter=2000)
    assert converged
    assert q.shape == (2,)
    assert 0 < iters <= 2000
    assert np.linalg.norm(error) <= 1e-4
    assert_allclose(error, target.ravel() - arm.fk(q)[:3, 3])
    assert_allclose(q0, initial)
    assert_allclose(target, original_target)


@pytest.mark.parametrize("method,kd", [("J_T", 0.001), ("pinv", 0.001), ("pinv", 0)])
def test_ik_stopping_and_singular_start(method, kd):
    arm = SerialArm([[0, 0, 0.7, 0], [0, 0, 0.5, 0]])
    q, error, iters, converged = arm.ik_position([1.2, 0, 0], method=method, K=np.eye(3), kd=kd)
    assert converged and iters == 0
    assert_allclose(error, 0)
    q, error, iters, converged = arm.ik_position([0.5, 0, 0], method=method, K=np.eye(3), kd=kd, max_iter=5)
    assert not converged and iters == 5
    assert np.all(np.isfinite(q))
    assert_allclose(error, np.array([0.5, 0, 0]) - arm.fk(q)[:3, 3])
    q, error, iters, converged = arm.ik_position([0.5, 0.5, 0], method=method, K=np.eye(3), max_iter=0)
    assert not converged and iters == 0


@pytest.mark.parametrize("method", ["J_T", "pinv"])
def test_ik_unreachable_and_prismatic(method):
    arm = SerialArm([[0, 0, 0.5, 0]])
    with pytest.raises(AssertionError):
        arm.ik_position([2, 0, 0], force=False, K=np.eye(3))
    q, error, iters, converged = arm.ik_position([2, 0, 0], method=method, K=np.eye(3), max_iter=3)
    assert not converged and iters == 3
    assert_allclose(error, np.array([2, 0, 0]) - arm.fk(q)[:3, 3])
    slider = SerialArm([[0, 0, 0, 0]], jt=["p"])
    q, error, iters, converged = slider.ik_position([0, 0, 0.3], method=method, K=np.eye(3))
    assert converged
    assert_allclose(q, [0.3], atol=1e-4)


def test_ik_validation_and_gain():
    arm = SerialArm([[0, 0, 0, 0]], jt=["p"])
    with pytest.raises(AssertionError):
        arm.ik_position([0, 0, 0])
    for kwargs in [{"method": "invalid"}, {"kd": -1}, {"tol": -1}, {"max_iter": -1}]:
        with pytest.raises(ValueError):
            arm.ik_position([0, 0, 0], K=np.eye(3), **kwargs)
    for method in ["J_T", "pinv"]:
        q, error, iters, converged = arm.ik_position([0, 0, 1], method=method, K=0.5*np.eye(3), kd=0, max_iter=1)
        assert_allclose(q, [0.5])
        assert_allclose(error, [0, 0, 0.5])
        assert not converged and iters == 1


def test_fk_iterable_and_scalar_inputs():
    arm = make_arm()
    assert_allclose(arm.fk(iter([0.3, 0.2, -0.1]), index=np.int64(2)),
                    arm.fk([0.3, 0.2, -0.1], index=2))
    slider = SerialArm([[0, 0, 0, 0]], jt=["p"])
    assert_allclose(slider.fk(0.3)[:3, 3], [0, 0, 0.3])


@pytest.mark.parametrize("method", ["J_T", "pinv"])
def test_ik_uses_frame_zero_and_converges_from_singular_start(method):
    arm = SerialArm([[0, 0, 0.7, 0], [0, 0, 0.5, 0]],
                    base=tr.se3(tr.rotz(0.7), [5, 4, 3]),
                    tip=tr.se3(p=[1, 2, 3]))
    target = np.array([0.7, 0.5, 0])
    q, error, iters, converged = arm.ik_position(target, method=method, K=np.eye(3), max_iter=2000)
    assert converged
    assert_allclose(arm.fk(q)[:3, 3], target, atol=1e-4)


def test_ik_debug_plot(monkeypatch):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    pauses = []
    steps = []
    monkeypatch.setattr(plt, "pause", lambda duration: pauses.append(duration))
    monkeypatch.setattr(plt, "waitforbuttonpress", lambda: steps.append(True))
    arm = SerialArm([[0, 0, 0, 0]], jt=["p"])
    q, error, iters, converged = arm.ik_position([0, 0, 0.3], K=np.eye(3), debug=True, debug_step=True)
    assert converged and iters == 1
    assert len(pauses) == len(steps) == 2
    plt.close("all")
