---
title: Merging U271 with U273 must keep the battery's place and its on disk rerun in the verdict U271 records
found: at the review of #702, U273, 2026-11-13.
issue: no
---

**The mechanism.** U271 (#700, `cloud/700-mutate-reads-battery-verdict`)
replaces `failing_ids()` with its own `measure_suite` and states that neither
script imports the other; U273 calls `failing_ids(place)` and loads the
battery into the driver by path (`_load_battery` in `scripts/mutate.py`).
A dry merge conflicts loudly in both scripts, the battery's tests, METHOD
and DEVELOPING, and U271's verdict is keyed on a digest of the baseline
file, whose header now names the place, so a verdict and a driver run in
different places cannot silently match. A resolution that takes U271's side
of `measure_suite` would drop the place and the rerun; U273's tests catch it.

**Measured cost.** Not a defect on either branch alone; a merge hazard,
measured by the review with `git merge-tree` in a scratch clone.

**Closes when:** whichever lands second keeps `failing_ids(place)`, builds
the verdict's ids from the ids after the rerun and its counts from the
memory run, and corrects U271's claim that neither script imports the other.
