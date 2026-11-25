---
title: "A key given through a created row's relationship is unseen by the whitelist's judge, and the mapper writes it only at the flush"
date: 2026-11-25
category: database-writes
module: src/cratekit/core/rb_writer.py
problem_type: testing_gap
component: database
severity: high
root_cause: incorrect_assumption
resolution_type: test_fix
applies_when:
  - "A mutation row on the read back's pending source or its flush reads zero and is about to be named equivalent"
  - "A test needs a created row whose stored value its object does not show, without planting by SQL"
  - "A writer is about to give a created row a lookup by its relationship rather than by its id column"
symptoms:
  - "Removing session.new from the read back's sources, or skipping its flush, kills no test"
  - "No column default or insert listener on the policy columns seems to exist, so no producer seems possible"
related_components:
  - pyrekordbox
  - sqlalchemy
tags:
  - gridless
  - read-back
  - relationship
  - flush
  - mutation-zero
  - r2075
---

# A key given through a created row's relationship is unseen by the whitelist's judge, and the mapper writes it only at the flush

## Context

`assert_created_rows_are_gridless` reads back every row a session creates,
from two sources, the binding's update buffer and `session.new`, and flushes
first so a still pending row has an identity to select by. R-2072's table read
both zero (S2, the pending source dropped; S3, the flush skipped), and R-2075
recorded that no producer was found: the binding sets no default and no
insert listener on any policy column, so a pending row's stored values looked
like exactly what the whitelist had already judged.

## The producer

A relationship. `DjmdContent.Key` is a relationship over the foreign key
`KeyID`, one of the ten columns a content row this product creates must leave
empty. Assigning `content.Key = key` on a pending row puts `Key` in the
instance dictionary and leaves `KeyID` out of it. The whitelist's in memory
judge, `rb_changes._declared_columns`, reads column names from that
dictionary, so it sees nothing to refuse. SQLAlchemy writes `KeyID` from the
relationship only when the row is flushed. Every check in `commit_guarded`
runs with the automatic flush suspended, so the read back's own flush is the
first moment the value exists anywhere, and the read back is the only layer
that refuses it. A row added with the binding's tracking off
(`db.registry.disabled()`) is in `session.new` and not in the buffer, so only
the pending source reads it.

On an existing row the same assignment is refused by the whitelist, by name:
a modification of `Key` is not a registered column. Only a creation leans on
the read back.

No writer in `src` gives a created row a key through the relationship, or adds
a row with tracking off, today; the tests stand for the next one that does.

## What works

`test_a_key_the_mapper_writes_only_at_the_flush_is_refused_by_the_read_back`
in `tests/test_rb_writer_db.py`, on the disposable database: a key row
committed through the guard, a content row added through the binding or with
tracking off, `content.Key = key`, an assert that `KeyID` is not in the
instance dictionary (the precondition that keeps the judge blind), then the
read back's own wording asserted and the whitelist's absent. It kills S2, S3,
and a flush moved before the pending set is gathered.

## The general rule

Before naming a guard equivalent for want of a producer, list every way the
mapper itself writes a column the object does not show: column defaults,
insert listeners, and relationship synchronisation of a foreign key. The last
is the easy one to miss, because the object does show something, under
another name.
