---
title: An account mirror plan reads the session log twice, once for the live batches and once for the landing tracks
found: at the review of #331, U150, 2026-11-01.
issue: no
---

**The mechanism.** `rotate.live_batches` reads the session log through
`rotate.landings`, and `account_mirror.landed_tracks` reads it again for each
row's recorded provider track, so one plan parses every record twice.

**Measured cost.** Not measured on the live library. One extra parse of the
session log per organize plan, local and without a provider request.

**Closes when:** one scan feeds both, or the cost is measured and found
negligible. Ledger only.
