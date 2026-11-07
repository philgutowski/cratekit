---
title: A continue of a refused finish is handed the check's listing by a clause no test pins
found: at the mutation table of #619, R-1420, 2026-11-07.
issue: no
---

**The mechanism.** Since R-1420 the write in `_write_account` in
`sync/pair_cli.py` hands a continue the check's listing as `expect` when an
earlier command began the order and the plan is no finish. The older clause
beside it, `steps.has(STEP_ORDER_REFUSED)`, now matters only for a refused
finish that also adds or removes, which is R-1419's shape: `expect` beside
the plan's reading as `agreed`.

**Measured cost.** None on the branch. Row E1 of `docs/mutation/r1420.md`,
the clause removed, killed none of 17448 on the full suite. A refused
finish so continued is asked `agreed` alone, which R-1419 says is the
reading it should be held to; no data cost either way.

**Closes when:** R-1419 decides whether a refused finish keeps `expect`,
and a test pins the choice. Ledger only.
