"""
Transforms Module - Contains code to describe SO(3) and SE(3)

Key for HW 04
"""

import numpy as np
from numpy import sin, cos, sqrt
from numpy.typing import NDArray
from byu_robomanip.utility import clean_rotation_matrix


## 2D Rotations
def rot2(theta: float) -> NDArray:
    """
    R = rot2(th)

    :param float theta: angle of rotation (rad)
    :return R: 2x2 numpy array representing rotation in 2D by theta
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], 
                     [s, c]])


## 3D Rotations
def rotx(theta: float) -> NDArray:
    """
    R = rotx(theta)

    :param float theta: angle of rotation (rad)
    :return R: 3x3 numpy array representing rotation about x-axis by amount theta
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0],
                    [0, c, -s],
                    [0, s, c]])


def roty(theta: float) -> NDArray:
    """
    R = roty(theta)

    :param float theta: angle of rotation (rad)
    :return R: 3x3 numpy array representing rotation about y-axis by amount theta
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s],
                    [0, 1, 0],
                    [-s, 0, c]])


def rotz(theta: float) -> NDArray:
    """
    R = rotz(theta)

    :param float theta: angle of rotation (rad)
    :return R: 3x3 numpy array representing rotation about z-axis by amount theta
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0],
                    [s, c, 0],
                    [0, 0, 1]])


# inverse of rotation matrix
def rot_inv(R: NDArray) -> NDArray:
    """
    R_inv = rot_inv(R)

    :param NDArray R: 2x2 or 3x3 numpy array representing a proper rotation matrix
    :return R_inv: 2x2 or 3x3 inverse of the input rotation matrix
    """
    # I think you told us to do it another way but ¯\_(ツ)_/¯
    return np.linalg.inv(R)


def se3(R: NDArray = np.eye(3), p: NDArray = np.zeros(3)) -> NDArray:
    """
    T = se3(R, p)

    Creates a 4x4 homogeneous transformation matrix "T" from a 3x3 rotation matrix
    and a position vector.

    :param NDArray R: 3x3 numpy array representing orientation, defaults to identity.
    :param NDArray p: numpy array representing position, defaults to [0, 0, 0].
    :return T: 4x4 numpy array representing the homogeneous transform.
    """
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = p
    return T

def DHval(theta: float, d: float, alpha: float, a: float) -> NDArray:
    """
    Creates the DH tranform based on values.

    """

    ct, st, ca, sa = np.cos(theta), np.sin(theta), np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct, -st * ca,  sa * st, a * ct],
        [st,  ca * ct, -sa * ct, a * st],
        [ 0,       sa,       ca,      d],
        [ 0,        0,        0,      1]
    ])

def inv(T: NDArray) -> NDArray:
    """
    T_inv = inv(T)

    Returns the inverse transform to T.

    :param NDArray T: 4x4 homogeneous transformation matrix
    :return T_inv: 4x4 numpy array that is the inverse to T so that T @ T_inv = I
    """
    # I think you told us to do it another way but ¯\_(ツ)_/¯  
    return np.linalg.inv(T)


def R2rpy(R: NDArray) -> NDArray:
    """
    rpy = R2rpy(R)

    Returns the roll-pitch-yaw representation of the SO3 rotation matrix.

    :param NDArray R: 3x3 Numpy array for any rotation.
    :return rpy: Numpy array, containing [roll, pitch, yaw] coordinates (in radians).
    """

    # TODO: Implement conversion from a rotation matrix to roll-pitch-yaw angles.
    # HW04 student task

    R = np.asarray(R, dtype=float)
    horizontal = np.hypot(R[0, 0], R[1, 0])
    pitch = np.arctan2(-R[2, 0], horizontal)
    if horizontal > 1e-12:
        roll = np.arctan2(R[2, 1], R[2, 2])
        yaw = np.arctan2(R[1, 0], R[0, 0])
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        yaw = 0.0
    return np.array([roll, pitch, yaw])


def R2axis(R: NDArray) -> NDArray:
    """
    axis_angle = R2axis(R)

    Returns an axis angle representation of a SO(3) rotation matrix.

    :param NDArray R: 3x3 rotation matrix.
    :return axis_angle: numpy array containing the axis angle representation
        in the form: [angle, rx, ry, rz]
    """

    # see equation (2.27) and (2.28) on pg. 54, using functions like "np.acos," "np.sin," etc.

    # TODO: Implement conversion from a rotation matrix to axis-angle form.
    # HW04 student task

    q = R2quat(R)
    length = np.linalg.norm(q[1:])
    if length == 0.0:
        return np.array([0.0, 1.0, 0.0, 0.0])
    angle = 2.0 * np.arctan2(length, q[0])
    return np.concatenate(([angle], q[1:] / length))


def axis2R(angle: float, axis: NDArray) -> NDArray:
    """
    R = axis2R(angle, axis)

    Returns an SO3 object of the rotation specified by the axis-angle.

    :param float angle: the angle to rotate about the axis (in radians).
    :param NDArray axis: components of the unit axis about which to rotate as
        a numpy array [rx, ry, rz].
    :return R: 3x3 numpy array representing the rotation matrix.
    """

    # follow formula in book, see equation (2.25) on pg. 54
    # TODO: Implement conversion from axis-angle form to a rotation matrix.
    # HW04 student task

    axis = np.asarray(axis, dtype=float).reshape(3)
    length = np.linalg.norm(axis)
    if not np.isfinite(angle) or not np.all(np.isfinite(axis)):
        raise ValueError("Angle and axis must be finite")
    if length == 0.0:
        if angle == 0.0:
            return np.eye(3)
        raise ValueError("Rotation axis must be nonzero")
    x, y, z = axis / length
    S = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    return np.eye(3) + np.sin(angle) * S + (1.0 - np.cos(angle)) * (S @ S)


def R2quat(R: NDArray) -> NDArray:
    """
    quaternion = R2quat(R)

    Returns a quaternion representation of pose.

    :param NDArray R: 3x3 rotation matrix.
    :return quaternion: numpy array for the quaternion representation of pose in
        the format [nu, ex, ey, ez]
    """

    # TODO: Implement conversion from a rotation matrix to quaternion form.
    # HW04 student task

    R = np.asarray(R, dtype=float)
    trace = np.trace(R)
    if trace > 0.0:
        s = 2.0 * np.sqrt(1.0 + trace)
        q = np.array([
            0.25 * s,
            (R[2, 1] - R[1, 2]) / s,
            (R[0, 2] - R[2, 0]) / s,
            (R[1, 0] - R[0, 1]) / s,
        ])
    else:
        i = int(np.argmax(np.diag(R)))
        j, k = (i + 1) % 3, (i + 2) % 3
        s = 2.0 * np.sqrt(max(0.0, 1.0 + R[i, i] - R[j, j] - R[k, k]))
        q = np.empty(4)
        q[0] = (R[k, j] - R[j, k]) / s
        q[i + 1] = 0.25 * s
        q[j + 1] = (R[j, i] + R[i, j]) / s
        q[k + 1] = (R[k, i] + R[i, k]) / s
    q /= np.linalg.norm(q)
    return -q if q[0] < 0.0 else q


def quat2R(q: NDArray) -> NDArray:
    """
    R = quat2R(q)

    Returns a 3x3 rotation matrix from a quaternion.

    :param NDArray q: [nu, ex, ey, ez ] - defining the quaternion.
    :return R: numpy array, 3x3 rotation matrix.
    """

    # TODO: Implement conversion from quaternion form to a rotation matrix.
    # HW04 student task

    q = np.asarray(q, dtype=float).reshape(4)
    if not np.all(np.isfinite(q)) or not np.any(q):
        raise ValueError("Quaternion must be finite and nonzero")
    q = q / np.max(np.abs(q))
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1 - 2 * (y*y + z*z), 2 * (x*y - w*z), 2 * (x*z + w*y)],
        [2 * (x*y + w*z), 1 - 2 * (x*x + z*z), 2 * (y*z - w*x)],
        [2 * (x*z - w*y), 2 * (y*z + w*x), 1 - 2 * (x*x + y*y)],
    ])


def euler2R(th1: float, th2: float, th3: float, order: str = "xyz") -> NDArray:
    """
    R = euler2R(th1, th2, th3, order='xyz')

    Returns a 3x3 rotation matrix as specified by the euler angles, we assume in all cases
    that these are defined about the "current axis," which is why there are only 12 versions
    (instead of the 24 possiblities noted in the course slides).

    :param float th1: angle of rotation about 1st axis (rad)
    :param float th2: angle of rotation about 2nd axis (rad)
    :param float th3: angle of rotation about 3rd axis (rad)
    :param str order: specifies the euler rotation to use, for example 'xyx', 'zyz', etc.
    :return R: 3x3 numpy array, the rotation matrix.
    """

    # TODO: Implement conversion from Euler angles to a rotation matrix.
    # HW04 student task

    if (not isinstance(order, str) or len(order) != 3
            or any(axis not in "xyz" for axis in order)
            or order[0] == order[1] or order[1] == order[2]):
        raise ValueError("Order must be one of the 12 intrinsic Euler sequences")
    rotations = {"x": rotx, "y": roty, "z": rotz}
    R = np.eye(3)
    for axis, angle in zip(order, (th1, th2, th3)):
        R = R @ rotations[axis](angle)
    return R
