---
title: "A worker that renames its item's file owes the resume an exact record of the new name, written before the rename"
date: 2026-09-08
category: workflow-issues
module: "src/cratekit/analysis/cli.py, src/cratekit/analysis/artifacts.py, src/cratekit/core/jobs.py"
problem_type: workflow_issue
component: job_engine
severity: high
root_cause: unverified_assumption
applies_when:
  - "A per item worker renames, moves or deletes the file its item identifies, and the item id is the pre change name"
  - "A queued verb's item is a filename or path rather than an identity that survives a rename"
  - "A resume refuses an item as source-missing over work that is visibly complete on disk"
  - "A worker recovers a missing item by scanning its folder for something that looks like the result"
  - "A unit binds a worker for intake, routing, rebuild or deletion, all of which move files under a queued item"
symptoms:
  - "A resume after a kill refuses an item as missing and the finished file sits in the folder under its new name"
  - "A resume reports a deleted source as done because an older file of the same stem was already in the folder"
  - "A recovery rule that strips a head and compares stems misses every file the naming template deduped or truncated"
  - "The job driver's contract says the artifact lands before the row flips, and the file was renamed before either"
related_components:
  - "job_engine"
  - "naming"
  - "resume"
tags:
  - "resume"
  - "rename"
  - "kill-window"
  - "item-identity"
  - "queued-verb"
  - "worker-binding"
---
# A worker that renames its item's file owes the resume an exact record of the new name, written before the rename

## Context

U58 (issue #76) bound `analyze.run` to a per item worker. Each item is an audio
filename relative to the frozen folder, and the worker's last act on a track is
the finalize: write the analysed values as tags, then rename the file to carry
its Camelot and tempo head. The job driver's contract is that an item's artifact
is made durable before its row flips to done, and that a resume redoes the one
unfinished item whole.

The rename lands INSIDE the handler. So there is a window, between the file
taking its new name and the driver flipping the row, where a kill leaves a
finished file under its head and a pending row under the old name. On resume the
worker looks for the item by its old name, finds nothing, and refuses it as
`source-missing`. The remedy it prints tells the person to re-run the verb over a
folder that has since changed.

## What happened

The unit's first fix for that window was a guess. The worker scanned the folder
for any file carrying a head whose stripped stem equalled the item, and if it
found one, reported the item as `skipped-prefixed`, resumed after a rename. The
test for it renamed the file by hand and asserted the resume was clean. It
passed, and the mutation table killed the guard.

The review over the whole branch found the guess wrong in both directions.

- **It matched the wrong file.** A folder that already held `08A - 124 - twin.flac`
  from an earlier pass, with a new `twin.flac` queued and then deleted before
  the resume, made the worker report the deleted source as analysed, with the
  older file's path in the report and the row flipped to done. A missing source
  was never surfaced.
- **It missed the right file.** The finalize renders the new stem through the
  naming template, which drops a trailing segment that repeats the lead and
  truncates an over budget stem with a hash tail. `Daft Punk - Around the World
  - Daft Punk.flac` is renamed to `08A - 124 - Daft Punk - Around the World.flac`,
  and stripping the head gives a stem that does not equal the item. The resume
  refused exactly the file the rule was written for.

The hand rename in the test hid both, because it produced a name the guess could
match and nothing else in the folder.

## Why the source does not explain it

Nothing in the worker says what a kill leaves behind, because the worker never
sees one. The driver's docstring describes the guarantee from the driver's side,
artifact then row, and the finalize's docstring describes its own order, tags
then rename. Each is correct. The window is in the composition, and the only
place it shows is a test that actually dies between the two.

## The rule

**A worker that changes the name of the thing its item identifies records the
new name in a place the resume reads, before making the change, and the resume
reads that record and nothing else.**

In U58 the record is a rename intent, a small JSON file in the item's staging
directory carrying the item id and the target path, written by the finalize
immediately before the rename. The resume, finding the source missing, reads the
intent, checks that the target exists, and only then reports the item as
resumed after a rename. No intent, or an intent for another item, or an intent
whose target is gone, is `source-missing`, which is the honest answer.

The staging directory is the right home because the driver clears it on the
next attempt at the same item, AFTER the resume has read it, and because it is
per item by ordinal, so two items with the same stem in different folders
cannot read each other's record.

## The test that holds it

The test for a kill window has to die in the window. The one that holds this
rule monkeypatches the staging call to raise a `BaseException` subclass on the
first finalized report, because `jobs.drive` converts `Exception` at the item
boundary and a kill is not one. The file is then under its head, the row is
still pending, and the second drive goes through untouched. A test that renames
the file by hand is a test of the hand rename.

## Where else this applies

Every remaining R-203 worker moves files under a queued item: intake finalizes
downloads into the library, routing moves tracks between folders, rebuild
rewrites a tree, deletion removes files. Each of them has this window, and each
needs its own record of what the item became, written before the change and read
by the resume, rather than a scan of the destination for something that looks
right.

## See also

- `docs/residual-findings.md`, R-283: the restamp has no such record, because its
  file is renamed by ANOTHER job's intent, which it cannot see.
- `docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`:
  the same unit's other lesson, that the first worker over an engine owns the
  engine's failure paths.
- `CONCEPTS.md`, "Rename intent".
