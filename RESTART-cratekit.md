# Restart: Cratekit parallel wave

**Last session 2026-08-14.** It corrected the countdown instruction text, found
and closed a flake that was making the battery a coin flip, merged U23, and
established that U27 cannot merge without a design decision. Seven units have now
cleared the merge bar.

## Do this first

1. **`docs/METHOD.md`.** The operating instruction and the only file you need
   before working: the merge bar, the workspace rules, the mutation table
   method, the driver rules, the four defect patterns, the battery, the merge
   constraints and the cost rules.
2. **`docs/wave-state-2026-08-14.md`** for what happened last and what to do
   next.
3. `CLAUDE.md` is the session contract.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git log --oneline -1                        # 6bff237
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # 5385 passed, 12 skipped
    .venv/bin/python scripts/board.py audit     # exit 0

**Seven units have cleared the merge bar: U32, U34, U24, U38, U30, U16 and U23.**

## The branches

| branch | tip | state |
|---|---|---|
| `unit/u27-setup-wizard-and-doctor` | `fb035fb` | VERIFIED MERGE and BLOCKED at the merge by R-80. Independent pass was clean: 42 rows, 25 deaths, no blocking finding. Merges WITHOUT a closing trailer. |
| `merge/u27-attempt-2026-08-14` | `01eb6da` | **DO NOT MERGE.** The resolved U27 merge, kept so its work is not paid for twice. Red on one guard. |
| `unit/u12-memory-derived-worker-sizing` | `fc73b82` | round 6, never verified. Needs a 25 run timing measurement, which the harness provides. |
| `fix/conformance-3-and-soft-delete-reader` | `897ef12` | parked. Its `write/metadata.py:195` defect is live on main. |

All are pushed. The u23 branch and worktree are gone, deleted in both places.

## What to do next, in order

1. **U27 needs a DECISION, not an ordinary fix round.** It lands `_probe` in
   `core/cause.py`, which opens a write capable handle with `os.O_RDWR`. That
   module is on the read only reports allowlist because both report modules
   import `Scope` and `refuse` from it, and the allowlist guard propagates a
   writer to its callers until the closure reaches `refuse` itself. Both remedies
   the guard offers were driven to their end and both fail. **Read R-80 first**,
   then `merge/u27-attempt-2026-08-14`. Do not widen `_os_open_reads`; it is
   correct.
2. **U12**, the last unverified unit, with
   `time_repeated(fn, repeats=25, threshold_seconds=threshold_seconds(multiplier))`.
3. `docs/METHOD.md` is over 265 lines against the 80 it was written to be and
   still wants a trim pass.

## Standing decisions

- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. **Main's highest is
  now R-101.**
- **A renumber is NOT finished inside `docs/residual-findings.md`.** A branch
  cites its own numbers in `docs/HANDOFF.md`, in its mutation tables and
  sometimes in source. Repoint only the lines that branch ADDED, because main's
  own citations of the same numbers are somebody else's stable addresses.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. `docs/mutation-rows.md`
  is an ARCHIVE; the method is METHOD.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **U24 and U27 merge WITHOUT closing trailers.** Every other unit gets one, and
  **check which it is BEFORE writing the merge commit**, not after pushing.
- **Do not touch** U30's board state, U20, U29, A1, A2.
- **Two or three units per session.** Do not relaunch a seven agent wave.

## Six things that will bite you

**Scan the whole pushed RANGE for closing keywords, not the merge commit**, and
run it as a GATE that stops the push. Never write a closing keyword next to an
issue number, even to quote one; backticks do not defuse it.

**A unit's issue number does NOT reliably match its unit number.** It held for
U16, U23, U24, U27, U32 and U34 and it does not for U38, whose unit issue is 51.
Look it up before writing any trailer:

    gh issue list --repo philgutowski/cratekit --state all --limit 200 \
      --json number,title --jq '.[]|select(.title|test("^U38:"))|"#\(.number) \(.title)"'

**A COUNTDOWN DISCHARGE IS THREE EDITS IN ONE COMMIT**, the entry, the mirrored
key in `EXPECTED_PENDING`, and the `@requires` decorator on every guard the key
gated. The instruction text now says so in all five places a person reads it, and
`docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md`
is the procedure. Run `grep -rn 'requires("<key>")' tests/` before deleting
anything, and run the newly armed guard on purpose.

**Every agent gets its own worktree, its own venv and its own scratch directory.
None of that isolates the PROCESS TABLE.** On 2026-08-14 one agent's
`pkill -f "scripts/mutate.py"` killed another agent's driver on a different
branch. Nothing was corrupted and that was luck. Kill by PID. Build venvs with
`/opt/homebrew/bin/python3.12`; the default `python3` is 3.14 and the project
refuses it. Never symlink a venv.

**Never let git restore a file mid measurement.** Snapshot and rewrite text, and
verify against `git show HEAD:<path>`.

**Reconcile collected counts BY IDENTIFIER, under `LC_ALL=C`, against the UNION
of both sides.** The U23 merge had 25 identifiers present on a side and absent
from the merge, and all 25 were renames or correct retirements. A total only
check reads that as health. Expect pinned populations in
`tests/test_reserved_causes.py` to move whenever a unit appends a cause slug:
re-measure and re-pin, never widen, and append rather than rewrite the figures
already there.

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git worktree remove .worktrees/uNN
    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP 400`.
Push one ref at a time. Still no pull requests.
