# R-390 and R-391 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/99` in the foreground, each batch under the
tool ceiling on its own. Every row named its subset: `tests/test_jobs.py`
for the engine rows, with `tests/test_master_cli.py`,
`tests/test_acquire_workers.py`, `tests/test_backup_cli.py` and
`tests/test_outbound_workers.py` where a row's guard is what those suites
resume through.

**`r390-a.md`**, 6 rows over `core/jobs.py`'s `retry` and the backup shell's
transfer refusal, null control 0 of 9928, no collect drift, every restore
verified against `git show HEAD`. All 6 killed. A1 is the original defect,
the unconditional re-arm, and dies 5 times across three suites. A2 is the
flag not read, which refuses a cancelled job and a retryable transfer too,
and dies 6 times. A6 is the flag the review round added on
`backup-transfer-failed`; dropped, the three backup resume tests and the
refusal test kill it.

**`r390-b.md`**, 7 rows over the failure verdict, the job cause and the all
failed envelope, null control 0 of 9928, every restore verified. All 7
killed. B1 is the original defect, `failed[-1].reason`. B2 reverses the
sorted order and dies, which is the order pin. B5 moves the mixed threshold
so one shared reason is reported as mixed, and dies twice.

13 rows in all, under the cap. Two more were considered and logged as
dropped in the row files: re-arming the items ahead of the refusal, which
is the same write A1 restores, and removing `sorted()` entirely, which on a
two string set would die on half its runs by the process hash seed and so
would report a pass rate rather than a count.

## One row that did not measure the first time

- **B6, the envelope dropping its reasons.** The first run reported a
  collect error: the row emptied the block under `if len(permanent_reasons)
  > 1:` and left an `if` holding only comments, which is a syntax error
  that takes the whole module out of collection. A collect error is not a
  zero and not a death. Re-run with `pass` as the body, it kills 1.

## No zero rows

Every user facing guard the unit added died on its own subset, so no row
was promoted to the full suite and no composite is owed.
