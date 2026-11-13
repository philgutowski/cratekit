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

**Measured cost.** Driven by round two of the review: with `ON_DISK` naming a
missing id, alone or beside a real one, `failing_ids("memory")` refused with
"pytest printed no summary line, so the run cannot be read", only after the
whole memory run, with pytest's own "ERROR: not found" naming the id above
it; nothing names `ON_DISK` as the line to edit. The driver's `run_pytest`
raised `MeasurementFailure` on pytest's exit 4. Only a memory run meets it,
and the default place is disk.

**Closes when:** the rerun takes only the listed ids the memory run itself
collected, or the refusal names `ON_DISK` as the line to edit.
