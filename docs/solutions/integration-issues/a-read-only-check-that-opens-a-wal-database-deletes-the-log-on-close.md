---
title: A read only check that opens a WAL database deletes the log on close, so it must never open the copy it vouches for
date: 2026-11-13
category: integration-issues
module: "src/cratekit/core/rb_writer.py, src/cratekit/core/snapshot.py, src/cratekit/core/restore.py"
problem_type: integration_issue
component: snapshot
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A capture of a database with a handle open is recorded verified, and restore.plan refuses it as recording two files it no longer holds"
  - "The capture directory holds the database alone, while its manifest lists the database, its -wal and its -shm"
  - "Every capture test is green, because each one injects a verifier that opens nothing"
applies_when:
  - "Anything opens a database through the binding, sqlite3 or SQLAlchemy to read it, and something else has already recorded which of its files exist"
  - "A check, a diagnostic or a rehearsal is run on a capture, a snapshot or any copy a later step reads by its file list"
  - "A test of a capture or a restore passes a stand in verifier rather than rb_writer.integrity_ok"
related_components:
  - "restore"
  - "integrity_check"
  - "testing_framework"
tags:
  - "wal"
  - "sqlite"
  - "snapshot"
  - "capture"
  - "restore"
  - "integrity-check"
  - "stand-in-verifier"
  - "r1665"
---

# A read only check that opens a WAL database deletes the log on close, so it must never open the copy it vouches for

## Context

`snapshot.capture` copies the database and its companion files, records which
of them landed by looking at the directory, and then runs the integrity check,
`rb_writer.integrity_ok`. The check ran `PRAGMA quick_check` through the
binding on the capture itself. A read, so nothing could change.

In write ahead log mode that is not so. When the LAST connection to a
database closes, SQLite checkpoints the log into the main file and deletes the
`-wal` and the `-shm`. The check's connection was the only one the capture
directory ever had, so its close folded the log into the captured database and
removed both companion files the manifest had just listed. `restore.plan` asks
`snapshot.assert_sources_present` before it writes anything, and refused the
capture: "records 2 files it no longer holds". The undo of the write the
capture was taken for could not run.

It needs only a log file present at the copy, which any WAL database has while
a handle is open. The caller's own `PRAGMA wal_checkpoint(TRUNCATE)` does not
help: it truncates the log to zero bytes and leaves the file, so the capture
still holds an empty log and the index, and the check still deleted both.

## Why the suite could not see it

Every capture test in `tests/test_snapshot.py`, `tests/test_restore.py` and
U272's flush tests passes a stand in verifier, because their database is a few
bytes of text. A stand in opens nothing, so it never closes anything, so the
capture always kept its files. The real check was driven on WAL databases only
in `tests/test_rb_writer_db.py`, on snapshots with no log beside them.

The test that catches it uses the suite's real disposable database, which is
built in WAL mode because the real library runs in it, holds a connection open
with `wal_autocheckpoint=0`, captures with no verifier argument, and plans the
restore: `tests/test_snapshot_wal_r1665.py`.

## What was done

Two layers, each pinned on its own:

1. `integrity_ok` copies the file set it is given into a private temporary
   directory through `_copy_file_set`, the loop the capture uses, and checks
   the copy. The verdict is about exactly the given bytes, log included, and
   the close deletes only the copy's log.
2. `snapshot.capture` walks the capture before the check and again after it,
   and records verified only when every file is still there at the size and
   modification time it was copied with and every directory still exists.
   What a check adds is not asked about; the flush after the check covers it.

## The rule

Never open a file through SQLite to read it when another record already says
which of its files exist. Open a throwaway copy, or accept that the close may
fold and delete. A test of a path that reads a database through SQLite runs
the real reader at least once on a WAL database with a handle held open.
