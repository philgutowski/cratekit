# Restart: Cratekit

**Last session 2026-08-24.** U27 and U28 both merged and pushed. Board audit
exit 0, 38 units, 37 done. **The pending register is EMPTY for the first time in
this build**, and the only open unit is issue 29.

## Do this first

1. `docs/METHOD.md`. The operating instruction: the merge bar, the workspace
   rules, the mutation table method, the driver rules, the four defect patterns,
   the battery, what CI is for, the merge constraints and the cost rules. **Read
   its "Do not touch" section before touching issue 29**, because the board will
   tell you to take it.
2. `CLAUDE.md` is the session contract.
3. This file for the current wave state. `docs/HANDOFF.md` is the longer
   narrative.

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

**Thirty seven units are done.** The last measured suite was **6239 passed and 1
skipped**. **Main's highest residual is R-164.** Append only.

## What the last session compounded

Two learnings were filed, both in `docs/solutions/workflow-issues/`, and both
came out of an adversarial review returning BLOCKING on a unit whose own battery
was green.

- `adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`,
  from U27. A restore whose every transfer failed exited OK, and the callee had
  shipped that way for as long as nothing called it.
- `a-checker-that-reimplements-what-it-checks-drifts-and-stays-green.md`, from
  U28. It also extends `CONCEPTS.md`'s Guard entry with a third axis, whether a
  guard consults the real subject or a model of it.

The second one flags one thing for a human to decide rather than doing it:
`docs/METHOD.md`'s "What a green suite cannot see" list has four items, and this
learning is a fifth of exactly that shape. METHOD is the auto loaded contract, so
a compound run does not edit it.

## The one open unit, and why the board is wrong about it

`board.py next` says **Take #29**. Do not take it. Ready is a statement about
DEPENDENCIES and not about who can do the work, and all seven of U29's blockers
are now closed, which is the only reason it says Ready.

U29 is the cutover and retirement of the live system. Its own brief says
**attended per workflow, do not batch cutovers**, and it requires each
replacement to run correctly **on the live library at least once**. The live
rekordbox database is off limits by standing constraint, so an agent can prepare
for U29 and cannot perform it. `docs/METHOD.md` now says this in the do-not-touch
section rather than just naming the unit, so the reasoning does not have to be
rediscovered.

**What is already prepared for it.** `tests/test_cutover_parity.py` is the parity
table U29's own test scenario asks for. It derives coverage from the verb
registry and fails when a Feature Inventory row has no covering verb, in both
directions.

**The cutover backlog is TEN of thirty seven rows, and it splits in two.**

| half | rows | waiting on |
|---|---|---|
| declared and unbuilt | 6, 7, 29, 30, 31 | a unit that exists: `acquire.download`, `acquire.audit`, `setbuild`, `master`, `backup.run` |
| cited by no registry entry at all | 16, 18, 19, 23, 32 | somebody deciding whether the product covers them |

The second half is the one that surprises. A parity table derived from the
registry alone reports those five as though they do not exist, which is why the
test reads the inventory instead. The first measurement taken for U28 put the
backlog at five.

## What else is open, and none of it is the queue

Every other open issue is the residual ledger or an attended chore: #38 through
#54 are residual issues from a single batch created on 2026-08-02, and A1 (#49)
and A2 (#50) are attended chores. **Do not take a residual issue and do not
backfill the rest of the ledger onto the board.**

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
  R-164.**
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

## Nine things that will bite you

**Scan the whole pushed RANGE for closing keywords, not the merge commit**, and
run it as a GATE that stops the push. Never write a closing keyword next to an
issue number, even to quote one; backticks do not defuse it.

**A unit's issue number does NOT reliably match its unit number.** U38 is #51.

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

**Reconcile the collected count by IDENTIFIER, under `LC_ALL=C`, against the
UNION of both sides.** A total moving by the right amount is not a reconciliation.

**A FINDING'S MECHANISM HAS TO BE DRIVEN, NOT ONLY ITS EXISTENCE**, and so does
its CAUSE. Both of U28's blocking findings were driven again locally before being
acted on, and doing so corrected the reported count on one of them.

**Re-pinning a population means naming what moved, not matching a count.** Name
the module by differencing the two SETS against `origin/main`'s own `src` tree
extracted into a scratch directory. U28 moved the holder count without moving the
literal count, which a pin watching totals alone would read as nothing happening.

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
