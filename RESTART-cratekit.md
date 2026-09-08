# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-07, U52 on `relay/70`, taken from the board as issue
#70 and run as relay task 70.** The branch's eleven commits from 2026-09-02
were built under the old method and interrupted by a timeout. This session
merged `main` into them, twenty seven commits including U55 and U56, resolved
five conflicts, and continued the unit from where it stopped rather than
starting over. **The pending register is still EMPTY**, `tests/_pending.py`
holds zero entries and `tests/test_pending_units.py` carries a test that says
so out loud.

**THE LABEL VERBS RUN, AND NO LABEL WORKFLOW CAN RUN.** Both halves are true at
once and confusing one for the other is the fastest way to misread this branch.
`crate sync labels` and `crate label import` derive real item ids from the
favourite label registry, queue them, and drive each item through one worker,
`cratekit.label.cli.handle`, bound under both keys in
`src/cratekit/cli/handlers.py`. `crate label harvest` was rebuilt and no longer
raises `label-playlist-unreadable` on every call over a provider it never
contacted. What none of the three can do is reach a provider: every one of them
resolves through `src/cratekit/label/catalogue.py`, whose `bound()` returns a
constant `False` and whose `resolve` raises `credential-missing` or
`label-catalogue-unbound`. **No implementation of the `Catalogue` protocol exists
anywhere in `src`.** So a queued label item ends FAILED with a named cause
instead of sitting pending for ever, and both queueing verbs warn at enqueue
while the warning is still useful. That is smaller than a working sweep and it
is the honest version of it. **R-258 is the whole remaining distance, and it has
no board issue yet.**

**THE INCOMING RESIDUALS WERE RENUMBERED AT THE MERGE.** The branch filed them
as R-235 to R-242 against a main whose highest was R-234. Main carried its
highest to R-256 through U55 and U56, so the eight took R-257 to R-264, and the
two amendments that cited them by number, in R-137 and R-139, were repointed.
Main's numbers did not move. `docs/plans/2026-09-02-1257-feat-label-workers-plan.md`
still says R-235 in its body and carries a parenthesis saying why. U52 also
CLOSED R-140 and amended R-135, R-137, R-138, R-139 and R-203 without closing
any of them.

**R-203 IS DOWN TO NINE.** It was written at eighteen queued verbs with no
worker. U50 and U51 took it to fifteen, U52 took two more on its branch, and
U55 and U56 took four on main, so the merged tree holds nine. **The title still
says eighteen deliberately.** Nothing in the repository derives from that prose:
`tests/test_handlers.py` derives the population from `registry.ENTRIES` and
fails the day a queued verb is in neither handler table. The nine are
`acquire.download`, `analyze.restamp`, `analyze.run`, `delete.review`,
`intake.playlist`, `intake.set`, `rebuild`, `route.resort` and `sync.all`.
**`sync.all` is one of them and binding `sync.labels` did not change that**,
because `src/cratekit/sync/cli.py` queues under `ctx.entry.handler_key`, which
is `sync.all`.

**THAT HAS NOT CHANGED ABOUT WHO DOES U29.** Issue 29 is attended, Phillip's to
perform against the live library one workflow at a time, which an agent cannot
touch by standing constraint. METHOD's do-not-touch section says so and the
reason does not expire. **`board.py next` will say "Take #29" and you must not.**

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

The last measured suite on `main` before this merge was **6780 passed and 1
skipped**. The last measured suite on `relay/70`, on the committed merged tree,
is recorded in the head commit's body rather than here, because this file is in
that commit. **Main's highest residual is R-264 once this branch merges**, no
duplicate headings, no heading deleted. Append only, and gaps are fine.

**The board: 59 units, 52 done, U52 in review, 6 ready, 0 blocked.**

## Read this before the next mutation pass

**`scripts/mutate.py` can exit 0 with its last mutant still on disk.** It did on
2026-09-07, leaving `src/cratekit/cli/handlers.py` with the `tag.retag` handler
binding deleted. The tree was clean before the run and the driver was the last
writer. The next act after a pass is the battery and a merge, so this ships
silently. A green suite does not say which tree it was green on.

**The mitigation costs one command. Run `git status --porcelain` after every
`scripts/mutate.py` return, before the battery and before trusting any row.**
Restore with `git show HEAD:<path> > <path>`, never `git checkout`. R-256 and
`docs/solutions/workflow-issues/a-mutation-driver-can-exit-clean-and-leave-a-mutant.md`
carry it. One field misleads: the sidecar's `head_verified` records that HEAD
verification was REQUESTED, not that it passed.

## What is open

| issue | unit | state |
|---|---|---|
| #70 | U52, the label workers | In review on `relay/70`, the relay runner owns the merge |
| #71 | U53, routing and rebuild workers | Ready |
| #72 | U54, the acquisition worker | Ready |
| #75 | U57, the recognition identifier | Ready |
| #76 | U58, the analysis workers | Ready |
| #77 | U59, land the conformance branch | Ready |
| #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended.

**Next is `#76`, U58**, per METHOD's serialized order, once U52 is merged.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it. METHOD's serialized order is
   what picks the work, not the ranking.
3. Grep `docs/solutions/` for the module you are about to touch.

## What U52 is, beyond the call site

U52 is wider than a call site, on purpose. METHOD's merge bar makes a finding
whose input a branch makes REACHABLE that branch's to answer, and binding these
two handlers made four recorded findings reachable at once.

**THE SEAM CAME FIRST, and it is named `catalogue` rather than `provider`.**
`cratekit.acquire.provider_session` already owns the word provider for the
credential and `crate doctor` already reports a `credential.provider` check; one
symbol meaning two things in two modules is on METHOD's list of what a green
suite cannot see. The protocol has exactly four members because there are exactly
four call sites, and **the failure contract is part of the type**: `artist_for`
and `playlist_for` RAISE and never return `None`, because `LabelSource.list_recent`
skipped a missing artist with a bare `continue`, so a returned `None` would have
become a sweep that offered nothing and reported that it looked. Three slugs
joined `src/cratekit/core/cause.py`: `label-catalogue-unbound`,
`label-registry-empty` and `label-sweep-incomplete`.

**THE INCREMENT STOPPED CLAIMING AN ACQUISITION IT DID NOT MAKE.**
`cratekit.sync.run.Source` gained an `acquires` attribute, `LabelSource` declares
it `False`, and `increment` returns before the intake append, the artifact
registration and the watermark advance when it is false. One return rather than
three guards, deliberately: those three writes are three statements of one claim,
and a fourth writer added later lands below that return where an offering source
cannot reach it. **Do not "simplify" that into three guards.** This closed R-140
and opened R-263, because the labels watermark can no longer advance and
`crate doctor` still reads its absence as "never ran".

**AN UNREADABLE LISTING NOW RAISES.** `sweep._crawl_or_refuse` turns an artist
exposing none of the listing methods, and any exception out of the crawl, into
`run.LookupFailure`, which `increment` converts to `sync-source-lookups-failed`.
Two of R-135's three producers close there. **The third must NOT be closed.**
`listing.paginate` treats a `None` first answer as exhaustion, and an EMPTY first
page from a method that exists is not a producer at all: that is a genuinely
exhausted crawl and it has to keep reporting empty, or every quiet label becomes
an error and R-135 has been traded for its mirror image.

**A SWEEP THAT READ RELEASES AND CONFIRMED NONE REFUSES.** `LabelSource` carries
the dropped population and `handle` raises `label-sweep-incomplete` when the
increment reports empty and releases were read and all discarded. Keyed on the
dropped set and never on an empty candidate list, so an all tombstoned label and
an exhausted crawl keep succeeding.

**HARVEST BECAME A COMMAND THAT CAN SUCCEED.** It lists through
`listing.playlist_tracks`, offers verified names, and emits `review_set/1`. An
empty playlist is a success reported as `NO_OP`, so a playlist with nothing in it
stays distinguishable from one that could not be read.
`label-playlist-unreadable` is raised in exactly one place now, and only after a
bound provider was asked and failed.

**ONE RESUME OWNER FOR BOTH VERBS, and `outbound/shell.resume` was NOT reused.**
That function calls `ctx.gate.require` unconditionally and digests the fixed
outbound triple of playlist, export and tracks; neither label verb declares a
gate or carries those keys. Two fragments were lifted rather than the function:
the itemless job refusal and the closed cause re-raise, and the second sits
OUTSIDE the `is_open` branch. `master`'s resume branch is missing that second
fragment and must not be copied.

**THE WORKER READS ITS LABEL FROM THE ITEM, never from the payload.** A handler
that reads its subject from the payload makes every item of a multi item job do
the same work. That was the first defect U46's end to end drive surfaced and it
is now written into three modules' docstrings.

## What U52 left behind, beyond the code

Eight residuals, R-257 through R-264. Three are worth knowing before touching
labels again:

- **R-258.** No catalogue adapter ships. Every label verb resolves to a constant
  refusal and the test substitution carries R-226's limit: the in process
  callers pick up a replaced `resolve`, and the child a resume spawns inherits
  nothing.
- **R-259 and R-137.** The labels path applies no ownership filtering at all,
  because nothing on it produces an owned identity set. R-137's reorder would
  change nothing until this one closes.
- **R-263.** A successful labels sweep still reads as "never ran" in
  `crate doctor`, because R-140's fix stopped the watermark and the reader was
  not told.

## The branches

| branch | state |
|---|---|
| `relay/70` | U52, in review, the relay runner merges it |
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
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. U52 and U56 each ran forty by explicit decision under the old method;
  neither is a precedent to follow silently. Do not edit `tests/` while it runs.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
