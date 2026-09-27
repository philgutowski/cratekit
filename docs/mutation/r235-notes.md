# R-235 mutation notes

**Verdict: measured, 25 rows in two batches, 25 killed, no zero.** Written on
`relay/220`, 2026-09-27, by the author, so a kill here is the author's and the
absence of a zero is the author not finding one, which is not the same as
there being none. Independent tables on this repository have found 1.2 to 1.7
times what the author's did.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r235-a` | 13 | 13 | 0 |
| `r235-b` | 12 | 12 | 0 |

Both batches were measured twice. The numbers in the tables are the second
measurement, taken after the last change to `src`, the flattened approval
screen. Between the two, `M13` moved from 7 kills to 11 and `M19` from 7 to 6,
because tests were added and one assertion was rewritten. No row changed its
verdict.

## What the rows cover

- **M1 to M9 and M11 to M14, `core/tree_registry.py`.** The strict read of the
  session log, the native write margin at both sides of its coefficient, the
  unparseable start, the three halves of what counts as a native write, the
  open run refusal on a revert, the library's own revert guard with the verb's
  left in place, the session lock, the refusal of a second record, a check
  dropped from the precheck table, and the empty export.
- **M10 and M15 to M21, `cli/cutover.py`.** The verb's revert guard with the
  library's left in place, the root count, the already native answer, the two
  registry assertions each removed alone, the refusal of an unready library,
  the precheck table on the refusal, and the digest.
- **M22 and M23, `core/rb_writer.py`.** The two filters of
  `top_level_folders`, each removed alone.
- **M24, `cli/doctor.py`,** and **M25, `adopt/apply_cli.py`.**

## Two rows that would have been zeros

`M14` and `M18` are killed by tests written from the row list BEFORE the first
measurement, `test_an_empty_export_is_no_export` and
`test_the_catalogue_tree_is_refused_as_not_rebuildable`. Nothing drove either
guard before that, so both were zeros in everything but the measurement.
`M14`'s guard is U20's, from the fixed sample of existing guards.

## Guards covered by another guard

`M9` and `M10` are one rule asked twice, the library's and the verb's. Each
was removed alone and each dies, `M9` on the library tests and `M10` on the
verb refusing after the approval instead of before it. `M17` and `M18` are the
verb's copies of two assertions `record_cutover` makes again. Removed at the
verb, each dies because the refusal then arrives after the question and not
before it, which is the property the verb's copy is for.

## Dropped

Nothing was dropped for the cap. Not measured, and said so: the branch of
`_predates` for a record with no cutover day, which no caller can reach since
`native_writes` is only meaningful for a recorded tree, and the wording of the
five refusal messages.

## The driver stopped twice

The second measurement of `r235-a` stopped twice on the driver's state leak
check: the real installation state gained entries while a child ran. Read
before rerunning, as the driver asks. The entries were a `backup.run` run
record and its outcome files, and one `doctor` run, written by a backup job
running on this machine at the time, under the installed copy and not under
this checkout. No test in this unit reaches the real state: the full suite ran
six times in this session and the real `runs` directory gained one record in
that hour. The third attempt ran with nothing written and is the table.
