---
title: "The first removal is a soft delete the binding returns to every reader, and the guard could not see one"
date: 2026-09-29
category: integration-issues
module: "src/cratekit/core/rb_writer.py, src/cratekit/write/trees.py, src/cratekit/write/rebuild.py, src/cratekit/adopt/move_cli.py"
problem_type: integration_issue
component: database
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A verb is about to remove, hide or retire a row in the rekordbox database for the first time"
  - "A reader goes through pyrekordbox's get_playlist, get_playlist_songs or get_content and reads no marker"
  - "A column is listed as bookkeeping so the write guard ignores a change to it"
  - "A plan is rebuilt from the library by a worker whose own write changes what the plan is built from"
  - "A find or create helper is used to resolve the place a read back will later look for"
symptoms:
  - "A track moved out of a playlist still reads as held there, so the same move is planned on every run"
  - "A track moved away and later moved back reads already present and is never added"
  - "A row whose only change is rb_local_deleted passes the whitelist in any table, the collection included"
  - "A resume refuses its own half finished work as a stale decision"
  - "An addition lands in a playlist rekordbox removed and the proof that it landed fails for ever"
related_components:
  - testing_framework
  - development_workflow
tags:
  - soft-delete
  - rb-local-deleted
  - guarded-writer
  - whitelist
  - membership
  - resume
  - r758
---

# The first removal is a soft delete the binding returns to every reader

## What happened

R-758 built the first verb that removes anything, `crate adopt move`. The
removal is rekordbox's own soft delete: the membership row stays and
`rb_local_deleted` is set. Four things followed that are not visible from the
code that makes the removal.

## 1. The binding hands a removed row back beside the live ones

`get_playlist_songs`, `get_playlist` and `get_content` filter nothing. While
no writer removed anything, a reader that ignored the marker on a membership
was right by accident, because a living playlist held no removed membership.
Measured on a copy of a snapshot on 2026-09-29: 4,817 membership rows carry
the marker and every one sits in a playlist that was itself removed.

The moment one verb removes, every reader is wrong at once. `read_tree` kept
reporting a moved track as held, so the plan that moved it planned the same
move again. `add_memberships` counted the removed row as present, so a track
moved away and back was never added.

**The rule.** Before the first removal lands, grep every call of the
binding's three lookups and decide the marker for each. A reader that asks
where a track SITS skips a removed row and a removed node.

## 2. The guard could not see a soft delete at all

`rb_local_deleted` is in `BOOKKEEPING_COLUMNS`, and the judge dropped
bookkeeping columns before it looked at anything. A row whose only change was
the marker read as untouched, in any table. "Writers are additive only" was
true of hard deletes and had never been true of the removal rekordbox
actually makes.

**The rule.** A column a guard ignores is a column a writer may change
unseen. Judge the marker before the filter. The pin on the ten bookkeeping
columns stays as it is, since the binding does touch them on create.

## 3. A worker whose write changes its own plan cannot compare digests

`adopt apply` rebuilds its plan in the worker and refuses when the digest
moved. A move changes what the tree holds, so a run stopped after its
additions rebuilds to a different plan and would refuse to finish. The
approved rows are frozen in the job, and the worker asks the plan's own rule
of each row against the library as it stands.

**The rule.** The check has to be the body the plan was built from,
`adopt.move.standing`. The first version compared the bucket and the sub, and
the built in review showed two states that keep both and that the plan would
leave alone.

## 4. Resolve what you add to the way you will look for it

The additive find or create reads no marker. The move's proof that a track
sits in its target walked live nodes only. With a removed namesake in the
tree the addition would land in it and the proof would fail on every resume.

**The rule.** One walk resolves both. Measured on the same snapshot, no
removed playlist or folder sits inside the routing tree today, so this was
fixed on the reading and not on an incident. The additive writers still use
the find or create that reads no marker, recorded as R-762.

## What was not observed

How rekordbox records ONE track taken out of a playlist that survives. The
binding's own call deletes the row outright and commits by itself. The soft
delete was chosen because it is reversible and because being wrong leaves a
track in both subs and never in neither. The attended run on a copy is what
settles it, recorded as R-761.
