# ME 537 Robotics Student Guide

The course uses one cumulative package throughout the semester. You begin with
all required function and class-method signatures. Each homework completes a
new labeled portion of that same package, so later assignments build directly
on your earlier work.

## Installation

Python 3.10 or newer is required. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

On macOS or Linux:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

The editable installation means changes under `src/byu_robomanip/` are used
immediately; you do not need to reinstall after every edit.

Confirm the import path:

```powershell
python -c "import byu_robomanip; print(byu_robomanip.__file__)"
```

The printed path should point into this repository.

## Import style

Use the installed package from homework scripts and notebooks:

```python
from byu_robomanip import transforms as tr
from byu_robomanip import kinematics as kin
from byu_robomanip import dynamics as dyn
from byu_robomanip.symbolic import dynamics as symbolic_dyn
from byu_robomanip.visualization import ArmPlayer, VizScene
```

Do not copy `transforms.py`, `kinematics.py`, `dynamics.py`, or
`visualization.py` into each homework directory. Do not use flat imports such
as `import kinematics`.

The assigned package sources are:

- `src/byu_robomanip/transforms.py`
- `src/byu_robomanip/kinematics.py`
- `src/byu_robomanip/dynamics.py`
- `src/byu_robomanip/symbolic/dynamics.py`

## Cumulative homework workflow

For each assignment:

1. Read the homework description and identify its package boundary.
2. Re-derive the relevant equation and write down the frame of every vector.
3. Open the labeled method under `src/byu_robomanip/`.
4. Implement a small coherent portion.
5. Inspect intermediate values, shapes, and frames with a debugger or prints.
6. Run the homework runner or notebook.
7. Run only the limited public checks for material you have reached.
8. Reconcile failures using the mathematics before changing code again.
9. Complete the course self-grading and AI-use reflection.

A later method may raise `NotImplementedError` until its homework. That does
not mean the installation is broken.

## Homework progression

| Homework | Main cumulative work | Student-facing support |
| --- | --- | --- |
| HW01 | Environment and visualization orientation | `homework/hw01/` |
| HW02 | 2D/3D rotations and rotation inverse | `homework/hw02/hw02_test_transforms.ipynb` |
| HW03 | Homogeneous transforms and inverse | `homework/hw03/hw03_test_homogeneous_transform.ipynb` |
| HW04 | Rotation representations, DH transforms, and forward kinematics | `homework/hw04/hw04_test_FK_notebook.py` |
| HW05 | Geometric Jacobian | `homework/hw05/hw05_test_jacobian.py` |
| HW06 | Position inverse kinematics | `examples/hw06/IK_intro_example.py` |
| HW07 | Singularities and Jacobian shifting | `homework/hw07/hw07_dh.py` |
| HW08 | Recursive Newton-Euler dynamics and numerical terms | `homework/hw08/params_hw08.py` |
| HW09 | Simulation and control | `homework/hw09/hw09_sim_and_control.py` |
| HW10 | Symbolic Euler-Lagrange dynamics | `homework/hw10/hw10_main.py` |

## Core conventions

### DH parameters and joints

DH rows are ordered:

```text
[theta, d, a, alpha]
```

This is the operation order used by the package. It may differ from the table
order used in another reference. Joint types are `"r"` and `"p"` and are
passed with `jt`:

```python
arm = kin.SerialArm(dh, jt=["r", "r", "p"])
```

### Coordinate frames

Before implementing an equation, annotate each rotation, position, velocity,
acceleration, force, and moment with the frame in which it is expressed.
Many numerically plausible robotics errors are actually frame errors.

For HW08, each returned wrench column is expressed in its corresponding link
frame. Gravity passed to numerical RNE is physical acceleration expressed in
frame 0, such as `[0, -9.81, 0]`.

### Numerical and symbolic dynamics

- Numerical `get_M(q)` returns the mass matrix.
- Numerical `get_C(q, qd)` returns the vector `C(q, qd) @ qd`.
- Numerical `get_G(q, g)` accepts physical gravity in frame 0.
- Symbolic HW10 `C(q, qd)` returns the matrix.
- Symbolic potential energy uses the corresponding positive gravity vector.

### HW09 state

The simulation state is:

```text
x = [qd, q]
```

Its derivative must have the matching order:

```text
xdot = [qdd, qd]
```

## Limited public checks

The public checks are intentionally incomplete. They check selected
conventions, shapes, and structural properties without acting as a general
answer oracle.

Run all currently available checks:

```powershell
python -m pytest tests/public
```

If you have not reached a later homework, run a specific file instead. A
passing public check is useful evidence, not proof that the implementation is
correct for arbitrary robots and configurations.

Avoid repeated guessing until a check passes. First predict what should happen
from the equations, then use the check to test that prediction.

## Debugging checklist

### Transforms and kinematics

- Is the angle in radians?
- Does the rotation satisfy `R.T @ R = I` and `det(R) = 1`?
- Is the DH row in `[theta, d, a, alpha]` order?
- Is the requested transform direction correct?
- Is each Jacobian column expressed in the requested frame?
- Does the Jacobian have shape `(6, n)`?

### Inverse kinematics

- Is the target a three-element position?
- Does the initial configuration avoid an obvious singularity?
- Is the positional Jacobian the top three rows?
- Does the error norm decrease?
- Are the gain and damping terms dimensionally sensible?

### Numerical dynamics

- Do `q`, `qd`, and `qdd` each contain one value per joint?
- Are COM vectors and inertia tensors expressed in link frames?
- Is every intermediate acceleration or wrench labeled with its frame?
- Is physical gravity rotated from frame 0 into the current link frame?
- Does `M(q)` have the expected shape and approximate symmetry?
- For HW08, run `python -m homework.hw08.check_rne` after implementing `rne`.
  It checks the published joint-force, mass-matrix, and zero-configuration
  checkpoints. To check COM accelerations, pass the array collected during
  your outward recursion to `check_rne_checkpoint` as described in
  `homework/hw08/README.md`.

### Simulation and control

- Is the state ordered `[qd, q]` everywhere?
- Does `xdot` return `[qdd, qd]`?
- Are damping, gravity, and commanded torque signs consistent?
- Does the controller use the intended model and desired trajectory?
- Are array shapes consistent before matrix multiplication?

## Visualization

Start with:

- [Visualization quick reference](docs/visualization/VISUALIZATION_QUICK_REFERENCE.md)
- [Full visualization guide](docs/visualization/VISUALIZATION_GUIDE.md)
- [Visualization examples](examples/visualization/)

Graphical checks are valuable for frame and motion intuition, but a plausible
picture does not replace a numerical or mathematical check.

## Using AI as a tutor

AI tools may help explain concepts, interpret tracebacks, review your attempt,
suggest small tests, or show a short syntax example. They SHOULD NOT write
complete assigned methods, fill in student-facing `TODO`s, or copy instructor
solutions.

When asking for help, include:

- The homework and method.
- The equation you intend to implement.
- The frame and expected shape of each important value.
- Your current attempt.
- The first failing line or unexpected intermediate value.

Use the coaching expectations in [AI_TUTORING_GUIDE.md](AI_TUTORING_GUIDE.md)
and follow the course requirement to disclose how AI was used.

## Getting help

If you are stuck, bring a focused question to a classmate, TA, office hours,
or the course discussion system. Include your derivation and the smallest
example that fails. Debugging from a clear prediction is faster and more
educational than changing several equations at once.
