# Residual findings

Findings that are accepted but not yet fixed. The Definition of Done requires
this file to be current before each merge, so a known problem is a recorded
decision rather than something a future reader has to rediscover.

Each entry says what was found, why it was not fixed here, and what closes it.

---

## R-1. The commit hook is off by default on a fresh clone

**Found:** during U6 verification, 2026-08-01.

`scripts/scan_repo.py` is wired as a pre-commit hook and as a CI job. The hook
is the one that matters, because a personal literal or a credential that reaches
a commit is already in the history, and removing it is a rewrite every clone has
to follow.

The hook only exists after `pre-commit install` has run, and that command only
exists after pre-commit is installed. Both were README steps. On a machine where
pre-commit was not on the PATH, a planted personal path committed cleanly with
no hook and no warning. The guard was not weak, it was absent, and nothing said
so.

**Partly fixed here:** a `dev` extra now carries pre-commit, pytest, and ruff, so
`pip install -e '.[dev]'` makes the documented setup executable.

**Still open:** nothing verifies the hook is actually installed in a given clone.
Installing the tool is not the same as installing the hook.

**Closes when:** the doctor verb checks that `.git/hooks/pre-commit` exists and
dispatches to this repository's configuration, and reports the exact command
when it does not. Doctor lands in U27.

---

## R-2. Four live portability and layering violations in the source repository

**Found:** during U6, while widening the guards. Confirmed independently against
the source at the lines given. Nothing in the source repository was changed.

These are recorded because Cratekit must not inherit them, and because two of
them are the exact blind spots the plan predicted the old guard had.

**Import direction, both masked by a lazy import:**

1. `src/dj_tools/DJ_common/routing.py:365` imports an analysis module from inside
   a function in the shared router. The router is domain-layer and the analysis
   module is a feature module, so this runs upward through the layering. The
   imported module pulls a numeric stack at module level, so a slim install
   raises on the first vocally routed track rather than at import, which is the
   worst place to discover it.
2. `src/dj_tools/DJ_common/sweep_prep.py:77` and `:126` import a feature module
   from a shared helper. This one is a genuine cycle, since that feature module
   imports four shared modules at module level. The laziness is what hides it.

Cratekit's `tests/test_layering.py` fails the build on either shape, so neither
can be ported in.

**Portability, in shipped skills the old guard could not see:**

3. A shipped skill document carries an absolute home-directory path. The old
   rule matched one volume literal only, so home directories were unchecked
   everywhere.
4. A second shipped skill carries a bare volume name with no path around it. A
   full-path match cannot see that shape at all.

Both are caught now: `scripts/scan_repo.py` covers every tracked path rather
than package source, and the bare-name tier plus the declared identity file
covers the second.

**Closes when:** the source repository is retired at the end of the migration.
These are not fixed there because it is the live system and this plan does not
change it. If any of these files is used as porting source, the violation is
fixed in the port, not carried across.

---

## R-3. The secret scan cannot read inside compressed archives

**Found:** during U6.

The scan skips binary content, so a credential inside a `.tar.gz` or `.zip` is
invisible to it. This matters concretely: the downloader artifact that gets
vendored currently sits in the same directory as a live session cache holding
OAuth tokens, an environment file holding service credentials, and a web token.

**Mitigated:** the scan flags credential-shaped *filenames* regardless of
content, so a credential store carried in by name is caught even when its bytes
are unreadable.

**Still open:** an archive whose *inner* paths carry a credential is not
inspected.

**Closes when:** the vendoring unit lands and the vendored tree is committed
unpacked, with its provenance recorded, rather than as an archive. Vendoring is
U13. If an archive must ship, the scan needs an archive-aware tier.

---

## R-4. Nine module toggles were added to satisfy R5, and two of them gate nothing

**Found:** during U5, while building the verb registry.

R5 says profile membership FOLLOWS the Feature Inventory: Module rows are opt-in
and a slim install runs the Core rows only. Nine Feature rows dispositioned
Module had no toggle to follow, so a verb for any of them would have had to ship
as core and be on in the slim profile, which is the opposite of what the
inventory says. `core/profiles.py` now declares those nine.

Two of the toggles that already existed, `web` and `desktop`, gate no verb,
because Feature 32 is deferred and the CLI is the launch product. They are
declared in `registry.DEFERRED_MODULES` so the "every toggle is used by a verb"
check can tell a deferred module from one whose verb somebody forgot to gate.

**Still open:** the reverse mapping is asserted, but nothing checks a toggle's
name against the extras table for modules that have no extras group, because
most of these have no heavy dependency at all. If one later grows one, the
`EXTRAS_BACKED` set has to grow with it, and only `tests/test_config.py`'s
existing extras assertion would catch the mismatch.

**Closes when:** each of the nine units lands its verbs and the corresponding
`planned_in` marker clears, at which point the toggle is exercised end to end
rather than only declared.

---

## R-5. Four conformance assertions are written in full and gated on units that have not landed

**Found:** during U5.

The verb conformance suite asserts nine properties. Four of them name a module
that does not exist yet: the review queue (U11), the job engine (U10), the
destructive-session gates (U8), and the doctor check registry (U27). Each is
registered in `tests/_pending.py` against the unit that lands it, so the skip is
a countdown rather than a hole, and `tests/test_pending_units.py` fails the build
the moment one of those modules appears.

**Two of the four are now closed.**

*U10's* landed with the job engine. Assertion 5 drives the engine rather than
importing it.

*U8's is closed here (2026-08-01).* Assertion 6 was an existence check
(`hasattr(session, "assert_gates")`) and is now behaviour. For every verb the
registry declares destructive, derived by iterating the registry rather than
listed, it drives all three refusals and asserts three distinct codes: a lock
held elsewhere is 20, a missing acknowledgment is 32, and a volume whose
recorded identity does not match is 22. "Zero writes" is asserted against the
FILESYSTEM, by fingerprinting the library root, the installation state directory
and the config directory either side of each call and comparing. That is what
made the gate ORDER load-bearing rather than stylistic: volume, then
acknowledgment, then lock, because the lock is the only gate that creates a file
and it therefore has to go last for the property to be true rather than
approximately true.

**What is honestly NOT covered, and why.** Every destructive registry entry
still carries a `planned_in` marker, so there is no landed destructive verb to
invoke through the dispatcher. What assertion 6 drives is the shared gate every
one of them must pass through, once per declared verb and under that verb's own
name. `tests/test_write_session.py` additionally drives the same three refusals
through a real destructive OPERATION, the backup restore, which does exist. The
end-to-end drive through `cli.run` waits on the first destructive verb landing.

**Still open:** U11's and U27's assertions remain existence checks against the
review store and the doctor check registry.

**Closes when:** U11 and U27 land. The unit that lands the module owns turning
its assertion from existence into behaviour, in the same commit that removes the
pending entry.

---

## R-6. Two shipped verbs have no argument surface beyond what U5 needed

**Found:** during U5.

`profile show`, `profile set`, `run show`, and `run decide` are the vertical
slice the plan asks for, chosen because between them they exercise every
contract this unit sets. They are real verbs, not scaffolding, but they are not
the verbs a user spends time in.

**Still open:** the registry declares roughly fifty more verbs with a
`planned_in` marker. Until those land, the per-verb conformance drives run over
four entries, so the assertions are proven correct on a small sample rather than
on the whole surface.

**Closes when:** each later unit clears its marker. The assertion that a planned
module is still genuinely absent is what forces that to happen rather than being
remembered.

---

## R-7. Backup pruning reclaims space only if the remote is configured to

**Found:** during U35, porting the backup script.

The source system's prune passes a Google Drive option so the deleted archive
folders bypass the provider's trash and stop counting against the quota
immediately. Without it, on Drive specifically, a pruned folder keeps occupying
the quota for thirty days, which defeats the point of pruning on a library this
size.

**Not carried across, deliberately.** The remote is configuration now, and that
flag is meaningless on most providers and wrong on some. Baking a
one-provider option into a command built for every provider is the shape this
port exists to remove.

**Still open:** nothing tells a user of that provider to set the equivalent.
rclone supports the option per remote in its own configuration, so the setting
exists; what is missing is the prompt.

**Closes when:** the setup wizard asks, or doctor reports, that a remote whose
provider trashes on delete has the per-remote option set. Both land in U27.

---

## R-8. The backup restore is not yet bound to the destructive-session gates

**Found:** during U35. **CLOSED 2026-08-01, by U8.**

A restore replaces a live rekordbox database and its sidecars. KTD24 binds the
library lock, the backup acknowledgment, and the volume identity assertion to
any operation that can destroy user data, whether or not it writes a database
row, and a restore is squarely one.

**Why it was not bound at U35:** the session boundary is U8 and was not present.
The verb was declared `destructive=True`, and the restore path already refused on
the two conditions it could check alone: an unconfirmed decision and a live
rekordbox process.

**How it is closed.** `modules/tools/backup.py` imports `cratekit.core.session`,
which is a downward import from the modules layer and therefore legal, and both
halves of a restore now run inside `session.assert_gates`:

- `plan_restore` enters the gates around its whole planning body. The one check
  that stays ahead of them is `_require_destinations`, which reads configuration
  and resolves no path; everything after it resolves paths on the library volume,
  and a destructive session has to refuse before it resolves one.
- `run_restore` enters them again around the execution, and its `cfg` is a
  REQUIRED positional rather than an optional keyword, so there is no call shape
  that reaches the destructive half with nothing to gate on. An optional one
  would be exactly the softening path P5 says to close in the commit that creates
  it.

The module's existing refusals are kept, not replaced: an unconfirmed decision
and a live rekordbox process still refuse by name and in this module's own
vocabulary. `runner` and `process_lister` stay injectable and a third seam,
`gates`, joins them, so this module's own battery stays hermetic while the wiring
itself is asserted with the real guard in place.

**The ordering question P6 asks, decided.** A dry run is NOT exempt from the
gates, and the test asserts that. Three reasons, in order of weight. The lock is
the one that matters: a rehearsal that runs while another destructive session is
writing describes a library that is changing underneath it, so its preview is a
report about a world that no longer exists, which is worse than no preview.
Second, the reason the plan and the run are one pair of functions is that a
preview built by a second code path can be wrong about the run it previews, and a
preview that skipped a guard the run does not skip is that divergence wearing a
different hat. Third, a rehearsal that passes is then evidence the real run will
reach its work, which is most of what a person rehearses for. What a dry run
still skips is the sidecar CLEARING, which is unchanged and is a different
question: clearing is itself destructive, so a rehearsal that cleared and then
transferred nothing would do the damage and skip the repair.

**Still open, and all three belong to the verb rather than to the wiring.** An
adversarial read of this commit found them; each is registered in
`tests/_pending.py` against `cratekit.core.restore` so it is a countdown rather
than a note.

1. **The plan and the run each take the lock and give it back.** With `gates`
   left at its default, `plan_restore` enters the guard, builds the plan, and
   releases on the way out; `run_restore` then enters it again. A second process
   can pass the same gates and commit in that window, and the run then copies a
   snapshot over a commit its plan was built before. The `GateGuard` seam exists
   so a caller can hold ONE session across both halves, and the verb must: a plan
   is a value and cannot own a live context manager, so the composition is the
   caller's to make.
2. **The record outlives the restore that answers it.** The session log is
   declared `SURVIVES_ROLLBACK`, deliberately, because rolling it back would
   erase the record of which sessions are restorable. So a
   `committed-unverified` record is still there after the restore that resolves
   it, and the verb has to call `session.resolve_unverified_session` on success.
   The function landed with U8; naming it in the verb's success path is U32's.
3. **Bare-metal recovery, where the library volume itself is gone, has no path.**
   Every gate is library-scoped by KTD21, on purpose: the lock, the
   acknowledgment and the session log all sit beside the library so a second
   machine contends with the first instead of holding an invisible lock of its
   own. The cost is that all three are unreachable when that disk is the thing
   that died, so the restore refuses with `library-volume-unmounted` and tells
   the user to mount a drive that no longer exists. Moving the volume assertion
   onto the restore TARGET does not fix this and should not be attempted: the
   refusal would simply move to the acknowledgment, which lives on the same dead
   volume, and the live case would lose a real check. What this needs is a
   recovery path that does not read its gates from the library it is rebuilding,
   which is a decision U32 owns.

---

## R-9. Two verification gates for this unit need hardware this run did not have

**Found:** during U35 verification.

The plan's verification step for this unit is "one real backup run and a restore
rehearsal to a scratch directory". Neither ran end to end against a real remote.
A real backup needs a configured remote holding a copy of a library measured in
hundreds of gigabytes, and no such destination is configured on this machine;
the library volume is also read-only to this work by instruction.

**What did run:** every decision and every command the run would issue, against a
temporary directory with the command runner and the process probe injected, plus
the restore's sidecar-clearing order asserted on real files. The uncovered
surface is exactly one thing: whether rclone accepts the argument vectors this
builds.

**Closes when:** the author configures a remote and runs the backup verb once
with its dry run, then for real, and records the outcome. That is an attended
step, like the other live-hardware gates in this plan.

---

## R-10. Membership insertion is one database round trip per track

**Found:** during U18 review, by the efficiency reviewer, confirmed against the
code it names.

`write_tree_membership` calls `rb_writer.add_membership` once per resolved track,
and that helper runs its own `get_playlist_songs(PlaylistID=..., ContentID=...)`
query before deciding whether to insert. A sweep over a few hundred sub-playlists
therefore issues hundreds to low thousands of individual select-then-maybe-insert
round trips inside one locked write session. One query per PLAYLIST, building the
set of content ids already in it and diffing in memory, would answer the same
question.

**Not fixed here, and the reason is the same argument this unit makes twice
elsewhere.** The idempotency check lives in `add_membership`, which is U7's. To
batch it from the caller, this unit would have to ask the database what a
playlist already holds and decide for itself what is new, which is a second
implementation of the rule `add_membership` owns. Two implementations of one rule
is how they come to disagree, and the disagreement here is a track silently
inserted twice or silently skipped. The same reasoning is why the medium check
goes through `tree_registry.anchored_root` rather than being spelled again.

It is also bounded by tracks per playlist rather than by library size, against a
local SQLite file, inside a session that is already holding a lock. The N times M
walk that WAS unbounded, the row index rebuilt per plan entry, was fixed in this
unit rather than recorded.

**Closes when:** `rb_writer` grows a batch membership primitive that takes a
playlist and many content ids and returns which ones it inserted. Then one call
replaces the loop and the rule stays in one place. That belongs to whichever unit
next has a reason to touch that module.

**One more of the same shape, found by the U18 performance review.**
`ensure_folder` and `ensure_playlist` are re-queried once per plan entry, so
entries sharing a folder re-issue the same lookup. Bounded to a few hundred extra
local queries per sweep, sub-second, and it closes with the same batch primitive.


---

## R-11. Four accepted findings from the U18 review

Seven reviewers ran over U18. Six findings were fixed in the unit, all of them
invisible to a green suite, and these four were judged and accepted instead.

**The CRLF-adjacency absorption is written out four times.** `insert_root_playlist`,
`remove_folder_node` and `insert_intake_playlist` each check for a break beside a
node and extend their range to swallow it, and U18's `insert_catalog_folder` adds
a fourth. A shared helper is the obvious answer and the goldens make the refactor
safe to verify. It was not done here because three of the four are landed writers
whose exact bytes nine goldens pin, and rewriting them is not this unit's work.
**Closes when:** any unit with a reason to touch those writers extracts the
helper and re-runs the golden suite unchanged.

**`apply_rating_changes` names one idea in two modules.** `trees` wraps
`rbxml`'s, adding only a mapping coercion. Judged and kept, on the same footing
as the collisions the handoff already records: the return types agree, so
importing the wrong one is harmless, and the wrapper is the entry point the
goldens name while the emitter is the byte primitive. Worth revisiting if the
wrapper ever grows behaviour, because then the two would genuinely diverge.

**The analysis watch refuses an empty root LIST, not an empty walk.** A reviewer
argued it should refuse when the walk finds no analysis files. It should not: a
library that genuinely holds none is ordinary, and refusing it would fire on
correct code, which is how a guard gets switched off (P7). What the review did
surface correctly is that no test names a root that actually holds an analysis
file, so the watch is armed and watching nothing in the battery. **Closes when:**
a database-half test seeds a real analysis file, rewrites it inside the session,
and asserts the `anlz-modified` refusal.

**A real record label is used as fixture data.** `tests/test_tree_writer.py` and
the pre-existing `tests/test_xml_splice_golden.py` both use a real label name,
which is in the author's own favourites list. D1 forbids a shipped artifact
naming a real volume, person, or track, and a label is none of those three, so
this is outside its letter. Recorded rather than changed because the string is
already baked into a committed golden file, so changing it means regenerating
that golden. **Closes when:** the author decides D1's intent is broader than its
three nouns, and both fixtures move to an invented label in one pass.

---

## R-12. The membership write takes a snapshot that nothing protects

**Found:** during U19, 2026-08-02, by the unit that became `write/trees.py`'s
first caller. Confirmed independently against the two modules before it was
recorded.

`write_tree_membership` takes a capture through `snapshot.capture` and asserts it
through `snapshot.assert_verified`, but it never opens a `SessionRecord`. There
is no `open_session`, no `attach_capture`, and no `close_session` anywhere in
`write/trees.py`.

`rb_writer.default_protected_snapshot_paths` derives its protected set by reading
`session_log` and keeping the captures named by records whose state is not
terminal. A capture with no record is named by nothing, so it is unprotected from
the moment it is taken, and a concurrent or subsequent `prune_snapshots` is free
to delete the capture that an in-flight membership write is the undo for. That is
the guarantee R30 states in one sentence: a snapshot an unfinished run may
restore from is not old, whatever its position in the retention order.

This is the same shape the RESTART note warned about when U8 was written, arriving
from the other side. U8 was told to write into `session_log` rather than the
installation-scoped `runs/` directory precisely so the protection scan would stop
matching nothing. It does match now, and the membership writer simply never
enrolls.

The second consequence is quieter. U32's `restore.list` reports timestamp,
workflow, and a change summary naming the affected trees and per-tree counts. A
membership write that records no session produces no `ChangeSummary`, so the one
database write this product makes to a governed tree is absent from the list of
things a person can restore, even though `MembershipReport` already carries the
exact `TreeChange(tree, created, updated)` numbers that listing wants.

**Not fixed here** because the fix is not a line in the caller. Enrolling the
membership write in a session means deciding how it composes with R29's one
source per run when the caller already owns a session, and U19 deliberately does
not pass its own gates factory in, because that reopens the analysis-roots hole
U8 registered against U26. Choosing that composition is a unit's work, not a
merge's.

**Closes when:** `write_tree_membership` opens a session record around its
capture, so the capture is protected for the life of the write and the write
appears in `restore.list` with its per-tree counts. The natural owner is U32,
which owns the restore verb and already carries three registered obligations, or
U26, which is the first workflow that will call the membership writer in anger.

---

## R-13. Four routing verbs name a CLI module no unit's file list declares

**Found:** during U19, 2026-08-02, and confirmed by its review.

`route.inbox`, `route.unplaced` and `route.resort` were declared in the registry
against module `cratekit.write.routing_cli` with `planned_in="U19"`, and U19 added
`route.pending` beside them. U19's declared file list never contained a CLI
module, and the unit could not land one: `test_conformance_3` requires a landed
gated verb to exit `OK` once its gate is answered, and every verb writing
`db_tree` must declare the cloud-sync gate, so a destructive database verb cannot
pass conformance on a machine with no database.

Left alone, closing issue #19 would have made all four markers name a unit that
had already landed, and nothing would have noticed. `test_cli_contract.py` only
fires when the module appears, and `scripts/board.py` reads `tests/_pending.py`
alone, so the obligation would have been owned by no mechanism at all.

**Fixed far enough to be safe:** `cratekit.write.routing_cli` is now registered in
`tests/_pending.py`, which is the file the board audit actually reads, so the
obligation is tracked whichever unit ends up holding it. All four `planned_in`
markers go through one `ROUTING_CLI_UNIT` constant and currently name **U20**,
on the reasoning that U20 flips trees to database-native and therefore has to
ship a destructive database CLI surface anyway.

**Settled 2026-08-02: U20 owns it, by Phillip's decision.** The inference is now
the answer, on the reasoning it was made for: U20 flips trees to database-native,
so it has to ship a destructive database CLI surface regardless, and the four
routing verbs ride along on work that unit already owes. `ROUTING_CLI_UNIT` and
the `tests/_pending.py` entry both name U20 and need no edit.

**This entry stays open only for the thing underneath it.** Conformance 3
requires a landed gated verb to exit `OK` once its gate is answered, and every
verb writing `db_tree` must declare the cloud-sync gate, so **no destructive
database verb can land on a machine without a database**. That is not a fact about
the routing CLI, it is a wall in front of every such verb, and U21, U24 and U32
all queue behind it. Recorded here rather than acted on, because relaxing a
conformance rule that four waves have honored is a deliberate act and not a
side effect of landing a CLI.

**Closes when:** conformance 3 can be satisfied against a disposable database
fixture, on the `CRATEKIT_TEST_DB` convention that already SUBSTITUTES rather
than skips, so the battery runs either way and a supplied fixture strengthens it.
The natural owner is U27, which lands doctor and is the unit that makes a machine
ready.

---

## R-16. Four report verbs were owed by a unit that was about to close, and named a module nobody could build

**Found:** during the U34 review, 2026-08-02, by two independent reviewers.

**Numbering note:** R-14 and R-15 are issues #52 and #53 and were never written
up here, so the gap is a missing pair of entries rather than two that somebody
deleted. Numbers are not reused, because a slug in a commit message outlives the
file.

`audit.coverage`, `audit.duplicates`, `report.library` and `report.intake-aging`
were declared in the registry against module `cratekit.reports.cli` with
`planned_in="U34"`. U34's declared file list is `src/cratekit/modules/reports/`
and its test module, and that is exactly what it landed: the duplicate audit and
the intake aging engines, no command-line surface. The unit also cleared its
`tests/_pending.py` entry, which was the required act of landing, since keeping
it would have made `board.py audit` report a contradiction and exit 2.

The two together are R-13 verbatim, one wave later. After `Closes #34`, all four
markers would have named a closed unit: `board.py audit` prints "The board
matches the repository" and exits 0, `test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
asserts the module is ABSENT so it passes forever and never fires, and
`scripts/board.py` reads `tests/_pending.py` and nothing else. Four verbs owned
by no mechanism at all.

The module path was also unbuildable as spelled. `test_layering.layer_of` ranks
`cratekit.reports.cli` as `modules` and `cratekit.cli.registry` as `cli`, so the
module that must dispatch through the registry could not have imported it. U10
and U11 each made the same correction on landing, and the comments above the job
and review blocks in the registry record both.

**Fixed here.** The four entries name `cratekit.cli.reports` and go through one
`REPORTS_CLI_UNIT` constant, and that module is registered in `tests/_pending.py`
against **U27**, which is the file the board audit actually reads.

**Why U27, stated so a human can move it again.** It is the only open unit whose
declared file list already lands modules in `src/cratekit/cli/`, `setup.py` and
`doctor.py`, so `cli/reports.py` is the same act in the same directory rather
than a new kind of work for a unit that does none of it. Three of the four verbs
emit `diagnostic/1`, which is doctor's own output surface, and U27 owns the check
registry that surface is rendered against. And U27 is unblocked today, so the
obligation can be discharged next rather than parked behind a dependency chain.

Two alternatives were weighed and rejected. **U29** is the only unit that
structurally cannot close while these verbs are missing, since its test scenario
generates a parity table from the verb inventory, but its declared files are
`docs/cutover.md` and `README.md` and its execution note forbids batching: giving
a code obligation to a documentation unit is the same "owned by nobody" failure
one hop later. **U36** owns `converge`, which is the database-side sibling of a
coverage report, but `audit.coverage` here reads an export rather than the
database, and neither aging nor duplicates has anything to do with tree rebuild.

**What U27 inherits with it, stated rather than hidden.** `audit.coverage` and
`report.library` have no engine anywhere in the tree; nothing computes tree
coverage or library statistics today. So that unit lands two report engines as
well as the shell. `audit.duplicates` and `report.intake-aging` are thin over
engines U34 landed.

**Closes when:** `src/cratekit/cli/reports.py` exists with the four builders, the
two missing engines land beside the two that exist, and the `tests/_pending.py`
entry is deleted, which arms the conformance assertions over all four verbs.

---

## R-17. The review-queue countdown is satisfied by an offer that never runs

**Found:** during the U34 review, 2026-08-02.

`tests/_source_guards.offers_into` answers True when a source contains a
`review.offer(queue=Queue.DUPLICATES, ...)` call, and it walks the syntax tree,
so the call may sit in a function nothing calls or under `if False:`. The armed
countdown in `tests/test_review_queue.py` that asserts a landed target genuinely
produces into the queue it was registered against therefore has a floor it cannot
see below: a package could satisfy it with an offer that never executes.

**Not fixed here.** Reachability is not decidable from a syntax tree in general,
and the cheap half, rejecting a call under a literally false branch, buys nothing
against an author who wanted to pass rather than to produce. The honest fix is a
behavioural assertion per registered producer, which is what
`tests/modules/test_reports.py` already does for this one: the audit is driven and
the item is read back out of a store opened in a second process. That is the
shape to generalize, and generalizing it belongs with the file it lives in.

**Narrowed in round 2.** Recording this finding turned out to have hidden a
second one underneath it. The guard the finding describes the floor of,
`_target_offers_into`, could be stubbed to `return True` with the entire suite
still green: every table entry but one is still a countdown and takes the early
return, and the one that has landed is covered from the other side by a test
calling a different helper. Its module-shape branch had never executed at all. So
the assertion that a landed producer really produces was carried by a function
nothing could show was capable of saying no, which is a strictly worse problem
than the reachability floor this entry names. The helper is now asserted in both
shapes and both polarities. What remains open is only the original floor: a
producer could still satisfy it with an offer in a function nothing calls.

**Closes when:** each entry in `NEW_SURFACE_OWED_BY` is answered by driving its
producer rather than by reading its source, once enough of them have landed for
the shared harness to be worth writing. The natural owner is U26, which is the
first unit to land a second producer into a declared surface.

---

## R-18. A third copy of the import-graph walk now lives in the reports suite

**Found:** during the U34 review, 2026-08-02.

`tests/_source_guards.py` exists because two files asked the same question with
two copies of one walk and the copies diverged: one learned to recognize an
aliased import and the other did not. `tests/modules/test_reports.py` adds a
third copy, in `_resolved_imports`, and it has already diverged from the
`tests/test_layering.py` copy over CapWords and dunder handling, which that file
excludes from module expansion and this one does not.

**Measured in round 2, corrected in round 3, and it changes no verdict today.**
Both walks were run over all four modules of the reports package and their
outputs compared. Round 2 recorded the divergence as one entry wide. It is
THREE entries across TWO modules: `from typing import Sequence` in
`duplicates.py` resolves to `typing.Sequence` here and to `typing` in
`test_layering.py`, and `export.py` diverges the same way twice, on
`collections.Counter` against `collections` and on `pathlib.Path` against
`pathlib`. All three are the CapWords rule and nothing else. All six spellings
are permitted by `_permitted`, because an allowlisted entry admits its dotted
children, so the forbidden set is empty under either walk for every module. The
conclusion survives the correction and the count does not: the divergence is
real, it is three entries wide, and it is not currently capable of letting an
import through or of failing a correct one.

**Not fixed here**, deliberately. U12 is concurrently generalizing
`_source_guards.ReviewImports` into a module-parameterized `ImportsOf`, which is
where this walk belongs, and collapsing three copies into a shared helper in this
round would put a large edit to a shared test module in front of that work and
conflict with it. The copy here was widened rather than collapsed: it now
resolves relative imports against a package read off the filesystem, expands a
`from X import y` where X is a real package directory at any depth, and reads
`__import__` as the import it is. Those three widenings are what the shared
version will have to carry, so the divergence is recorded rather than deepened by
accident.

**Closes when:** `ImportsOf` lands from U12 and all three call sites read it,
including the CapWords and dunder rule, which must be settled in one place rather
than three. The natural owner is U12.

---

## R-19. The option a person picks is addressed by an identifier a re-import changes

**Found:** during the U34 round 2 verification, 2026-08-03.

`duplicates.DuplicateGroup.options` builds one `review.Option` per copy with
`option_id=member.track_id`, and the track id is the rekordbox `TrackID` from the
export. That identifier is unique WITHIN one document, which U34 now refuses over
when it is not, and it is not stable ACROSS documents: re-importing a library
gives every row a new one, and `test_a_renamed_or_re_imported_copy_keeps_the_decision`
demonstrates exactly that, one line below the assertion that the item id survives.

So the item survives a re-import and the answer inside it does not. An ACCEPTED
verdict on a duplicate group names which copy is kept, and after a re-import that
name points at whatever row now holds the number. `review.offer` leaves a resolved
item's options alone by design, which is correct and is also what freezes the
stale identifier in place. Nothing in this unit reads a verdict back, so nothing
is wrong today; the surface that acts on it is the deletion pass R35 and R36
declare, which is U24's.

There is no stable per-copy identifier available in a collection export. The
track id moves on re-import and the location moves on a rename, and the module
promises that neither of those orphans a decision. That is why this is recorded
rather than patched: choosing one of the two would trade a wrong answer in one
direction for a wrong answer in the other, and the choice belongs with the unit
that consumes it.

What is available to the consumer is already carried: each option's `detail`
holds the copy's location, and the payload holds every member's track id and
location together.

**Closes when:** the deletion surface either re-verifies a chosen option against
the export it is acting on before deleting anything, or the pair agree on an
identity that survives both a re-import and a rename. The natural owner is U24.

---

## R-20. Two reflection spellings reach a writer past both structural guards

**Found:** during the U34 round 3 verification, 2026-08-03.

Rule 4 of `filesystem_mutations` covers `getattr` and only `getattr`. The
attribute dictionary reaches the same method by SUBSCRIPT, and a subscript is not
a call, so neither the attribute rule nor the call rules have anything to read:

```python
Path.__dict__["write_text"](path, decided)
vars(Path)["write_text"](path, decided)
```

Both write a file, and both were run to confirm it rather than reasoned about.
The CLASS has to be named, not the instance's type: `Path("x")` is a `PosixPath`
and `write_text` is defined on `Path`, so `type(obj).__dict__["write_text"]`
raises `KeyError` on an inherited method. That is a detail worth writing down,
because getting it wrong makes the escape look like it does not exist. `forbidden_imports` says nothing, because nothing is imported
that is not already permitted. `filesystem_mutations` says nothing, because the
mutating name appears only inside a string subscript and the outer call's `func`
is itself a subscript expression. The allowlist audit says nothing for the same
reason, so a helper spelled this way in an admitted module is never forced into
`FILESYSTEM_MUTATIONS` either.

**Not fixed here**, deliberately, and this is an accepted boundary rather than a
deferred repair. Round 2 widened rule 4 to cover the reflective shape that a
person actually writes; this pair is exotic in a way `getattr` is not, and it was
equally uncovered before round 2, so recording it is a widening of what the
guards claim rather than a regression they introduced. The cost of covering it is
a rule that reports every constant string subscript whose value happens to name a
method, which is the P7 shape this whole guard is written around: the first
correct `mapping["write_text"]` in a report would fail it.

Both spellings are written out above so the next person can add them as fixtures
rather than rediscover them. The behavioural half is not blind to either: a
report that writes through one still moves a byte or a modified time, and
`_tree_digest` carries both.

**Closes when:** a rule exists that separates a reflective method lookup from an
ordinary constant subscript, or the structural guards state in their own
docstrings that subscript reach is out of scope. The natural owner is whichever
unit next widens `filesystem_mutations`.

**Closed in U34 round 5.** Round 4 covered both spellings and paid exactly the
price this entry predicted: it compared every constant subscript key against
`FILESYSTEM_MUTATIONS` with no receiver read at all, so `counts["rename"] +
counts["unlink"]` in a report was two findings, and `row["truncate"]`,
`LABELS["touch"]` and `ACTIONS["mkdir"]` were one each. The separation this entry
asked for exists now and it is exact rather than heuristic: a type's `__dict__`
and the `vars` of one are the only two spellings that hand back the function
object itself, and `_namespace_owner` reads for those. A mapping is a mapping.
Measured across all 75 files under `src`: zero hits, so the rule still costs
nothing.

---

## R-21. One reflective call shape stays out of reach, and it is named

**Found:** during the U34 round 5 fix, 2026-08-03.

Rule 4's computed half fires when a reflective read's RESULT IS CALLED, and round
5 moved that decision onto the binding table so it covers the indirect spellings:
bound to a name and called, returned and called, stored in a container whose
element is called, used as a decorator, handed to a factory invoked on the spot,
bound at module level and called in another function, and the same through a
conditional, a walrus and an annotated assignment. Eleven shapes, each with a
fixture, each with a mutation row.

One is not covered and will not be by this technique:

```python
map(getattr(path, name), items)
```

The read is handed to a callee that will invoke it, and whether a callee invokes
its argument is a fact about the CALLEE, not about the file being read. A rule
that assumed it would fire on `print(getattr(row, field))`, which is the P7 shape
this whole guard is written around: a guard that reports correct code is a guard
somebody routes around. Naming a set of builtins that invoke their first argument
would cover `map` and `filter` and would be a list nothing keeps true.

What IS read, and the distinction is the whole of it, is the factory invoked in
place: `partial(getattr(p, n))(d)` is covered, because the invocation is written
in this file where the checker can see it.

**Not fixed here**, deliberately. This is an accepted boundary of a guard whose
own docstring already says it is aimed at an ordinary author rather than at an
author who has read it. Recording the shape here means the next reader adds it as
a fixture rather than rediscovering it.

**Closes when:** either a rule exists that reads whether a callee invokes its
argument, which needs cross-module analysis this suite does not do, or the shape
is accepted permanently. The natural owner is whichever unit next widens
`filesystem_mutations`.

---

## R-22. A namespace method with no argument is an unreadable lookup

**Found:** during the U34 round 7 fix, 2026-08-04.

Rule 5's ASKED branch required a first argument to compare, so a method of a
type's attribute mapping that takes none walked past it on ARITY alone.
`vars(Path).copy()` was measured quiet on all four guards and executed to confirm
it hands back a mapping that still holds `write_text`. The branch no longer
requires an argument: no key to read is answered the way an unreadable key is
answered, on the reflection switch, so inside the governed package it is a finding
and everywhere else it is silent.

**The cost is measured rather than asserted, and it is one line.** Across all 75
files under `src` the whole tree contains exactly ONE namespace expression,
`vars(obj)` at `src/cratekit/core/rb_writer.py` line 1840, and exactly one lookup
through it, `state.items()` at line 1843. With the reflection switch ON that call
is now reported as a key this cannot read. Nothing asks it that question today:
`rb_writer` is neither one of the four governed report modules nor on the
allowlist, and the audit runs with the switch off. The four governed modules
contain no `vars` and no `__dict__` at all.

**Not fixed here**, deliberately, because every narrowing available is worse.
Naming the mapping methods that return a mapping is the enumeration this round
exists to stop doing, and gating on the result being called would lose
`vars(Path).popitem()` handed to something else. What is recorded is the one
place in this repository where the rule would fire on correct code if the
governed set widened.

**Closes when:** either `cratekit.core.rb_writer` is proposed as a governed or
admitted module, at which point line 1843 is the thing to decide about, or the
ASKED branch learns to read what a mapping method hands back.

---

## R-23. Two reflection spellings stay quiet, and each needs a refused import

**Found:** during the U34 round 7 fix, 2026-08-04.

Three further spellings reach a writing method through a type's attribute
mapping. One of them is now covered by the propagation rule and its own import is
refused as well:

```python
MappingProxyType(vars(Path))["write_text"](path, decided)   # caught, and types is refused
```

Two are not covered, and neither is live:

```python
itemgetter("write_text")(vars(Path))(path, decided)         # operator.itemgetter is refused
getattr_static(Path, "write_text")(path, decided)           # inspect.getattr_static is refused
```

Both were measured `[]` by `filesystem_mutations` and by `_unnamed_writers`, and
both were measured as REFUSED by `forbidden_imports`: `operator.itemgetter` and
`inspect.getattr_static` are not on `ALLOWED_IMPORTS`, so neither can be written
inside the governed package at all. The structural import guard is what holds
them, not rule 5.

**Not fixed here**, deliberately. Covering `itemgetter` means reading which
argument of an arbitrary callable is the mapping, and covering `getattr_static`
means naming a third reflective reader whose import is already banned. Recording
them means the next reader who widens `ALLOWED_IMPORTS` knows what widening costs.

**Closes when:** either `operator` or `inspect` is proposed for the allowlist, at
which point the corresponding spelling needs a rule and a fixture.

---

## R-24. A container built by a comprehension binds none of its elements

**Found:** during the U34 round 5 verification, restated in round 7, 2026-08-04.

`_elements` reads a list, tuple, set or dict LITERAL and reads nothing else, so a
container built by a comprehension binds no element and a lookup through it
resolves to nothing:

```python
class Row:
    def __init__(self):
        self.mods = [config for _ in range(1)]

    def go(self, cfg):
        self.mods[0].save(cfg)
```

Measured `[]` by all three guards, and identically quiet in round five, so this
is a standing limit rather than a regression either round introduced.

**Not fixed here**, deliberately. A comprehension is a scope with its own binding
table and its element is an expression evaluated once per iteration, so reading
one means resolving the comprehension's own target bindings and then deciding
which iteration's value the subscript names. `MODS = [config]` and `MODS =
[[config]]` are the shapes an ordinary refactor produces and both are covered.

**Closes when:** whichever unit next widens the binding table decides a
comprehension's elements are worth a scope walk of their own.

---

## R-25. A class rebound after its own definition is no longer reachable by name

**Found:** during the U34 round 7 fix, 2026-08-04, and it is a coverage TRADE
rather than a discovery: round six caught this shape and round seven does not.

A class is identified by its DEFINITION SITE now, and its NAME is an ordinary
lexical binding whose value is that identity. That is what lets a parameter
called `Keeper` take the name back, which round six could not do, and what keeps
two factories that each return a `Keeper` apart. It costs one shape, measured
against the real `aging` on both sides:

```python
class Keeper:
    mod = config


Keeper = dataclass(Keeper)          # a decorator applied by hand


def go(cfg):
    Keeper.mod.save(cfg)            # FIRES at round 6, quiet at round 7
```

The `class` statement and the assignment are two bindings of one name that do
not agree, so the name settles to neither. `dataclass` really does hand the same
class back, so the write is real and is missed. Round six kept it only because it
keyed the attribute as flat TEXT and a rebinding of the name was invisible to
that reading, which is the same reading that reported `def go(Keeper)` as a write.

### What is still open, named one spelling at a time

The wording above said "a class rebound after its own definition", which is a
sentence three more spellings fall inside without being measured or named. Round
eight drove all three against the real `aging`, executed each one to confirm
`Keeper.mod is config` at runtime, and they are quiet:

```python
Keeper = type("Keeper", (Keeper,), {})   # a subclass built by hand
Keeper = _wrap(True)(Keeper)             # a decorator factory applied by hand
Keeper = dataclass(Keeper)               # the original, above
```

All three are the same undecidable question and all three are still open. Naming
them is the point: a residual whose wording covers a shape nobody measured is a
residual that cannot be checked.

### What round eight closed, and why those two were never undecidable

Two shapes were inside this finding's wording, or next to it, and neither needed
a decision about what a callee hands back. Both are fixed and both have fixtures.

```python
if flag:                    # only ONE arm runs, so nothing took the name
    class Keeper:
        mod = config
else:
    class Keeper:
        pass


Keeper = Keeper             # both bindings ARE the same class
```

The conditional one was worse than a miss: **this finding said it went quiet
correctly, and that judgement was transferred rather than measured.** The
`AttributeError` reasoning below is true of two `class Keeper` statements in ONE
statement list, where the first is genuinely unreachable. In two arms of a
conditional only one arm runs, there is no `AttributeError`, and the write is
real. The sentence naming that shape as correct is withdrawn.

`Keeper = Keeper` needs no reading of a callee at all: a statement whose right
hand side is the spelling of its own target cannot change what the target is
bound to, whatever it was bound to.

`if flag: Keeper = dataclass(Keeper)` is closed as well, and for a third reason
again: a veto cast inside an arm a run can skip is not a veto that run cast, so
the name is still the class on the path that skipped it. The UNCONDITIONAL
spelling, the one at the top of this finding, is untouched.

### What still goes quiet CORRECTLY

Three neighbouring shapes were measured and are right to be silent: reading
`Keeper.mod` where a later `class Keeper` in the SAME STATEMENT LIST has taken
the name (an `AttributeError` at runtime), reading a factory's local class from
outside the factory (a `NameError`), and reading `Outer.Keeper.mod` where `Outer`
is a parameter.

**Not fixed here**, deliberately, for the three wrapper spellings only. Closing
them means deciding whether an arbitrary callee hands its argument back, which is
the same undecidable question the residual titled "One reflective call shape stays
out of reach, and it is named" declines to answer for `map(getattr(p, n), items)`.
The decorated spelling that an author actually writes, `@dataclass` above the
class, is covered and has a fixture.

**Closes when:** either a bounded reading of "this call returns its argument"
exists, or the three wrapper spellings are accepted permanently. The natural owner
is whichever unit next widens the binding table.
