---
title: "A merge falsifies a guard's invariant and every remedy the guard offers breaks something else"
date: 2026-08-14
category: workflow-issues
module: tests/modules/test_reports.py
problem_type: workflow_issue
component: development_workflow
severity: high
resolution_type: documentation_update
applies_when:
  - "A merge turns a guard red that neither branch turned red alone"
  - "A guard's docstring names its remedies and every one of them terminates in breaking something else"
  - "A unit gives a new capability to a module some unrelated guard's allowlist already admits"
  - "A finding fails the battery but no user facing cost can be found or claimed"
  - "Correct resolution work sits on a merge that cannot land"
symptoms:
  - "Two branches each pass the full battery and their merge does not"
  - "A guard reports a violation inside a package whose own code did not change"
  - "The transitive closure a guard walks reaches a name other modules are required to import"
related_components:
  - testing_framework
  - documentation
  - tooling
tags:
  - guard
  - allowlist
  - merge
  - residual-finding
  - transitive-closure
  - design-decision
  - cross-unit
---

# A merge falsifies a guard's invariant and every remedy the guard offers breaks something else

## Context

Cratekit has structural guards that assert an ARGUMENT rather than a behaviour.
The reports allowlist in `tests/modules/test_reports.py` is the clearest one. It
carries `ALLOWED_IMPORTS`, the set of modules the reports package may import
(`tests/modules/test_reports.py:1656`), and a comment block stating why that set
is safe. An earlier version of that comment claimed the list alone was the
argument, that nothing admitted could touch a file except through `pathlib`. U34
measured the claim and found it false, so the guard was rebuilt around a better
one: the list is safe because of the list PLUS a named set of every writer the
admitted modules expose, held in step by
`test_the_allowlist_admits_no_writer_this_guard_cannot_name` (`:5047`). The
comment states that argument in terms of `FILESYSTEM_MUTATIONS` (`:1698`); the
guard enforces it over two sets, because `QUALIFIED_MUTATIONS` (`:1753`) carries
the writers that must be spelled with the module in front of them, and the
test's own assertion message names both. That test's docstring states the rule
and the two ways out of a failure: name the writer in the set, or take the module
off the allowlist, and "What is not available is leaving the argument written
down and untrue".

That is a good guard. It is falsifiable, it was falsified once, and it was
rebuilt around what the falsification taught. This document is about what
happens when the guard is still right, its argument has become false a second
time, and neither of the two ways out is available.

On 2026-08-14 the U27 merge produced exactly that state. U27 had been verified
independently as MERGE by an agent that did not write the code: 42 mutation rows
against the author's 19, 25 deaths, 17 zeros, no blocking finding, full battery
green on the branch. `main` was green too. The merged tree was not, and neither
side could have observed why, because the sentence the two units jointly
falsified lives in a third file that neither of them edited.

The finding itself is recorded as R-80 (`docs/residual-findings.md:5257`), filed
on `main` in commit `f2f8d5b`. **This document is not that record.** R-80 is the
measurement of one collision. This is the procedure to run on the next one. R-80
itself was decided and closed on 2026-08-15: the write capable handle was
replaced with metadata readings, driven against the handle over twelve real
arrangements, and U27 merged. Nothing in the procedure below changed.

**The class is not new here, which is worth knowing before treating any instance
as exotic.** (session history) One day earlier, U30 built an emission ratchet in
DJ_tools and its review found the same shape from the other side: the guard's own
enumeration of governed entry points did not match the set of entry points that
actually write, so a shipped CLI writing through raw emitters slipped past both
the audit and the consult. The same review also found the mirror failure, a
depth blind probe that would have blocked a user playlist merely named `INBOX`.
A guard standing in for a concept can be coarser than the concept in either
direction, and neither direction is visible to the person who wrote the guard.

## Guidance

**Read a red guard on a merged tree as a claim about the merged tree, not about
either branch.** A guard whose argument is a sentence about what a package can
reach is falsifiable by any unit that adds a capability to any module that
sentence covers, including a unit that never opened the guard file and never
opened the package the guard governs. Neither author is careless and neither
branch is wrong. The failure is a property of the union, so the union is the
only place to reason about it.

**Drive each remedy the guard offers to its end. Do not reason about them.** The
assertion message names its remedies and every one of them will look plausible
from the armchair. In the U27 case the naming remedy looked correct for three
consecutive rounds before it stopped being correct. Only driving revealed where
it terminates.

**When a guard propagates, compute the transitive closure in one pass rather
than chasing it a layer per run.** The allowlist guard reports a writer's callers
as writers, so naming one symbol surfaces its direct callers on the next run, and
naming those surfaces theirs. Chasing that one round at a time has two costs. The
first is that a set like `QUALIFIED_MUTATIONS` ends up half filled, which is
worse than empty because it reads as considered. The second, and the one that
matters, is that it hides where the closure ENDS. Walk the module's own call
graph with an AST pass, seeded from the direct callers of the offending symbol,
and propagate until the set stops growing. Then look at what is in it BEFORE
adding anything to the guard.

**When every offered remedy terminates in breaking something else, stop. That is
information about the design.** It is not a licence to take the third path. The
third path always exists, is always available, and is always wrong when the guard
is correct: teach the checker to accept the thing it was written to catch. Here
that meant widening `_os_open_reads` (`tests/modules/test_reports.py:4109`), a
helper whose whole job is to decide whether an `os.open` call's flags say read
only, by comparing every flag name against `_READING_FLAGS` (`:4070`) and
answering true only when all of them read.

**Be precise about WHY it declines, and get the precision by ASKING THE GUARD
rather than by reading it.** Two accounts of this were written before anybody
did, and both were wrong. R-80 said the guard inspects the conditional and
concludes one branch writes. The first version of this document corrected that to
unreadability, which is the right category, and then named the wrong unreadable
shape: it said a conditional expression is what the flag reader cannot parse.

**Driven 2026-08-14, the actual mechanism.** `_os_open_reads` reads the CALL
ARGUMENT. The call is `os.open(path, flags)` and the argument is the bare local
name `flags`, which the helper cannot resolve back to its assignment, so it
answers "flags this cannot read as a read". **The assignment is never examined at
all**, whatever shape it has. Five rewrites of it were driven and every one
stayed red, including `flags = os.O_RDONLY` with no conditional and no `getattr`
in it. Inlining the expression into the call is what the helper can read, and it
then behaves exactly as designed: `os.open(path, os.O_RDONLY | os.O_NONBLOCK)`
passes and `os.open(path, os.O_RDWR | os.O_NONBLOCK)` fails.

So the guard's objection is "I cannot tell what this opens", and the thing it
cannot see through is one level of local variable indirection. The finding stays
real, because the handle genuinely is write capable. But the correction opens a
resolution none of the three recorded ones name, which is the practical cost of
having reasoned about the helper twice instead of running it once.

**The general lesson is the one this repository keeps paying for.** Three
accounts of a guard's behaviour were written from reading its source, by three
readers, one of them an independent verifier, and the first two were wrong in
different ways. The guard is thirty lines long and answers in under two seconds
when asked directly. METHOD's rule that a finding must be driven end to end
applies to the MECHANISM of a finding and not only to its existence.

**This repository already has the same rule in a different scope, and the
consistency is the argument.** `scripts/board.py audit` deliberately does not
auto repair its exit 2 contradictions, because repairing them automatically means
picking one source of truth to overwrite, which is how the wrong one wins
silently. A guard whose invariant and whose admitted set now disagree is that
situation exactly. Widening the guard is picking a side and calling it a fix.

**Record the refusal where the next reader will be standing.** An empty set with
no note reads as an oversight. An empty set carrying the driven reasoning reads
as a decision and stops the next session repeating the three rounds. On the
preserved merge branch the block under `QUALIFIED_MUTATIONS` opens with "NOTHING
WAS ADDED HERE AT THE U27 MERGE ATTEMPT, 2026-08-14, and the reason is the
finding", then walks both remedies to their ends.

**Separate two rules that are easy to collapse, because they answer different
questions.** The merge bar (`docs/METHOD.md:11`) governs whether a finding BLOCKS
on its own merits, and requires all three of: driven end to end, a named user
facing cost, and a reachable input whose producer was driven. The battery rule
(`docs/METHOD.md:185`) governs whether a tree may merge at all, and is
unconditional. A finding can therefore be a RESIDUAL under the merge bar and
still stop a merge dead. R-80 is exactly that: no user facing cost was found or
claimed, so it does not block, and the tree still cannot go green, so the merge
does not happen. Getting this backwards in either direction is the likeliest
error. Calling it blocking invents a user harm nobody measured. Calling it "only
a residual" and merging red destroys the one signal the whole discipline rests
on.

**Preserve the resolved but red merge on its own branch, pushed, and marked DO
NOT MERGE in its own commit body.** A merge attempt that stops is not wasted
work. The conflict resolutions, the register discharge, the renumber, and any
reservation added because only the merged tree could see the obligation are all
independent of the blocker and all correct. Discarding them means paying for them
again, and paying again is how the second attempt gets one of the same six places
differently wrong.

**Send the unit back for a decision, not a repair.** R-80's closing condition
names three candidate resolutions and each changes a design rather than a line.
Under METHOD's cap each unit has at most two fix rounds left, so sending it back
is inside the process rather than an exception to it.

## Why This Matters

A guard that asserts an argument is more valuable than a guard that asserts a
behaviour, and it is also the only kind that can be falsified by somebody who
never read it. That asymmetry is the whole mechanism, and it is worth spelling
out in the order it happened.

1. **U27 lands `_probe` in `src/cratekit/core/cause.py`.** It computes
   `flags = (os.O_RDWR if writing else os.O_RDONLY) | getattr(os, "O_NONBLOCK", 0)`,
   calls `os.open(path, flags)`, and closes the handle. There is no `O_CREAT` and
   no `O_TRUNC`, so it cannot create a file and cannot empty one. It exists to
   ask the operating system whether a write would be permitted rather than guess
   from a driver level error that says "unable to open database file" and nothing
   else. It changes nothing, and it does open a write capable handle.

2. **U34's allowlist admits `cratekit.core.cause`, and not by oversight.** Both
   report modules import from it: `src/cratekit/modules/reports/export.py:71` and
   `src/cratekit/modules/reports/aging.py:62` each read
   `from cratekit.core.cause import Scope, refuse`. Refusing structurally is what
   the reports do instead of returning an empty view, so the refusal vocabulary
   is load bearing for them.

3. **The guard propagates a writer to its callers.** That propagation is correct
   and is the only thing that makes the guard hard to walk past: a report calling
   a private helper that calls a writer is still a report that can write. It also
   means the failure grows a layer per run, which is what makes one round at a
   time so misleading.

4. **The closure was computed instead of chased.** An AST walk in one pass,
   seeded from the single direct caller of `os.open`, propagated until it stopped
   growing: eleven names, and `refuse` is among them. The path runs through
   `CratekitError.cause` calling `classified`. **That edge exists only on the
   merged tree.** On `main` at `b4c9b45`, `CratekitError` still sets its cause as
   a plain attribute; U27 turns it into a property, and a property is what puts a
   call to `classified` inside the class body where the guard's walk can see it.
   The property is correct on its own terms, because `raise X from exc` sets
   `__cause__` after the object is built, so a value computed in `__init__`
   cannot see what the raising site just declared the failure to be.

5. **Naming `refuse` fires the reports' own guard.** With `refuse` in the
   mutation sets, the reports package is reported as able to change a file at its
   two real refusal sites, `src/cratekit/modules/reports/aging.py:248` and
   `src/cratekit/modules/reports/export.py:195`. The remedy for one guard trips
   the other, and the second report is not wrong either.

6. **Dropping the module fails both report modules' imports**, per step 2.

7. **Widening `_os_open_reads` was refused**, per the Guidance above.

So the sentence "nothing the reports package can reach can change a file" is now
false on the merged tree, the one test written to catch exactly that has no
answer available to it, and no report mutates anything in fact, because `_probe`
opens and closes.

**The cost is not a user harm. It is a false invariant with no repair inside the
merge.** That is precisely why the residual and blocking distinction has to be
made explicitly rather than felt. Both facts are true at once, and a session that
remembers only one of them will either overstate the finding or ship red.

**A specific, measured hazard prediction is not the same as knowing what will
bite.** (session history) The session before this one named U27's next merge as
carrying "the single highest risk countdown discharge in the tree", and backed it
with a real measurement: `cratekit.cli.doctor` had two gated sites in two
different files, which is exactly the shape where a grep stopping at the first
hit leaves the second file to lose its collection. That prediction was correct
and the hazard was real, and it was prepared for and passed cleanly. The trap
that actually stopped the merge was a different one, in a different file, that
nobody had named. Both were live at the same merge and they are independent of
each other. Preparing for the hazard you measured does not reduce the number of
hazards.

**Expect the first write up of a merge trap to be too narrow.** (session history)
This repository has already corrected itself on exactly that: the countdown
learning was drafted as a first occurrence, and the related docs pass then
surfaced R-21 item 5 recording the same mechanism on the earlier U36 merge, which
also contradicted wording that had been added to METHOD the night before. The
document was rewritten to say it was the second occurrence. Treat the present
document the same way, as the current best account rather than the complete one.

## When to Apply

Apply this when a guard goes red on a merged tree and the redness is not
obviously somebody's mistake. Concretely:

- **A structural guard fails and neither branch's suite fails.** Check this
  first. If both branches are green, no author's code is wrong, and the question
  is about the union.
- **The guard's failure message offers remedies.** Enumerate them from the
  message text itself rather than from memory, and drive each one.
- **A remedy makes the guard report MORE, not less.** That is propagation, and it
  is the signal to stop iterating and compute the closure in one pass.
- **The closure reaches a name the package legitimately calls.** A public entry
  point, a constructor, a decorator: anything whose presence in the guard's set
  would make correct code fail. That is the terminal condition, and the remedy is
  not available.
- **You catch yourself considering an edit to the CHECKING helper rather than to
  the checked code.** Stop and ask whether the helper is behaving as designed. If
  it is, this is a design decision and not a merge task.
- **The finding has no measurable user facing cost and the battery is still
  red.** File it as a residual with its full measurement, and do not merge. Say
  both halves out loud in the record, because a reader who sees only "residual"
  will ask why the merge stopped, and one who sees only "merge stopped" will
  assume it was blocking.

Do NOT apply this when the guard is red for an ordinary reason: a genuine writer
that genuinely should be named, an import somebody added without thinking, a
conflict resolved wrongly. Drive the remedies first. This procedure is what is
left when driving them all produces no survivor.

## Examples

The U27 merge attempt into `main`, 2026-08-14.

**The rounds, as the session reported them rather than as an artifact records
them.** Naming `_probe` was correct on its face, and it made the guard report its
direct callers instead. Naming those surfaced theirs, and so on. The session's
account is three rounds before the remedy stopped looking like it was
converging; the branch comment says only "one row at a time" and no artifact
carries the count, so treat the number as narrative and the shape as the point.

**The pass that ended it.** An AST walk over `src/cratekit/core/cause.py`, seeded
from the one direct caller of `os.open` and propagated until the set stopped
growing: eleven names, containing `refuse`. Naming `refuse` was then DRIVEN
rather than predicted, and the reports' own guard fired: the reports package can
change a file, at `src/cratekit/modules/reports/aging.py:248` and
`src/cratekit/modules/reports/export.py:195`. Those are the two sites the reports
genuinely have, and they are correct code.

**The other remedy, driven.** Dropping `cratekit.core.cause` from
`ALLOWED_IMPORTS` fails the imports at
`src/cratekit/modules/reports/export.py:71` and
`src/cratekit/modules/reports/aging.py:62`.

**The third path, refused.** Adding `O_RDWR` to `_READING_FLAGS`, or teaching the
helper to chase a local variable back to an assignment it then has to evaluate,
would make it answer "this reads" about a handle that can write. The guard is
behaving exactly as designed, so it was left alone.

**A fourth path, which only the corrected mechanism makes visible.** Because an
INLINE read only flag expression passes, splitting the probe's two intents so the
read only one spells its flags at the call site narrows the problem to the single
write intent caller. It was not available while everyone believed the guard was
objecting to the conditional. Recorded in R-80 rather than taken here.

**A fifth path, driven and refused, and the reason it is worth writing down.**
Moving the raw open into a module the allowlist does not admit, and leaving
`cause.py` calling it, turns the guard GREEN with the reachability unchanged,
because the audit walks only the modules the allowlist names. The layering guard
catches that particular relocation, and is then satisfied by adding one name to
one regex. Both structural guards can be satisfied by a change that fixes
nothing. That is R-102, filed as a finding about the guard rather than about this
merge.

**What happened to the merge.** It did not proceed. `main` stayed green and
untouched. R-80 was filed on `main` in commit `f2f8d5b` with the full
measurement, and the merged tree was committed to the branch
`merge/u27-attempt-2026-08-14` at `01eb6da`, pushed, and marked DO NOT MERGE in
its own commit body. Commit identifiers are given here with the branch they sit
on, because this project uses no pull requests, so there is no PR number to cite
and a bare identifier is not a durable address. `01eb6da` is deliberately NOT
reachable from `main`, which is the point of it; it is reachable from
`merge/u27-attempt-2026-08-14` on the remote. A claims checker that resolves
identifiers against the default branch will flag it, and the flag is correct.

What that branch is holding, none of which the blocker affects:

- Six conflicts resolved, per that commit's own body, including
  `tests/_pending.py`, which auto merged and was then verified by hand rather
  than trusted: nine keys, `main`'s ten minus `cratekit.cli.doctor`. The key
  count is checkable against the branch and the conflict count is not, because
  the preserved commit has a single parent and so carries no merge topology to
  diff a conflict set against.
- A countdown discharge done in full, with both decorator sites removed, the now
  unused `requires` import taken out of `tests/test_config.py`, and the two
  formerly gated guards run on purpose and passing. That is the sibling learning
  in this same directory being applied correctly, at the same merge that produced
  this one.
- `src/cratekit/cli/registry.py` and `tests/test_cli_contract.py` resolved as
  unions, then swept with an AST walk over every dict and set literal in `src`
  and `tests` for duplicate keys. Zero found.
- Ten incoming residuals renumbered in that branch's own file, with `main`'s
  numbers unmoved, which is the rule.
- The `grant-path-access` reservation added in `src/cratekit/cli/exit_codes.py`,
  an obligation only the merged tree could see: U27 added the remedy, and U38
  landed the reservation registry after U27's branch was cut.
- The cause population re-pinned from 101, 79, 22 to 106, 83, 23, re-measured
  rather than widened. Those are the BRANCH's figures. `main` moved to 103, 81, 22
  through a later merge that appended two cause slugs of its own, and then to
  108, 85, 23 when U27 itself merged on 2026-08-15, so a reader checking these
  numbers against `main` will find different ones and neither set is wrong. That
  final re-pin was the first to move the reserved half, and it was done by naming
  the five members rather than matching the delta; the bare numbers here are the
  shape `a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md`
  argues a re-pin comment should not stop at.

Every one of those would have to be redone on a second attempt, and each redo is
a chance to get one of them differently wrong.

## Related

- `countdown-entry-discharge-drops-a-whole-test-file.md`: this repository's other
  merge time trap, and this document's pair. Both fire only at a merge, both are
  one unit's change meeting another unit's mechanism, and neither is visible from
  either branch alone. They differ in what they threaten. That one silently
  removes evidence, so its danger is a merge that looks finished. This one
  produces a loud red that cannot be made green, so its danger is a merge that
  gets forced. That document calls `tests/_pending.py` the repository's highest
  risk merge surface, and that claim is about a FILE and remains true: R-80 is
  not in the register and does not touch it. The merged TREE is a separate class
  of surface, and this is the entry for it.
- `docs/residual-findings.md`, R-80: the canonical record of this specific
  collision, with the corrected mechanism, the measured cost, what was preserved,
  and the candidate resolutions. Cited without a line number on purpose, because
  the entry has since grown and a line number into a file that gets appended to
  is a citation with a shelf life.
- `docs/residual-findings.md`, R-102: the hole the fifth path went through. The
  allowlist audit reads only the modules the allowlist names, so an admitted
  module can delegate its writing one hop out and be read as ordinary code. That
  is a finding about the guard and outlives this merge entirely.
- `docs/METHOD.md`, "The merge bar, decided 2026-08-09" at line 11, and "The
  battery" at line 185: the two rules this document insists on keeping apart.
- `docs/METHOD.md:245`: the class this belongs to, named there as "a rule
  verified against source while a second surface carries the same coupling". It
  sits in the residual renumbering section rather than in the four recurring
  defect patterns at `:157`, which is worth knowing, because the phrase reads
  like one of the four and is not.
- `docs/history/wave-state-2026-08-14.md`: the session narrative, with U27's independent
  verification numbers and the merge outcome.
- `tests/modules/test_reports.py:1632` onward: the allowlist's own comment block,
  a worked example of a guard whose argument was found false once and rebuilt
  around the falsification rather than deleted. Start at 1632 rather than later:
  the sentence that makes it worth reading is the one admitting the earlier
  version of the comment was wrong.
