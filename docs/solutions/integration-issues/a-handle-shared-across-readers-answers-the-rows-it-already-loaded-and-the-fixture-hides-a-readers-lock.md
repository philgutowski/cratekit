---
title: "A handle shared across readers answers the rows it already loaded, and the WAL fixture hides a reader's lock"
date: 2026-11-12
category: integration-issues
module: src/cratekit/core/rb_writer.py
problem_type: integration_issue
component: database
severity: medium
root_cause: shared_session_state
resolution_type: code_fix
applies_when:
  - "Several readers that each opened their own rekordbox handle are made to read through one"
  - "A test wants to prove a held handle locks nothing while a provider is asked"
symptoms:
  - "A row changed by another process between two readers reads as it was when the first reader loaded it"
  - "A BEGIN EXCLUSIVE probe from a second connection succeeds even while a statement is open on the handle"
related_components:
  - pyrekordbox
  - sqlalchemy
tags:
  - shared-read
  - identity-map
  - wal
  - lock-probe
  - u267
---

# A handle shared across readers answers the rows it already loaded, and the WAL fixture hides a reader's lock

## Context

U267 made `crate organize --report` read the library through one handle,
`rb_writer.SharedRead`, where each step had opened its own. Two things about
sharing a binding handle were not where they looked.

## The identity map

The binding's handle is a SQLAlchemy session. A query for a row the session
has already loaded answers the object it holds, with the attributes it loaded
then, not the row as the database holds it now. A reader on its own handle
never sees this, because its handle starts empty and is closed after. A
second reader on a shared handle does: with rekordbox running and writing
during a report, it would take a row an earlier reader loaded as current.

So a shared handle is released between readers with
`db.session.expunge_all()`, which is what `SharedRead.release` does. Not
`rollback()`: that expires every loaded object instead, so an object a reader
kept would reload, or fail once detached, rather than keep what it read.
`tests/test_organize_one_read.py::test_a_release_forgets_every_row_so_the_next_reader_reads_afresh`
changes a row through a second connection and holds both sides, the stale
answer without a release as the control and the fresh one after.

## The fixture is WAL

The suite's fixture databases are in WAL mode, where a reader blocks no writer,
so a probe that takes `BEGIN EXCLUSIVE` from a second connection succeeds even
while a statement is open on the handle, and proves nothing. Switch the
disposable copy to the rollback journal first (`PRAGMA journal_mode=DELETE`),
where an open statement's lock keeps the probe out, and keep a control that
shows the probe refused while a statement is open.

The SQLAlchemy session keeps its own transaction object after a read, and with
it the pooled connection, but the driver begins no database transaction for a
SELECT, so a released handle holds no lock. Asking `db.session.in_transaction()`
answers True and says nothing about the database; the probe is the measurement.
