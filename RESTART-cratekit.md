# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-10, U61 on `relay/79`, taken from the board as issue #79
and run as relay task 79.** `crate sync all` is a COMPOSER now. It plans every
enabled source, asks the favourites confirm once, then queues each source through
that source's own `queue_sweep` under that source's own handler key, with one
intake run. Nothing is queued under `sync.all`, so its entry dropped
`long_running` and `argv_builder` and **R-203 CLOSED**: `HANDLERS_NOT_YET_BOUND`
holds only the `job.resume` exemption. Playlists has no worker and is reported as
not built, so a slim pass is a no-op rather than an ok.

**A COMPOSED JOB NEEDS A RUN ITS OWN VERB OWNS.** The dispatcher refuses a `--run`
whose record belongs to another verb, so the favourites job could not carry the
pass's run as its gate run. `Gates.hand_off` copies the recorded answer onto a new
run owned by `sync.favorites`. The learning is
`docs/solutions/integration-issues/a-verb-that-queues-another-verbs-job-must-hand-it-a-run-that-verb-owns.md`.

**U61 HAS NO MUTATION TABLE EITHER, and the reason is now measured.** The null
control is hardcoded to the full suite at `scripts/mutate.py:1002`, so the
driver's preflight is two full runs, about 720 seconds, whatever the rows say.
R-329 carries the correction, `docs/mutation/u61-notes.md` the sampled timing.

**The session before, 2026-09-10, U60 on `relay/78`, taken from the board as
issue #78 and run as relay task 78.** `delete.review` stopped claiming a queue. Its entry
dropped `long_running` and `argv_builder`, `delete_argv` is gone, and the verb
left `HANDLERS_NOT_YET_BOUND`, so R-149 closed in the direction it left open.
R-134 closed too, at a schema cost of zero fields: the first run's baseline rides
the gate's existing context onto the refusal as `cause.detail.shown`, which
`render_gate` prints for a person, and `review_set/1` is untouched.

**A NEW REGISTRY GUARD HOLDS THE CLASS.**
`test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues` parses every
landed long-running verb's module for an `enqueue` call, with `job.resume` exempt
by role. It failed on `main` for `delete.review` alone. Its module-wide bar is
R-328.

**U60 HAS NO MUTATION TABLE, AND THAT IS A MEASURED GAP, NOT A CLEAN ONE.**
`scripts/mutate.py` reruns a six minute full baseline on every call, and a relay
task runs every command in the foreground under a ten minute ceiling, so two
attempts ended in preflight with no row measured. The rows are committed and
ready, `docs/mutation/u60-notes.md` holds the measurements, and R-329 is the gap
with three options, all Phillip's. The learning is
`docs/solutions/workflow-issues/the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`.

**Two sessions before, 2026-09-10, R-322 closed on `relay/81`, taken from the
board as issue #81 and run as relay task 81.** The first residual issue to be worked
rather than a unit, and the first work of the ninth line in METHOD's serialized
order. It added SEVEN tests and thirteen lines of `scripts/board.py`, no new
behaviour, and it closed the audit's detector being driven by nothing.

**THE CONTRADICTION DETECTOR HAS A DRIVER NOW.** `contradictions()`,
`units_by_issue_number`'s exclusion of unlabelled unit-shaped titles, the
residual repoint half of the return, the default register read, and
`cmd_audit`'s exit codes are all driven. Both rows R-322 was built out of went
from zero to killing, re-run verbatim from U59's row file so the comparison is
two measurements of one experiment. `docs/mutation/u81-notes.md` is the reading
and it carries one correction to its own first row file.

**THE DOUBLE IS THE `gh` PAYLOAD, NOT THE GRAPH, AND THAT IS THE DECISION R-322
ASKED FOR.** A hand-built graph would type every key `build_graph` derives, so
the producer could drift and the tests would stay green. The fixture is the issue
list JSON, `build_graph` runs on it for real, and the field list is read out of
`load_issues`'s syntax tree and compared against the double's keys. The learning
is filed at
`docs/solutions/workflow-issues/a-double-belongs-at-the-producer-boundary-not-at-the-shape-it-produces.md`
and it carries two traps that cost a round here.

**The pending register is still EMPTY** and nothing in this session touched it,
so no `@requires` decorator exists anywhere.

**U59, the session before this one, built on `relay/77`.** It ran the whole
pipeline in one session: plan, the merge, the built in `/code-review`, a six
finding fix round, a twenty five row mutation table with one composite, and its
record. The merge is what kept the pending register empty: git took `main`'s
empty `PENDING` and only the branch's three-state `module_state` probe, so
nothing was re-armed.

**THE SOFT DELETE DEFECT IS OFF MAIN.** `write/metadata.resolve_genre_id` no
longer defaults the marker. A row that cannot report it refuses with
`soft-delete-marker-unreadable` at run scope rather than reading as active, and
the rule is driven through the SHIPPED reader, `crate tag retag` into
`plan_library` into `plan_genre_retag`, not only through the function's own
rows. R-186 closes.

**THE CONFORMANCE BRANCH IS LANDED AND ITS WORKTREE IS UNTOUCHED.**
`.worktrees/conformance` and `fix/conformance-3-and-soft-delete-reader` are
exactly as they were; the merge was taken on `relay/77` in the primary checkout.
**Two of its eleven commits were already on `main`**, the conformance 3 pair, so
`tests/test_cli_contract.py` is byte identical to `main` and this merge armed
three guards rather than the five the brief names. That is R-326.

**PHASE E'S AGENT HALF IS DONE.** Three verbs stopped reporting work nobody had
done. `route.inbox` applies on the confirmed branch instead of returning the
plan on both. `route.unplaced` reads the library instead of being
`_plan([], ...)`. `rebuild` and `route.resort` queue one item per governed tree
and drive them, and a library that has flipped no tree files no job at all
rather than an empty one. Both workers go through
`rebuild.rebuild_governed_tree`, which is the FIRST CALLER of `rebuild_tree`
anywhere in `src`.

**EVERY QUEUED VERB HAS A WORKER**, with `job.resume` exempt by role. Measured:
eighteen landed verbs queue and seventeen are bound. `delete.review` left the
population in U60 by ceasing to be queued, and `sync.all` left it in U61 by
queueing its work under keys that have workers. R-203 is closed with a note in
place. Its title stays at eighteen on purpose, because the title names what was
true when the entry was written.

**R-131 IS DOWN TO ITS ATTENDED HALF.** Everything in it that a session could do
is done and driven against a disposable database copy. Nothing has run on a live
tree, which is the whole of what the entry now says.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 1 on the In review card, R-265

The last measured suite was **7253 passed and 1 skipped**, taken on `relay/79` on
a committed tree. Against U60's 7235 BY TOTAL ONLY, not by identifier, which is
a gap: `tests/test_sync_all.py` arrived with twenty tests, measured by a collect
run, and the old `queue_all` test in `tests/test_incremental_sync.py` was deleted
because its claim is what this unit falsified. That is nineteen against the
eighteen moved, so one parametrised case left somewhere and was not named. **Main's highest residual is R-332 once this branch merges**, no
duplicate headings, no heading deleted, and R-203 and R-329 gained notes in place
rather than moving. Append only, and gaps are fine.

**THE AUDIT EXITS 1 NOW, NOT 2, AND THE REASON IS A BOARD WRITE NOBODY RECORDED.**
Measured on 2026-09-10 while closing R-322: issue #25 is OPEN with a state reason
of REOPENED, so `contradictions()` returns nothing and the exit 2 U59 predicted
is gone. The registry still owes U25 two modules, which is now the register
working rather than a contradiction, and R-324 and #80 stay open because whether
that is U25's answer is #80's judgement. Do not weaken the check to get a green
audit; **the detector is now driven and softening it fails tests.**

**The one thing the audit does report is R-265, and `sync` is the wrong answer to
it.** `#81 status is In review, should be Ready`. `derive_status` knows five
statuses and the field has six, so every relay card reads as drift for the whole
of its run, and the remedy the audit prints would drag the card back to Ready
mid review. Leave it. Confirmed a second time on #81.

## Read this before touching a write path again

**A GUARD THAT REFUSES AN EMPTY LIST CANNOT SEE A BARREN ONE.** The unit's
learning, filed at
`docs/solutions/integration-issues/a-guard-that-refuses-an-empty-list-cannot-see-a-barren-one.md`.
Both new writes named `root/Music` as their `analysis_roots`, which is one entry
so it passed `write_tree_membership`'s empty-list refusal, and which holds no
ANLZ file, so the beat grid watch fingerprinted nothing and would have reported
a clean session whatever happened to the grids. Every other caller in the
package names the library root. **Judge a new call site's argument against what
the existing call sites pass, not against whether the callee accepted it.**

**THE ITEMS ARE THE DECISION, NOT THE CALL SITE.** Binding a queued verb is one
line at the call site and two real decisions before it: what an item IS, and
what the per item worker does. For these two the item is a TREE, which is what
makes a partial failure recoverable rather than a single collapsed failure.

**A RESUME OWES THREE CHECKS, and the corrected shape is in `intake/cli.py`.**
Refuse a job queued for another verb, because `handlers.run_job` reads the worker
off the JOB ROW and not off the verb somebody typed. Refuse a job with no items,
because every rebuild and resort queued before U53 has none. Re-raise the job's
own cause when it did not end well, which is R-225: `drive` raises only when
EVERY item failed, so a partial failure returns normally and an unconditional OK
exits zero over half a library.

**THE RESORT IS ADDITIVE**, which is R-312. There is no database removal path in
this build, so a genre change leaves the track in its old sub as well as its new
one and the convergence check names the leftovers.

## What U61 left behind

Three residuals, two notes in place, one learning and one learning corrected.

- **R-330.** A job an older build queued under `sync.all` stays in the queue with
  no worker and reads as a defect until somebody cancels it.
- **R-331.** A handed decision carries no record that it was handed, so a run
  record alone cannot tell it from one given directly.
- **R-332.** A pass where every source refused raises the first refusal, so the
  person sees one remedy and meets the other on the next pass.
- **R-329's second option was written on a wrong reading of the driver**, and the
  learning about the ten minute ceiling said the same thing. Both are corrected.

## What U60 left behind

Two residuals and one learning.

- **R-328.** The new queueing guard accepts an `enqueue` call anywhere in a
  verb's module, so two verbs sharing a module pass on one call. Nothing
  exploits it today: every shared-module pair also shares a worker.
- **R-329.** The mutation driver cannot finish a batch inside a relay task's ten
  minute foreground ceiling. U60's twenty rows are committed and unmeasured.
  **Read the learning before an unattended session plans a table**: if the
  battery's full suite is past roughly four minutes, commit the rows, record the
  gap and land, rather than spending ceiling length calls finding out.

## What U59 left behind, beyond the code

Seven residuals, R-320 and R-321 renumbered in from the branch and R-322 through
R-326 filed by this session, plus one learning. Four are worth knowing before
touching the board tooling or a source guard again:

- **R-324.** The registry owes U25 two modules. Its issue was reopened by
  somebody between the U59 merge and 2026-09-10, so the audit no longer exits 2
  and the loud half is discharged while the substantive half is not. The section
  above carries the measurement. #80 is still the decision.
- **R-322. CLOSED on `relay/81`, and the head of this file says what it took.**
  Both zero rows kill now. What replaced it is R-327, the board's WRITE half,
  which is a harder case rather than the same one: `reconcile` reads a user-owned
  project that a repository-scoped token cannot see at all, so there is no local
  payload seam to build an honest double at.
- **R-323.** A trailer names an ISSUE and both registers name a UNIT. Twenty
  four units are mismatched today and none of them is owed a module, which is why
  this was never seen. `audit` resolves the mapping through the issue titles now.
  The network-free hook cannot, so it says that it guessed.
- **R-326.** Two of the parked branch's eleven commits were already on `main`.
  Found by reconciling the collected count BY IDENTIFIER; a total-only check
  showed a healthy rise and would have said nothing.

**A GUARD THAT GOES RED AT A MERGE HAS TWO POSSIBLE CAUSES AND ONLY ONE IS THE
GUARD.** Four went red here and all four were right about their rule and stale
about the tree. Filed at
`docs/solutions/workflow-issues/a-guard-written-against-an-old-tree-goes-red-holding-a-rule-that-is-still-right.md`.
The dangerous reading is the other one: weaken a stale guard to get green, and
the rule it was holding goes with it.

## What U53 left behind, still current

Eight residuals, R-312 through R-319, corrections to R-203 and R-131, and one
learning. Four are worth knowing before touching routing again:

- **R-312.** The resort adds and never removes, so a re-place doubles a track's
  membership until somebody takes the old one out by hand.
- **R-314.** `assert_addressable` kills ZERO tests, and so does the composite
  over the refusal inside it, measured over the full suite twice. Nothing in the
  repository produces a colliding destination set. The extraction into
  `plan_destinations` is what made that measurable; the gap predates it.
- **R-316.** Neither worker derives the vocal dimension and neither reports the
  gap the engine hands them, so a library with vocal playlists declared gets a
  clean job and an unfiled dimension.
- **R-313.** `route.unplaced` declares `writes` and `destructive` and only
  reports, so a person is told to close rekordbox for a read.

## What U57 left behind, still current

**THE RECOGNITION IDENTIFIER IS REAL AND HAS SPENT NOTHING.** The spend is known
BEFORE the first call, not counted after it, and a spend refusal is its own cause
and never a miss. Identifying at the queue is un-resumable spend, R-304, and the
ledger counts attempts the service never received, R-306. No live key is bound,
so the response table has met no real answer, which is R-300.

**A SEAM THAT RETURNS ONLY ROWS READS ABSENCE AS EVIDENCE OF ABSENCE**, filed at
`docs/solutions/workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md`.

**R-308.** `core.artifacts` landed and the four feature copies are not migrated
onto it.

## What U54 and U58 left behind, still current

**R-289**, the acquisition staging tree is a dotfile and `tagging.tag.audio_files`
walks dotfiles. **R-290**, a blocked job reports outcome `ok` and exits 0 in every
queued verb, which is the envelope contract rather than any one verb's line.

**The resume reads a rename intent, never the folder**, filed at
`docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`.
It applies to every remaining R-203 worker that moves files.

**The heavy stack stays behind the extra**, because `cli.jobs.argv_for` imports
the verb module by name to build a resume line.

**A fallback must not fill an absence somebody meant**, filed at
`docs/solutions/workflow-issues/a-remedy-fallback-overwrites-an-absence-somebody-meant.md`.

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | DONE on `relay/77` |
| | #78 | U60, the deletion pass | DONE on `relay/78`, no mutation table (R-329) |
| | #79 | U61, `crate sync all` composes the source increments | DONE on `relay/79`, no mutation table (R-329) |
| | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**Phase E is complete with the U53 merge, so line 7 is next and it is
Phillip's**: the explainer over the range from `46d5a4c` to the U53 merge
commit. A session does not run it.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Each was taken as a relay task, which is Phillip placing it.

**#42, R-5 is now probably a close.** METHOD's line 9 says so, on the grounds
that U59 lands the conformance assertions R-5 records as gated. Read R-5 against
the merged tree before assuming it, because two of those commits turned out to
be on `main` already, which is R-326.

Residual issues carry the `residual` label. They are the queue after the units,
each done or closed back to the ledger. A2 is attended. **#81, R-322, is the
first of them to be worked and it is done**, which leaves the rest of that label
as the live list; run
`gh issue list --repo philgutowski/cratekit --label residual --state open` rather
than trusting a count written here. R-324 is tracked on #80 and R-327 has no
issue, which is the normal state for a residual: the ledger holds it until
somebody decides to act on it.

**Every unit in METHOD's serialized list is now built, and so are #78 and #79.**
What is left on that list is Phillip's: the two explanations, the residual
issues, and #29.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds.
2. `board.py next`. It names #29. Do not take it. METHOD's serialized order is
   what picks the work, not the ranking.
3. Grep `docs/solutions/` for the module you are about to touch. A unit that
   opens a destructive write reads the barren list entry before it names an
   `analysis_roots`; a worker that moves files reads the rename intent entry
   before it binds.

## The branches

| branch | state |
|---|---|
| `relay/79` | U61, the branch this record is on; delete after the merge |
| `relay/78` | U60, merged to `main`; delete if it still exists |
| `relay/81` | R-322, merged to `main`; delete if it still exists |
| `relay/77` | U59, merged to `main`; delete if it still exists |
| `fix/conformance-3-and-soft-delete-reader` | LANDED into `relay/77` by merge. Still in `.worktrees/conformance`, untouched, and now redundant. Deleting it and the worktree is Phillip's call, not a session's, because the merge is not pushed yet |

## When a relay run is cut off mid unit

It has happened three times, all three on a usage limit, and the shape is worth
recognising. The endings differ:

- **The runner had already merged.** Its own verify then refuses to call the
  task landed, `halt_class: partial_landing`, and the tracker issue stays open.
  So `main` carries a unit whose review, table and record never happened. That
  was #72.
- **The runner had not merged.** The task branch holds the work and the tree is
  left dirty, `halt_class: unclean_exit`, and the run stops there whatever
  `on_halt.continue_past_task_halt` says. That was #75.

The state lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`, `halt_class`,
`halt_message`, `findings`, and `transcript_path`. Read the task's last assistant
messages to learn which pipeline step it reached. Finish it on the task's own
branch, merge, and close the issue from there. **Do not re-run the unit from the
board as though nothing had landed.**

**`verify` needs the issue named as `#N`.** After a hand landing, `relay_cli.py
verify <manifest> <task>` promotes the record only when it can find the link. It
derives one from a default branch commit naming `#N` when the record carries no
`landing_ref`; when the record already carries one, as a `partial_landing` record
does, it instead wants a tracker COMMENT naming that sha, and one comment is the
whole repair. native-relay's own `docs/solutions/` carries both halves.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why. **Never
  run `git checkout` on a file while a fix is uncommitted**: this session reverted
  one of its own review fixes that way and had to re-apply it, which is METHOD's
  driver rule arriving by hand instead of through a driver.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved, and U59 hit the sharper version: the soft delete
  reader pin went from two members to a DIFFERENT two, so the count did not move
  at all while both members did.
- **A guard that goes red at a merge is usually right and out of date.** Ask
  whether the RULE moved or the TREE did, and drive the answer. Weakening a stale
  guard to get green takes the rule with it. Four of them in U59, all four right.
- **The audit's exit code is a measurement, not a constant.** It exited 2 for
  R-324 until issue #25 was reopened and it exits 1 now for R-265, the `In
  review` card. Read what it printed rather than what a record predicted, and do
  not soften `contradictions()` either way. Softening it now fails tests, which
  is new: R-322 put seven of them behind that function.
- **A double belongs at the PRODUCER's boundary, not at the shape it produces.**
  Hand-build the payload the network returns and let the real derivation run over
  it. Hand-building the derived structure asserts what its author believes the
  producer makes. And making an input injectable moves the undriven path one
  frame UP, to the caller that supplies nothing, so write the row for the default
  branch too.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
  The worktree stays on that list even though its branch has landed, because
  removing it is a cleanup Phillip takes once the merge is pushed.
