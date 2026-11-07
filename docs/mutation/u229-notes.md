# U229 mutation table, read

One table, the author's and not independent, `u229.md`, measured by
`scripts/mutate.py` on the cloud container, so a Linux measure of a macOS
suite, green net of the machine's failures. 21 rows over
`src/cratekit/sync/pair_cli.py`: sixteen over what U229 added (the two widened
steps of `_owned`, the per plan copies on `_Reader`, `mirror_codes`,
`landed_isrcs` and the configuration error handling of the fix round) and a
fixed sample of five of the guards they sit behind. Null control 0 of 17258,
every restore verified against `git show HEAD`. 14 killed, 7 zero.

## How it was measured

- Fourteen rows were measured at `f12ce333`. The container restarted during
  row S1, leaving its mutation in the source; it was restored from
  `git show HEAD:` and compared before anything else ran.
- M15 read zero at `f12ce333`: its test left nothing lacking, so the widened
  step never ran. `c3b6bdc0` keeps that step asked, the row was taken out of
  the sidecar, and `--resume` measured it and the seven rows left at
  `c3b6bdc0`, reusing the fourteen. The commit between adds a test and
  changes no source, so a reused row's count can only be lower than a fresh
  one.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base, 161 ids, plus two from
`tests/test_repair_rows.py`, the inode bound tests:
`test_an_id_above_the_bound_that_is_the_files_inode_is_not_random` and
`test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`. They
killed the null control once and reddened the baseline once. Run alone on the
base `0c519b7d`, four times, the first failed four of four and the second
three of four. Neither touches `pair_cli`. They were added in a scratch copy
passed to the driver, each with that measurement as its comment, and the
measured baseline file was not edited. `/var/tmp` gave inodes under the bound
on this container, so it was not used. See
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`.

## The zeros

- **M7, the owning pair's re raise of a configuration error** (user facing).
  It keeps the base's refusal for a pair whose own job no longer reads. Its
  composite is M6, catching the error at all, killed 1. That the re raise is
  the right answer is round two's residual, filed as one.
- **M13, the reports copy** (maintainer). A plan reads each job's reports
  once; reading them per ask gives the same answer.
- **M14, an unreadable job read as empty** (maintainer). The same answer by
  design: the control on the None branch.
- **M16, the widened job step reading this pair's own jobs again**
  (maintainer). Equivalent, as round two found: the own step has already
  answered every one of them.
- **S3, S4 and S5, three of the sampled earlier guards** (user facing, from
  U128 and U130, unchanged by U229). They are: a landing still awaiting its
  import read as a landing; only a SUCCEEDED job's reports read; only an
  `owned` report taken. No composite was measured, and they are filed as one
  ledger residual rather than argued.

Every row is the author's.
