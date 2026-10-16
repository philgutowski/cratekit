---
title: "A minted content ID is an int but a stored row's is text, so a flush that mixes a new row and a dirtied existing one cannot sort by primary key"
date: 2026-10-16
category: database-writes
module: "src/cratekit/intake/native.py, src/cratekit/favorites/colour.py"
problem_type: binding_quirk
component: rekordbox_write
severity: medium
resolution_type: code_change
applies_when:
  - "A write creates a new content row with db.add_content AND dirties an existing content row in the same commit"
  - "The existing row was loaded from the database rather than created this session"
  - "The commit flushes several djmdContent rows at once"
tags: [pyrekordbox, sqlalchemy, djmdContent, flush, primary-key, u153, favorites, colour]
---

## The trap

`pyrekordbox`'s `add_content` mints a new row's `ID` with
`generate_unused_id`, which returns a Python `int`, and sets `ID=id_` on the
object. The `djmdContent.ID` column is text, so once the row is flushed and
read back it is a `str`, which is why this package stores `str(content.ID)`
everywhere. The divergence lives only in memory, between an unflushed new row
(int) and an already-loaded existing row (text).

It bit the moment U153 made the landing dirty an EXISTING content row in the
same commit as a new one, to colour a heart Pink. SQLAlchemy's unit of work
sorts the pending rows of each table by primary key before flushing, and a
`djmdContent` set holding one int ID and one text ID raises

    Could not sort objects by primary key; primary key values must be sortable
    in Python (was: '<' not supported between instances of 'int' and 'str')

and the whole commit fails inside the binding, after the files were already
moved. Before U153 no writer dirtied an existing content row beside a new one,
so only new rows (all int) were ever pending together and the sort never saw a
mix. A green suite hid it because every test that lands a file stages a new
one; the clash needs a new row and a pre-existing row written together.

## The rule

Coerce the minted ID to the form the database stores, on the object before the
guard's flush, so the in-memory representation matches what every later open
reads and what every caller already assumes. `_restamp` does it in one line,
`content.ID = str(content.ID)`, next to where it already corrects the path, the
device and the file id the binding got wrong. This is the fix at the source;
do not chase the symptom by committing the colour separately or by sorting the
session yourself.

A second, independent safety net sits in `favorites.colour.find_row`: it
returns a row the session holds pending-insert before querying, so a heart made
this commit is coloured on the one instance rather than loading a second. With
the ID coerced that path is redundant (the autoflush `get_content` triggers
finds the same row), which the U153 mutation table records as a composite-held
zero, but it is the clearer expression of intent and is kept.

## How to check

Land a file (a new row) in the same commit as a write to an existing content
row, and assert the commit succeeds and both rows carry their intended values.
`tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
is that shape. The guard that fixes it is pinned by the `N1_restamp_id_text`
mutation, ten deaths.
