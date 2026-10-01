---
title: "A record that withholds a candidate needs an exit on every branch of the walk that skips it"
date: 2026-10-01
category: workflow-issues
module: "label/sweep.py list_for_label, label/gate.py, core/review.py held_offers, label/catalogue.py ReleaseTracks"
problem_type: workflow_issue
component: core_logic
severity: high
root_cause: incorrect_assumption
applies_when:
  - "A producer gains a new way to set a candidate aside without filing it, a hold, a deferral, a quarantine"
  - "A walk over a bounded window gains a state that is recorded once and read back on later walks"
  - "Two askers read the same rows through one reader and one of them is only sometimes asked"
tags: [label, sweep, offer-window, held-offers, genre-gate, outage-counter, r-798, r-790]
---

# A record that withholds a candidate needs an exit on every branch that skips it

## Problem

R-798 gave the label sweep a third thing to do with a release. It already
filed one for review or left it for later. Now it can hold one, recorded in
`held_offers`, because the general catalogue says it is not the kind of music
the label is followed for.

The first build wrote the hold and judged it again in exactly one place: the
branch of the window walk that meets a release with a standing hold. It was
green, and it read correct. Two passes of the built in review then found six
ways a hold was written and never looked at again.

## What was missed, and why it was easy to miss

`list_for_label` walks a label's releases newest first and stops when the
offer window is full. Every release leaves the walk on one branch: deleted on
purpose, already in the queue, not confirmed, owned, filed, or never reached.
A hold is a row that outlives the walk, so it has to be right on ALL of those
branches, and only one of them was written with a hold in mind.

- **Never reached.** Newer releases push a held one past the window. Nothing
  judged it again, so it stayed counted as held under a reason the label's
  new kind had made untrue.
- **Deleted on purpose.** The tombstone branch runs first and continues.
- **Already in the queue.** Two writes file a release and drop its hold. A
  process that dies between them leaves both, and the queue branch continues
  before the hold is looked at.
- **Owned.** A released hold was filed without asking whether the library
  had come to own the release, where an ordinary release is asked.
- **The label is gone.** A hold is only judged by a sweep of its label.
- **Held somewhere else.** `label approved` applies the same rule to an
  accepted release and held one that no sweep had ever held, so no row named
  it and the verb that returns a held release refused it.

## The rule

When a walk gains a record that outlives it, list every branch that ends an
iteration and say what the record becomes on each. Then list the ways the
subject can leave the walk entirely. For each, either the record is dropped,
or it is kept on purpose with the reason written down, or a person is told.
A record with one writer and one reader is the shape to distrust.

After the walk, reconcile what the walk did not reach. Here that is one
query for the label's holds in force and a judgment of each from the words
it recorded, with no request made.

## The second trap, same unit

The gate and the ownership question read a release's rows through one shared
reader. The first build let each asker count failed reads in a row for
itself. The ownership question is asked of every confirmed release and the
gate only of the ones not owned, so the gate never saw the successful reads
in between and counted three failures in a row that were not. Every later
release of the label was filed unjudged.

A consecutive count belongs to the thing every read passes through, never to
an asker. It lives in `ReleaseTracks` now, once, and remembered answers do
not move it.

## Where to look

- `src/cratekit/label/sweep.py`, `list_for_label`: `stale`, and the loop
  after the walk over `gate.in_force`.
- `src/cratekit/label/catalogue.py`, `ReleaseTracks`.
- `tests/test_label_genre_gate.py`: the tests named for a hold the window no
  longer reaches, a held release deleted on purpose, a hold on a queued
  release, and a read the gate never saw.
- `docs/residual-findings.md`, R-812: the two exits left open on purpose.
