---
title: "A queued worker's report does not reach its resume envelope"
date: 2026-09-19
category: integration-issues
module: src/cratekit/core/jobs.py
problem_type: integration_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - "A verb's resume has to report something its worker's engine call returned"
  - "A brief says a resume should read a report 'the job already wrote'"
tags: [jobs, workers, resume, envelope, warnings, rebuild, r-316]
---

# A queued worker's report does not reach its resume envelope

## What looked true

The R-316 brief said the rebuild resume should read `not_compared` from "the
ConvergenceReport the rebuild already wrote". It reads as if the report were
stored somewhere a resume could open.

## What is true

Nothing stores it. A worker is `handle(job, item, cfg) -> Produced | None`, and
`Produced` is a staged file and its final path, the durability channel for an
artifact and nothing else. `jobs.drive` keeps no per item result, and
`handlers.run_job` hands the verb a `DriveResult` holding counts and a job. So
whatever the engine returns to the worker, `RebuildReport` included, is gone
when the item completes. The only way back from a worker to its verb's
envelope is a file, a database row the verb then reads, or a warning the verb
works out for itself.

## What to do

Before promising a surface a value from a worker, check whether the value
depends on the library at all. The vocal gap does not: it is a function of the
declaration and the threshold, so the resume asks
`rebuild.governed_not_compared()` and gets the same answer with no input or
output, pinned against the derivation by
`test_the_gap_rule_is_the_derivations_own`. A value that DOES depend on what
the item read, a count or a difference list, needs a channel that does not
exist today: changing the worker's return or `jobs.drive`, which is a unit of
its own. Re-running the comparison in the resume is the tempting third option.
It walks the whole library a second time and can refuse after a job that
succeeded. R-443 records the choice and when it stops holding.
