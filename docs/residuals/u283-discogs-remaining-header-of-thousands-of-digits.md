---
title: A Discogs answer whose remaining count header runs past Python's integer digit limit raises ValueError out of a tag sweep's search
found: at the review of #799, U283, 2026-11-13.
issue: no
---

**The mechanism.** `searchers._remaining` reads `x-discogs-ratelimit-remaining`
with `int(raw)` whenever the text is ASCII digits. A header of more than 4300
digits makes `int` raise `ValueError`, which `DiscogsAsker._read` does not
catch, and a sweep's `search` catches only `CratekitError`. Setup's token
check meets the same raise and, since U283's first fix round, notes it as a
FAIL with nothing stored; the sweep is older than this branch and unchanged.

**Measured cost.** Driven by round two's reviewer:
`discogs_asker(token, fetch=<a 5000 digit header>).ask(...)` raised
`ValueError: Exceeds the limit (4300 digits)`. Not driven through a tag run.
The only producer is a server posing as api.discogs.com; Discogs sends a
count under a hundred.

**Closes when:** `_remaining` returns None for a header longer than a handful
of digits, with a test. Ledger only: no realistic producer.
