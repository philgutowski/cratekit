---
title: "Asserting an absence pins the observation and not the mechanism, so two implementations can both satisfy it"
date: 2026-08-26
category: workflow-issues
module: "src/cratekit/tagging/retag.py, tests/test_genre_retag.py, src/cratekit/write/metadata.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A test's central assertion is that a collection is empty, a count is zero, a field is unchanged, or nothing was raised"
  - "A guard proves a filter by asserting the filtered item is missing downstream rather than asserting where it was dropped"
  - "A mutation row measures zero on the exact line a test names in its own function name"
  - "The code under test has more than one refusal gate between the input and the observable"
  - "A value is stringified on its way into a lookup, so a None becomes the key \"None\" that a lookup politely misses"
symptoms:
  - "A test named for the property it protects kills zero mutants of the line that implements that property"
  - "assert plan.changes == () holds under both the correct and the mutated implementation, for two different reasons"
  - "Swapping outcome.written for outcome.results puts the refused row into the plan, and the suite stays green"
  - "resolve_genre_id looks up a genre literally named \"None\", finds nothing, and returns the row as skipped instead of changed"
  - "The pass or fail of the assertion carries no information about which code path produced the empty result"
related_components:
  - development_workflow
  - documentation
tags:
  - mutation-testing
  - zero-row
  - test-fidelity
  - absence-assertion
  - decorative-assertion
  - silent-failure
  - genre-retag
  - guard
---

# Asserting an absence pins the observation and not the mechanism, so two implementations can both satisfy it

## Context

U40 gave the genre retag pass its database half, the planner that turns a folder
sweep into `GenreID` writes on live rows. It merged to `main` as `ea45237`,
"merge: correct a genre that is already wrong". This repository forbids pull
requests by contract (`CLAUDE.md`, "No pull requests. Feature branch per unit,
merge to `main` locally, push `main`, delete the branch"), so there is no PR
number to cite and the merge commit is the citation.

The author's own full mutation table is `docs/mutation/u40-author-full.md`,
measured on branch `unit/u40-genre-retag-for-mis-tagged-arrivals` at `aea668e`,
45 rows against METHOD's 45 row cap for a full pass, 65 pytest invocations, a
green baseline of 6314 collected and a null control that killed 0 of 6314.
Eight rows measured zero, five of them user facing, and the table's own "Zero
rows and what they owe" section printed the standing sentence for each of the
five: `USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it`.

One of the five is the subject of this doc. `D1_plan_from_selection` mutates one
line in `plan_library` at `src/cratekit/tagging/retag.py:463`:

```python
    written = outcome.written
```

to

```python
    written = outcome.results
```

The row's description in round one is "Plan from every result rather than from
what was written, so a refused file's row is retagged anyway"
(`docs/mutation/u40-author-full.md:575`). It was promoted to the full suite per
METHOD:90 and reported "Collected: 6314 against a baseline of 6314. Kills: 0
(zero)".

That line is not incidental. `plan_library`'s docstring opens with the property
in capitals (`src/cratekit/tagging/retag.py:437`): "THE WRITTEN RESULTS AND NOT
THE SELECTION. A plan built from what was proposed rather than from what
happened is the reporting half of the first-caller defect the corpus records: it
would name a row for a file whose write was refused, and the database would then
disagree with the file on disk in the direction nobody checks." There was a test
carrying exactly that name,
`test_the_plan_is_built_from_what_was_written_and_never_from_the_selection`, and
it killed nothing.

The reason it killed nothing is the learning, and it is not a case of a missing
test or an inert mutation. The test was real, the mutation was real, and the two
trees genuinely behave differently. They just happen to arrive at the same empty
tuple by two different routes, and the assertion only looked at the tuple.

**THIS CLASS WAS HIT THREE DAYS EARLIER AND NOT CAPTURED, WHICH IS WHY THIS DOC
EXISTS** (session history). U27's restore shell, on 2026-08-23, produced a row
its own session called "the story worth keeping":
`S5_the_off_machine_half_runs_second`. The ordering test measured the database's
bytes AFTER the call, and a mutation that runs the capture restore both before
and after the mirror pull satisfies that assertion exactly, because the last
write is the capture either way. The resolution then was to rewrite the test to
assert the SEQUENCE rather than the end state, after which it killed. That is
this same failure, in a different register, and it went into a unit report rather
than into `docs/solutions/`. Two learnings about zero rows were written in that
period and neither of them names this one.

The same sessions record a third variant nobody captured either: the mutation
genuinely differs, and the test's FIXTURE makes both trees observe the same thing
(U27's `adopt.apply` row `S3`, where the narrowed analysis watch still covered a
grid file the fixture had written inside the narrowed root; and U39's naming
fixtures, which used the same body on both surfaces and so hid a defect that
would have stripped the artist from roughly 9,800 real files). The honest framing
of the family is one sentence: **the assertion, the fixture, or the observation
window can each collapse the two trees onto one outcome, and only the mechanism
differs.** This doc is the assertion branch.

## Guidance

**WHEN A GUARD'S EXPECTED OUTCOME IS AN ABSENCE, ASK WHAT ELSE PRODUCES THAT
SAME ABSENCE, AND ASSERT AGAINST THE OTHER MECHANISM TOO.** An empty list, a
count of zero, a field left unchanged, nothing raised, no file on disk. Each of
those is a value that many different code paths can produce, and a mutation only
has to reach one of the other paths to survive. Asserting the absence pins the
observation. It does not pin the mechanism, and the mechanism is what the guard
is about.

The failing question is "did the wrong thing happen". The question that pins a
guard is "did the wrong thing happen, and did it fail to happen for the reason I
claim". Those come apart precisely when the system has more than one refusal
gate on the path, which is the normal shape of a pipeline that validates as it
goes.

**Write down every route to the absence before you write the assertion.** For
`plan_library` there are at least three routes to `plan.changes == ()`, and they
are visible in the code without running anything:

- the file never entered the plan, because it was filtered out of `written`
  (`src/cratekit/tagging/retag.py:463`),
- the file entered but resolved to no live row, so it landed in `unmatched`
  (`:472` through `:479`),
- the file entered, resolved fine, and then the genre lookup refused it, so it
  landed in `plan.skipped` (`src/cratekit/write/metadata.py:336` through
  `:339`).

Three routes, one observable. A test that names the first route and asserts only
the observable is satisfied by all three. There are at least two more, a
contested location where two written files claim one row
(`src/cratekit/tagging/retag.py:482` through `:487`) and a falsy genre skipped
without comment (`src/cratekit/write/metadata.py:334` through `:335`), which is
the point rather than a footnote: the routes to one absence are hard to
enumerate, and that is exactly why the assertion has to close them off by
register rather than by imagination.

**Assert the other outputs to zero as well, not only the one you care about.**
`Plan` carries two tuples, `changes` and `skipped`
(`src/cratekit/write/metadata.py:246` and `:247`), and `LibraryPlan` carries
`unmatched` alongside the plan (`src/cratekit/tagging/retag.py:423`). A guard
claiming a file never entered the planner should say so with every one of those
empty, because "never entered" means every downstream register is untouched. A
guard claiming a file entered and was refused should name which register caught
it. Both assertions are cheap. One line each.

**A sibling in the same file already does this the right way, so the pattern was
available.** `test_a_soft_deleted_row_is_never_retagged` at
`tests/test_genre_retag.py:644` asserts the empty change list and then names the
positive side channel it expects:

```python
    assert planned.plan.changes == ()
    assert [(u.path, u.outcome) for u in planned.unmatched] == [(str(path), "absent")]
```

That second line is the mechanism assertion. It says which of the three routes
the file took, so a mutation that routed it differently and still produced an
empty change list would fail. The D1 test was the same shape of claim with only
the first line.

**Prefer a positive assertion about the mechanism when one exists, and fall back
to zeroing the siblings when it does not.** For the tombstone case there is an
observable that says what happened, the `unmatched` entry with outcome
`"absent"`. For the refused file case there is no positive observable at all,
because the correct behaviour is that nothing anywhere records the file. So the
assertion has to be the other absences, and it has to be all of them.

**Stating the assertion is necessary and not sufficient, which sharpens a
diagnostic the corpus already carries** (session history). U27's `adopt.apply`
session settled on a test for telling a genuine gap from an inert mutation: if
you can state the assertion that would kill the row, it is a real gap; if you
cannot, suspect inertness. That test is still right and this case passes it. The
assertion was statable, it was stated, it was aimed at the correct line, and it
still did not discriminate. Add the second half: having stated the assertion, ask
whether the value it observes is reachable by any other path.

## Why This Matters

**The two trees really do differ, and both of them produce an empty change
list.** Under the correct implementation, `outcome.written` filters the results
to the ones whose `written` field is set
(`src/cratekit/tagging/retag.py:137` through `:139`):

```python
    @property
    def written(self) -> tuple[RetagResult, ...]:
        return tuple(result for result in self.results if result.written)
```

A refused file has no genre written to it. `_ask` builds its result without a
`written` argument (`:311` through `:317`), and `RetagResult.written` defaults
to `None` (`:124`), with the class docstring stating the invariant that "reason
is empty exactly when `written` is set, so the two can never both describe the
same file". So the refused file is filtered out before the planner sees it,
`genres` stays empty, `plan_genre_retag` is handed nothing, and `plan.changes`
is `()`.

Under the mutation, `outcome.results` carries the refused file into the loop. It
matches a live row, so it is not unmatched. It reaches `:489`:

```python
        genres[content_id] = str(result.written)
```

`result.written` is `None` here, and `str(None)` is the four character string
`"None"`. `plan_genre_retag` then calls `resolve_genre_id(db, "None")`
(`src/cratekit/write/metadata.py:336`), which walks the library's genre rows
looking for one named `"None"`, finds none, and returns `None`. The planner
appends a skip and continues (`:336` through `:339`):

```python
        genre_id = resolve_genre_id(db, wanted)
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
```

So the mutated tree produces `plan.changes == ()` as well, with one entry in
`plan.skipped` carrying reason `genre-unknown` and detail `"None"`. Driven
directly against the current tree with the test file's own `Row` and `FakeLookup`
doubles, `plan_genre_retag([Row("1", GenreID=None)], {"1": str(None)}, db=db)`
returns an empty `changes` and exactly that one skip, and
`resolve_genre_id(db, "None")` returns `None`.

The assertion `planned.plan.changes == ()` therefore held on both trees, and it
held for opposite reasons. On the correct tree it held because the file was
never a candidate for a change. On the mutated tree it held because a genre
lookup on a stringified `None` happened to miss.

**The survival was luck, and the luck runs out.** The mutated tree is one
coincidence away from writing. `resolve_genre_id` matches on `Name`, so any
library containing a genre row literally named `"None"` would resolve, and the
refused file's row would be retagged to it. Nothing forbids that name. More to
the point, the guard's real subject is not the genre lookup at all. It is that
the reporting half must be built from what happened rather than from what was
proposed, and a second gate accidentally catching the overflow says nothing
about whether the first gate exists.

**The measured before and after.** Round one, `docs/mutation/u40-author-full.md`
at `aea668e`, baseline 6314 collected, null control 0 of 6314, D1 promoted to
the full suite and reported 0 kills of 6314 collected. Round two,
`docs/mutation/u40-author-round-2.md` at `91d300b`, a light pass of 10 rows, 19
pytest invocations, baseline 6319 collected, null control 0 of 6319. D1 there
reports "Collected: 40 against a baseline of 40. Kills: 1 (killed)" on the
subset `tests/test_genre_retag.py`, killed by
`test_the_plan_is_built_from_what_was_written_and_never_from_the_selection`. The
row's round two description is blunt about what it is: "Round one zero, and the
most useful row in the table".

The kill comes from exactly the test that had been failing to kill it, which is
the strongest form of the result. The guard did not need a new test. It needed
one more line in the test it already had.

**This is a third family alongside the two zero row learnings already in the
corpus, and it is the one neither of them covers.** The inert mutation doc
covers a zero where the two trees behave identically. The dismissal doc covers a
zero read as inert when the gap was real. D1 is neither. The trees behave
differently, the gap was real, and nobody dismissed anything. The measurement was
correct and the test was sincere. What failed is narrower and more ordinary, an
assertion chosen to observe an absence when the property under test was a
mechanism.

**Absence assertions are not rare here, they are the house dialect.**
`tests/test_genre_retag.py` alone carries seventeen assertions of the shape
`== ()`, `== []` or `== 0`, and eleven of them are on `plan.changes`,
`outcome.written` or a write report's `written`. Every one of them is a candidate
for the same failure, and each has to be checked individually, because whether a
second route to the empty tuple exists depends on what sits downstream of that
particular call.

**It is an instance of a pattern METHOD already names, rather than a new one.**
`docs/METHOD.md`'s second recurring defect pattern is "Identity that is not
unique to the thing it identifies. A path digest, an inode pair, a symbol
fingerprint. Each was a single field trusted alone." An empty tuple observed as
evidence of one particular refusal is that same defect applied to a test
observation rather than to a data field. It is NOT the fourth pattern, a fix
justified by a measurement taken on a fixture rather than on the tree: the
measurement here was honest and the fixture was real.

**METHOD already says a zero is a finding, and this is what the finding was.**
`docs/METHOD.md:71` states the rule, "Revert each new guard one at a time, run
the suite, count the deaths. A guard that kills zero tests is a finding."
`docs/METHOD.md:39` says a table over a suite this size "always finds a zero
death row, because that is a property of large test suites rather than of any
branch." What neither says is that a zero on a guard you can point at by name is
worth more attention than a zero on a guard you cannot, because it means the
guard exists, ran, and held nothing. That is the shape here, and it is the shape
easiest to close.

## When to Apply

- A test's central assertion is an empty collection, a zero count, a `None`, or
  an unchanged field. Before it is written, enumerate every code path that
  reaches that value and say which one the test is claiming.
- The code under test has more than one gate on the path between the input and
  the observable. Two gates means two ways to reach the same refusal, and a test
  that names the first one must rule out the second.
- A dataclass or result object carries several parallel registers, changes and
  skipped, written and unmatched, applied and refused. Zeroing one and ignoring
  the others is the exact gap this doc records. Zero all of them or name which
  one caught the case.
- A value is stringified on its way into a lookup, `str(x)`, an f-string, a
  format call. `str(None)` is `"None"` and `str([])` is `"[]"`, and both are
  keys a lookup will politely miss rather than reject. A miss downstream can
  mask a defect upstream.
- A mutation table row measures zero on a guard that has a test named after it.
  Read the test's assertion, not just its name. A named guard with a zero row is
  a guard that ran and held nothing, which is cheaper to close than a guard that
  does not exist.
- You are about to file a user facing zero into `docs/residual-findings.md`
  under METHOD's severity floor. If the guard's assertion is an absence, try
  strengthening the assertion first. On D1 the fix was one line and the row went
  from 0 kills to 1.
- A test asserts that a destructive or write-declaring verb did nothing. The
  absence is the whole point of such a test, so it is exactly where an
  unpinned mechanism costs the most.
- The test asserts an END STATE where the property is really about ORDER or
  provenance. U27's restore ordering row is the worked case: measure the
  sequence, not the bytes that survive it.

## Examples

**Before**, at `91d300b^`, in `tests/test_genre_retag.py`. The docstring states
the property precisely and the assertions do not reach it:

```python
def test_the_plan_is_built_from_what_was_written_and_never_from_the_selection(tmp_path):
    """The reporting half of the first-caller defect the corpus records.

    A plan built from the selection would name a row for a file whose write was
    refused, and the database would then disagree with the file on disk in the
    one direction nobody checks afterwards.
    """
    path = tmp_path / "track.flac"
    refused = retag.RetagOutcome(
        results=(
            retag.RetagResult(
                path=path, current=CATCH_ALL, reason=retag.ANSWER_TOO_COARSE
            ),
        )
    )
    rows = [trees.ContentRow(content_id="1", recorded=str(path), deleted=False)]
    mapped = {"1": Row("1", GenreID=None)}
    db = FakeLookup([Row("7", Name=SPECIFIC, rb_local_deleted=0)])

    planned = retag.plan_library(refused, rows, mapped, root=tmp_path, db=db)
    retag.apply_library(planned, mapped)

    assert planned.plan.changes == ()
    assert mapped["1"].GenreID is None
```

The second assertion looks like a second opinion and is not one.
`mapped["1"].GenreID` stays `None` under the mutation too, because
`apply_library` applies the plan and the plan has no changes to apply. Both
assertions observe the same absence through the same downstream gate.

**After**, in `91d300b` ("test(retag): close five zero rows the author table
found, and one it could not"), reachable from `main` through the merge
`ea45237`. The fixture is unchanged and the assertions now read:

```python
    assert planned.plan.changes == ()
    # THE SKIP LIST IS THE ASSERTION THAT MATTERS, and asserting only the empty
    # change list is what let a mutation of this exact line survive. Planning from
    # the selection puts the refused row in the plan with its genre stringified
    # from None, the lookup for a genre named "None" resolves to nothing, and the
    # row comes back SKIPPED rather than changed. So the change list is empty for
    # the wrong reason and the weaker assertion holds for both implementations.
    assert planned.plan.skipped == (), (
        "the refused file reached the plan and was rejected by the genre lookup "
        "rather than never entering it, so the plan is built from the selection"
    )
    assert mapped["1"].GenreID is None
```

One added assertion and one added message. The message is doing real work,
because the failure it reports is not "the plan changed something" but "the plan
refused the file at the wrong gate", and a bare tuple comparison would leave the
next reader to rediscover the difference.

**The re-measurement.** `docs/mutation/u40-author-round-2.md`, light pass, 10
rows at `91d300b`, baseline green at 6319 collected, 19 pytest invocations, null
control killed 0 of 6319. The D1 row:

    D1_plan_from_selection    subset tests/test_genre_retag.py
                              collected 40 against a baseline of 40
                              kills 1 (killed)
                              test_the_plan_is_built_from_what_was_written_and_never_from_the_selection

The subset went from 36 collected in round one to 40 in round two, because
`91d300b` added tests to that file for four other zero rows. The baseline went
from 6314 to 6319. Neither number is the point. The point is that the one test
whose name already claimed this property is now the test that kills the row.

**The contrasting sibling, further down the same file**
(`tests/test_genre_retag.py:644`). Same planner, same empty change list, and a
mechanism assertion instead of a second absence:

```python
    assert planned.plan.changes == ()
    assert [(u.path, u.outcome) for u in planned.unmatched] == [(str(path), "absent")]
    assert mapped["1"].GenreID is None
```

Here the file is written but its row is a tombstone, so the correct behaviour
does leave a trace, the `unmatched` entry with outcome `"absent"`. Where a trace
exists, assert the trace. Where the correct behaviour leaves no trace anywhere,
as with the refused file, assert that every register is empty rather than the
one you were thinking about.

## Related

- [A zero death row can be a test gap or an inert mutation, and the table cannot tell you which](a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md).
  The other half of the zero row pair, and the one that supplies the diagnostic
  this learning extends. Its rule is that an inert row cannot be closed by
  writing a test, so if you cannot state the assertion the row is inert. U40
  shows the next question after that one: you could state the assertion, you did
  state it, and it still did not discriminate, because the value you asserted was
  an absence that two implementations both produce. Stating the assertion is
  necessary and not sufficient.
- [A zero row's dismissal is a claim about the mutated tree, and reasoning from the unmutated one cannot settle it](dismissing-a-zero-row-is-a-claim-about-the-mutated-tree.md).
  The nearest neighbour, and the one this doc completes rather than repeats. That
  doc ends its U39 example on the sentence "An empty plan is a real assertion,
  not the absence of one, whenever a mutation can make the plan non empty." U40
  is the case where the whenever clause fails: a mutation made the plan non empty
  in a different field, so the empty change list stayed empty and the assertion
  held for both trees. There the question was whether a zero row could be
  dismissed; here the row was correctly read as a real gap and the open question
  was why an assertion that looked like a guard was not one.

  **Read these three as a set.** The table cannot tell a gap from an inert row
  (2026-08-23), a dismissal of a zero is an unverified claim (2026-08-25), and an
  assertion that kills nothing may be correctly aimed and still not discriminate
  (2026-08-26).
- [A count that moved by the right amount is not a measurement of what moved](a-count-that-moved-by-the-right-amount-is-not-a-measurement-of-what-moved.md).
  The same shape one register over. There a total that moved by the expected
  delta was taken as a measurement of which members moved, and a member leaving
  while another joined read as no change. Here an empty result was taken as a
  measurement of which mechanism produced it, and a refusal that never entered
  the plan read the same as a refusal that entered and was rejected. Both say an
  aggregate is not evidence about the mechanism behind it, and both remedies are
  the same move: name the thing the aggregate is hiding.
- [Discharging a countdown entry by half takes a whole test file out of collection](countdown-entry-discharge-drops-a-whole-test-file.md).
  Same family, one layer further out: a green signal that measures nothing
  because the thing it was supposed to measure never ran. That one is a whole
  file leaving collection, R-173 is a loop body that iterates zero times, and
  this one is an assertion that runs and holds for the wrong reason. Three ways
  to be green while holding nothing, ordered by how much of the test survives.
- [Adding the first caller to an existing function makes you the owner of its unreviewed defects](adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md).
  U40's other learning, and it is a different one. That doc's class recurred on
  this unit: U40 was the first caller of `write/metadata` in `src` and inherited
  two defects from it. Worth a pointer so a reader of either one knows the same
  merge produced both, and not worth more than a pointer, because ownership of a
  callee's defects and the strength of an absence assertion share nothing but the
  commit.
- Issue #58, "U40: Genre retag for mis-tagged arrivals", closed by the merge at
  `ea45237`. The unit this learning came from. There is no PR, by contract.
