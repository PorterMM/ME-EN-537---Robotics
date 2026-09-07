<<<<<<< HEAD
# ME-EN-537---Robotics
This is a copy of the class repo
=======
# ME 537 Robot Manipulation Homework

This repository contains the cumulative Python package, homework support,
examples, and limited checks used in ME 537.

Python 3.10 or newer is required.

## Start here

1. Read [STUDENT_GUIDE.md](STUDENT_GUIDE.md).
2. Create and activate a Python virtual environment.
3. From the repository root, install with
   `python -m pip install -e ".[dev]"`.
4. Confirm the package imports:

   ```powershell
   python -c "import byu_robomanip; print(byu_robomanip.__file__)"
   ```

5. Run `python homework/hw01/hw01.py` for the visualization setup check.

## Repository map

- `src/byu_robomanip/`: the cumulative package you develop through the semester
- `homework/hwNN/`: homework-specific notebooks, checks, scripts, and data
- `examples/`: demonstrations for Python, kinematics, dynamics, and visualization
- `docs/visualization/`: visualization guides and quick reference
- `tests/public/`: intentionally limited formative checks

## Important conventions

- Install the repository; do not copy the package modules beside each script.
- DH rows use `[theta, d, a, alpha]`.
- Use the constructor keyword `jt` for joint types.
- Numerical RNE receives physical gravity expressed in frame 0.
- HW09 state is `[qd, q]`, and its derivative is `[qdd, qd]`.
- Numerical `get_C(q, qd)` returns `C(q, qd) @ qd`; the symbolic HW10
  callable returns the Coriolis matrix.

The detailed implementation workflow, imports, debugging checklists, and AI
use expectations are in the student guide.
>>>>>>> upstream/main
