---
title: An unmapped row is not a row on a missing volume, so a guard that refuses on every one stops the verb on most real libraries
date: 2026-09-19
category: integration-issues
module: "src/cratekit/core/locations.py, src/cratekit/write/naming_cli.py, src/cratekit/write/trees.py, src/cratekit/deletion/candidates.py"
problem_type: integration_issue
component: recorded_path_resolution
root_cause: wrong_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A new guard refuses when any collection row resolves UNMAPPED, and existing tests over a folder outside the library only pass once they are given a prefix rule mapping the folder onto itself"
  - "A verb that ran yesterday refuses today over a track imported from a downloads folder, or over the demo tracks rekordbox installs"
  - "The brief says to refuse on an unmapped row the way the deletion pass does, and the literal reading is the defect"
applies_when:
  - "A guard is being written over locations.resolve_recorded_path and branches on Resolution.UNMAPPED"
  - "A fix is asked to make one writer agree with the deletion pass about rows it could not resolve"
  - "Existing tests need new configuration to keep passing after a guard lands"
tags:
  - "locations"
  - "prefix-map"
  - "unmapped"
  - "name-apply"
  - "fail-closed"
  - "r500"
---

# An unmapped row is not a row on a missing volume

## Context

R-500: `name apply` renamed a file a collection row names, because the row was
recorded under an old volume name with no prefix rule, so its only key was a
spelling no file carries. The brief said to refuse on any row whose prefix
matches no rule, the way the deletion pass does.

## What the name hides

`Resolution.UNMAPPED` reads like "the volume is not mapped". What
`resolve_recorded_path` actually returns it for is every absolute path that is
**not under the library root and under no rule**. Existence is deliberately not
asked there. So the same answer covers two rows that could not be more
different:

- `/Volumes/VOLUME/Music/a.flac`, the drive renamed years ago. Nothing on this
  machine carries that spelling. Which file the row names is unknown.
- A track imported from a downloads folder, or a demo track rekordbox installed
  under the home folder. The recorded spelling **is** the one on disk. Nothing
  about the row is in doubt.

Refusing on both is what the first cut did. It passed its own new tests and a
green suite, and it would have stopped `name apply` on almost any real library.

## The signal that was there before the review

Two of U67's tests, a root outside the library and a row recorded through a
link, failed until each was given an identity rule, `from` equal to `to`. The
session read that as "this is how such a folder is declared now" and edited the
tests.
**A guard that makes existing tests need new configuration is telling you what
it will ask of every user.** The built in review said the same thing afterwards,
with the demo tracks as its example.

## The rule that landed

A row is DARK, and refuses, only when both hold: it resolves `UNMAPPED` **and**
its decoded recorded path does not exist on this machine. A row whose file
exists has answered, and the as recorded key already protects that file. The
existence test fails closed, a path that cannot be inspected reads as absent,
and `exists` rather than `lexists`, so a link to nothing is dark.

This is a deliberate difference from the deletion pass, which refuses on every
unmapped active row. That pass needs a filesystem identity from every row to
prove a removed file unreferenced. `name apply` only needs to know no row could
name a candidate, and a row whose own file is present cannot.

## Also true at this seam

- A prefix is compared exactly, case included. A rule differing from the
  recorded volume only in case is no rule, to every consumer. Matching it in one
  verb makes that verb a second locate.
- A refusal that tells a person to write a rule must quote the **decoded**
  location. Rules are matched against the decoded path, and a percent encoded
  spelling copied into a rule never matches.
- `run-doctor` is the wrong remedy token for this condition. No doctor check
  reads the prefix map, R-527.
- `trees.located` is the one decode then resolve step. Call it rather than
  pairing `location_to_path` with `resolve_recorded_path` again.

## Narrowed again, 2026-09-23

The first live plan that would rename anything found 582 dark rows on the
live library and no honest rule for any of them: streamed tracks rekordbox
records as `/v4/catalog/tracks/<id>/`, a slash path with no file behind it,
and tombstones under folders that are gone (R-675). A dark row now refuses
only when its file name is one the pass would rename, since a renamed volume
changes a prefix and never a leaf. That rule closed R-523 and R-524 as well.
The learning beside this one, "A guard the verb consults only when there is
work", is why sitting 7 never saw it.

## Still open

R-525, drive letter rows are excused here and refused there.
