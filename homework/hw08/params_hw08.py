"""
HW 10 reuses the parameters from HW 8, so they are defined in this file for
convenience. This file is imported by both HW 8 and HW 10.
"""

import numpy as np

# defining kinematic parameters for robot
dh = [[0, 0, 0.4, 0], [0, 0, 0.4, 0], [0, 0, 0.4, 0]]

joint_types = ["r", "r", "r"]

link_masses = [1, 1, 1]

# r from frame i to center of mass of link i expressed in frame i
r_i2com_i = np.array([[-0.2, 0, 0], [-0.2, 0, 0], [-0.2, 0, 0]])

# Ixx and Iyy are technically non-zero, but they are not used
Izz = 0.01
link_inertia = [[0, 0, 0], [0, 0, 0], [0, 0, Izz]]

g_in_0 = np.array([0, -9.81, 0])

q = [np.pi / 4.0] * 3
qd = [np.pi / 6.0, -np.pi / 4.0, np.pi / 3.0]
qdd = [-np.pi / 6.0, np.pi / 3.0, np.pi / 6.0]
