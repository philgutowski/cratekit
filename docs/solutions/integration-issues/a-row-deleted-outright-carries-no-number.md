---
title: A row deleted outright carries no number, so the deletion pass numbers it at its first sighting, and only what the landing made tells a removal from a rollback
date: 2026-11-21
category: integration-issues
module: "src/cratekit/deletion/run.py, src/cratekit/deletion/watermark.py, src/cratekit/deletion/library.py, src/cratekit/intake/native.py"
problem_type: integration_issue
component: deletion_watermark
root_cause: wrong_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A track removed in rekordbox 7.2 is never offered by crate delete review, which reaches its gate with offered: 0"
  - "A brief says a session record names the rows a landing wrote, and the record holds no row"
applies_when:
  - "A reader treats a row the database no longer holds as a removal"
  - "Code orders a removal against the deletion watermark and the removal has no rb_local_usn"
  - "A brief names what a session record holds and the plan depends on it"
tags:
  - "deletion"
  - "watermark"
  - "remove-from-collection"
  - "r1037"
  - "r1844"
  - "u288"
  - "restore"
  - "absence-as-evidence"
---

# A row deleted outright carries no number

## What happened

rekordbox 7.2.19 deletes a removed track's rows outright (A178, A185), so the
soft delete marker the deletion pass partitions on never says the row went.
U288 read the removals `crate sync removed` records; R-1037's card asked the
pass to read the rows a native landing recorded. **The landing recorded none**:
the brief said its session record named each row it wrote, and a record
driven on the fixture held the batch playlist and the change counts and no
row. The card's first commit was therefore the write half, `collection_landed`
on the landing's record.

## The two traps

**An absent row has no sequence.** The watermark offers a removal whose
`rb_local_usn` is past it, and a row that is not there has none. A marked row
carries its own and a `sync removed` record states the count its commit left;
a row rekordbox deleted has neither. Numbering it at the current count on
every run moves it past every advance, so it is offered forever; numbering it
at the landing's count puts it under any watermark taken since, so it is
never offered. The pass keeps the count at the FIRST run that sees it gone,
in the watermark's document beside the position it is compared against, and
forgets it when the row is seen live again.

**Absence is not removal.** The session log survives a rollback and the
database does not, so a database from before a landing, put back by `restore
run`, by `restore bare-metal` from an older snapshot, or by a hand copy, leaves
the landing's record naming rows the database no longer holds, exactly as a
removal does. Two guards were tried and failed at review: a restore session
started after the landing (bare metal and hand copies write no record), and the
update count at the first sighting not yet past the landing's commit (any later
work moves it past before a review runs). The fact that holds is a playlist the
landing MADE: no database from before the landing holds one, and rekordbox's
removal leaves every playlist row. So a landed row is offered only while every
playlist its landing made remains, and a landing into a playlist already there,
which made none, offers nothing.

**A playlist is not a fact a person leaves alone (R-1844).** rekordbox 7.2.19
deletes a playlist outright when a person deletes it in the sidebar (A200), so
the playlist guard alone read the most ordinary tidy up as a rollback. The
landing now records each row's UUID beside its columns, and a landing stands
when the database holds one of its rows, live or marked, under that UUID, or
every playlist it made. The content id is random and the UUID a fresh one the
landing wrote, so no database from before the landing holds the pair; the id
alone is not enough, since an import after a rollback can draw the same random
id. What is still read as a rollback, a landing whose every row is gone and
whose playlists are not all held, is counted on the gate's screen.

## How to apply

Before planning on what a record holds, dump one from the fixture. Before
reading absence as an event, list every producer of the same absence (each
restore path, a recovery that writes no record, a hand copy) and find a fact
that exists in the database after the event and in no database from before it.
A record that some producers write is not that fact.
