# U313 mutation table, read

One table, the author's and not independent, `u313.md`, measured by
`scripts/mutate.py` on the cloud container at `0418fca0`, so a Linux measure of
a macOS suite, green net of the machine's failures. 25 rows, one per driver
rule that is a property of `mutate.py` (D1 to D15, over `mutate.py` and
`mutate_table.py`), the ledger numbering, the queue and the closing check in
`board.py` (B1 to B6), the checked run `cloud_battery.py`'s baseline and
compare now share (C1 to C3), and `revendor_downloader.py`'s shared target
check (V1). Null control 0 of 22,905, every restore verified against
`git show HEAD`. 23 killed, 2 zero.

## The known failures it subtracted

`.cloud-battery/baseline.txt` as measured on the base, 249 ids, plus one:
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`.
It killed the null control of the first driver run, so that table was
invalid and is not kept. Run alone it failed 3 of 3 on the base checkout and
4 of 4 on the branch, under `/tmp` and under `/var/tmp` alike (fresh inodes
near 620,000 against its bound of 2,000,000), so the `/var/tmp` remedy of
`docs/solutions/workflow-issues/an-inode-bound-test-passes-once-on-linux-so-the-baseline-misses-it-and-the-null-control-dies.md`
does not hold on this container. The id was added in a scratch copy passed to
the driver, with that measurement as its comment, as the solution file says;
the measured baseline file was not edited. The driver therefore measured its
own full baseline rather than reading the battery's record.

## The two zeros

- **C2_static_checks_skipped**, maintainer facing: the checked run going on
  past a red ruff or scan. No test held it on the base either. A test written
  after the table, `test_a_red_ruff_or_scan_refuses_baseline_and_compare_before_the_suite`
  in `tests/test_cloud_battery.py`, kills it: with the row's mutant applied it
  fails, without it passes, measured by hand on the branch. The row was not
  measured again by the driver.
- **V1_missing_target_patched**, maintainer facing: a vendor patch whose
  target file is gone. It held on the base in three copies, none tested; one
  line, as METHOD says for a maintainer facing zero. A renamed upstream module
  would surface when `revendor_downloader.py` is next run by hand.

## What the table shows

Every driver rule that is a property of the driver kills: no `-q` (D1), the
collected count (D2), a zero promoted (D3), no bytecode (D4), whole node ids
(D5), the restore verified against `HEAD` and always made (D6, D7), a dirty
target refused (D8, D9), a shallow clone (D10), a red baseline (D11), the
known failures header (D12), the null control (D13), and the exit codes
(D14, D15), which no test held before this unit.
