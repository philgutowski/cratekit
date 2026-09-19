---
title: "A gated verb driven on sample arguments over an empty library can never end on PENDING_HUMAN"
date: 2026-09-18
category: workflow-issues
module: "tests/test_cli_contract.py, src/cratekit/intake/land_cli.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: incorrect_assumption
resolution_type: design_decision
applies_when:
  - "A new entry in cli/registry.py declares at least one GateSpec"
  - "The verb's engine would normally end a real run on PENDING_HUMAN, a pending human action, or any other non-OK terminal outcome"
  - "_sample_arguments in tests/test_cli_contract.py is given arguments for the new verb"
  - "The fixture the conformance suite drives against is a fresh, unconfigured, or otherwise empty library"
symptoms:
  - "test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds fails asserting code == ExitCode.OK on the final act"
  - "A gated verb's handler is correct against a real batch of work but fails the shared contract suite on the sample arguments chosen for it"
  - "A unit concludes its verb cannot land and parks the obligation elsewhere, when the actual fix is treating the empty case as a no-op"
related_components:
  - "cli_registry"
  - "gate_contract"
tags:
  - "conformance-3"
  - "gated-verb"
  - "empty-input"
  - "no-op"
  - "pending-human"
  - "sample-arguments"
---

# A gated verb driven on sample arguments over an empty library can never end on PENDING_HUMAN

## Context

U72 bound `crate intake land`, a verb gated behind `intake.land.confirm`. Its
real job, once a person answers apply, is to move files and end on
`Outcome.PENDING` with a `rekordbox_import` pending action, because the
import into rekordbox is a person's to do outside the tool. That is the
correct terminal state for a real landing.

`tests/test_cli_contract.py:_conformance_3` drives every gated entry in the
registry through its declared gates using `_sample_arguments`, and asserts
`code == int(ExitCode.OK)` on the drive that follows the final gate answer.
The fixture behind every entry in that parametrization is `configured`, a
freshly configured library with nothing acquired, nothing staged, nothing
downloaded. `_sample_arguments["intake.land"]` therefore points the verb at
`library.root / "Music"`, a folder that exists and is empty.

## The rule this makes

**A verb whose real engine can legitimately end on PENDING_HUMAN, or any other
non-OK terminal, must still exit OK when conformance 3 drives it, because
conformance 3's own input is always the empty-library case.** The suite does
not special-case verbs whose happy path is a pending action; it asks all of
them, uniformly, to reach OK after the gate is answered. A verb that would
correctly end on PENDING_HUMAN over a real batch has to look at what it was
actually handed, and when that turns out to be nothing, answer NO_OP instead.
That is not a workaround for the test: `name apply` and `route inbox` set the
same precedent independently, that an empty input state is a fresh install's
genuine state and must be reported as "nothing to do" rather than routed
through the outcome that real work would have produced.

`land_cli.py:_planned` is where U72 drew this line: a folder that exists and
lists no files becomes `landing.Plan(items=())` rather than being handed to
`landing.plan`, and `intake_land` checks `not planned.items` right after the
gate and returns `Outcome.NO_OP` before the engine, and before the
`PENDING_HUMAN`/pending-action branch, is ever reached.

## Why this is easy to miss

Nothing in the brief, the registry, or the gate machinery says this. A unit
author reading only the engine's own contract ("land files, then tell the
person to import them") has no reason to think about the empty case as
anything but a degenerate no-op that hardly matters. The trap is that
conformance 3 does not drive a verb over a realistic batch, it drives every
gated verb over the SAME minimal fixture, so the empty case is not a corner
of the contract, it is the entire contract as far as that test is concerned.
A verb designed only around its real, non-empty happy path will pass its own
unit tests and its own mutation table and still fail conformance 3, and the
fix is not to weaken the assertion or special-case the verb in the test, it
is to make the handler's empty-input branch answer OK (as NO_OP) the same way
every other gated verb's does.

## The general rule

When adding a new gated entry to `cli/registry.py`, before writing the
handler, ask what `_sample_arguments` will hand it and confirm that input
resolves to nothing to do. If the verb's natural empty-input behavior is to
raise, refuse, or route to a pending human action, add the same kind of early
check `land_cli._planned` uses: detect the empty case ahead of the engine and
return `Outcome.NO_OP` for it, leaving the pending-action or refusal path
reachable only when there is real work to report.

## See also

- `docs/residual-findings.md`, R-436, the neighboring finding from the same
  unit: naming `route.pending` as this verb's `verify_verb` proves nothing
  before the first tree cuts over, because that verb answers OK without
  opening anything until then.
- `src/cratekit/intake/land_cli.py`, the `_planned` docstring, which states
  the empty-folder-is-a-plan convention this rule generalizes from.
