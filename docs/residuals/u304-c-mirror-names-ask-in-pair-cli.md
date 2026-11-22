---
title: The outbound mirror's tie comment points at sync/pair_cli._ask, which lives in sync/pair_plan.py since U304
found: at the review of #861, U304, round one, 2026-11-22.
issue: no
---

**The mechanism.** `src/cratekit/modules/outbound/mirror.py` line 275 says the pairs break a tie the same way since U208 (``sync/pair_cli._ask``). U304 moved `_ask` to `sync/pair_plan.py`. The file is #866's (U309), so U304 left it.

**Measured cost.** A maintainer following the pointer finds no `_ask` in `pair_cli.py`. No person using the tool is affected.

**Closes when:** the comment names `sync/pair_plan._ask`, in #866 or the next docs sweep. Ledger only.
