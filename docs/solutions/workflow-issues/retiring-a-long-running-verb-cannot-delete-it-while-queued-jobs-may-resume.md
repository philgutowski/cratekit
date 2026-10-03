---
title: Retiring a long running verb cannot delete it while jobs queued under its key may resume
date: 2026-10-03
category: workflow-issues
module: src/cratekit/label/cli.py, src/cratekit/cli/registry.py
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - A unit retires or replaces a verb that queues background jobs
  - The brief says "removed, or reduced to a refusal" and either looks equivalent
tags:
  - retire-verb
  - job-resume
  - argv-builder
  - registry
---

# Retiring a long running verb cannot delete it while jobs queued under its key may resume

## Problem

U109 (#248) retired `crate sync labels` in favour of the guided `crate label sync`.
The brief allowed "removed, or reduced to a refusal". Removal looks cleaner, but a
labels sweep queued before the change must still resume or be refused with a
remedy, never silently dropped.

## Cause

`crate job resume` does not read the job's own record to restart it. It rebuilds the
job's argv through the registry entry's `argv_builder` and spawns the verb. Delete
the entry and a job queued under its handler key has nothing to respawn through.

## What to do next time

Reduce, do not delete. U109's shape: without `--job` the verb refuses
`verb-retired` and names the replacement, with `--job` it resumes the old sweep.
The cost is that the entry keeps its `long_running`, `destructive` and write
declarations and its doctor checks, so a retired verb stays in `crate --help` and
in doctor's readiness. That residual is filed as R-885. Remove the entry only
after a check that no job is queued under its key, and pin both paths with tests
(refusal without `--job`, resume with it).

Related: the refusal's text must also reach the raised-cause exit, see
`a-queued-verb-has-two-exits-and-an-advisory-on-the-envelope-only-reaches-one.md`.
