---
title: The stealing suite's real runs pass under xdist's default distribution most of the time, so only the two pins catch work stealing being dropped
found: at the review of #680, U251, 2026-11-12.
issue: no
---

**The mechanism.** `tests/_stealing_suite.py` writes a suite in which, under
`--dist worksteal`, a queued test must move to the idle worker, and the
moved test's failure is what the driver and the battery are each asked to
report. Under `--dist load` a queued test usually moves too, because the
default distribution hands the holding worker only a short first chunk. So
the three tests that run the suite (`tests/test_suite_distribution.py`,
`tests/test_mutation_driver.py` and `tests/test_cloud_battery.py`) pass under
either distribution on most runs. The review drove it: under `--dist load`
the moved assertion failed in 4 of 22 runs, under `--dist loadgroup` in 5 of
12, and the holding test never timed out.

**Measured cost.** None while the two pins stand: dropping `--dist worksteal`
from `pyproject.toml`, or the driver stripping it, fails
`test_the_suite_runs_on_every_core_and_steals_queued_work` or
`test_the_mutation_driver_passes_the_distribution_on` every time (the
mutation table's W1 to W3). Without them it would read as an intermittent
failure rather than a red one.

**Closes when:** the suite holds a property only work stealing produces on
every run, for instance a holding worker given its whole half up front whose
tail is read back from xdist's own scheduling log, or the pins are accepted
as the guard and this is closed as such. Ledger only.
