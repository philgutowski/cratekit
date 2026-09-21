---
title: A record nested inside the gates closes before the gates have judged the session
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/core/session.py"
problem_type: workflow_issue
component: seam_design
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A session the analysis watch refused over a moved grid is on record as closed, with its capture released"
  - "A context manager written as `with assert_gates(...) as gates, something(gates) as record:` reads as one unit and exits in two steps"
  - "An exception out of `commit_guarded` is read as nothing having been committed, and the rows are there"
applies_when:
  - "Adding anything that records the OUTCOME of a gated session: a session record, a job state, a watermark"
  - "Writing a second context manager beside `session.assert_gates` in one with statement"
  - "Deciding in an except block whether a database commit landed"
tags:
  - "session"
  - "assert-gates"
  - "analysis-watch"
  - "context-manager-order"
  - "commit-witness"
  - "restore"
---

## The trap

R-375 asked for a session record around a gated database write, so that the
capture the write takes is an undo `restore list` can show. The obvious shape is
a context manager the writer nests in its body:

    with session.assert_gates(...) as gates, recorded_write(cfg, gates) as record:
        ...

It was built that way first, every test passed, and it was wrong. Context
managers in one with statement exit in REVERSE order, so the record exits
first. It closed `closed`, which releases its capture to retention, and only
then did `assert_gates` run its own exit, which is where the analysis watch
compares every grid file against what it fingerprinted on the way in. A session
refused with `anlz-modified` was already on record as cleanly finished.

`assert_gates` looks like an entry check. It is also an EXIT check, and anything
that records how the session ended has to run after it.

`restore.recovery_session` had the same fault for the same reason. It opened its
record inside the gates by hand and closed it before the gates exited. That was
found one file over while fixing this, which is METHOD's fifth pattern doing its
job.

## What is true now

The gates own the record. `assert_gates(keep=session.Keep.RECORD)` opens it
between the lock and the analysis watch and hands it over as `Gates.record`, so
the watch's refusal passes through the record on its way out and closes it
`abandoned`. `Keep` is an enum and not a boolean because
`test_no_blanket_affirmative_satisfies_the_acknowledgment` reads the gate's
signature for a boolean parameter and refuses one, correctly: that is what a
blanket affirmative looks like (R34).

A caller that takes a capture does three things, and an AST guard in
`tests/test_write_session.py` asks every function in `src` that calls
`snapshot.capture` for all three:

1. `keep=session.Keep.RECORD` on the gates.
2. `session.attach_capture(gates.record, capture.root, cfg)` the instant the
   capture exists, BEFORE `snapshot.assert_verified`, because `restore list`
   lists an unusable capture rather than dropping it.
3. `session.record_commit(...)` the instant the commit lands, and only when the
   write added something. `restore._committed` reads committed sources to decide
   whether a restore would discard work, so a no-op that claims a commit makes
   every later restore refuse over sessions that created nothing.

## The second trap, in the same except block

An exception out of `rb_writer.commit_guarded` does not mean nothing was
committed. pyrekordbox's `commit` calls `session.commit()` FIRST and then
reconciles and saves rekordbox's legacy playlist file, so a failure saving that
file arrives as an exception over rows that are already durable. The rollback in
the except block does nothing by then.

Do not infer it from where the exception came from. Ask the engine:
`rb_writer.commit_witness(db)` listens for SQLAlchemy's `after_commit` on the
handle's session and its `landed` flag is the answer. Both writers record a
witnessed commit before re-raising.

The mutation table found the test for this was hollow on first writing. The only
failing write in the suite raised before any membership was counted, so the rule
that a pass which added nothing claims no commit was covering for the witness,
and a writer that recorded a commit on EVERY raise still passed. A guard covered
by another guard is a guard nothing covers. The killing test counts one
membership and then fails.

## What is still open

A hard kill runs no exit code at all, so it leaves the record `open`. That was
R-598, closed on `relay/187`: the record now names the lock's holder and
`crate session release` abandons it once that holder is provably gone. See
`the-lock-file-cannot-prove-who-owned-a-session-record.md`. A power loss is
still open as R-647.
