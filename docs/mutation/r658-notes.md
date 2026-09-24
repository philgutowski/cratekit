# R-658, mutation notes

Three tables, twenty rows, one pass. The author's own table, so every zero reads
as "the author could not kill it".

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r658-a`, the conftest guards | 7 | 7 | 0 |
| `r658-b`, the eleven sites | 12 | 10 | 2 |
| `r658-c`, the composite for S4 | 1 | 1 | 0 |

**Table A.** C1 to C6 each put one isolation fixture's patches back on the
shared `monkeypatch`, which is the tree before R-658. Every one is killed by
`tests/test_isolation_survives_undo.py`, C1 twice. C7 is C1's composite: the
state roots fixture stops setting HOME, and the platformdirs config write test
refuses before it writes.

**Table B.** Each row removes or weakens the scoped patch at one of the eleven
sites, and each killer is that site's own test and nothing else, so each site
still drives the failure it was written for.

**S4 is paired with S4c, run as table C** because `pairs_with` resolves within a
batch only. S4 removes the evicted stat from
`test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway` and
kills nothing, promoted to 10133. That is expected. The test pins that
production no longer branches on eviction, so without the patch the file reads
the same way. S4c puts the old branch back, a dataless file answered as
unreadable in `_look_at`, and that one test kills it. The scoped patch still
reaches the branch it was written to catch.

**S11, maintainer facing, zero promoted to 10133.** It drops the scoped `undo()`
before `time.tzset()` in the zone test, so the worker keeps New York's zone
state after the test. No other test in the suite depends on the process zone,
so nothing dies. The `undo()` is kept because it is what makes the `tzset()`
restore the zone the process had.
