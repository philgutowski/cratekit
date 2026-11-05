---
title: The sync pair write's call forecast is held to the account adapter over a fake client and unmeasured live
found: at the build of #500, U210, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_calls.py` counts a write's provider calls from
the account adapter's shape: a playlist opened and read a page at a time,
made with three calls, added to a hundred a request, taken off fifty a
request with a read back each, ordered one move and read back a track. The
check's folder reads are counted at one call each. The gates show the sum,
and a ceiling stop names a `--calls` with a quarter's margin, rounded up to a
hundred.

**Measured cost.** Held exactly to the shipped adapter over a counting fake
client (`tests/test_sync_pair_calls.py`), never to the live provider. A folder
of more than fifty playlists costs the check more than one read, and a
provider that pages differently would move every count.

**Closes when:** the next attended `crate sync pair` records its answer's
`totals.calls_expected` against `totals.calls`. Ledger only.
