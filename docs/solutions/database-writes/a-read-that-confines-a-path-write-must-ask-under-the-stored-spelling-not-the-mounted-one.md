---
title: "A read that confines a path write must ask under the stored spelling, not the mounted one, or it finds none of its own rows and refuses a correct commit"
date: 2026-10-26
category: database-writes
module: "src/cratekit/intake/shelve.py, src/cratekit/intake/native.py"
problem_type: integration_issue
component: rekordbox_write
severity: high
resolution_type: code_change
applies_when:
  - "A write sets or changes djmdContent.FolderPath and then reads rows back by path to judge the commit"
  - "The library's djmdProperty records a base drive that differs from the mounted volume, as the live library's does"
  - "A LIKE or prefix read over FolderPath is written from a path the code composed on this machine"
tags: [djmdContent, FolderPath, base-drive, stored_folder_path, confinement, LIKE, u154, shelve]
---

## The trap

rekordbox stores every row's path under the drive the database was MADE on,
`djmdProperty`'s base drive, and remaps it to the mounted path at runtime.
`native.stored_folder_path` has spelled a written path that way since R-746,
so the landing's rows match the ones rekordbox made. The live library is such
a library: it was built on one volume name and mounted under another, and
every row it holds is stored under the old name.

U154 wrote the one verb that moves a row's file, `intake shelve`, and guarded
its commit with a read from SQL: every row stored under the target folder has
to be one the plan put there. The first draft composed that read's `LIKE`
prefix from the mounted target path. The rows were written, correctly, under
the base drive. On a library whose drives agree the check passed; on the live
library it would have found zero rows under the mounted prefix, read every
planned row as "not stored there", rolled back and refused a correct commit
as a whitelist violation. Every test passed, because the fixture's drives
agree. METHOD's hunt for what a green suite cannot see found it before the
review, and the live rehearsal proved it: the one row read back under the
recorded base drive, not the mount.

## The rule

A read that judges a path write asks under the SAME spelling the write used.
Carry the stored spelling on the plan (`ShelfBatch.stored_target`, produced
by the same `stored_folder_path` call that spells the rows) and build every
prefix, `LIKE` or `startswith`, from it. Never compose a stored path from a
mounted one at the point of reading. The one place that knows the stored
spelling is the writer's own function, and a reader that spells its own is a
second implementation that disagrees on exactly the libraries that matter.

Two more things the same read taught. SQLite `LIKE` is case blind for ASCII,
so a broad `LIKE` fetch is judged exactly in Python afterwards, or a folder
differing only in case is counted as a violation. And a target that is free
on disk may still hold rows in the collection, from a folder a person filed
by hand and moved since; the free name rule asks the collection too, under
the stored spelling, or the confinement check refuses the plan's own choice.

## How to see it

A fixture whose drives agree cannot show it. `tests/test_intake_shelve.py::
test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
monkeypatches `rb_writer.recorded_db_drives` to return a base drive other
than the root and asserts the rows are stored under it and the commit lands.
Any writer that reads rows back by path needs the same test.
