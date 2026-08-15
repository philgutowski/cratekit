# Restart: Cratekit parallel wave

**Last session 2026-08-15.** It ran the three item batch the previous session
queued: amended the stale coordination note and dated R-57 and R-111 (#56,
closed), **decided R-80 and merged U27** (#27, stays open by design), and decided
what CI is for (#55, R-115, closed). **Nine units have cleared the merge bar**,
and CI on `main` is green for the first time in the visible history.

## Do this first

1. **`docs/METHOD.md`.** The operating instruction and the only file you need
   before working: the merge bar, the workspace rules, the mutation table
   method, the driver rules, the four defect patterns, the battery, what CI is
   for, the merge constraints and the cost rules.
2. `CLAUDE.md` is the session contract.
3. `docs/wave-state-2026-08-14.md` for the previous session's narrative. This
   session wrote no wave state file; its record is the three merge commits on
   `main` and the residuals they filed.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git log --oneline -1                        # subject below, and pushed
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # 5926 passed, 11 skipped, 5937 collected
    .venv/bin/python scripts/board.py audit     # exit 0

Main's tip is the commit subject `merge: R-115, CI proves packaging and
portability rather than nothing`. **No hash is written here on purpose.** This
file is itself part of the commit it would be naming, so every correction to
the hash changes the hash. Check the subject and `git status -sb` for the ahead
or behind count instead.

**Nine units have cleared the merge bar: U32, U34, U24, U38, U30, U16, U23, U12
and U27.**

## The branches

| branch | tip | state |
|---|---|---|
| `fix/conformance-3-and-soft-delete-reader` | `897ef12` | parked. Its `write/metadata.py:195` defect is live on main. Its `SoftDeleteNames` still matches by dotted tail, read 2026-08-15 and not driven. |

The u27 branch and worktree are gone, deleted in both places, and so is
`merge/u27-attempt-2026-08-14`: the U27 merge landed as its own resolution, so
the preserved attempt described a merge that happened differently and held no
unmerged work.

## What to do next, in order

**Work is picked from the board, by number.** `board.py next` names #22 as the
one that releases the most. Two things sit outside the ranking:

1. **#27 stays open and In Progress by design.** U27's code has merged. Its
   issue stays open because it still owes three modules in `tests/_pending.py`:
   `cratekit.session.restore_cli`, `cratekit.cli.reports` and
   `cratekit.adopt.apply_cli`. A closing trailer naming its issue would make
   `board.py audit` exit 2 permanently. Leave it until those land or are
   re-owned.
2. **#54, R-102**, the allowlist audit being one hop deep. A real design change
   rather than a fix. R-80's resolution removed the one admitted writer, so the
   audit's one hop now finds nothing, which makes this less urgent and not less
   real.

`docs/METHOD.md` is over 300 lines against the 80 it was written to be and still
wants a trim pass. Do not trim "What CI is for": it is a week old.

## Standing decisions

- **The board is the BUILD, `docs/residual-findings.md` is the LEDGER.** Units and
  attended chores are issues; a residual earns one only if somebody decides to act
  on it. **Do not backfill.**
- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. **Main's highest is
  now R-128.**
- **A renumber is NOT finished inside `docs/residual-findings.md`.** Repoint only
  the lines the branch ADDED. Each incoming entry's NUMBERING paragraph is
  addressed to the merge and goes at the merge, replaced by one header.
- **CI does not run the suite and never will on Linux.** A step in the workflow
  must be able to pass. A check that cannot belongs in the battery. See METHOD.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. Pass `--repo-root` and
  `--out-dir` when driving a worktree from the main checkout's script.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
  This session applied that rule to a REPLACEMENT as well: the two rows where the
  new probe disagreed with the old were over an input the one producer cannot
  produce, and that was driven rather than argued.
- **U24 merges WITHOUT a closing trailer.** U27 has merged. Every other unit gets
  one, and check which it is BEFORE writing the merge commit.
- **Do not touch** U30's board state, U20, U29, A1, A2.
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
run the newly armed guard on purpose. The U27 merge did this for
`cratekit.cli.doctor` and the two guards behind it had never executed once.

**A GUARD WRITTEN TO FAIL ON A DATE WILL FAIL ON THAT DATE.** One test asserted
doctor was planned so that the day doctor landed it would say it had gone stale.
Answer it rather than delete it: derive what it forbids from the registry so the
property outlives the verb.

**Every agent gets its own worktree, its own venv and its own scratch directory.
None of that isolates the PROCESS TABLE.** Kill by PID. Build venvs with
`/opt/homebrew/bin/python3.12`. Never symlink a venv.

**Reconcile the collected count by IDENTIFIER, under `LC_ALL=C`, against the
UNION of both sides, and check the cwd of the shell you count from.** This
session's first reconciliation ran with the shell sitting inside a worktree and
counted 3452 against a union of 5966. A total moving by the right amount is not
a reconciliation.

**A FINDING'S MECHANISM HAS TO BE DRIVEN, NOT ONLY ITS EXISTENCE**, and so does
its CAUSE. R-115 named five causes, all platform, from reading a run list. Five of
the failures were a shallow checkout, driven on macOS in ninety seconds. Before
blaming the platform for a red CI run, clone at depth 1 and run it here.

**Re-pinning a population means naming what moved, not matching a count.** Ask
git whether each member existed before, or difference the two sets in a scratch
worktree. A count that moved by one says a member joined and does not say which,
and a member leaving while another joined reads identically.

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git worktree remove .worktrees/uNN
    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP 400`.
Push one ref at a time. Still no pull requests.
