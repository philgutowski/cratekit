---
title: Revoking a tombstone after a prune never returns the track to its year playlist
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** `label prune` moves a tombstoned track from `added` to
`pruned` in the outbound ledger, and `folders.plan` never adds a track the
ledger records as pruned. Revoking the tombstone makes the version
acquirable again and leaves the track off its year for good.

**Measured cost.** Driven end to end by the round one review: tombstone,
prune, revoke, full build, and the year stayed without the track. One track to
add by hand on the account.

**Closes when:** a prune records why a track left, and a build adds back a
track whose reason no longer stands. Ledger only.
