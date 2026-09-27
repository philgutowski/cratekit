---
title: "A refusal's steps are claims about other verbs, so drive them in the order a person would"
date: 2026-09-27
category: workflow-issues
module: "cratekit.adopt.apply_cli, cratekit.core.jobs, cratekit.cli.cutover"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - "A refusal is gaining a step that names another verb"
  - "The refusal is raised inside a queued job's worker"
  - "The step tells a person to resume or retry the job that refused"
symptoms:
  - "A step reads correctly and the verb it names refuses when it is followed"
  - "crate job resume answers job-not-retryable on the job a refusal told a person to resume"
related_components:
  - "tooling"
tags:
  - "remediation"
  - "job-resume"
  - "retryable"
  - "cutover"
---

## The trap

R-235 was a refusal naming a remedy nobody could perform. The unit that closed
it wrote the remedy as two steps on the adoption refusal: cut the tree over,
then resume this job. The second step was false, and it was written by the
session whose whole brief was a false remedy.

A worker that raises fails its item, and a job whose every item failed ends
FAILED. `crate job resume` reads the job's cause, and a cause with
`retryable` False, which is the default every `refuse` takes, is refused
`job-not-retryable` with nothing re-run. The cutover did not change that: the
cause was recorded when the job failed, and it says what was true then. The
step that works is the verb again, `crate adopt apply`, which queues a new job.
Nothing was lost by the first one, because the ledger is marked last.

The built in review asked a different question, whether the step covered every
precheck, and the test written to answer it drove the steps in order and met
the refusal.

## The rule

A step that names a verb is a claim about that verb's behaviour in the state
the refusal leaves behind. Drive it: reach the refusal, perform each step as
written, in order, through the real dispatcher, and assert the last one ends
OK. `tests/test_cutover_cli.py`
`test_the_steps_the_refused_adoption_names_are_the_steps_that_work` is the
shape.

Before writing "resume this job" on a refusal raised inside a worker, check
the cause's `retryable`. If the cause is not retryable the job is over, and
the step is the verb that queued it.

## Related

`docs/residual-findings.md` R-235, and `core/jobs.py` `retry`, which is where
the resume is refused.
