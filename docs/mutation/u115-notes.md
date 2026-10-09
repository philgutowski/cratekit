# u115, the author's notes

Twenty four rows against the file id unit, issue #272, measured in two
passes: twenty one on 2026-10-09 at `65decdd` (16:47Z), and the three rows
whose text the review's fix round had changed, retyped and measured on
`--resume` at `0081c50` (18:01Z). Every row killed, the null control zero on
both passes, baseline green over 12,804 collected, the installation state
unchanged across every child. The table is `u115.md`.

**No zero row.** Twenty two rows are user facing and two maintainer facing
(F4, the binding's id limit as a coefficient; F15, the file id policy
registered on a run that renumbers nothing; F17 is maintainer too, the bound
reported as zero). The two R-923 samples kept, F10 and F20, killed 14 and 1.

**What the resume cost, recorded so the next session does not pay it
twice.** The first `--resume` was launched from a shell whose sandbox was
failing and its baseline read 517 failures across unrelated suites; the
second died inside xdist's worker spawn with `BlockingIOError: [Errno 35]`.
The cause was not the tree: Pioneer's `FwUpdateManagerd`, running four days,
had 2,357 unreaped zombie children and the per user process table (2,666)
was full, so every fork failed. Terminating that daemon dropped the table to
488 processes. The third resume's null control killed one test and the
fourth's baseline failed one, `test_export_set.py::
test_the_same_exact_track_served_again_on_the_next_page_is_one`, which
passes alone three times; both ran while another session's intake job held
the fifteen minute load average above 14. The fifth resume measured the three
rows clean. A red baseline or a killing null control on a loaded machine is
starvation first, as `docs/solutions/` already says of the Google Drive
mirror.

**F6, killed 13, the largest.** Every nonzero id judged above the bound
renumbers the stale row and the whole row, and the counts, the digest and
the two acts all move. **F5, killed 2**: an id equal to the bound is the
pure test's boundary case and the whole row at 4242 is under it, so the
plan test moved only through the parametrized judge. **F8, killed 1**: the
matching inode row renumbered to itself refuses in `_fill` on `SKIP_SAME`,
which the one test naming that row catches.

**F3, killed 3 on 3,524.** The file id policy as fill if empty leaves the
random id in place, refused in `_fill`, and the full writer subset was run
because `rb_writer` is imported by 41 test files.
