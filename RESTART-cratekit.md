# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-10, U57 finished on `relay/75`, taken from the board as
issue #75 and run as relay task 75.** The task built the whole unit and reached
its record before the FABLE usage limit ended it mid step, so five commits and a
twenty five row mutation table were already in place and the working tree held
the residuals and the learning, uncommitted. This session committed that tree,
wrote what the record still owed, ran the battery and merged. **The pending
register is still EMPTY.**

**THE RECOGNITION IDENTIFIER IS REAL, AND IT HAS SPENT NOTHING.**
`intake/acrcloud.py` is the implementation behind the seam `recognize.identify`
has declared since U37. Credentials come through `core.secrets` at CALL time,
the carver and the transport are injected with shipped defaults, and the call
count is known from the recording's duration BEFORE the first chunk is carved,
checked against a per run cap and the month's ledger. A spend refusal is its own
cause and never a miss, which is the distinction the whole entry turns on.
`ffprobe` joins the recognition gate, because measuring the recording is what
makes the spend knowable in advance. No live key has been bound and no paid call
has been made, so the response table has met no real answer: that is R-300, and
R-132's attended half is now exactly what is left of R-132.

**BOTH INTAKE VERBS EXECUTE.** `intake.set` identifies the recording at the
queue and queues one item per identified track with the tracks frozen in the
payload; a mix URL is refused honestly because this build fetches none, and a
set nobody recognised is a NO_OP that says what it cost. `intake.playlist`
lists through the catalogue seam and freezes the provider rows. Both resume
branches reconcile, refuse an empty job, and drive it. The shared worker
resolves one frozen track against the frozen library, offers a needs review row
to the review queue, and commits a per item report saying owned, offered or
missing. **It never acquires**, and the registry says it writes, which is R-302.

**FOUR QUEUED VERBS HAVE NO WORKER.** `delete.review`, `rebuild`,
`route.resort` and `sync.all`, with `job.resume` exempt by role. Fifteen are
bound. R-203 carries the correction and its title stays at eighteen on purpose,
because the title names what was true when the entry was written.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 0

The last measured suite was **7109 passed and 1 skipped**, on the record commit; the commits
before it were the build, the fix round and the table, and the record touched
documents only. **Main's highest residual is R-311 once this branch merges**, no
duplicate headings, no heading deleted. Append only, and gaps are fine.

## Read this before touching intake or recognition again

**THE SPEND IS KNOWN BEFORE THE FIRST CALL, NOT COUNTED AFTER IT.** The duration
gives the chunk count, which gives the call count, which is checked against the
cap and the ledger before anything is carved. A design that counted as it went
would discover the overspend after paying for it.

**A SPEND REFUSAL IS NOT A MISS.** `intake-recognition-spend-bound` is its own
cause. Folding it into "nothing recognised" would tell somebody their set has no
identifiable tracks when what actually happened is that the run declined to pay.

**IDENTIFYING AT THE QUEUE IS UN-RESUMABLE SPEND**, which is R-304, and the
ledger counts attempts the service never received up to the streak stop, which
is R-306. Both are the cost of the queue side identification this unit chose,
recorded rather than hidden.

**A SEAM THAT RETURNS ONLY ROWS READS ABSENCE AS EVIDENCE OF ABSENCE.** The
unit's learning, filed at
`docs/solutions/workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md`.
Counts known one layer down are gone by the time the caller sees the rows, so
the caller cannot tell "asked and got nothing" from "never asked".

## What U57 left behind, beyond the code

Twelve residuals, R-300 through R-311, corrections to R-203 and R-132, and one
learning. Four are worth knowing before touching intake again:

- **R-300.** The ACRCloud status table is the source system's, corrected twice,
  and has met no live answer. Everything the identifier believes about the
  service's replies is inherited rather than observed.
- **R-302.** The intake worker resolves and offers; it does not acquire, and the
  registry entry says it writes.
- **R-304 and R-306.** Identification happens at the queue, so a kill between
  the spend and the queue write pays for nothing, and the ledger counts attempts
  the service never received.
- **R-308.** `core.artifacts` landed and the four feature copies are not
  migrated onto it. The pointer lines are in place; the migration is not.

## What U54 left behind, still current

Eleven residuals, R-289 through R-299. The two worth carrying: **R-289**, the
acquisition staging tree is a dotfile and `tagging.tag.audio_files` walks
dotfiles, so tagging the download root queues partial downloads; and **R-290**,
a blocked job reports outcome `ok` and exits 0 in every queued verb, which is
the envelope contract rather than any one verb's line.

**A fallback must not fill an absence somebody meant**, filed at
`docs/solutions/workflow-issues/a-remedy-fallback-overwrites-an-absence-somebody-meant.md`,
and **a test named for an invariant must assert it**. U57 found the first shape
again from the other end, which is why both entries are worth reading before
translating any seam's optional field.

## What U58 left behind, still current

**The resume reads a rename intent, never the folder.** The finalize writes
`rename-intent.json` into the item's staging directory immediately before the
rename, and `_finalized_twin` reads that and nothing else. It applies to every
remaining R-203 worker, all of which move files. Filed at
`docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`.

**The heavy stack stays behind the extra, and so does numpy.** Every librosa,
torch and model touch is a lazy import inside a function, because
`cli.jobs.argv_for` imports the verb module by name to build a resume line.

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 6 | #71 | U53, routing and rebuild, the last R-203 workers | Ready, and NEXT |
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | Ready, last on purpose |
| | #78 | U60, the deletion pass | Ready |
| | #79 | U61, `crate sync all` composes the source increments | Ready |
| | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Where they fall is Phillip's to say, so a session does not take them.

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended.

**Next is `#71`, U53**, per METHOD's serialized order.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it. METHOD's serialized order is
   what picks the work, not the ranking.
3. Grep `docs/solutions/` for the module you are about to touch. A worker that
   moves files reads the rename intent entry before it binds; a worker that
   translates another layer's optional field reads the remedy fallback entry and
   the absence-as-evidence entry, which are the same trap from two ends.

## The branches

| branch | state |
|---|---|
| `relay/75` | U57, merged by hand after the Fable limit; delete after the merge |
| `fix/conformance-3-and-soft-delete-reader` | U59's input, in `.worktrees/conformance`, far behind main. DO NOT TOUCH |

## When a relay run is cut off mid unit

It has happened three times now, all three on a usage limit, and the shape is
worth recognising. Two different limits have done it: a general session limit
on 2026-09-08, and the FABLE model limit on 2026-09-09, which the run's own
tasks were all configured to use. The endings differ:

- **The runner had already merged.** Its own verify then refuses to call the
  task landed, `halt_class: partial_landing`, and the tracker issue stays open.
  So `main` carries a unit whose review, table and record never happened, and
  the board is right to still call the unit unfinished. That was #72.
- **The runner had not merged.** The task branch holds the work and the tree is
  left dirty, `halt_class: unclean_exit`, and the run stops there whatever
  `on_halt.continue_past_task_halt` says, because a dirty tree is a fact about
  the repository rather than about one task. That was #75.

The state lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`,
`halt_class`, `halt_message`, `findings`, and `transcript_path` for what the
session was doing when it stopped. Read the task's last assistant messages to
learn which pipeline step it reached; both times the answer was precise enough
to finish the unit by hand from where it stopped. Finish it on the task's own
branch, merge, and close the issue from there. **Do not re-run the unit from the
board as though nothing had landed.**

**`verify` needs the issue named as `#N`.** After a hand landing, `relay_cli.py
verify <manifest> <task>` promotes the record only when it can find the link. It
derives one from a default branch commit naming `#N` when the record carries no
`landing_ref`; when the record already carries one, as a `partial_landing`
record does, it instead wants a tracker COMMENT naming that sha, and one comment
is the whole repair. native-relay's own `docs/solutions/` carries both halves.

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
