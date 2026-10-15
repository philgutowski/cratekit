---
title: The favourites backfill opens its gate with nothing to place, where the split and the refresh end NO_OP
found: at sitting 42, 2026-10-15, the live `crate favorites backfill` (U146, #325).
issue: no
---

**The mechanism.** After the live backfill had placed its 58 hearts, a second
run planned 0 hearts and 0 memberships with 235 already placed and still
stopped at `favorites.backfill.approve` for a decision; `favorites split` the
same minute ended `no_op` with no gate, and `favorites refresh` does the same.
A third run after a fresh heart on an owned track did the same again: count
0, gate asked. The verb reaches its gate before it reads its own plan as empty.

**Measured cost.** Three aborted runs in the sitting, and a "second run plans
nothing" proof that needs the plan read rather than the outcome. An unattended
driver that answers gates answers one that should not have been there.

**Closes when:** the backfill ends `no_op` before its gate when it has no
heart to place and no membership to add, as the split does. Ledger only.
