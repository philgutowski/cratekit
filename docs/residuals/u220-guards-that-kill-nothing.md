---
title: Three of U220's guards kill no test
found: at the reviews of #543, U220, 2026-11-05.
issue: no
---

**The mechanism.** `apply_pair`'s `except jobs.Parked: raise` is dead today,
since no park reason is in `ORDER_REFUSALS`, and is there so that adding one
cannot swallow a park. `_stale_tag`'s guard against a cyclic chain is never
met by a test (three cyclic chains were driven by hand and terminate).
`_pause(0)` returns the last pause, not the first; every caller passes one or
more.

**Measured cost.** None reaches a person.

**Closes when:** ledger only.
