---
title: "A fixture in a position where the mutated line cannot matter fails red first, and the obvious repair makes the guard green on both trees"
date: 2026-08-27
category: workflow-issues
module: "src/cratekit/setbuilder/cli.py, tests/test_setbuilder_cli.py, src/cratekit/core/naming.py, docs/mutation/u43-author-light.toml, docs/mutation/u43-round-2-rows.toml"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A test is being written specifically to close a mutation table's zero death row"
  - "A guard written to close a zero row comes back RED on the unmutated tree and the obvious repair is to assert the value the code just produced"
  - "The property under test depends on WHERE a value sits in a string, a path or a list rather than on whether it is present"
  - "The property under test is a bound, a cap or a threshold, and the fixture supplies the population the bound is applied to"
  - "A fixture helper is being copied to make a marked, tagged or decorated variant of an existing one"
symptoms:
  - "A mutation row measures zero, a guard is written for it, and the guard fails red on correct code for reasons that look like a wrong expectation"
  - "Repairing the expected value to what the code printed makes the guard green under both the correct and the mutated tree"
  - "The fixture never puts the system into the state where the mutated line can change the observed value"
  - "A cap assertion holds whether or not the cap is applied, because the fixture supplies fewer items than the cap"
  - "An author's mutation table and an independent adversarial review both return clean over a surface whose fixtures cannot reach the defect"
related_components:
  - development_workflow
  - documentation
tags:
  - mutation-testing
  - zero-row
  - test-fixture
  - fixture-position
  - test-fidelity
  - characterization
  - guard
---

# A fixture in a position where the mutated line cannot matter fails red first, and the obvious repair makes the guard green on both trees

## Context

U43 gave the set building engine its command line surface. The engine landed in
U35 as `src/cratekit/modules/tools/setbuilder.py` and had no verb over it, so U43
wrote `crate setbuild`, a read only shell at `src/cratekit/setbuilder/cli.py`. It
merged to `main` as `2fa9efc`, "merge: the setbuild shell, and the anchor that is
a path rather than a title", closing issue #61. This repository forbids pull
requests by contract (`CLAUDE.md`, "No pull requests. Feature branch per unit,
merge to `main` locally, push `main`, delete the branch"), so the merge commit is
the citation and there is no PR number.

The author's round one table is `docs/mutation/u43-author-light.md`, run from
`docs/mutation/u43-author-light.toml` on branch
`unit/u43-the-setbuild-command-line-shell-row-29` at `17b758d`. A light pass, 25
rows against METHOD's cap of 25, a green baseline of 6351 collected, and a null
control that killed 0 of 6351. Tallied from the table's own verdict column: **17
killed, 7 zero, 1 collect error.** One of the seven zeros is the null control, so
six are real, and all six are on a user facing surface. The table's "Zero rows and
what they owe" section prints the driver's standing sentence for each of the six:
`USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it`.

**THE PROSE AROUND THIS UNIT GOT THOSE COUNTS WRONG AND THE TABLE IS THE
MEASUREMENT.** The closing commit `d285a46` opens "Round one of the mutation table
measured 25 rows: 18 killed, one collect drift, and six zeros of which one is the
null control", the merge commit repeats it, and the round two spec's header
comment says "The five user facing zeros from round one" while the file then
defines six re-measurements (`docs/mutation/u43-round-2-rows.toml`). Every one of
those totals 25 and every one puts a row on the wrong side of the killed and zero
line. Recorded here rather than quietly corrected, because a number recalled into
a commit message and then repeated three times is the ordinary way a wrong figure
becomes the record.

One of the six is the subject of this doc. `H4_template_loses_the_marker` mutates
the single return of `_template` at `src/cratekit/setbuilder/cli.py:90`:

```python
    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))
```

to

```python
    return NameTemplate()
```

Round one reported "Collected: 6351 against a baseline of 6351. Kills: 0 (zero)",
promoted to the full suite per `docs/METHOD.md:90`. Nothing in the suite carried a
lossy marked fixture at all, so the template's marker declaration was decoration
as far as any test could tell.

**THE MISTAKE WAS MADE WHILE CLOSING THE ROW, NOT WHILE WRITING THE CODE.** The
first fixture written for H4 put the lossy marker at the END of the title tag,
spelling the companion's title `08A - 124 - Lossy Companion [MP3]`. That looks
like a marked file and reads like one. It is in the one position where the
declared template's marker rule has no effect at all.

## Guidance

**WHEN A TEST YOU WROTE TO KILL A ZERO ROW COMES BACK RED, DO NOT REPAIR THE
EXPECTATION UNTIL YOU HAVE DRIVEN BOTH TREES.** This is the diagnostic and it is
the part that is easy to get backwards. A dead position fixture does not announce
itself by passing suspiciously. It announces itself as an ordinary red assertion
on correct code, which is the most familiar failure in testing and has the most
familiar repair: change the expected value to the one the code actually produced.

Driven on 2026-08-27 against the current tree through
`cratekit.modules.tools.setbuilder.parse_entry`, with the marker at the end of the
title:

- marker declared, parsed title `'Lossy Companion [MP3]'`
- marker undeclared, parsed title `'Lossy Companion [MP3]'`

The assertion actually shipped is exact set membership,
`assert "Lossy Companion" in titles` (`tests/test_setbuilder_cli.py:630`). On that
fixture it is FALSE on both trees. So the sequence a person actually walks is:
write the guard, run it, watch it go red on correct code, conclude the expectation
was wrong, change it to `'Lossy Companion [MP3]'`, and now hold a guard that is
green on both trees and looks like a closed row.

**The failure mode is not a guard that silently passed. It is a guard that failed
for a reason indistinguishable from an ordinary wrong expectation, whose cheapest
repair converts a dead fixture into a permanently green assertion nobody will
revisit.**

**BEFORE WRITING THE ASSERTION, FIND WHERE THE PRODUCTION CODE PUTS THE THING, AND
PUT THE FIXTURE THERE.** For a marker the answer is one line of the renderer
(`src/cratekit/core/naming.py:705`), and it says the marker follows the head
terminator rather than trailing the name. The fixture that discriminates spells the
title `08A - 124 - [MP3] Lossy Companion`. Driven the same way:

- marker declared, parsed title `'Lossy Companion'`, match key
  `'birch lossy companion'`
- marker undeclared, parsed title `'[MP3] Lossy Companion'`, match key
  `'birch mp3 lossy companion'`

Different on the two trees, so the guard discriminates, and round two reports H4
killed with 1 kill.

**A TEST WRITTEN TO KILL A ZERO ROW OWES A MUTATION ROW THAT BREAKS THE TEST'S
PREMISE, NOT ONLY THE CODE'S.** The row already there mutates the line under test.
What it cannot tell you is whether the fixture put the system into a state where
that line is reachable. Those are two different claims and only one of them is
measured by re-running the original row.

Round two added three rows whose whole job is to break the premise of a guard
written in the same round. All three are defined in
`docs/mutation/u43-round-2-rows.toml` and measured in
`docs/mutation/u43-author-round-2.md`:

- `V2_marker_position_moved` changes the declared literal to `"[NOTAMARKER]"`, a
  string the fixture does not contain. A lossy guard whose fixture sits in the
  dead position survives this. Measured: 1 kill, by
  `test_a_lossy_marked_companion_comes_back_with_a_clean_title`.
- `V1_pool_total_is_the_union` reports the union size where the payload says
  pool. Measured: 1 kill, by `test_a_count_caps_the_companions`.
- `V3_root_check_reports_instead_of_refusing` turns the missing root refusal into
  an empty plan and an OK exit, so a guard that only catches the crash shape
  survives it. Measured: 1 kill, by
  `test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`.

The recipe is three questions, one per shape. What literal, position or key does
this fixture depend on, and what happens to the guard if the code stops using it
(V2). What population does this fixture supply, and is it large enough for the
bound under test to bite (V1, and the size case below). What FORM of failure does
the guard catch, and is the defect's real form the same one (V3).

**BE PRECISE ABOUT WHAT THE VALIDATION ROW BUYS, BECAUSE RE-RUNNING THE ORIGINAL
ROW IS ALREADY A DETECTOR.** Had the dead position fixture shipped with a repaired
expectation, H4 would have reported zero again in round two, because a guard green
on both trees kills nothing. So the cheap detector catches this too. What the
validation row adds is a pin on WHY the guard dies. H4 removes the marker
declaration entirely, which also removes the marker only pattern that
`_leading_head_res` appends when `template.markers` is non empty
(`src/cratekit/core/naming.py:355` through `:359`), so a guard could in principle
die to H4 through the shape of the template rather than through the literal. V2
keeps a marker rule and changes only the string, which leaves nothing else to
credit.

**FIXTURE SIZE IS THE SECOND SPELLING OF THE SAME DEFECT AND IT LOOKS IDENTICAL.**
`P6_count_ignored` drops the count on the way to the engine, from `count=count` to
`count=None`, and measured zero in round one. Nothing was in a dead position there.
The fixture was simply too small for the bound to bite. Both spellings present as a
guard that exists, runs, and holds nothing.

## Why This Matters

**THE MECHANISM IS THAT THE HEAD PARSER IS ANCHORED AT THE START OF THE STRING, SO
A MARKER ANYWHERE ELSE IS OUT OF ITS REACH.** The renderer writes the marker
immediately after the head terminator (`src/cratekit/core/naming.py:705`):

```python
    return template.head_sep.join(parts) + template.head_term + markers
```

The stripper is built to match that shape and only that shape.
`_leading_head_res` (`src/cratekit/core/naming.py:339`) compiles one pattern per
emittable head shape, each assembled at `:354` as:

```python
        out.append(re.compile(rf"^\s*{body}{term}{markers}"))
```

The `^` is the whole story. The marker sub pattern comes from `_marker_pattern` at
`:328` and is a concatenation of optional groups appended AFTER the head
terminator. A marker sitting past the title is not at the start, not adjacent to
the terminator, and therefore never inside the span the match consumes.
`split_head` (`:461`) slices exactly that span, so whatever the pattern did not
consume stays in the remainder. The trailing head patterns are no help either:
they compile `rf"{sep}{body}\s*$"` at `:377`, with no marker term in them at all.

That is why the two trees are byte identical on the bad fixture and different on
the good one. `parse_entry` calls `split_head` and takes the remainder as the clean
title (`src/cratekit/modules/tools/setbuilder.py:301` through `:303`), then derives
the match key from that same clean title at `:320`. On the end position fixture the
marker was never in the head's reach, so declaring it or not changes neither value.

**THE COST OF AN UNSTRIPPED MARKER IS RECORDED IN THE SOURCE AND IT IS NOT
COSMETIC.** `_marker_pattern`'s own docstring is the best available evidence that
this guard is worth having:

> A stripper that left the marker behind is why a marked lossy copy and its
> lossless twin produced different match keys, so both landed in one playlist as
> duplicates instead of deduping against each other.

The drive above shows the shell reproducing exactly that: with the marker declared
the match key is `'birch lossy companion'`, without it
`'birch mp3 lossy companion'`. Two keys for one piece of music.

**A GREEN GUARD HERE IS WORSE THAN A ZERO ROW LEFT OPEN, AND THE REPOSITORY
ALREADY SAYS SO IN A NEIGHBOURING REGISTER.** `RESTART-cratekit.md` carries the
warning under "AND SO IS A CLOSURE, WHICH COST MORE":

> A test written to make a zero row die, whose expected value was read off what
> the code already does rather than off a decision about what it should do, is not
> a guard. It is a characterization of the defect wearing a guard's costume, and it
> converts an open question into a green assertion nobody will revisit. That is how
> R-168 hid for a day inside a row reported as closed.

**The fixture branch is how a person arrives at that trap without ever intending
to.** Nobody sets out to read the expected value off the code. They set out to
write a guard, hit a red assertion, and repair it the way red assertions are
normally repaired. The dead position fixture is what makes the repair produce a
characterization, because on that fixture the value the code produces is the only
value any tree produces. An open zero row is a known gap sitting in the table with
a sentence saying it owes a composite. A closed row with a characterization is a
gap with the sentence removed.

**THIS IS THE BRANCH A MUTATION TABLE STRUCTURALLY CANNOT CATCH, AND THE CORPUS
HAS THE PROOF ALREADY** (session history). U39's instance was not found by a
mutation row at all. The author's own table came back clean, an INDEPENDENT 22 row
adversarial review came back CLEAN, and the defect surfaced only when somebody drove
the shipped verb against real library files. `_spec_for` in
`src/cratekit/write/naming_cli.py` was collapsing `NameSpec.title` and
`NameSpec.stem` onto one value, and every fixture ever written for that surface
synthesized both from the same source string, so the collapse was unobservable by
construction. Only a case where the title tag is deliberately SHORTER than the
filename body exposes it. That became R-168 and the brief for U41.

That is the argument for taking this branch seriously: a table measures what its
fixtures can observe, so a fixture that cannot reach a state makes every row about
that state report the same honest, uninformative number. Independence of the
reviewer does not help, because an independent reviewer writes rows against the
same fixtures.

**A NUMBER FROM THAT INSTANCE IS AN EXTRAPOLATION AND IS CITED ELSEWHERE AS A
COUNT** (session history). The neighbour doc says U39's defect "would have stripped
the artist from roughly 9,800 real files". The session measured 149 of 150 on a
sample against a library of 9,867 audio files, and a later U41 sample of 500 found
only 5 where the tag body equalled the filename body. The extrapolation is
defensible and it is an extrapolation. Repeat it as one.

**IT IS A NEIGHBOUR OF METHOD'S FOURTH RECURRING DEFECT PATTERN RATHER THAN AN
INSTANCE OF IT.** `docs/METHOD.md` states the fourth pattern as "A fix justified by
a measurement taken on a fixture rather than on the tree. The most dangerous,
because it arrives with a confident number, a defensible argument and a green
suite."

Argue it both ways before answering. In favour of calling this an instance: the
guard was authored alongside the closure it justifies, and a green subset is
exactly the "green suite" the pattern names. Against: the justifying number in this
workflow is a mutation kill count, and that count is taken on the tree by
construction, since `scripts/mutate.py` edits the real source and runs the real
suite. The number a dead position fixture produces is zero, not a false one.

So the fourth pattern's own question, "was this taken on the tree", returns the
right answer here and still does not save you. The answer is neighbour. The fourth
pattern warns that a number measured on something authored alongside the fix is not
evidence about the tree. This case says a number measured honestly ON the tree is
still not evidence about the property, because **the fixture bounds which states
the tree can be asked about, and a state the fixture cannot reach is a state no row
can measure.** The companion question is one step earlier: not only was this number
taken on the tree, but could the fixture the suite runs on ever have reached the
line the number is about.

**METHOD ALREADY SAYS THE ZERO IS A FINDING AND SAYS WHAT A USER FACING ZERO
OWES.** `docs/METHOD.md:71` through `:72`: "A guard that kills zero tests is a
finding."
`docs/METHOD.md:101` through `:103`: "A zero death row on a guard with a USER
FACING surface is acceptable only when a composite shows what it does hold. Pair it
with a mutation of the thing it guards and report both counts. A prose argument is
not evidence." What neither says, and what U43 adds, is that **the guard written to
discharge that obligation is itself an unmeasured claim until a row exists that can
falsify it.**

**THE MEASURED BEFORE AND AFTER.** Round one at `17b758d`, baseline 6351 collected,
null control 0 of 6351, H4 promoted to the full suite and reporting 0 kills of
6351. Round two at `d285a46`, light pass, 10 rows, baseline green at 6355
collected, null control 0 of 6355, and 9 killed. Every non control row reports 1
kill on a subset of 34 against a baseline of 34, including all six re-measured
zeros and all three validation rows. **Both tables are the author's own.** The round
two spec records the gap in its dropped row `D6_independent_pass`: no independent
verifier ran, and the measured gaps between an author's table and an independent one
on this project are 10 against 17, 39 against 49, and 49 against 83.

## When to Apply

- You are writing a test whose purpose is to make a specific mutation row die.
  Before the assertion is written, name the state the mutated line needs in order
  to matter, and check the fixture reaches it. That check is the whole of this doc.
- The new guard comes back RED on correct code. Treat that as the decision point
  rather than as a typo. Drive both trees before touching the expected value,
  because the repair that turns red into green is the same edit whether the
  expectation was wrong or the fixture was dead.
- You are about to change an expected value to the one the code just printed.
  `RESTART-cratekit.md` names that exact move as how a characterization gets a
  guard's costume. If the value came off the run rather than off a decision, the row
  is still open.
- The property under test depends on WHERE something sits in a string, a path, a
  list or a file, rather than on whether it is present. Position sensitive
  properties are the natural home of a dead position fixture, and a marker, a
  prefix, a suffix, a header line or a leading separator are all this shape.
- The code under test is a regex anchored with `^` or `$`, a slice, an index, or a
  `startswith`. Anchoring is what creates positions where a value exists and is
  unreachable.
- The property under test is a BOUND: a cap, a limit, a threshold, a page size, a
  truncation. Count the population the fixture supplies and confirm it exceeds the
  bound, or the assertion holds whether or not the bound is applied. Assert the
  inequality itself so the fixture cannot silently shrink later.
- A guard is closed and the row is about to be reported closed on a green suite
  alone. Re-run the identical mutation, byte for byte, and then add a row that
  attacks the fixture's premise.
- Two or more surfaces are exercised by the same fixture body. U39's naming fixtures
  used one body for both surfaces, and the defect lived inside the agreement.
- You are copying an existing fixture helper to make a marked, tagged or decorated
  variant. The variant's decoration has a correct position defined by the production
  writer, and the copy is where it drifts.

## Examples

**The fixture that cannot discriminate.** Title tag
`08A - 124 - Lossy Companion [MP3]`, driven on 2026-08-27 through
`cratekit.modules.tools.setbuilder.parse_entry` on the current tree, with
`NameTemplate(markers=(MarkerRule(field="lossy", literal="[MP3]"),))` for the
correct tree and `NameTemplate()` for the H4 tree:

    marker declared    title 'Lossy Companion [MP3]'   match 'birch lossy companion mp3'
    marker undeclared  title 'Lossy Companion [MP3]'   match 'birch lossy companion mp3'

Identical. The shipped assertion, `"Lossy Companion" in titles`, is FALSE on both,
so the guard fails red and the repair that greens it greens it everywhere.

**The fixture that discriminates.** Title tag `08A - 124 - [MP3] Lossy Companion`,
same drive:

    marker declared    title 'Lossy Companion'         match 'birch lossy companion'
    marker undeclared  title '[MP3] Lossy Companion'   match 'birch mp3 lossy companion'

**What shipped**, in `tests/test_setbuilder_cli.py`. The correction lives in the
`place` fixture, where the comment states the rule at the point of use
(`:428` through `:431`):

```python
        # The marker goes immediately AFTER the head, which is where the renamer
        # writes it and the only position where the declared template's marker
        # rule has any effect. See the lossy-companion test.
        head = f"{key} - {bpm:g} - {marker + ' ' if marker else ''}{title}"
```

and the guard itself at `:608`, whose docstring ends by naming the mistake so the
next reader does not repeat it:

```python
    THE MARKER'S POSITION IS THE WHOLE TEST. The first attempt at this fixture put
    it at the END of the title, where it changes nothing either way, and would
    have been a guard that passes under the mutation it was written to catch.
    """
```

**The validation row that pins the fixture's position**, from
`docs/mutation/u43-round-2-rows.toml`:

```toml
[[rows]]
id = "V2_marker_position_moved"
description = "The marker rule is declared with a separator that puts it somewhere the head parser does not strip. If the lossy guard passes this, its fixture is in a position where the declaration cannot matter, which is the mistake the first attempt at it made"
file = "src/cratekit/setbuilder/cli.py"
surface = "user"
old = '''    return NameTemplate(markers=(MarkerRule(field="lossy", literal=cfg.naming.lossy_marker),))'''
new = '''    return NameTemplate(markers=(MarkerRule(field="lossy", literal="[NOTAMARKER]"),))'''
```

On the shipped fixture that literal makes `parse_entry` return title
`'[MP3] Lossy Companion'`, so the membership assertion is false and the row dies. On
the end position fixture it would have returned `'Lossy Companion [MP3]'`, matching
the repaired expectation, and survived.

**The size variant, `P6_count_ignored`.** `build_plan` slices
`pool[: count or DEFAULT_POOL]` (`src/cratekit/modules/tools/setbuilder.py:833`) and
`DEFAULT_POOL` is 8 (`:209`). The narrow `index` fixture is eight tracks including
the anchor, which yields five compatible companions. Driven through
`setbuild_cli.plan_for`:

    count=None   pool 5   totals count 5   items 5
    count=2      pool 2   totals count 5   items 5

In round one the payload had no `pool` field at all; it was added by the same commit
that fixed this, `d285a46`. So the only observable was the union, and the union is 5
either way, because `pool[:2]` and `pool[:8]` union with the same four entry
sequence to the same five items. The cap assertion held whether or not the cap
applied.

The fix is a wider fixture, `wide_index` at `tests/test_setbuilder_cli.py:198`.
Driven on it:

    count=None   pool 8   totals count 8   items 8
    count=2      pool 2   totals count 4   items 4

And the guard's first assertion is the inequality itself, so a fixture that shrinks
back below the bound reports rather than passes (`:229` through `:232`):

```python
    assert uncapped["totals"]["pool"] > capped["totals"]["pool"], (
        "the fixture yields too few companions for a cap to be observable, so "
        "this measures nothing"
    )
```

That assertion is the size branch's version of the V2 row. It is a guard on the
fixture rather than on the code, written into the test where a mutation row would
otherwise have to catch it.

## Related

- [Asserting an absence pins the observation and not the mechanism, so two implementations can both satisfy it](asserting-an-absence-pins-the-observation-and-not-the-mechanism.md).
  The nearest neighbour, and the doc that named this one's territory in advance
  without capturing it. It states the family in a sentence, "the assertion, the
  fixture, or the observation window can each collapse the two trees onto one
  outcome, and only the mechanism differs", and closes that paragraph with "This doc
  is the assertion branch". This is the fixture branch. That passage also names the
  two fixture instances that went uncaptured: U27's `adopt.apply` row `S3`, where the
  narrowed analysis watch still covered a grid file the fixture had written inside
  the narrowed root, fixed by moving the grid directly under the library root
  (session history); and U39's naming fixtures. Neither has its own entry, and this
  doc is the first of the three to get one.
- [A zero death row can be a test gap or an inert mutation, and the table cannot tell you which](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md).
  Supplies the diagnostic this doc extends. Its rule is that if you can state the
  assertion that would kill the row, the row is a real gap. U43 adds the next
  question after that one: you could state it, you did state it, and the fixture the
  assertion runs on could not reach the state that makes it discriminate. Stating
  the assertion is necessary and still not sufficient, which is the same shape the
  absence doc found from the other side.
- [A zero row's dismissal is a claim about the mutated tree, and reasoning from the unmutated one cannot settle it](dismissing-a-zero-row-is-a-claim-about-the-mutated-tree.md).
  Same family, and this doc is the third half turn on that screw. That one says a
  DISMISSAL of a zero is an unverified claim. Its postscript adds that a CLOSURE is
  not trustworthy either unless the expected value was decided from something other
  than the code. This one says a closure is not trustworthy even when its expected
  value IS correctly decided, if the fixture cannot distinguish the two trees at all.

  **Read these four as a set.** The table cannot tell a gap from an inert row
  (2026-08-23), a dismissal of a zero is an unverified claim (2026-08-25), an
  assertion that kills nothing may be correctly aimed and still not discriminate
  (2026-08-26), and the fixture the assertion runs on may never reach the state where
  the mutated line could matter (2026-08-27).
- [Adding the first caller to an existing function makes you the owner of its unreviewed defects](adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md).
  U43's other inheritance, and a pointer rather than a relationship. U43 was the
  first caller of `cratekit.modules.tools.setbuilder` anywhere in `src` and took on
  its failure paths, two of which became the `positive_count` guard. Worth knowing
  the same unit produced both, and not worth more than that.
- `docs/METHOD.md`, the mutation table section. It states the zero-is-a-finding rule
  and the user facing composite rule this doc operates under, and says nothing yet
  about the guard written to discharge that obligation being an unmeasured claim of
  its own. Like its three siblings, this doc fills a gap one level below METHOD's
  stated rules rather than contradicting them.
- Issue #61, "U43: The setbuild command-line shell (row 29)", closed by the merge at
  `2fa9efc`. The unit this learning came from. There is no PR, by contract.
