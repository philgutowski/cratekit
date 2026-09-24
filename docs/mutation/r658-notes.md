# R-658, mutation notes

Four tables, twenty two rows, one pass. The author's own table, so every zero
reads as "the author could not kill it".

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r658-a`, the conftest guards | 7 | 7 | 0 |
| `r658-b`, the eleven sites | 12 | 10 | 2 |
| `r658-c`, the composite for S4 | 1 | 1 | 0 |
| `r658-d`, the undo ban | 2 | 2 | 0 |

**Tables A to C were measured before the review round, D after it.** The
review folded the two conftest helpers back into their fixtures and rewrote the
zone test, so A's and S11's `old` text no longer matches the tree. A was not
re-run as a table. The reshaped guard file was run by hand against `main`'s
conftest once more: the four undo tests fail, the two ban tests pass because no
body undo is left anywhere, and the config test fails at its resolution check,
before any write.

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

**S11, maintainer facing, zero promoted to 10133.** It dropped the scoped
`undo()` before `time.tzset()` in the zone test, so the worker kept New York's
zone state after the test, and no other test depends on the process zone. The
review then removed that inner `undo()` altogether: the `try` now sits outside
the context, whose exit restores TZ before the `tzset()` in `finally` runs.

**Table D.** D1 puts a body `monkeypatch.undo()` back into the restore retry
test and the ban names it. D2 loosens the ban to match a method called
`undone`, and `test_the_ban_sees_an_undo` kills it.
