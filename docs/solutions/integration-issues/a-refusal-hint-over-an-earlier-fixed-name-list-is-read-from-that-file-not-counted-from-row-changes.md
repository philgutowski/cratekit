---
title: "A refusal hint over an earlier fixed name list is read from that list's file, not counted from how rows changed since"
date: 2026-09-19
category: integration-issues
module: "src/cratekit/intake/missing_cli.py"
problem_type: integration_issue
component: intake
severity: low
root_cause: unverified_assumption
applies_when:
  - "A listing verb refuses to overwrite a job's fixed name list and tells the person why"
  - "The hint would say what changed in the rows since the job ran"
tags:
  - "intake-missing"
  - "fixed-name-list"
  - "refusal"
  - "offered-rows"
  - "review-answer"
---
# A refusal hint over an earlier fixed name list is read from that list's file, not counted from how rows changed since

## Problem

R-503 made an offered row listable once its review item was answered. The listing
verb then refused when the job's fixed name list already existed, and the first
attempt at its hint counted how many offered rows had changed since the job ran.
That count is wrong, because nothing records when the earlier list was written.
Rows answered before the list was written and rows answered after look the same.

## Cause

The row state and the list file have no shared timestamp. Any number derived from
row changes describes the rows now, not what the earlier list holds.

## What to do next time

Read the earlier list file itself and compare against it. The code review found
this in R-503's refusal step and the fix reads the file. Apply the same rule to
any hint on a fixed name refusal, in particular R-476 and R-508.

Related: [[a-list-named-from-its-identifiers-meets-the-emitters-whole-file-comparison]].
