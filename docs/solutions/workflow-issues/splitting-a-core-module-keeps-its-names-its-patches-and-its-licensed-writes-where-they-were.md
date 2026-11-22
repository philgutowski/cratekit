---
title: Splitting a core module keeps its names, its patches and its licensed writes where they were
date: 2026-11-22
category: workflow-issues
module: "src/cratekit/core/jobs.py, src/cratekit/core/review.py, tests/modules/test_reports.py, tests/ratchets/reserved_causes/"
problem_type: workflow_issue
component: development_workflow
root_cause: missing_workflow_step
resolution_type: code_fix
severity: medium
symptoms:
  - "A test that patches jobs.complete_item still sees the real function called after the drive loop moved to another module"
  - "tests/modules/test_reports.py fails naming cratekit.core.review_suppressions: ['DecisionStore'] after a split that changed no behaviour"
  - "Two test_reserved_causes pin tests fail naming only the modules a split created"
applies_when:
  - "A unit under the refactor epic splits a core module over 1,500 lines into a parent and parts"
  - "A name of the module is patched by a test, or used outside the module"
  - "The code being moved writes a file"
tags:
  - refactor
  - split
  - monkeypatch
  - reports-guard
  - reserved-causes
---

# Splitting a core module keeps its names, its patches and its licensed writes where they were

## The shape that works (U301)

The part is a module of its own that imports what it needs from the parent,
and the parent imports the part's names back at its foot, after everything
the part reads is defined (`core/jobs.py` and `core/jobs_drive.py`;
`core/review.py` and `review_holds`, `review_exchange`, `review_groups`,
`review_surfaces`). Every name stays reachable at its old path, so no caller,
registry entry or test changes. Only the parent imports a part: importing a
part first meets a parent that is still loading.

## Three things a green test of the part does not show

1. **A patched name must still be read where the patch lands.** A test that
   patches `jobs.complete_item` replaces the parent's binding; a moved drive
   loop that imported `complete_item` by name keeps calling the original. The
   part reads every name a test patches through the parent
   (`_jobs.complete_item`, `_jobs.get`). List the patches first, by AST over
   `tests` (`monkeypatch.setattr(module, "name")` and `patch("...")`), not by
   grep.
2. **The reports guard licenses one module to persist.**
   `tests/modules/test_reports.py` exempts `cratekit.core.review`
   (`SANCTIONED_PERSISTENCE`) and audits every module it reaches, so a writer
   moved out of `core.review` (the decision stores' JSON file) fails it.
   Leave the writer in `core.review` and move code that writes no file instead.
3. **The reserved cause pins are per module.** A cause literal that moves to a
   new module fails `tests/test_reserved_causes.py` until the package's own
   pin file under `tests/ratchets/reserved_causes/` names the new module.
   Measure the four tables on the tree (`kebab_literals_by_module`,
   `modules_holding_a_named_cause` both ways, `modules_holding_a_cause_literal`)
   and copy what they say, with a dated comment.

The kill set replay follows moved text by itself: `killset.py rows --after`
finds a row's text in a file that did not hold it at the base commit.
