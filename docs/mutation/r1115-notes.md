# r1115 mutation notes

21 rows, all reported killed, measured on `d87dfe7` with
`--known-failures .cloud-battery/baseline.txt` and `TMPDIR` under `/var/tmp`.
The author wrote and measured these rows; every count is the author's.

**Two invalid batches first.** The driver's first two runs were refused as
INVALID because the null control killed
`tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
(the first time with the known inode test beside it). The cause was the suite,
not the branch: a vocal loader an earlier test leaves bound in the xdist worker
adds `analyze vocals` to the tail. Reproduced by binding the loader in a test
run first in the same process, and fixed after the table by pinning the model
unable in the go suite's fixtures (`docs/solutions/workflow-issues/a-vocal-loader-bound-by-an-earlier-test-adds-a-rescore-to-the-tail.md`).
The third run's null control killed zero; it reached the tool's background
ceiling after 18 rows, the one mutant it left in `src/cratekit/label/go.py` was
restored from `git show HEAD:` and verified, and `--resume` measured the rest.

**G11 is a zero, not a kill.** Its subset killed nothing, and its promotion to
the full suite killed only the intermittent test above, which the mutation
cannot reach: that test resumes nothing. G11 is an equivalent mutant. In
`_resume` the line it mutates is reached only past `and not nothing`, where a
settled download has a track done, so `read.settled` and `read.landed` agree
there. Read it as "the author could not kill it, by construction".

**What the table does not cover.** The drift warning the carried path drops is
a residual of this card, not a row. `_drive`'s re-raise of a refusal raised
before any drive (a job with no items) is the same `if not read.settled` line
G2 mutates, and was not driven separately.
