---
title: A branch that renames or deletes a test on the battery's on disk list cannot be measured in memory
found: at the review of #702, U273, 2026-11-13.
issue: no
---

**The mechanism.** `ON_DISK` in `scripts/cloud_battery.py` names whole node
ids, and after a run in memory both the battery and the driver rerun every
listed id the run's paths cover (`runs_node` in `scripts/mutate.py` reads a
full run as covering all). A branch that renames or deletes the inode bound
test asks pytest for an id that no longer exists: the battery refuses the
run (pinned by the `not-collected` case), and the driver raises
`MeasurementFailure` on pytest's exit 4 (not driven).

**Measured cost.** Not driven. Only a memory run meets it, and the default
place is disk; a branch that renames the test edits `ON_DISK` with it, which
the battery's refusal names.

**Closes when:** the rerun takes only the listed ids the memory run itself
collected, or the refusal names `ON_DISK` as the line to edit.
