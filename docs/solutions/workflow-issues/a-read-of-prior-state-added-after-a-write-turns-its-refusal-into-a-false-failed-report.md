---
title: "A read of prior state added after a write turns its refusal into a false failed report over a completed write"
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/analysis/cli.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "A verb that already writes something is extended to also read prior state, for example to report old and new values"
  - "The new read can raise a refusal"
tags: [refusal, partial-write, report, calibrate, u90]
---

# A read of prior state added after a write turns its refusal into a false failed report

## Problem

U90 added `analyze calibrate --vocal-cut N`, which reports the old and new cut. Reading the old cut can refuse, for example when the state file is unreadable. If that read raises after the write has already happened, the verb reports failure over a cut that was in fact written.

## Cause

A raised refusal means "nothing happened" to every caller and to the report. That holds only when the read comes before any write. Once a write has completed earlier in the same call, a raise from a later read contradicts the disk.

## What to do next time

- Put the prior-state read before the write, where a refusal is true, or
- If it must come after a write, record its failure as a per check failure inside the report, not as a raised refusal, so the report says the write landed and the read did not.
- Test it by making the read fail after the write and asserting the report still says the write happened.

Related: `a-refusal-raised-from-an-oserror-handler-loses-its-slug-to-path-permission-denied.md`, since an unreadable state file surfaces there as `path-permission-denied`, not its own slug.
