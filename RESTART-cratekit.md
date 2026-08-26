# Restart: Cratekit

**Last session 2026-08-26.** U43 merged and pushed. Board audit exit 0, **45
units, 41 done, 4 ready**. **The pending register is EMPTY.**

**`board.py next` WILL SAY "Take #29" AND YOU MUST NOT.** Issue 29 is attended,
Phillip's to perform against the live library, which an agent cannot touch by
standing constraint. It ranks first only because it is the one unit with a
dependent. **The three takeable units are #60, #62 and #63**, and they are all
Ready, all independent of each other, and each releases nothing, which is why
they rank below an untakeable unit.

**Take #62 next if you are taking one.** It is the smallest of the three: one
verb over one engine, where #60 is two verbs over one module and #63 also has to
publish the backup age the write session consults. All three QUEUE, unlike #61,
so each of them needs an argv builder and has to satisfy the resume contract.
Read U43's shell first, `src/cratekit/setbuilder/cli.py`, then
`src/cratekit/tagging/retag_cli.py` for the queueing half U43 did not need.

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

**Forty one of forty five units are done.** The last measured suite was **6354
passed and 1 skipped**. **Main's highest residual is R-190.** Append only.

## What the last session did

U43 built `crate setbuild`, the shell over the set-building engine U35 landed.
It is a pure read: no database, no job, no byte written.

**THE ANCHOR IS A PATH UNDER THE LIBRARY, NOT A TYPED TITLE**, and that decision
is the unit. The engine's `resolve_anchor` fuzzy matches a typed string, and
`token_set_ratio` scores a subset at 100, so an exact query naming a track and
that track plus a version suffix are indistinguishable and `extractOne` returns
whichever it met first. Driven, not argued. A path is also what every other
file-taking verb accepts, so a test hands it something under the configured
library rather than a real path off somebody's machine (R1). The cost, stated
rather than hidden: an unowned anchor and a supplied Camelot key cannot be
expressed at all, and both exist to serve a web lookup this product does not
ship.

**IT WRITES NO CACHE, AND THAT IS THE OTHER DECISION THE BRIEF ASKED FOR.**
`build_index` accepts a `cache_path` and `config` declares
`setbuilder_index_cache` waiting for one. Passing it would be a `files` write
from an entry declaring none, and declaring one makes the verb destructive by
`Entry.__post_init__`'s own invariant, which binds the library lock, the backup
acknowledgment and the volume identity assertion to a read-only recommender.
Filed as R-188 rather than paid for quietly.

Read `docs/mutation/u43-author-light.md` and its round two companion: 25 rows
then 10, and **round two is where the value was**, as it was for U40. Round one
left five user-facing zeros and every one of them was a real gap. Four residuals
are filed, R-187 through R-190.

**THE VERIFICATION GAP, STATED BECAUSE NOBODY ELSE WILL SAY IT.** Both tables are
the AUTHOR'S. No independent verifier ran, because the session was instructed not
to spawn one. METHOD asks a light pass to be run by an agent that did not write
the code, and the measured gaps between an author's table and an independent one
on this project are 10 against 17, 39 against 49, and 49 against 83. Every zero
in those two tables reads as "the author could not kill it", never as "nothing
can". If a later session wants a cheap high-yield target, this unit is one.

## What is left

**Three of the four new units, #60, #62 and #63.** Each is a command-line SHELL
over an engine that already shipped, and together they clear the rest of the
cutover backlog. Created 2026-08-26 on Phillip's decision, after the U40 handoff
found five Feature Inventory rows uncovered with no issue owning any of them.

| issue | unit | verb(s) | row(s) | engine that already exists |
|---|---|---|---|---|
| #60 | U42 | `acquire.download`, `acquire.audit` | 6, 7 | `src/cratekit/acquire/download.py` and siblings |
| ~~#61~~ | ~~U43~~ | `setbuild` | 29 | DONE 2026-08-26, `src/cratekit/setbuilder/cli.py` |
| #62 | U44 | `master` | 30 | `src/cratekit/modules/tools/mastering.py` |
| #63 | U45 | `backup.run` | 31 | `src/cratekit/modules/tools/backup.py` |

**FOUR ISSUES FOR FIVE ROWS, AND THE ARITHMETIC IS DELIBERATE.** Rows 6 and 7 are
both served by `acquire.download` in one module, `cratekit.acquire.cli`, and the
`planned_in` countdown keys on the MODULE rather than the verb. Splitting them
would create two units that must land together, which is the hazard the countdown
machinery exists to prevent.

**THE THREE THAT ARE LEFT ALL QUEUE, AND U43 DID NOT.** Every one of them is
`long_running`, so each needs an `argv_builder` and has to satisfy the resume
contract, and a gate answered inside a queued verb has to freeze its gate run or
the respawned child meets the gate with nothing recorded. `retag_argv` in
`src/cratekit/tagging/retag_cli.py` is the worked example and its docstring says
why. U43's shell is the model for the read-only half and for nothing else.

**Why they existed as a gap at all.** Every one of the remaining verbs carries a
`planned_in` marker naming a unit whose issue is CLOSED: U15 and U35 landed the
engines and never landed the shells. Four more verbs are in the same state and
are NOT in the backlog, because another landed verb covers their row:
`session.ack` and `session.release` (U8, row 12), `analyze.vocals` and
`metadata.mytags-vocals` (U25, row 10). Eight declared verbs now have no module,
down from nine, and four of them are what stands between this repository and a
mechanically possible cutover. `tests/test_cutover_parity.py` derives that and
`test_the_cutover_is_not_yet_possible_and_says_why` fails on the day it empties,
which is the day #60, #62 and #63 are all done.

**A UNIT ISSUE IS IDENTIFIED BY ITS `unit` LABEL, NOT BY ITS TITLE.** `board.py`
reads `"unit" in labels` at `scripts/board.py:113`. All four of these were created
without it and were invisible to `next` and to `audit` while looking perfectly
correct on the board, because the title regex at `:50` is only used to name a
branch. If you create a unit issue by hand, `gh issue edit N --add-label unit`
then `board.py sync`, then re-audit.

**Issue 29, the cutover.** Attended, per workflow, against the live library.
Not an agent's. METHOD says why in its do-not-touch section and the reason does
not expire. It stays first in `board.py next` because ranking is by transitive
reach and it is the only unit with a dependent.

**The residual ledger.** 190 numbers, 189 entries, none of them queued. R-183 is
the one with product consequences: nothing in `src` claims a job item, so no
long-running verb's work is executed by shipped code. `crate setbuild` is the
first verb in a while that is UNAFFECTED by it, because it does not queue at all,
and all three units left do queue, so this gets worse before somebody fixes it.
Of U43's four, **R-187 is the one to read**: the engine's fuzzy anchor lookup
returns the wrong track for an exact query, driven, and it stays a residual only
because two candidate producers were driven and neither reaches it.

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
  R-190.**
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

## Twenty things that will bite you

**A FIXTURE CAN SIT WHERE THE THING IT TESTS CANNOT MATTER, AND IT LOOKS
IDENTICAL TO A GUARD.** U43 wrote a lossy-marked fixture to close a zero row and
put the marker at the END of the title. The renamer writes it immediately AFTER
the head, and only there does the head parser strip it, so the guard would have
passed under the very mutation it was written to catch and the row would have
been reported closed. Caught by driving both positions before writing the
assertion, and pinned afterwards by a row that MOVES the marker to a position the
parser ignores: if the guard survives that, its fixture is in the dead position.
When you write a test to kill a zero, add a row that breaks the test's own
premise, not only the code's.

**A CAP CAN LAND ON ONE CONTRIBUTOR AND THE OUTPUT BOUNDARY WIDENS IT BACK.**
`--count 2` returned five items, because `build_plan` caps the pool while the
sequence is drawn from the FULL ranked list and was then unioned back in. The
test asserting the cap passed, because the fixture yielded fewer companions than
the default and both branches produced the same five. Two defects wearing one
green: a fixture too small to discriminate, and a surface whose arithmetic was
invisible. `totals` now reports `pool` beside `count`.

**A REGISTRY FLAG A PARAMETRISATION KEYS ON REPORTS AS A COLLECT ERROR, AND THAT
IS THE CORRECT READING.** Restoring `planned_in` on a landed entry moves the
collected count by two, three landed-only conformance cases leaving and one
countdown case arriving. `mutate.py` refuses to call it a zero and names twelve
kills. Read the kills and say what the drift was; do not chase a clean number.

## The seventeen that were already here

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
its non emptiness, and `tests/test_cli_contract.py` now carries that one.

**AND A REGISTRY FLAG A PARAMETRISATION KEYS ON CANNOT BE MEASURED CLEANLY AT
ALL.** This is the correction to the entry above, and it is written down because
the first attempt at it was a confident wrong justification of exactly METHOD's
fourth pattern. Moving the guard to a file whose count "does not move" does not
work: `test_conformance_5_long_work_is_queued_rather_than_run_inline` parametrises
over `long_running` too, so the count still moved, 532 to 531. Wherever such a
guard lives, removing the flag drops parametrised cases somewhere and the driver
reports drift rather than a death. What the move actually bought is smaller and
real: three cases of drift became one, and the row now NAMES its kill instead of
reporting nothing. Do not chase a zero-drift measurement for a flag like this;
read the named kills and say what the drift was.

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
