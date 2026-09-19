---
title: "A verb's nothing-to-do answer that a pending check reads as proof of import must not double as the answer to a failed run"
date: 2026-09-18
category: workflow-issues
module: "src/cratekit/write/routing_cli.py, src/cratekit/write/trees.py"
problem_type: workflow_issue
component: pending_action_check
severity: high
root_cause: ambiguous_zero
applies_when:
  - "A verb ends on a rekordbox_import pending action whose check treats a re-run inserting nothing as proof the import landed"
  - "A new path can insert nothing for a reason other than having already succeeded"
---

# A nothing-to-do answer that a pending check reads as proof must not double as a failure

## Problem

`route inbox --export X` (U86, issue #131) is idempotent: a second run over its own output inserts nothing. The pending action's check reads that same "inserted nothing" as evidence the import landed. Two paths also inserted nothing without having succeeded: writes the export's tree could not take, and files that could not be read before any write. On those, a failed run gave the same answer as a finished one and passed as a completed import. The code review found the writer path and the read path had the same defect.

## Cause

One answer, zero inserted, carried two meanings, "already done" and "could not do". Nothing in the code shows the pending check depends on that distinction, so each new early exit looks harmless.

## Next time

When a verb's idempotent no-op answer is also what a pending check reads as success, list every path that inserts nothing and give each non-success one a distinct, refusing answer (a warning or a failure), before any write happens. Test each early exit against the pending check, not just against the verb's own output. Related: [[a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence]], [[adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects]].
