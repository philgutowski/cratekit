---
title: "A job cause that ignores item retryable tells a person to resume work that cannot succeed"
date: 2026-09-18
category: workflow-issues
module: "src/cratekit/core/jobs.py, src/cratekit/cli/jobs.py, tests/test_outbound_workers.py"
problem_type: workflow_issue
component: jobs
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "jobs.drive is wrapping item failures into a job level cause"
  - "Item rows already carry retryable false and a named permanent reason"
  - "A live run printed resume-job or retry later over those items"
  - "A test asserts the job cause is not internal-error, or is unavailable-transient, without reading the items"
symptoms:
  - "A label sweep whose failures are that the provider has no artist named for them tells the person to resume when the provider is reachable"
  - "The inner cause on the item is exact and final, and the job cause contradicts it"
  - "A test that forbids internal-error on the job cause stays green over the dishonest wrapper"
related_components:
  - "jobs"
  - "label-sweep"
  - "causes"
tags:
  - "retryable"
  - "job-cause"
  - "wrapper"
  - "resume-job"
  - "silent-failure"
---

# A job cause that ignores item retryable tells a person to resume work that cannot succeed

## Context

The first real `crate sync labels`, 2026-09-17, swept 15 of 47 labels and failed
the other 32 because the provider has no artist named for them. Each failed item
carried `sync-source-lookups-failed`, `retryable` false. The job reported
`unavailable-transient`, `retryable` true, remedy resume-job.

## What happened

`jobs.drive` always built the job cause through `_partial_failure_cause`, which
hardcoded the transient slug, the retryable flag, and the resume-job remedy, and
nested the last item's cause as `inner`. `evidence_or_raise` did the same for
the all failed envelope as `no-evidence`, `retryable` true. The item rows were
honest. The cause a person is told to act on did not read them.

R-266 described the same wrapping when the catalogue was unbound. The adapter
landed, so it stopped being every run. The wrapping was still the engine's
verdict on any job whose items failed for a permanent reason.

A test in `tests/test_outbound_workers.py` asserted the job cause was not
`internal-error`. The fake raises `RuntimeError`, which the item records as
`internal-error`. The assertion was true only because the wrapper hid that
reason behind `unavailable-transient`. Updating the engine to report the item's
own cause made that test fail for an honest reason.

## Why the source does not explain it

Nothing at the raise site on the worker looks wrong. The item cause is the
right slug and the right flag. The lie is one layer up, in the function that
turns "some items failed" into a job the person is told to resume. A suite that
pins the wrapper's slug, or that forbids `internal-error` on the job, will stay
green over that lie.

## The rule

**A job cause built from item failures has to read those items' `retryable`
flags.** If every failure is permanent, the job is not resumable, even when some
items succeeded. Nesting the honest cause as `inner` is not enough: the top
level flag and remedy are what a person and a script act on.

A test that forbids `internal-error` on a job cause is pinning the wrapper, not
the worker. Pin the item's reason, or pin `retryable`, not the absence of a
slug the wrapper used to hide.

`crate job resume` still re-arms failed items without reading `retryable`.
That remaining hole is R-390.
