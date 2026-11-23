# U307's two user facing zero rows, driven by hand after a test was written for them

The driver measured `docs/mutation/u307-rows.toml` at `c301885a` (`u307.md`):
21 killed, three zero, one collection error. R3 is read as killed: forwarding
a dunder through `native.__getattr__` stops `tests/test_intake_writers_native.py`
from collecting (`NameError` on `native_plan`), so no test of the module runs.
R7 is a maintainer facing guard, the origin the `landing.refuse` partial
carries, which no test reads: one line, by METHOD.

R1 and R2 are the failure path `native.apply_rows` takes when a step fails
after the commit is on disk: the session record names what the commit wrote,
then the failure is raised. No test made a failure happen there, so both
read zero over the full suite (22,562 collected). The test
`tests/test_intake_land_native.py::test_a_failure_after_the_commit_landed_is_recorded_and_still_refuses`
was written for them: it makes `rb_writer.commit_guarded` commit and then
raise, drives the landing through its gate, and asserts the verb refuses and
the one session record names the landed rows.

Each row applied by hand to the tree at the commit that adds the test, the
file restored after:

| row | mutation | the test |
|---|---|---|
| R1_landed_failure_swallowed | the failure is recorded and not raised | failed (exit 1) |
| R2_landed_failure_unrecorded | the failure is raised and nothing recorded | failed (exit 1) |

So both guards are held, by that test, and the rows are read as killed by
hand, not by the driver.
