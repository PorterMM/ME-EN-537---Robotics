# HW08

- Shared support: `params_hw08.py`
- Published RNE intermediate checker: `check_rne.py`
- Package boundary: numerical `rne`, `get_M`, `get_C`, and `get_G`

HW10 imports this parameter module explicitly so there is only one maintained
copy of the common three-link robot definition.

For the single three-link configuration in Problem 2(a), check the published
intermediate arrays with:

```python
from homework.hw08.check_rne import check_rne_checkpoint

result = check_rne_checkpoint(
    com_accelerations=ac,
    joint_forces=wrenches[:3, :],
)
```

After implementing `rne`, the easiest check is to run the helper as a module
from the repository root:

```powershell
python -m homework.hw08.check_rne
```

That command runs your current `SerialArmDyn` on the published configuration
and checks the returned joint-force rows, the Problem 2(b) mass matrix, and
the link origins at the zero configuration. It first prints all four published
reference arrays in a copy-friendly format. If a check fails, it also prints
the expected and actual arrays, frame reminders, and suggestions for which
part of the recursion or kinematics to inspect. To check COM accelerations as
well, collect your outward-recursion COM acceleration array and pass it to
`check_rne_checkpoint` as shown above.

Both arrays are 3-by-3. Column `i` must be expressed in link frame `i`.
`com_accelerations` is the COM acceleration collected during the outward
recursion; `wrenches[:3, :]` is available from the normal `rne` return. The
checker reports a maximum absolute residual against the rounded published
values. It is valid only for the stated configuration and is not evidence that
RNE is correct for arbitrary inputs.
