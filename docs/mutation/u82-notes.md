# U82 mutation tables, read

Four tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/127`. Every zero row in this record means the
author could not kill it, not that nobody could. The unit writes to a streaming
account, so it took the full 25 rows.

**`u82-a.md`**, 8 rows over the engine at `06cc92f`: four over
`sync/marks.py`'s one stat file check and four over `sync/playlists.py`'s new
`only` and `marking_sweep`. Subset `tests/test_sync_mark.py` and
`tests/test_sync_all.py`, named explicitly, 100 collected. Null control 0 of
8419, no collect drift, every restore verified against `git show HEAD`. All 8
killed, between 1 and 17 deaths.

**`u82-b.md`**, 8 rows over `sync/mark_cli.py`'s decisions about which
playlists a landed file finishes, subset `tests/test_sync_mark.py`, 29
collected, null control 0 of 8419. 7 killed, 1 zero promoted to the full suite:
`B2_paths_compared_resolved`, 0 of 8419. It is user facing, since the landed
and owned counts are on the gate screen, and nothing drove a library reached
through a link.

**`u82-c.md`**, 9 rows over the settle step, the gate, the digest and the
failure report, same subset, null control 0 of 8419. All 9 killed.

**`u82-d.md`**, the one zero measured again at `f9f1f1f`, after
`test_a_library_reached_through_a_link_still_reads_its_files_as_landed` was
written for it. Null control 0 of 8420. Killed, 1 death.

25 distinct mutations, which is the cap, and one re-measure on top of it, so 26
runs. The re-measure is the same mutation as B2 and is what turns that zero
into a death, and it is said here as one over rather than folded in.

Three guards were given a test BEFORE the table was run, at `06cc92f`, because
reading the verb showed each would kill nothing: the not listed reason, the
failed job reason, and the planned renames inside the digest. Rows B5, B6 and
C7 then measured them as killed. A table run first would have reported three
more zeros, and the record says so because the 24 of 25 on the first pass is
flattered by it.

**Dropped, and why each ranked below the cap.** Nine, logged in the rows files:
the engine's recheck skip and the already prefixed skip in `pending_marks`,
both measured in `docs/mutation/r358.md`; the refusal over an intake file
naming no local track and the catch over a Location on another host, neither of
which can cause a wrong rename; the early return that spares the library walk,
which costs minutes and no rename; the no pass branch, whose input comparison
is row B3; the report of a planned item the recheck skipped, which is a test's
own assertion; and the two static registry declarations, asserted literally.
