# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-07, the method change.** The compound engineering plugin
and Relay are out of the loop. `docs/METHOD.md` was rewritten around a native
pipeline one session runs alone, `CLAUDE.md` says so, and the wave era
narrative moved to `docs/history/`. `docs/HANDOFF.md` stayed at its path
because a test pins it, and its header says it is history. The parked
conformance branch is unparked and is U59, issue #77. Board drift on U55, whose
issue read In Progress after its merge, was synced.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

The last measured suite on `main` was **6678 passed and 1 skipped**, in a worktree with its
own venv. **Main's highest residual is R-244**, 243 entries, no duplicate
headings. Append only.

**The board: 59 units, 51 done, 8 ready, 0 blocked, audit exit 0.**

## What is open

| issue | unit | state |
|---|---|---|
| #70 | U52, the label workers | In Progress on `relay/70`, 11 commits ahead of main, tree clean at last look |
| #74 | U56, the catalogue searcher and tag workers | In Progress on `relay/74`, 7 commits ahead of main, PLUS UNCOMMITTED WORK, see below |
| #71 | U53, routing and rebuild workers | Ready |
| #72 | U54, the acquisition worker | Ready |
| #75 | U57, the recognition identifier | Ready |
| #76 | U58, the analysis workers | Ready |
| #77 | U59, land the conformance branch | Ready |
| #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended.

**`relay/74` holds uncommitted U56 work in the main checkout:** 316 added lines
in `docs/residual-findings.md`, a one line change in
`src/cratekit/tagging/cli.py`, and two untracked mutation tables under
`docs/mutation/`. The session that takes #74 commits that first, before reading
anything else, because it is the only copy.

**Both in flight branches were built under the old method and both rewrite this
file.** On merge, take the incoming branch's `RESTART-cratekit.md`, then rewrite
it against the merged tree. Take `main`'s `docs/METHOD.md` and `CLAUDE.md`
without exception. A branch that references `/ce-work` or an independent
verifier in its record is describing how it was built, not how the next one is.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it.
3. Grep `docs/solutions/` for the module you are about to touch.

## The branches

| branch | state |
|---|---|
| `relay/70` | U52, in flight |
| `relay/74` | U56, in flight with uncommitted work, checked out in the main checkout |
| `fix/conformance-3-and-soft-delete-reader` | U59's input, in `.worktrees/conformance`, 377 commits behind main |

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2.
