---
title: "A guard that reads a flag defaulting to false treats every raise site that never set it as having proven it"
date: 2026-09-22
category: workflow-issues
module: "src/cratekit/core/jobs.py, src/cratekit/backup/cli.py, src/cratekit/core/cause.py"
problem_type: workflow_issue
component: jobs
severity: high
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A new guard refuses or performs on a boolean field that has a default"
  - "The field was informational before the guard, read by a message and nothing else"
  - "Raise sites across several modules build the same cause type and most do not set the field"
  - "A test suite re-arms, resumes or retries after a fake failure in more than one worker suite"
symptoms:
  - "A unit that adds the guard reddens tests in suites it never touched, all on the new refusal"
  - "A worker whose failure is plainly transient, a dropped connection, is refused a resume as permanent"
  - "The fix looks like rewriting those tests to the refusal, and the product loses a path it had"
related_components:
  - "jobs"
  - "backup"
  - "causes"
  - "retryable"
tags:
  - "retryable"
  - "default"
  - "guard"
  - "resume"
  - "raise-site-sweep"
---

# A guard that reads a flag defaulting to false treats every raise site that never set it as having proven it

## Context

R-380 made the job cause read the items' `retryable` flags, 2026-09-18. R-390
made `jobs.retry` refuse a job whose cause says `retryable` is false,
2026-09-22. Between the two, the flag went from a word in a message to the
thing that decides whether a resume happens at all.

## What happened

`Cause.retryable` defaults to false, and so does `refuse`'s. Before R-390
nothing performed on it, so a raise site that never set it cost nothing. The
refusal landed and eleven tests in six suites the unit never touched met it,
every one a fake failure followed by a re-arm through `jobs.retry`.

Read one at a time, six were fakes that raised a `RuntimeError` or a refusal
with the flag unset to model a dropped connection, and the fake was what was
wrong. Three were the backup shell's own transfer refusal,
`backup-transfer-failed`, built by `refuse` with the flag unset. A dropped
connection mid mirror had been recorded permanent since R-380, the job had
said resume could not succeed, and the new refusal made the verb agree. The
per portion ledger the backup job exists for could never be used, and the
first draft of the unit rewrote those three tests to assert the refusal,
which is the product losing a path it had with a green suite to show for it.
The built in review named it and the flag was set at the raise site.

## Why the source does not explain it

The raise site is correct on its own terms: a slug, a message, a reservation
with a remedy. Nothing at the site says the flag is now load bearing, and the
guard that made it so is in another module. The default hides the difference
between "this failure is permanent" and "nobody said", and a guard reads
both as the first.

## The rule

**Before a guard performs on a field with a default, sweep every raise site
the guard will govern and sort them into the ones that set the field and the
ones that never did.** The second group is not evidence of anything. For each
one, decide at the raise site whether the default is the honest value, and
set it explicitly where it is not, in the same unit as the guard. A test that
reddens on the new guard in a suite the unit never touched is the sweep
arriving late; read the fake for what it models before rewriting the test to
the refusal, because a refusal test over a transient failure pins the loss.

The sweep is a grep for the cause constructor and for `refuse(` across
`src/`, filtered to the sites whose failures reach the guard. For
`jobs.retry` that is every worker's item failure. Two remain permanent by
their module's own choice and are R-656.
