# Limited Student-Facing Checks

These checks provide small, intentionally incomplete checkpoints for the
cumulative `byu_robomanip` package. They help students catch convention,
shape, and interface mistakes without acting as a full answer oracle.

The checks intentionally do not include:

- the instructor-only HW05 Jacobian matrices;
- general HW08 dynamics answers; use `homework/hw08/check_rne.py` for the
  published HW08 checkpoints;
- complete controller trajectories or tuned gains;
- the symbolic HW10 reference expressions.

Students should run only the checks for homework they have reached. A later
homework check is expected to fail with a homework-labeled
`NotImplementedError` until that method has been completed.

From the repository root:

```powershell
python -m pytest tests/public
```

Passing these checks is useful evidence, but it does not establish that an
implementation is correct for all inputs. Students are still expected to
reason from the course mathematics and develop their own focused tests.

See `../../STUDENT_GUIDE.md` for the cumulative workflow and debugging
checklists.
