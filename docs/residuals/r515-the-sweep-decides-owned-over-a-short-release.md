---
title: The label sweep decides a release owned over the rows the provider served
found: at the review of #284, R-515, 2026-10-10.
issue: no
---

**The mechanism.** `sweep.py` `OwnedReleases._holds` decides owned over the
served rows and drops the shortfall `release_tracks` now carries, so a release
whose unowned tracks the provider withholds reads as owned and is never
offered, with nothing said.

**Measured cost.** Not driven. A short release whose missing tracks are the
unowned ones is never offered by the sweep.

**Closes when:** the sweep keeps the shortfall and either offers such a
release or says it was left. Ledger only; the watcher chose to leave this
surface on #264.
