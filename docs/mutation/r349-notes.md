# R-349 mutation notes

The author's own table, 12 rows across `r349-a.md`, `r349-b.md` and
`r349-c.md`, under the 25 row cap. Every row is a guard this unit added. All
twelve were killed on their subset, so none was promoted to a full suite run.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| a, the two channels and the two readers | 4 | 4 | 0 |
| b, absence, listing, stale record, staging error | 4 | 4 | 0 |
| c, argv pairing, write failure step, unparseable record, argv render | 4 | 4 | 0 |

A1 is the brief's named row: dropping the failure path JSON write kills three
tests, the failed transfer scenario, the re-arm scenario and the P1 walk.

C3 was a zero before it was measured: nothing drove an unparseable record, so
`test_a_record_that_cannot_be_parsed_is_reported_rather_than_skipped` was
written first and the row then killed one.

Not measured, and why: the P1 mode itself belongs to `config.atomic_write_bytes`
and `_mkdir_private`, which are shared and already tabled, so this unit walks
the new directory under umask 000 instead of reverting them.
