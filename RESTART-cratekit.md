# Restart: Cratekit parallel wave

**Last session 2026-08-10.** It changed the merge bar, cut the method out of the
narrative record, verified U24 round 9, and landed fix rounds on U34 and U38.
Nothing merged.

## Do this first

1. **`docs/METHOD.md`.** This is the operating instruction and it is the only
   file you need to read before working. Eighty lines, fixed size. It carries
   the merge bar, the workspace rules, the mutation table method, the driver
   rules, the four defect patterns, the battery and the merge constraints.
2. **`docs/wave-state-2026-08-10.md`** for what happened last session and what
   to do next.
3. `CLAUDE.md` is the session contract.

The older `wave-state-2026-08-04.md` and `wave-state-2026-08-09.md` are history.
Read one when you need the reasoning behind a rule. **Do not read them to find
out how to work.** Every rule they carry is already in METHOD.md.

## The bar changed on 2026-08-10, and this is the headline

**A finding blocks a merge only if it was driven end to end and has a named user
facing cost.** Everything else is a residual. Behind that sits a hard cap of two
more fix rounds per unit, after which the unit merges and open findings become
residuals.

Twenty consecutive blocking verdicts measured the problem: the previous bar,
that the verifier found nothing, is not a reachable state, because a mutation
table over a suite this size always finds a zero death row. This reverses the
2026-08-09 decision on evidence gathered since.

## Main, verify before trusting it

    git log --oneline -1                        # 24b58d1
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # 3422 passed, 17 skipped
    .venv/bin/python scripts/board.py audit     # exit 0

**U32 is still the only unit ever to clear the merge bar.**

## The branches, all clean, all pushed, none merged

| unit | tip | round | state |
|---|---|---|---|
| u12 | `fc73b82` | 6 | never verified. Needs a 25 run timing measurement. |
| u16 | `3262bc8` | 7 | never verified. Merges AFTER U24. |
| u23 | `6f8db39` | 8 | never verified. Needs a mounted FAT image. |
| u24 | `b5a4e86` | 9 | verified BLOCKING, 4 findings. Needs round 10. |
| u27 | `44ced7e` | 8 | never verified. Needs a read only volume image. |
| u34 | `1a7cdf7` | 10 | fixed, UNVERIFIED. Light pass next. |
| u38 | `c2fda57` | 8 | fixed, UNVERIFIED. Light pass next. |
| conformance | `897ef12` | parked | its `write/metadata.py:195` defect is live on main. |

## What to do next, in order

1. **U24 round 10.** Record the identity scheme version in the store at write
   time, so history reconstruction is a lookup and not a recomputation. Round 9
   froze the composer and not what the composer calls, which is why this is the
   fourth consecutive "correct fix, hole still open" on that branch. Stores
   written by unmerged branch tips are OUT of scope; nothing has shipped.
2. **Verify U34 round 10 and U38 round 8**, light pass, scoped per METHOD.md.
   Both are author written, and an author's table is a draft.
3. **Apply the severity floor to those verdicts.** On the evidence so far both
   units are close to merging.
4. **U12, U23 and U27 need hardware fixtures.** Building them once as a reusable
   harness is now cheaper than deferring them a fourth session.

## Standing decisions

- **U24 and U27 merge WITHOUT closing trailers.** Scan every merge body first;
  the command is in METHOD.md. GitHub matches a closing keyword anywhere in a
  body, not only in trailer position.
- **Residuals renumber sequentially at each merge**, decided 2026-08-10. Safe
  now: zero numeric `R-NN` citations remain in `src`, `tests` or `scripts` on any
  branch.
- **Do not touch** U30's board state, U20, U29, R-9, A1, A2.
- **Two or three units per session.** Do not relaunch a seven agent wave.

## Two things that will bite you

**Every agent gets its own worktree, its own venv and its own scratch directory
named for its unit.** Three concurrent agents ran clean on 2026-08-10, the first
time since the failure was named. Do not regress it.

**Never let git restore a file mid measurement, by driver OR by hand.**
`git checkout` and `git checkout-index` silently discard uncommitted edits. Third
instance on 2026-08-10, by hand that time. Snapshot and rewrite file text, and
verify restores against `git show HEAD:<path>`.

**Never pass `-q` to pytest**, including a collection run. `pyproject.toml` sets
it and a second one becomes `-qq`, which suppresses the summary line.

## The remote

Every branch is on origin. Merging a unit now means deleting it in both places:

    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP 400`.
Push one branch at a time. Still no pull requests.
