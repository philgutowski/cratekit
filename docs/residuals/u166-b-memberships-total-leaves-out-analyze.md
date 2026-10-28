---
title: A native landing's memberships total leaves out the INBOX / Analyze memberships it wrote
found: at the first review of #347, U166, 2026-10-28.
issue: no
---

**The mechanism.** `NativeLanded.memberships_added`, which the landing's
envelope reports as `totals.memberships`, counts the batch and account
playlist memberships. The Analyze memberships are counted on the session
record under the intake tree and named in the `rows-await-analysis` warning,
but not in that total, and nothing reads them back after the commit the way
the set playlist's are.

**Measured cost.** A landing of five reads `memberships: 5` in its envelope
and `created: 10` under the intake tree on its record. Nobody is told
anything false about the tracks, since the total has always meant the
batch's, and every membership is on the record a restore reads.

**Closes when:** the envelope carries the Analyze count beside the batch's,
and the landing reads the Analyze memberships back after the commit. Ledger
only.
