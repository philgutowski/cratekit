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

**2026-08-02: U24 met the SECOND wall, which is not about databases at all.**
`delete.review` declares an **explicit** gate. R34 says an explicit gate is
answerable only by a separate recorded act and never inline in the invocation
that discovered it, and conformance 3 drives exactly that inline answer and then
requires exit `OK`. So no verb with an explicit gate can pass conformance 3 as
it is written today, whatever database fixture is supplied. Every explicit gate
in the registry belongs to an unlanded verb, so this is a wall in front of
`session.ack`, `session.release`, `restore.run`, `adopt.apply`,
`doctor.repair-paths` and the four routing verbs as well. The fixture closes the
database half; the explicit half needs conformance 3 to answer an explicit gate
the way the product says it must be answered, which is through `run.decide`
against a recorded run. A branch is correcting that assertion.

**2026-08-03: that branch landed and the explicit half is DOWN.** Main's
`3269ab1` rewrote conformance 3, and `delete.review` was built on a throwaway
merge and driven through all four acts: it refuses at its gate, refuses an inline
answer without recording it, takes the answer from a separate `run decide` act
with its actor, and resumes past the gate. It stops one step later at exit 22,
`library-directory-missing`, which is the DATABASE half above, unchanged and
still owned by U27. The paragraph above is left standing rather than rewritten,
because what it recorded was true when it was written and the correction is worth
more beside it than instead of it. The full record is in `docs/HANDOFF.md`,
`tests/_pending.py` and `src/cratekit/deletion/__init__.py`.

**2026-08-02, same evening, CORRECTED.** U24's first pass re-pointed both
deletion verbs to U27 through a `DELETION_CLI_UNIT` constant. That is reverted,
and the reasoning is recorded because the reversal is itself a judgement:

- U27 is a wizard and a doctor. It ships no deletion domain and no destructive
  verb, and on the same evening it proved it could not carry an explicitly gated
  verb by moving `doctor.repair-paths` away for the identical reason.
- U27 **closes in the same wave as U24**, so the re-point moved a contradiction
  from one closing unit to another rather than resolving one. `board.py`'s own
  `contradictions()` reports the same final register state in both merge orders;
  only the moment it fires changes.
- The recorded reason was wrong in one clause. `delete.review` does **not**
  refuse on a missing database: it declares `writes={"files"}`, has no `db_tree`
  or `db_metadata` surface, takes no cloud-sync gate, and names no database
  doctor check. One wall, not two.
- `tombstone.list` never needed to wait and was withheld only because it shared
  a module with its sibling. It declares no gate, so conformance 3's loop over
  its gates runs zero times; it is not destructive, writes no surface, and opens
  no database. It has **landed**, as `cratekit.deletion.tombstone_cli`, which is
  what makes R36's "listable and revocable" a sentence about a person rather
  than about an internal function.

`cratekit.deletion.cli` therefore stays registered against **U24**, holding
`delete.review` alone. U24's other countdown is discharged rather than moved:
the guard asserting that declines and tombstones go through U11's revocable
decision stores is armed and runs unconditionally over `cratekit.deletion`.

**Still open, and it is a decision rather than a defect:** U24 closes with
`cratekit.deletion.cli` outstanding, so `board.py audit` will report the
contradiction on the merge. That is honest, and it is the same shape U19 left
behind. The two ways to settle it are to reopen #24 until `delete.review` lands,
or to land `delete.review` in the first unit after the conformance branch merges
and clear the register entry then. Nothing in the repository can pick between
those.

---

## R-16. Five findings the U24 review accepted, and the reason each stands

**Found:** during the U24 adversarial reviews, 2026-08-02. Every one was
reproduced end to end. Three are fixed here and named so the fix is findable;
two are recorded and open.

**Fixed here, listed because a reader of the review needs to know they are gone:**

1. A prefix rule whose target directory does not exist made every active row
   answer "the file is missing", which left the reference set EMPTY, `complete`
   true, and every removed row proved unreferenced against nothing. Split at the
   ANCHOR: a resolved path whose library root or prefix-rule target is not there
   is `unanchored` and refuses, naming the directory.
2. A declined row reported `handled`, so the watermark passed its sequence and
   revoking the decline could never re-offer the file. `HANDLED` is now `{GONE}`
   alone, and revoking a decline also clears the review item that carried the
   rejection.
3. A verdict travelled to whatever the row resolved to at apply time, so editing
   the volume prefix map between the review and the apply moved a different file
   while the one the person saw stayed on disk. The path the item was offered
   with is now compared before the move.

**Open 1: R38 asserts one volume and the pass can act on N.**
`session.assert_volume_identity` checks `cfg.library.root` against
`cfg.library.volume_id` and nothing else. A prefix rule can send a removed row
onto any other mounted volume, and its file is trashed there with no identity
assertion at all. Verified against a real second volume: the file moved and
landed in that volume's own `.Trashes/501`. The module's own decoy-clone
argument applies verbatim to a backup drive mounted at a map target, which is
exactly the disk whose copies the recovery story depends on.

**Closes when:** configuration can carry a volume identity per prefix rule, and
the pass asserts the identity of every volume it is about to write to rather
than only the one the library root sits on. That is a config shape change, so it
belongs with a unit that owns the config surface.

**Open 2: a permanently non-deletable candidate pins the watermark forever.**
`present` offers only `DELETABLE`, so `COLLIDES_WITH_ACTIVE_ROW`,
`STILL_REFERENCED`, `SIZE_MISMATCH`, `UNRESOLVED` and `UNIDENTIFIABLE` can never
receive a verdict and none of them is handled. Measured over three consecutive
runs with one permanent collision: 2, 3 and 4 candidates while the watermark
stayed where it started. R24 degrades monotonically from the first one onward
and nothing inside the product clears it.

`DECLINED` now joins that set deliberately, which makes this reachable by an
ordinary act rather than only by a rare one. It is the price of R35's
revocability and it is paid knowingly: a declined row short-circuits at the top
of the categoriser, before any path is resolved and before any file is touched,
so the cost is one dictionary lookup per run rather than a filesystem call.

**Closes when:** a person can retire a candidate the software cannot act on,
through the review queue rather than through the watermark, so "I have seen this
and there is nothing to do" is a recorded decision instead of a permanent pin.

**Open 3: a crash between the exclusive create and the rename leaves a
zero-byte file carrying the track's exact name in the Trash.** Verified. The
placeholder is removed on every failure the process survives, including
`BaseException`, so this needs a hard kill or a power loss. Nothing reclaims the
orphan afterwards, and each one consumes one of `MAX_NAME_ATTEMPTS` permanently.
It is worse than it sounds for one reason: the orphan looks exactly like the
file that was supposed to be there.

**Closes when:** the claim carries a marker that says it is a claim rather than
a file, so a later run can tell an interrupted reservation from a real trashed
track and reclaim it. Every shape of that costs a second name or a sidecar, and
choosing one is a decision rather than a repair.

**Open 4: the anchor check asks whether the anchor is THERE, never whether it is
RIGHT.** Added 2026-08-03, after the second review round reproduced it end to
end. One real file, one removed row on it, and one active row on the same file
through a prefix rule whose target EXISTS but is the wrong directory: the
reference set comes back empty, `complete` is true, `assert_complete` passes, the
candidate is `DELETABLE`, and the only copy of the file moves to the Trash. With
the rule correct the same library reports `COLLIDES_WITH_ACTIVE_ROW`. It is the
original defect in full, reachable through a narrower door.

**Why it is not fixed here.** Every rule that catches it needs a threshold on
some missing fraction, and every threshold that catches it also refuses the
ordinary case, which is a prefix rule that legitimately matches a handful of rows
whose files the user moved by hand. The reproduction above has exactly ONE row
through the rule, so any rule with a minimum row count misses it and any rule
without one refuses libraries that are fine. Picking a number there is a product
decision about how much availability to spend, not a repair.

**What is delivered instead** is a signal with no threshold in it.
`ReferenceSet.suspect_anchors` names every anchor that exists, indexed nothing at
all, and had at least one row go missing under it, and the pass logs a WARNING
per anchor naming the directory. That is per ANCHOR rather than per run, which
is what the first version got wrong: it fired only when the whole reference set
was empty, and one unrelated active row resolving anywhere in the library
silenced it. The module docstring now states the limit rather than claiming the
split closed it.

**Closes when:** the pass can tell a rule target that is right from one that is
merely present, which needs something on the volume to identify it, in the shape
`R38`'s volume identity already has for the library root. That is the same
config change Open 1 needs, and the two should land together.

**Open 5: a mapped volume that is not plugged in refuses the WHOLE pass, and
that is an availability regression this round introduced.** A two drive library
with the archive volume deliberately detached: one root row indexed, three
archive rows unanchored, refused, including for candidates that live entirely on
the library root. Deleting the rule does not help, because those rows become
`unmapped` and refuse too. There is no configuration in which a deletion runs
while a mapped volume is detached.

Before this round that library ran, and for root resident candidates its proof
was in fact sound, because a file on an unmounted volume cannot share a
`(dev, ino)` with a file on a mounted one.

**Why the refusal is not scoped to the affected candidates.** `categorize`
already scopes correctly per candidate, returning `UNRESOLVED` rather than
`GONE`, and it was tempting to make `reference_set` do the same. It is not sound.
A dead anchor means the mapping is broken, and the code cannot tell "the rule is
right and the volume is out" from "the rule is wrong", which is Open 4 above. In
the second case the row's file is not on any detached volume; it is somewhere
this machine can reach, possibly under the library root, where it could be
exactly the file a candidate is about to trash. Narrowing the refusal would
assume the rule is correct, which is the assumption the whole anchor split exists
to stop making.

**Reduced rather than closed:** the refusal now carries a step naming the
directory to mount or the rule to correct, so the person meeting it is one act
from a run that works rather than reading "run doctor".

**Closes when:** configuration can record that a mapped target is expected to be
offline, so the user asserts once that those rows live on that volume and the
pass may then scope the refusal to candidates resolving through it. That is a
deliberate assertion by a named person, in the same class as the backup
acknowledgment, and it is config surface rather than a repair.

**Now pinned:** that step was the round 2 remediation and NOTHING asserted it.
`grep '\.steps' tests/test_deletion.py` returned zero hits, so deleting the
expression left the suite green and the person met the wall the step exists to
remove. Both branches are asserted now, the one that names a directory and the
one that must offer none, and the assertion goes through `render.render_cause`
so it covers the step reaching a person rather than only existing.

---

## R-17. Case folding merges two different releases into one identity

**Found:** during the U24 round 3 review, 2026-08-03. Verified in the
interpreter against `cratekit.core.tombstone.fold`.

`fold` calls `str.casefold`, which is the correct Unicode operation for
case-insensitive comparison and which also performs full case folding. Full case
folding is not a bijection: it maps several distinct characters onto one
sequence. Three verified examples, each a pair that folds to one string and
therefore produces ONE `version_identity`:

- `Straße` and `Strasse` both fold to `strasse`
- `Maße` and `MASSE` both fold to `masse`
- `ﬁre`, spelled with the `fi` ligature, and `fire` both fold to `fire`

So two different releases whose titles differ only in one of those ways address
one tombstone, and deleting either reports the other suppressed. That is the
over-suppression direction, which the module's own docstring names as the worse
one: a missed suppression re-acquires something and REPORTS it, while an
over-eager one silently withholds music the user wants.

**Why it is not fixed here.** Every alternative is worse in a way that is not
smaller. `str.lower` is not full case folding: it leaves the Greek final sigma
`ς` alone where `casefold` maps it onto `σ`, so two spellings of one Greek title
would stop matching, and `ς` is a real title character. It would also change the
identity of every record already written, which is decisive on its own and would
be decisive even if the Greek case did not exist. **The Turkish sentence that
used to stand here was wrong and is removed:** `lower` and `casefold` behave
IDENTICALLY for the dotless `ı` and the dotted `İ`, verified in the interpreter,
so Turkish does not distinguish the two operations and never argued for either.
Comparing the unfolded strings as well
would make the identity carry two spellings of one field, so a recorder and a
consulter that normalised differently would stop matching, which is exactly the
property the two-field identity exists to guarantee. There is no folding here
that is both case-insensitive and injective.

**Frequency, stated so the cost is legible:** low. It needs two releases in one
library whose titles differ only by an eszett, a ligature, or the equivalent, and
one of them deleted. It is recorded rather than fixed because the fix costs a
correctness property that is load-bearing every day, to close a collision that is
rare, and that trade should be made deliberately rather than inside a fix round.

**Closes when:** the identity can carry a discriminator that both a recorder and
a consulter always have and that survives folding, or the product decides the Greek
final sigma cost and the re-keying of every record already written are acceptable
and moves to a narrower fold. Either one is a decision about the identity
contract rather than a repair.

---

## R-18. A recorded location that is not an absolute path is excused from the completeness proof, and `locations` cannot tell two kinds apart

**Found:** during the U24 round 3 review, 2026-08-03. **The file is
`src/cratekit/core/locations.py`, which belongs to another unit and is not
rewritten from inside U24.** Half of it is closed in U24's own consumer; this
entry is the half that is not.

`resolve_recorded_path` returns `NOT_A_PATH` for any recorded value that does not
start with `/`, and `reference_set` EXCUSES those rows from the completeness
proof rather than refusing. The excusal is sound for exactly one reason, which
the module states: a streamed track has a pseudo-location rather than a file, so
it cannot be the row that references a file, and counting it against completeness
would refuse the whole feature for any library that has ever streamed anything.

That argument covers rows referencing NO file. It does not cover a row that
references a file perfectly well and is spelled in a form this build does not
decode, and two such shapes exist:

1. **Windows.** Every `C:\` row fails the leading-slash test, so on Windows every
   active row is excused, the reference set comes back EMPTY, `complete` is true,
   and every removed row is proved unreferenced against nothing at all. That is
   the 144-file shape with a different door. `locations` already ships a Windows
   separator seam in `_native_to_url_path`, so the platform is anticipated
   elsewhere in the same module.
2. **A percent-encoded `file://` location.** `locations.location_to_path` is the
   decoder built for exactly the two spellings rekordbox has used, and
   `deletion.library.read_collection` reads `FolderPath` raw and never routes it
   through the decoder, so such a value is excused the same way.

**What U24 closed from inside its own package.** `candidates._unnameable`
inspects the recorded value of every row the resolver excused and splits it. It
recognises exactly two spellings, and the list is exhaustive rather than
illustrative:

- a value matching `^[A-Za-z]:[\\/]`, a drive-letter path;
- a value matching `^file://` case-insensitively, the one URL scheme that names
  a file.

Both are `unnameable` and REFUSE through `assert_complete`. **Everything else
stays `not_a_path` and still runs, and that is a decision rather than an
omission.** `tidal://track/123`, `spotify://track/abc`, `beatport://12345` and
`https://api.tidal.com/v1/tracks/123` all reference NO file, which is the entire
argument for excusing them, so all four are excused and all four are pinned as
such. The round 3 recogniser asked `locations.looks_like_location`, which is
`"://" in value` and therefore true of every one of them, and that turned the
whole destructive verb off for any library holding one streamed row spelled as a
URL, with a remedy no such row can ever satisfy. It is fixed and both directions
are asserted.

**What is still open, and why it is not U24's to close.** The recogniser is a
list of known shapes rather than a decision the resolver makes, so a spelling
nobody has met yet is still excused silently. One is already known and stays
open: a Windows DRIVE-RELATIVE path, `C:Music/Track.flac` with no separator after
the colon, is a real path that names a file relative to the current directory of
drive C, and `_DRIVE_LETTER` requires the separator, so that row is excused. Two
of the three Windows spellings are closed and this is the third. It is left with
the rest of R-18 rather than patched into the regular expression, because
widening the pattern to `^[A-Za-z]:` would also catch a pseudo-location of the
form `x:something`, and choosing between those two on a per-shape basis is
exactly the guessing the resolver should be doing instead.

The real repair is in `locations`: `resolve_recorded_path` should distinguish
"this is not a path" from "this is a path this build cannot name", and
`read_collection` should route recorded values through `location_to_path` so the
decoder that already exists is actually used. Both are edits to another unit's
file, and a deletion pass reaching into the resolver to fix the resolver is how
two decoders end up in one tree, which is the fault that cost 144 files.

**Closes when:** `core.locations` returns the two answers separately and the
library reader decodes through it, at which point U24's consumer drops its
recogniser and reads the resolver's own answer.

---

## R-19. A square-bracketed mix name never matches the provider spelling of the same version

**Found:** during the U24 round 4 review, 2026-08-03. Verified against
`cratekit.deletion.stores` with a recorded tombstone.

`core.tombstone.fold` folds case, surrounding space, internal runs of space and
Unicode composition form, and nothing else. Punctuation stays, so `Track (Live)`
and `Track [Live]` are deliberately two identities. That is the module's stated
conservatism and it is right in general, but it has one consequence worth naming
concretely:

    row:       title "Sun Path [Nightwave Remix]", version "Nightwave Remix"
    identity:  {"artist": "...", "title": "sun path [nightwave remix]"}
    consulted: suppressed_version(artist, "Sun Path (Nightwave Remix)") -> False

The row already carries its mix name, so `version_title` correctly does not
compose a second one, and the brackets survive into the identity. Every provider
this product will ask spells that version with parentheses, so the tombstone is
written, is listable, is revocable, and answers NOT SUPPRESSED to the only
question ever asked of it.

**Direction:** under-suppression. The version is re-acquired and the acquisition
reports what it acquired, which this package calls the milder of the two
failures. The over-suppression direction is what the conservatism buys, and it is
the one that silently withholds music.

**Pre-existing rather than introduced.** Round 3 put it inside U24's stated scope
by making the recorder compose, so it is recorded here rather than left unsaid.

**Why it is not fixed here.** Closing it means folding punctuation, which is a
change to what an identity IS for every recorder and every consulter in the
product, including ones outside deletion, and it would re-key every record
already written. It also cannot be done halfway: normalising `[` to `(` on the
recording side alone gives the recorder and the consulter two spellings of one
rule, which is the exact fault `core.tombstone` exists to prevent.

**Closes when:** the identity contract decides whether bracket style is part of a
version, and both sides move together.

---

## R-20. A SIGKILL between the move and the tombstone still loses the record, and no handler can catch it

**Found:** during the U24 round 4 review, 2026-08-03, as the honest half of the
F2 fix.

`run._record_or_put_it_back` closes the window where a file has reached the Trash
and its tombstone has not been written. Round 3 caught `Exception`, which missed
`KeyboardInterrupt` and the `SystemExit` a SIGTERM handler raises, and the store
write takes a sibling lock, which is the slowest part of the pass and therefore
where a Ctrl-C lands. Both are caught now, matching `trash.move_to_trash`, which
already used `except BaseException` for the identical window.

**What is left is what no in-process code can reach.** A SIGKILL, a power loss,
or a kernel panic between the rename and the store write leaves the file in the
Trash with no tombstone. On the next run the categoriser answers `GONE`, `GONE`
is the one member of `HANDLED`, and the watermark retires the row. R36's "every
completed deletion writes a tombstone" is then false for that row with nothing
recording it.

**What bounds the cost rather than removing it:** the window is one rename plus
one store write per candidate; the file is in the TRASH rather than unlinked, so
it is still the user's file; and what is lost is the suppression rather than the
music, so the version becomes re-acquirable, which is the under-suppression
direction. `Category.GONE`'s docstring states this as the partial guarantee it is
rather than claiming the state is unreachable, which is what it claimed before.

**NARROWED IN ROUND SIX, and the narrowing is worth stating because it changes
what the entry is about.** The sentence above, "on the next run the categoriser
answers `GONE` and the watermark retires the row", is no longer true for the only
path that can reach this state. A file only ever moves after a person CONFIRMS
its removal, and a verdict is durable, so what the next run finds is a confirmed
row whose file is absent with no tombstone. `run._settle_a_confirmed_absence`
now writes the record that deletion owes rather than retiring the row in silence,
so the interrupted deletion COMPLETES on the next run and R36 becomes true for it
again. What is left is the window itself: between the SIGKILL and that next run,
the suppression does not exist, and if the person clears the review item in
between, nothing will ever write it. The durable repair below is unchanged.

**Closes when:** the tombstone is written as a PENDING intent before the rename
and settled after it, so an interrupted deletion is discoverable from the store
rather than from the absence of a file. That is a change to the decision store's
contract, since `core.review` records settled decisions and has no pending state,
and it belongs with whoever owns that contract rather than inside a fix round for
one consumer.

## R-21. The Subtitle vocabulary's false negatives collide, and the ISRC tells a collision from a convergence

**Found:** during the U24 round 5 review, 2026-08-03. **Rewritten during round
six, 2026-08-04, because two of its three claims were wrong and the third was a
number nothing here can measure.**

`tombstone.VERSION_WORDS` decides whether a rekordbox `Subtitle`, which is ID3
`TIT3` and holds anything at all, names a version of the recording. Against 75
genuine version designations a real library holds, 56 read as NOT a version:
`Acappella`, `A Cappella`, `Vocal`, `Refix`, `Rerub`, `Redux`, `Dubplate`,
`Rmx`, `Retouch`, `Reimagined`, `Revisited`, `Intro`, `Outro`, `Beats`,
`Beatapella`, `Tool`, `Nightcore`, `Sped Up`, `Slowed`, `Slowed + Reverb`,
`Mono`, `12 Inch`, `Bonus Track`, `Take 2`, `Unreleased`, `Orchestral`, and
every non-English spelling including `Ao Vivo`, `En Vivo`, `Versão`, `Versión`,
`Mezcla`, `Acústico`, `Livemitschnitt`, `ライブ` and `Живая`. Against 42 ordinary
`TIT3` values, 15 read AS a version, among them `Original Motion Picture
Soundtrack`, `Extended Play`, the labels `Club Sweat` and `Toolroom Club`, and
the artists `Radio Slave`, `Dub Pistols`, `Cut Chemist` and `Mix Master Mike`.

**WHAT THOSE TWO NUMBERS ARE AND WHAT THEY ARE NOT.** The 75 and the 42 are
hand-authored ENUMERATIONS OF EXAMPLES. An error rate over a named list is
checkable by anyone holding the list, and both rates above are. A FREQUENCY
claim over a real column is not, because chosen examples carry no information
about how often each kind occurs, and nothing in this repository samples one:
those spellings appear in exactly two files, both as prose, and there is no
corpus and no sampler. An earlier version of this entry justified a decision
with "roughly half of all subtitled rows, since `TIT3` holds a label or a credit
about as often as it holds a mix name". **That number was asserted, never
measured, and it is deleted rather than restated.** The decision it was offered
in support of may still be right; it is argued below without it.

**The two directions do not cost the same.** A false negative leaves the row
with a bare title, so two versions of one recording collide onto one identity
and deleting either suppresses the other: the user loses a track they did not
delete. A false positive composes an extra parenthetical, so the tombstone is
written and listable and matches no provider spelling: the deletion fails to
stick and the version becomes re-acquirable.

**THE INDISTINGUISHABILITY CLAIM WAS FALSE AS STATED, AND THIS IS THE
CORRECTION.** This entry used to say that telling the feared COLLISION from the
legitimate CONVERGENCE "needs a signal neither the row nor the library carries
today", and that the same shape flags an ordinary duplicate import so no local
check could be built. `RemovedRow.isrc` is read from the `ISRC` column in
`deletion.library.read_collection` and already rides in every tombstone's
payload. It settles all three cases:

* the legitimate convergence, `Strobe` with `Michael Woods` in the remixer
  column against `Strobe (Michael Woods Remix)` with it filled in as well, is
  ONE recording filed twice and carries ONE code;
* the feared collision, two recordings whose designations the vocabulary did not
  believe, both keeping a bare title, is TWO recordings and carries TWO codes;
* the ordinary duplicate import, one row with a label subtitle and one without,
  is one recording imported twice and carries the SAME code, which is the case
  the entry cited as the reason not to build the check and is the case the check
  resolves rather than trips over.

`deletion.stores.ambiguous_versions` runs over the one collection walk
`run.plan` already holds, and `candidates.Category.AMBIGUOUS_VERSION` refuses a
convergence whose rows carry two codes that are both present and different. It
is INCONCLUSIVE where a code is absent, and silence is read as agreement: an
absent code is not evidence against the identity's own claim, and refusing on
silence would refuse most of a library with thin metadata.

**THE EXAMPLE WAS ALSO WRONG AND IS CORRECTED.** This entry said `Title='Sun'`
with `Sun Path` in a version column composes onto the identity of a row
genuinely titled `Sun (Sun Path)`. Measured on the current build, a `Sun Path`
in `RemixerName` composes `sun (sun path remix)`, which does not collide with
`sun (sun path)` at all. The collision it describes arises only for a FLIPPED
`Subtitle` default, where the value is believed and composed verbatim, and it
should have been stated as a consequence of the flip rather than as a property
of the code as it stands.

**THE BELIEF DEFAULT IS STILL NOT FLIPPED, AND HERE IS THE ARGUMENT WITH THE
DISCRIMINATOR IN HAND.** The reason is no longer "nothing local can tell the two
apart", which is now false.

1. **The discriminator attacks the worse direction directly, so keeping the
   default costs less than it did.** What the false negatives cause is the
   collision, which is over-suppression and the direction that costs the user
   music. That is exactly what `AMBIGUOUS_VERSION` refuses. The remaining cost of
   a false negative is a row reported rather than deleted, which is a refusal a
   person can see and act on.
2. **Flipping trades a measured rate for an unmeasured one.** The false-positive
   rate over the named list is 15 of 42; how often a real `TIT3` holds a label
   rather than a mix name is the number this entry used to assert and cannot
   measure. Flipping is a bet on that number, and there is nothing here to
   settle it with.
3. **The discriminator does not cover the shape a flip would introduce.** Its
   evidence is the removed half of the collection walk. The row a composed title
   would collide with, `Sun (Sun Path)`, can be an ACTIVE row, and the active
   half is read as `trees.ContentRow`, whose `__dataclass_fields__` are exactly
   `content_id`, `recorded` and `deleted`, with no artist, title or code at all;
   `run.plan` feeds `stores.ambiguous_versions(seen.removed)` and nothing else.
   So a flip would introduce a collision class the check STRUCTURALLY cannot see,
   which is the opposite of the position it improves. **An earlier version of
   this point said such a row is "very often" active. That is a frequency over a
   real library, unmeasured and unmeasurable from this repository, which is the
   standard applied to "roughly half" sixty lines above, and it is deleted rather
   than restated.** The structure carries the argument without it: a class the
   check cannot see at all is a hole whatever its size.

**Closes when:** either a real `TIT3` column is sampled, so the frequency the
flip depends on is measured rather than asserted, or the active half of the walk
carries enough identity for the discriminator to answer for an active row, at
which point the flip and the check cover the same ground and the trade can be
made on numbers.

## R-24. A designation filed in the remixer column is spelled unmatchably, deliberately

**Found:** during the U24 round 6 fix, 2026-08-04. **Rewritten during round
seven, 2026-08-04, because the rule it described was measurably worse than what
it replaced and because its own safety claim was false.**

`RemixerName` is an association proxy over `RemixerID` into `djmdArtist`, so it
holds an ARTIST NAME, and composing it needs the provider's spelling, `Strobe
(Michael Woods Remix)` rather than `Strobe (Michael Woods)`. The append is
skipped only when it would say `Remix` twice, which is
`tombstone.already_spelled_as_a_remix`, and that function consults no vocabulary
at all.

**WHY THE VOCABULARY WAS TAKEN OUT, MEASURED.** Two rounds asked a word list to
classify this column: round five asked whether a version word appeared anywhere,
round six asked whether it appeared last. Over 65 values in three classes, 40
genuine designations and 25 artist names, misses were 25 of 25 on the artist
classes for round five and 15 of 25 for round six. The shipped rule misses NONE
of the 25 and misses 38 of the 40 designations. The totals, 33 and 35 against 38,
are reported and are not the criterion: a total over a hand-authored set is a
weighted average whose weights are how often this column holds a designation
rather than an artist name, which is the same unmeasurable frequency R-21 deleted
a claim about.

**THE ROUND SIX SAFETY CLAIM WAS FALSE AND THAT IS WHY THE CLASSES ARE NOT
INTERCHANGEABLE.** That entry said both error directions are under-suppression,
because "composing only ever adds a bracket". Composing does, but leaving a value
VERBATIM does not: `Strobe` with `The Cut` in `RemixerName`, an artist, and
`Strobe` with `The Cut` in `Subtitle`, a designation, both composed `strobe (the
cut)`. One identity, two versions, and deleting either suppresses the other,
which is over-suppression. So an error on an artist name has both directions and
an error on a designation has only the milder one, and the right rule is the one
that never errs on an artist name whatever it costs on designations.

**WHAT IS STILL SPELLED WRONGLY, WHICH IS THE RESIDUAL.** A column genuinely
holding a designation that does not end in `Remix`, `Extended Mix` or `Michael
Woods Refix`, gets `Remix` appended and composes `(Extended Mix Remix)`. That is
38 of the 40 designations in the value set. It is the UNDER-suppression
direction: the tombstone matches no provider spelling, so the deletion fails to
stick and the version is re-acquirable. The second residual is an artist whose
name's last word is literally `Remix`, which would be left verbatim; none is
known and none is in the value set.

**Closes when:** the recorder can ask what a provider actually spells for this
version rather than deriving it, which needs a provider lookup at deletion time
and is a dependency this pass deliberately does not have (R36: a deletion is a
fact about this disk and nothing here touches a streaming service).

## R-26. An anchor with no active rows through it can still settle a removal off an empty directory

**Found:** during the U24 round 7 fix, 2026-08-04, while closing the empty mount
point defect, and recorded rather than papered over.

`candidates.categorize` answers `GONE` for a removed row whose file will not stat
as long as the anchor DIRECTORY exists, and an empty directory standing where a
volume mounts passes that. `run._the_anchor_proved_nothing` now refuses to settle
or retire such a row when `references.suspect_anchors` names its anchor, which is
an anchor that exists, indexed nothing, and had at least one ACTIVE row go
missing under it.

**The signal needs an active row to exist.** `missing_under` is only populated
from the active half of the walk, so an anchor with NO active rows through it is
never suspect, and a mapped volume holding only removed rows still settles off an
empty mount point. On the library this pass is built for that case does not
arise, since the volume carries thousands of active rows, but it is not excluded
by anything in the code.

**Why it is not closed here.** With no active row through that anchor there is no
evidence either way, and the only local alternative is a threshold over how many
REMOVED rows look gone at once. Every threshold that catches an unmounted volume
also catches a person who deleted an album folder in the Finder, which is the
all-or-nothing rule `suspect_anchors` was built to replace.

**Closes when:** the pass can ask the operating system whether a path is a mount
point and whether the volume mounted there is the one the prefix rule names,
which is the same volume identity question `core.preflight` already answers for
the library root and would need extending to every mapped target.

## R-25. The active half of the collection walk carries no identity, so nothing can be proved about an active row's version

**Found:** during the U24 round 6 fix, 2026-08-04, while building the ISRC
discriminator.

`library.read_collection` returns the active rows as `write.trees.ContentRow`,
which carries a content id, a recorded path and a deleted flag. It carries no
artist, no title, no version column and no ISRC. Every question this pass asks
about an ACTIVE row is therefore a question about its file: is this the same
inode, is it the same size, does a playlist point at it.

That is enough for everything R37 asks for and it is not enough for one thing
the tombstone side wants. `deletion.stores.ambiguous_versions` can see that two
REMOVED rows compose onto one identity and carry two different ISRCs, so it can
refuse that deletion. It cannot see that a removed row composes onto the identity
of an ACTIVE row, which is the shape "The Subtitle vocabulary's false negatives
collide, and the ISRC tells a collision from a convergence" names as the reason
its belief default is not flipped: the user keeps one version and deletes the
other, and it is the kept one whose identity the tombstone would collide with.

**What bounds it today.** The vocabulary is a whitelist, so a `Subtitle` is
believed only when it reads as a version, and the composed titles it produces are
mix names rather than arbitrary text. The collision needs a composed title that
another row holds bare, which is a coincidence rather than a routine shape while
the default stands. Flipping the default is what would make it routine, and that
is why the flip waits on this.

**Closes when:** the active half carries enough of an identity for
`ambiguous_versions` to answer for an active row. That is a widening of
`ContentRow`, which the routing pass also reads, so it belongs with whoever owns
that type rather than inside a deletion fix round.

## Note. Round 5's mutation evidence, and the shared scratch directory it was measured through

**Recorded:** 2026-08-03, because a measurement whose conditions are not written
down is a number rather than evidence.

Eight parallel agents were given one scratch directory. Another unit's mutation
driver overwrote this unit's driver and its restore snapshot at 22:23, which is
how it was noticed: a batch launched at that moment ran the foreign driver
instead. Everything from that point used a private driver under a scratch
directory belonging to this unit alone.

**What was checked, and what was found.** The worktree was compared against the
git object database rather than against any snapshot, since a snapshot that has
been overwritten certifies itself. No leaked mutation was present. Commit
`b4540ee` was inspected line by line for content this unit did not write,
including every line it REMOVES, which is where a staged mutation would show; the
one file it touches that other units also touch, `src/cratekit/core/cause.py`,
carries a single appended reason slug and nothing else.

**Every row measured before the switch was re-measured afterwards** and all
eleven reproduced their counts exactly: S1-A1 1, S1-A2 1, S1-A3 2, S1-B 1, S1-C1
1, S1-C2 1, S1-E 1, X08 1, X09a 1, X09b 2, G09 1. Two rows from that window,
R08 and C05, had already been re-measured against changed code and are reported
in the stage one commit under their final form.

**One separate defect this exposed, worth keeping.** The driver used a full-suite
run per row and one batch was killed by a timeout partway through, which left a
mutation applied in the tree. It was caught by comparing against the snapshot and
restored, but the failure mode is real: a mutation driver that is interrupted
leaves the code it was measuring in place. Any future round should checkpoint per
row, as this one's did after the incident, and verify the tree against git rather
than against its own snapshot before trusting the next number.
