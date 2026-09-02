# Restart: Cratekit

**Last session 2026-09-02.** U52 landed on `relay/70`, taken from the board as
issue #70. **The pending register is still EMPTY**, `tests/_pending.py` holds
zero entries and `tests/test_pending_units.py` carries a test that says so out
loud, because an emptily parametrized countdown is SKIPPED by pytest and a silent
skip is the exact hazard that file warns about.

**THE LABEL VERBS RUN, AND NO LABEL WORKFLOW CAN RUN.** Both halves are true at
once and confusing one for the other is the fastest way to misread this branch.
`crate sync labels` and `crate label import` now derive real item ids from the
favourite label registry, queue them, and drive each item through one worker,
`cratekit.label.cli.handle`, bound under both keys in
`src/cratekit/cli/handlers.py`. `crate label harvest` was rebuilt and no longer
raises `label-playlist-unreadable` on every call over a provider it never
contacted. What none of the three can do is reach a provider: every one of them
resolves through `src/cratekit/label/catalogue.py`, whose `bound()` returns a
constant `False` and whose `resolve` raises `credential-missing` or
`label-catalogue-unbound`. **No implementation of the `Catalogue` protocol exists
anywhere in `src`**, measured as six references, all of them a definition, an
export line, an import or an annotation. So a queued label item ends FAILED with
a named cause instead of sitting pending for ever, and both queueing verbs warn
at enqueue while the warning is still useful. That is smaller than a working
sweep and it is the honest version of it. **R-236 is the whole remaining
distance, and it has no board issue yet.**

**MAIN'S HIGHEST RESIDUAL MOVED, TWICE SINCE THIS FILE LAST SAID SO.** It was
R-209 after U46. Main carried it to **R-234** through U47, U50 and U51, and U52
takes it to **R-240**. Append only: main's numbers never move, and an incoming
branch's residuals take fresh numbers above main's highest. U52 added R-235
through R-240, CLOSED R-140 and amended four entries without closing any of them,
R-135, R-137, R-138 and R-139. R-139's amendment follows R-204's "still open"
shape on purpose: its closing condition is met in the code and is not met for a
person, and the second half is what the entry is for.

**R-203 IS DOWN TO THIRTEEN.** It was written at eighteen queued verbs with no
worker, corrected to fifteen on 2026-09-02 after U50 and U51, and binding the two
label keys takes it to thirteen. **The title still says eighteen deliberately.**
Nothing in the repository derives from that prose: `tests/test_handlers.py`
derives the population from `registry.ENTRIES` and fails the day a queued verb is
in neither handler table, which is why the count in the ledger is a record rather
than a repair. The thirteen are `acquire.download`, `adopt.apply`, `adopt.scan`,
`analyze.restamp`, `analyze.run`, `delete.review`, `intake.playlist`,
`intake.set`, `rebuild`, `route.resort`, `sync.all`, `tag.folder` and
`tag.retag`. **`sync.all` is one of them and binding `sync.labels` did not change
that**, because `src/cratekit/sync/cli.py` queues under `ctx.entry.handler_key`,
which is `sync.all`.

**The population to reason about is the REGISTRY, not the resume branches.** An
`ast` walk finds seventeen `if ctx.args.job` branches in fifteen modules, and that
is a different set: `sync/cli.py` carries one branch serving three handler keys and
`delete.review` is a landed queued entry with no branch at all. The first draft of
U46's plan sized its exemption list from the branches and was wrong by three.

**Board before the U52 merge: exit 0, 58 units, 50 done, 8 ready, 0 blocked**,
and the highest ranked Ready is the one you must not take.

**THAT HAS NOT CHANGED ABOUT WHO DOES U29.** Issue 29 is attended, Phillip's to
perform against the live library one workflow at a time, which an agent cannot
touch by standing constraint. METHOD's do-not-touch section says so and the reason
does not expire. **`board.py next` will say "Take #29" and you must not.**

**There ARE takeable units now, and that is new.** Six worker binding units sit
Ready behind U52 and none of them is attended: #71 routing and rebuild, #72
acquisition, #73 the collection reader and the adopt verbs, #74 the catalogue
searcher and the tag verbs, #75 recognition and the intake verbs, #76 the
analysis workers. Each names its own R-203 slice. `board.py next` ranks them all
at zero released units, so pick by what the product needs rather than by the
ranking.

## Do this first

1. `docs/METHOD.md`. The operating instruction: the merge bar, the workspace
   rules, the mutation table method, the driver rules, the four defect patterns,
   the battery, what CI is for, the merge constraints and the cost rules. **Read
   its "Do not touch" section before touching issue 29**, because the board will
   tell you to take it.
2. `CLAUDE.md` is the session contract.
3. This file for the current wave state. `docs/HANDOFF.md` is the longer
   narrative and its "State" section has been stale since U27; trust this file
   and `board.py` over it.

Older `wave-state-*.md` files are history. Read one for the reasoning behind a
rule, never to find out how to work.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

**DO NOT VERIFY MAIN BY ITS TIP SUBJECT.** This line used to name a subject and
a subject is wrong the next time anybody commits. What actually answers "is main
what this file describes": `git status -sb` shows no ahead or behind count,
`git status --porcelain` is empty, the suite matches the number below, and
`board.py audit` exits 0. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

The last measured suite, on `relay/70` with all six U52 commits in, was **6685
passed and 1 skipped**, run in the foreground from the main checkout's own
`.venv`. **Main's highest residual is R-240 once this branch merges.** Append
only.

## What the last session did

U52 is six commits and it is wider than a call site, on purpose. METHOD's merge
bar makes a finding whose input a branch makes REACHABLE that branch's to answer,
and binding these two handlers made four recorded findings reachable at once.

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
cannot reach it. **Do not "simplify" that into three guards.** This closed R-140.

**AN UNREADABLE LISTING NOW RAISES.** `sweep._crawl_or_refuse` turns an artist
exposing none of the listing methods, and any exception out of the crawl, into
`run.LookupFailure`, which `increment` converts to `sync-source-lookups-failed`.
Two of R-135's three producers close there. **The third must NOT be closed.**
`listing.paginate` treats a `None` first answer as exhaustion, and an EMPTY first
page from a method that exists is not a producer at all: that is a genuinely
exhausted crawl and it has to keep reporting empty, or every quiet label becomes
an error and R-135 has been traded for its mirror image.

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

## What is left

**U29, and it is not an agent's.** See the top of this file.

**Six worker binding units, #71 through #76.** Each is a slice of R-203 and each
inherits whatever its engine's unreviewed failure paths hold, under
`docs/solutions/workflow-issues/adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md`.
R-204 is the worked example of what that costs: U46 declined the acquisition
binding because three critical residuals sat behind it.

**The adapters.** R-226 is the outbound seam with no `RemoteAccount` and R-236 is
the label seam with no `Catalogue`. They are separate seams on purpose, sharing a
credential and not a capability. Both need an attended session against a live
account, which is why R-144 has stayed open since 2026-08-17.

**The residual ledger.** 240 numbers, 239 entries, and it is a REGISTER of what
was accepted rather than a queue. Do not backfill it onto the board.

**The parked conformance branch**, with its `write/metadata.py:195` defect live
on main. Out of scope until Phillip says otherwise. R-186 records what U40
changed about its reachability.

## The branches

| branch | tip subject | state |
|---|---|---|
| `fix/conformance-3-and-soft-delete-reader` | five defects in the scoping and exclusion rules | parked in `.worktrees/conformance`. Its `write/metadata.py:195` defect is live on main. Do not touch the worktree or the branch. |

## Standing decisions

- **The board is the BUILD, `docs/residual-findings.md` is the LEDGER.** Units
  and attended chores are issues; a residual earns one only if somebody decides
  to act on it. **Do not backfill.**
- **Residual numbers are APPEND ONLY.** Main's numbers never move; an incoming
  branch's residuals take fresh numbers above main's highest. **Main's highest is
  R-240.**
- **The pending register is empty**, and the test that says so is what keeps an
  empty countdown from reading as a passing one. Re-opening any countdown re-arms
  the machinery with no edit.
- **CI does not run the suite and never will on Linux.** A step in the workflow
  must be able to pass. See METHOD.
- **Use `scripts/mutate.py`.** Do not hand roll a driver. Pass `--repo-root` and
  `--out-dir` when driving a worktree from the main checkout's script. **Do not
  edit `tests/` while it runs**: it snapshots and restores the src file it
  mutates and nothing protects the suite, so an edit mid-batch measures some rows
  against one version of the tests and some against another.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `origin/main`'s own tree in a scratch worktree. A count that moved by
  the right amount is not a measurement of what moved.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent. `docs/METHOD.md` records this firing twice.
- **Do not touch** U30's board state, U20, R-9, A1, A2, or `.worktrees/conformance`.
