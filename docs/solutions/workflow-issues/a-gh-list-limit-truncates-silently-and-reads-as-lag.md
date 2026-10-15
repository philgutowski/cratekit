---
title: "A gh list limit truncates silently, and the missing tail reads as lag"
date: 2026-10-15
category: workflow-issues
module: "scripts/board.py"
problem_type: workflow_issue
component: tooling
severity: medium
root_cause: silent_truncation
resolution_type: code_fix
applies_when:
  - "board.py audit reports cards as not on the board that are on it"
  - "a status reads None for a card whose status is set"
  - "any gh issue list or gh project item-list call carries a --limit"
tags: [board, audit, sync, gh, truncation, U148]
---

# A gh list limit truncates silently, and the missing tail reads as lag

## Problem

From 2026-10-13 `board.py audit` reported the newest cards as "is not on the
board" and "status is None, should be Done", though each was on project 2 with
its status set when read back by node. `sync` did not clear it. The watcher
record and a memory called it "the item list lag" and waited for it to clear.

## What it actually was

Both board reads asked `gh` for at most 300 rows, `gh issue list --limit 300`
and `gh project item-list --limit 300`. The project passed 300 items. `gh`
honours `--limit` by stopping, with no warning and no nonzero exit, so the
newest rows were simply absent from every read, and every read dropped the
same ones. A lag clears; a truncation never does. The tell is that the missing
cards are always the NEWEST, and that the count of missing ones equals the
project's `totalCount` minus the limit.

## Fix

U148: both reads ask for `READ_LIMIT` (5000), and refuse by name, as
`Truncated`, any read that fills it or comes back shorter than the count
GitHub gives (`totalCount` on the item payload, a GraphQL `issues.totalCount`
asked before the issue read). A read with no count to check is refused too.

## Applies elsewhere

Any `gh ... list --limit N` in a script is a silent ceiling. Search the
skills and scripts that read this board the same way before trusting their
counts, and the census commands in `docs/` (two carried 300 and were raised).
This is METHOD's first defect pattern: an absent row read as a row that does
not exist.
