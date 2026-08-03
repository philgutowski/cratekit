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

**Diagnosed 2026-08-02, and most of the wall was a defect in the assertion.**
The paragraph above states the wall as one fact. It was three, and two of them
were never true of the product.

**Defect one: an explicit gate.** `test_conformance_3` drove every gate the same
way: refuse, hand the answer back
on `-d`, assert `OK`. `Gates.require` refuses an inline answer for an **explicit**
gate whenever nothing is recorded against the run, and `cli.run` mints a fresh run
whenever `--run` is absent, so `recorded` is `None` on every fresh invocation and
the refusal is unconditional. Driven through the real dispatcher, an explicitly
gated verb returns `10 DECISION_REQUIRED` to the first drive AND to the second,
and returns `0 OK` only after the decision is recorded and the run is resumed with
`--run`. Assertion 3 therefore asserted that an explicit gate must **not** be
honoured, which is the precise inverse of R34, and it had done so since it was
written. It was never caught because no landed entry declares an explicit gate:
fifteen do, and all fifteen are planned, so the branch was never driven.

**Defect two: a verb with two gates, no explicit flag required.** The assertion
drove once per DECLARED gate and answered only that one gate, on a fresh run
every time. A verb carrying two gates therefore refused at whichever gate the
current drive had not answered, so both iterations exited `DECISION_REQUIRED`
and the entry could never pass. Reproduced against a two-gate synthetic with
both gates plain: the old assertion returns `10` for the second drive on both
iterations. `restore.run`, `name.apply`, `route.inbox` and `adopt.apply` all
carry two gates and were blocked by this independently of R34.

The cost was paid by four units in one wave, each concluding independently that
its CLI verb "cannot land" and parking the obligation on a different unit, which
produced five incompatible workarounds for a phantom.

**Fixed** on `fix/conformance-3-and-soft-delete-reader`. Assertion 3 now answers
gates CUMULATIVELY, one drive per gate reached rather than one per gate declared,
which is the single change that covers both defects. An ordinary gate accumulates
a flag and keeps the one-command path unchanged. An explicit gate takes R34's two
acts: the first drive refuses, an inline answer refuses AGAIN and records nothing,
and `OK` comes only after `run decide` writes the decision with its actor and the
verb resumes under `--run`. A second gate is then reached with the first still
answered, in both orderings.

All three branches ship DRIVEN against synthetic entries, the real `profile.set`
with its gate promoted and with a second gate added, so they are proved before the
first real one arrives rather than by the unit that lands it. That is precisely
how both defects survived: the code path existed and nothing exercised it.

A gate an entry declares but never reaches is no longer asserted about, because
`write.cloudsync.unreadable` fires only when the sync state is unreadable and
demanding a refusal the environment cannot produce would have been a third wall
of the same kind.

**The register bookkeeping done in response should be reverted at merge.** Three
places now carry reasoning that is false: the `ROUTING_CLI_UNIT` comment in
`src/cratekit/cli/registry.py`, the `cratekit.write.routing_cli` entry in
`tests/_pending.py`, and
`test_the_routing_verbs_name_a_unit_that_can_actually_land_them` in
`tests/test_deferred_routing.py`. All three say U19 could not land the module
because a gated verb cannot exit `OK`, and the gate half of that is the phantom.
Whether U20 should still own the routing CLI is a separate question with its own
good answer, so this is a correction to the stated reason and not automatically a
re-point. Left untouched here because those files belong to landed units and to
branches in flight, and rewriting another unit's reasoning inside a fix branch is
how one correction becomes four merge conflicts.

**What is left of the wall is real and smaller.** A verb that writes the database
still has to succeed to exit `OK`, and it cannot succeed on a machine with no
database. That half stands, and it is what the closing condition below addresses.
A verb with an explicit gate and no database write, `session.ack` being the
clearest, is landable today.

**Closes when:** conformance 3 can be satisfied against a disposable database
fixture, on the `CRATEKIT_TEST_DB` convention that already SUBSTITUTES rather
than skips, so the battery runs either way and a supplied fixture strengthens it.
The natural owner is U27, which lands doctor and is the unit that makes a machine
ready.

---

## R-14. Analysis-file paths are share-relative, and the wrong join finds nothing

**Found:** during the DJ_tools staging repair, 2026-08-02. Issue #52.

A rekordbox library on an external volume has **two** directory trees ending in
`PIONEER/USBANLZ`, and only one is the analysis store. The one under
`PIONEER/Master/share/` is UUID-keyed, holds the beat grids, and every local row
resolves into it. The one at the volume root is the USB-export cache, a different
key shape, regenerable, and **zero rows resolve into it**.

`djmdContent.AnalysisDataPath` is stored **share-relative**. Joining it to the
library root resolves zero of 10,070 rows and reads as "the analysis files are
missing", which is a measurement artifact rather than a defect.

This matters to U23, which adopts an existing library and must resolve analysis
data to judge what it is adopting; to U32, because a database restored without its
analysis tree brings back rows without their grids and the failure is silent; and
to `modules/tools/backup.py`, which documents the database path and says nothing
about the share.

It cost the source repository twice: once carried as a false open item, and once as
a grid-rollback step that named the wrong tree and would have protected regenerable
device output while leaving every grid it existed for uncovered.

**Not fixed here** because U23 and U32 are unwritten. This is a constraint to write
them against, not a patch to apply after.

**Closes when:** every place that resolves, backs up or verifies analysis data joins
to the share, and a test pins the join so the wrong one cannot come back.

---

## R-15. Guard whitelists assert what is forbidden, never what is permitted

**Found:** during the DJ_tools staging repair, 2026-08-02. Issue #53.

The guard tests assert what must **not** be whitelisted, and that every entry is a
real table in the binding. Nothing asserts **exact membership**.

Those are different questions, and only exact membership catches a widening. Adding
a table or a column is a two-word diff that raises the ceiling for every writer in
the repository, present and future, and it passes a green suite as long as it is not
one of the specifically-named forbidden entries. Verified in the source repository:
sneaking one column into the content allow-list turned two tests red where the same
edit had previously passed twenty-four green.

The bookkeeping set needs this most, and for a subtler reason. Entries there are
IGNORED when judging a modification, so an addition does not grant a write, it stops
the guard from looking at one. Quieter than widening the allow-list, and worse,
because the resulting session passes the guard rather than being permitted by it.

Related and cheap: `Rekordbox6Database(db_dir=...)` does not open the database in
that directory, and with `path` unset it falls back to the configured live library.
`core/rb_writer.py` passes `path=` correctly and is the only such call today; an AST
assertion would keep it that way. The general form is worth stating in the guard's
own terms: refusing the live path as an argument is not the same as not reading it.

**Not fixed here** because it is test work in a module three waves are queued behind,
and the pins are worth writing deliberately rather than alongside something else.

**Closes when:** the permitted-tables set, the content-column allow-list and the
bookkeeping set each carry an exact-membership assertion, each verified to fail on a
deliberate widening rather than merely existing.

---

## R-18. Two records of the pending work, and nothing compared them

**Found:** 2026-08-02, on `fix/conformance-3-and-soft-delete-reader`, from a
third and fourth adversarial review of this wave. **Needs its own issue.**

The repository keeps **two** registers of work a unit still owes. `tests/_pending.py`
holds guards waiting for the module they govern. `planned_in` on a
`cratekit.cli.registry` entry holds a verb waiting for its own. Both are the same
promise in different files, and until this branch, `scripts/board.py` read only
the first.

Three consequences, all live.

**Seven verbs are owed by closed units and nothing has ever said so.** U8, U15 and
U35 are closed and still carry `planned_in` markers between them. `board.py audit`
audits units against a register that never mentioned those verbs, so the marker is
invisible to the one mechanism that exists to expire it.

**The countdown that should catch it cannot fire for half the tree.**
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker` probed with
`find_spec` inside `except ModuleNotFoundError`, and `find_spec` raises when an
ANCESTOR package is missing rather than the module. Both were read as "not
present". Fixed here: `_pending.module_state` reports `present`, `absent` or
`ancestor-missing`, walks ancestors top down, and no longer swallows a
`ModuleNotFoundError` raised from inside an ancestor that does exist, which was a
defect in our own tree reported as a countdown ticking quietly.

**Measured, and the distinction is not a rule.** Seventeen planned verb modules
are `ancestor-missing` and almost all belong to units that have not started, so
asserting against that state would fire on correct pending work. The two records
were compared instead, and they disagree exactly once: U23's package is
`cratekit.adopt` in the register and `cratekit.adoption` in the registry.
`test_the_two_registers_agree_on_each_unit_s_package_name` pins that one case as
exact membership, so U23 resolving it turns the test red and forces the deletion.

**Fixed far enough to be safe on this branch:** `board.py` gained `planned_units`,
`owed_by_unit` and a network-free `closing` check that refuses a `Closes #n`
trailer while either register still owes Un, wired as a `commit-msg` hook and
called by `audit`. `contradictions()` now reads both registers. Rule A refuses a
register key naming a command-line module no verb declares, because such a key can
never be satisfied and its unit's close becomes a permanent exit 2.

**Left open, and this is what needs the issue.** Nothing decides WHICH record is
right when they disagree, and this branch deliberately did not pick for U23. The
seven markers on closed units are not repaired here either, because re-pointing
another unit's verbs is that unit's judgement and not a side effect of a fix
branch. Four closing contradictions are queued in this wave right now and the new
check will refuse all four at their merge, which is the intended outcome and will
need somebody to answer each one.

**Closes when:** the markers on U8, U15 and U35 are re-pointed or landed, U23's
package name is settled in both records, and the `closing` check has refused and
been answered at least once so the refusal path is known to be usable rather than
merely correct.
