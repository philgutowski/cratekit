---
title: "A residual waiting on somebody's decision may have been decided since, somewhere the ledger cannot see"
date: 2026-09-20
category: workflow-issues
module: "docs/residual-findings.md, src/cratekit/cli/registry.py, src/cratekit/setbuilder/cli.py"
problem_type: workflow_issue
component: documentation
severity: low
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - "A residual's closing condition reads 'closes when somebody decides'"
  - "The decision belongs to a shared table, the verb registry, the state inventory, the cause table"
  - "Weeks of units have landed since the residual was filed"
tags: [residuals, registry, writes, state-files, setbuilder, R-188]
---

# A residual waiting on a decision may have been decided elsewhere

## Problem

R-188 said the set builder could not fill its declared index cache until
"somebody decides whether a state-file write is a `writes` surface at all", and
called that a registry decision above a shell unit. Read alone, that is a stop
for an unattended session: the decision is a person's, so record the options
and pick the conservative one, which is to leave the cache off.

## What was actually true

The registry had decided it thirteen days after the residual was filed. The
unit that landed `analyze.calibrate` writes two library scoped state files,
declares no write surface, and says why in a comment on its entry: `writes`
names the library's own material, files, database and XML, and a calibration is
none of those. Nobody went back to R-188, because nothing connects a comment in
`registry.py` to a ledger entry that never names that verb.

## The rule

Before treating a "somebody decides" residual as blocked, grep the shared table
it names for a later entry that already lives under the answer:

    git grep -n 'state file\|Not in ``writes``' -- src/cratekit/cli/registry.py
    git log -S'<the phrase>' --format='%h %ad %s' --date=short -- <the table>

A shipped precedent with a recorded reason IS the decision. Follow it, cite it
in the closing note with its date, and do not invent a second answer. If the
grep finds nothing, the residual is still a stop.

## The second half, which cost the fix round

Following the precedent switched on a parameter that had never had a caller.
`build_index(cache_path=...)` was tested and dormant, and the built in review
drove six failure paths in it the day a verb passed a path. That is METHOD's
rule about an engine's first caller, and the state file's own `why` text had
been describing a cache nobody had ever filled.
