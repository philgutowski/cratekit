---
title: The stale check's unread comparison on a part written pair, and the digest's unread ids, kill no test on a resume
found: at the review of #532, R-1264, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_cli.py` `check` compares the unread set with the
plan's on both of its paths. On the path for a pair this run part wrote
(U210), reverting the comparison kills no test, since no test resumes a write
whose account listing gained or lost an unread track after the account step.

**Measured cost.** None driven: the review's round one reverted it and the
suite stayed green, and drove no part written resume whose unread set moves
(0 candidates driven). A stale such a resume should refuse would be written
instead; reachability unmeasured. The digest's unread ids are now pinned by
`tests/test_sync_pair_unread.py`.

**Closes when:** a resume test in `tests/test_sync_pair_resume.py` stops a
write after the account step, adds an unread track, and continues, refusing
stale. Ledger only: a guard with no driven producer.
