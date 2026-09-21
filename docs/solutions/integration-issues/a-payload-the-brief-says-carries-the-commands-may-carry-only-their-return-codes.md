---
title: "A payload the brief says carries the commands may carry only their return codes"
date: 2026-09-21
category: integration-issues
module: src/cratekit/backup/cli.py
problem_type: integration_issue
component: development_workflow
severity: medium
root_cause: wrong_api
resolution_type: code_fix
applies_when:
  - "A brief says to persist an existing report or payload so a person can read what ran"
  - "A reader has to tell an unreadable directory from an empty one"
tags: [backup, rclone, outcome-payload, job-show, glob, iterdir, r-349]
---

# A payload the brief says carries the commands may carry only their return codes

## What looked true

The R-349 brief said to persist `backup.outcome_payload(outcome)` and print it
from `job show`, so a person could read which rclone argv ran. It assumed the
payload already held the argv.

## What is true

`PortionOutcome` kept only each `CommandResult` return code, with no record of
which `Command` produced it. Persisting the payload alone would have written a
file that still could not answer the question the card was opened for. The
outcome had to grow the argv paired with each return code first.

Before writing a persistence unit, read the producer's type and confirm the
field the reader needs exists on it. A "persist X" brief is only as good as X.

## A second trap, in the reader

On Python 3.12, `Path.glob` yields nothing for a directory it cannot read.
A reader of the failure state directory that must distinguish an unreadable
directory (report it) from an empty one (nothing to show) cannot use `glob`.
List with `iterdir` inside the `try`, so the `OSError` reaches the handler.

## Related

The failure channel is separate on purpose. Routing a refusal through
`jobs.Produced` would complete the item DONE, so a resume would report success
over a half backup. See [a queued worker's report does not reach its resume
envelope](a-queued-workers-report-does-not-reach-its-resume-envelope.md).
