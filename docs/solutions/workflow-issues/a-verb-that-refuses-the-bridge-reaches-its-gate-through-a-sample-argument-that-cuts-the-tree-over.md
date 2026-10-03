---
title: A verb that refuses a bridge intake tree reaches its conformance gate through a sample argument that cuts the tree over
date: 2026-10-03
category: workflow-issues
module: "tests/test_cli_contract.py, src/cratekit/intake/rotate_cli.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: missing_workflow_step
resolution_type: test_fix
applies_when:
  - "A new gated verb works on a database native tree only and refuses a tree on the xml bridge"
  - "Conformance 3 fails because the verb refuses with tree-unconverged before its gate"
  - "UNREACHABLE_GATES looks like the way to a green conformance run"
symptoms:
  - "test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds fails with an exit that is neither OK nor DECISION_REQUIRED"
  - "Adding the gate to UNREACHABLE_GATES does not help, since the drive still has to reach OK"
tags:
  - "conformance"
  - "explicit-gate"
  - "database-native"
  - "sample-arguments"
---

# A database native verb reaches its conformance gate through a sample argument

## Context

`crate inbox rotate` (U111) works only on an intake tree that has cut over,
and the brief requires it to refuse a bridge tree naming `tree cutover`. The
conformance fixture, `configured` in `tests/test_cli_contract.py`, has every
tree on the bridge. Conformance 3 drives each gated verb until it exits OK and
accepts DECISION_REQUIRED along the way and nothing else, so a refusal before
the gate fails it.

## Why the exemption map is not the answer

`UNREACHABLE_GATES` exempts a GATE from having to fire, not a verb from having
to reach OK. The native landing's gates sit there because the same verb
reaches OK on the bridge through its other gate. A verb with no bridge medium
still refuses on the fixture with every gate exempt. The map is also pinned by
`EXPECTED_UNREACHABLE_GATES`, where a new entry is a decision.

## What works

`_sample_arguments` accepts a CALLABLE, evaluated under the `configured`
fixture each time the verb is driven. `_intake_cut_over` gives the fixture's
database an INBOX root through `cutover_fixtures.one_root`, records the intake
tree database native in the tree registry, and returns no arguments. The verb
then plans an empty INBOX, asks its explicit gate, and reaches OK by the two
acts. The gate is really reached, and the bridge refusal is driven in the
verb's own suite. A verb that reads the acknowledgment first also goes in
`ACKNOWLEDGED_BEFORE_THE_GATE`, as the neighbouring entry on the gated write
verb says.

## Related

`a-new-gated-write-verb-has-to-reach-its-gate-on-the-conformance-fixture.md`,
the order such a verb keeps.
