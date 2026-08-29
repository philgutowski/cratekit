---
title: "A zero death row can be a test gap or an inert mutation, and the table cannot tell you which"
date: 2026-08-23
category: workflow-issues
module: scripts/mutate.py
problem_type: workflow_issue
component: testing_framework
severity: high
resolution_type: workflow_improvement
applies_when:
  - "A mutation table row reports zero deaths and is about to be classified as an untested guard"
  - "A mutation row deletes a keyword argument whose value equals the callee's own default"
  - "A user facing zero is about to be paired with a composite under METHOD's severity floor"
  - "A zero row is about to be promoted to a full suite run, which every zero in this driver is"
  - "A zero row is about to be written into docs/residual-findings.md as a known and accepted finding"
symptoms:
  - "A row deletes an explicit keyword argument and kills nothing because the callee's default already equals the deleted value"
  - "The zero is written up as an untested guard when the guard it appears to indict does not exist"
  - "A composite written to satisfy the user facing zero rule changes no evidence, because both trees behave identically"
  - "A full suite run is spent promoting a zero that could not have moved"
  - "The inert row sits on top of a genuine missing guard, and reading it as a test gap walks past that guard"
related_components:
  - development_workflow
  - documentation
  - testing_framework
tags:
  - mutation-testing
  - zero-row
  - inert-mutation
  - mutation-table
  - test-fidelity
  - method-compliance
---

# A zero death row can be a test gap or an inert mutation, and the table cannot tell you which

## Context

U27 landed the four report verbs and the two engines nothing in the tree had, and
it merged to `main` as `67a3d0a`. The author's light mutation pass on the reports
shell is `docs/mutation/u27-reports-round-1.md`: twenty three rows plus the
generated null control, thirty two pytest invocations, a green baseline of 6115
collected, measured on branch `unit/u27-reports-cli` at `3ee992f`.

Four of the twenty three rows measured zero deaths, and all four were classified
`user` facing, so the table's own "Zero rows and what they owe" section printed
the same sentence four times: `USER FACING ZERO WITH NO COMPOSITE: pair it or
reclassify it`. The four are `C3_uncovered_order`, `L2_genre_parent`,
`S5_handler_key` and `D1_probe_creates`.

Three of them were real. `C3_uncovered_order` dropped
`uncovered=tuple(sorted(uncovered, key=_by_name))` and killed nothing because the
test that was supposed to hold the order compared two reads of one document and
required them to agree, which the deterministic walk satisfies for free
(`tests/modules/test_reports_engines.py:198`, whose docstring now says "THE
VERSION THIS REPLACES MEASURED NOTHING"). `L2_genre_parent` loosened
`folder[-2] != tree_display` to `tree_display not in folder` and killed nothing
because every fixture in that module was exactly three deep, and at that depth
the two rules agree (`tests/modules/test_reports_engines.py:415`).
`D1_probe_creates` flipped `trash.probe(path, create=False)` to `create=True` at
`src/cratekit/cli/doctor.py:455` and killed nothing because the guard watched a
temporary directory for a created folder, and on macOS `layout_for` resolves that
directory's volume root to `/`, so the create was refused by the filesystem
rather than by the argument under test (`tests/test_doctor.py:2449`).

The fourth was not a test gap at all, and round one read it as one.

`S5_handler_key` deleted `handler_key=ctx.entry.handler_key` from the shell's
call into the duplicates engine. The row's own description says what it believed
it was measuring: "Offer duplicate items without the verb's handler key, so the
queue cannot show them by name". It measured zero, and the zero was correct,
because the mutated tree behaves exactly like the original. That is an **inert
mutation**: a row whose new text is semantically identical to its old text on
this tree, so the row is not a failed measurement, it is not a measurement.

## Guidance

**Before believing a zero, ask whether the mutated expression's value actually
differs from the original on the tree under test.** A zero has two possible
causes and the table renders them identically. Either the suite does not notice a
real behaviour change, which is a finding, or there was no behaviour change to
notice, which is nothing at all. `scripts/mutate.py` reports `kills=0` for both,
prints the same "pair it or reclassify it" line for both, and has no way to tell
them apart, because distinguishing them requires reading the surrounding code
rather than counting failures.

Three inert shapes are worth recognising by sight:

- **Deleting an argument that equals its own default.** This is the U27 case and
  it is the easiest one to author by accident, because the deletion looks like a
  real subtraction and the default sits in a different file.
- **Replacing a constant with an alias of itself.** Two names bound to one value,
  or a literal swapped for the constant that spells it.
- **Reordering operations that commute.** A sort key permuted where the fields
  are independent, a filter and a map exchanged where neither has an effect, two
  appends to a set.

**An inert row is not a residual, and filing it as one is worse than dropping
it.** `docs/METHOD.md:33` lists "a guard that kills zero tests" among the real
problems that get recorded in `docs/residual-findings.md` rather than holding a
merge. That is right for the three genuine zeros. Applied to an inert row it
writes a claimed test gap into the ledger that never existed, and the ledger is
the register a later session trusts when it decides what is known.

**An inert row cannot be closed by writing a test, and that is the diagnostic.**
If you sit down to write the test that would kill the row and find you cannot
state what behaviour it would assert, the row is inert. No test can distinguish
two trees that behave the same. The remedy is to replace the row with one that
moves something, and to run it.

**METHOD's composite rule does not apply, and following it manufactures
evidence.** `docs/METHOD.md:101` says a user facing zero "is acceptable only when
a composite shows what it does hold. Pair it with a mutation of the thing it
guards and report both counts. A prose argument is not evidence." The rule
assumes there is a guard. For `S5_handler_key` the guard it appeared to indict
did not exist, so a composite would have been a pair of counts documenting a
property nobody had. Reclassifying it to maintainer facing under
`docs/METHOD.md:105`, "a zero row on a maintainer facing guard gets one line, not
a composite", is the same evasion one word smaller.

**Look for what the inertness is telling you, because it is usually telling you
something.** An argument equal to its own default means one value is spelled in
two places, and two copies of one string agreeing is an invariant nothing was
comparing. `docs/METHOD.md:183` already carries "one symbol meaning two things in
two modules" on the list of what a green suite cannot see. This is its mirror,
two symbols meaning one thing in two modules, and the inert row is the thing that
points at it.

**Count the cost before you shrug.** `scripts/mutate.py:127` is explicit: "Promote
a zero to a full suite run before reporting it as a zero. A death on a subset is
a real death, so a killing row stops there and stays cheap. A zero on a subset is
only a zero within that subset. Promoted zeros are marked as promoted in the
output." Every zero therefore buys a full suite run. An inert zero buys one for a
measurement that could not have moved.

## Why This Matters

The driver already knows inert mutations exist. It builds one on purpose, once
per batch. `scripts/mutate.py:144` describes it: "A NULL CONTROL row, generated
automatically, which appends a comment line to a Python target. It changes
nothing semantically, so it MUST kill zero. If it kills anything, the measuring
apparatus is broken rather than the code, the batch is declared invalid and the
run stops." The constant it appends is `NULL_CONTROL_COMMENT` at
`scripts/mutate.py:210`, and round one's control killed 0 against 6115 collected,
which is the line that makes the rest of the table believable.

So the batch contains exactly one row whose zero is known to mean "nothing
changed", and it is the row the driver wrote. Every other zero is read under the
opposite assumption. `scripts/mutate.py:21` states that assumption as a plain
fact: "A guard whose removal kills zero tests is not tested, whatever the
coverage report says, because coverage measures which lines RAN and a mutation
table measures which lines MATTER." `docs/METHOD.md:71` states it again at the
top of the mutation table section: "Revert each new guard one at a time, run the
suite, count the deaths. A guard that kills zero tests is a finding." Both
sentences carry an unstated premise, that the revert produced a tree that behaves
differently, and neither the driver nor METHOD says so anywhere. The whole
mutation table section of METHOD, from `:69` through `:114`, covers scoping, row
caps, subset promotion, author bias, the user facing composite, the maintainer
facing one line, and writing the table into the repository. It says nothing about
inertness. The null control is the concept implemented and never named.

The consequence is a specific misreading, and round one made it. `kills=0` on
`S5_handler_key` was read as "this guard is untested", which puts a false entry
into whichever register the round writes to and points the next round at work
that does not exist. It also hides the real work. The reason the row was inert is
that `src/cratekit/modules/reports/duplicates.py:101` spells `HANDLER_KEY =
"audit.duplicates"` and `src/cratekit/cli/registry.py:1074` spells
`handler_key="audit.duplicates"` on the entry named at `:984`, and nothing in the
suite compared them. That drift is silent when it happens, because the review
queue accepts items under any key and an item filed under a key no verb name
resolves is simply invisible to the one query a person has. The inert row was
sitting on top of a genuine missing guard and reading it as a test gap in the
shell walked straight past it.

The scale is the argument for writing this down. One light pass on one unit
produced four zeros, and the ratio was three to one. Zeros are not rare here:
`docs/METHOD.md:39` says a mutation table over a suite this size "always finds a
zero death row, because that is a property of large test suites rather than of
any branch", and `:107` through `:108` records one verifier producing forty zero rows in a
single pass. At forty rows, a one in four inertness rate is ten rows of invented
findings, each one having cost a full suite run to produce.

## When to Apply

- Any row in a mutation table measures zero. Before classifying it, read the
  mutated site with its surroundings and say what the two trees do differently.
  If you cannot say, the row is inert.
- A row deletes a keyword argument. Find the callee's signature and check the
  parameter's default against the value being deleted. `handler_key` in
  `src/cratekit/modules/reports/duplicates.py:315` and again in `:276` is the
  worked case, and the value flows through two defaults rather than one.
- A row swaps one constant for another name. Check whether both names resolve to
  the same object.
- A row reorders anything. Check whether the operations commute on the fixtures
  the subset actually runs.
- You are about to write a composite for a user facing zero under
  `docs/METHOD.md:101`. Confirm the guard exists first. A composite over a
  nonexistent guard is the prose argument that rule forbids, wearing counts.
- You are about to file a zero into `docs/residual-findings.md`. An inert row
  does not go in the ledger, because the ledger is a register of what is known
  and accepted and an inert row is neither.
- A zero row's remedy is obvious and you cannot state the assertion the remedy's
  test would make. Stop and re-read the mutation.

## Examples

Round one's `S5_handler_key`, in full. The old text at
`src/cratekit/cli/reports.py:267`, inside `audit_duplicates` at `:254`:

```python
        report = duplicates.audit_and_offer(
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
        )
```

The new text, with the argument deleted:

```python
        report = duplicates.audit_and_offer(
            view, store, template=_template(cfg)
        )
```

`ctx.entry` is the registry entry named `audit.duplicates`
(`src/cratekit/cli/registry.py:1070`), whose `handler_key` is the string
`"audit.duplicates"` (`:988`). The callee is
`src/cratekit/modules/reports/duplicates.py:310`, whose parameter is
`handler_key: str = HANDLER_KEY` (`:315`), and `HANDLER_KEY` is the string
`"audit.duplicates"` (`:101`). Delete the argument and the parameter takes a
default equal to the argument deleted. The row ran on the full suite, because the
subset derivation found no test file importing `cratekit.cli.reports` on that
tree, and reported "Collected: 6115 against a baseline of 6115. Kills: 0 (zero)".
Correct, and worth nothing.

Round two, `docs/mutation/u27-reports-round-2.md`, replaced that one row with two
that are not inert, and every row in that table killed. The first passes a wrong
key from the shell rather than deleting the argument:

```python
            view, store, template=_template(cfg), handler_key="duplicates"
```

`S5_handler_key_wrong` killed 2 on a subset of 22, both in
`tests/test_reports_cli.py`:
`test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key` and
`test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default`.

The second drifts the engine's own copy of the key away from the registry's,
which is the failure the two spellings actually admit:

```python
HANDLER_KEY = "duplicates.audit"
```

`S5b_engine_default_drift` killed 3 on a subset of 371, across
`tests/modules/test_reports.py:781`, `:800` and
`tests/test_reports_cli.py:264`.

That third kill is the guard the inert row had hidden the need for, and it is
three lines of assertion with a docstring that is longer than the test
(`tests/test_reports_cli.py:264`):

```python
def test_the_two_copies_of_the_duplicate_handler_key_cannot_drift():
    """One verb name lives in two modules, and nothing compared them.
    ...
    They are the same string today, which is exactly why the author's mutation
    table measured ZERO for dropping the shell's argument: the mutation was
    semantically inert on this tree, so the row said nothing about the wiring.
    """
    assert duplicates.HANDLER_KEY == registry.entry("audit.duplicates").handler_key
```

The wiring itself, the thing the deleted argument was supposed to be about, is
driven separately at `tests/test_reports_cli.py:279` by wrapping
`duplicates.audit_and_offer` with `monkeypatch`, running the real verb, and
asserting `seen == [registry.entry("audit.duplicates").handler_key]`. Its
docstring says why the mutation could never have reached it: "The engine's
parameter is a default evaluated when the function is defined, so replacing the
module constant proves nothing. Wrapping the call and reading what the shell
actually handed it does."

For contrast, the three genuine zeros were closed exactly the way METHOD expects,
by writing tests. Round two re-ran each against its replacement guard and each
killed: `C3_uncovered_order` 2, `L2_genre_parent` 2, `D1_probe_creates` 1. Six
rows, twelve pytest invocations, a 6120 baseline, and no zeros left. The
difference in method is the whole point. Three rows were answered with tests.
The fourth could not be, and was answered by replacing the measurement.

## Related

- `docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md`,
  the closest sibling and the same family as `D1_probe_creates`: a green signal
  that measures nothing, there because a file left collection entirely, here
  because a guard passed for a reason unrelated to its property. `D1` watched a
  temporary directory for a folder the filesystem was always going to refuse, and
  `C3_uncovered_order` asserted that two reads of one document agree, which a
  deterministic walk gives away for free. Both are guards that ran and held
  nothing. An inert mutation is the third member of that family, one level up: a
  measurement that ran and held nothing.
- `docs/METHOD.md:69` through `:114`, "The mutation table". The section this
  learning is missing from, including `:71` on a zero being a finding, `:101` on
  the user facing composite and `:105` on the maintainer facing one line.
- `docs/METHOD.md:33`, the residual rule that would have taken the inert row into
  `docs/residual-findings.md` as an accepted gap.
- `docs/METHOD.md:183`, "one symbol meaning two things in two modules", on the
  list of what a green suite cannot see. The U27 case is its mirror, and the
  inert row is what pointed at it.
- `scripts/mutate.py:16` onward for what a mutation table is, `:127` for the
  promotion rule that makes every zero cost a full suite, and `:144` with `:210`
  for the null control, which is an inert mutation the driver builds on purpose
  and the only zero in a batch whose meaning is known.
- `docs/mutation/u27-reports-round-1.md` and
  `docs/mutation/u27-reports-round-2.md`, the two tables. Round one is where the
  inert row was measured and misread; round two is the replacement.
- Merge commit `67a3d0a`, "merge: U27 report verbs and the two engines nothing in
  the tree had", the merge this landed on.
