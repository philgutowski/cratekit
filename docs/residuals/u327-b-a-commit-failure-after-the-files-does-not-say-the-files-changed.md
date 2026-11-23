---
title: An analyze adopt whose commit fails after the files were written says only the database's error, not that the files already carry the new head
found: at the review of #944, U327, 2026-11-23.
issue: no
---

**The mechanism.** The adopt writes the title tags and key tags inside the
session, then the rows, then commits. A commit that raises (a locked
database, a guard refusal) ends the verb with the engine's own cause, for a
lock `internal-error` "OperationalError: database is locked", and nothing in
the message says the files had already taken rekordbox's key and tempo.

**Measured cost.** Driven at review round one with the commit raising a lock
error. No data is lost: the record keeps every old value, and the plan run
again sees the files corrected and writes only the rows (`test_a_file_already
_corrected_is_continued_by_planning_again`). A person reading the refusal is
not told the two surfaces now disagree until the rerun.

**Closes when:** a failure after the first file names the files written and
the rerun that finishes the rows. Ledger only: nothing is lost and the next
run converges.
