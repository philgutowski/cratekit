---
title: "A double belongs at the producer's boundary, not at the shape it produces"
date: 2026-09-10
category: workflow-issues
module: "scripts/board.py, tests/test_pending_units.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_workflow_step
resolution_type: test_fix
applies_when:
  - "A function is undriven because its only input comes from the network, a subprocess, or a live database"
  - "A residual says a test would need a fixture and treats that as a reason not to write one"
  - "You are about to hand a function a hand-built version of the structure some other function in the same file derives"
  - "The function under test also reads a file from a path it computes itself, so its return is part fixture and part tree"
symptoms:
  - "Two mutation rows over one function both kill zero, which says the function has no driver rather than that a guard is redundant"
  - "A typed fixture holds derived keys that a real producer computes: closure flags, reverse edges, transitive counts"
  - "A test over a hand-built structure keeps passing after the producer gains a field, while production has moved"
  - "A fixture value chosen to look realistic matches the addressing scheme of a real document the function reads, and a live record decides the test's answer"
related_components:
  - development_workflow
  - testing_framework
tags:
  - mutation-testing
  - zero-row
  - test-double
  - fixture-boundary
  - board-tooling
  - residual-finding
  - method-compliance
---

# A double belongs at the producer's boundary, not at the shape it produces

## Context

`scripts/board.py:contradictions` reports a board claiming work landed that the
repository says did not. It is the whole of why `board.py audit` exits 2, and
`sync` deliberately refuses to repair what it finds, because repairing a
disagreement between two sources of truth means choosing one to overwrite.

U59 measured that nothing in the suite executed it, and measured it properly:
one row restoring a real defect killed zero, which is ambiguous, so it was paired
with a composite that deletes the closure test entirely and reports a
contradiction over every open unit. That killed zero too. Two zeros over one
function is not a redundant guard. It is a function with no driver.

U59 recorded why it did not close it, and the reason is the interesting part.
`contradictions` takes the graph, the graph comes from `gh`, and a test therefore
needs a fixture. That unit's own table had just finished demonstrating what a
fixture-shaped measurement is worth, so it declined to write one and left the
decision recorded.

## What was wrong with the obvious answer

The obvious fixture is a hand-built graph, four dicts with the keys the function
reads. It is three lines and it passes.

It also measures almost nothing. The graph is not an input to this program, it is
an OUTPUT of `build_graph`, which computes closure flags from a state string,
reverse edges, a transitive reach count and an open-dependency list. Typing those
beside the test asserts that the function works on a structure the test's author
believes `build_graph` produces. Add a field to the real producer, or change how
`closed` is derived, and the typed graph goes on passing while production has
moved. That is this project's fourth recurring defect pattern named exactly: a
fix justified by a measurement taken on a fixture authored alongside it, arriving
with a confident number and a green suite.

## The rule

**Put the double at the boundary the code genuinely cannot cross, and let
everything downstream of it run for real.**

Here that boundary is one JSON payload: the list of dicts
`gh issue list --json number,title,state,body,labels` returns. The test builds
that, `build_graph` runs on it unmodified, and `contradictions` receives a graph
the code derived rather than one a person typed. The fixture is now a
transcription of an external API's response, which is the one thing in this path
that no local code owns.

Two things make it hold:

1. **Pin the payload against the request.** The remaining drift is that the
   double stops resembling what the caller asks for. Read the field list out of
   the calling function's own syntax tree and compare it against the double's
   keys. Read it structurally, not with a pattern over field names: a pattern has
   to describe what a field name looks like, and `[a-z,]*` cannot express gh's
   `closedAt` or `stateReason`, so the first camelCase field added would have
   failed the test with a message about the literal being unfindable when the
   real problem was the double drifting. A wrong diagnosis sends the reader to
   the wrong file.
2. **Take the OTHER inputs as arguments.** `contradictions` also read the live
   register through `owed_by_unit()`. A test keyed to whatever `main` owes today
   passes for a reason unrelated to the code and goes red the day somebody
   discharges a marker, so the register became an optional argument, exactly as
   the sibling function `unresolved_closes` already took it.

## The trap that comes with step 2, and it cost a round here

**Making an input injectable moves the undriven path one frame up.** Every new
driver supplied a register, and the only production caller, `cmd_audit`, supplies
none. So `owed = owed or {}` in place of the `is None` test kept the entire
battery green while the audit stopped reporting register contradictions and
returned 0 where it owed 2. That is the same finding the work was opened to
close, reproduced by the fix for it, which is the fifth pattern METHOD names: a
fix round fixes the instance it was handed and reproduces the class one file
over. Measured as `B5_owed_default_dropped`, two kills, only after a row was
written for the default branch on purpose.

## The second trap: a function that is half fixture and half tree

`contradictions` returns its register comparison PLUS `repointed_residuals`,
which reads `docs/residual-findings.md` from a path it computes itself. So no
double can make its return fully synthetic.

This is not theoretical. The first draft of the driver included a non-unit board
item titled `R-4: a residual, not a unit`, chosen to look like the real board.
`R-4` is a real address in a fourteen thousand line ledger nobody edited for the
test, the repoint check found a genuine mismatch, and the assertion failed
against a second finding the test had not asked for.

The remedy is to know which half is which and choose deliberately:

- Exercise the node SHAPE without the addressing scheme. An attended-chore title
  is the same kind of node, a board item that is not a unit, and drags nothing in.
- Drive the file-reading half separately, with the reader replaced, so what is
  measured is the comparison rather than the parse.
- Pin the parse against the real document only where the document's own rules
  make that stable. Residual numbers here are append only and a renumber is
  forbidden, so one heading asserted by number and title says the same thing next
  year, and a red test would mean a rule this project treats as absolute has been
  broken.

## Do not record a limitation you have not driven

The same task's first row file dropped a row over `cmd_audit` with the logged
reason that it shells out to `gh`, so it could not run without a token. False.
Every name that function calls is module level and replaceable, the test file
already replaced two of them, and the module loader used there returns a fresh
module per call so nothing leaks. The row was re-run in a later batch and killed.

Worse than being wrong, it certified the hole: the next reader would have found
the gap considered and settled. The same error is already recorded in this
repository from the other direction, in the same test file, where an earlier
version of the closing-spelling table asserted that `Fixes #36` does not close an
issue and justified it with the repository's own contract. A test, or a dropped
row, may not assert a limitation into a fact.

## Where the record lives

`docs/mutation/u81.md`, `u81-round-2.md` and `u81-round-3.md` are the three
batches, ten rows, eight deaths and two explained zeros.
`docs/mutation/u81-notes.md` is the author's reading, including the correction
above. R-322 carries the closure and R-327 carries what is still undriven, the
board's write half, which needs a project-scoped token and has no local payload
seam to build a double at.
