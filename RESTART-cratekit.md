# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-07, U56 merged.** The catalogue searcher landed and both
tagging verbs execute, which takes two of R-203's queued verbs off that list and
leaves eleven. The branch's uncommitted work turned out to be one third
authored and two thirds mutation driver residue: the change sitting in
`src/cratekit/tagging/cli.py` was a live mutant from a pass interrupted on
2026-09-03, not a fix, and it was restored from HEAD rather than committed. The
pass was then resumed and finished, forty rows, and it left a mutant on disk
after exiting zero. That is R-256 and it is the thing to know before running the
next one.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

The last measured suite on `main` was **6780 passed and 1 skipped**, measured on
the merge commit itself in this checkout, not carried over from the branch.
**Main's highest residual is R-256**, 255 entries, no duplicate headings, no
heading deleted. Append only, and gaps are fine.

**The board: 59 units, 52 done, 7 ready, 0 blocked, audit exit 0.**

## Read this before the next mutation pass

**`scripts/mutate.py` can exit 0 with its last mutant still on disk.** It did on
2026-09-07, leaving `src/cratekit/cli/handlers.py` with the `tag.retag` handler
binding deleted, which is the row `R40` mutates and the exact thing U56 existed
to land. The tree was clean before the run and the driver was the last writer.

The next act after a pass is the battery and a merge, so this ships silently. A
green suite does not say which tree it was green on.

**The mitigation costs one command. Run `git status --porcelain` after every
`scripts/mutate.py` return, before the battery and before trusting any row.**
Restore with `git show HEAD:<path> > <path>`, never `git checkout`. It did not
reproduce, and no mechanism is offered, so the check is the whole defence for
now. R-256 and
`docs/solutions/workflow-issues/a-mutation-driver-can-exit-clean-and-leave-a-mutant.md`
carry it. One field misleads: the sidecar's `head_verified` records that HEAD
verification was REQUESTED, not that it passed.

## What is open

| issue | unit | state |
|---|---|---|
| #70 | U52, the label workers | In Progress on `relay/70`, 11 commits ahead of main, never pushed |
| #71 | U53, routing and rebuild workers | Ready |
| #72 | U54, the acquisition worker | Ready |
| #75 | U57, the recognition identifier | Ready |
| #76 | U58, the analysis workers | Ready |
| #77 | U59, land the conformance branch | Ready |
| #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended.

**Next is `#70`, U52**, per METHOD's serialized order. That branch was built
under the old method and rewrites this file. On merge, take the incoming
branch's `RESTART-cratekit.md` and rewrite it against the merged tree, and take
`main`'s `docs/METHOD.md` and `CLAUDE.md` without exception. A branch that
references `/ce-work` or an independent verifier in its record is describing how
it was built, not how the next one is.

**`relay/70` has never been pushed**, exactly as `relay/74` had not been. Its
eleven commits exist only on this machine, so treat it the way the order treated
U56: it is the only copy.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it. METHOD's serialized order is
   what picks the work, not the ranking.
3. Grep `docs/solutions/` for the module you are about to touch.

## The branches

| branch | state |
|---|---|
| `relay/70` | U52, in flight, local only |
| `fix/conformance-3-and-soft-delete-reader` | U59's input, in `.worktrees/conformance`, far behind main |

## What U56 left behind, beyond the code

Twelve residuals, R-245 through R-256. Three are worth knowing before touching
tagging again:

- **R-245.** No catalogue page shape here has been verified against a live site.
  Every parser was read from DJ_tools and every test feeds synthetic page text
  through the injected seam. A wholly broken parser and a working one produce the
  same green suite. A live call is attended by standing constraint, so an agent
  can prepare for it and cannot perform it.
- **R-246 and R-185.** `tag.retag` corrects the files and nothing writes the
  library row, while the registry declares it writes `db_metadata`. R-185 was
  driven rather than argued this time, and the measurement found the resumable
  ledger its closing condition asks for: `jobs.drive` already commits a per item
  artifact carrying the path, the previous genre and the written one. The
  deferred half needs a caller, not a new register.
- **R-255.** `tag.retag` raises its confirm gate before deriving its selection,
  so a person running it over a folder with nothing to correct still has to
  record a decision before being told there was nothing to do. Reversed into on
  purpose, because conformance 3 holds every declared gate to firing.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. U56 ran forty by explicit decision and logged the overrun with its cost;
  that was a decision taken with Phillip, not a precedent to follow silently.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2.
