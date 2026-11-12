---
title: A first delete review baselines before the reference set is built, so its clean gate proves nothing about the set
date: 2026-11-12
category: workflow-issues
module: "src/cratekit/deletion/run.py, src/cratekit/deletion/candidates.py"
problem_type: workflow_issue
component: deletion_reference_set
root_cause: wrong_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A residual about the reference set is closed on a live delete review that reached its gate with no refusal"
  - "The same library later refuses deletion-reference-set-incomplete on a run that has removals to offer"
applies_when:
  - "A live run of crate delete review is read as evidence about the reference set, the prefix map or which rows refuse"
  - "A first run on a database, or a run after a re-baseline, is the one being read"
tags:
  - "deletion"
  - "reference-set"
  - "watermark"
  - "baseline"
  - "absence-as-evidence"
  - "r676"
  - "u243"
---

# A first delete review proves nothing about the reference set

## What happened

R-676 said the deletion pass would refuse on the 137 rekordbox streaming rows
recorded as `/v4/catalog/tracks/<id>/`. It was closed at the ninth attended
sitting because a live `crate delete review` reached its gate with no
`deletion-reference-set-incomplete`: baselined, 7404 rows accepted as history,
0 offered. Seven weeks later the next removal on the same library refused over
exactly those rows (U243, #672), and the files were trashed by hand.

## Why the first run could not have refused

`run.plan` reads the collection, and when the database has no watermark it
records the baseline and RETURNS, before `candidate_rules.reference_set` is
ever called. A first run, and any run that re-baselines, never builds the set,
so it cannot refuse over any row in it. "Reached the gate with no refusal" was
a statement about the baseline branch, read as one about the reference set:
the first of the four recurring defect patterns, absence read as evidence of
absence.

## What to do

- Read a reference set claim only off a run whose plan says `baselined: false`.
  The gate screen carries it (`shown.baselined`); a run that says `true` is
  evidence about the watermark and nothing else.
- To measure the set on a library without trashing anything, run the verb
  twice on a disposable copy: the first run baselines, the second builds the
  set and either refuses or reaches the gate, where `abort` moves nothing.
- Since U243 the gate screen says how many rows the proof excused as no local
  file, and the refusal names every unmapped prefix, so the second run's
  screen is the measurement.
