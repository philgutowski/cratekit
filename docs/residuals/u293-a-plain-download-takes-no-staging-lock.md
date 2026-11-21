---
title: A plain acquire download, intake missing and sync bandcamp take no staging lock
found: at the plan of #850, U293, 2026-11-21.
issue: no
---

**The mechanism.** `core/staging_lock.py` is held by `crate sync land`, `crate label sync --go` and `crate sync night`, the passes the brief names. A plain `crate acquire download`, a job a person resumes by hand, and `crate sync bandcamp` (which stages into a batch folder of its own under the staging folder) take no lock, so one of them can still download beside a night pass.

**Measured cost.** Not driven as a collision. R-1499's arrival check still refuses the night pass's landing over anything that arrived during its tail, so nothing lands wrong; the cost is a night pass refused at its landing and the tracks to sort by hand.

**Closes when:** every verb that writes into the staging folder holds the lock, or the record says why one need not.
