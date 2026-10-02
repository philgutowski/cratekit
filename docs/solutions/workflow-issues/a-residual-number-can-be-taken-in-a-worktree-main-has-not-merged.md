---
title: "A residual number can already be taken by a worktree's ledger that main has not merged"
date: 2026-10-02
category: workflow-issues
module: "docs/residual-findings.md"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_workflow_step
resolution_type: process_change
applies_when:
  - "A session is about to number a new R-N residual while an attended worktree exists under the repository"
tags: [residual-ledger, numbering, worktree, relay]
---

# A residual number can already be taken by a worktree's ledger that main has not merged

## Problem

Unit 244 (R-840) read the tail of `main`'s ledger and numbered its new residuals from the next
free number. The attended worktree under the repository already held R-846 on a commit `main`
did not have. Had the unit numbered from main's tail it would have reused R-846, and the two
branches would have collided at merge, the same renumbering cost recorded in
`renumbering-incoming-residuals-at-a-merge-moves-the-citations-too.md`.

## Cause

`main`'s ledger tail is the last merged state, not the last claimed number. Numbers are claimed
on whichever branch writes them first, and an attended worktree can sit ahead of `main` for
days. The unit caught it only because it happened to look at the worktree.

## What to do next time

Before numbering a residual, read the tail of the ledger in every worktree (`git worktree list`,
then the last `## R-` heading in each `docs/residual-findings.md`) as well as `main`'s, and
start above the highest. A unit that exits before its merge cannot create the issue for a
residual it filed, so say in the card comment that the issue is owed and must be titled with
the ledger heading exactly.

A related contract worth knowing: `review.redescribe` now accepts a function that receives the
open item's current payload under the write lock. Any writer that changes some fields of an
open item should use that form, so it cannot take back what another writer put on the item
between its read and its write.
