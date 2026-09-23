---
title: A value given a new source does not inherit the guards written for the old one, so re-walk every check downstream of it
date: 2026-09-23
category: workflow-issues
module: src/cratekit/write/naming_cli.py
problem_type: workflow_issue
component: naming
severity: high
root_cause: guard_written_for_the_old_source
resolution_type: checking_path_rule
applies_when:
  - A unit changes where a value comes from, a filename body that was carried from the name and is now composed from tags, and leaves the code that consumes it alone.
  - A unit adds a new held or refused class upstream of an existing guard, so some inputs now leave the function before the guard runs.
  - A plan and apply pass re-derive the same value on both sides of a gate, and the digest covers the plan and not the re-derivation.
tags:
  - naming
  - gate
  - checking-path
  - R-669
  - R-407
  - R-172
---

# A value given a new source does not inherit the guards written for the old one, so re-walk every check downstream of it

## Problem

R-669's unit changed one thing in `name apply`: the body of a filename that
is digits only is composed from the artist and title tags instead of being
carried from the name. The author's suite was green, fifteen new tests over
real containers through the dispatcher, and the built in review found two
holes the change had opened without touching the code that held them.

The first: the new `unnamed` hold was decided in `_spec_for`, before the
candidate list, so a held file never reached the collection check that every
rename candidate passes through. An imported identifier file with no artist
tag, which is what every one of the fifty four files becomes once landed and
imported, was reported as unnamed and owed on every sweep, sending a person
to write a tag that R-407 makes irrelevant.

The second: the apply pass re-reads the tags after the gate, which is
correct, and then renamed to whatever they rendered. While the body came
from the filename it could not drift during the gate, so no comparison to
the approved name had ever been needed. Composing it from tags opened a
window in which a tag edited during the gate produced a rename to a name
nobody saw, and the re-read that was added for the hold was exactly what
carried the drift through.

## Why the suite could not see it

Both guards were correct for the old source. The collection check ran over
every file that could be renamed, and every file could be renamed. The
digest covered the plan, and the plan was the only thing that could change.
Neither guard was wrong. Each was written against a property the unit had
quietly removed, and no test of the guard fails when the property it relies
on goes, because the test exercises the guard on the inputs that still reach
it.

This is METHOD's third pattern, a fix on the performing path, in a shape the
pattern's wording does not name: the fix was on the right path, and it
changed which inputs the checking path saw.

## The rule

When a unit changes the source of a value, list every guard that reads that
value or reads something derived from it, and for each ask two questions.
Does every input still reach it, or does the new branch leave before it? And
did the guard rely on a property of the old source, one that the new source
does not have? Here the first question caught the hold placed before the
collection check, and the second caught the body that could now drift.

In this verb the concrete rules are: a new held class is decided AFTER the
collection is read, and the collection wins over it; and the apply pass
compares the name it renders after the gate to the `to` the plan was
approved with, and owes the rename when they differ, for every file and not
only the composed ones.

## Related

- R-407 and U67, the collection check this unit's hold walked past.
- R-172, the incomplete list the drifted rename is owed to.
- `docs/solutions/workflow-issues/a-name-filter-added-to-the-offering-path-alone-leaves-the-renaming-path-eligible.md`,
  the same shape in the acquisition path.
