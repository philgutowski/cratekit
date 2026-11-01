# U167 mutation notes

The table is the author's, 25 rows over the guards `crate analyze check` added,
measured once by `scripts/mutate.py` against the base's 167 Linux failures. 23
rows killed and two were zeros, each driven below. A zero is "the author could
not kill it", as METHOD says, and no independent table was run.

**M2_file_length, zero, kept as measured.** The check that an analysis file's
stated length equals its size is layered under the tag fits check (M3, killed
2): every truncation reaches a tag that no longer fits before the walk ends,
and trailing bytes beyond the stated length either form a tag that must fit or
fail it. The composite is M3 itself, which with M2 present is the only guard a
cut off file meets. Filed in the write watch residual as a guard that kills
nothing alone.

**M18_unknown_landing, zero, then pinned.** Removing the refusal of a named
landing nothing recorded fell through to the second refusal, a landing whose
playlists hold no live row, under the same slug, so the exit and the reason
held and only the sentence changed. The test now asserts the sentence ("no
closed landing is recorded"), and the row was driven again by hand after the
table: 2 failed, 55 passed, source restored and verified against HEAD. The
table was not measured a second time, one pass per unit per session.

**M3 needed a bounded test before it could be measured.** The first batch hung
on M3: a tag of length zero walks in place for ever without the guard, and the
driver's per run timeout files a hang as an error, not a death. The damaged
file test now reads on a thread with a ten second bound, so a walk that never
ends fails it, and M3 kills 2.
