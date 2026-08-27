---
title: "Keeping a fixture green under a new guard is not evidence the guard is tested"
date: 2026-08-27
category: workflow-issues
module: "src/cratekit/modules/tools/mastering.py, tests/modules/test_tools.py, docs/mutation/u44-author.md"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: missing_validation
resolution_type: test_fix
applies_when:
  - "A mutation table row measures zero deaths on a guard just added in the same commit"
  - "An existing test's stand-in fixture or fake runner is edited in the same commit that adds a new guard, to keep an unrelated assertion green under it"
  - "A fixture starts writing, producing, or returning something only because a newly added guard now requires it to"
  - "A test's name or docstring already claims to cover the function a new guard was just added to"
  - "A zero-death row is about to be dismissed as covered because a same-function test already exists"
symptoms:
  - "A guard added in the mutation row is reverted by the row and kills zero tests, even though a test directly exercises the function it guards"
  - "The same commit that adds the guard edits an existing test's stand-in runner or fixture to keep an old assertion passing under it"
  - "A comment above the fixture edit explains why the runner now writes or produces something, but the explanation is scoped to preserving an unrelated assertion"
  - "No assertion anywhere checks the guard's own refusal or success condition"
  - "The gap closes only when a new test is added later, asserting the specific behavior the guard exists to enforce"
related_components:
  - development_workflow
  - documentation
tags:
  - mutation-testing
  - zero-row
  - fixture-edit
  - test-fidelity
  - guard
  - silent-failure
  - mastering
  - concat-guard
---

# Keeping a fixture green under a new guard is not evidence the guard is tested

## Context

U44 built `crate master`, the CLI shell over the mastering engine U35 landed and never
gave a surface to, closing issue #62 with merge commit `921c8b6`, "merge: the master
shell, and the archive no flag can switch off", reachable from `main` (`git log
--oneline -5 main` shows it as the tip). This repository forbids pull requests by
contract, "Feature branch per unit, merge to main locally, push main, delete the
branch", so the merge commit is the citation and there is no PR number.

The unit's own merge message names a finding it owned as first caller: the engine
reported success over an output it never read. An encoder that exits zero and writes
nothing left `mastering.master` returning a `Report` whose `output_bytes` fell back to
`0` and whose `size_reduction` was therefore `1.0`, a clean report over a file that was
not there. The fix is `_wrote_or_refuse`, added at
`src/cratekit/modules/tools/mastering.py:645`, whose docstring states the reasoning and
is called once after the main encode, `mastering.py:606`, and once after
`concatenate`'s join, `mastering.py:736`. The merge message calls this second call site
"the same shape one function over, found by sweeping for it rather than by anybody
reporting it".

`concatenate` (`mastering.py:683`) joins a recording a device split across several
files, using ffmpeg's concat demuxer under a stream copy. Before U44 it read the join's
zero exit status as proof the file existed and returned the destination path unread.
`git grep -n "concatenate(" -- tests src` returns six lines: the `def` itself, two call
sites, both in `tests/modules/test_tools.py:1057` and `:1077`, and three `np.concatenate`
calls in `src/cratekit/analysis/vocal.py:86` through `:88`, which are numpy's function
and not this one. So nothing in `src` calls `concatenate` at all as of this merge, a
fact `mastering.py:734` states directly in its own comment. The unrelated hits are worth
naming rather than filtering out silently, because a reader who runs the command and
sees six lines where the prose promised three has been handed a reason to distrust the
rest of it.

U44's round one mutation table, `docs/mutation/u44-author.md`, measured row
`B3_concat_output_unread`: reverting the `_wrote_or_refuse(destination, "join")` call
back to a bare `return destination` and running the suite. Baseline was green at 6380
collected, and the row's own record is exact:

```
Collected: 6380 against a baseline of 6380
Kills: 0 (zero)
Promoted: subset killed 0, full suite killed 0
Note: confirmed on the full suite
```

A guard that was driven into production, then measured against the whole suite, and
found by that suite to change nothing observable anywhere. The table's own framing for
a row like this is blunt: `USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify
it` (`docs/mutation/u44-author.md:37`). Round two re-measured the identical row after a
new test was added and reports it killed, by exactly one test:

```
Collected: 151 against a baseline of 151
Kills: 1 (killed)
Killed:
  - tests/modules/test_tools.py::test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning
```

The old and new text on both rows is identical, `_wrote_or_refuse(destination, "join")`
reverted to `return destination`. What changed between round one and round two is not
the mutation. It is what the suite had to say about it.

## Guidance

**When you edit an existing fixture, not write a new test, so a pre-existing test stays
green under a newly added guard, that edit is the signal to add the assertion the guard
owes, in the same sitting.** The two acts look similar and are not the same act. Editing
a stand-in so it satisfies a new precondition makes a test pass. Writing an assertion
against the guard's failure branch is what makes a test say anything about the guard.
Doing only the first and calling the sitting closed is how B3 measured zero: the fixture
was made to succeed under the new check, and nothing was ever written that made it fail
under the check's absence.

This is a different shape from the one
`docs/solutions/workflow-issues/a-fixture-where-the-mutated-line-cannot-matter-fails-red-first.md`
documents, and the difference is worth stating precisely rather than folding the two
together. That doc's case, U43's `H4_template_loses_the_marker`, is a new test written
specifically to close a zero row. It fails red on correct code first, because the
fixture places a marker in a string position the parser's anchored regex cannot reach,
so the guard's own assertion is false on both the correct tree and the mutated one. The
diagnostic that doc teaches is: when a guard written to kill a zero row comes back red,
drive both trees before repairing the expectation, because the fixture may be sitting
somewhere the mutated line cannot touch.

B3 never reached that moment, because no new guard was ever written in round one. The
fixture here does reach a passing state, on both the correct tree and the mutated one,
for a much simpler reason: the edited stand-in writes the destination file
unconditionally (`tests/modules/test_tools.py:1054`,
`Path(command.argv[-1]).write_bytes(b"joined")`), so `_wrote_or_refuse`'s check,
`target.exists() or target.stat().st_size == 0`, is satisfied whether the check runs or
not. There is no red assertion to diagnose, because the pre-existing test's own
assertion, `assert "it''s part one.wav" in written["text"]` (`test_tools.py:1058`), was
never about the new guard's property in the first place. It is about quote escaping in
the concat list file. The fixture edit was mistaken for coverage of a property the test
was never written to check.

Where U43's H4 is a discrimination failure in a guard that exists, B3 is a guard with no
discriminating test at all, wearing a coverage number that looked like one because the
existing suite still passed. `docs/METHOD.md`'s zero-is-a-finding rule caught this
correctly on the first measurement, what the round one table could not do by itself was
turn that finding into a fix. That required someone to read the zero, notice the
fixture edit was defensive rather than exploratory, and write the test the edit had
made unnecessary to write.

## Why This Matters

A comment explaining a guard is not an assertion of it. The comment added at
`test_tools.py:1048` through `:1053` is a genuinely good comment: it names U44, names
what changed, and names why leaving the write out "would make the fixture assert that
the join is unchecked". It is exactly right about what not writing the destination
would have meant. It says nothing, and was never going to say anything, about what
leaving the guard itself out would mean, because the test the comment sits in was never
driving that branch. A comment can describe a property correctly and still not be the
thing that measures it. Only an assertion against the guard's failure branch, a runner
that returns `returncode=0` and writes nothing, does that, and that assertion did not
exist until round two.

A fixture edited to satisfy a guard's precondition produces a test that is silent about
the guard's failure branch, by construction, whether or not the person editing it
intends silence. `CONCEPTS.md`'s Mutation table entry names the general shape one level
up: coverage measures which lines ran and a mutation table measures which lines
mattered. The edited stand-in makes every line of `_wrote_or_refuse` run, since the
guard's `if` condition is evaluated and found false. It makes none of them matter,
since the same run happens with the guard deleted. Coverage tooling would have reported
this line green on both trees, exactly the gap the mutation table exists to close, and
the table did close it, correctly, as a zero.

What a mutation table cannot do on its own is tell a reader why a row is zero, only
that it is. `CONCEPTS.md`'s account of a real mutation zero versus an inert one, and the
further causes underneath it (an assertion that observes an absence both trees produce,
a fixture that cannot reach the state a guard is about) all describe reasons a row can
measure zero honestly. B3 is closest to, and not identical to, the fixture-reach
family: the fixture here was fully capable of reaching the failure state, as round two's
new test proves by using the same runner shape with the write removed. The gap was not
structural. It was that nobody had yet asked the fixture to reach it, because the
sitting that touched this test was answering a different, narrower question, "does the
apostrophe survive quoting", and the destination write was added only to keep that
question answerable at all under the new check.

That is why round two's targeted re-measurement, not just a new green suite, is what
closed this. Re-running the identical `B3_concat_output_unread` row, byte for byte, is
what confirms the new test actually discriminates rather than merely existing beside the
old one; a new test that also failed to exercise the guard's failure branch would have
left the row at zero regardless of how confident its author felt writing it. The round
two table's one-line record, "Killed: 1 (killed)" naming
`test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning` by name,
is the only thing in this record that is actually evidence the guard is tested, as
opposed to merely present.

`concatenate` is also, as of this merge, a function with no caller anywhere in `src`
(`git grep -n "concatenate(" -- src` returns its own definition and the three
`np.concatenate` calls named above, which are a different function). That is the
precondition
`docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`
argues makes a function's defects easy to leave unreviewed, since nothing exercises its
failure paths except its own suite. The parallel is real and only partial: that doc's
case is about a function whose caller newly made a dormant defect reachable from a
shipped verb. Here the same unit both added the guard and owns the only tests that touch
it, and `concatenate` is still not reachable from any shipped verb; the gap this doc
describes is inside the function's own test coverage rather than between the function
and a caller. Worth knowing both traps sit in the same unit's work. Not worth treating
as one trap.

## When to Apply

- You are editing a stand-in, mock, or fixture used by a pre-existing test, specifically
  to keep that test green after adding a new check, guard, or precondition to the code
  it exercises. That edit is defensive: its purpose is to make the stand-in succeed,
  not to explore what happens when it fails.
- The edit adds behaviour to the stand-in (writing a file, returning a different value,
  populating a field) that the guard now requires, and the test's own assertions say
  nothing about that behaviour, only about something else the test was originally
  written to check.
- A mutation row against the new guard measures zero on the existing suite, and the
  suite already contains a test that reaches the guarded code path. Read that test's
  assertions before assuming a new test is needed from scratch, the gap may be that an
  existing test's fixture was widened to pass, not that no test reaches the code at all.
- Before closing the sitting, ask the complementary question the edit itself answers by
  omission: what does this code do when the new precondition is not met. If no test in
  the suite constructs that state, the guard has a comment and no assertion.

## Examples

Before U44,
`tests/modules/test_tools.py::test_joining_split_parts_quotes_a_path_containing_an_apostrophe`
drove `concatenate` with a stand-in that recorded the ffmpeg concat list text and
returned success without writing anything. U44 added `_wrote_or_refuse(destination,
"join")` at `mastering.py:736`, so the unmodified stand-in would have made every call to
`concatenate` in the suite raise `MasteringRefused`. The fixture was edited in the same
commit, `53c31e0`, to keep the test's real subject, quote escaping, reachable:

```python
def runner(command):
    listing = Path(command.argv[command.argv.index("-i") + 1])
    written["text"] = listing.read_text()
    # THE STAND-IN WRITES THE DESTINATION, because a real ffmpeg does and
    # U44 made ``concatenate`` read its own output. Before that, a zero exit
    # status was taken as proof the join happened and the path was returned
    # unread, so this runner could report success over a file that was never
    # created. Leaving the write out here would make the fixture assert that
    # the join is unchecked, which is the behaviour that was removed.
    Path(command.argv[-1]).write_bytes(b"joined")
    return mastering.CommandResult(returncode=0)

mastering.concatenate([part], tmp_path / "joined.wav", runner=runner)
assert "it''s part one.wav" in written["text"]
```
(`tests/modules/test_tools.py:1045` through `:1058`)

The comment is accurate and the test's one assertion never mentions
`_wrote_or_refuse`, the exception it can raise, or the file it checks for. Reverting the
guard produces byte-identical behaviour on this fixture, which is exactly what round
one measured.

Round two added the test the edit had made room for without writing:

```python
def test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning(tmp_path):
    """Closes B3 in ``docs/mutation/u44-author.md``.

    The test above adapted its stand-in to the check U44 added and asserted
    nothing about the check itself, so the guard could be removed and the file
    stayed green. This is the row's premise: a zero exit status over no output is
    a refusal, not a path.
    """
    part = tmp_path / "part.wav"
    part.write_bytes(b"")
    destination = tmp_path / "joined.wav"

    def silent_success(command):
        return mastering.CommandResult(returncode=0)

    with pytest.raises(mastering.MasteringRefused) as excinfo:
        mastering.concatenate([part], destination, runner=silent_success)
    assert excinfo.value.refusal is mastering.Refusal.ENCODER_FAILED
    assert not destination.exists()
```
(`tests/modules/test_tools.py:1061` through `:1079`)

The only difference from the existing stand-in is what it leaves out: `silent_success`
returns a zero exit code and writes nothing, which is precisely the state the earlier
edit made permanently unreachable in that other test. Round two's table confirms this is
what closed the row, naming the new test as the sole kill against the identical
old and new text pair from round one.

## Related

- [A fixture in a position where the mutated line cannot matter fails red first, and the obvious repair makes the guard green on both trees](a-fixture-where-the-mutated-line-cannot-matter-fails-red-first.md).
  The nearer neighbour by subject, both are this project's mutation-zero postmortems
  from the same week of units, and a different shape by mechanism. That doc's guard is a
  new test that fails red first because its fixture sits where an anchored parser cannot
  reach it, the repair a person reaches for first, adjusting the expected value, is what
  turns the dead fixture into a permanent characterization. B3 never produces a red
  assertion to repair, because no new test existed in round one at all: the pre-existing
  test's fixture was edited defensively to stay green, and its own assertion was never
  aimed at the guard. Read that doc for the red-first diagnostic, this one is for the
  earlier moment, deciding whether an edited fixture needs a companion assertion before
  the sitting that touched it is called done.
- [Adding the first caller to an existing function makes you the owner of its unreviewed defects](adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md).
  Adjacent, not identical. `concatenate` has no caller anywhere in `src` as of this
  merge (`git grep -n "concatenate(" -- src` returns the definition plus three unrelated
  `np.concatenate` calls in `src/cratekit/analysis/vocal.py`), which is the
  condition that doc's rule keys off. But U44 is not a new caller making a dormant
  defect in someone else's code reachable, U44 both wrote the guard and owns the only
  tests that touch it, and the function remains uncalled from any shipped verb. The
  overlap is that an uncalled function's tests are shaped by whoever last had a reason
  to care, and here that person edited a fixture for a narrower reason than the guard
  needed.
- `docs/mutation/u44-author.md`, row `B3_concat_output_unread`, the round one
  measurement that reported the zero: killed 0 of 6380, confirmed on the full suite,
  promoted.
- `docs/mutation/u44-author-round-2.md`, the same row re-measured after the new test
  landed: killed 1 of 151, naming
  `test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning` as the
  kill.
- Merge commit `921c8b6`, "merge: the master shell, and the archive no flag can switch
  off", closing issue #62. `docs/residual-findings.md` R-191 through R-194 are this same
  unit's residuals and are unrelated to this finding, B3 was closed with a real test in
  the branch, never filed as a residual.
