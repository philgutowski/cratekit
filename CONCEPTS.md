# Concepts

Shared domain vocabulary for this project: entities, named processes, and status
concepts with project-specific meaning. Seeded with core domain vocabulary, then
accretes as ce-compound and ce-compound-refresh process learnings; direct edits
are fine. Glossary only, not a spec or catch-all.

## The build

### Unit
A numbered increment of the build, specified by its own issue and delivered on
its own branch. The unit is the atom of this project: work is picked as a unit,
verified as a unit, and merged as a unit, and a unit's issue is its full brief
rather than a pointer to one.

A unit's number and its issue number are not guaranteed to match, so the issue is
looked up rather than assumed. Units declare dependencies on other units, and
those declarations are the only input to whether a unit is ready.

### Board
The queue that says which unit to take next. Ready and blocked are derived values,
computed from unit dependencies and issue closure rather than set by hand, so the
board is recomputed rather than remembered. Ranking is by how much of the
remaining build a unit releases, counted transitively, so a unit whose single
dependent gates a whole phase outranks one with several dead end dependents.

Two failure states are distinct and are not repaired the same way. Drift is a
derived value that fell out of date, and is repaired by recomputing it.
Contradiction is the board and the repository disagreeing about whether work
landed, and is never repaired automatically, because doing so means choosing one
source of truth to overwrite silently.

## Verification

### Guard
A test that enforces a standing constraint rather than exercising a feature.
Guards exist to make a class of violation impossible to introduce silently, which
is why some are written before the code they govern: a guard that arrives after
its subject can only confirm what already shipped.

### Pending register
The one declaration of guards whose subject does not exist yet. Each entry names
the missing thing, the unit that will land it, and what the guard behind it
asserts. It exists so that a guard written early is a countdown rather than a
hole, and so that no such gate can be created anywhere else.

An entry is an obligation with an expiry, not an exemption. When the unit lands
the subject, a meta test fails on purpose, and discharging it means removing the
entry, removing its mirrored copy in the meta suite's expected set, and removing
the gating decorator from every guard the entry covered. Removing the entry alone
does not arm the guard: the gate helper refuses an undeclared key at import time,
which takes the guard's entire file out of test collection. A full run then stops
outright and executes nothing, so the loss reads as ordinary only to a run told to
continue past collection errors, to a subset run that never names the affected
file, or to a comparison of collected totals rather than identifiers. An entry
that no guard actually cites gates nothing, and is an unenforced countdown wearing
the costume of an enforced one.

### Battery
The fixed set of checks that must all be clean before anything merges. It is one
named gate rather than a list assembled per change, so asking whether the battery
was run has a single unambiguous answer. An author running their own battery is
not a review: every defect the adversarial reviews have found here passed a green
suite written by the person who wrote the defect.

### Mutation table
A measurement of whether the suite would notice the code breaking. Each row
reverts one guard, runs the tests, and counts how many fail, and that count is the
guard's death count. A guard whose removal kills nothing is untested whatever the
coverage report says, because coverage measures which lines ran and this measures
which lines mattered.

A death confirmed on a narrow subset is a real death, while a zero on a subset is
not yet a zero and is promoted to a full run before it is reported. Row counts are
capped by the depth of the pass, and a truncation that nobody logged reads as
coverage.

## Findings

### Residual finding
A real defect, gap, or overclaim that is recorded rather than allowed to hold a
merge. Recording it with its measured cost is the point; residuals are not
deferred work items so much as the honest register of what is known and not fixed.

Residual numbers are append only. A number, once given, belongs to that finding
for life, and numbers already recorded never move when new ones arrive, because
the number is cited from surfaces the repository cannot see and a renumber
repoints those citations silently.

### Blocking finding
A finding that does hold a merge. It qualifies only on three conditions together:
it was driven end to end rather than argued from reading the source, it has a
named cost to a person, and its input is reachable by a producer that was actually
driven. Everything else is a residual.

The third condition is the one that is usually skipped. A cost over an input that
nothing can produce is not a cost, and the honest report of a failed hunt names
how many candidate producers were driven rather than claiming that nothing
produces it.

## Flagged ambiguities

- "Guard" and "test" are not interchangeable here. Every guard is a test, but a
  test that exercises a feature is not a guard, and the distinction decides
  whether the pending register is the right home for it.
- Discharging a pending register entry has been described as two halves, meaning
  the entry and the decorator. It is three edits, because the meta suite keeps its
  own mirrored copy of the key that must move with them.
