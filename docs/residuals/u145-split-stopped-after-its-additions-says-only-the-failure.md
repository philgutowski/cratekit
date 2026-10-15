---
title: A month split stopped between its two commits reports only the failure, not that its additions landed
found: at the build of #324, U145, 2026-10-15.
issue: no
---

**The mechanism.** `split.apply` commits the month memberships, records that
commit on the session, then retires the quarters in a second commit. A failure
in the second half propagates as it was raised. The genre Favorites refresh
wraps the same window in `RefreshInterrupted` so its caller can say the
additions landed; the split does not.

**Measured cost.** Driven by
`test_a_run_stopped_after_its_additions_replans_to_the_same_digest_and_finishes`:
the person is shown the failure alone, while the months already hold their
members and the session record says so. Running the verb again plans the same
digest, adds nothing and retires the quarters, so nothing is lost and nothing
is left half done once it is run again.

**Closes when:** the second half's failure is reported with what the first
commit wrote, the refresh's way. Ledger only.
