---
title: "A worker's report write clears its own staging, so evidence written earlier in the same attempt is gone"
date: 2026-11-05
category: integration-issues
module: src/cratekit/analysis/artifacts.py
problem_type: integration_issue
component: development_workflow
severity: high
root_cause: wrong_api
resolution_type: code_fix
applies_when:
  - "A job worker writes a file beside its staged report so a resume can read it"
  - "A worker acts on disk (a rename, a move) before it returns its Produced"
tags: [jobs, workers, resume, staging, artifacts, rename-intent, interrupt, u223, a60]
---

# A worker's report write clears its own staging, so evidence written earlier in the same attempt is gone

## What looked true

`intent_path` said the rename intent "outlives a kill" and that
`staged_path` clears it "on the next attempt, which is after the resume has
read it". A kill test passed: it died before `produced` was called.

## What is true

Every `artifacts.produced` call runs `staged_path`, which cleared the item's
whole staging directory before writing the report, and `produced` is the last
thing the worker does, after the rename. So the intent lived only until the
same attempt finished. The window that loses it is not a rare kill: it is
`jobs.drive`'s interrupt checkpoint, which releases a produced item
uncommitted whenever a Ctrl-C landed during the handler's work, the seconds a
decode takes. A60's live run hit it on its first try.

## What to do

Anything a resume must read lives where the report write cannot clear it
(`staged_path` now keeps `rename-intent.json`), and is removed only where it
is known false. Test a resume window with a real signal through the engine's
own checkpoint after `produced` returns, not only with a raise before it:
the two leave different files on disk. The other artifacts copies under
`core`, `tagging`, `adopt` and `sync` still clear the whole directory; that is
safe only while no worker of theirs writes beside its report.
