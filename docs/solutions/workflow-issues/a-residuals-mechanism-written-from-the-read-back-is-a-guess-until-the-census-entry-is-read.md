---
title: "A residual's mechanism written from the read back is a guess until the census entry is read, so probe the copy before building against the card"
date: 2026-09-30
category: workflow-issues
module: "cratekit.adopt.move, cratekit.adopt.plan"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: insufficient_investigation
resolution_type: workflow_improvement
applies_when:
  - "A residual names specific tracks or rows on the author's library and states why a verb missed them"
  - "The mechanism was written at an attended sitting from what the read back showed, not from the plan entry"
  - "The card's Why paragraph is the only account of the cause, and the brief says it was carded on the author's word"
symptoms:
  - "The existing tests already cover the shape the card describes and pass, so the defect cannot be reproduced from the card"
  - "The fix the card implies lands in a place the named rows never reach"
related_components:
  - "database"
  - "adoption"
tags:
  - "residual-findings"
  - "disposable-copy"
  - "adoption"
  - "move"
---

# A residual's mechanism written from the read back is a guess until the census entry is read

## The trap

R-780 said `adopt apply` found Nations and Mumbling Yeah already present in
their target and withheld nothing, so `adopt move`, which plans from
adoption's withheld list, never saw their stale second band. The card was
written at sitting 20 from the read back of the copy, which shows where a
track sits and not what adoption made of it, and it was carded on the
author's word the same day.

The shape the card describes, a track already in its target beside a stale
sub with a genre that routes to that bucket, was already a move under
R-758: `test_a_track_in_both_has_only_the_stale_one_removed` and the fixture
row `m-both-reads-high` both pass on `main`. A build against the card would
have had nothing to change, or would have changed the wrong layer.

## What the probe showed

A disposable copy of the live database, opened read only in a temporary
directory with rekordbox closed, answered in one query per track. Nations
carries the genre Progressive House, so its plan entry's bucket is
Progressive House, where it holds one sub, and the Organic House pair is in
a bucket its genre does not name. Mumbling Yeah has no genre at all, so its
disposition is needs-genre and it has no plan bucket. Neither was in the
situation the card described. The fix therefore lands on which buckets the
plan asks, not on how adoption's list is read, and the brief's own test
scenarios only make sense once that is known.

## The rule

When a residual names rows on the author's library, read those rows the
way the verb reads them before building: the collection row, its genre,
its plan disposition and bucket, the placements the tree gives it, and the
reading off the file. The standing constraint allows it, a disposable copy
in a temporary directory with rekordbox and its agent gone, and it costs a
minute. Then compare what the card says with what the entry says, and build
against the entry. Record the correction in the closing paragraph so the
next reader of the ledger does not learn the wrong mechanism from it.

The neighbour of this learning is
`a-cause-read-from-a-log-is-not-a-cause-driven-by-reproducing-it`, which
says the same of a cause read from a log. A read back is a log of where
things ended, and it says nothing about the path that put them there.
