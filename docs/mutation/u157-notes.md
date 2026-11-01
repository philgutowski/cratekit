# U157 mutation table, read

One table, the author's and not independent, `u157.md`, measured by
`scripts/mutate.py` on the cloud container at `727a22f`, so a Linux measure of
a macOS suite, green net of the machine's failures. 24 rows over
`analysis/detect.py` (10), `core/drift.py` (3), `core/config.py` (2),
`analysis/cli.py` (2), `intake/native.py` (5) and `intake/land_cli.py` (2).
Null control 0 of 15028, every restore verified against `git show HEAD`.
22 killed, 2 zero.

## The environment it ran in

The container's own venv has no analysis extra, so every test that drives the
drift measurement skips there. The driver ran instead under a side venv with
the `analysis` extra and soundfile, an editable install of this checkout. The
same side environment, built over a worktree of the base `c20fcea`, failed
exactly the 167 ids of `.cloud-battery/baseline.txt` over the whole suite, so
that file is the base's failures under either venv.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base, plus one:
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
the ext4 inode test `docs/solutions` names. It killed the null control in the
first driver run. Run alone on the base in the worktree it failed four times of
four. The id was added in a scratch copy passed to the driver, with that
measurement as its comment, and the measured file was not edited. A second run
was refused when the null control killed
`tests/test_label_sync_go.py::test_two_labels_answered_all_and_one_picked_produce_one_summary_and_one_gate`,
which passed alone three times and in its file; the third run, the one this
table is, did not redden it.

## The first measure, and what its zeros bought

The first valid run, at `a54db3a`, had three zeros: D5, D6 and D7. D6 and D7
were the two checks of the minimum window count, each covered by the other.
`727a22f` made the up front check answer only a track with no whole window and
added a test holding a minute with a pulse in two windows as unknown; D6 kills
3 since, and D7 is now a maintainer guard against a median of nothing.

## The zeros

- **D5, the relative onset gate, user facing.** Composite, driven by a script
  over the suite's own breakdown track: shipped 0.06, D5 alone 0.06, the pulse
  gate removed alone (D3) 17.07, D3 and D5 together 17.07. The pulse gate holds
  the breakdown, and on this fixture the relative gate holds nothing, since the
  breakdown's windows sit above half the median. Filed as a residual with the
  window length, which the review found kills nothing either.
- **D7, maintainer.** Removing the no whole window answer reaches the counted
  check with an empty list, which answers unknown as well.

Every zero row here reads as "the author could not kill it".
