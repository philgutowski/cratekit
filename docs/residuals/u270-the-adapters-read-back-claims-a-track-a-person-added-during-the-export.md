---
title: The adapter's read back records a track a person added by hand during an export as the export's own
found: at the review of #699, U270, 2026-11-13.
issue: no
---

**The mechanism.** `TidalAccount.add_tracks` reads the playlist back when the
provider's answer leaves out a track it was asked for, and returns every asked
track the playlist then holds. The membership it decides what to send from is
read once per playlist per process. A track a person adds by hand while an
export runs, if a later batch of the same run sends it, is skipped by the
provider as a duplicate, found by the read back, and recorded by
`export.apply` as added, row and all.

**Measured cost.** Driven by round two of the review through the driver, 150
tracks: a person's hand add of a batch two track during batch one is recorded
as written, and `prune.plan_export` with its row gone takes it off. `main`
does the same a track at a time, so U270 did not cause it.

**Closes when:** a track the read back holds and the answer did not name is
reported as already there rather than recorded, or the membership is read
again before each batch. Ledger only by origin; its cost is a prune taking off
a person's track, so it is worth a card if it is ever met live.
