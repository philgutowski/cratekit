---
title: "A closing paragraph under a ledger entry is not evidence that entry closed, and a triage brief goes stale"
date: 2026-09-21
category: workflow-issues
module: docs/residual-findings.md
problem_type: workflow_issue
component: development_workflow
severity: low
root_cause: inadequate_documentation
resolution_type: documentation_update
applies_when:
  - "Triaging residual ledger entries for what is already fixed in code"
  - "A brief cut from an earlier triage read lists entries to close or repoint"
---

# A closing paragraph under a ledger entry is not evidence that entry closed

## Problem

U106 (issue #151) closed ledger entries that were fixed in code. Two things did not match the brief. The closing paragraph dated the fourth attended sitting sat under R-147, but its content closed R-144. And the brief said R-130 had no pointer to R-403, but R-130 already had one.

## Cause

Closing paragraphs are appended at the end of a region and can land under the neighbouring entry. A CLOSED heading inside an entry reads as that entry's status even when the text belongs to another. Briefs cut from a triage read record what was true on that day, and other work lands between the read and the run.

## Next time

- Read a closing paragraph against the entry's own closing condition before trusting it. R-147 stayed open because no AST check of requires keys exists, while R-144 gained a pointer to the paragraph that closed it.
- Re-verify every candidate in a triage brief against the ledger and `src` before editing. Leave it open with a line saying what was checked if the check fails.
- The ledger is append only, so fix a misfiled paragraph with a pointer, never by moving it. Numbers never move.
