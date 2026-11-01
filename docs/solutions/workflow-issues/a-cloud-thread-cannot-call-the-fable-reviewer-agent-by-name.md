---
title: "A cloud thread cannot call the fable-reviewer agent by name, so the review runs as a general agent on Fable reading the agent file"
date: 2026-11-01
category: workflow-issues
module: ".claude/agents/fable-reviewer.md, cloud-unit"
problem_type: workflow_issue
component: development_workflow
severity: low
root_cause: undocumented_tool_behavior
resolution_type: workaround
applies_when:
  - "A cloud build thread reaches the review step of the cloud-unit skill"
  - "The Agent tool lists claude, Explore, general-purpose and Plan, and no project agent"
symptoms:
  - "Asking for the fable-reviewer agent type answers that the type is not found"
tags:
  - "fable-reviewer"
  - "cloud-lane"
  - "review"
  - "r1091"
---

# A cloud thread cannot call the fable-reviewer agent by name

## Problem

The cloud-unit skill says to run the `fable-reviewer` agent on the branch.
In a project build thread on 2026-11-01 (R-1091) the Agent tool refused the
type: only the built in agents were registered, and the repository's own
agent files were not loaded. R-1056's record met the same and said so in a
sentence, which is where the next session would not look.

## What works

Start a `general-purpose` agent with the model set to `fable`, and make its
first instruction to read `.claude/agents/fable-reviewer.md` and follow it as
its definition: the reading, driving rather than arguing, the hunting order
and the report form. Pass the branch, the card number, what the branch does,
the deliberate choices worth challenging, the container's rules (targeted
test files, the baseline of machine failures, leave the tree as found,
scratch under `/tmp`) and, for round 2, what round 1 found and what the fix
commit was. Run it in the background and start nothing against the tree
until it reports, since it mutates files to drive its findings.

Both rounds of R-1091 ran this way, found one blocking finding in round 1
that a green suite had hidden, and left the tree clean each time.
