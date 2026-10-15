---
title: board.py audit reads every issue twice, once in reconcile and once after
found: at the review of #327, U148, 2026-10-15.
issue: no
---

**The mechanism.** `cmd_audit` calls `reconcile`, which builds the graph from
`load_issues()`, then builds it again from a second `load_issues()` for the
unit counts and the contradictions. Since U148 each read is a full read of
every issue body plus a GraphQL count, so an audit makes two of each, and the
two can disagree if an issue changes between them.

**Measured cost.** Not driven as a cost to anyone. On 2026-10-15 a whole audit
on the real board, 317 issues and 317 items, took seconds. Passing the graph
into `reconcile` was tried at the review and reverted, because two existing
tests, in `tests/test_pending_units.py` and
`tests/test_restart_and_residual_files.py`, replace `reconcile` with a double
of the three argument signature, and the brief kept those tests unchanged.

**Closes when:** `reconcile` takes the graph `cmd_audit` already built, with
those two doubles widened to accept it. Ledger only, maintainer facing.
