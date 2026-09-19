---
title: "A share gate fed a partial read moves its verdict both ways, so an unread release makes the label unknown, not smaller"
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/core/routing.py, the label approved verb"
problem_type: workflow_issue
component: gate_caller
severity: medium
root_cause: verdict_over_subset
applies_when:
  - "A caller hands a threshold gate a set built from reads that can individually fail"
  - "A gate that has never had a caller gets its first one"
---

# A share gate fed a partial read moves its verdict both ways

## Problem

U101 made `label approved` the first caller of `gate_decisions`, which holds a
label whose share of one genre family crosses a threshold. The first build
dropped releases whose genre could not be read and gated the rest. The built in
review found the share then depended on which releases happened to fail to read.

## Cause

The gate's share is a fraction of the set it is handed. Removing unread releases
shrinks the denominator, and that can push a label over the threshold (held when
it should be listed) or under it (listed when it should be held). Dropping
unread rows is not neutral, it is a claim that the label is only the releases
that were read.

## Next time

- A label with any release unread this run is unknown, not a smaller label. List
  it on a failing ungated line, never gate it on the readable part.
- The same rule covers no genre known and rows that disagree.
- The shipped Tidal catalogue carries no genre on an album or a track, so the
  gate cannot hold anything until a genre source is bound. Any unit that relies
  on the gate holding a release binds that source first. R-420 stays narrowed
  for this reason.
- See [[adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects]].
