# U297 mutation tables, read

Two tables, both the author's and not independent, both measured by
`scripts/mutate.py` on the cloud container, so a Linux measure of a macOS
suite, green net of the machine's failures.

- **`u297.md`**, the card's own: 25 rows, the cap, at `1f52f9a7`, over
  `scripts/mutate.py` (6), `scripts/killset.py` (7),
  `scripts/behaviour_compare.py` (11) and `tests/behaviour/conftest.py` (1).
  Null control 0 of 21,639, every restore verified against `git show
  HEAD`. 25 of 25 killed on their own subsets, none promoted, 31 pytest runs for
  the batch.
- **`u297-replay-tombstone.md`**, the brief's end to end replay: the two live
  recorded kills of `src/cratekit/core/tombstone.py`, both from `r431-a.json`,
  written by `scripts/killset.py rows`, measured under the `replay` pass at
  `1b3010b7`. Both killed, 21 and 17 deaths against the 22 and 17 their table
  recorded, on the row's own subset of six test files. One full baseline, one
  subset baseline, one null control (0 of 21,638) and two rows: five pytest
  runs for the batch. `scripts/killset.py check` of the table against itself
  exits 0, two rows killed before and two after as written.

## The known failures both subtracted

`.cloud-battery/baseline.txt` as measured on the base `34f6c074`, 161 ids,
plus one, in a scratch copy passed to the driver; the measured file was not
edited: `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`.
The battery's `compare` at `1b3010b7` listed it as newly failing. Run alone
in this container on 2026-11-21 it failed 3 times of 3 on the base and 3 of 3
on the branch: it expects a new file's inode above 2,000,000, and this disk
hands out about 600,000 under `/tmp` and the checkout and 1,900,000 under
`/var/tmp`. The baseline run had caught it passing. See
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`.

Because the driver was handed that copy and not the measured file, it could
not read the battery's verdict for its full baseline and measured its own,
which each table says.

One driver run of the card's table was refused at a red baseline on another
test of that file,
`test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`, which
compares a new file's inode with an older file's. Run alone it passed 3 of 3
on the base and 3 of 3 on the branch, so it is intermittent under the
parallel run on a disk that reuses inodes, and by the cloud-unit skill the
driver was run again. It did not redden a baseline a second time.

## The one zero, and the test it bought

A first valid run of the card's table at `62764386` killed 24 of 25, null
control 0 of 21,638, and left one zero, user facing and confirmed on the full
suite:

- **B4, a failed run closed as a capture.** Reverting `run_capture`'s reading
  of the scenario run's exit code killed nothing. Every test of a failed run
  also tripped the reading of what the run left unrecorded, which closes the
  capture on its own, so the exit code was held by nothing alone. A fixture
  that fails as it is torn down exits 1 with every record written and
  listed, and only the exit code says so.
  `test_a_run_that_failed_with_every_record_written_is_not_a_capture`.

It bought a test and not a composite. The table here is the full run after
that test, not a resume: a resume reuses a row whose text is unchanged, so it
would have carried the zero over.

## Ranked below the cap

Thirteen entries are logged in the row file's `[[dropped]]` and in the
table, each with why it ranked below the 25. They are not coverage. The two
review rounds reverted 116 guards between them in a copy of the tree, and
what those left at zero after the two fix rounds is the residual
`u297-b`, by name.

## What the table does not measure

The six scenario files and the pins of `tests/behaviour/__init__.py` have no
row of their own. They are held by one test,
`test_two_captures_of_one_commit_are_equal`, which runs the real capture
twice over every scenario and fails on anything a scenario prints or writes
that the stage did not pin.
