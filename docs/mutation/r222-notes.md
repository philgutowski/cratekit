# R-222 and R-223, the mutation tables read together

Author run, 2026-09-19, on `relay/154`. Two tables, `r222-a.md` over the archive
rotation and `r222-b.md` over the open twin guard, run as two FOREGROUND batches
because a Relay session cannot wait on a background job and one 25 row
invocation can pass the 600 second tool ceiling. Batch a took 3 minutes 48
seconds and batch b 4 minutes 11. Both tables are valid, every row's restore was
verified against HEAD, and each null control killed 0 of 9034 collected.

**25 rows, the cap, 25 killed. No zero.** That is the author's count and reads
as "the author could kill every row the author thought to write". The
independent tables in this repository's history found more than the author's
every time they were run.

Rows that kill only because the author saw the zero coming and wrote or changed
a test first, said here so the 25 is not read as 25 guards the first suite
covered:

- `A9_rehearsal_purges`, a sample of an EXISTING guard. The change made the two
  tests that cover it vacuous, since their fixtures record no completed mirror
  and the engine then purges nothing for anyone. They were re-armed. The learning
  filed with this unit is about exactly this.
- `A10_plan_text_at_keep_zero`, `B5_whole_payload_compared`,
  `B8_every_exception_is_unreadable`, `B12_warnings_from_the_live_configuration`
  and `B3_any_library_is_a_twin` guard review findings, and each test was written
  with its fix.

Thirteen rows die to exactly one test. Each is one guard with one reason to exist,
and none was promoted to a full run because a death on a subset is a death.

## Considered and dropped at the cap

**None of these was measured.**

- `sorted(...)` on the listing in `_prune_archive`. Existing, unchanged, and the
  held and settled split depends on it; `A1` and `A5` measure the split.
- The `max(0, ...)` on the settled slice. Existing and unchanged.
- The unreadable twin's warning falling back to the live configuration for the
  share and identity warnings. `B12` measures the readable side.
- The twin envelope's `data` being the twin's and not a new job's. `B1` kills
  six through it.
- `_rotation_detail` at a negative keep. Existing wording, moved not changed,
  and asserted by the new parametrized test.

## The hunts a green suite cannot see

- Expected values from the code under test: the engine tests compute expected
  folder names with `backup.stamp_for`, which the engine also calls. It is not
  the function under test, it is unchanged, and it has its own tests, so the
  assertions are about WHICH folders survive and not how a stamp is spelled.
- One symbol, two meanings: `ArchiveRemote` in `tests/modules/test_tools.py` and
  `_ArchiveRemote` in `tests/test_backup_cli.py` are near copies. The test files
  here do not import from each other, and the two are not identical on purpose,
  one can overwrite nothing.
- The first caller owns the engine's failure paths: `_rotation_floor` is the
  first caller of `backup_facts.read_facts` from inside the prune. Its one
  failure, `BackupFactsUnreadable`, is driven by
  `test_a_record_that_cannot_be_read_purges_nothing` and is already translated
  by `perform_backup`, which wraps the whole of `run_backup`.
- The same shape one file over: recorded in the closing notes of both ledger
  entries, in the note added to R-549, and in R-558.
