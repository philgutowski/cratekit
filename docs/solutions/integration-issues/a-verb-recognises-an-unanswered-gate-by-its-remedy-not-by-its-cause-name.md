---
title: A verb recognises an unanswered gate by its remedy, not by its cause name
date: 2026-09-23
category: integration-issues
module: "src/cratekit/intake/land_cli.py"
problem_type: integration_issue
component: cause_vocabulary
root_cause: wrong_api
resolution_type: code_fix
severity: low
symptoms:
  - "A modules layer verb that imports cratekit.cli.gates to detect an unanswered gate fails the layering test"
  - "A verb that spells decision-required as a string literal grows the pinned at-risk population and fails tests/test_reserved_causes.py"
applies_when:
  - "A verb must tell a gate that still wants an answer from a refusal it should surface itself"
tags:
  - "gates"
  - "cause-vocabulary"
  - "reserved-causes"
  - "layering"
---

# A verb recognises an unanswered gate by its remedy, not by its cause name

## Problem

R-677 moved the export check onto the `crate intake land` plan read, so a
refusal replaces an unanswered gate but a recorded answer is still honored. The
verb has to know whether the gate is unanswered. The obvious routes both fail.

## Cause

Verbs in the modules layer may not import `cratekit.cli.gates`. Writing the
cause name `decision-required` as a string literal in a verb adds a member to
the at-risk population that `tests/test_reserved_causes.py` pins, and the suite
fails.

## What to do next time

Read the refusal's remedy. Compare against `Remedy.ANSWER_DECISION` from
`core.cause`, which a verb may import and which names the same condition
without holding a reserved cause string.

Related: [the reserved binary keys are remedy tokens](the-reserved-binary-keys-are-remedy-tokens-not-reasons-a-verb-can-refuse-with.md).
