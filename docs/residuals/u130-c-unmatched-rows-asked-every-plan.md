---
title: A pair's unmatched rekordbox rows are asked of the provider on every plan
found: at the review of #298, U130, 2026-10-10.
issue: no
---

**The mechanism.** `sync/pair_cli.plan_pair` matches every unlinked rekordbox
row through `match_track`, and a row the account has no track for is never
remembered, so each plan asks again. Both explicit gates mean one sync plans
three times. A row whose ISRC exactly one track on the account playlist carries
is linked without a call, and a row with no ISRC anywhere is not asked.

**Measured cost.** Provider calls per sync of about three times the unmatched
rows that carry an ISRC, paced by the provider gate. Not driven against the
live account.

**Closes when:** the pair records the rows it asked about and the answer, and a
plan asks again only after a set interval or when asked to. Ledger only.
