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

WHAT BELONGS ON IT is a separate question from how it derives, and the two were
confused for weeks. The board carries WORK: units, and the attended chores that are
somebody's to do. It does not carry the register of known and accepted problems,
which is a ledger rather than a queue, so a residual finding earns a place here
only when somebody decides to act on it. Mirroring the ledger onto the board would
assert intent that does not exist and would swamp the few items genuinely ready.

Two failure states are distinct and are not repaired the same way. Drift is a
derived value that fell out of date, and is repaired by recomputing it.
Contradiction is the board and the repository disagreeing about whether work
landed, and is never repaired automatically, because doing so means choosing one
source of truth to overwrite silently.

### Coordination note
A warning written into source on one branch, addressed to whoever performs a
future merge, about a collision no tool will report. It exists for the case where
two branches each change the same thing correctly and both merge cleanly, so the
only thing that can raise the alarm is a person who saw it coming.

It is the unenforced counterpart of the pending register, and the difference
decides which to reach for: a register entry is an obligation the suite fails on,
while a note is prose whose claim no check evaluates. So a note has no expiry, no owner,
and no way to go red, and it is written in the present tense about a branch its
author cannot run and often has not read. Its instruction and the fact that
instruction rests on are separate claims with separate lifetimes, and the fact
may have been unmeasured from the moment it was written, so a reader obeys the
warning and re-measures the fact. A note whose fact was actually checked says so.
A note that survives the merge it was written for is corrected or deleted,
because it has stopped describing anything that exists. Notes come in pairs more
often than their authors realize, since each side of a collision has its own
reason to write one, so a merge reads both branches' records rather than only the
one it is standing on.

## Verification

### Guard
A test that enforces a standing constraint rather than exercising a feature.
Guards exist to make a class of violation impossible to introduce silently, which
is why some are written before the code they govern: a guard that arrives after
its subject can only confirm what already shipped.

Some guards assert a BEHAVIOUR and some assert an ARGUMENT, and the second kind
behaves differently enough to be worth separating. An argument asserting guard
carries a claim in prose about what some part of the system can reach or do, and
enforces that claim mechanically. Such a guard is more valuable than a behavioural
one because the claim is falsifiable, and it is also the only kind that can be
falsified by somebody who never read it: any change that gives a new capability
to anything the claim covers can make the sentence untrue, from a different unit,
in a different file, with every suite still green. That failure is a property of
the combined tree rather than of either contributing change, so nothing short of
the combination can observe it.

When such a guard offers remedies for its own failure, the remedies are driven
rather than reasoned about, and a remedy that makes the guard report MORE is
propagating rather than converging. When every offered remedy terminates in
breaking something else, that is a finding about the design and never a licence
to widen the guard so it accepts what it was written to catch.

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
the costume of an enforced one. A future obligation that cannot be stated as a
missing thing the suite can name is not a register entry at all and belongs in a
coordination note, which is the weaker instrument on purpose.

### Planned verb
A command the registry names before the module that implements it exists. The
name is in the table so the whole surface can be checked before every unit has
shipped. The marker does not clear itself: a countdown fails the moment that
module is importable, and that failure is the signal to remove the marker that
has been keeping the verb out of the running command tree.

A planned verb whose first typed word is already a one-word command cannot enter
the running tree as written: the parser treats that word as a finished command,
not as a group that can grow a child. The name has to change before the marker
clears, because clearing the marker is what puts the verb in front of the parser.

### Battery
The fixed set of checks that must all be clean before anything merges. It is one
named gate rather than a list assembled per change, so asking whether the battery
was run has a single unambiguous answer. An author running their own battery is
not a review: every defect the adversarial reviews have found here passed a green
suite written by the person who wrote the defect.

What it checks is code, imports and repository structure. One of its parts does
read prose, hunting machine specific paths and secrets in any text it finds, but
nothing in it evaluates whether a sentence is TRUE. So any claim made in prose is
outside the battery entirely, whether it sits in a comment, a docstring, or the
instruction files a session reads before it starts, the session contract among
them. That is the property a coordination note depends on and suffers from, and it
is what lets a confident sentence about the project's own state stay wrong
indefinitely while every check stays green.

The battery is the merge gate and continuous integration is not. Integration
runs on a hosted machine that lacks the hardware and tools the suite proves
things against, so a check that cannot pass there says nothing when it fails
there. Integration is confined to what it can actually establish, that the
package installs and imports cleanly on each supported interpreter and that no
personal path or secret reached the tree, and it does not run the suite. Nothing
in it is skipped or deselected, because a skipped proof reads as a passing one.

The battery is unconditional and is a separate question from whether any
particular finding blocks. Whether a finding blocks on its own merits is decided
by the conditions under Blocking finding; whether a tree may merge at all is
decided here, and nothing overrides it. The two are independent, so a finding can
be a residual and still stop a merge, and the reason a merge stopped is stated
alongside the finding's classification rather than inferred from it.

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

### Pinned population
A count the suite recomputes from the tree on every run and asserts as an exact
figure, so that a number a document argues from cannot decay silently as the
tree grows. When a merge moves it the pin fails, and the rule is to look, then
re-measure and re-pin, never to widen the assertion.

A re-pin names its members rather than matching a delta, because a member
leaving while another joins reads as no change and two joining while one leaves
reads as one joining. The comment above the pin is a dated ledger of what joined
and what left at each merge. When the members are literals in the tree, each is
asked of git against the pre-merge commit; when a walk derives them, the same
walk is run over the pre-merge tree and the two sets are differenced.

## Sync

### Sync watermark
An audit record of how far one source got on a clean increment. It does not
decide what the next increment lists or keeps.

A sync watermark advances only when that source completed without error and
actually processed items. A listing that failed entirely is not an empty
catalogue, and it does not write one. Status reads the record. Restore replaces
the coupled file. Scope does not read it.

*Avoid:* treating this as the deletion watermark, or as a date floor.

### Owned dedup
The sync scope rule: take the newest N items the source listed, then drop any
identity the library already holds. That is how a second run processes only what
is new, without reading the sync watermark.

## Findings

### Residual finding
A real defect, gap, or overclaim that is recorded rather than blocking a merge on
its own merits. Recording it with its measured cost is the point; residuals are
not deferred work items so much as the honest register of what is known and not
fixed. A residual therefore lives in that register and not on the board, which
carries work; it moves onto the board only if somebody decides to act on it.

"On its own merits" is the whole of the qualification and it is not the same as
"never stops a merge". A residual whose account the battery is red on stops the
merge through the battery, which answers a different question and admits no
exceptions.

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

- "Watermark" is not one job. Deletion's watermark is a sequence floor, and
  filtering removals by it is the design. Sync's watermark is an audit record,
  and filtering increment scope by it is the silent empty-run bug.
- "Guard" and "test" are not interchangeable here. Every guard is a test, but a
  test that exercises a feature is not a guard, and the distinction decides
  whether the pending register is the right home for it.
- Discharging a pending register entry has been described as two halves, meaning
  the entry and the decorator. It is three edits, because the meta suite keeps its
  own mirrored copy of the key that must move with them.
- "Landed" names two different events. A unit lands when it merges. A verb lands
  when its planned marker clears because the module exists. They can happen in
  different sessions, and only the second puts the name in front of the parser.
- Unit, attended chore, and residual finding have all been called "an item on the
  board". Two of the three are work and belong there; a residual is a record of an
  accepted problem and belongs in the register instead. Collapsing them is what
  makes people ask why the board does not list everything the project owes, and the
  answer is that owing and intending are different.
- A pending register entry and a coordination note have both been called "a note
  for a future unit". They are different instruments and the choice between them
  is not stylistic: one is enforced by the suite and one is not, and only the
  register can make a future obligation fail on arrival.
- "Residual" does not mean "does not stop a merge". It answers only whether a
  finding blocks on its own merits. A residual with no cost to any person still
  stops a merge whenever the battery is red on its account, and both halves are
  said out loud, because a reader given only the classification will ask why the
  merge stopped and a reader given only the outcome will assume it was blocking.
