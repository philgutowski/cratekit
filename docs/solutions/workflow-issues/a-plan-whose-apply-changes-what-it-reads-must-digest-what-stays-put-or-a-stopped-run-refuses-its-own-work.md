---
title: "A plan whose own apply changes what it reads must digest what stays put, or a stopped run refuses its own work"
date: 2026-10-02
category: workflow-issues
module: "src/cratekit/adopt/plan.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "A plan lists only the changes still to make, and the apply moves some of them into the state the plan reads"
  - "The approval is a digest over the plan, as adoption's gate is"
tags: [digest, gate, adopt, vocal, idempotence, r-788, r-758]
---

# A plan whose apply changes what it reads must digest what stays put

## Problem

R-788 made `adopt apply` file vox tagged tracks under a bucket's `with vox` sub. If the digest covered only the memberships still to add, a run that stopped partway would re-plan with fewer rows, produce a different digest, and refuse its own earlier approval as a stale decision.

## Cause

The plan reads the tree it is about to write to. Each membership applied moves from "to add" to "already present", so a digest over only the "to add" rows shrinks as the apply proceeds. The move verb hit the same shape under R-758.

## Next time

Digest every membership an apply may write, present or not, and have the gate list both groups, each saying whether the tree already holds it. The digest then stays equal before, during and after a partial run. Test it directly: the digest must change when a membership is added to the plan, and must not change when one already present is applied.

Related: R-841 is open on which signal owns the vocal sub, the tag row (adoption) or the file's score (routing derivation). Settle that before touching vocal filing again. Adoption approvals given before this build are stale once, since the digest gained two keys.
