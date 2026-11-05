---
title: A second copy of a track put on a paired account playlist reads as no change to the check before the write
found: at the review of #500, U210, 2026-11-05.
issue: no
---

**The mechanism.** The check before the write (U209's `check`, and U210's
reading of a part written playlist in `_beyond`, `sync/pair_cli.py`) compares
the account listing after `pair_merge.distinct`, and the listing seam freezes
rows by track identifier, so a track the author put on the playlist a second
time between the gate and the write, or between a stop and its continue, is
the same list to both. The write goes on and the snapshot records the list
distinct.

**Measured cost.** Driven at round one (S12): the continue answered OK and the
account kept the track twice, which is what the author did; nothing was lost
or written over. The cost is that the check does not name the change it saw.

**Closes when:** the listing the check reads keeps each copy, and a count
that differs from the plan's refuses stale as a reorder does. Ledger only: no
data is lost and the author's copy stands.
