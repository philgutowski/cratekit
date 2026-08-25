---
title: "A zero row's dismissal is a claim about the mutated tree, and reasoning from the unmutated one cannot settle it"
date: 2026-08-25
category: workflow-issues
module: "scripts/mutate.py, src/cratekit/write/naming_cli.py, tests/test_naming_apply_cli.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_workflow_step
resolution_type: test_fix
applies_when:
  - "An independent adversarial mutation review returns CLEAN while rows in its own table killed zero tests"
  - "A zero row is about to be dismissed as a poor discriminator, an inert mutation, or otherwise not worth pinning"
  - "The argument for dismissing a zero row describes what the code does today rather than what the mutated code would do"
  - "A mutation drops one operand of a boolean or, one branch of a conditional, or one side of a precedence pair"
  - "A reviewer's zero row disposition is about to be carried into docs/residual-findings.md or closed out without a test"
symptoms:
  - "Six of twenty two rows kill zero tests and the review verdict is still CLEAN"
  - "A row's disposition argues the two versions cannot be told apart, and the argument only holds on the unmutated tree"
  - "Dropping one operand of a boolean or reads as redundant, when the dropped half is the one whose loss destroys data"
  - "A row goes from zero deaths to one after a single test is written, so the row was killable the whole time"
  - "Three sibling rows carry the same reasoning and the same defect, because one dismissal shape was applied across the table"
related_components:
  - "development_workflow"
  - "documentation"
tags:
  - "mutation-testing"
  - "zero-row"
  - "mutation-table"
  - "adversarial-review"
  - "unchecked-claim"
  - "test-fidelity"
  - "method-compliance"
  - "silent-failure"
---
# A zero row's dismissal is a claim about the mutated tree, and reasoning from the unmutated one cannot settle it

## Context

U39 (issue #57) made the naming engine write the zero padded Camelot form at
write time and carry a file's existing head through `crate name apply`. It
merged to `main` as `31bf91f`, with the restart note following in `71340a3`.
The unit's central new surface is one shared spec builder,
`_spec_for` at `src/cratekit/write/naming_cli.py:48`, whose docstring
(`:49` through `:63`) says why it exists: "The two passes previously built
their specs separately and disagreed on the lossy flag, so a marked file was
promised a rename the apply pass was never going to perform. One builder makes
agreement structural."

The author's own mutation table ran fourteen rows and every one killed
(`docs/mutation/u39-author-full.md`). `docs/METHOD.md:95` says what to do with
a result like that: "An author's own table is a draft, not a result. Every fix
agent on this project has run its table honestly and still missed guards its
own round created, because it mutates what it believes it changed. Measured
gaps between an author's table and an independent one: 10 against 17, 39
against 49, 49 against 83." So an independent adversarial review was run by an
agent that did not write the code, in its own worktree with its own virtual
environment (`docs/u39-naming-review.md`).

The independent table ran 22 rows against a 45 row full pass cap, with 77 total
deaths, a null control of 0 deaths, and a green baseline of 6254 collected
(`docs/mutation/u39-naming-independent.md`). Six rows killed zero. That is the
expected shape rather than a surprise, and METHOD:39 says so: a mutation table
over a suite this size "always finds a zero death row, because that is a
property of large test suites rather than of any branch." The verdict was
CLEAN. Fourteen author rows found no zeros. Twenty two independent rows found
six.

METHOD has a rule for each kind of zero. `docs/METHOD.md:101` says "A zero
death row on a guard with a USER FACING surface is acceptable only when a
composite shows what it does hold. Pair it with a mutation of the thing it
guards and report both counts. A prose argument is not evidence."
`docs/METHOD.md:105` says a maintainer facing zero "gets one line, not a
composite." The reviewer followed both, and went further, pairing every user
facing zero with a scratch driver scenario that drove the shipped code's actual
behaviour on the branch each zero touched.

The gap this doc closes is one level up from METHOD:95. METHOD treats the
author's table as a draft because the author mutates what they believe they
changed. Nothing in METHOD treats a reviewer's REASON for leaving a zero at
zero the same way, and on U39 one such reason was wrong in a way that would
have left the most destructive row in the table unpinned.

**The author's table never had to reason about a zero, and never saw this line.**
(session history) The session that built U39 authored fourteen rows, confirmed
`scripts/mutate.py`'s exact byte matching semantics before writing any of them,
verified every anchor string was unique in the tree, and every row killed. No
zero appeared, so no composite was owed and no dismissal was ever made. The
`lossy=marker in path.stem or marker in title` line is not named, quoted, or
mutated anywhere in that session. Both operands of the condition went
unconsidered until the independent pass, which is METHOD:95 operating exactly as
written.

**The project already had a working diagnostic for this, applied in the other
direction, and a standing bar.** (session history) Two days earlier the
adopt.apply round hit three zeros and tested each with one question stated
explicitly in that session: can I name the assertion that would kill this row?
For each it could, so each was closed with a named guard, and the round ended on
the line that is the real bar here: "No zeros remain across either round, and
none was reclassified to get there." Reclassification is treated on this project
as the failure mode rather than the resolution. The U39 dismissal did not
contradict that bar so much as skip it.

**The re-drive rule existed but had only ever been pointed at positive
findings.** (session history) When an independent reviewer returned BLOCKING on
an earlier unit, the author's stated rule was to verify both findings personally
first, "because a fix justified by someone else's confident number is exactly the
pattern METHOD warns about." That rule was applied every recorded time a reviewer
CLAIMED something. Nothing in the recorded history applies it to a reviewer
DISMISSING something, and a dismissal is where K2 sat.

## Guidance

**Deciding that a zero row is inert, undiscriminating, or otherwise not worth
pinning is a claim about the MUTATED tree. Evaluate it there, or you have not
evaluated it.** A zero row asserts that no test in the suite behaves differently
between two trees. Any argument that the row could not be killed has to describe
the mutated tree's behaviour on some input and show it matching the original's.
An argument that describes only what the original does on that input is not an
argument about the row at all, however true it is.

The failure is easy to make because the unmutated tree is the one sitting in
front of you. You read the line, you picture a file flowing through it, you
notice that nothing happens to that file today, and you conclude that nothing
could distinguish the two trees. The step you skipped is applying the mutation
before picturing the file.

**Write the assertion sentence out loud before you dismiss the row.** The
sibling learning,
`docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`,
already states this as a diagnostic: "An inert row cannot be closed by writing a
test, and that is the diagnostic. If you sit down to write the test that would
kill the row and find you cannot state what behaviour it would assert, the row
is inert." That diagnostic is correct and it is the right tool here. The U39
error was not disagreeing with it. The U39 error was reaching the diagnostic's
conclusion without running the diagnostic: concluding that no test could
discriminate, without ever attempting to state the assertion. The assertion was
one line and the test that carries it is five.

The two learnings are mirror images and both are about the same unverified step.
The sibling documents reading a zero as a real test gap when the mutation was
semantically inert, so a composite got written for a guard that did not exist.
This one documents reading a zero as inert when the gap was real and severe. In
both cases the table reported `kills=0`, the driver was working correctly, and
the classification came from reasoning the table could not check.

**On a boolean operator, each operand is a separate claim and a test that
satisfies both operands at once pins neither.** This is the concrete shape U39
hit. When a row drops one operand of an `or`, ask what the surviving operand
alone produces for an input where only the DROPPED operand was true. If the
suite has no such input, the row is a genuine gap even though the expression is
obviously exercised.

**A reviewer's independence buys measurement, not reasoning.** The 22 rows, the
77 deaths, the null control and the promoted zeros are measurements, and an
independent agent's measurements are worth more than an author's precisely
because METHOD:95 is true. The sentence explaining why a row sits at zero is not
a measurement. It is a prose argument, and METHOD:103 already says of prose in
this exact position, "A prose argument is not evidence."

**Count what a dismissal saves and what it costs.** `docs/METHOD.md:90` requires
promotion: "Confirm deaths on a subset, spend a full suite only on zero rows.
Select the subset as the test files importing the mutated module. A death on a
subset is a real death. A zero on a subset is not yet a zero, so promote it to a
full run before you report it." Every zero has therefore already bought a full
suite run by the time anybody argues about it. Dismissing it saves the cost of
one test. Closing it costs the cost of one test. On U39 the four closures came
to four tests, and the suite went from 6254 collected to 6258 collected, which
is exactly plus four.

## Why This Matters

The row that was dismissed was the one that loses data.

`_spec_for` computes the lossy flag at `src/cratekit/write/naming_cli.py:80`:

```python
        lossy=marker in path.stem or marker in title,
```

`marker` is `cfg.naming.lossy_marker`, whose default is the literal `[MP3]`
(`src/cratekit/core/config.py:2239`), and the template attaches it as a marker
rule on the `lossy` field (`src/cratekit/write/naming_cli.py:35` through `:38`).
`lossy` is the only markable flag the engine has, `MARKED_FLAGS = ("lossy",)`
at `src/cratekit/core/naming.py:141`, and marking it is not optional.
`_render_markers` at `src/cratekit/core/naming.py:679` raises if a spec sets a
marked flag the template declares no marker for, and the comment at `:683` says
why: "R21: there is no configuration in which a marked condition goes unmarked.
A template that permits the condition without declaring its marker is a
configuration error, and the file it would produce is indistinguishable on disk
from a lossless one." When the flag is true the marker literal is emitted into
the rendered name (`:691`), placed right after the head by `_render_head`
(`:705`).

The row `K2_lossy_filename_side_dropped` reduces that line to

```python
        lossy=marker in title,
```

which is the mutation described in the table as "The lossy OR loses its filename
operand; only a title-carried marker is recognized"
(`docs/mutation/u39-naming-independent.md:479`, under the row header at `:477`).
It killed 0 of 6254 on the full
suite.

The reviewer's dismissal, at `docs/u39-naming-review.md:125` through `:128`,
inside scenario G:

> (Marker in the filename alone happens to already equal its own rendered
> target, so that half is a poor discriminator; case G's title-only half is the
> one that matters and it passes.)

That sentence is true of the unmutated tree. A file named `[MP3] Cola.flac`
whose title tag is clean sets `lossy` true through the filename operand, renders
back to `[MP3] Cola.flac`, and the plan proposes nothing, so no shipped
assertion of the "expected rename" form can catch it.

Under the mutation the sentence stops being true, and the mutated tree is the
only tree whose behaviour decides whether the row is killable. With the filename
operand gone, a clean title leaves `lossy` false, the renderer emits no marker,
and the rendered target is `Cola.flac`. The plan therefore proposes renaming the
marked file to its unmarked form. That is not a missing rename, it is a rename
that destroys the byte distinguishing a lossy copy from a lossless one, proposed
by a verb whose registry entry declares `writes=frozenset({"files"})` and
`destructive=True`.

**The cost, stated by the code and driven rather than argued.** The marker on
disk is the ONLY carrier of the lossy distinction. `core.tags.FIELDS` has no
lossy field, driven at the current tree:

```
tags.FIELDS -> artist, energylevel, genre, initialkey, inizio, title,
               voxgender, voxgenderconf, voxlevel
```

So once the filename loses the marker, nothing on the file records that it is a
lossy copy. `src/cratekit/core/naming.py:683` says exactly that, in a comment
written about a different route to the same end state: "the file it would
produce is indistinguishable on disk from a lossless one."

**And R21's guard cannot catch it, which is why the mutation is silent.**
`_render_markers` at `src/cratekit/core/naming.py:679` raises only when a
marked flag is True and the template declares no rule for it. This mutation
leaves the template alone and corrupts the FLAG, which becomes False, so the
guard is never reached, no marker is emitted, and the rename is proposed
without complaint. R21 enforces a template that permits a condition without
marking it. It cannot see a spec that miscomputes the condition.

**One nearby claim that does NOT hold, recorded because it is tempting.**
`_marker_pattern`'s docstring at `src/cratekit/core/naming.py:328` says a
stripper that left a marker behind made a marked lossy copy and its lossless
twin produce DIFFERENT match keys, so they failed to dedupe. That is a
different failure in the opposite direction, and it does not describe this
row's cost. Match keys are not the injury here: `strip_head` removes the
marker, so `[MP3] Cola` and `Cola` both normalize to `Cola` already, before any
rename, driven at the current tree. The rename changes what a person and the
filesystem can see, not what the matcher computes. Reaching for that docstring
because it mentions the same two files is the identical error this whole
learning is about, one layer down.

Its sibling row `K1_lossy_title_side_dropped` drops the other operand and is
also a real gap, but it fails in the recoverable direction. A marker present
only in the title is a crash window artifact, a run that wrote the marked title
and died before the rename, and the mutation makes the pass stop repairing it.
Nothing already on disk gets worse. Two rows, one line, one shape, and one of
them silently removes information while the other silently declines to restore
it. The dismissal was aimed at the destructive one.

The reason neither row was pinned is worth stating plainly, because it is the
shape that generalizes. The only shipped test touching that line,
`tests/test_naming_apply_cli.py:133`
(`test_the_plan_and_the_apply_agree_on_a_marked_file`), puts the marker in BOTH
operands at once:

```python
    _track(folder, f"{marker} Cola.flac", title=f"{marker} Cola")
    assert _plan(folder)["items"] == []
```

That test is not weak. It closes exactly the plan and apply disagreement U39 was
built to fix, and `K3_lossy_flag_dropped`, which sets `lossy=False` outright,
kills it. But a fixture that makes both operands true cannot say which operand
carries the case, so the same fixture leaves both single operand rows at zero.
The independent table found this because it mutated the branches of an `or` that
the author's fixtures never separated, which is precisely the class METHOD:95
says an author's table misses.

Scale makes it worth writing down. The independent pass produced six zeros where
the author's produced none, and one of the six was dismissed on unverified
reasoning. `docs/METHOD.md:107` records verifiers producing 40 zero rows in a
pass, another 14, another 11. At those counts, a dismissal habit that is right
most of the time still walks past real gaps regularly, and the ones it walks
past are not randomly distributed. They cluster on lines whose fixtures never
disagree with themselves, which is where the destructive branches hide.

**The equivalence judgment is the one step in this apparatus with no mechanical
guard.** (session history) `scripts/mutate.py` already catches one way a zero row
can lie, by comparing each row's collected count against the baseline so a row
that silently drops tests from collection cannot read as a clean zero. It builds
one deliberately inert row per batch, the null control, and invalidates the whole
batch if it kills anything. What it has never had is any way to detect that a
mutated tree behaves identically to the original, or that it does not. That
judgment has always been human, in both directions, and it is therefore the step
where both this learning and its mirror land.

## When to Apply

- Any time you are about to leave a zero row at zero on a reason other than "I
  wrote the test and it kills it now." State the mutated tree's behaviour on a
  concrete input, in writing, before the row is classified.
- A row drops one operand of an `and` or an `or`. Find an input where only the
  dropped operand is true and say what the mutated tree does with it. If the
  suite has no such input, the row is a gap.
- You catch yourself reasoning that a file, record, or request "already equals
  its own output" so nothing could distinguish the trees. That is the unmutated
  tree's identity. Apply the mutation and recompute the output.
- You are reviewing somebody else's mutation table, or your own from a previous
  session. The measurements are trustworthy in proportion to the driver. The
  classifications are claims, and an independent reviewer's dismissal of a zero
  is exactly as unverified as an author's table is a draft.
- You are running the sibling doc's inertness diagnostic. Actually run it. Write
  the assertion sentence. Concluding "no test could discriminate" without
  attempting the sentence is the U39 error, and the sentence is cheap.
- A zero sits on a line in a verb whose registry entry declares
  `destructive=True` or writes files. Rank it above the other zeros. A mutation
  that removes information from disk is a different class of miss from one that
  declines to add information.
- You are about to file a zero into `docs/residual-findings.md`. A residual is
  the honest register of what is known and accepted, so filing a wrongly
  dismissed row records an acceptance nobody actually made, and dismissing it
  with no filing at all records nothing.

## Examples

**Before.** The independent review's Finding 1
(`docs/u39-naming-review.md`) filed `K1` and `K2` together as one residual and
argued the filename half away, in the parenthetical quoted above. The proposed
disposition was a single residual, proposed as R-166, with the note that "case G's title-only half is
the one that matters." Under that disposition the shipped suite would have
carried a line whose destructive branch had no test, with a review on record
saying it could not have one.

**After.** Four of the five findings were closed with tests rather than filed,
in `2cb5d08` ("test(naming): pin the three branches the shipped fixtures never
disagreed on") and `a73deab` ("test(naming): pin the marker's other operand, the
one that loses data"), both reachable from `main` through the merge `31bf91f`.
The test that closes `K2` is `tests/test_naming_apply_cli.py:230`:

```python
def test_a_marker_in_the_filename_alone_is_not_stripped_off(configured):
    """The other operand of the same ``or``, and the direction that loses data.
    An acquired file is marked in its name while its title tag arrives clean
    from the source. If only the title were consulted the render would drop
    the marker, and the pass would propose renaming the marked file to its
    unmarked form, which is how a lossy copy and its lossless twin stop being
    distinguishable. It proposes nothing instead."""
    folder = _folder(configured)
    marker = configured.naming.lossy_marker
    _track(folder, f"{marker} Cola.flac", title="Cola")
    assert _plan(folder)["items"] == []
```

The assertion the reviewer could not state is `_plan(folder)["items"] == []`,
and the reason it discriminates is that the mutated tree proposes a rename here
while the original proposes nothing. An empty plan is a real assertion, not the
absence of one, whenever a mutation can make the plan non empty.

Its sibling at `tests/test_naming_apply_cli.py:218` closes `K1` from the other
side, and its docstring names why the pair was needed at all: "the only other
test of that ``or`` puts it in BOTH at once, so it cannot say which operand
carries the case."

**The re-measurement.** All four rows were re-run with `scripts/mutate.py`
against the same expressions the review mutated, and the results are recorded in
the review's postscript (`docs/u39-naming-review.md:429` onward), which was
added by the session that received the review and left every measurement above
it untouched:

    baseline               6258 collected, up from 6254 by exactly the four new tests
    null control           0 deaths
    R3_head_precedence_swapped        0 -> 1   test_the_filename_head_wins_when_both_heads_parse_and_disagree
    R8_stem_source_swapped            0 -> 1   test_the_body_text_comes_from_the_title_and_not_the_filename
                                               (that test was REMOVED the same day, see the postscript below)
    K1_lossy_title_side_dropped       0 -> 1   test_a_marker_in_the_title_alone_is_still_recovered
    K2_lossy_filename_side_dropped    0 -> 1   test_a_marker_in_the_filename_alone_is_not_stripped_off

Each row is killed by exactly the one test written for it, which is a stronger
result than a death somewhere in the suite, because it shows the new assertion
is the thing holding the branch rather than an incidental collision with an
existing fixture. Final suite: 6257 passed, 1 skipped.

**The correction, in the review's own words** (`docs/u39-naming-review.md:462`
onward):

> Finding 1 records the marker's filename-only half as "a poor discriminator",
> on the grounds that such a file already equals its own rendered target. That
> is true of the unmutated tree and it is not true under the mutation, which is
> the only state that matters for whether a row is killable.

and the general rule it draws, at `:493`:

> METHOD says an author's own mutation table is a draft rather than a result.
> The same applies one level up: a reviewer's reason for leaving a zero row at
> zero is itself an unverified claim, and it is verified the same way everything
> else here is, by driving it.

**What still got filed, and why that is not the same thing.** The other two
zeros became residuals `R-166` (the CUT.md reconciliation has no guard against
drifting back apart) and `R-167` (the Camelot regex's end anchor has zero test
coverage) in `docs/residual-findings.md:9102` and `:9133`. Both were filed after
being driven, not after being reasoned about. `R-167` in particular was
confirmed by running the unmutated code, `is_camelot("1Axyz")` returns `False`
today, so the finding is a coverage gap on a currently correct guard rather than
a live defect. The difference between those two and `K2` is not that one set was
dismissed and the other pinned. It is that every disposition in the final set
rests on a driven observation, and the dismissal that got corrected rested on an
inference from the wrong tree.

## Related

- `docs/solutions/workflow-issues/a-zero-death-row-can-be-a-test-gap-or-an-inert-mutation.md`,
  the mirror of this learning and the one to read alongside it. That doc covers
  reading a zero as a real test gap when the mutation was semantically inert,
  and supplies the assertion diagnostic. This doc covers the opposite
  misclassification, reading a zero as inert or undiscriminating when the gap
  was real, and it is the diagnostic skipped rather than the diagnostic wrong.
  Together they say: a zero is unclassified until you have described the mutated
  tree's behaviour, in either direction.
- `docs/METHOD.md:69` through `:113`, "The mutation table". `:71` on a zero being
  a finding, `:90` on promotion, `:95` on an author's table being a draft with
  the three measured gaps, `:101` on the user facing composite, `:105` on the
  maintainer facing one line, `:111` on writing the table into the repository.
- `docs/METHOD.md:32` through `:41`, the severity floor and the residual rule, on
  what a zero row becomes when it is accepted rather than closed.
- `docs/u39-naming-review.md`, the independent review. Finding 1 at the "lossy
  marker's OR" section is the dismissal, scenario G at `:125` is where it is
  stated, and the postscript at `:422` is the correction and the re-measurement.
- `docs/mutation/u39-naming-independent.md`, the 22 row table: `K1` at `:452`,
  `K2` at `:477`, the summary at `:27` and `:28`, and the "Zero rows and what
  they owe" section at `:38`. `docs/mutation/u39-author-full.md` is the author's
  fourteen rows for contrast.
- `src/cratekit/write/naming_cli.py:48`, `_spec_for` and its docstring, the
  shared builder both passes now use, with the lossy expression at `:80`.
- `src/cratekit/core/naming.py:328`, the stripper docstring on match keys;
  `:141`, `MARKED_FLAGS`; `:679`, `_render_markers` and the R21 refusal that
  makes marking mandatory.
- `tests/test_naming_apply_cli.py:133`, the pre-existing test that set both
  operands at once, and `:218` and `:230`, the pair that separated them.
- Issue #57, the unit's brief. Merge commit `31bf91f`, "merge: the padded form
  at write time, and the head that survives a rename", with the tests in
  `2cb5d08` and `a73deab` and the review in `07efed0`.


## Postscript: the fourth closure was itself the error, 2026-08-25

Added by the session that wrote this doc, hours after writing it, and left here
rather than folded in because the sequence is the point.

Three of the four rows above were closed correctly. The fourth,
`R8_stem_source_swapped`, was closed with a test asserting that a file's body
text comes from the title tag rather than from the filename. That test was
removed the same day and `R8` is a zero death row again.

The row mutates `stem = naming.strip_head(title, template=template)` to read the
filename's own stem instead. Closing it required deciding which source is
correct, and that decision was never made. It was inferred from a docstring and
from the shape of the surrounding code, and the test was written to match what
the code already did. Driven afterwards against the real library, the code was
wrong: the filenames carry `Artist - Title` or `Title - Artist - Album` while
the title tag holds the title alone, so taking the body from the tag truncates
almost every name. 149 of 150 sampled files out of 9867 lose text. That is
R-168, and U41 owns the fix.

**The lesson is one turn of the screw tighter than the one above.** This doc
says a dismissal is a claim about the mutated tree and has to be driven there.
The same is true of a CLOSURE. A test written to make a zero row die, whose
expected value was read off the current behaviour rather than derived from a
decision about what the behaviour should be, does not pin a guard. It pins
whatever was there, and it converts an open question into a settled looking
green assertion. The row stopped reporting and nothing had been learned.

So the rule has two halves, and the second was learned expensively:

- A zero row is not dismissed until the mutated tree has been driven.
- A zero row is not CLOSED until somebody has decided what the correct
  behaviour is, from something other than the code under test. Otherwise the
  test is a characterization of the defect wearing the costume of a guard.

`R8` is deliberately left at zero. `tests/test_naming_apply_cli.py` carries a
comment where the test was, saying why, and saying not to close the row by
matching current behaviour a second time.
