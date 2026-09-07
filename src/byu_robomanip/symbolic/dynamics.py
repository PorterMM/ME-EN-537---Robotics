import sympy as sp
from byu_robomanip.symbolic import kinematics as kin


class SerialArmDyn(kin.SerialArm):
    """
    SerialArmDyn class represents serial arms with dynamic properties and is used to calculate forces, torques, accelerations,
    joint forces, etc. using the Euler-Lagrange formulations.

    ``grav`` is the positive vector used to construct potential energy
    ``P = sum(m_i * grav.T * p_i)``. It is intentionally distinct from the
    downward physical acceleration vector passed to numerical RNE.
    """

    def __init__(
        self,
        dh,
        jt=None,
        base=sp.eye(4),
        tip=sp.eye(4),
        joint_limits=None,
        mass=None,
        r_com=None,
        link_inertia=None,
        motor_inertia=None,
        joint_damping=None,
        radians=True,
        grav=sp.Matrix(3, 1, [0, 0, 0]),
    ):

        kin.SerialArm.__init__(self, dh, jt, base, tip, radians)
        self.masses = mass
        self.coms = r_com
        self.Is = link_inertia
        self.Ims = motor_inertia

        self.q_sym = sp.symbols("q_1:" + str(self.n + 1), real=True)
        self.qd_sym = sp.symbols("qd_1:" + str(self.n + 1), real=True)
        self.qdd_sym = sp.symbols("qdd_1:" + str(self.n + 1), real=True)
        self.g_sym = sp.Matrix(3, 1, sp.symbols("gx, gy, gz"), real=True)

        self.grav = grav
        self.generate_EL()

    def generate_EL(self):
        """
        Generate and store numerical callables for M(q), C(q, qd), and G(q).

        The intended derivation is:

        1. Find each link COM position and its translational/angular Jacobian.
        2. Use the Jacobians to form the kinetic-energy mass matrix ``M``.
        3. Use the partial derivatives of ``M`` to form the Coriolis matrix
           ``C`` using Christoffel symbols.
        4. Form the potential energy ``P`` and differentiate it to obtain
           ``G``.
        5. Convert the symbolic matrices to numerical callables with
           :func:`sympy.lambdify`.

        The generated ``C(q, qd)`` callable returns the Coriolis matrix. Obtain
        the generalized Coriolis/centrifugal vector with ``C(q, qd) @ qd``.
        This differs from numerical ``SerialArmDyn.get_C``, which directly
        returns that vector.
        """
        # Suggested roadmap:
        #
        # For each link i, use self.fk(q, i + 1) to get its pose and transform
        # self.coms[i] into the base frame.  Then evaluate self.jacob_shift at
        # that COM.  Its first three rows are Jv_i and its last three rows are
        # Jw_i.  Keep the link rotation R_i^0 as well; the inertia tensor is
        # supplied in the link frame and must be rotated into the base frame.
        #
        # The main symbolic quantities below are deliberately initialized for
        # you.  Fill them in using the following stages:
        #
        #   M += m_i * Jv_i.T * Jv_i
        #        + Jw_i.T * R_i^0 * I_i * (R_i^0).T * Jw_i
        #
        #   C[k, j] = sum_i 1/2 * (
        #       dM[k, j]/dq_i + dM[k, i]/dq_j - dM[i, j]/dq_k
        #   ) * qd_i
        #
        #   P += m_i * self.grav.T * p_com_i
        #   G[k] = dP/dq_k
        #
        # Here ``self.grav`` is the positive vector used in the potential
        # energy convention documented above.  The numerical HW08 interface
        # instead receives a downward physical acceleration vector.
        jacob_com = []
        T_jts = []
        M_EL = sp.zeros(self.n, self.n)
        C_EL = sp.zeros(self.n, self.n)
        P = sp.Matrix([0])
        G_EL = sp.zeros(self.n, 1)

        # These symbolic variables are provided because they are the inputs to
        # the final numerical callables below.
        q = self.q_sym
        qd = self.qd_sym

        # TODO - use one loop to store each link transform, COM position, and
        #         COM Jacobian in T_jts and jacob_com.
        # TODO - use one loop to add each link's translational and rotational
        #         kinetic-energy terms to M_EL.
        # TODO - use three nested loops to fill C_EL from derivatives of M_EL.
        # TODO - use one loop to add each link's contribution to P.
        # TODO - use one loop to differentiate P and fill G_EL.
        # TODO - lambdify M_EL, C_EL, and G_EL with the correct symbolic inputs.

        # HW10 student task

        # Provided: convert the symbolic expressions to numerical callables.
        # The first argument lists the symbolic inputs; the second is the
        # expression to evaluate; and "numpy" selects NumPy-compatible output.
        self.M = sp.lambdify([q], M_EL, "numpy")
        self.C = sp.lambdify([q, qd], C_EL, "numpy")
        self.G = sp.lambdify([q], G_EL, "numpy")


        raise NotImplementedError("Complete SerialArmDyn.generate_EL for HW10")


if __name__ == "__main__":

    r = sp.Matrix(3, 1, [-0.5, 0, 0])
    a = 1
    m = 1
    I = sp.Matrix([[0, 0, 0], [0, a**2 * m / 12, 0], [0, 0, a**2 * m / 12]])

    dh = [[0, 0, a, 0], [0, 0, a, 0]]

    joint_type = ["r", "r"]
    link_masses = [m, m]
    r_coms = [r, r]
    link_inertias = [I, I]
    arm = SerialArmDyn(
        dh, jt=joint_type, mass=link_masses, r_com=r_coms, link_inertia=link_inertias
    )

    print(arm.M([0] * 2))
