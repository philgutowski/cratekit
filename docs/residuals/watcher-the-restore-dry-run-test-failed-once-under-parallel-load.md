---
title: The restore dry run test failed once in a parallel full run and passes alone, with its cause unread
found: at the watcher's gate of the U119 join, 2026-10-10, a single sighting.
issue: no
---

**The mechanism.** `tests/test_restore_cli.py::test_a_dry_run_walks_every_step_and_performs_none_of_them`
failed once in a full parallel run (`pytest` with `-n` workers) on the join of
U119 onto main, on a host that was busy with other work through the night (the
load at the moment of the failure was not read). The same test then passed three times alone on the join and
twice alone on main, and a full rerun of the join was green. U119 changed no
file named for restore, so the failure was not that unit's. The failing
traceback was not kept: the run's output was filtered to the `FAILED` line, so
what the test actually tripped on is unknown. A dry run that walks every step
reads like a test that touches the filesystem, a clock or a subprocess, any of
which a loaded machine can disturb, but that is a guess from the test's name,
not a reading of its body.

**Measured cost.** One red gate that cost a rerun. It was not seen again in the
full runs that followed the same night. Nothing was
written to a live library.

**Closes when:** the test fails a second time and its traceback is read and
filed here with the cause, or the test body is read once and shown independent
of load (no wall clock, no shared path, no subprocess timing). A third outcome,
no second failure over a month of full runs, closes it as not reproduced. Ledger
only.
