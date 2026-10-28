---
title: A set whose frozen playlist name is Analyze is refused with a remedy that cannot work for a set
found: at the second review of #347, U166, 2026-10-28.
issue: no
---

**The mechanism.** `native.plan_rows` refuses a batch named `Analyze`, the
reserved queue name, telling the person to land with another `--name` or
rename the file. A set landing's INBOX playlist keeps the set's frozen name
whatever `--name` says, so for a set frozen as `Analyze` neither remedy
changes anything and the set cannot land.

**Measured cost.** Driven with the frozen name written straight into the set
job, both `--name` values refused `intake-list-unusable` with the files left
in staging. The producer, renaming the INSPIRATION playlist to Analyze and
exporting the set again, was not driven, so reachability is unmeasured.

**Closes when:** the refusal names the set's own remedy for a set, or a set
of that name takes `Analyze 2` the way an account playlist does. Ledger only.
