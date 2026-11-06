---
title: label heard adds run it again after a removal's read back refusal that says to check the playlist by hand first
found: at round one's review of #558, R-1308, 2026-11-06.
issue: no
---

**The mechanism.** prune's refusal wrapper drops its "run again" step when
the account's problem is `read-back-differs`; `label heard`'s
`_failed_part_way` appends "run crate label heard again" after it whatever
the problem. Driven at round one's review on the adapter's read back refusal.

**Measured cost.** A heard user is told in one answer to check by hand and to
run again; no data is lost, since a run again's removal is planned from a
fresh reading (see the residual beside this one on a lagging read's tag).

**Closes when:** heard's wrapper keeps the account's steps alone on a
`read-back-differs`, as prune's does. Ledger only, a wording fix.
