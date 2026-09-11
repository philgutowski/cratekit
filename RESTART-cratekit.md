# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last session 2026-09-11, R-102 on `relay/54`, taken from the board as issue #54
and run as relay task 54.** The twelfth residual issue worked, and the last of
METHOD's guard group. Test work, closed in place, with one piece filed. The
reports allowlist audit in `tests/modules/test_reports.py` now walks the IMPORT
CLOSURE of `ALLOWED_IMPORTS`, not the list: `_admitted_closure` follows import
statements, `__import__` and `importlib.import_module` in one worklist pass and
returns what it cannot follow, which the audit refuses. Driven on the real tree,
`cause` calling a planted `access_probe` reads clean to the one hop walk and red
to the closure. **The closure is eighteen modules and reaches `rb_writer`**
through `rbxml`, `tree_registry` and `session`, so forty nine writers are now
named in `QUALIFIED_MUTATIONS`. **A unit that adds a writer to the write path
will now fail `test_reports.py`**, and the learning is
`docs/solutions/workflow-issues/the-reports-allowlist-audit-reaches-the-write-path-so-a-new-writer-there-fails-test-reports.md`.
The built in review drove three holes in the first version, `import_module`
unread, an unconditional package fallback, and a resolver asking the real tree
for a planted one, and all three are fixed and driven. R-340 is the report side:
a report calling a named writer through another module's attribute is not
caught. Sixteen rows are in `docs/mutation/r-102-rows.toml`, fourteen killing
and two predicted maintainer facing zeros, checked by hand on the one file and
recorded in `docs/mutation/r-102.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-15 on `relay/53`, taken from the board as issue #53
and run as relay task 53.** The eleventh residual issue worked, and the third of
METHOD's guard group. Test work, closed in place, with one piece filed. Measured
before any pin: a sixth permitted table and a bookkeeping column swapped for a
content column killed nothing in the full suite. `tests/test_whitelist_membership.py`
pins `PERMITTED_ROW_TABLES`, `BOOKKEEPING_COLUMNS`, and the content allow list,
which is registry derived here and so is pinned at baseline, per metadata
operation with its ownership mode, and fully enabled. The two deny lists beside
them, `GRIDLESS_ON_CREATE_COLUMNS` and the unwritable metadata fields, are pinned
too, since a removal is their widening. An AST audit holds every
`Rekordbox6Database` call in `src` to an explicit non empty `path=`. The built in
review found that `db_dir` also sets the binding's share directory, and that the
rows file's batch name would have let the driver overwrite the hand record, now
`r-15-driver`. Checking which file the connection opened is R-339. Ten widening
rows are in `docs/mutation/r-15-rows.toml`, all ten checked red by hand on the pin
file and recorded in `docs/mutation/r-15.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-14 on `relay/52`, taken from the board as issue #52
and run as relay task 52.** The tenth residual issue worked, and the first of
METHOD's correctness group. A fix, closed in place, with one piece filed. Read
against the tree, nothing in `src` joined `AnalysisDataPath` to anything. What
did exist was seven call sites arming the analysis watch over the library root
alone. With an acknowledged database outside the root, the share and every grid
sit outside it too, so each of those sessions watched nothing. `core.analysis_store`
now owns the join. `share_root` is the directory beside the configured database,
`analysis_file` joins a stored value to it, and `watch_roots` adds the share when it
sits outside the root. The seven sites take `watch_roots`, and an AST guard in
`tests/test_analysis_store.py` refuses a hand listed root. The backup carries the
share only when it sits under the root. Outside it, the plan, the outcome and the
verb's envelope now say `analysis-share-not-carried`, which the built in review
found reached nobody until the envelope asked for it. Carrying the share is R-338.
The kebab literal pin moved 401 to 402. Ten mutation rows are in
`docs/mutation/r-14-rows.toml`, two checked red first by hand and the rest unrun,
for R-329's reason.

**The session before, 2026-09-11, R-11 on `relay/48`, taken from the board as issue #48
and run as relay task 48.** The ninth residual issue worked, and the last of
METHOD's surface group. Two of its four findings closed, two stay on the ledger.
The CRLF absorption was three copies, not the four R-11 counted, since the
catalog writer takes the break after a node rather than before it. The three are
now `rbxml._absorb_lead_break`, and the goldens pass unchanged. The analysis
watch is now driven through the database half:
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session` plants a
real ANLZ file under the library root and asserts the `anlz-modified` refusal.
`apply_rating_changes` stays kept, since the wrapper has grown nothing. The real
label in two fixtures is still the author's decision about D1. Nothing new was
filed. Six mutation rows are in `docs/mutation/r-11-rows.toml`, two checked red
first by hand and the rest unrun, for R-329's reason.

**The session before, 2026-09-11, R-10 on `relay/47`, taken from the board as issue #47
and run as relay task 47.** The eighth residual issue worked, and the second of
METHOD's correctness group. A fix, not a close. `rb_writer.add_memberships`
takes one playlist and many content ids, reads what the playlist holds in one
query, and returns the ids it inserted. `add_membership` is a one id call into
it, so the only when absent rule still lives in one place. `write_tree_membership`
makes one call per playlist instead of one per track, and resolves each folder
once per session instead of once per plan entry. What remains per inserted track
is the binding's own content lookup and track count inside `add_to_playlist`,
which R-10 did not describe. R-10 is closed in place and nothing new was filed.
Eight mutation rows are committed in `docs/mutation/r-10-rows.toml` and unrun,
for R-329's reason.

**The session before, 2026-09-11, R-7 on `relay/44`, taken from the board as issue #44
and run as relay task 44.** The seventh residual issue worked, and the third of
METHOD's surface group. A close, since U27's doctor already reports a trashing
remote with its option unset, and setup runs doctor. Read against rclone
1.74.3's own backend help, two of that check's rows were wrong and are fixed.
Dropbox's row named an option the Dropbox backend does not have, so it failed
every run with a fix nothing could apply. OneDrive's `hard_delete` does nothing
on a personal drive and read green there. `TrashPolicy.applies_when` now gates
it on `drive_type`. R-336 and R-337 are filed. Six mutation rows are committed in
`docs/mutation/r-7-rows.toml` and unrun, for R-329's reason.

**The session before, 2026-09-11, R-6 on `relay/43`, taken from the board as issue #43
and run as relay task 43.** The sixth residual issue worked, and the second of
METHOD's surface group. Another close, measured on the registry: sixty four
entries, sixty two landed, and conformance 1, 2 and 3 parametrise over all
sixty two rather than the four R-6 described. The two markers left are U25's
vocals verbs, which R-324 and the reopened issue already own, so R-6 did not
carry them a second time. The `cratekit.cli.verbs` docstring said the package
held exactly U5's four verbs and it also holds `login`; it is corrected. No guard
changed, so there is no mutation table, and nothing new was filed.

**The session before, 2026-09-10, R-5 on `relay/42`, taken from the board as issue #42
and run as relay task 42.** The fifth residual issue worked, and the one METHOD's
ninth line names first. It was a close, as that line guessed. R-5's closing
condition was already true: U11 and U27 are closed, conformance 4 drives the
review queue and conformance 8 drives the doctor, and neither is an existence
check. What was false was the claim, in R-5 and in the docstrings of conformance
4 and 6, that no adjudicating or destructive verb had landed. Every adjudicating
verb has, and twenty two of twenty four destructive ones. The docstrings are
corrected. The gap they described, that neither assertion drives a landed verb
through the dispatcher, is still real and is R-335. No guard changed, so there is
no mutation table.

**The session before, 2026-09-10, R-4 on `relay/41`, taken from the board as
issue #41 and run as relay task 41.** The fourth residual issue worked, and the first of
METHOD's surface group. R-4's written closing condition was already true: each
of the nine toggles U5 declared gates a landed verb and none carries
`planned_in`. `registry.Entry` now refuses an `extras` group that is not the
verb's own `module_id` or is missing from `EXTRAS_BACKED`, because the stub
prints that field as the install command and nothing tied it to pyproject. A
derived parametrized test drives all thirteen toggles with landed verbs through
the resolver and parser in both directions. R-4 is closed in place, nothing new
was filed, and six mutation rows are committed in `docs/mutation/r-4-rows.toml`
and unrun, for R-329's reason.

**Two sessions back, 2026-09-10, R-3 on `relay/40`, taken from the board as issue #40
and run as relay task 40.** The third residual issue worked, and the second of
METHOD's guard group. `scripts/scan_repo.py` REFUSES a tracked archive now
instead of skipping it, by suffix and by header, so a renamed archive is refused
too. R-3's written closing condition was already true on the tree, since U13
committed the downloader unpacked, and nothing kept it true. R-3 is closed in
place. R-334 is the list still being closed, plus the same silent skip for a
`.db` or `.sqlite` file, and the choice there is Phillip's. Fifteen mutation rows
are committed in `docs/mutation/r-3-rows.toml` and unrun, for R-329's reason.

**Three sessions back, 2026-09-10, R-1 on `relay/38`, taken from the board as
issue #38 and run as relay task 38.** The second residual issue worked rather than a unit,
from the guard group in METHOD's ninth line. `crate doctor`'s `repo.commit_hook`
now reads every hook type `.pre-commit-config.yaml` names and checks each
installed hook, not only `.git/hooks/pre-commit`. R-1 is closed in place, and
R-333 is the one conservative call, a FAIL when PyYAML is not importable.

**THE PRIMARY CHECKOUT FAILS THAT CHECK, AND IT IS RIGHT TO.** It has a
pre-commit hook and no `.git/hooks/commit-msg`, so the board closing hook has
never run locally. Only CI has been judging trailers. The fix is Phillip's,
because it writes into `.git/hooks`:
`pre-commit install --hook-type pre-commit --hook-type commit-msg`. Twenty five
mutation rows, all killing, are in `docs/mutation/r-1.md`. The driver outran
the ten minute foreground ceiling twice, and a polling wait in the foreground
carried it through.

**Four sessions back, 2026-09-10, U61 on `relay/79`, taken from the board as
issue #79 and run as relay task 79.** `crate sync all` is a COMPOSER now. It plans every
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

**Five sessions back, 2026-09-10, U60 on `relay/78`, taken from the board as
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

**Six sessions back, 2026-09-10, R-322 closed on `relay/81`, taken from the
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

**Main's highest residual is R-340 once `relay/54` merges**, R-340 being that
branch's only filing, with R-102 closed in place, no duplicate heading and no
heading moved. Its suite was **7379 passed and 1 skipped**, in 358 seconds, on
`relay/54` on a committed tree. The eight since R-15's 7371 are this branch's
eight new identifiers in `tests/modules/test_reports.py`: six cases of
`test_the_audit_follows_an_admitted_module_to_the_module_that_writes`,
`test_the_closure_reports_an_import_it_cannot_follow`, and
`test_a_symbol_imported_from_a_package_follows_the_package_initializer`. That is
the new names matched against the delta, not the full collection differenced
against `main`. The R-15 record follows.

R-15's suite was **7371 passed and 1 skipped**, in 356 seconds, on
`relay/53` on a committed tree. The nineteen since R-14's 7352 are all in the new
`tests/test_whitelist_membership.py`: seven membership pins, the tree open audit,
ten audit refusals and one acceptance. The R-14 record follows.

R-14's suite was **7352 passed and 1 skipped**, in 352 seconds, on `relay/52` at
the record commit. The fourteen since R-11's 7338 are this branch's own: eleven in the new
`tests/test_analysis_store.py`, `test_the_analysis_watch_reaches_a_share_outside_the_library_root`
in `tests/test_adopt_apply_cli.py`, and the outside and contained drives in
`tests/test_backup_cli.py`. The R-11 record follows.

The last measured suite was **7338 passed and 1 skipped**, in 352 seconds, taken
on `relay/48` on a committed tree. One of the four since R-7's 7334 is R-11's
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session`; the other
three arrived with R-10, whose own count was not recorded, so that split is not
reconciled by identifier. **Main's highest residual stays R-337 once this branch
merges**, since R-11 filed nothing. The earlier record follows. Against R-6's
7328 the six are R-7's own in
`tests/test_doctor.py`: four cases of
`test_a_onedrive_remote_where_hard_delete_does_nothing_is_a_note` and two of
`test_dropbox_is_not_told_to_set_an_option_rclone_does_not_have`. **Main's
highest residual is R-337 once this branch merges**, R-336 and R-337 being this
branch's, with no duplicate headings and none deleted. R-5 and R-6 changed no
test. Against R-3's 7312 the 16 before those are R-4's
own, reconciled by identifier in `tests/test_cli_contract.py`: two rejection
rows in `test_an_entry_missing_its_metadata_fails_to_register`,
`test_every_live_toggle_is_driven_by_the_toggle_test_below`, and thirteen cases
of `test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off`. **Main's
highest residual stays R-335 once this branch merges**, no duplicate headings, no
heading deleted, and R-6 gained its closing note in place rather than moving.
Append only, and gaps are fine.

**The kebab literal pin in `tests/test_reserved_causes.py` moved 401 to 402** on
R-14, for `analysis-share-not-carried`, a warning code and not a cause. Before
that it moved 391 to 401 for ten git hook type names, differenced as sets
against `main`, none of them a cause.

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
| 9 | #38 | R-1, doctor checks every configured hook type | DONE on `relay/38`, 25 of 25 rows killing |
| | #40 | R-3, the scan refuses a tracked archive | DONE on `relay/40`, 15 rows committed and unrun (R-329) |
| | #41 | R-4, extras tied to their module and every toggle driven | DONE on `relay/41`, 6 rows committed and unrun (R-329) |
| | #42 | R-5, conformance 4 and 8 already drive behaviour, closed in place | DONE on `relay/42`, no guard changed, R-335 filed |
| | #43 | R-6, the conformance drives cover sixty two landed verbs, closed in place | DONE on `relay/43`, no guard changed, nothing filed |
| | #44 | R-7, doctor reports a trashing remote, closed in place with two rows fixed | DONE on `relay/44`, 6 rows committed and unrun (R-329), R-336 and R-337 filed |
| | #47 | R-10, one membership call per playlist and one folder lookup per folder | DONE on `relay/47`, 8 rows committed and unrun (R-329) |
| | #48 | R-11, the lead break helper and the watch driven through the database half | DONE on `relay/48`, 6 rows committed and unrun (R-329), two findings still open in the ledger |
| | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**Phase E is complete with the U53 merge, so line 7 is next and it is
Phillip's**: the explainer over the range from `46d5a4c` to the U53 merge
commit. A session does not run it.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Each was taken as a relay task, which is Phillip placing it.

**#42, R-5 was a close**, read against the tree rather than assumed. Its
successor is R-335, which has no issue.

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
| `relay/48` | R-11, the branch this record is on; delete after the merge |
| `relay/47` | R-10, merged to `main`; delete if it still exists |
| `relay/44` | R-7, merged to `main`; delete if it still exists |
| `relay/43` | R-6, merged to `main`; delete if it still exists |
| `relay/42` | R-5, merged to `main`; delete if it still exists |
| `relay/41` | R-4, merged to `main`; delete if it still exists |
| `relay/40` | R-3, merged to `main`; delete if it still exists |
| `relay/38` | R-1, merged to `main`; delete if it still exists |
| `relay/79` | U61, merged to `main`; delete if it still exists |
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
