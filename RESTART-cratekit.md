# Restart: Cratekit

**Last session 2026-09-02, U55 on `relay/73`.** The collection reader landed, so
`adopt.scan` and `adopt.apply` both read the person's own library, derive real
items, and resolve to workers. **R-148 is CLOSED**, in the shape its condition
named: the memberships an apply collects are written, in a session opened after
the apply loop's has closed. **Main's highest residual is now R-244**, and every
number below R-235 in this file's older text predates that.

**Two things the drive found that reading did not.** The first draft applied and
then wrote memberships, and against a library whose tree had not been cut over the
ledger came back holding every entry while the database held no membership row at
all, so the next run found nothing outstanding and the gap was permanent. The
recoverable write goes first now. The second is R-148's hazard wearing a new
shape: `write_tree_membership` SURFACES a row it cannot place rather than raising,
and the caller marked it applied anyway.

**THE APPLY'S WRITE PATH IS REACHABLE ONLY FROM TESTS, which is R-235.** Nothing
in `src` calls `tree_registry.record_cutover`, and `write_tree_membership` refuses
a tree that is not database native with a root the library has. So on any real
library `crate adopt apply` refuses per entry, marks nothing, and stays resumable
for the day a cutover verb exists. `crate adopt scan` has no such wall and runs
end to end.

**Thirteen queued verbs still have no worker**, which is R-203 minus the five now
bound. The board has eight Ready and one of them is U29, which is still attended
and still not an agent's to take.


## Before U55

**Last session 2026-09-01.** U46 landed on `relay/64`, taken from the board as
issue #64 rather than from the unit sequence: it is a residual somebody decided to
act on, which is what moves a residual onto the board. **The pending register is
still EMPTY.**

**U46 CLOSED R-198 AND DID NOT CLOSE R-183.** `cratekit.core.jobs.drive` now has
one caller in `src`, `cratekit.cli.handlers.run_job`, and `crate master` runs a
queued item from `pending` to `done` through shipped code. R-183 asks that EVERY
long running verb's engine have a caller, and one binding does not meet that: of
the registry's twenty landed `long_running` entries, one is bound, `job.resume` is
exempt by role, and eighteen are `R-203`. `crate job list` and `crate job show`
now say which. R-204 records why the acquisition binding, and the first caller
obligation that travels with it, was not this unit's. R-205 through R-209 are the
resume path no test sees in one piece, the staging directory a successful master
leaves behind, and three findings the review reasoned out but did not drive.
Main's highest residual was R-209 at that point, and is R-244 now.

**The population to reason about is the REGISTRY, not the resume branches.** An
`ast` walk finds seventeen `if ctx.args.job` branches in fifteen modules, and that
is a different set: `sync/cli.py` carries one branch serving three handler keys and
`delete.review` is a landed queued entry with no branch at all. The first draft of
U46's plan sized its exemption list from the branches and was wrong by three.

**Before U46, board audit was exit 0 with 45 units, 44 done, 1 READY, 0 blocked**,
and the one that is Ready is the one you must not take.

**THE CUTOVER BACKLOG IS EMPTY AND THE CUTOVER IS MECHANICALLY POSSIBLE.** U45
cleared Feature Inventory row 31, the last owed row without a landed verb.
`tests/test_cutover_parity.py` flipped its headline assertion on that merge:
`test_the_cutover_is_not_yet_possible_and_says_why` is gone and
`test_the_cutover_is_mechanically_possible_and_says_what_is_left` stands in its
place, asserting the emptiness beside the two populations it is a statement
about so that a broken derivation cannot read as completion.

**THAT CHANGES NOTHING ABOUT WHO DOES U29.** Issue 29 is the only unit left and
it is attended, Phillip's to perform against the live library one workflow at a
time, which an agent cannot touch by standing constraint. METHOD's do-not-touch
section says so and the reason does not expire. **`board.py next` will say "Take
#29" and you must not.**

**There is no takeable unit left on this board.** Every other issue is closed.
That sentence was true on 2026-09-01 and is not now: U51 through U58 were created
after it and seven of them are open.
If you are starting a session and want work, it is either U29 with Phillip
driving, one of the residuals somebody decides to act on, or the parked
conformance branch once Phillip unparks it.

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

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

**DO NOT VERIFY MAIN BY ITS TIP SUBJECT.** This line used to name a subject and
a subject is wrong the next time anybody commits. What actually answers "is main
what this file describes": `git status -sb` shows no ahead or behind count,
`git status --porcelain` is empty, the suite matches the number below, and
`board.py audit` exits 0. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Forty four of forty five units are done, plus U46 off the residual ledger.**
The last measured suite was **6483 passed and 1 skipped**. **Main's highest
residual is R-209.** Append only.

## What the last session did

U45 built `crate backup run`, the shell over the backup engine U35 landed, and
it is the last of the four shells the U40 handoff found missing. Feature
Inventory row 31 now reads as covered.

**THE SHELL IS THE SMALL HALF. THE AGE IS THE UNIT.** A destructive write
session consults the backup age before it lets anything through, so a backup
shell that runs and does not put the fact where the session looks leaves the
product refusing destructive work immediately after the person took a backup.

**THE ENGINE ALREADY PUBLISHES IT, so this shell never writes it.**
`run_backup` calls `backup_facts.record` per portion and only on success. What
the shell owns is READING IT BACK: `published_ages` re-opens the fact file and
reports what a session would now see, through `backup_facts.ages`, which is the
function `core.session._shown_ages` calls. Deriving it from the outcome instead
would be a second copy of the engine's publish rule living in a different file
from the rule it copies, and the drift runs in the expensive direction, a report
saying a portion is backed up over a file that says never-recorded. **Do not
"simplify" that into a derivation while fixing anything.**

**FIRST CALLER.** `git grep -n run_backup -- src` returned the definition, the
`__all__` entry and a comment before this call was written, so U45 owns the
engine's unreviewed failure paths under
`docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`.
`run_backup` reads its return codes, so the engine half of the U27 defect is not
present. The SHELL half is refused explicitly: the report comes from
`outcome_payload` and the fact file, and `plan_payload` is called nowhere.

**A DEFECT FOUND WHILE WRITING IT AND FIXED HERE.** `cause.refuse` defaults an
absent remedy to the exit code's class default, which for every backup refusal
is `run-doctor`, while the reservation table holds `install-binary` for
`rclone-missing` and `run-setup` for `remote-not-configured`.
`session/restore_cli._refused` already reads that table for the same exception
type, and its own mutation table had measured that dropping it kills zero tests.
The first draft of this shell reproduced it one file over, which is METHOD's
implied fifth pattern running forwards. `_engine_refusal` reads the table.

**A FIXTURE THAT NAMED THE WRONG MECHANISM.** `no_rclone` emptied `PATH` and set
the per-binary override, and read as though the two worked together.
`binaries.find` returns None for a set-but-broken override BEFORE it consults
PATH, and consults the fallback directories AFTER it, so the override alone
decides it and PATH alone would have found the real rclone at
`/opt/homebrew/bin/rclone` on this machine. The fixture now asserts
`binaries.find("rclone") is None` rather than assuming it.

**THE TABLES.** Read `docs/mutation/u45-round-1.md` and its round two companion.
Round one was 43 rows against a green baseline of 6437 with the null control at
zero: **36 killed, 5 zero, 2 collect error**. Every guard the round was written
around held, including the engine's publish path from both sides and the row for
the reserved-remediation fix above, which matters because a fix nothing would
notice losing is a fix that comes back.

Four of the five zeros were user facing and round two closed each with one test:
the refusal MESSAGE (nothing read what the refusal told anybody, only its slug),
the reported age NUMBER (asserted where the session reads it back, never on the
verb's own report), the `--job` resume branch (never driven), and
`BackupOutcome.ok`. The fifth, `H4`, is maintainer facing and gets a line rather
than a composite. The two collect error rows are the registry ones and report no
death count, because the mutation is refused at import before a test runs; they
are not kills.

**`E5` IS THE ONE TO READ, because it could not be closed where it was found.**
`refusal_for` raises whenever a portion failed, which is exactly the condition
making `ok` false, so no report this shell can emit ever carries `ok: false`. The
property was driven on the ENGINE's return value instead, where it is reachable,
and the field being unfalsifiable in the report is filed as R-202.

**THE VERIFICATION GAP, STATED AGAIN.** Both tables are the AUTHOR'S. No
independent verifier ran. Every zero reads as "the author could not kill it", and
METHOD's measured gaps between an author's table and an independent one were 10
against 17, 39 against 49, and 49 against 83.

## What is left

**Only U29, and it is not an agent's.** See the top of this file.

**The residual ledger.** 209 numbers, 208 entries, none of them queued. R-198 is
CLOSED: `cratekit.cli.handlers.run_job` calls `jobs.drive` and `crate master` runs
a queued item to done. **R-203 inherits its consequence for the other eighteen
queued verbs**, and `crate job show` now reports which of them have no worker.
U46's own residuals are R-203 through R-209. U45's own two are R-200, a failed
archive prune that reaches no report at all, and R-201, `core/session.py`
discarding the `grant-path-access` remedy that `backup_facts` raises for a
permission and that `doctor` and the new shell both carry through.

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
  R-209.**
- **The pending register is empty.** `tests/test_pending_units.py` now carries a
  test that says so out loud, because an emptily parametrized countdown is
  SKIPPED by pytest and a silent skip is the exact hazard that file warns about.
  Re-opening any countdown re-arms the machinery with no edit.
- **CI does not run the suite and never will on Linux.** A step in the workflow
  must be able to pass. See METHOD.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. Pass `--repo-root` and
  `--out-dir` when driving a worktree from the main checkout's script. **Do not
  edit `tests/` while it runs**: it snapshots and restores the src file it
  mutates and nothing protects the suite, so an edit mid-batch measures some rows
  against one version of the tests and some against another.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `origin/main`'s own tree in a scratch worktree. A count that moved by
  the right amount is not a measurement of what moved.
- **Do not touch** U30's board state, U20, R-9, A1, A2, or `.worktrees/conformance`.
