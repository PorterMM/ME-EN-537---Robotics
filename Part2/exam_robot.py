"""Define your robot here, then run this file to check its appearance."""

import numpy as np
from byu_robomanip import kinematics as kin

# TODO: enter YOUR DH table from the exam drawing, one row per joint.
# Each row is [theta offset, d, a, alpha], in radians and meters.
# All joint coordinates equal to zero must give the pictured configuration.
dh = None

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
