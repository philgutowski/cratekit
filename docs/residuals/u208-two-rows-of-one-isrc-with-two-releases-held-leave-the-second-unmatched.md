---
title: Two rows of one pair carrying one ISRC, with two unlinked releases of it on the account, leave the second row unmatched and the free release named ambiguous
found: at the review of #498, U208, 2026-11-05, round two.
issue: no
---

**The mechanism.** The `held_there` branch in `sync/pair_cli.plan_pair`
takes the lowest of the account's unlinked releases of a row's ISRC, and does
not exclude a release another row of the same playlist already took
(`seen_remote`), so the second row takes the same release and is refused as
"another row of this playlist ... is already the account track it matches".
The free release then finds two library rows by ISRC and is named ambiguous.

**Measured cost.** Driven by the review: row 2 given row 1's ISRC and words,
account [101, 202]: links {101: row 1}, row 2 unmatched, 202 ambiguous, every
sync. The provider path before U208 reached the same outcome for two such
rows (reasoned from `_ask` to `_lowest`, not driven on main).

**Closes when:** `held_there` leaves out releases another row of the plan
took, so the second row takes the free release, with a test. Ledger only: two
rows of one recording in one playlist is a duplicate the person made.
