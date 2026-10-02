---
title: A new gated write verb has to reach its gate on the conformance fixture, which decides where it opens the database and what an empty plan does
date: 2026-10-01
category: workflow-issues
module: "tests/test_cli_contract.py, src/cratekit/tagging/rows_cli.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - "A new verb declares an explicit gate and writes database rows"
  - "The handler is being ordered: when to open the database, when to read the acknowledgment, when to ask"
  - "The plan can be empty on a library that needs nothing"
  - "An entry in UNREACHABLE_GATES looks like the quick way to a green conformance run"
symptoms:
  - "test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds fails for the new verb with app-version-pin-unrecorded, exit 23 where 10 was expected"
  - "The same test reports the verb declares a gate its handler never reached"
  - "test_the_unreachable_exemption_set_is_exactly_the_intended_one goes red when a gate is added to the exemption map"
related_components:
  - "testing_framework"
tags:
  - "conformance"
  - "explicit-gate"
  - "write-intent"
  - "empty-plan"
  - "backup-acknowledgment"
---

# A new gated write verb has to reach its gate on the conformance fixture

## Context

`crate tag rows` (R-816, built on `relay/239`) was first ordered the way the
native landing is, `intake.land_cli.ask_then_write`: open the database with
write intent, plan, read the backup acknowledgment, ask the gate, write. A plan
that wrote nothing returned a no op without asking. That order passed 45 tests
of its own and failed conformance 3, and the fix was a restructure, not a pin.

## What conformance 3 holds a verb to

`tests/test_cli_contract.py` drives every landed verb that declares a gate on
ONE shared fixture, `configured`, and asserts that every declared gate fired
and that the verb then reached exit OK. Three properties of that fixture
decide the order of a new handler, and none is visible from the handler.

1. **The fixture records no application pin.** `rb_writer.open_db` with
   `require_closed=True` refuses `app-version-pin-unrecorded` there. A verb
   that opens the database to write BEFORE its gate never reaches the gate on
   the fixture. The native landing gets away with it because its native gates
   are exempt for another reason, the fixture's intake tree is on the bridge.
2. **The fixture's two rows record no path.** Any plan over files is empty
   there. A verb that skips its gate on an empty plan never asks on the
   fixture.
3. **The fixture has no backup acknowledgment.** A verb that reads the
   acknowledgment before its gate (R-733) is refused ahead of it, unless the
   verb is named in `ACKNOWLEDGED_BEFORE_THE_GATE`, which requires a named
   test that drives the refusal elsewhere.

The way out that looks cheap is an entry in `UNREACHABLE_GATES`. That map is
pinned by `EXPECTED_UNREACHABLE_GATES` with the sentence "a fourth one is a
decision, not a diff", so it is red by design and it is not a session's call.

## The order that passes with no exemption

It is the one `adopt move`, `adopt apply` and `tag retag` already keep.

- Read the backup acknowledgment first, before the plan.
- Build the plan on a handle opened to READ (`require_closed=False`) and close
  it. What the plan returns must be values, so nothing mapped outlives the
  handle.
- Ask the gate over the digested plan, and ASK ON AN EMPTY PLAN TOO. Then
  return a no op when the plan writes nothing, without opening anything.
- Only on `apply` over a plan that writes, open the database with write
  intent. Because the plan and the write are now on two handles, the engine
  checks each row is still as the plan read it before it writes.
- Add the verb to `_sample_arguments` and to `ACKNOWLEDGED_BEFORE_THE_GATE`,
  naming the test that drives the verb with no acknowledgment.

## Also pinned, and found the same way

Adding a verb that writes rows moves four more pins, each of which names what
to do in its own failure message: the kebab literal population and the at risk
module count in `tests/test_reserved_causes.py`, the set of functions that
take a capture in `tests/test_write_session.py`, and the set of modules that
read the soft delete marker in `tests/test_rb_writer_guard.py`. The last one
is a real guard and not a count: read a tombstone through
`trees.soft_delete_marker` and never off a SQL row.

## Related

`src/cratekit/tagging/retag_cli.py`, "AN EMPTY SELECTION STILL ASKS", which
records the empty plan half of this from the unit that met it first.
