---
title: Discharging a countdown entry by half takes a whole test file out of collection
date: 2026-08-13
category: workflow-issues
module: tests/_pending.py
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_workflow_step
resolution_type: workflow_improvement
applies_when:
  - A merge brings a module onto main that the pending register was waiting for
  - "The countdown meta test goes red for a key, which is the design working"
  - A merge conflict lands inside the pending register
related_components:
  - development_workflow
  - documentation
tags:
  - pytest
  - test-collection
  - pending-register
  - countdown
  - merge
  - decorators
  - silent-failure
---

# Discharging a countdown entry by half takes a whole test file out of collection

## Context

Cratekit ports safety guards BEFORE the code they govern. U6 chose that ordering
deliberately: a guard arriving after its code can only confirm what already
shipped, while a guard arriving first makes the violation impossible to introduce
silently. The cost is that some ported guards name a module that does not exist
yet.

`tests/_pending.py` pays that cost without opening a hole. Its `PENDING` dict
maps a missing thing, either a dotted module path probed with `find_spec` or a
`path:` prefixed repo path probed against the filesystem, to the unit that will
land it and a line saying what the gated guard asserts. A waiting guard carries
`@requires("<key>")`, which returns a `pytest.mark.skipif` whose reason names the
unit. `tests/test_pending_units.py` then enforces that the declared set is
exactly the intended set, that every declared target is genuinely still absent,
and that no skip is constructed anywhere outside the register.

The design is a countdown rather than a hiding place. When a unit lands its
module, the meta test goes red on purpose, and clearing it is supposed to arm the
guard.

**The gap this document closes is at the other end of the countdown.** The
register tells you loudly to delete the entry. It does not tell you that the
entry is one part of what has to move, and moving only that part is worse than
moving nothing.

This is the repository's **second** encounter with the mechanism. The first is
recorded in `docs/residual-findings.md` under R-21, item 5, found on the U36
merge against `cratekit.write.rebuild` and `tests/test_restore.py`. That entry
even corrects an earlier account of itself for being wrong about the failure's
shape and size. The rule still did not reach `docs/METHOD.md` until the U16 merge
produced it a second time on 2026-08-13. A residual that records a defect is not
the same thing as a rule that prevents it, and that gap is most of why this
document exists.

## Guidance

A countdown discharge is **three edits, in one commit**, not two:

1. Delete the entry from `PENDING` in `tests/_pending.py`.
2. Delete the matching key from `EXPECTED_PENDING` in
   `tests/test_pending_units.py`. That set duplicates every key on purpose, so
   the register is already a two place edit before decorators are counted.
3. Remove the `@requires("<key>")` decorator from **every** guard it gated, so
   those guards run unconditionally.

`docs/METHOD.md` and `RESTART-cratekit.md` both state this as "two halves". That
phrasing is a compression of steps 1 and 2 into one idea, and it is fine as a
reminder to somebody who already knows the mechanism. Followed literally by a
session that does not, it is wrong.

**Run the grep before deleting anything.** A key is usually cited from more than
one file, and a grep that stops at the first hit is how the second file loses its
collection:

    grep -rn 'requires("<key>")' tests/

Then check what the grep tells you. Two entries in the register today are cited
by no decorator at all. For those, step 3 is empty and no collection failure is
possible. `tests/test_restore.py` names that shape directly: an entry that no
`@requires` cites gates no test, and is an unenforced countdown wearing the
costume of an enforced one. The grep is what distinguishes the two cases, which
is why it runs first rather than as a confirmation afterwards.

**Do not follow the KeyError message.** It offers exactly one remedy, to add the
key to the register with the unit that lands it. That is correct for a new key
someone typed by hand and exactly backwards at a merge. The message assumes the
key is arriving. At a discharge it is leaving.

Three finishing steps that are part of the practice rather than extras:

- Remove the now unused `from tests._pending import requires` import if that file
  has no other gated guard. Ruff catches it, which is one more reason to run the
  whole battery rather than the one file you touched.
- **Run the armed guard on purpose and read its result.** It has never executed
  once. A green run is the first evidence it works at all, and it can just as
  easily be the first evidence that the two things it compares disagree.
- Reconcile the collected count **by identifier**, not by total. On the U16 merge
  the total rose from 4445 to 4776 while 24 identifiers went missing underneath
  it, so a total only check would have certified the merge.

## Why This Matters

`@requires(...)` is evaluated when its module is imported, because a decorator
expression runs at definition time. Pytest imports a test module in order to
collect it. So a `KeyError` out of `requires` is not a test failure. It is a
**collection** failure, and it removes the whole file's tests from existence
rather than turning one of them red.

That difference is the point. An assertion failure is scoped, named, and
counted: one test, one red line, one identifier you can grep for. A collection
failure removes the tests before anything can count them, and nothing downstream
can distinguish "this file's tests all passed" from "this file's tests were never
built". On the U16 merge the file was `tests/test_match_states.py`, which holds
330 tests, measured at the tree with
`pytest tests/test_match_states.py --collect-only -o addopts=`.

`requires` raises rather than degrading, and that is deliberate: a skip must not
become permanent by accident. The refusal that protects an authoring mistake is
the same refusal that kills the importing file at a discharge.

**Be precise about the silence, because the loud case is the common one.** A
plain `pytest` run does not report green here. It exits 2 with `Interrupted: 1
error during collection` and runs nothing at all. It does not look like a suite
that passed, it looks like a suite that refused to start. R-21 item 5 makes
exactly this correction against its own earlier text. The failure reads as green
only under one of these conditions:

- a run told to continue past collection errors, which does not abort the session
- a subset run that never names the affected file, which is the normal shape of
  "I only touched this module, so I ran its tests"
- a comparison of collected totals rather than identifiers, where a rise in the
  total hides a collapse underneath it

A fourth condition is specific to this repository: `pyproject.toml` already sets
`-q`, so an added `-q` becomes `-qq` and suppresses the summary line. METHOD
carries that as its own rule for the same reason.

**The same class already has a rule in a different scope.** METHOD's mutation
driver rules say to check the collected count on every row, because a file that
fails to collect takes its tests with it and the run still looks green.
`scripts/mutate.py` enforces it by comparing each row's collected count against a
baseline and invalidating the row. The driver met this one row at a time and
built machinery against it. The merge path meets it once, at the moment the tree
is largest and a reviewer is most inclined to read a clean summary as a clean
tree.

**The asymmetry is what makes the wrong half the likely one.** Skipping step 3
leaves a broken collection. Skipping steps 1 and 2 leaves the meta test red,
which is annoying and completely visible. The dangerous half is the register
edit, and it is the half under pressure: `board.py audit` exits 2 when a unit's
issue is closed while the register still owes it a module, so the visible
incentive at merge time points straight at deleting the entry. Nothing points at
the decorator.

**The trigger is usually cross branch, which is why nobody feels responsible.**
On the U16 merge, U24 had landed `cratekit.core.tombstone` on main while U16's
branch carried a guard gated on that module's absence. The countdown therefore
fired for a person who had not landed the module and was working in a different
unit. That is why METHOD files this under merge rules rather than authoring
rules.

## When to Apply

Every time a merge brings a module onto `main` that the register was waiting for.
Concretely:

- A branch's `@requires("X")` names a module that now exists on the merged tree.
  This fires without anyone deciding it should, because the branch predates the
  unit that landed X.
- `test_a_pending_target_that_has_landed_must_be_removed_from_the_registry` goes
  red for a key. That test is designed to fail this way.
- `board.py audit` exits 2. A closed issue whose unit still owes the register a
  module is the contradiction that exit reports.
- A merge conflict lands inside `tests/_pending.py`. Note the neighbouring METHOD
  rule: use git's merge algorithm only, because `diff3 -m` silently produces a
  broken merge of this same file. The register has now produced two distinct
  merge time traps, which is a fact about the file rather than about either trap.
  Treat it as the repository's highest risk merge surface.

The register carries ten entries today, gating thirteen decorator sites across
eight test files, so the average entry gates more than one site and the grep is
not optional. The two highest risk discharges ahead are
`cratekit.intake.collection_xml` and `cratekit.cli.doctor`, because each has
gated sites in two different files: a grep that stops at the first hit removes
one decorator, leaves the other, and the register edit takes the second file out
of collection.

## Examples

The U16 merge into `main`, 2026-08-13, merge commit `e2b5ce3`.

U24 had already landed `cratekit.core.tombstone` on `main`. U16's branch predated
that and carried its own byte for byte replica of the same identity algorithm,
plus a guard whose entire purpose was to compare the two copies once both lived
in one tree. That guard could not run on either branch alone, so it was gated:

```python
@requires("cratekit.core.tombstone")
def test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist():
    ...
```

At the merge the register entry was deleted, which is what both the register
docstring and the meta test demand. The suite was then run:

    KeyError: "'cratekit.core.tombstone' is not declared in _pending.PENDING. ..."
    ERROR collecting tests/test_match_states.py
    Interrupted: 1 error during collection

Not one failing test. One file, 330 tests, gone from collection, including the
guard the merge existed to arm.

With all three edits applied together, the guard ran for the first time in its
life and passed. What it was carrying: the tombstone kind against U24's own
constant, the store key, the fold over every pinned input, and the version
vocabulary whose two live answers had already caused a real miss, where a list
spelling reported MISSING and re-fetched a file that was already on the shelf.

That is what the 330 tests were holding. The half discharge would have removed
them and left the merge looking finished.

## The follow up this learning is still owed

**The instruction text a person reads at the moment of discharge is wrong, in
both places, and it is the proximate cause of both occurrences.**

There are **four** such strings, in two files:

1. `tests/_pending.py`, module docstring: when the meta test goes red, "the only
   way to make it green is to delete the entry, which arms the guard".
2. `tests/test_pending_units.py`, module docstring, point 2: "the only way to
   make it green is to delete the entry, which arms the guard. Nobody has to
   remember; forgetting is what fails."
3. `tests/test_pending_units.py`, the countdown test's docstring: "That single
   deletion arms every guard gated on it".
4. `tests/test_pending_units.py`, the assertion message a failing run actually
   prints, which tells the reader to remove the key from both sets and says
   "That arms the guard".

All four are false as written. The deletion does not arm the guard. It raises
`KeyError` at import and removes the guard's whole file from collection. None of
the four mentions the decorator, and the fourth is the one a person reads at the
exact moment they are acting.

Correcting those strings is the highest value follow up, because METHOD now
carries the right rule while the tooling still prints the wrong one. Scope the
work to all four; a fix that stops at the two obvious ones leaves the module
docstrings still teaching the wrong procedure.

Two smaller ones. The countdown table in `docs/HANDOFF.md` has drifted from the
register it copies: eleven targets across ten rows, because one row names two,
against the register's ten keys, with three dead targets and two current keys
missing entirely. And this rule now exists in METHOD, in RESTART, and in the wave
state, so those should become pointers to this document rather than a fourth and
fifth retelling that can disagree.

## Related

- `docs/METHOD.md`, "Committing and merging": the merge rule, added 2026-08-13 in
  commit `453af26`. This document is its explanatory home, so METHOD can shrink
  to a pointer in the trim pass the last wave state already asked for.
- `docs/METHOD.md`, driver rules: check the collected count on every row, never
  pass a second `-q`, and reconcile the collected count by identifier. The same
  defect class scoped to the mutation driver, plus the detection procedure.
- `docs/residual-findings.md`, R-21 item 5: the first occurrence, on the U36
  merge, with the correction about shape and size.
- `docs/residual-findings.md`, R-5: the origin of the register and the countdown
  obligation, still tracked as an open residual.
- `docs/residual-findings.md`, R-25: a countdown that arms correctly and still
  proves nothing, because the guard walks a syntax tree and a call under a false
  branch satisfies it. Arming the guard is not the end of the obligation.
- `docs/history/wave-state-2026-08-13.md`: the narrative record of the U16 merge.
- `tests/test_restore.py`: the one worked escape hatch in the tree, where an
  obligation was taken off the countdown entirely and rewritten as a test that
  asks what the build contains.
