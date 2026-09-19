---
title: "A trial write with nothing to add returns before the refusals it was run to find"
date: 2026-09-19
category: integration-issues
module: src/cratekit/write/trees.py
problem_type: integration_issue
component: xml_bridge
root_cause: incorrect_assumption
severity: medium
resolution_type: code_fix
applies_when:
  - "A caller runs a byte writer over a copy of a document to learn whether the real write will refuse"
  - "The real write happens after something that cannot be taken back, a file move, a recorded intent, a database row"
  - "The trial is handed an empty list because the real ids are not known yet"
tags: [preflight, trial-write, catalog-tree, landing, early-return, rbxml, u77, r-455]
---

# A trial write with nothing to add returns before the refusals it was run to find

## What bites

The landing engine moves files out of staging and only then writes the label
tree, so it asks the catalog writer about a COPY of the export before the first
move. A refusal there costs nothing. The same refusal after the moves leaves a
batch in the library with no labels.

The first version of that check handed every year playlist an empty id list,
on the reasoning that where a folder goes, and whether two siblings share a
name, does not depend on the ids. That is true of the folder. It is not true of
a playlist the document already holds. `rbxml._extend_playlist` dedupes the
incoming ids against the held ones and **returns success when nothing is left
to add**, before its three refusals about the playlist's own layout: a tag that
does not start its own line, a missing `Entries` attribute, a close tag sharing
its line. An empty list always has nothing left to add.

So the check passed an export whose held `Kompakt 2025` had no `Entries`
attribute, the files moved, and the real write refused. The suite was green,
because every test of the check used a fresh export with no held playlist.

## Why it was not where it looked

The check called the same function the write calls, on the same bytes, with
the same tree. "Same code path" was the argument for trusting it, and it was
wrong: an idempotent writer has a fast path for "nothing to do", and a trial
with degenerate input takes the fast path. METHOD's third defect pattern is a
fix that lands on the performing path and not the checking path. This is its
mirror, a check that never reaches the performing path.

## The fix

`trees.check_record_labels_tree` gives every year ONE id no document holds,
`_TRIAL_ID = -1`, since rekordbox track keys are positive. The trial runs on a
copy, so the id is written nowhere. Pinned by
`test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend` and,
through the landing,
`test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`.
Mutation row `B6_trial_id` in `docs/mutation/u77-b.md` reverts it and kills two.

## How to apply it

Before trusting any trial of an idempotent writer, read the writer for an early
return on "nothing to add" and hand the trial an input that gets past it. Then
test the check against a document that ALREADY holds what the write will
extend, not only against a fresh one. `landing._check_export` also trials
`insert_intake_playlist` with an empty list. That one was read and is safe: it
replaces a held playlist whole and has no refusal that depends on the ids.
