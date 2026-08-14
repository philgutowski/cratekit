# Restart: Cratekit parallel wave

**Last session 2026-08-14, the second that day.** It corrected R-80's recorded
mechanism, which was wrong in three separate documents, narrowed that finding
from a whole module to one function, and **merged U12**. It filed R-102, R-115
and twelve incoming residuals. **Eight units have now cleared the merge bar.**

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

    git log --oneline -1                        # subject below, and pushed
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # 5652 passed, 13 skipped, 5665 collected
    .venv/bin/python scripts/board.py audit     # exit 0

Main's tip is the commit subject `Merge U12: memory derived worker sizing`.
**No hash is written here on purpose.** This file is itself part of the commit it
would be naming, so every correction to the hash changes the hash, and the two
sessions that tried it left a stale identifier behind. Check the subject and
`git status -sb` for the ahead or behind count instead.

**Eight units have cleared the merge bar: U32, U34, U24, U38, U30, U16, U23 and
U12.**

## The branches

| branch | tip | state |
|---|---|---|
| `unit/u27-setup-wizard-and-doctor` | `46e04ae` | Still blocked by R-80, but R-80 is now ONE FUNCTION rather than the whole probe. The probe was split per intent so its flags are readable at the call site, verified on a real merge: the guard went from reporting `_probe` to reporting `_probe_writable`. The write behaviour is now pinned by a test that bites. Branch battery green: 3435 passed, 14 skipped, 3449 collected. Merges WITHOUT a closing trailer. |
| `merge/u27-attempt-2026-08-14` | `01eb6da` | **DO NOT MERGE.** The resolved U27 merge, kept so its work is not paid for twice. **Red on THREE guards, not one**, measured 2026-08-14: R-80, plus that branch's own un-re-pinned kebab literal population and a fixture the `grant-path-access` reservation moved. The other two are re-pin work, not a second collision. See R-80. |
| `fix/conformance-3-and-soft-delete-reader` | `897ef12` | parked. Its `write/metadata.py:195` defect is live on main. |

All are pushed. The u23 branch and worktree are gone, deleted in both places.

## What to do next, in order

1. **U27 has ONE question left and it is small.** The probe was split per intent
   on 2026-08-14, verified on a real merge, and the guard now reports
   `_probe_writable` alone instead of the whole `_probe`. The remaining question
   is whether that one function keeps its write capable handle. **Read R-80
   first**; it carries the six driven scenarios comparing the handle against the
   metadata alternative, which agreed on all six, the one divergence class that
   was NOT driven (a network mounted volume), and a reframing that weakens the
   objection: the probe only ever runs for a driver error that already
   established a write was refused, so it is explaining a refusal rather than
   predicting one. Attack that reframing first. The behaviour is now pinned by
   `test_the_write_probe_classifies_every_way_a_write_is_refused`, so any
   replacement has something to fail against. Do not widen `_os_open_reads`; it
   is correct, and do not relocate the probe, which is R-102.
2. **R-115, CI has been red on `main` for at least ten consecutive runs** and
   cannot go green, because the workflow runs Linux against proofs that require
   macOS and deliberately fail rather than skip. It is not a regression and
   nothing is broken. It needs a decision about what CI is for, and METHOD should
   then say so, since it currently rests everything on three local commands and
   never mentions CI at all.
3. `docs/METHOD.md` is over 265 lines against the 80 it was written to be and
   still wants a trim pass.

## Standing decisions

- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. **Main's highest is
  now R-115.**
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

## Eight things that will bite you

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

**A FINDING'S MECHANISM HAS TO BE DRIVEN, NOT ONLY ITS EXISTENCE.** R-80's
mechanism was written from reading a thirty line helper, by three readers
including an independent verifier, and the first two accounts were wrong in
different ways. The helper answers in under two seconds when asked directly.
Before recording WHY a guard fires, run it and ask it. The same applies to a
guard's offered remedies: R-80's first closing condition was called the honest
answer by two documents and, when driven, turns every structural guard green
while changing nothing.

**Do not hand roll a driver for a row that feels too small for
`scripts/mutate.py`.** One batch of four rows this session went through a shell
function that never passed its argument to `python3 -c`. No mutation applied, and
all four reported the previous row's result. It was caught only because a
traceback printed above each identical result line. Four rows that would
otherwise have read as a clean measurement.

## The remote

Every branch is on origin. Merging means deleting it in both places:

    git worktree remove .worktrees/uNN
    git branch -d unit/uNN-...
    git push origin --delete unit/uNN-...

**`git push origin --all` fails on this connection** with `RPC failed; HTTP 400`.
Push one ref at a time. Still no pull requests.
