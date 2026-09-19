# R-259 mutation tables, read

Two tables, the author's and not independent, measured by `scripts/mutate.py`
on `relay/161`. Every zero row in this record means the author could not kill
it, not that nobody could.

**`r259.md`**, 24 rows from `r259-rows.toml`, measured on the tree after the
`/code-review` fix round. 23 over the guards this unit added to
`label/sweep.py` and `label/cli.py`, and one sample of the increment's
existing owned filter in `sync/scope.py`. Subsets derived from imports, every
zero promoted to the full suite. 19 killed, 5 zero. Nothing was dropped.

**`r259-b.md`**, the two user facing zeros re-measured after the tests they
bought: both killed.

**A first attempt at `r259` was invalid and was discarded.** Its null
control, a comment appended to `label/cli.py`, killed 25 tests, every one in
`tests/test_rebuild.py`, over a baseline of 8257 collected and exit 0. The
driver refused the batch as it should. `tests/test_rebuild.py` then passed
alone, 103 of 103, and the rerun's control killed nothing. Not investigated
further: one occurrence, not reproduced, and not this unit's module.

## The five zeros

- **O2, a row the reader cannot read counts as owned.** User facing. Bought
  `test_a_release_with_a_row_the_reader_cannot_read_is_offered`, a release with
  one row naming no artist beside rows the library holds. Killed in `r259-b`.
- **F5, a successful track read no longer resets the run of failures.** User
  facing: failures that are not in a row would stop the asking. Bought
  `test_a_track_read_that_succeeds_breaks_the_run_of_failed_reads`. Killed in
  `r259-b`.
- **O6, the empty identity guard.** Maintainer facing, one line: an empty
  identity sent to the real adapter raises `ReleaseUnresolvable`, which answers
  not owned, so the guard saves a call and changes no answer.
- **L3, the cache keeps every job's view.** Maintainer facing, one line: only a
  process driving two jobs could see it, and the CLI drives one.
- **L4, the cache key forgets the job.** Maintainer facing, one line: the same.
  A later job in one process would read an earlier job's library walk.
