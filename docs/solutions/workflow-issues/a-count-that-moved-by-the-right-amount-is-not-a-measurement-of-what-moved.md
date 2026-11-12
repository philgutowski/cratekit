---
title: "A count that moved by the right amount is not a measurement of what moved"
date: 2026-08-15
category: workflow-issues
module: tests/test_reserved_causes.py
problem_type: workflow_issue
component: testing_framework
severity: high
resolution_type: test_fix
applies_when:
  - "A test pins a population count as an exact tuple and METHOD requires re-measure and re-pin on every merge that touches it"
  - "A merge lands new members into a set the pin is supposed to protect"
  - "The set the pin covers is derived by a walk rather than named directly in source"
  - "A reconciliation counts members across a tree while the shell's cwd sits inside a worktree of that same tree"
  - "A pin's docstring argues a comparison between two halves of one population"
symptoms:
  - "A pinned tuple fails after a merge and the delta matches the unit's diff, so the tempting fix is to bump the number"
  - "A member leaving the set while another joins reads identically to no change at all"
  - "A reconciliation undercounts because the shell was silently inside a worktree of the same tree"
  - "The comment above a pin states a total without naming which members are new"
  - "A per-member check against git returns everything as new because the walk reports package-relative paths"
related_components:
  - development_workflow
  - documentation
tags:
  - re-pinning
  - test-fix
  - regression-testing
  - git-worktree
  - set-comparison
  - measurement
  - method-compliance
  - reconciliation
---

# A count that moved by the right amount is not a measurement of what moved

## Context

`tests/test_reserved_causes.py` ends with a test whose whole job is to keep the
numbers a residual argues from honest.
`test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
(`tests/test_reserved_causes.py:4592`) recomputes five populations from the
tree on every run and pins each as an exact tuple:

- the declared refusal causes, split into the non-reserved and reserved halves,
  `(len(causes), len(causes - CAUSES), len(CAUSES)) == (108, 85, 23)` (`:4647`);
- every kebab-shaped string literal in the package, and how many of those are
  not causes, `(len(literals), len(literals - set(causes))) == (282, 175)`
  (`:4667`);
- the modules holding a NAME that resolves to a declared cause, measured
  without and with each file's own enum declarations, and how many of the
  latter also hold an in-range integer,
  `(len(without), len(with_own), len(both)) == (8, 21, 12)` (`:4717`);
- the modules holding a cause LITERAL, and how many of those also hold an
  in-range integer, `(len(literal_holders), len(literal_both)) == (45, 14)`
  (`:4741`);
- and the sharpest single case, `core/exit_codes.py` (module paths in this
  document are spelled the way the walk reports them, relative to
  `src/cratekit/`, which matters later): its declared enum
  values, how many of those are also reserved causes, and its in-range
  integers, `== (45, 7, 28)` (`:4774`).

The docstring is explicit about what a failure means. "WHEN THIS FAILS, the fix
is to look and then to update BOTH this line and the residual's prose, which is
the review the numbers exist to trigger. It is not to widen the assertion"
(`:4603`). Every merge that lands a refusal cause moves at least one of these
tuples, so above each assertion sits a comment block that is a dated re-pin
history: U38 on 2026-08-10, U16 on 2026-08-13, U23 on 2026-08-14, and now U27 on
2026-08-15 (`:4616` onward, `:4650` onward, `:4696` onward, `:4723` onward,
`:4762` onward).

The three earlier re-pins were done by arithmetic. The U16 and U23 merge
sessions each read the failing tuple's new numbers, matched the delta to what
the unit's brief said it landed, "U16 added one cause slug, so the population
moved 100 to 101", and edited the tuple. Every one of those inferences happened
to be right, and none of them was a set difference (session history).

The U27 merge, "Merge U27: the setup wizard and the doctor, and a probe that
stopped opening for write" (5167f15, on `main`), moved all five. It was also the
first merge in four re-pins to move the reserved half of the cause population,
22 to 23, which is the half the docstring says the pin exists to protect. That
made it the wrong merge to re-pin by arithmetic, and the way it was re-pinned
instead is the learning here.

## Guidance

**A re-pin names its members. Difference sets, not counts.** `docs/METHOD.md`
already says every number was measured or the report says it was not
(`docs/METHOD.md:154`), and the test's own docstring already says never widen
(`tests/test_reserved_causes.py:4603`). Those two rules leave one gap, and it is
the gap a count falls into: a total that moved by the right amount is not a
measurement of what moved. A member leaving while another joins reads as no
change. Two joining while one leaves reads as one joining. A count that went
from 20 to 21 tells you a module joined and does not tell you which, and the
comment above the pin, if all it says is "20 to 21", has recorded that you did
not look. The comment is a ledger of what joined and what left at each merge,
and it should read like one: names, not deltas.

There are two techniques, and which one applies depends on whether the tree
exposes the set directly or a walk derives it.

**When the tree exposes the set directly, ask git per member.** The cause slugs
are string literals in `src`, so for each of the 108 declared causes the
question "did this exist before the merge" is one `git grep` against the
pre-merge commit. Run `git grep -q -F "<slug>" <pre-merge> -- src` for every
member of the merged set and collect the misses. At U27 that gave exactly five:
`grant-path-access`, `library-root-unreachable`, `path-locked`,
`path-permission-denied` and `path-read-only`. One of them, `grant-path-access`,
is the reservation the merge itself added to `src/cratekit/cli/exit_codes.py`
(`:257` for the comment explaining why only the merged tree could see the
obligation, `:279` for the entry), and that is why the reserved half moved for
the first time. The comment at `tests/test_reserved_causes.py:4630` says all of
that, by name, and says how it was measured.

**When a walk derives the set, run the same walk over the pre-merge tree and
difference the two sets.** `modules_holding_a_named_cause`
(`tests/test_reserved_causes.py:4524`) walks every module under measurement and
asks whether it holds a name resolving to a cause declared elsewhere. Nothing in
git answers that per member, because the answer depends on the whole tree's
declarations. So put the pre-merge commit in a scratch worktree, point
`PYTHONPATH` at that worktree's `src` and `tests`, import the test module there,
print the sorted set, and difference it against the same set from the merged
tree. At U27 that named `core/preflight.py` as the single module that joined,
and the comment at `:4709` records both the name and the method.

The first attempt at that difference failed for a reason worth keeping. It
tried to skip the worktree by asking `git cat-file -e <pre-merge>:<path>` for
each module in the merged set, and every module came back "new". The walk
reports package-relative paths (`acquire/adapter.py`) and git wants
repo-relative ones (`src/cratekit/acquire/adapter.py`). Nothing errored, the
list was just wrong. The derivation over the pre-merge tree is the robust form
because it uses the same code on both sides and never has to translate a path.

**The same shape applies to the halves that moved by more than one.** The
kebab literal population moved 270 to 282 and 168 to 175: twelve literals
landed, five of them the causes above and seven not causes at all (`:4661`).
The literal at-risk half moved 42 to 45, and the three new holders are exactly
the three modules the unit landed, `cli/doctor.py`, `cli/setup.py` and
`cli/verbs/login.py`, of which only `cli/doctor.py` also holds an in-range
integer (`:4734`). `core/exit_codes.py` went 42 to 45 declared enum values, and
the three are `GRANT_PATH_ACCESS`, `REMOUNT_WRITABLE` and `UNLOCK_PATH`
(`src/cratekit/core/exit_codes.py:156`, `:162`, `:166`), the three acts round
eight split one instruction into; reserved-also moved 6 to 7 because only the
first is a reserved cause, and the integers stayed at 28 (`:4762`). Each of
those comments names its members. "Twelve literals" alone would have been a
count.

**Trap paid for: check which checkout the shell is in before counting
anything.** The first collected-count reconciliation for this same merge was
run from a shell whose working directory had silently stayed inside
`.worktrees/u27` after an earlier `cd`, a worktree that no longer exists
because it was removed once the merge landed. `pytest --collect-only` therefore
counted the BRANCH, 3452 tests, while the union of both sides was 5966, and the
"lost" list came back hundreds long. Nothing errored, no path in the output
looked wrong, and the numbers were internally consistent. Run
`git rev-parse --show-toplevel` in the same shell you are about to count from,
read what it prints, and if it is not the checkout you meant, rerun from the one
you meant rather than reasoning about the difference. `RESTART-cratekit.md:116`
carries the same warning for the collected count; it applies to every one of
these measurements.

## Why This Matters

The pins exist because six figures in a residual once decayed silently while
the tree grew, and the test's docstring says the unit "filed that one against
itself twice" (`tests/test_reserved_causes.py:4599`). A pin that is re-pinned by
matching totals reintroduces the same decay one level up: the assertion is
green, the comment says the number moved, and nobody can say from the record
whether the reserved half grew because a reservation was added or because one
left and two joined. The reserved half is the half the docstring's whole
argument rests on. At U27 it moved for the first time, and the only reason the
comment can say "this is not the routine bump" and mean it is that the five
members were named and one of them was traced to its reservation.

The named-cause pin makes the point sharper. Its without-own half has been 8
across five measurements and four merges (`:4715`), and that stability is the
evidence that no module has gained a name resolving to a cause declared
elsewhere. A count of 8 that hides one leaving and one joining would look
identical and mean the opposite. The set difference is what makes "still 8" a
claim rather than a coincidence.

There is a general form of this that reaches beyond this one test. Cratekit's
method is that a number in a document is either measured or marked as not
measured. A re-pin is the moment a measured number is replaced with another,
and the replacement is only measured if it can say what changed. Two numbers
that agree on a delta are not the same measurement.

## When to Apply

- Any merge turns `test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  red. The fix is to name the members that moved in each tuple, write them into
  the comment above the pin, update the residual's prose, and only then change
  the tuple.
- Any pinned population anywhere in the suite moves and the tempting fix is to
  bump the number because the delta matches the unit's diff.
- A count is stable across a merge and you are about to write "unchanged". Say
  how you know nothing left and nothing joined, or difference the sets.
- A per-member git check is possible because the members are literals in the
  tree. Prefer it; it is one command per member and needs no worktree.
- A per-member git check is not possible because the set is derived by a walk
  that reads the whole tree. Use the scratch worktree and run the same
  derivation on both sides.
- You are about to count anything from a shell that has moved between a
  worktree and the main checkout. Print the toplevel first.

## Examples

Per-member check for a set the tree exposes directly. Run from the merged
checkout, with `<pre-merge>` being the commit `main` was on before the merge:

```sh
cd /path/to/Cratekit
.venv/bin/python -c '
import sys; sys.path.insert(0, "tests")
from test_reserved_causes import declared_causes
print("\n".join(sorted(declared_causes())))
' > .scratch/causes-after.txt
while read -r slug; do
  git grep -q -F "$slug" <pre-merge> -- src || echo "NEW $slug"
done < .scratch/causes-after.txt
```

Set difference for a set a walk derives. Cut the scratch worktree before
merging, or from the pre-merge commit after. Since U258 the helper takes the
package sources its caller read once, and before it took none, so the recipe
asks the signature and works on either side of that change:

```sh
cd /path/to/Cratekit
git worktree add --detach .scratch/pre-merge <pre-merge>
PYTHONPATH=.scratch/pre-merge/src:.scratch/pre-merge/tests \
  .venv/bin/python -c '
import inspect
from test_reserved_causes import modules_holding_a_named_cause as named, package_sources
given = (package_sources(),) if "sources" in inspect.signature(named).parameters else ()
print("\n".join(sorted(named(*given, own_declarations=True))))
' > .scratch/named-before.txt
PYTHONPATH=src:tests .venv/bin/python -c '
import inspect
from test_reserved_causes import modules_holding_a_named_cause as named, package_sources
given = (package_sources(),) if "sources" in inspect.signature(named).parameters else ()
print("\n".join(sorted(named(*given, own_declarations=True))))
' > .scratch/named-after.txt
diff .scratch/named-before.txt .scratch/named-after.txt
git worktree remove .scratch/pre-merge
```

Confirm `git rev-parse --show-toplevel` prints the main checkout before either
of those, and remember the walk reports package-relative paths, so do not hand
its output to `git cat-file` without prefixing `src/cratekit/`.

The comment to copy, from `tests/test_reserved_causes.py:4709`:

```
# Re-pinned again on the U27 merge, 2026-08-15: core/preflight.py is the one
# module added, taking the with-own half from 20 to 21 and the also-holds-an
# -integer half from 11 to 12. Named rather than counted, and measured by
# running this same derivation over main's own tree in a scratch worktree and
# differencing the two SETS, because a count moving by one says a module
# joined and does not say which, and a module leaving while another joined
# reads identically. THE WITHOUT-OWN HALF IS STILL 8, now across five
# measurements and four merges.
```

Date, member names, the new figures, the method, and what did not move. That is
the shape.

## Related

- `docs/METHOD.md:154`, "Every number was measured or the report says it was
  not." This learning is the re-pin corollary: a number replaced by matching a
  delta was not measured.
- `tests/test_reserved_causes.py:4603`, the docstring rule that a failing pin is
  updated after looking, never widened.
- `RESTART-cratekit.md:128`, "Re-pinning a population means naming what moved,
  not matching a count", the wave-state form of this rule, and `:116` for the
  collected-count reconciliation and the cwd trap.
- `tests/test_reserved_causes.py:4592`, the test itself, and its comment blocks
  at `:4616`, `:4650`, `:4696`, `:4723` and `:4762`, which are the ledger.
- Merge commit "Merge U27: the setup wizard and the doctor, and a probe that
  stopped opening for write", 5167f15 on `main`, the re-pin this was learned on.
- `docs/solutions/workflow-issues/merge-falsifies-a-guard-invariant-and-every-remedy-breaks-something.md`,
  the closest sibling: a structural guard whose argument a merge falsifies when
  neither branch did alone. That one is about a guard whose remedies all break
  something; this one is about a pin whose remedy is easy and the honesty of
  the remedy is the whole question.
- `docs/solutions/workflow-issues/a-cause-read-from-a-log-is-not-a-cause-driven-by-reproducing-it.md`,
  the same session's other learning about a number carried rather than
  measured, there a count of platform failures read from a run list.
