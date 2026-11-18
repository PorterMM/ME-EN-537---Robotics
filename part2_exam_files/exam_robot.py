"""Define your robot here, then run this file to check its appearance."""

import numpy as np
from byu_robomanip import kinematics as kin

# Each row is [theta offset, d, a, alpha], in radians and meters.
# All joint coordinates equal to zero must give the pictured configuration.
dh = [
    [np.pi/2, 4.0, 0.0, np.pi/2],
    [np.pi/6, 0.0, 0.0, np.pi/2],
    [0.0,     4.0, 0.0, np.pi/2],
    [np.pi/6, 0.0, 2.0, np.pi/2],
]

if dh is None:
    raise NotImplementedError(
        "Derive the robot's DH table and replace dh = None in exam_robot.py."
    )

arm = kin.SerialArm(dh)


if __name__ == "__main__":
    # This preview runs only when you run exam_robot.py directly.
    from byu_robomanip.visualization import VizScene

    viz = VizScene()
    viz.add_arm(arm)
    viz.update(qs=[np.zeros(arm.n).tolist()])
    viz.hold()
