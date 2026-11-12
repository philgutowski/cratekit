# U244 mutation notes

The table, `u244.md` and `u244.json`, measured 25 rows at the head of fix
round two, `05ef5e74`, against a scratch copy of the Linux known failures. The
batch is valid: the null control killed nothing, the baseline was green net of
the known failures, and every row's restore was verified against `HEAD`.
Measured by the author, so every zero reads as "the author could not kill it".

**One id subtracted beyond the measured baseline.** The first run was refused
as INVALID: the null control killed
`tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`
under the full parallel run. It passed alone 6 of 6 on the branch, its file
imports nothing this unit touched, and it is the inode bound class
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`
names. `/var/tmp` and `/tmp` gave fresh files inodes of 575152 and 417824,
both under the test's bound, so that entry's `TMPDIR` remedy did not apply.
Following its fallback, `.cloud-battery/baseline.txt` was copied to the
scratchpad with that id and this measurement appended, and the copy was passed
to `--known-failures`; the measured file was not edited.

**21 rows killed, 4 zero, each promoted to the full suite.**

- `M12_unread_release_not_a_miss`, zero, maintainer facing. Fix round two put
  `if held is not None: return held` ahead of the styleless match, so the last
  line's held branch can no longer be reached and its mutation changes
  nothing. The held answer is pinned through the earlier line by
  `M10_unread_outranks_styleless` (killed) and by
  `test_a_release_that_could_not_be_read_beside_misses_is_not_a_miss`.
- `M15_empty_title_guard`, zero, maintainer facing. With the guard gone, an
  empty side strips to nothing and takes the fallback branch, which answers
  False for it too, so the guard is redundant with the branch below it. That
  branch is `M16_bracket_title_guard` (killed).
- `M19_fallback_bucket_passed_over`, zero, user facing: the shipped template
  lists the fallback's name as too coarse, so the next check covered it. The
  composite is a copy whose too coarse list leaves the fallback's name out,
  where only this check stands:
  `test_a_word_resolving_to_the_fallback_is_passed_over_where_its_name_is_not_too_coarse`,
  added after the table, fails under the M19 mutation and passes without it
  (run by hand, 1 failed and 1 passed; the source restored from `HEAD` and
  diffed clean).
- `M25_upgrade_table_kept_whole`, zero, a backstop on a write path. The block
  appended is checked by `cut_table` to parse to exactly the shipped table,
  the non vocabulary keys are checked beside it, and TOML refuses a second
  definition of the table, so no copy was found that parses with its
  vocabulary changed beyond the one table added. No producer driven; the
  author could not kill it.

**Dropped below the cap of 25:** the malformed token check (replaced by the
kept passed over row, round two's B2), the results naming no release by
number (replaced by the unread pressing outranking a styleless match, round
two's R1), the not JSON answer, `_remaining`'s ASCII check, the summary's art
only exclusion, and `for_discogs`' keychain refusal. Each has a test in
`tests/test_discogs_searcher.py`; none was measured here.
