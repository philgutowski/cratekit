---
title: No test passes empty analysis roots to the four intake writes that share watched_roots
found: at review round one of #978, U329, 2026-11-23.
issue: no
---

**The mechanism.** `tests/test_inbox_rotate.py`'s empty roots test calls
`rotate.watched_roots([])` alone, though it is named for every write that
shares it. The review replaced the call with a plain list in turn at
`intake/analyzed.py`, `intake/refill.py`, `intake/shelve.py` and
`intake/rotate.py`'s apply, and five intake suites stayed green each time.
Before U329 as after it; the full suite was not run for these mutants.

**Measured cost.** None driven: every caller passes the roots the
configuration names, and no verb produces an empty list for these writes
that the review found. A write whose watch covers nothing would report a
session clean whatever happened to the library's grids.

**Closes when:** each of the four writes is driven with empty roots and
refuses before the gate. Ledger only.
