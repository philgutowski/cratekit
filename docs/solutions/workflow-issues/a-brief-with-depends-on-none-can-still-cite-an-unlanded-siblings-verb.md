---
title: A brief with Depends on none can still cite an unlanded sibling's verb
date: 2026-09-18
category: workflow-issues
module: docs/METHOD.md
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: missing_validation
resolution_type: workflow_improvement
applies_when:
  - A Phase G unit's brief has "Depends on: none" or names dependencies that are all landed
  - The brief's test scenarios or approach section names a CLI verb, flag, or file it expects a sibling unit to produce
  - board.py show N reports the unit READY, so the formal dependency gate is silent
  - The named verb belongs to a unit that has not landed on the tree being built against
symptoms:
  - A test scenario in the issue body cannot be written because the verb it names does not exist on main
  - grep for the cited command in src/cratekit/cli/registry.py or docs/GUIDE.md returns nothing
  - The unit is READY on the board despite one of its own test scenarios depending on unlanded work
  - The gap is discovered mid build rather than at board.py show time
related_components:
  - testing_framework
  - documentation
tags:
  - brief
  - dependency
  - board
  - relay
  - phase-g
  - residual
  - planning
---

# A brief with Depends on none can still cite an unlanded sibling's verb

## Context

U70's brief (`crate intake playlist favorites`, issue #115) opened with
`**Depends on:** none` and `board.py show 70` reported it READY. Its test
scenarios section named `intake missing --job` over the finished job as the
end to end check: queue the missing hearts, then run that verb and confirm it
writes two rows. `intake missing --job` is U69's verb. U69 had not landed on
the tree U70 was built against. The brief's own dependency line said there was
nothing to wait for, and one of its verification steps named something that
did not exist.

METHOD's Relay section tells a session to check dependencies before building:
"Before building, run `board.py show N`. If any issue on its `Depends on`
line is still open, the outcome is BLOCKED" (`docs/METHOD.md:389-392`). That
check reads the board's dependency edge, which `scripts/board.py` derives from
the issue's `Depends on` line and the linked issues' open or closed state. It
does not read the brief's prose. A verb named in Approach or Test scenarios
text is not a dependency edge unless someone also wrote it on the `Depends on`
line. U70's author did not, because the brief's own author believed the two
units were independent enough to run in parallel, and mostly they were: U70
owns the listing and resolution half, U69 owns the write-the-list-document
half. The one seam between them, one verb's name, was not declared.

The task process that built U70 (relay task 115) caught the gap itself,
mid build, by trying to write the named test scenario and finding no such CLI
surface. It did not block the whole unit, and it did not invent the missing
verb. It pinned the half it owned, `intake.cli.frozen_rows` queuing missing
hearts with their provider ids, drove that with
`test_the_missing_hearts_carry_the_provider_id_acquisition_reads`, and
recorded the rest as owed to U69 in the R-423 narrowing
(`docs/residual-findings.md`, "Narrowed 2026-09-18 on relay/115, U70").

## Guidance

`board.py show N`'s READY verdict answers one question: are this unit's
declared dependencies closed. It does not answer whether every verb the
brief's own prose leans on already exists. Before trusting a brief's test
scenarios or approach section as buildable as written, check that any CLI
verb, flag, or file it names is actually on the tree: grep the registry
(`src/cratekit/cli/registry.py`) or run the command's `--help`. A brief can be
internally consistent about scope and still cite a sibling's unlanded surface,
because the dependency line records unit order, not every name inside the
prose.

When a cited verb turns out not to exist, do not block the unit and do not
guess at the missing verb's shape to make the scenario pass. Build the half
the brief's Files and Goal actually assign to this unit, pin whatever test
would exercise the missing seam once the sibling verb exists, and record the
gap in the ledger as owed to the unit that actually owns it, the way R-423 was
narrowed rather than closed. That keeps the two units' scope boundary honest
without inventing a false dependency after the fact or stalling a unit that
is genuinely independent of everything except one line of test scenario text.

## Why This Matters

The board's dependency graph is what `cratekit-parity.order` and the feeder
use to decide what is safe to launch next (`docs/METHOD.md:381-387`). If a
brief's cited-but-undeclared seam were treated as a reason to add a real
dependency after the fact, every Phase G brief that mentions a sibling verb
for context would start acquiring dependency edges nobody asked the board to
enforce, and the feeder would stop launching units that are actually
independent. Treating it as a scope boundary to record, not a blocker to
declare, keeps units parallel where they truly are parallel and keeps the
ledger honest about the one seam that is not.

## When to Apply

Before building a unit whose test scenarios or approach section names a CLI
verb, flag, or file this brief does not itself create. Confirm the name
exists on the tree independent of what `Depends on` says, since the two are
not the same check. If it does not exist, pin your own half and narrow the
relevant ledger entry rather than blocking or guessing.

## Related

- `docs/residual-findings.md`, R-423 narrowing on `relay/115`: the recorded
  instance, the half U70 owns closed, the half owed to U69 left open with the
  pinning test named.
- `docs/METHOD.md:389-392`: the `board.py show N` dependency check this gap
  sits beside without triggering.
