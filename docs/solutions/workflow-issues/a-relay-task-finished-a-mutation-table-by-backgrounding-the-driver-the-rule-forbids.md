---
title: "A relay task finished R-1's mutation table by backgrounding scripts/mutate.py, which is the exact pattern METHOD's driver rules forbid"
date: 2026-09-10
category: workflow-issues
module: "scripts/mutate.py, docs/METHOD.md"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: unverified_assumption
resolution_type: documentation_update
applies_when:
  - "A relay task's mutation table would exceed the ten minute foreground call ceiling, the situation the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md describes"
  - "A session is deciding whether to run scripts/mutate.py under a background job and poll it from a foreground loop"
  - "A session is about to treat relay task 38's closeout of R-1 as a template for finishing a table inside a relay task"
symptoms:
  - "A mutation table completes with all rows killing inside a relay task whose battery-measured baseline was already known to exceed 600 seconds"
  - "The driver's own transcript or notes describe polling pgrep for the mutate.py process while a background job runs it"
tags:
  - "mutation-driver"
  - "relay"
  - "foreground-ceiling"
  - "background-forbidden"
  - "method-compliance"
---

# A relay task finished R-1's mutation table by backgrounding scripts/mutate.py, which is the exact pattern METHOD's driver rules forbid

## What happened

Relay task 38 closed R-1 (U27, issue #27) and reported this as its own
learning: it finished the twenty five row table for `docs/mutation/r-1.md` by
moving the `scripts/mutate.py` call to a background job and running a
foreground Python loop that slept and polled `pgrep` for the mutate.py
process, so the turn never ended and the ten minute foreground ceiling
documented in
[`the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`](the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md)
never applied. A row that refused on a text mismatch was rerun with
`--resume`.

`docs/METHOD.md`'s driver rules say the opposite, without qualification:

> **Run rows synchronously in the foreground.** A backgrounded driver outlived
> its parent twice and contaminated later rows.

That rule is listed under "Driver rules, every one of them paid for," the
section title telling you each one was learned from an incident. This task's
technique is a background driver by the rule's own definition: `mutate.py`
running under a job the session is not blocking on, observed only by polling
`pgrep` rather than holding the call open.

## Why this run came out clean anyway

`git status` after the merge is clean, the battery passed, and all twenty five
rows in `docs/mutation/r-1.md` report killing. The task's background job was
tracked by the harness's own job control (a backgrounded Bash call the
session polls and can still see the exit of), not a `nohup`'d process
detached from the session the way the two prior contaminations were. That
distinction may be why this run did not repeat the failure METHOD's rule
describes, but the rule does not carve out an exception for it, and nothing
in this run proves the distinction is what protected it rather than luck.

## The rule

**Do not read relay task 38's closeout of R-1 as a validated technique for
the ten minute ceiling problem.** It is one clean run against a rule stated
as absolute for a reason that has already cost two contaminated tables. If a
future unit's baseline exceeds the ceiling, follow
`the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`: write the
rows, commit them, record the gap, land the unit, and run the table attended
or outside the relay task. Backgrounding the driver again, harness-tracked or
not, is the thing to bring to Phillip before repeating, not a shortcut to
reach for on the next relay task that hits the same ceiling.

## Related

- `the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`, the
  entry this run's technique appears to route around.
- `docs/METHOD.md`, "Driver rules, every one of them paid for."
- `docs/residual-findings.md`, R-1 (closed 2026-09-10) and R-333, filed by
  this same relay task.
