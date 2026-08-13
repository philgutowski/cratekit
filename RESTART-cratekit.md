# Restart: Cratekit parallel wave

**Last session 2026-08-13.** It built the hardware fixture harness, merged it,
merged U16, and retired the stale mutation procedure. Six units have now cleared
the merge bar.

## Do this first

1. **`docs/METHOD.md`.** The operating instruction and the only file you need
   before working: the merge bar, the workspace rules, the mutation table
   method, the driver rules, the four defect patterns, the battery, the merge
   constraints and the cost rules.
2. **`docs/wave-state-2026-08-13.md`** for what happened last and what to do
   next.
3. `CLAUDE.md` is the session contract.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git log --oneline -1                        # 258a1cd
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # 4763 passed, 13 skipped
    .venv/bin/python scripts/board.py audit     # exit 0

**Six units have now cleared the merge bar: U32, U34, U24, U38, U30 and U16.**

## The branches, all clean, all pushed, none merged

| unit | tip | round | state |
|---|---|---|---|
| u12 | `fc73b82` | 6 | never verified. Needs a 25 run timing measurement. **The harness now provides it.** |
| u23 | `6f8db39` | 8 | never verified. Needs a mounted FAT image. **The harness now provides it.** |
| u27 | `44ced7e` | 8 | never verified. Needs a read only volume image. **The harness now provides it.** Merges WITHOUT a closing trailer. |
| conformance | `897ef12` | parked | its `write/metadata.py:195` defect is live on main. |

The u16, u32 and fixtures branches and worktrees are gone, deleted in both
places after merging.

## The hardware harness, built 2026-08-13 and the reason the next three units can move

`tests/_hardware.py`, with `scripts/calibrate_timing.py` and its committed
baseline. Three fixtures, all merged and green:

- `time_repeated(...)` returns a `TimingTable` carrying the repeat count, every
  duration and a pass rate. It cannot produce the one number shape METHOD
  forbids, and it refuses a record whose count disagrees with its own durations.
- `fat_volume()` is a real mounted FAT32 image, torn down on every exit path.
- `read_only_volume(populate)` populates a volume while writable, then remounts
  it read only, and VERIFIES what it serves against what `populate` wrote.

Express a timing threshold as `threshold_seconds(multiplier)`, a multiple of the
calibrated median, never an absolute number. **The calibration is bound to the
machine that wrote it and refuses to load elsewhere**, so a new machine runs
`scripts/calibrate_timing.py` first, on a quiet machine. Current baseline:
median 0.0680s over 25 runs, spread 0.098.

Three things it already knows so you do not pay for them again: FAT32 refuses to
format under about 33 MB and hdiutil reports that as a permissions error; the
macOS FAT driver ALLOWS symlinks, so ask `filesystem_kind` rather than probing
behavior; and the volume tests FAIL rather than skip when hdiutil is missing,
because a skipped hardware proof reads as a passing one.

## What to do next, in order

1. **U27**, then **U23**, then **U12**, each with the harness. All three have
   been deferred five sessions and the thing blocking them is now built.
   U27 merges WITHOUT a closing trailer.
2. `docs/METHOD.md` is 265 lines against the 80 it was written to be. It wants a
   trim pass.

## Standing decisions

- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. GitHub issue
  titles carry the number in their text, which a renumber silently repointed.
  **Main's highest is now R-78.**
- **Use `scripts/mutate.py`.** Do not hand roll a driver. `docs/mutation-rows.md`
  is now an ARCHIVE of historical rounds and says so; the method is METHOD.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **U24 and U27 merge WITHOUT closing trailers**, and U24's issue is
  deliberately open because the register still owes it a module.
- **Do not touch** U30's board state, U20, U29, A1, A2.
- **Two or three units per session.** Do not relaunch a seven agent wave.

## Five things that will bite you

**Scan the whole pushed RANGE for closing keywords, not the merge commit.**
GitHub reads every commit in a push. U24's issue closed twice on prose that
existed to warn against it. Never write a closing keyword next to an issue
number, even to quote one; backticks do not defuse it. Run the scan as a GATE
that stops the push, not as a line printed beside it.

**A unit's issue number does NOT reliably match its unit number.** CLAUDE.md says
it does. It held for U16, U24, U32 and U34 and it does not for U38, whose unit
issue is 51 while issue 38 is the residual R-1. A trailer written on that
assumption closed the wrong issue on 2026-08-10. **Look the number up before
writing any trailer:**

    gh issue list --repo philgutowski/cratekit --state all --limit 200 \
      --json number,title --jq '.[]|select(.title|test("^U38:"))|"#\(.number) \(.title)"'

**A COUNTDOWN ENTRY IS DISCHARGED IN TWO HALVES AND ONE HALF ALONE IS WORSE
THAN NEITHER.** Learned on the U16 merge. When a unit lands a module that
`tests/_pending.py` was waiting for, delete the register entry AND remove the
`@requires(...)` decorator from the guard in the same edit. Deleting only the
entry makes `requires` raise `KeyError` at import, which takes the whole test
file out of COLLECTION: 330 tests stop existing and the run still looks green.
Deleting only the decorator leaves the meta test red. Check both with
`grep -rn 'requires("<key>")' tests/` before you delete anything.

**Every agent gets its own worktree, its own venv and its own scratch directory
named for its unit.** Never symlink a venv. Build venvs with
`/opt/homebrew/bin/python3.12`; the default `python3` is 3.14 and the project
refuses it.

**Never let git restore a file mid measurement, by driver or by hand.** Snapshot
and rewrite text, and verify against `git show HEAD:<path>`.

**Reconcile collected counts by identifier under one collation.** `comm` needs
`LC_ALL=C` on both sides; mixing Python's sort with the shell's invents
differences that are not there. Reconcile against the UNION of both sides, not
against either one: the U16 merge moved the total from 4445 up to 4776 while 24
identifiers went missing underneath it, and a total only check would have read
that rise as health.

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP 400`.
Push one branch at a time. Still no pull requests.
