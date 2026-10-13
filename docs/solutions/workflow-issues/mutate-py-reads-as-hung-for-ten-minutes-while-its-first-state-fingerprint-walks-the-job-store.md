---
title: "mutate.py reads as hung for ten minutes while its first state fingerprint walks the job store"
date: 2026-10-13
category: workflow-issues
module: "scripts/mutate.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: incorrect_assumption
resolution_type: workflow_change
applies_when:
  - "A session starts scripts/mutate.py on the Mac that holds the real installation state and sees no pytest child and no output"
tags:
  - mutation
  - state-guard
  - timing
---

**What it looks like.** On 2026-10-13, U142's table was started on the Mac
the board runs on. For ten minutes the driver ran no pytest child, wrote
nothing to its log and left no sidecar. A stack sample showed it busy in
Python with `_sha2` loaded, which reads as a hang or a loop.

**What it was.** The state guard (R-343) fingerprints the real installation
state directory, `~/Library/Application Support/cratekit` on macOS, before
the first child and again after every child. It walks every entry and
hashes the content of every file at or under 64 KB. That directory held
429,305 entries and 921 MB, and 912 MB of it was `jobs/`. The first walk,
with the file cache cold, took about ten minutes. Every later walk took
about 35 seconds because the cache was warm. The 23 row table then ran 31
pytest invocations in about 20 more minutes, all clean.

**What to do.** Do not stop the driver because it is silent at the start.
Check for a pytest child (`pgrep -f 'pytest -p mutate_'`). If none has
appeared, the guard is still walking. Budget ten minutes before the first
child plus about a minute a run after that. The driver has to run as a
tracked background job anyway (METHOD's driver rules), and the cold walk
alone is enough to pass a foreground call's ceiling. Count the store first
when the wait matters: `find ~/Library/Application\ Support/cratekit | wc -l`.
The walk grows with every job the product keeps, so this gets slower over
time, not faster.

**Not changed.** The guard watches the real config and state because a probe
outside `tests/` once overwrote the live config. Pointing the driver at a
scratch state directory would make it fast, and it would also make the guard
watch nothing. That trade is the person's to make, not a session's.
