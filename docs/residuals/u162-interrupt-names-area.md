---
title: A rehearsal interrupted outside its apply, during the copies, leaves nothing named on the screen
found: at the review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** The fix round turned an interrupt during the rehearsal's plan, apply and read back into the `cancelled` refusal naming the kept area. An interrupt inside `rehearsal.open_area`, while the database or the staged files are being copied, is caught by `open_area`'s own cleanup, which removes both halves and re raises, so nothing is left behind there; but an interrupt between `open_area` returning and the rehearsal's first step, or a kill that no handler sees, leaves the area under the library state directory's `rehearsals` folder with only the run id to find it by.

**Measured cost.** Not driven past the interrupt the round tested. A stale folder on the volume, which the next backup would mirror until removed. Nothing false, nothing lost.

**Closes when:** `crate doctor` lists rehearsal areas older than a day with their run ids, or the next rehearsal removes areas whose run ended. Ledger only.
