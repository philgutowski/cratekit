---
title: "A coordination note's fact went stale in two hours, and rewriting the note twice did not re-measure it"
date: 2026-08-14
category: workflow-issues
module: tests/_source_guards.py
problem_type: workflow_issue
component: development_workflow
severity: high
resolution_type: documentation_update
applies_when:
  - "A note in source names a future unit and tells a later merge what it must do"
  - "A note asserts the current state of a file on a branch the reader is not on"
  - "A paragraph containing a claim about another branch is being edited for other reasons"
  - "Two branches each grow their own copy of one walk and the copies must collapse into one"
  - "A constructor signature narrows on one branch while every caller on main still passes the wider one"
symptoms:
  - "A coordination note is right that a collapse is not textual and wrong about which copy carries the defect"
  - "A guard reports offenders in a source that has none"
  - "Dropping an argument raises nothing because resolution falls back to matching by dotted tail"
  - "The thing the merge actually had to fix was written down in advance, on the other branch, and never read"
related_components:
  - testing_framework
  - documentation
  - tooling
tags:
  - merge
  - coordination-note
  - guard
  - cross-branch
  - stale-documentation
  - import-resolution
  - silent-failure
  - cross-unit
---

# A coordination note's fact went stale in two hours, and rewriting the note twice did not re-measure it

## Context

Cratekit builds in units on separate branches, and several of those branches edit
one file. `tests/_source_guards.py` is the worst of them: it holds the shared AST
walks every structural guard reads, and R-57 (`docs/residual-findings.md:2946`)
records that three copies of one import walk were alive at once, on three
different branches, all answering "does this source reach that module" and not
all answering it the same way.

R-57 was fixed on `main` in its fourth round. Both of `main`'s own copies were
collapsed onto one `_import_targets`, which resolves a relative import's level
against the importing file's package instead of matching the module's dotted
tail. The two copies on other branches were deliberately not touched, because
several branches were editing the file and the change was kept minimal on
purpose.

So the author did the right thing and left a note, in the `ExitCodeImports` class
docstring. At `main` commit `be7b6e9` it read:

> U12 COORDINATION. This is the same walk ``ReviewImports`` does, asked about
> a different module, and the relative half of it is now literally shared:
> both call ``_import_targets``. U12 is generalizing ``ReviewImports`` into a
> module-parameterized ``ImportsOf`` on its own branch, and the conformance
> branch has a third copy as ``SoftDeleteNames``. All three merge textually
> clean in any order, so nothing will flag it. When they land together, this
> class collapses into ``ImportsOf(tree, EXIT_CODE_MODULE)`` with one
> narrowing, because this one records only the ``ExitCode`` symbol where
> ``ImportsOf`` records every symbol a source imported, and ``SoftDeleteNames``
> collapses the same way. THE COLLAPSE HAS TO TAKE ``_import_targets`` WITH IT.
> The two copies on the other branches still carry the suffix match this file
> has now replaced in both of its own, and a collapse onto either of them
> would reinstate the defect in one place instead of two. The residual
> "Two copies of one import walk still carry a relative-import defect" records that.

That is a good note. It names the file, the three symbols, the branches they sit
on, the exact collapse to perform, and the reason the collapse is dangerous. Its
central prediction was correct: on 2026-08-14 the U12 merge landed as `038168a`
and the three walks did merge textually clean, with nothing flagging the
collision.

This document is about the sentence carrying the note's whole warning, which was
true for one hour and forty seven minutes and was then rewritten twice without
being re-measured, and about the fact that the other branch had written its own
note naming the thing this merge actually had to fix.

## Guidance

**A rewrite is not a re-measurement.** This is the whole of it. Editing the
paragraph a claim lives in feels like revisiting the claim and is not. The
author here revised this very paragraph twice after its fact had gone false,
changing the sentences around it both times, and carried the false sentence
through unexamined on both passes.

**Measured, not inferred.** The claim's whole life, from git:

| when | what | the claim |
|---|---|---|
| 2026-08-03 12:29:41 | `70c160f` first writes "The other two copies still carry the suffix match this one replaced" | TRUE |
| 2026-08-03 14:17:26 | `646a464` on U12's branch replaces tail matching with package resolution | goes FALSE, 1h 47m later |
| 2026-08-03 20:01:59 | `1b80f00` rewrites the paragraph. "TAKE THE RELATIVE HANDLING BELOW WITH IT" becomes "TAKE ``_import_targets`` WITH IT", "instead of three" becomes "instead of two", the residual is recited by title. The stale sentence is carried through | still false |
| 2026-08-03 23:17:40 | `2fb7c8a` touches the paragraph again | still false |
| 2026-08-14 19:10:39 | `038168a`, the merge reads it | false for eleven days |

So the honest account is not "nobody ever measured it". Somebody did, and was
right, and the measurement had a shelf life of one hour and forty seven minutes
because it was a measurement of somebody else's branch. What failed twice after
that was the assumption that editing a paragraph refreshes it.

**Treat every coordination note as a measurement with a date on it.** It has no
expiry, no test, and no owner. MOST claims in this repository are either executed
by the suite or dated in `docs/residual-findings.md`. A docstring note is neither,
is written in the present tense about other people's branches, and those branches
keep moving after it is written.

That sentence said "every other claim" until 2026-08-14, and it was corrected the
same day by its own counterexample. The session contract asserted a false census
about the repository's own management state, neither executed nor dated, and it is
not a docstring note either, so it fell outside a set this document had called
exhaustive. See `a-false-claim-in-the-auto-loaded-contract-compounds-silently.md`.
A document about unverified prose is not exempt from writing some.

**A fact about another branch has a shelf life you do not control.** That is what
makes this different from ordinary documentation rot. The claim did not decay
because the code around it drifted; it was invalidated by a commit on a branch
its author could not see, less than two hours after being written, and no event
anywhere told them.

**When you edit a paragraph, re-measure every claim it makes about somewhere
else, or mark the ones you did not.** The cheapest version of this is a date and
an admission: a sentence reading "as of 2026-08-03 12:29, unverified since" would
have told the merge exactly how much to trust it.

**Obey the note's WARNING. Re-verify its FACTS.** A note tells you where to look.
It does not tell you what is there now.

**Read the other side's records, not just your own.** This is the correction that
costs the most to skip, and this merge skipped it. U12's branch had filed R-111
(`docs/residual-findings.md:6851`) on 2026-08-03, and it names the exact hazard
the merge would hit:

> **What the collapse must carry.** The `package` argument, at every call site
> that walks real files. Without it the walk falls back to the tail heuristic,
> which is deliberate so that inline fixtures with no package still work, and the
> five false positives come back in the single place every guard reads. That is
> strictly worse than three copies each wrong in its own corner, because one
> wrong answer would then be everybody's answer.

The merge found that defect by driving the callers, and would have found it
faster by reading the branch it was merging. **Two notes existed, one on each
branch, and each was accurate about its own side and wrong or silent about the
other.** R-111 confirms the symmetry from its own end: "The two sibling copies
were deliberately not read while this was decided, so the collapse still owes
them a comparison." Neither author read the other. Both wrote with confidence.

So the merge-time reading list is both sides' notes, and the branch's residual
file is part of the branch.

**Re-verify by driving, not by reading.** The check that settled the resolver
question was not reading the two functions' prose. Both are well documented and
both docstrings are honest, and reading them leaves open whether they AGREE,
because they are spelled differently. What settled it was implementing both in a
scratch script and running them over the same inputs. This repository has now
paid for that lesson twice, and the sibling document records the first time:
three accounts of a thirty line guard's behaviour were written from reading its
source, by three readers including an independent verifier, and the first two
were wrong in different ways.

**Check every place the note names, not just the one it emphasizes.** The note
made one claim about two copies, and it is half right. `SoftDeleteNames` on the
conformance branch has not moved and still matches by tail. A re-verification
that stopped at the first copy would have concluded "the note is stale" and been
half wrong in the more expensive direction.

**A note narrows attention, and narrowed attention is itself a hazard at a
merge.** The note pointed hard at one line of one function. The defect that
actually had to be fixed was a dropped argument in a two line subclass, which
exists only in the union of the two branches. After you have discharged a note,
ask separately what is wrong only in the union.

**When you find a note has aged, correct it or delete it in the same commit that
proves it aged.** A note that survives the event it was written for stops being
coordination and becomes a description of a branch that no longer exists. That
happened here and is still live, and the Examples section says exactly what is
still false in it.

**Keep writing the notes.** Nothing here argues against them. The note did the
one job a note can do that a test cannot: it warned about a collision no tool
would report, because both sides merge clean and both suites stay green. What
changes is what the note contains and what the reader does with it.

**Write the note so it can be checked rather than only obeyed.** Three things
make the difference, and the U12 note has the first two:

- Name the file, the symbol, and the branch, so the reader can go look.
- State the ACTION, in the imperative, so there is no ambiguity about what to do.
- State the FACT the action rests on as a falsifiable sentence, dated, and say
  whether you actually checked it. "As of 2026-08-03, unverified, I believe
  `ImportsOf` on U12's branch matches relative imports by dotted tail; if it does
  not, this instruction is void" is a sentence a reader can spend two minutes on.
  "The two copies still carry the suffix match" is a sentence a reader either
  believes or does not.

## Why This Matters

The value of the note and the cost of the note come from the same property: it is
the only record of a hazard no automated check can see. Told in the order it
happened.

1. **2026-08-03 12:29, `main`.** `70c160f` writes the first version of the note,
   including the sentence "The other two copies still carry the suffix match this
   one replaced". At this moment the sentence is true of both copies.

2. **2026-08-03 14:17, U12's branch.** `646a464` lands `_absolute_module`
   (`tests/_source_guards.py:71` at that commit) and `package_of`. From this
   moment U12's walk resolves a relative import against the importing file's
   package and falls back to tail matching only when no package is supplied,
   which is structurally the same design `main` adopts later the same day. The
   note's sentence is now false about one of its two copies, one hour and forty
   seven minutes after being written, and nothing on `main` can know it.

3. **2026-08-03 20:01 and again at 23:17, `main`.** `1b80f00` fixes R-57,
   introduces `_import_targets`, and REWRITES the note's paragraph: the
   imperative changes from "TAKE THE RELATIVE HANDLING BELOW WITH IT" to "TAKE
   ``_import_targets`` WITH IT", the count changes from "instead of three" to
   "instead of two", and the residual is recited by title rather than by number.
   `2fb7c8a` edits the paragraph again the same evening. The false sentence
   survives both passes unchanged. About `SoftDeleteNames` it stays correct, and
   it remains correct today.

4. **Also on U12's branch, R-111.** The branch's own review files the verdict on
   which walk to keep, and closes by naming what the collapse must carry: the
   `package` argument, or "one wrong answer would then be everybody's answer". It
   also records that the sibling copies were deliberately not read. Each side has
   now written a note about a collapse, and neither has read the other's.

5. **2026-08-14, the merge.** The note is read and its warning is taken. Its fact
   is checked rather than believed, and comes back half false.

6. **The two resolvers are compared on inputs rather than read.** Both were
   reimplemented in a scratch script and run over 5 packages of 1 to 5 parts,
   levels 1 through 7, and 4 module tails including the empty one that
   `from . import X` produces. 140 cases, zero disagreements. They reach the same
   answers by different routes on the interesting band, the climb off the top of
   the package tree: `main`'s guard is `node.level - 1 >= len(parts)`, the
   branch's is `level - 1 > len(parts)` followed by a separate `if not base`
   check, and the case each catches with a different clause is the same case.

7. **So the collapse onto the branch's resolver reinstates nothing.** Had the
   note been obeyed literally, the merge would have kept `_relative_module` and
   discarded `_absolute_module` and `package_of` with it: work performed to
   protect against a defect that was not there, on the copy R-111 had already
   argued was the one worth keeping.

8. **The real defect at this merge was in neither branch's diff.**
   `ReviewImports` on the branch took only a tree:

   ```python
   def __init__(self, tree: ast.AST) -> None:
       super().__init__(tree, REVIEW_MODULE)
   ```

   Every review caller on `main` passes a package positionally, for example
   `calls_review(source, "offer", "cratekit.core")` at
   `tests/test_review_queue.py:2230`. The subclass is correct on its branch,
   where no caller passes a package, and the callers are correct on theirs. Only
   the union is wrong. R-111 predicted this class of failure from the other side;
   the merge did not read R-111 and rediscovered it by driving.

9. **And the union is wrong SILENTLY.** Dropping the forward raises nothing. The
   argument reaches `ImportsOf` as `None`, resolution falls back to matching by
   dotted tail (`_dotted_tail_of`, `tests/_source_guards.py:59`), and the guard
   answers about the wrong file rather than erroring. `from . import review` in
   `cratekit.intake` and `from . import review` in `cratekit.core` are the same
   text naming different modules, and the tail fallback cannot tell them apart.
   That is the exact discrimination the level resolution was added to perform.

10. **Driven, not argued.** With the forward restored to the branch's form at
   runtime, and no tracked file modified, `tests/test_review_queue.py` goes from
   `147 passed, 1 skipped` to `3 failed, 144 passed, 1 skipped`.

The reason this is worth a document rather than a residual is that every
automated defence in this repository was working correctly and none of them could
fire. Both branches were green. Both suites were honest. The merge was textually
clean. The collision existed because three people solved the same problem at
once, and the only artifacts that knew about it were two paragraphs of prose on
two branches, each with no test behind it, neither read by the author of the
other.

## When to Apply

Apply this whenever you are about to act on a coordination note, a TODO naming
another branch, a docstring that says "when X lands", or a residual whose closing
condition describes work on somebody else's tip. Concretely:

- **The note describes a file on a branch you are not on.** That is the whole
  trigger. The note's author could not run the other branch's tests, and the
  evidence here is that they did not read its source either.
- **You are merging and the note's unit is one of the two sides.** The note was
  written to be read at exactly this moment, and this is also the moment its
  subject is most likely to have changed, because the branch it describes has had
  its whole life since.
- **Before merging, read the incoming branch's own records.** Its residual file,
  its handoff, and its mutation tables are part of the branch. The thing this
  merge had to fix was written down there in advance.
- **The note names more than one other place.** Check each independently. One
  having moved says nothing about the others, in either direction.
- **The note's instruction is "keep mine, discard theirs" or the reverse.** That
  is a claim about the relative quality of two implementations, and it ages
  fastest, because the losing side is usually the side being actively worked on.
- **After discharging the note, before declaring the merge done.** Ask what is
  wrong only in the union. Argument mismatches, one side generalizing while the
  other adds a parameter, and a guard's allowlist meeting another unit's new
  capability are all this shape.

Do NOT apply this as a reason to distrust notes generally, and do not spend the
re-verification budget on notes that are not load bearing. A note recording why a
line looks odd, or pointing at a document, carries no instruction and cannot
mislead an action. The ones worth re-measuring are the ones telling you to delete
something, keep something, or skip a check.

Do NOT re-verify by reading. If the note's fact is about behaviour, the check is
to run both behaviours over the same inputs.

## Examples

The U12 merge into `main`, 2026-08-14, merge commit `038168a`, parents `be7b6e9`
and `f7cae42`. Commit identifiers are given with the branch they sit on, because
this project uses no pull requests, so there is no PR number to cite.

**The two resolvers, compared on inputs.** `main`'s `_relative_module` takes an
`ast.ImportFrom` node and a package; the branch's `_absolute_module` takes a
package, a level and a module tail. The table drives both with the same logical
inputs. `main`'s helper is never reached at level 0, because `_import_targets`
guards it with `if not node.level` first, so level 0 is the branch's alone.

| package | level | module tail | `_relative_module` | `_absolute_module` | same |
| --- | --- | --- | --- | --- | --- |
| `cratekit.core` | 1 | `review` | `cratekit.core.review` | `cratekit.core.review` | yes |
| `cratekit.core` | 1 | (none) | `cratekit.core` | `cratekit.core` | yes |
| `cratekit.core.sub` | 3 | `review` | `cratekit.review` | `cratekit.review` | yes |
| `cratekit.core.sub` | 4 | `review` | `None` | `None` | yes |
| `cratekit.core.sub` | 5 | `review` | `None` | `None` | yes |
| `cratekit` | 2 | `review` | `None` | `None` | yes |
| `cratekit` | 1 | `exit_codes` | `cratekit.exit_codes` | `cratekit.exit_codes` | yes |

Rows four and six are the ones worth looking at, because the two functions reach
`None` by different clauses. At `cratekit.core.sub` with level 4, `main` returns
`None` from `node.level - 1 >= len(parts)`, which is `3 >= 3`; the branch's
`level - 1 > len(parts)` is `3 > 3` and does not fire, and the `if not base`
check catches the empty slice instead. At `cratekit` with level 2 it is the same
story one part shorter. The differently spelled guards cover the same band.

Swept exhaustively over 5 packages of 1 to 5 parts, levels 1 through 7, and 4
module tails including the empty one: 140 cases, 0 disagreements. The finding is
that the two implementations AGREE on every case checked, not that they are
identical, and the sweep covers importable and unimportable relative spellings
rather than all possible packages.

R-105 (`docs/residual-findings.md:6647`) measures the adjacent question from the
other direction: deleting the branch resolver's climb guard entirely kills zero
tests, because every input in the band it protects is an import the interpreter
itself refuses. That is a fact about the branch's function against itself rather
than about the two functions against each other, and the two measurements are
independent.

**The parameter mismatch, driven.** The forward was restored to the branch's form
at runtime through a pytest plugin living outside the repository, so no tracked
file was modified:

```python
def _branch_init(self, tree, package=None):
    g.ImportsOf.__init__(self, tree, g.REVIEW_MODULE)

g.ReviewImports.__init__ = _branch_init
```

Baseline, `tests/test_review_queue.py`: `147 passed, 1 skipped`. With the forward
dropped: `3 failed, 144 passed, 1 skipped`. The three:

- `test_a_relative_import_is_resolved_against_the_package_the_file_sits_in`, the
  `from .review import Queue, offer` parametrization. Fails at
  `tests/test_review_queue.py:2232` on
  `assert not calls_review(source, "offer", "cratekit.intake")`, reported as
  `assert not True`.
- The same test, the `from . import review` parametrization. These two are the
  two relative spellings a sibling of the review module would write, which are
  precisely the shapes R-57 was filed about.
- `test_the_countdown_reads_a_decision_store_through_a_relative_import`, failing
  at `:2294` with `assert {'record', 'revoke'} == set()`. That is a guard
  reporting two offending method calls in a source that has none, which is the
  wrong file being answered about.

The merge commit's body and the resolved docstring both describe the
`{'record', 'revoke'} == set()` shape as belonging to the first of the three
failures. Measured at `9b03c0e`, that shape belongs to the third in both
collection order and file order. The substance is unaffected: three tests fail,
both sibling spellings are among them, and the failure shape is a guard reporting
offenders where there are none.

**What the merge did about it.** Forwarded the argument, and recorded the reason
where the next reader will be standing, at `tests/_source_guards.py:265` onward.
That docstring carries the driven result rather than the reasoning, which is the
right half to keep.

**What the merge did not do, and the cost is live.** The note itself was left
untouched. At `9b03c0e` it is still at `tests/_source_guards.py:612`, still
present tense about a branch that has merged, and still telling a future reader
that `ImportsOf` carries a suffix match. The collapse it describes is genuinely
still outstanding: `main` today holds `ImportsOf` at `:118` and `ExitCodeImports`
at `:609`, and therefore two relative resolvers in one file, `_absolute_module`
at `:76` and `_relative_module` at `:533`. R-57 and R-111 both remain open
against that collapse. So the note still has a job. It is now describing a two
copy problem inside one file as a three copy problem across three branches, and
the next reader will spend this same trip again working out which sentences still
hold.

## Related

- `merge-falsifies-a-guard-invariant-and-every-remedy-breaks-something.md` and
  `countdown-entry-discharge-drops-a-whole-test-file.md`: the other two merge time
  traps in this directory. All three are invisible from either branch alone and
  exist only in the union. They differ in what the repository knew in advance and
  in the direction of the danger. The countdown trap silently removes evidence,
  so its danger is a merge that looks finished. The guard invariant trap produces
  a red that cannot be made green, so its danger is a merge that gets forced.
  **This one is the case where two authors saw it coming, each wrote down what to
  do, and neither read the other**, so its danger is a merge that confidently
  performs the wrong work. For the other two the question is "what could go wrong
  here". For this one the question is "which sentences in this warning are still
  true, and what did the other side write down".
- `a-false-claim-in-the-auto-loaded-contract-compounds-silently.md`: the fourth
  document in this directory and the only one that is NOT a merge trap. The other
  three fire when two branches meet; that one is always on, in a file every session
  reads before it does anything. It is this document's closest relative in
  mechanism, both being prose whose truth no check evaluates, and its furthest in
  radius: a note misleads one merger for one merge, a contract misleads every
  session for as long as it stands. It also corrects the overclaim in the Guidance
  above.
- `docs/METHOD.md:17`, the merge bar's first condition (section heading at `:11`): "It was driven end to end, not
  argued from reading the source." The re-verification here is that rule applied
  to a NOTE rather than to a finding. The sibling document already extended it
  from a finding's existence to a finding's mechanism; this extends it to the
  standing instructions a merge inherits.
- `docs/METHOD.md:154`: "Every number was measured or the report says it was not."
  The note is the counterexample that shows the rule needs a home in prose too. It
  stated an unmeasured fact without saying it was unmeasured, in a kind of artifact
  whose truth the battery cannot judge. The battery DOES read the file, hunting
  machine specific paths and secrets; what it never does is ask whether a sentence
  is true. An earlier wording here said the battery cannot read it, which is a
  different and false claim, corrected 2026-08-14.
- `docs/residual-findings.md`, R-57: the origin. It created the note, names all
  three copies, and carries its own correction, because an earlier round recorded
  a live defect as living on somebody else's branch. That correction is this same
  error class one step earlier, in the same file, by the same author.
- `docs/residual-findings.md`, R-111: U12's own verdict on which walk to keep,
  filed on the branch as R-17. It names the `package` argument as the thing the
  collapse must carry, which is exactly what the merge had to add, and it records
  that the sibling copies were deliberately not read. The two notes are mirror
  images and neither author saw the other's.
- `docs/residual-findings.md`, R-105: the zero row on the branch resolver's climb
  guard. Adjacent to the comparison table above and measuring a different pair.
- `docs/residual-findings.md`, R-103 through R-107 and R-108 through R-114: U12's
  twelve residuals, and the renumber that split them.
- Merge commit `038168a` on `main`: the contemporaneous account. Read it with
  `git show 038168a`, and read the pre-merge note with
  `git show be7b6e9:tests/_source_guards.py`. Its body says the note "had aged",
  which this document corrects: the note was false the day it was written.
- `docs/wave-state-2026-08-14.md:344`, "U12 merged, and the coordination note that
  had aged": the session narrative, carrying the same correction.
- `tests/_source_guards.py:258`, `ReviewImports`: the resolved code, whose
  docstring records the parameter mismatch and the three failing tests. The
  neighbouring `ImportsOf` docstring at `:118` explains why the package argument
  makes the relative half exact rather than approximate.
