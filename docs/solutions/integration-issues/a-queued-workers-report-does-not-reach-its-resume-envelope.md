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
tags: [jobs, workers, resume, envelope, warnings, rebuild, artifacts, item-report, r-316, r-312]
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

## Corrected 2026-09-21, by the R-312 fix: the channel exists, and it is the item report

The section above says a value that depends on what the item read "needs a
channel that does not exist today". That was wrong when it was written, and it
cost the R-312 fix a whole first version.

The channel is the item report. `Produced` IS described above as "the durability
channel for an artifact and nothing else", and an artifact is any JSON a worker
cares to write: `core.artifacts.produced(where, cfg, job, item, report)` stages
it, the driver commits it before the item flips to done, and
`core.artifacts.committed(where, cfg, job_id)` reads every item's report back in
order. The tagging, adoption, outbound, analysis and intake workers all report
this way already. Returning one changes neither the worker contract nor
`jobs.drive`.

The R-312 fix read this file first, believed it, and kept the engine's
measurement in a module level dict that the resume drained. The built in review
named the two runs that loses. A job that fails part way leaves through its
cause, and a refusal envelope has no warnings, so the advisory has to be a step
on the cause as well, which is
`workflow-issues/a-queued-verb-has-two-exits-and-an-advisory-on-the-envelope-only-reaches-one.md`.
And a driver that dies takes the dict with it, while the items it finished stay
done. The resort worker now returns its tree's leftovers as its item report and
the resume reads them back on both exits.

So, before promising a surface a value from a worker: if the value does not
depend on the library, ask the engine, as R-316 did. If it does, return it as
the item's report. Do not re-run the comparison, and do not hold it in memory.
The rebuild worker still returns None, R-635, and R-443 closes the day it stops.
