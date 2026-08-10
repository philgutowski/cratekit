# Restart: Cratekit parallel wave

**Last session 2026-08-10 evening.** It merged U34, U24 and U38, merged the
mutation driver, and named the defect class that produced four blockers.

## Do this first

1. **`docs/METHOD.md`.** The operating instruction and the only file you need
   before working: the merge bar, the workspace rules, the mutation table
   method, the driver rules, the four defect patterns, the battery, the merge
   constraints and the cost rules.
2. **`docs/wave-state-2026-08-10-evening.md`** for what happened last and what
   to do next.
3. `CLAUDE.md` is the session contract.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git log --oneline -1                        # 63e11da
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # 4410 passed, 14 skipped
    .venv/bin/python scripts/board.py audit     # exit 0

**Four units have now cleared the merge bar: U32, U34, U24 and U38.**

## The branches, all clean, all pushed, none merged

| unit | tip | round | state |
|---|---|---|---|
| u12 | `fc73b82` | 6 | never verified. Needs a 25 run timing measurement. |
| u16 | `3262bc8` | 7 | never verified. **Its blocker U24 has merged, so it is next in line.** |
| u23 | `6f8db39` | 8 | never verified. Needs a mounted FAT image. |
| u27 | `44ced7e` | 8 | never verified. Needs a read only volume image. Merges WITHOUT a closing trailer. |
| u32 | `cf333dd` | 7 | already merged; the branch was never deleted. |
| conformance | `897ef12` | parked | its `write/metadata.py:195` defect is live on main. |
| fixtures | no commits | | empty worktree with its own venv, ready for the harness build. |

## What to do next, in order

1. **Build the hardware fixture harness.** Approved 2026-08-10 and not built. One
   reusable set: a repeat count timing runner reporting a pass rate, a FAT image
   created and mounted with hdiutil and torn down, and a real read only volume.
   It unblocks U12, U23 and U27, deferred four sessions. **Calibrate the timing
   fixture on a quiet machine**, not while other agents are running.
2. **U16**, ready now that U24 has merged.
3. `docs/mutation-rows.md` still documents the hand rolled driver and disagrees
   with METHOD. Retire it or point it at `scripts/mutate.py`.

## Standing decisions

- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. GitHub issue
  titles carry the number in their text, which the renumber silently repointed.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. 2 tool calls against 26
  on five rows, and it runs a null control that invalidates a bad batch.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **U24 and U27 merge WITHOUT closing trailers**, and U24's issue is
  deliberately open because the register still owes it a module.
- **Do not touch** U30's board state, U20, U29, A1, A2.
- **Two or three units per session.** Do not relaunch a seven agent wave.

## Four things that will bite you

**Scan the whole pushed RANGE for closing keywords, not the merge commit.**
GitHub reads every commit in a push. U24's issue closed twice on prose that
existed to warn against it. Never write a closing keyword next to an issue
number, even to quote one; backticks do not defuse it. Run the scan as a GATE
that stops the push, not as a line printed beside it.

**A unit's issue number does NOT reliably match its unit number.** CLAUDE.md says
it does. It holds for U24, U32 and U34 and it does not for U38, whose unit issue
is 51 while issue 38 is the residual R-1. A trailer written on that assumption
closed the wrong issue on 2026-08-10. **Look the number up before writing any
trailer:**

    gh issue list --repo philgutowski/cratekit --state all --limit 200 \
      --json number,title --jq '.[]|select(.title|test("^U38:"))|"#\(.number) \(.title)"'

**Every agent gets its own worktree, its own venv and its own scratch directory
named for its unit.** Never symlink a venv. Build venvs with
`/opt/homebrew/bin/python3.12`; the default `python3` is 3.14 and the project
refuses it.

**Never let git restore a file mid measurement, by driver or by hand.** Snapshot
and rewrite text, and verify against `git show HEAD:<path>`.

**Reconcile collected counts by identifier under one collation.** `comm` needs
`LC_ALL=C` on both sides; mixing Python's sort with the shell's invents
differences that are not there.

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP 400`.
Push one branch at a time. Still no pull requests.
