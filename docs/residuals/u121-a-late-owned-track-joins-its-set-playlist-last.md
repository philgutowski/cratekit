---
title: A track that becomes owned after the set's playlist was written joins it last, not in set order
found: by the review of U121, 2026-10-09, reading the read back.
issue: no
---

**The mechanism.** The playlist is found by its name under the folder, so a
second write on the same day adds what the playlist lacked, and
`add_memberships` appends: rekordbox numbers an added track after every
track the playlist holds. A track that was a question at the first write
and owned at the second therefore sits last. The read back holds every asked
id live and holds the order only for a playlist this commit filled, so the
second write is reported as what it was, one track added, and not refused.

**Measured cost.** Driven on the disposable library:
`test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`, three
tracks, the middle one owned between two writes, read back One, Two, Three
for a set that played One, Three, Two. Order only; nothing is lost.

**Closes when:** the write re-sorts the memberships to set order, a
`TrackNo` rewrite the guarded writer does not make today. Ledger only.
