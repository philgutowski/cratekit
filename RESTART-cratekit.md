# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-09, U54 finished on `u54/finish`, taken from the board
as issue #72.** The unit's CODE was already on `main`: relay task 72 built it
on 2026-09-08 and the runner merged and pushed it, then a session limit cut
that session down mid `/code-review`, so relay recorded the task as
`partial_landing` and `main` carried a unit nobody had reviewed. Relay tasks
71, 75 and 77 never ran at all, two seconds each and `no_envelope`, because the
limit was still in force. This session did what task 72 still owed: the review
over the merged range, five of its eight findings fixed with a test each, three
recorded, the mutation table measured, its one zero chased to its cause and
killed, eleven residuals filed and one learning. **The pending register is
still EMPTY.**

**`crate acquire download` ACTUALLY DOWNLOADS.** The shell reads the list at
the queue through `match_cli.read_list`, the one list reader the product has,
and queues one item per track keyed by the provider's own track identifier,
which is the only thing the adapter contract can be asked for. A pasted
tracklist and a list from another service are refused at the queue rather than
queued as items nothing can acquire. `handle` in `src/cratekit/acquire/cli.py`
is the worker: it builds `AdapterSettings` from the FROZEN configuration with
the download directory redirected to a per item staging directory, constructs
the adapter through `acquire.build` by the frozen name, and drives
`download.acquire_paced` with one request. It is the first caller of both.

**THE MARKER IS DECIDED BY THE FILE, NOT BY THE OFFER.** `requires_lossy_marker`
comes from what the provider SAID it was about to send, and under a permissive
policy `vendored.landed_file` returns without probing anything, so trusting the
claim committed an unmarked lossy file whenever the provider promised lossless
and landed AAC. That is the single state the audit verb exists to find.
`lossy_landing` asks the file, and the requirement is the claim OR the probe.
A file the probe cannot read is still committed unmarked, which is R-292 and
deliberate: refusing it is a decision about what the permissive policy means
and it is Phillip's, not a session's.

**A DEAD CREDENTIAL PARKS THE RUN. A BROKEN TOOL DOES NOT.** The worker builds
an adapter and authenticates inside every item, so failing the item let the
driver claim the next one and log in again: measured at five constructions for
a five item job, which is two hundred failed logins for a two hundred track
list, and repeated failed logins are what triggers the lockout the acquisition
docstring calls unrecoverable. `AUTH_FAILED` therefore raises `jobs.Parked`.
`ADAPTER_BROKEN` still fails its item, because the crash may be about that
track and the brief asks for a resume that redoes only it. The asymmetry has
its own test so it cannot be flattened by accident.

**`jobs.Parked` is the engine's new seam.** A per item worker that learns the
provider refused the CLIENT raises it; `drive` catches it BEFORE the item
boundary, releases the claimed item back to pending, and records the job
BLOCKED with the cause. Released and not failed, because `retry` re-arms failed
items only for a terminal job and a blocked job is open.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

The last measured suite on this branch was **6990 passed and 1 skipped**, on the record
commit; the commits before it were the fixes and the table, and the record
touched documents only. **Main's highest residual is R-299 once this branch
merges**, no duplicate headings, no heading deleted. Append only, and gaps are
fine.

**The board before this merge: 61 units, 54 done, 7 ready, 0 blocked, and
`board.py audit` exits 1.** Five drift items, all of them the interrupted relay
run's leavings: #70 and #76 are Done on the tracker and still In review on the
board, #72 is In review while its issue is open, and #78 and #79, U60 and U61,
are on the tracker and not on the board. `sync` repairs all five and there is
no longer a unit under review for it to disturb, so run it.

## Read this before touching acquisition again

**THE ITEM IS THE PROVIDER'S TRACK IDENTIFIER.** Not a filename, not a
recording. `TrackSource.offer` and `fetch` take a key and there is no search,
so a list that does not carry provider identifiers cannot be acquired at all,
and that is refused at the QUEUE rather than discovered by a worker.

**THE LIST REACHES THE READER AS TYPED.** `read_list` refuses a pasted web
address by matching a scheme at the front of the string, and
`expanduser().absolute()` turns `https://host/x` into a relative path under the
working directory that the guard cannot match. The freeze is still absolute,
because the child a resume spawns inherits the resuming process's directory;
it just happens AFTER the read.

**A FALLBACK MUST NOT FILL AN ABSENCE SOMEBODY MEANT.** The learning this unit
paid for, filed at
`docs/solutions/workflow-issues/a-remedy-fallback-overwrites-an-absence-somebody-meant.md`.
A permanently unavailable track carries no remedy on purpose, and the fallback
told that person to relax the product's central promise over a delisted track.
The branch the fallback was written for was DEAD, because a policy refusal
always carries its own remedy. Ask which outcomes can actually reach a branch,
and read the producer's validator to find out.

**A TEST NAMED FOR AN INVARIANT MUST ASSERT IT.** Twice in one unit.
`..._carries_no_remedy` asserted the reason and the retryable flag and not the
remedy, and the partial file test passed with the staging clear reverted
because the FAKE always wrote its landing and overwrote the stale bytes itself.
A fake's convenience standing in for coverage is what a mutation table is for:
that row read zero across 6991 tests, and killed once the fake was taught to
skip a landing already there, which is what the wrapped tool does.

## What U54 left behind, beyond the code

Eleven residuals, R-289 through R-299, and R-296 amends R-248 with a seventh
copy of the resume tail. Four are worth knowing before touching acquisition or
tagging again:

- **R-289.** The acquisition staging tree is a dotfile, and
  `tagging.tag.audio_files` walks with `rglob` and no dot filter, so
  `crate tag folder <download_staging>` queues partial downloads and files the
  landing check refused. Driven. R-288 records the same walker's asymmetry from
  the analysis side.
- **R-290.** A blocked job reports outcome `ok` and exits 0, in EVERY queued
  verb. `ctx.envelope` has no cause parameter and `envelope_problems` requires
  a top level cause exactly when the outcome is not a success, so reporting it
  honestly changes the envelope contract for all of them at once.
- **R-294 and R-295.** R-204 is discharged by HALF. `acquire_paced` and
  `acquire_concurrently` have their first caller; `dispatch_invocation` and
  `adapter_names` still have none. `acquire_paced` catches two exceptions and
  anything else out of the session scope reaches the item boundary as
  `internal-error`, reachability UNMEASURED rather than absent.
- **R-297.** One request per call, so a configured `concurrency` above one is
  inert on this path and nothing says so.

## What U58 left behind, still current

R-283 through R-288, and the rename intent rule below. **The resume reads a
rename intent, never the folder**: the finalize writes `rename-intent.json`
into the item's staging directory immediately before the rename, and
`_finalized_twin` reads that and nothing else. It applies to every remaining
R-203 worker, all of which move files. The learning is at
`docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`.

**The heavy stack stays behind the extra, and so does numpy.** Every librosa,
torch and model touch is a lazy import inside a function, because
`cli.jobs.argv_for` imports the verb module by name to build a resume line.

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 5 | #75 | U57, the recognition identifier | Ready, and NEXT |
| 6 | #71 | U53, routing and rebuild, the last R-203 worker | Ready |
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | Ready, last on purpose |
| | #78 | U60, the deletion pass | Ready, added to the board by this session's sync |
| | #79 | U61, `crate sync all` composes the source increments | Ready, same |
| | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Where they fall is Phillip's to say, so a session does not take them.

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended.

**Next is `#75`, U57**, per METHOD's serialized order, which is the fifth line
and the first whose issue is still open.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it. METHOD's serialized order is
   what picks the work, not the ranking.
3. Grep `docs/solutions/` for the module you are about to touch. A worker that
   moves files reads the rename intent entry before it binds; a worker that
   translates another layer's optional field reads the remedy fallback entry.

## The branches

| branch | state |
|---|---|
| `u54/finish` | U54's review, fixes, table and record; delete after the merge |
| `u58/pre-relay-76` | U58's first five commits, fully contained in `main`; delete |
| `u52/pre-relay-70` | U52's pre relay branch, merged through `relay/70`; delete |
| `relay/72` | U54's build, fully contained in `main`; delete |
| `fix/conformance-3-and-soft-delete-reader` | U59's input, in `.worktrees/conformance`, far behind main. DO NOT TOUCH |

## When a relay run is cut off mid unit

It has happened twice now, both times on a session limit, and the shape is
worth recognising. The runner merges and pushes the branch, then its own verify
refuses to call the task landed, `halt_class: partial_landing`, and the tracker
issue stays open. So `main` carries a unit whose review, table and record never
happened, and the board is right to still call the unit unfinished. The state
lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`, `halt_class`,
`halt_message`, `findings`, and `transcript_path` for what the session was
doing when it stopped. Finish it on a branch off `main` and close the issue with
a trailer from there; do not re-run the unit from the board as though nothing
had landed.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
