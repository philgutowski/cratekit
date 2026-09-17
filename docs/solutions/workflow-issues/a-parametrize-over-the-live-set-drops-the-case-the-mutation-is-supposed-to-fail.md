---
title: "A parametrize over the live set drops the case the mutation is supposed to fail"
date: 2026-09-17
category: workflow-issues
module: "tests/test_adapter_listing.py, scripts/mutate.py, src/cratekit/acquire/listing.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A mutation row removes a member from a production set or mapping"
  - "The suite parametrises over that same live set at collection time"
  - "A residual or brief says to derive the cases from the set rather than write them beside it"
  - "scripts/mutate.py is about to measure whether removing a name from a guarded set kills a test"
symptoms:
  - "Removing a member from the production set kills nothing, and the collected count drops by one"
  - "The remaining parametrized cases pass, so the row reads as a zero with collect drift rather than a failure"
  - "Adding a name to the set grows the case list automatically and still does not fail when a name is deleted"
related_components:
  - development_workflow
  - documentation
  - testing_framework
tags:
  - mutation-testing
  - parametrize
  - circularity
  - guarded-set
  - test-fidelity
  - silent-failure
---

# A parametrize over the live set drops the case the mutation is supposed to fail

## Context

U65's mutation row `F2_the_structural_guard_loses_a_method_name` removed
`get_ep_singles` from `acquire.listing.GUARDED_METHODS` and killed nothing on the
full suite, 7584 collected. Filed as R-386. The residual's own closing condition
said the fix was a case per guarded method name, "driven from `GUARDED_METHODS`
itself so adding a name arms its own case".

U66 (issue 89) is that fix. The naive reading of that sentence, parametrise
`test_the_guard_catches_a_hand_written_pagination_loop` over
`listing.GUARDED_METHODS` at collection time, still zeros F2.

## What is actually going on

`scripts/mutate.py` mutates `src` and never the suite. Pytest then collects
against the mutated tree. A `@pytest.mark.parametrize("method",
listing.GUARDED_METHODS)` decorator reads the set after the mutation, so the
`get_ep_singles` case is not collected. The remaining cases pass. Collected
drops by one. The row is a zero.

"Derived from the set" and "fails when that member is removed" cannot both be
true of a parametrize over the live import, because the driver and the
parametrize share the same source of names and the driver edits it first.

## Guidance

The planted names live in the **test file**, which the driver does not mutate.
A separate assertion holds that test local set equal to the production set.

1. Removing a member still runs that member's planted case, which now reports
   no violation, and the case fails. That is the kill.
2. Adding a member without a planted case fails the equality pin. That is
   "adding a name arms its own case": the pin refuses the addition until the
   planted corpus grows.

U66 measured this. F2's exact mutation now kills 2 on
`tests/test_adapter_listing.py`, collected 47 against 47: the
`get_ep_singles` planted case and the equality pin. A collected count change
without a failure is not a close. Table `docs/mutation/u66.md`.

P4 still holds. The production set and the planted corpus describe the same
thing. Neither is a second handwritten list that can silently drift. The
equality is the derivation.

## When to Apply

- A brief says to parametrise over a production set so that adding a name
  arms a case.
- A mutation row deletes or adds a member of that set.
- A zero row is about to be dismissed because "the tests already parametrise
  over the set".
- A collected count dropped by the number of removed members and no test failed.

## Related

- `docs/solutions/workflow-issues/a-checker-that-reimplements-what-it-checks-drifts-and-stays-green.md`
  is the sibling failure, a second handwritten table that drifts. This one is
  the inverse: no second table, so the mutation deletes the case that would
  have caught it.
- `docs/solutions/workflow-issues/a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md`
  is why a collected count drop of one is not evidence the `get_ep_singles`
  case failed.
- `docs/residual-findings.md` R-386, closed in place by U66.
