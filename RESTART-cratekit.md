# Restart: Cratekit

**Last session 2026-08-26.** U40 merged and pushed. Board audit exit 0, 41
units, 40 done. **The pending register is EMPTY.**

**THERE IS NO TAKEABLE UNIT LEFT.** `board.py next` will name issue 29 and issue
29 is attended, Phillip's to perform against the live library, which an agent
cannot touch by standing constraint. Read "What is actually left" below before
picking anything up, because the next piece of work on this repository is a
decision rather than a queue entry.

## Do this first

1. `docs/METHOD.md`. The operating instruction: the merge bar, the workspace
   rules, the mutation table method, the driver rules, the four defect patterns,
   the battery, what CI is for, the merge constraints and the cost rules. **Read
   its "Do not touch" section before touching issue 29**, because the board will
   tell you to take it.
2. `CLAUDE.md` is the session contract.
3. This file for the current wave state. `docs/HANDOFF.md` is the longer
   narrative and its "State" section has been stale since U27; trust this file
   and `board.py` over it.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git log --oneline -1                        # subject below, and pushed
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

Main's tip subject names this file's own restart commit. **No hash is written
here on purpose**, since this file is part of the commit it would be naming.
Check the subject and `git status -sb` for the ahead or behind count instead.

**Forty units are done.** The last measured suite was **SUITE_COUNT**. **Main's
highest residual is R-186.** Append only.

## What the last session did

U40 built `crate tag retag`, the verb that can correct a genre that is already
wrong. `tag.folder` is fill-if-empty by construction, so a file arriving with a
vendor catch-all is skipped by every tagging verb, routes to the fallback bucket
and stays there for ever. The selection is the user's own taxonomy through
`is_too_coarse_as_source`, never a list in code, and two refusals hold it: an
answer that is itself too coarse is never written, and a file with NO genre is
never selected even though the predicate calls the empty string too coarse,
because that state is `tag.folder`'s under a different ownership policy.

Feature Inventory row 18 moved from Cut to Module, and the plan's own row 18
cell was amended in DJ_tools at `1e041cb` in the same sitting. **Those two trees
are coupled and the coupling is deliberate**: `tests/test_cutover_parity.py`
drift checks `registry.FEATURES` against the plan whenever DJ_tools is checked
out beside this repository, so editing either side alone leaves main red. If a
future unit moves a disposition, it moves both.

Read `docs/mutation/u40-author-full.md` and `docs/mutation/u40-author-round-2.md`
for the measurements. Six residuals are filed, R-181 through R-186.

**R-186 is the one to read.** `write/metadata.resolve_genre_id` defaults the
soft-delete marker to the permissive answer, which is the shape
`trees.soft_delete_marker` refuses by having no default. U40 did not write that
line and U40 is what gave it a caller: `plan_genre_retag` had no caller anywhere
in `src` before this unit, so the defect was dormant and is now reachable from a
verb a person types. The mechanism was driven; the producer was not, and METHOD's
do-not-touch section assigns that line to the parked conformance branch, which is
why it is filed rather than fixed.

## What is actually left, and none of it is on the board

**Issue 29, the cutover.** Attended, per workflow, against the live library.
Not an agent's. METHOD says why in its do-not-touch section and the reason does
not expire.

**Five Feature Inventory rows with no landed verb and NO ISSUE OWNING THEM.**
This is the part a `board.py next` reading will not show you:

| row | title | awaiting verb | declared in |
|---|---|---|---|
| 6 | vendored concurrent downloader | `acquire.download` | U15, CLOSED |
| 7 | fallback lossy acquisition | `acquire.audit`, `acquire.download` | U15, CLOSED |
| 29 | set builder | `setbuild` | U35, CLOSED |
| 30 | set recording mastering | `master` | U35, CLOSED |
| 31 | library backup | `backup.run` | U35, CLOSED |

Every one of those verbs still carries a `planned_in` marker naming a unit whose
issue is CLOSED. Four more verbs are in the same state and are NOT in the
backlog, because another landed verb covers their row: `session.ack` and
`session.release` (U8, row 12), `analyze.vocals` and `metadata.mytags-vocals`
(U25, row 10). So nine declared verbs have no module, and five of them are the
whole of what stands between this repository and a mechanically possible
cutover. `tests/test_cutover_parity.py` derives that table and
`test_the_cutover_is_not_yet_possible_and_says_why` fails on the day it empties.

**Building any of them is a DECISION, not a queue item.** Do not create issues
for them without Phillip saying so, and do not build one off the board.

**The residual ledger.** 186 entries, none of them queued. R-183 is the one with
product consequences: nothing in `src` claims a job item, so no long-running
verb's work is executed by shipped code. `crate tag retag` queues like every
other one and the engine behind it has no caller in `src`, exactly as
`tag.folder`'s has none.

**The parked conformance branch**, with its `write/metadata.py:195` defect live
on main. Out of scope until Phillip says otherwise. R-186 records what U40
changed about its reachability.

## The branches

| branch | tip subject | state |
|---|---|---|
| `fix/conformance-3-and-soft-delete-reader` | five defects in the scoping and exclusion rules | parked in `.worktrees/conformance`. Its `write/metadata.py:195` defect is live on main. Do not touch the worktree or the branch. |

## Standing decisions

- **The board is the BUILD, `docs/residual-findings.md` is the LEDGER.** Units
  and attended chores are issues; a residual earns one only if somebody decides
  to act on it. **Do not backfill.**
- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. **Main's highest is
  R-186.**
- **The pending register is empty.** `tests/test_pending_units.py` now carries a
  test that says so out loud, because an emptily parametrized countdown is
  SKIPPED by pytest and a silent skip is the exact hazard that file warns about.
  Re-opening any countdown re-arms the machinery with no edit.
- **CI does not run the suite and never will on Linux.** A step in the workflow
  must be able to pass. See METHOD.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. Pass `--repo-root` and
  `--out-dir` when driving a worktree from the main checkout's script.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Every unit gets a trailer**, and U24's exception is the only one left. Check
  which issue it is BEFORE writing the merge commit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, or `.worktrees/conformance`.

## Sixteen things that will bite you

**`board.py start N` TAKES THE ISSUE NUMBER AND WILL HAPPILY START THE WRONG
ONE.** This session ran `board.py start 40` for U40, which branched on issue #40,
a residual from the 2026-08-02 batch, and marked it In Progress. It refuses a
dirty tree and a blocked unit and it does not refuse a non unit. U40 is #58 and
U38 is #51. Look the number up with `board.py next` or `gh issue list` and read
the title back before you type it. Recovering is three steps: `git checkout
main`, delete the branch, `board.py sync` to recompute the status it changed.

**A WEAK ASSERTION PASSES FOR TWO MECHANISMS AND READS AS A GUARD.** U40's test
that the database plan is built from what was WRITTEN asserted an empty change
list. Planning from the selection instead also produces an empty change list, by
a different route: the refused row enters the plan with its genre stringified
from `None`, the lookup for a genre named "None" resolves to nothing, and the row
comes back SKIPPED rather than changed. One mutation, two mechanisms, one green
test. Assert what must NOT have happened on the other path, not only what did not
happen on this one.

**A PROPERTY BUILT INLINE IN A HANDLER IS UNREACHABLE RATHER THAN UNTESTED.**
`tag.retag`'s plan digest was computed inside the handler, so the property that
matters most about it, that it is a function of what the person was shown, could
only be driven through a configured machine, a job store and a gate. A mutation
replacing it with a constant killed nothing. Pulling `plan_for` out as a pure
function made it a three line test. When a mutation of a load bearing expression
kills zero, ask whether anything CAN reach it before writing a composite.

**A DERIVED POPULATION CAN SILENTLY SHRINK, AND THE COLLECTED COUNT IS THE ONLY
WITNESS.** `tests/test_queued_resume_contract.py` derives its guarded set from
`long_running` AND `argv_builder`. Removing `long_running` from an entry removes
that verb from every guard in the file, and the suite goes green with three fewer
tests. `mutate.py` refused to call it a zero because the collected count moved,
which is the whole reason that check exists. Any test file that parametrizes over
a derived population owes a guard on the population's own membership, not only on
its non emptiness.

**A GUARD THAT RUNS ZERO TIMES REPORTS THE SAME GREEN AS ONE THAT HOLDS.** U41's
central test was a loop over the planned moves with no assertion outside it, so
an implementation proposing no rename passed it. Any test whose whole body is a
`for` over a computed collection owes an assertion on that collection's length,
and R-173 is the worked case.

**A REVIEWER'S REASON FOR LEAVING A ZERO ROW AT ZERO IS ITSELF A CLAIM.** U39's
independent pass called one row unkillable because the file already equalled its
own rendered target. True of the unmutated tree, false under the mutation, which
is the only state that decides it, and that row was the direction that lost data.
An author's table is a draft; so is a reviewer's dismissal. Drive it.

**AND SO IS A CLOSURE, WHICH COST MORE.** A test written to make a zero row die,
whose expected value was read off what the code already does rather than off a
decision about what it should do, is not a guard. It is a characterization of
the defect wearing a guard's costume, and it converts an open question into a
green assertion nobody will revisit. That is how R-168 hid for a day inside a
row reported as closed. Decide the correct behaviour from something other than
the code under test, or leave the row at zero and say why.

**ADDING THE FIRST CALLER MAKES YOU THE OWNER OF THE CALLEE'S DEFECTS.** U40 was
the first caller of `write/metadata` anywhere in `src` and inherited two: an
operation nobody registered decides SKIP_UNOWNED for every change, so a sweep
that skipped `enable` would write nothing, raise nothing and report a clean run;
and R-186's permissive soft-delete default. Run `git grep -n "<function>" -- src`
before you write the call. Two hits, a `def` and an `__all__` entry, means the
failure paths are now yours.

**A POPULATION PIN CAN CATCH WHAT NO TEST OF YOURS DOES.** U40's empty-folder
branch raised a refusal slug `cause.REASONS` did not declare, so `refuse` would
have raised `UnknownReason` at the boundary instead of refusing. Nothing in the
unit's own suite typed an empty folder. `tests/test_reserved_causes.py`'s literal
population count is what reported it. When that file fails, look at what joined
before you move the number.

**RE-PINNING A POPULATION MEANS NAMING WHAT MOVED, NOT MATCHING A COUNT.**
Difference the two SETS against `origin/main`'s own tree extracted into a scratch
directory. U40 moved three pins in one test and each one names the members that
joined; U28 moved a holder count without moving the literal count, which a pin
watching totals alone reads as nothing happening.

**`board.py sync` CAN REPORT A CORRECTION IT DID NOT MAKE.** On 2026-08-25 it
printed "Corrected 2 item(s)" for a new issue it never added to the project, and
the next audit failed identically. Re-running it does not help. Add the item with
`gh project item-add 2 --owner philgutowski --url <issue url>`, then sync for the
derived status. Always re-audit after a sync rather than trusting its output.

**Scan the whole pushed RANGE for closing keywords, not the merge commit**, and
run it as a GATE that stops the push. Never write a closing keyword next to an
issue number, even to quote one; backticks do not defuse it.

**A COUNTDOWN DISCHARGE IS THREE EDITS IN ONE COMMIT.** The register is empty
now, so the next one to open is also the next one to get this wrong. Also:
removing the last entry leaves `frozenset({})`, and empty braces are a DICT, which
crashes the AST guard that reads the literal; and annotating the register turns an
`Assign` into an `AnnAssign` that guard was not looking for.

**A `path:` KEY IS COUPLED TO A LOCATION THE REGISTER CANNOT SEE.** `_is_absent`
resolves one against the repository root, so a key naming a location the landing
unit then has to change stays green forever and the register goes on claiming a
debt that is paid. That is R-158, and it is why `path:skills` never fired.

**Every agent gets its own worktree, its own venv and its own scratch directory.
None of that isolates the PROCESS TABLE.** Kill by PID. Build venvs with
`/opt/homebrew/bin/python3.12`. Never symlink a venv.

**A CHECKER THAT REIMPLEMENTS THE THING IT CHECKS WILL DRIFT FROM IT.** U28's
skill lint hand rolled a token walker doing three of argparse's jobs and checked
no positional at all, so six of eight broken shipped commands passed it. Hand the
input to the real thing.

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git worktree remove .worktrees/uNN
    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP
400`. Push one ref at a time. Still no pull requests.
