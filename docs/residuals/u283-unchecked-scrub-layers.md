---
title: The Discogs token check's only scrub of a transport note is the asker's shared one, and no test reverts it alone for the check
found: at the review of #799, U283, 2026-11-13.
issue: no
---

**The mechanism.** `DiscogsAsker.identity` returns the note `_read` built
through `_said`, which replaces the token with `[token]`. Round one found two
scrub layers, each killing nothing alone; the fix round dropped the redundant
one in `identity`, leaving `_said` as the one layer the check relies on.
`tests/test_setup_discogs.py` now asserts a transport note carrying the token
comes back scrubbed, which reverting `_said`'s scrub fails.

**Measured cost.** No leak was reachable: the round one reviewer drove the
check through real `requests` against a local server answering 200, 401 and
500, and through a transport failure whose message carried the token, and
found the token in no output, log record, envelope or file.

**Closes when:** the mutation table's row on `_said`'s scrub is killed by the
check's own test, measured in `docs/mutation/u283.md`. Ledger only.
