---
title: "A dimension derived from the tree is derived after the rebuild's own write, or the clearing reads the tree the favourites were read from"
date: 2026-10-10
category: workflow-issues
module: "src/cratekit/write/rebuild.py, src/cratekit/write/genre_favorites.py, src/cratekit/write/tree_read.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
resolution_type: code_change
applies_when:
  - "A rebuild or convergence check gains a dimension whose placements come from the database (a playlist, the tree) rather than from the files"
  - "A new module both reads the rebuild's tree walk and hands the rebuild its placements"
  - "A mutation row on a new engine's guard is zero while the CLI test for the same situation passes, because the shared gate re-plans first"
tags: [rebuild, derivation, genre-favorites, convergence, cycle, tree_read, u119]
---

# A dimension derived from the tree is derived after the rebuild's own write

## What bit

The genre Favorites (U119) are the first dimension the rebuild files that is
derived from the DATABASE: which tracks are favourites is a playlist, and
which folder a favourite sits in is the tree. The first build derived them
beside the file placements, before the rebuild's write, and the review found
the hole by reading: a favourite whose tag had moved it to another folder was
placed in the folder it was READ from, the rebuild moved the track, the after
check converged on the stale placements and cleared the unconverged flag over
a Favorites that lacked the track. On a damaged tree the same order adds
favourites to the wrong folder's Favorites, which is additive and stays.

## The shape that holds

- Derive from the files, write, then derive from the tree as the write left
  it, write that in a second pass, and run the after check over both. The
  before check may use the pre-write derivation, since it reports and clears
  nothing.
- Give the second pass its own destinations and merge them into the node
  record, so a rename resolves through the record next time.

## The cycle it forces, and how it was broken

The engine needs the rebuild's tree walk (`read_tree`, `TreeNode`) and the
placement record (`DeclaredPlacement`); the rebuild needs the engine's
placements. The layering suite refuses a cycle even when one side imports
lazily. The walk and the two records moved to `write/tree_read.py`, which
both import, and the rebuild re-exports every name so `rebuild.read_tree`
and friends still resolve for every reader and test that knew them there.

## Two smaller things the same unit paid for

- A conformance sample that creates the thing a verb reads has to create it
  in the state the verb accepts: the fix round made an emptied source a
  refusal, and the sample that made an empty one turned the mutation
  driver's baseline red twice. The binding's query object is truthy with no
  rows, so a guard written as `if not handle.get_playlist_songs(...)` never
  fires; list it.
- A new key on a declared record defaults to the value every existing
  declaration meant (`signal = "vox"`), and the shipped template is what
  measures it: flipping the default kills the suite at collection, which the
  driver reports as a collection error rather than a death count.
