---
title: The reports guard's qualified mutations still name session._recorded, which U953 inlined into assert_gates
found: at the review of #953, U953, 2026-11-23.
issue: no
---

**The mechanism.** `tests/modules/test_reports.py` lists `session._recorded`
among its `QUALIFIED_MUTATIONS`, the calls a report must never make. U953
inlined that private function into `session.assert_gates`, which the list
also names, so the entry names a function that no longer exists. The guard
never checks that a listed name exists, so it passes, and a call of
`assert_gates` is still caught.

**Measured cost.** None today: found by a syntax tree scan for strings naming
deleted names, the only hit in src, tests and scripts. A later reader may
trust the entry as a live call.

**Closes when:** the suite card that holds `tests/modules/test_reports.py`
drops the entry, and the guard learns to fail on a listed name that does not
resolve. Ledger only.
