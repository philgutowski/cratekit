# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-10, U59 built on `relay/77`, taken from the board as
issue #77 and run as relay task 77.** The unit ran the whole pipeline in one
session: plan, the merge, the built in `/code-review`, a six finding fix round,
a twenty five row mutation table with one composite, and this record. **The
pending register is still EMPTY**, and the merge is what kept it that way: git
took `main`'s empty `PENDING` and only the branch's three-state `module_state`
probe, so nothing was re-armed and no `@requires` decorator exists anywhere.

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

**TWO QUEUED VERBS HAVE NO WORKER.** `delete.review` and `sync.all`, with
`job.resume` exempt by role. Seventeen are bound. R-203 carries the correction
and its title stays at eighteen on purpose, because the title names what was
true when the entry was written.

**R-131 IS DOWN TO ITS ATTENDED HALF.** Everything in it that a session could do
is done and driven against a disposable database copy. Nothing has run on a live
tree, which is the whole of what the entry now says.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 2, and that is expected

The last measured suite was **7227 passed and 1 skipped**, taken on the branch
before the record commit; the record touches documents only. Collected 7228,
reconciled against `main`'s 7140 BY IDENTIFIER: zero ids lost, and the gain is
`test_pending_units.py`, `test_rb_writer_guard.py`, `test_metadata_policy.py`
and `test_genre_retag.py`. **Main's highest residual is R-326 once this branch
merges**, no duplicate headings, no heading deleted. The branch's own R-18 and
R-19 became R-320 and R-321, and their two source citations moved with them.
Append only, and gaps are fine.

**THE AUDIT EXITS 2 AND IT IS NOT DRIFT.** Issue #25 is closed while the verb
registry still carries `planned_in="U25"` on two entries whose modules do not
exist. This merge is what made that visible, because `contradictions()` read one
register and there are two. It is R-324, it needs a decision rather than a
repair, and `board.py sync` will not touch it on purpose. Do not weaken the
check to get a green audit.

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

## What U59 left behind, beyond the code

Seven residuals, R-320 and R-321 renumbered in from the branch and R-322 through
R-326 filed by this session, plus one learning. Four are worth knowing before
touching the board tooling or a source guard again:

- **R-324.** U25 is closed while the registry owes it two modules, so the audit
  exits 2 until somebody rules on it. The section above says why that is not
  drift.
- **R-322.** `contradictions()` is driven by NOTHING. The zero row over it was
  paired with a composite that deletes its closure test entirely, and the
  composite killed zero as well, which is what turns the first zero from a
  question into an answer.
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
| | #78 | U60, the deletion pass | Ready |
| | #79 | U61, `crate sync all` composes the source increments | Ready |
| | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**Phase E is complete with the U53 merge, so line 7 is next and it is
Phillip's**: the explainer over the range from `46d5a4c` to the U53 merge
commit. A session does not run it.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Where they fall is Phillip's to say, so a session does not take them.

**#42, R-5 is now probably a close.** METHOD's line 9 says so, on the grounds
that U59 lands the conformance assertions R-5 records as gated. Read R-5 against
the merged tree before assuming it, because two of those commits turned out to
be on `main` already, which is R-326.

Thirteen residual issues carry the `residual` label. They are the queue after
the units, each done or closed back to the ledger. A2 is attended. R-324 is a
fourteenth finding that needs a decision and has no issue yet.

**Every unit in METHOD's serialized list is now built.** What is left on that
list is Phillip's: the two explanations, the residual issues, and #29. #78 and
#79 exist and are not placed, which is his call.

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
| `relay/77` | U59, the branch this record is on; delete after the merge |
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
- **The audit exits 2 and it is R-324.** That is a decision waiting, not drift,
  and not a reason to soften `contradictions()`.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
  The worktree stays on that list even though its branch has landed, because
  removing it is a cleanup Phillip takes once the merge is pushed.
