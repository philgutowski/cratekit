---
title: "The built in /code-review checks out main in the shared working tree mid run, so a battery started alongside it can run over an unknown mix of branches"
date: 2026-09-11
category: workflow-issues
module: relay
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: undocumented_tool_behavior
resolution_type: sequencing_change
applies_when:
  - "A relay task or session runs the built in /code-review and the battery in the same working tree"
  - "Anything else is launched in parallel with /code-review against a branch checkout"
  - "A registry or file count taken mid session disagrees with a count taken right after review"
symptoms:
  - "A battery run alongside /code-review passes or fails in a way that does not reproduce afterward"
  - "The working tree is briefly on main when nothing in the session's own commands checked it out"
  - "A count of registry entries taken during review differs from the same count taken moments later"
tags:
  - "code-review"
  - "relay"
  - "working-tree"
  - "concurrency"
  - "battery"
  - "sequencing"
---

# The built in `/code-review` checks out main in the shared working tree mid run

## Context

Relay task 42 (closing R-5, `docs/residual-findings.md`) ran the built in
`/code-review` as a forked agent against the working tree the task's branch was
checked out in. To count the verb registry, that forked agent ran `git checkout
main`, did its counting, and checked the branch back out when it was done. This
is not documented anywhere the task could have read in advance; it is something
the review tool does to itself, invisible from this repository's own code.

The task had also started the battery (`ruff`, `pytest`, `scan_repo.py`) in
parallel with the review, on the assumption that review and battery touch
different things and do not need to be sequenced. Because both run against the
same working tree rather than each in its own checkout, the battery's run
window overlapped the review's `git checkout main` and back, so the battery
result could have been produced against `main`, against the branch, or against
a moment mid switch, and there is no way after the fact to know which. The
result was not trustworthy even though nothing threw an error.

Separately, the same review pass overcounted destructive verbs by three,
because it counted a combined listing of "adjudicating or destructive" entries
rather than filtering to the destructive flag alone. That count is corrected in
`4fcd9e7` and is a one-line reminder rather than a pattern: count each registry
flag on its own, not a union of flags that happens to look like the one you want.

## Guidance

**Run `/code-review` and the battery in sequence, never in parallel, in the same
working tree.** The battery's own instruction in `CLAUDE.md` already says to run
it "from inside the checkout that holds the branch"; the addition here is that
`/code-review` is not a read only bystander to that checkout while it runs.
Treat any built in reviewer the same way until proven otherwise: assume it may
touch the working tree's checked out ref, not just read files, and do not treat
"they read different things" as license to run it alongside anything else that
depends on the ref not moving.

**After a review pass that ran in the same tree, confirm the branch before
trusting anything that ran alongside it.** `git status` or `git branch
--show-current` costs nothing next to re-running a battery that may have run
over the wrong tree.

## When to Apply

- Before parallelizing any two steps of the pipeline in `docs/METHOD.md` inside
  one working tree, check whether either step is documented to touch the
  checked out ref, and when it is undocumented, assume it might.
- When a relay task or session reports a battery or count result that looks
  right but was produced while another tool was also running against the same
  checkout.

## Related

- `docs/METHOD.md`, step 4 (Review) and step 6 (Merge): the canonical pipeline
  already runs these in sequence, not in parallel. This entry is the reason
  that ordering is load bearing, not just convention.
- `docs/residual-findings.md`, R-5 and R-335: R-5 closed in this task; R-335
  records the separate, still open gap that neither the review queue nor the
  doctor conformance assertion drives a landed verb through the dispatcher.
- Commit `4fcd9e7`: the destructive verb count correction, twenty two of
  twenty four rather than twenty five of twenty seven.
