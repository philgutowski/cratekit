---
title: A restore of an analyze adopt session puts the rows' titles back and not the files' title and key tags
found: at the review of #944, U327, 2026-11-23.
issue: yes
---

**The mechanism.** `crate analyze adopt` keeps each file's old title tag and
`initialkey` in its session record under `head_adopt_before`, persisted with
the capture before the first file is written, as the brief asks ("before
values kept in the run's record so a restore can put both sides back").
`crate restore run SESSION` restores the database capture and its coupled
state, and nothing under `src` reads `head_adopt_before`, so the files keep
rekordbox's key and tempo while the rows go back to Cratekit's.

**Measured cost.** Driven at review round one: adopt, then `restore run` on
its session, exit 0 `ok` with no warning; Golf read back with the database
Title `01A - 124 - Golf`, the title tag `09A - 98 - Golf` and `initialkey`
`09A`. Nothing is lost, since the record keeps every old value, and the
adopt's own answer now says a restore puts the rows back and not the files,
but an undo needs a hand edit per file and the two surfaces disagree until it
is made. A plan run again after such a restore reads the title tag's body as
the row's and plans each row again, so the next adopt re-corrects the rows.

**Closes when:** a restore of a session whose record holds
`head_adopt_before` writes each file's title tag and key tag back, read back,
or names the files it could not, and says so in its answer. An issue, since
an undo a DJ needs cannot finish with the shipped verbs (board bar (c)).
