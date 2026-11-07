# U230 mutation table, read

One table, the author's and not independent, `u230.md`, measured by
`scripts/mutate.py` on the cloud container at `3b25a517`, so a Linux measure
of a macOS suite, green net of the machine's failures. 22 rows over
`modules/outbound/mirror_edits.py` (15), `organize/mirror_downloads.py` (3)
and `organize/account_mirror.py` (4), and two considered and dropped. Null
control 0 of 17272, every restore verified against `git show HEAD`. 20
killed, 70 deaths, two maintainer zeros read below.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base `0c519b7d`, 161 ids,
plus one:
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`.
After the container restarted on 2026-11-07 it failed four times of four run
alone on the base, because it expects a file inode above 2,000,000 and ext4
here gave 575,000 to 690,000 under `/tmp` and `/var/tmp` alike, so the
`/var/tmp` route did not hold. The id was added in a scratch copy passed to
the driver, with that measurement as its comment, and the measured baseline
file was not edited. See
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`.

Four driver runs were refused before this one, none for the tree:

- the container restarted under the first, which was restored from `HEAD`;
- the null control of the next three killed one test each, a different one
  every time: `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`,
  the inode test above, and
  `tests/test_sync_land.py::test_a_stale_queued_analyze_job_is_replaced_not_resumed`.
  The first and the last passed alone three times and with their whole files,
  so they are intermittent under the parallel run, and neither reddened
  twice.

## The zeros, and what they bought

The first table, at `db61a574`, read four zeros:

- **M6 and M11, user facing, each bought a test.** No test held a never
  agreed queuing playlist whose row a person moved, gave a second band, or
  took out of the tree in rekordbox before any carry, so dropping the
  landing's filing guard, or reading no band as the landing's, was not seen.
  `test_a_band_a_person_chose_before_any_carry_is_not_lifted_over` and
  `test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over`.
- **M7 and M9 are equivalent since round one's guard** and are dropped with
  that reason: the lift takes only a never agreed playlist, whose base is its
  account side (`Mirrored.base`), so the account guard and the base guard
  answer alike.

The table here is a full run after both tests, not a resume, which would have
carried the zeros over.

The two zeros it leaves are maintainer rows, each without a user facing
consequence:

- **M17**, `queued_from` keeping a job with a blank source: the reader maps
  only a truthy remote identifier to a title (`_read_edits`' `titled`), so a
  blank source names no playlist and lifts nothing. The first table counted
  it killed by one death in the full suite fallback, which was the inode
  test.
- **M21**, `_read_edits` naming the queue for a track with no landing: such
  a track has no `filed` places, and `_as_queued` lifts nothing without
  them, so the filter only trims the map. Read the same way as M17 on the
  first table.
