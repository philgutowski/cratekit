---
title: crate sync land's stop names Reload Tags and the landed batch, not INBOX / Analyze
found: at the plan of #333, U152, 2026-10-28.
issue: no
---

**The mechanism.** The brief's addendum says the stop names `INBOX / Analyze` (#347, U166) and that Reload Tags is not needed once #344 (U163) writes the row fields. Neither unit is built, so `REKORDBOX_STEPS` in `src/cratekit/cli/sync_land.py` names Reload Tags before Analyze Tracks, on Phillip's standard settings, over the batch playlist the applied landing names.

**Measured cost.** None today: the steps are right for the landing as it is built. They go stale the day U163 or U166 lands.

**Closes when:** U166 lands and the stop names `INBOX / Analyze`, and U163 lands and the Reload Tags step is dropped. Ledger only.
