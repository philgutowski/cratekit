# R-1385 mutation table, read

One table, the author's and not independent, `r1385.md`, measured by
`scripts/mutate.py` on the cloud container, so a Linux measure of a macOS
suite, green net of the machine's failures. 15 rows over
`src/cratekit/sync/pair_cli.py`: the jobs every pair holds and a pair's own
read from them, the plan's ask and its registry, the order the twin hold is
asked in, the reason an awaiting row carries and its name fallback, the
apply time check, the warning's two sentences, and a sampled existing guard,
the failed and cancelled jobs `pair_jobs` passes over. Null control 0 of
17315, every restore verified against the branch head. 13 killed, 54
deaths; two zeros, read below.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base `2413a366`, 161 ids,
plus one in a scratch copy:
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
which failed alone here and killed the first run's null control. Temporary
files on this container took inodes near 606,000 under `/var/tmp` as well,
below the bound of 2,000,000, so the scratch copy and not a `TMPDIR` was
the route. The measured baseline file was not edited. See
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`.

## Runs refused

Three runs were refused or lost, none for the tree:

- Run one: the null control killed the inode test above and
  `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`,
  which passed alone twice.
- Run three: the null control killed
  `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`,
  which passed alone three times and with its file under `-n auto`.
- A container restart stopped one run mid null control; the comment it had
  appended to `pair_cli.py` was restored to the branch head before the next.

The two deaths were different tests, each green alone, so they read as
intermittent under the full parallel suite rather than the branch's. Runs
two and four were valid, the null control killing none.

## The two zeros

Both are guards round one of the review named unreachable, each reached only
by a code change, so the row file reads them as maintainer facing, one line
each:

- **M3, `_queued_elsewhere` reads a pair's own job as another's.**
  `plan_pair` asks the pair's own jobs first, so a track one of them holds
  never reaches the guard. M9, the pair reading none of its own jobs, kills
  7: the check that shadows it holds.
- **M5, `_queued_elsewhere` reads a pair's own ask as another pair's.**
  `plan` plans each pair once, and `plan_pair` registers its ask after its loop, so a
  pair's own ask is never there when it asks. M6, the ask never registered,
  kills 3: the registry it refines holds.

The first table, `9c564d02`, still read both as user facing: `--resume`
keeps a reused row's stored surface, filed as
`r1385-a-resumed-mutation-row-keeps-its-old-surface`. The two rows were
taken out of the sidecar and measured again for this table.

## Ranked below the cap

None: 15 rows under a medium card's table, every guard the diff adds
measured.

## Where each number was measured

The 13 killed rows are run two's, at `710e270a`, reused; M3, M5, the
baseline and the null control are this table's own, at `9c564d02`. No file
under `src` changed between `b143f84d` and either head, so every row
measured the same code.
