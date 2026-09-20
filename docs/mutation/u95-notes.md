# U95 mutation notes

What the four tables cannot say for themselves.

**The author's own table.** No independent verifier ran. Every number below reads
as "the author could or could not kill it".

**Four files, one table of 25 rows.** `u95-a` is where the paths come from, 8
rows. `u95-b` is the re-basing rule one field and one clause at a time, 7 rows.
`u95-c` is the new guard with each layer removed alone, 8 rows, plus the fixed
sample of two existing guards, `Held.authorises_path` and the issued terms
comparison in `Held.still_open`. `u95-b1` is NOT a 26th row, it is row B1
measured a second time. The split exists only because this session had to run
the driver in the foreground and one run has to finish inside the ten minute
tool ceiling. The four runs took 3:43, 5:09, 4:14 and 3:02, each with its own
green baseline of 9271 collected, its own null control at zero, and every row
`head_verified` against `git show HEAD:`.

**Result: 24 killed on the first pass, 1 zero, 0 zeros after one fix.**

**The zero, B1, and what it was.** `_rebased_capture` leaving `Capture.root` at
the dead root killed nothing. It was a test gap, not an inert mutation. That
field is what `_captured_by_key` composes captured coupled entries from, so with
it wrong an unchanged watermark is looked for on the dead volume, not found, read
as "did not exist", and the plan invents an effect it cannot undo. The steps were
identical, which is all the moved plan test compared. The test now holds one
watermark that did not move and one tombstone store that was written, strips the
configured root of its state before the bare metal plan, and asserts the
effects, the unconverged trees and the discarded sessions. Re-measured through
the driver in `u95-b1`: 1 kill.

**Why the end to end test strips the configured root.** The built in review
pointed out that a byte identical twin left at the configured root answers any
read that still goes there. Rows A5, A7, B2 and B4 each have exactly one kill,
and in each case that kill depends on the twin being gone. Those four are the
thinnest rows in the table.

**One kill rows, 12 of 25.** A4, A5, A7, A8, B2, B5, B6, C1, C4, C7, C8, S2. A
single test is a single point of failure for the guard it pins.

**Two logged drops, neither run.** B7 and C9, each the second member of a family
whose first member is measured. B9 is logged as an equivalent mutant.

**What the table does not cover.** `bare_metal_session`'s own gates, which this
unit did not change and which now matter more, since the session can write:
R-585. `list_sessions`, which was not rooted: R-586.
