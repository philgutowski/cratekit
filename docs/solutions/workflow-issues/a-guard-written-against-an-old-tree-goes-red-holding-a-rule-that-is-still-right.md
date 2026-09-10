---
title: A guard written against an old tree goes red holding a rule that is still right
date: 2026-09-10
category: workflow-issues
module: tests/
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: stale_fixture_premise
resolution_type: workflow_improvement
applies_when:
  - A long parked branch is merged rather than rebased
  - A guard pins an exact population and the population has legitimately moved
  - A test writes a file into src/ to make its own premise true
  - "A test's setup depends on a short circuit in the code never being taken"
related_components:
  - development_workflow
  - mutation_testing
tags:
  - stale-fixture
  - exact-membership-pin
  - merge
  - parked-branch
  - collected-count
  - reachability
  - silent-failure
---

# A guard written against an old tree goes red holding a rule that is still right

## Context

U59 merged `fix/conformance-3-and-soft-delete-reader`, eleven commits cut 444
commits behind `main`. Four guards went red on the merged tree. Not one of them
was wrong about its rule. Every one had gone stale about the TREE, and the four
had four different shapes, which is the part worth keeping.

## The four shapes

**A population that legitimately moved.** `SOFT_DELETE_READERS` pins the exact
set of modules that read rekordbox's soft-delete column. It declared
`metadata.py` and `routing_pass.py`. On the merged tree the readers are
`metadata.py` and `trees.py`, because U24 landed `trees.soft_delete_marker` as
the single sanctioned implementation and moved `routing_pass`'s direct read into
it. Two before, two after, a DIFFERENT two. A pin that checked for growth would
have seen a stable count and said nothing. The pin's own comment had predicted
this exact move, and predicting it is what made re-pinning a five minute job
instead of an argument.

**A countdown that fired.** `KNOWN_PACKAGE_NAME_DISAGREEMENTS` recorded, as
exact membership, that U23's package was spelled two ways in two registers. U23
answered the question. The guard going red IS the discharge instruction, and the
comment above it said so in advance.

**A fixture that wrote into `src/` to make its own premise true.** A test owed
`cratekit.write.rebuild`, wrote `src/cratekit/write/tree_rebuild.py` to play the
near-miss sibling, and asserted the diagnosis named it. U36 landed
`rebuild.py`, so the function now short circuits on the owed module EXISTING and
never looks for a sibling at all. The test depended on a branch never being
taken and gave no signal the day it started being taken.

**A rule that caught its own author.** The branch cited two residuals by NUMBER
in a source docstring. `main` carries a guard forbidding exactly that, because
numbers collide across branches. One of the two numbers was a finding the branch
had filed itself, and append-only numbering moved it at the merge. The guard was
right, the branch was wrong, and the citation would otherwise have gone on
pointing at whatever `main` had put in the vacated slot.

## What to do about it

**Merge, do not rebase, and expect every guard to be re-aimed.** Rebasing eleven
commits across 444 resolves the same conflicts eleven times. The merge resolves
them once, and then each guard is driven against the merged tree as its own
piece of work. That IS the unit, not a formality after it.

**Difference the sets. Never adjust a count.** When a pinned population changes,
name what LEFT and what ARRIVED and say why for each. A count that moved by the
right amount is not a measurement of what moved, and here the count did not move
at all while both members did.

**Refuse a new member before admitting one.** The raw measurement offered a
third reader, `tests/test_adopt_collection.py`. It assigns the attribute on a
stand-in row and reads it nowhere: the detector was counting an assignment
TARGET as a read. Admitting it would have made the pin fire on the next fixture
anybody wrote, which is how a guard gets deleted. The detector was narrowed to
load context instead, and the narrowing was pinned from both sides.

**Reconcile the collected count by identifier, never by total.** Zero ids lost
and fifty one gained, none of them in `tests/test_cli_contract.py`, against a
branch whose diff adds four hundred lines to that file. That is how it emerged
that two of the eleven commits were already on `main`: the conformance 3 work
had been cherry-picked across, so the file was byte identical and the brief's
description of what this merge arms was overstated by two commits. A total-only
check would have shown a healthy rise and said nothing.

**Re-aim a stale fixture at the tree rather than patching its premise.** The
near-miss test was re-pointed at `cratekit.write.routing`, which is genuinely
absent beside two genuine siblings, so it writes nothing anywhere. And the short
circuit it had silently depended on got a row of its own, because the failure
was never that the code was wrong; it was that nothing said when the premise
stopped holding.

## What this cost

Four red rows on a green branch, and about an hour to establish that all four
guards were right and all four fixtures were out of date. The dangerous version
is the opposite reading: a session that treats a stale guard as a wrong guard
weakens it to get green, and the rule it was holding goes with it. Ask of every
guard that goes red at a merge whether the RULE moved or the TREE did, and drive
the answer instead of inferring it.
