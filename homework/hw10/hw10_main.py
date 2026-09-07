# %%
from byu_robomanip.symbolic import dynamics as dyn
from homework.hw08 import params_hw08 as P
import sympy as sp
import numpy as np

np.set_printoptions(precision=4, suppress=True)


# %%
# defining three different centers of mass, one for each link
r_coms = [sp.Matrix(3, 1, r) for r in P.r_i2com_i]
link_inertias = [sp.Matrix(P.link_inertia)] * len(P.joint_types)

# This is the positive gravity vector used in potential energy, not the
# downward physical acceleration vector passed to numerical RNE.
arm = dyn.SerialArmDyn(
    P.dh,
    jt=P.joint_types,
    mass=P.link_masses,
    r_com=r_coms,
    link_inertia=link_inertias,
    grav=sp.Matrix(3, 1, np.abs(P.g_in_0)),
)


# %% [markdown]
# # Comparing E-L equation output to the answer from RNE from HW 08:
# ## Start with calculating $\tau$, given $q, \dot{q}, \ddot{q}$ (this is HW 08, problem 2a):
# %%

# making q, qd, and qdd into numpy arrays, it works better if we pass
# lists into our E-L functions, but then multiply with the correct
# column vectors. This is a little clunky.
q_vec = np.array(P.q).reshape(3, 1)
qd_vec = np.array(P.qd).reshape(3, 1)
qdd_vec = np.array(P.qdd).reshape(3, 1)

# we could write a function that does this, but I want you to see it explicitly
tau_EL = arm.M(P.q) @ qdd_vec + arm.C(P.q, P.qd) @ qd_vec + arm.G(P.q)

print("tau for E-L is:")
sp.pprint(tau_EL)


# %% [markdown]
# # Comparison for HW 08 - Problem 2, part b) - Mass Matrix

M_EL = arm.M(P.q)
print("generalized mass matrix from E-L is:")
sp.pprint(M_EL)

# %% [markdown]
# # Comparison for HW 08 - Problem 2, part c) - Coriolis terms:
# %%

# calculating C using the E-L function
C_EL = arm.C(P.q, P.qd) @ qd_vec
print("Coriolis vector from E-L is:")
print(C_EL)

G_EL = arm.G(P.q)
print("Gravity vector from E-L is:")
print(G_EL)
