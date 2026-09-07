"""
dynamics Module - Contains code for:
- Dynamic SerialArm class
- RNE Algorithm
- Euler - Lagrange formulation

John Morrell, Jan 28 2022
Tarnarmour@gmail.com

modified by:
Marc Killpack, October 25, 2022
               Nov. 20, 2023
"""

import numpy as np
from byu_robomanip.kinematics import SerialArm


class SerialArmDyn(SerialArm):
    """
    SerialArmDyn class represents serial arms with dynamic properties and is used to calculate forces, torques, accelerations,
    joint forces, etc. using the Newton-Euler and Euler-Lagrange formulations. It inherits from the previously defined kinematic
    robot arm class "SerialArm".
    """

    def __init__(
        self,
        dh,
        jt=None,
        base=np.eye(4),
        tip=np.eye(4),
        joint_limits=None,
        mass=None,
        r_com=None,
        link_inertia=None,
        motor_inertia=None,
        joint_damping=None,
    ):

        SerialArm.__init__(self, dh, jt, base, tip, joint_limits)
        self.mass = mass
        self.r_com = r_com
        self.link_inertia = link_inertia
        self.motor_inertia = motor_inertia
        if joint_damping is None:
            self.B = np.zeros((self.n, self.n))
        else:
            self.B = np.diag(joint_damping)

    def rne(
        self,
        q,
        qd,
        qdd,
        Wext=np.zeros((6,)),
        g=np.zeros((3,)),
        omega_base=np.zeros((3,)),
        alpha_base=np.zeros((3,)),
        v_base=np.zeros((3,)),
        acc_base=np.zeros((3,)),
    ):
        """
        tau, W = RNE(q, qd, qdd):
        returns the torque in each joint (and the full wrench at each joint) given the joint configuration, velocity, and accelerations
        Args:
            q: Joint positions.
            qd: Joint velocities.
            qdd: Joint accelerations.
            Wext: External tip wrench, expressed in the tip frame.
            g: Physical gravitational acceleration expressed in frame 0. For
                example, the HW08 downward acceleration is [0, -9.81, 0].

        Returns:
            tau: Generalized joint forces.
            W: Joint wrenches, with column i expressed in link frame i.

        We start with the velocity and acceleration of the base frame, v0 and a0, and the joint positions, joint velocities,
        and joint accelerations (q, qd, qdd).

        For each joint, we find the new angular velocity, w_i = w_(i-1) + z * qdot_(i-1)
        v_i = v_(i-1) + w_i x r_(i-1, com_i)


        if motor inertia is None, we don't consider it. Solve for now without motor inertia. The solution will provide code for motor inertia as well.
        """

        # TODO: Implement the recursive Newton-Euler dynamics calculation.
        # HW08 student task

        raise NotImplementedError("Complete SerialArmDyn.rne for HW08")

    def get_M(self, q):
        """Return the numerical joint-space mass matrix M(q)."""
        # TODO: Compute the numerical joint-space mass matrix M(q).
        # HW08 student task

        raise NotImplementedError("Complete SerialArmDyn.get_M for HW08")

    def get_C(self, q, qd):
        """Return the Coriolis/centrifugal vector C(q, qd) @ qd.

        Unlike the symbolic HW10 ``C`` callable, this method does not return
        the Coriolis matrix itself.
        """
        # TODO: Compute the numerical Coriolis/centrifugal vector C(q, qd) @ qd.
        # HW08 student task

        raise NotImplementedError("Complete SerialArmDyn.get_C for HW08")

    def get_G(self, q, g):
        """Return the gravity generalized-force vector for acceleration ``g``.

        ``g`` is the physical acceleration vector expressed in frame 0, not
        the positive potential-energy vector used by the symbolic HW10 model.
        """
        # TODO: Compute the numerical gravity generalized-force vector G(q).
        # HW08 student task

        raise NotImplementedError("Complete SerialArmDyn.get_G for HW08")


if __name__ == "__main__":

    ## this just gives an example of how to define a robot, this is a planar 3R robot.
    dh = [[0, 0, 0.4, 0], [0, 0, 0.4, 0], [0, 0, 0.4, 0]]

    joint_type = ["r", "r", "r"]

    link_masses = [1, 1, 1]

    # defining three different centers of mass, one for each link
    r_coms = [np.array([-0.2, 0, 0]), np.array([-0.2, 0, 0]), np.array([-0.2, 0, 0])]

    link_inertias = []
    for i in range(len(joint_type)):
        iner = 0.01
        # this inertia tensor is only defined as having Izz non-zero
        link_inertias.append(np.array([[0, 0, 0], [0, 0, 0], [0, 0, iner]]))

    arm = SerialArmDyn(
        dh, jt=joint_type, mass=link_masses, r_com=r_coms, link_inertia=link_inertias
    )

    # once implemented, you can call arm.RNE and it should work.
    q = [np.pi / 4.0] * 3
    qd = [np.pi / 6.0, -np.pi / 4.0, np.pi / 3.0]
    qdd = [-np.pi / 6.0, np.pi / 3.0, np.pi / 6.0]
    arm.rne(q, qd, qdd, g=np.array([0, -9.81, 0]))
