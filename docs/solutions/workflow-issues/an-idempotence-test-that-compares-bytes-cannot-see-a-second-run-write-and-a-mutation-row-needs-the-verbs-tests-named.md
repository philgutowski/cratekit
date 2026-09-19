---
title: "An idempotence test that compares bytes cannot see a second run write, and a mutation row over label/cli.py must name its tests"
date: 2026-09-19
category: workflow-issues
module: src/cratekit/label/cli.py
problem_type: workflow_issue
component: testing_framework
severity: medium
resolution_type: workflow_improvement
applies_when:
  - "A verb promises that a run which adds nothing writes nothing, and a test pins that by comparing file bytes"
  - "A mutation row targets src/cratekit/label/cli.py"
symptoms:
  - "The mutation that removes the write skip kills zero rows although the idempotence test is green"
  - "A mutation over the verb's code runs the suite subset and reports the row survived because the verb's own test file was never selected"
tags:
  - mutation-testing
  - idempotence
  - registry-adopt
  - mutation-table
  - test-fidelity
---

# An idempotence test that compares bytes cannot see a second run write, and a mutation row over label/cli.py must name its tests

## Problem

U100 added `label registry adopt`, which must write nothing when it adds nothing.
The test ran adopt twice and compared the registry file's bytes after the second
run with the bytes after the first. The row that deleted the "skip the write when
nothing was added" guard killed zero.

## Cause

Two separate causes.

1. Saving an unchanged registry produces the same bytes. Equal bytes prove the
   content did not change, not that the second run declined to write. The test
   could not tell a skipped write from a rewrite of identical content.
2. The mutation driver derives the tests to run from what they import. No test
   imports `cratekit.label.cli` to reach the verb, so the derived subset never
   includes the verb's own test file, and every row over that module silently
   ran the wrong tests.

## What to do next time

- To pin "a run that adds nothing does not write", observe the write itself, not
  the result of it. Either count saves through a spy at the seam, or make the
  fixture hold something the loader drops, so a rewrite changes the bytes and a
  skip does not. U100 used the second, and the row then died.
- In any mutation row over `src/cratekit/label/cli.py`, name the test files
  explicitly instead of relying on the import derived subset.
- Related: [a zero death row can be a test gap or an inert mutation](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md).
