# Homework Material Layout

The cumulative implementations live in `src/byu_robomanip/`. Homework
directories contain assignment runners, limited checks, and support data.

See `../STUDENT_GUIDE.md` for the cumulative workflow and debugging guidance.

Run scripts and notebooks from the repository root after installing the
package with `python -m pip install -e .`.

| Homework | Student-release material | Package boundary |
| --- | --- | --- |
| HW01 | `hw01.py`, `hw01.ipynb` | Environment and visualization setup |
| HW02 | `hw02_test_transforms.ipynb` | HW02 transformation methods |
| HW03 | `hw03_test_homogeneous_transform.ipynb` | `se3` and `inv` |
| HW04 | `hw04_test_FK_notebook.py` | Transform conversions, DH, and FK |
| HW05 | `hw05_test_jacobian.py` | `SerialArm.jacob` |
| HW06 | Examples only | `SerialArm.ik_position` |
| HW07 | `hw07_dh.py`, `data/singular_configurations.mat` | `SerialArm.Z_shift` |
| HW08 | `params_hw08.py` | Numerical dynamics |
| HW09 | `hw09_sim_and_control.py`, `data/desired_accel.mat` | Simulation and control |
| HW10 | `hw10_main.py`; reuses `../hw08/params_hw08.py` | Symbolic Euler-Lagrange generation |