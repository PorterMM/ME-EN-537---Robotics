"""Limited intermediate-value checkpoint for the published HW08 RNE case.

This helper intentionally checks only the one three-link configuration stated
in the homework. It is a debugging aid, not a general RNE answer oracle.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike

CHECKPOINT_ATOL = 5e-5

# Each column is expressed in its corresponding link frame. These rounded
# values are the faculty-published debugging checkpoints for Problem 2(a).
EXPECTED_COM_ACCELERATIONS = np.array(
    [
        [-0.0548, -0.2393, -0.2041],
        [-0.1047, 0.0342, 0.4866],
        [0.0, 0.0, 0.0],
    ]
)
EXPECTED_JOINT_FORCES = np.array(
    [
        [20.0753, 18.8923, 6.7326],
        [20.3562, 0.2339, -6.4501],
        [0.0, 0.0, 0.0],
    ]
)
EXPECTED_MASS_MATRIX = np.array(
    [
        [1.0825, 0.5428, 0.1066],
        [0.5428, 0.3731, 0.1066],
        [0.1066, 0.1066, 0.0500],
    ]
)
EXPECTED_ZERO_LINK_ORIGINS = np.array(
    [
        [0.4, 0.0, 0.0],
        [0.8, 0.0, 0.0],
        [1.2, 0.0, 0.0],
    ]
)

CHECKPOINT_GUIDANCE = {
    "center-of-mass accelerations": (
        "Check the outward recursion, the gravity sign, the COM offset in "
        "the correct frame, and the angular-acceleration cross-product terms."
    ),
    "joint forces": (
        "Check the inward recursion, the terminal wrench condition, the "
        "force/moment rows, and the frame used for each wrench."
    ),
    "mass matrix": (
        "Check the unit joint-acceleration runs used to form each column of "
        "M(q), and verify that all columns use the same q configuration."
    ),
    "zero-configuration link origins": (
        "Check the DH convention, link lengths, joint-angle units, and that "
        "the zero configuration places all links along +x."
    ),
}


def _load_hw08_params():
    """Load the sibling parameter file in module or direct-file mode."""

    if __package__:
        from homework.hw08 import params_hw08

        return params_hw08

    params_path = Path(__file__).with_name("params_hw08.py")
    spec = importlib.util.spec_from_file_location("hw08_params", params_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load HW08 parameters from {params_path}")

    params = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(params)
    return params


def _format_array(values: np.ndarray) -> str:
    """Format a checkpoint array for readable student-facing output."""

    return np.array2string(
        values,
        precision=4,
        suppress_small=False,
        floatmode="fixed",
        separator="  ",
    )


def print_expected_checkpoints() -> None:
    """Print the rounded reference arrays for the published HW08 case."""

    print("\nPublished HW08 reference values (rounded):")
    print("A_com (columns are links 1, 2, and 3 in frames 1, 2, and 3):")
    print(_format_array(EXPECTED_COM_ACCELERATIONS))
    print("\nf (columns are links 1, 2, and 3 in frames 1, 2, and 3):")
    print(_format_array(EXPECTED_JOINT_FORCES))
    print("\nM(q) at the published configuration:")
    print(_format_array(EXPECTED_MASS_MATRIX))
    print("\nLink origins at q = [0, 0, 0], expressed in frame 0:")
    print(_format_array(EXPECTED_ZERO_LINK_ORIGINS))


def _check_array(
    name: str,
    actual: ArrayLike,
    expected: np.ndarray,
    frame_guidance: str,
    troubleshooting_guidance: str,
    atol: float,
) -> bool:
    """Report one high-level checkpoint without identifying an incorrect entry."""

    try:
        values = np.asarray(actual, dtype=float)
    except (TypeError, ValueError):
        print(f"{name}: REVIEW -- values must form a numerical array.")
        return False

    if values.shape != expected.shape:
        print(f"{name}: REVIEW -- expected shape {expected.shape}, got {values.shape}.")
        print(f"  Frame reminder: {frame_guidance}")
        print(f"  Suggested checks: {troubleshooting_guidance}")
        return False
    if not np.all(np.isfinite(values)):
        print(f"{name}: REVIEW -- the array contains a non-finite value.")
        print(f"  Suggested checks: {troubleshooting_guidance}")
        return False

    residual = float(np.max(np.abs(values - expected)))
    passed = bool(np.allclose(values, expected, rtol=0.0, atol=atol))
    status = "PASS" if passed else "REVIEW"
    print(
        f"{name}: {status} -- maximum absolute residual {residual:.3e} "
        f"(tolerance {atol:.1e})."
    )
    if not passed:
        print(f"  Frame reminder: {frame_guidance}")
        print(f"  Suggested checks: {troubleshooting_guidance}")
        print(f"  Expected {name}:\n{_format_array(expected)}")
        print(f"  Actual {name}:\n{_format_array(values)}")
    return passed


def check_rne_checkpoint(
    *,
    com_accelerations: ArrayLike | None = None,
    joint_forces: ArrayLike | None = None,
    mass_matrix: ArrayLike | None = None,
    zero_link_origins: ArrayLike | None = None,
    atol: float = CHECKPOINT_ATOL,
) -> dict[str, bool]:
    """Check selected values for the single published HW08 configuration.

    ``com_accelerations`` and ``joint_forces`` are 3-by-3 arrays. Their columns
    must correspond to links 1--3 and must be expressed in the corresponding
    link frame. For the RNE return value, ``joint_forces`` is normally
    ``wrenches[:3, :]``. ``mass_matrix`` is the 3-by-3 ``M(q)`` from Problem
    2(b). ``zero_link_origins`` contains the three link origins at the zero
    configuration, expressed in frame 0.

    The returned dictionary maps each supplied checkpoint name to ``True`` or
    ``False``. A passing checkpoint is useful debugging evidence, but does not
    establish that RNE works for other configurations.
    """

    if all(
        value is None
        for value in (
            com_accelerations,
            joint_forces,
            mass_matrix,
            zero_link_origins,
        )
    ):
        raise ValueError("supply at least one HW08 checkpoint array")
    if not np.isfinite(atol) or atol <= 0.0:
        raise ValueError("atol must be a positive finite number")

    print("HW08 RNE checkpoint: published three-link configuration only")
    print_expected_checkpoints()
    results = {}
    if com_accelerations is not None:
        results["com_accelerations"] = _check_array(
            "center-of-mass accelerations",
            com_accelerations,
            EXPECTED_COM_ACCELERATIONS,
            "column i is expressed in link frame i.",
            CHECKPOINT_GUIDANCE["center-of-mass accelerations"],
            atol,
        )
    if joint_forces is not None:
        results["joint_forces"] = _check_array(
            "joint forces",
            joint_forces,
            EXPECTED_JOINT_FORCES,
            "use the force rows of each wrench in its corresponding link frame.",
            CHECKPOINT_GUIDANCE["joint forces"],
            atol,
        )
    if mass_matrix is not None:
        results["mass_matrix"] = _check_array(
            "mass matrix",
            mass_matrix,
            EXPECTED_MASS_MATRIX,
            "M(q) is expressed in joint coordinates.",
            CHECKPOINT_GUIDANCE["mass matrix"],
            atol,
        )
    if zero_link_origins is not None:
        results["zero_link_origins"] = _check_array(
            "zero-configuration link origins",
            zero_link_origins,
            EXPECTED_ZERO_LINK_ORIGINS,
            "each row is a link origin expressed in frame 0.",
            CHECKPOINT_GUIDANCE["zero-configuration link origins"],
            atol,
        )
    return results


def main() -> int:
    """Run the published HW08 checkpoints with the current package."""

    from byu_robomanip.dynamics import SerialArmDyn

    P = _load_hw08_params()

    arm = SerialArmDyn(
        P.dh,
        jt=P.joint_types,
        mass=P.link_masses,
        r_com=[row.copy() for row in P.r_i2com_i],
        link_inertia=[np.array(P.link_inertia) for _ in P.joint_types],
    )
    _torque, wrenches = arm.rne(P.q, P.qd, P.qdd, g=P.g_in_0)
    zero_q = np.zeros(len(P.joint_types))
    zero_link_origins = np.array(
        [arm.fk(zero_q, index=i + 1)[:3, 3] for i in range(arm.n)]
    )
    results = check_rne_checkpoint(
        joint_forces=wrenches[:3, :],
        mass_matrix=arm.get_M(P.q),
        zero_link_origins=zero_link_origins,
    )

    if all(results.values()):
        print("HW08 joint-force, mass-matrix, and zero-configuration checks passed.")
        return 0

    print("HW08 checkpoint needs review.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
