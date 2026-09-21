---
title: "A new input shape can make a rare branch the common one, and the old fixtures never reached it"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/modules/tools/setbuilder.py, src/cratekit/setbuilder/cli.py, tests/test_setbuilder_cli.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A unit adds a new kind of input to an engine that already has a green suite"
  - "The new input lacks a field the old inputs always carried, such as an unowned anchor with no energy"
  - "A fallback or filler branch only runs when the primary picks run short"
tags: [setbuilder, unowned, either-companion, fixtures, U98]
---

# A new input shape can make a rare branch the common one

## Problem

U98 added `crate setbuild --unowned LABEL --key 8A`, an anchor the library does
not hold. Driving it exposed a defect already on main. `build_plan` placed an
"either" companion (one that fits before or after) on both sides of the anchor,
so a thin library produced a sequence holding one track twice with no position 1.

## Cause

Owned anchors carry energy, so most companions are sorted into a before or an
after pick and the either filler is rarely needed. Every owned fixture had enough
before and after picks, so the filler never ran and the suite stayed green. An
unowned anchor carries no energy, so nearly every companion is either, and the
filler runs on most calls.

## Next time

When a unit introduces an input that lacks a field the old inputs always had,
ask which branches that field was quietly keeping dark, and drive those branches
on the new input before trusting the green suite. A pin for such a branch must
make every candidate take it (the U98 pin was narrowed to the anchor's own wheel
number so every companion is either), or it passes without ever reaching it.
Mutation notes: `docs/mutation/u98-notes.md`.
