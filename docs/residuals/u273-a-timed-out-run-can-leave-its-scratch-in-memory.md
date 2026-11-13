---
title: A run that times out or is killed can leave its temporary files in /dev/shm, and the timeout reads as a cleanup error
found: at the review of #702, U273, 2026-11-13.
issue: no
---

**The mechanism.** U273 moved a run's `TMPDIR` inside the workspace that
`tempfile.TemporaryDirectory` removes, in `scripts/mutate.py` `run_pytest`
and `scripts/cloud_battery.py` `run_directory`. When `subprocess.run` times
out it kills the controller, but xdist workers still writing race the
removal, so the rmtree can fail with `Directory not empty` and leave the
directory behind; that `OSError` then replaces the `TimeoutExpired`, so the
row's note names the wrong reason. A SIGTERM to the battery leaves its
directory too, since nothing turns the signal into a clean exit. In memory
the files left hold RAM until removed by hand.

**Measured cost.** Driven by the review on a synthetic suite under `-n 2`
with `run_pytest(timeout=2)`: the branch leaked 2 of 7 runs in memory and 3
of 6 on disk, the base 0 of 6 (its `TMPDIR` was outside the workspace). A real
row past the driver's 3600 s timeout was not driven. Today the default place
is disk, so only a session that names memory meets it in RAM.

**Closes when:** the child runs in its own session and the whole group is
killed on a timeout, the cleanup is retried and never replaces the timeout,
and the battery turns SIGTERM into a clean exit, each with a test that times
a writing suite out and finds nothing left in the place.
