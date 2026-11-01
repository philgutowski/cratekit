---
title: Three U150 guards kill no test, each covered by another layer
found: at the reviews of #331, U150, 2026-11-01.
issue: no
---

**The mechanism.** Each was reverted alone by the review with the suite green.
`label_filing.supported_only` keeps only the refs of targets the landing makes
or finds, and `label_filing.write` maps refs through `by_target`, which holds
only landed targets anyway. `mirror.Matcher` drops a known track that is
empty, and `account_mirror.landed_tracks` already strips blanks while the
match skips an empty answer. A guard covered by another guard is a guard
nothing covers, so the record names them.

**Measured cost.** None: the second layer holds in each case.

**Closes when:** each has a test that drives its own layer alone, or the
redundant layer is dropped. Ledger only.
