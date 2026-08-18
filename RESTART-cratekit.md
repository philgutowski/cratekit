# Restart: Cratekit

**Last session 2026-08-18.** Board audit exit 0. No unit was started. `board.py
next` named issue 27 as already In Progress and then named nothing ready. That
is not an empty build. Issue 27 is held open on purpose, and the three modules
it still owes are the remaining unit work.

## Do this first

1. `docs/METHOD.md`. The operating instruction: the merge bar, the workspace
   rules, the mutation table method, the driver rules, the four defect
   patterns, the battery, what CI is for, the merge constraints and the cost
   rules.
2. `CLAUDE.md` is the session contract.
3. This file for the current wave state. `docs/HANDOFF.md` is the longer
   narrative. Its pending table is a copy of `tests/_pending.py` and has
   drifted; the register is the authority.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git log --oneline -1                        # subject below, and pushed
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count written here
    .venv/bin/python scripts/board.py audit     # exit 0

Main's tip subject is `docs: refresh restart for the week wrap` on top of
`merge: U33 outbound service writes`. **No hash is written here on purpose.**
This file is itself part of the commit it would be naming. Check the subject
and `git status -sb` for the ahead or behind count instead.

**Thirty five units are done.** The three still open are issue 27 (U27), issue
28 (U28), and issue 29 (U29). U33 shipped as `cratekit.export.cli` and
`cratekit.favorites.cli`. The shared engine is `cratekit.modules.outbound`.
Live account verification is R-144. Post-merge U26 findings are R-135 through
R-143. Last residual is R-144. Append only.

## The branches

| branch | tip subject | state |
|---|---|---|
| `fix/conformance-3-and-soft-delete-reader` | five defects in the scoping and exclusion rules | parked in `.worktrees/conformance`. Its `write/metadata.py:195` defect is live on main. Do not touch the worktree or the branch. |

## What to do next, in order

**Work is picked from the board, by number.** `board.py next` will print issue
27 as already In Progress and then say nothing is ready. Do not stop. Do not
invent work from the ledger. Do not run `board.py start` on issue 27 again.

1. **Stay on issue 27. Build `cratekit.cli.reports` first.** The wizard and
   doctor have merged. The issue stays open because `tests/_pending.py` still
   owes `cratekit.session.restore_cli`, `cratekit.cli.reports`, and
   `cratekit.adopt.apply_cli`. A closing trailer naming that issue would make
   `board.py audit` exit 2. Landing all three is what unblocks issue 28, which
   unblocks issue 29. Reports is first because it is the only one of the three
   not tangled with the parked conformance branch or a destructive restore.
   Branch by hand. Leave the issue open until all three land or are re-owned.
2. **Do not take issue 28 or issue 29 while they are blocked.** 28 waits on 27.
   29 waits on 28.
3. **Do not reopen issues 26, 24, or 25.** Do not re-own the three modules onto
   new issues unless Phillip asks. Moving them would make 28 Ready without
   landing the verbs.
4. **#54, R-102**, the allowlist audit being one hop deep. A real design change
   rather than a unit. Not the queue.

`docs/METHOD.md` is over 300 lines against the 80 it was written to be and still
wants a trim pass. Do not trim "What CI is for".

## Standing decisions

- **The board is the BUILD, `docs/residual-findings.md` is the LEDGER.** Units
  and attended chores are issues; a residual earns one only if somebody decides
  to act on it. **Do not backfill.**
- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. **Main's highest
  is R-144.**
- **A renumber is NOT finished inside `docs/residual-findings.md`.** Repoint
  only the lines the branch ADDED.
- **CI does not run the suite and never will on Linux.** A step in the workflow
  must be able to pass. A check that cannot belongs in the battery. See METHOD.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. Pass `--repo-root` and
  `--out-dir` when driving a worktree from the main checkout's script.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **U24 merges WITHOUT a closing trailer.** U27's code has merged; its issue
  stays open. Every other unit gets a trailer, and check which issue it is
  BEFORE writing the merge commit.
- **Do not touch** U30's board state, U29's board state, A1, A2, or
  `.worktrees/conformance`.
- **Two or three units per session.**

## Eight things that will bite you

**Scan the whole pushed RANGE for closing keywords, not the merge commit**, and
run it as a GATE that stops the push. Never write a closing keyword next to an
issue number, even to quote one; backticks do not defuse it.

**A unit's issue number does NOT reliably match its unit number.** U38 is #51.
Look it up before writing any trailer.

**A COUNTDOWN DISCHARGE IS THREE EDITS IN ONE COMMIT**, the entry, the mirrored
key in `EXPECTED_PENDING`, and the `@requires` decorator on every guard the key
gated. Run `grep -rn 'requires("<key>")' tests/` before deleting anything, and
run the newly armed guard on purpose.

**A GUARD WRITTEN TO FAIL ON A DATE WILL FAIL ON THAT DATE.** Answer it rather
than delete it: derive what it forbids from the registry so the property
outlives the verb.

**Every agent gets its own worktree, its own venv and its own scratch directory.
None of that isolates the PROCESS TABLE.** Kill by PID. Build venvs with
`/opt/homebrew/bin/python3.12`. Never symlink a venv.

**Reconcile the collected count by IDENTIFIER, under `LC_ALL=C`, against the
UNION of both sides, and check the cwd of the shell you count from.** A total
moving by the right amount is not a reconciliation.

**A FINDING'S MECHANISM HAS TO BE DRIVEN, NOT ONLY ITS EXISTENCE**, and so does
its CAUSE. Before blaming the platform for a red CI run, clone at depth 1 and
run it here.

**Re-pinning a population means naming what moved, not matching a count.**

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git worktree remove .worktrees/uNN
    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP
400`. Push one ref at a time. Still no pull requests.
