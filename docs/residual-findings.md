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

**All three were still open, and all three are CLOSED 2026-08-02, by U32.** Each
was registered in `tests/_pending.py` against `cratekit.core.restore` so it was a
countdown rather than a note, and clearing that entry is what armed the guard.
What closed each is recorded beneath it. One residue survives, and it is the
wiring rather than the mechanism: the two restore verbs still have no
command-line module, so the composition in item 1 is proven at the seam and is
not yet called by anything a user can type. That obligation moved to
`cratekit.session.restore_cli` in the same register, with the reasoning for
re-pointing it left legible.

1. **The plan and the run each take the lock and give it back.** With `gates`
   left at its default, `plan_restore` enters the guard, builds the plan, and
   releases on the way out; `run_restore` then enters it again. A second process
   can pass the same gates and commit in that window, and the run then copies a
   snapshot over a commit its plan was built before. The `GateGuard` seam exists
   so a caller can hold ONE session across both halves, and the verb must: a plan
   is a value and cannot own a live context manager, so the composition is the
   caller's to make.

   **Closed by** `restore.recovery_session`, which enters the gates once and
   yields a `Held` whose `guard` is a pass-through the modules layer passes in as
   `gates`. Holding the value is not the same as being inside the block, so
   `restore.plan` and `restore.run` both assert that this process still holds the
   lock at the moment they are called rather than merely that it once did.
2. **The record outlives the restore that answers it.** The session log is
   declared `SURVIVES_ROLLBACK`, deliberately, because rolling it back would
   erase the record of which sessions are restorable. So a
   `committed-unverified` record is still there after the restore that resolves
   it, and the verb has to call `session.resolve_unverified_session` on success.
   The function landed with U8; naming it in the verb's success path is U32's.

   **Closed by** a `resolve-session` step in the restore's own ordered plan, one
   per condemning record, placed last because it is the claim that the work is
   done. Every such record is answered rather than only the one being restored
   to: the library now holds a capture that passed its integrity check, so no
   earlier unverified commit condemns these bytes either.
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

   **Closed by** `restore.bare_metal_session`, which substitutes one gate at a
   time and says what each substitute is worth. The volume assertion becomes two:
   that the configured library is genuinely UNREACHABLE, refusing on "mounted
   elsewhere" and on "this platform cannot say" because neither is the same
   question; and that the target is a real filesystem rather than the empty
   folder an unmounted volume leaves behind at its own mount point, which is the
   failure that would otherwise write a whole library onto the internal disk. The
   lock becomes an installation-scoped one, and nothing is lost, because with the
   library gone there is no shared volume for two machines to contend over. The
   acknowledgment becomes an explicit decision by a derived actor at a
   controlling terminal, and that substitute is WEAKER than the gate it replaces:
   the recorded acknowledgment R34 asks for lives on the volume that died. That
   is stated rather than papered over. The advice not to move the volume
   assertion onto the target was followed: the target assertions are additional
   to the unreachability assertion, not a replacement for it.

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
**The three parts named, and which of them survived.** The paragraph this entry
opened with states the wall as one fact. It is three, and separating them
matters, because a verb held by none of them was parked behind it once already:

1. the **explicit-gate refusal**, which is conformance 3's requirement that a
   landed gated verb refuse and then proceed;
2. the **one-gate-per-drive shape**, which is what makes the first part
   drivable at all;
3. the **database**, which is the part that cannot be satisfied where no
   rekordbox database exists.

Parts 1 and 2 are the defect diagnosed above, and they are fixed on `main` as of
the conformance 3 merge. Part 3 stands and is the whole of what remains. A verb
that declares no gate and writes nothing is behind none of the three:
conformance 3's loop body never executes for it, conformance 5 and 6 filter it
out, and conformance 1 and 8 already assert over every entry landed or not.

**U36 hit part of this wall, and a correction is recorded here because the first
answer was wrong, 2026-08-02.** `converge` and `rebuild` were declared against
one module, `cratekit.write.converge_cli`, with `planned_in="U36"`. Only
`rebuild` belongs behind the wall: it writes `db_tree` and is destructive. Its
sibling `converge` declares no gate, writes nothing and is destructive of
nothing, and it was parked purely because both verbs named ONE module and the
countdown in `tests/_pending.py` keys on the module rather than on the verb.
Parking it parked the remedy: both of U36's refusals name `converge` as
remediation step one, and it is exactly what a person reaches for when a tree is
already refusing every write.

The correction: U36 split the modules and landed `cratekit.cli.converge`, with
its conformance properties asserted like any other landed verb. Only
`cratekit.cli.rebuild` stays behind the wall, registered in `tests/_pending.py`
against **U20** through a `REBUILD_CLI_UNIT` constant, and backed by a real
`requires(...)` guard rather than by prose. That brings the count waiting on the
wall to five verbs rather than six.

**A false claim made in this document on 2026-08-02 is withdrawn.** The
paragraph that stood here said "U36's brief names no CLI module it could have
landed". Issue #36's Files line reads `src/cratekit/write/rebuild.py`,
**`src/cratekit/cli/rebuild.py`**, `tests/test_rebuild.py`. The brief names a CLI
module explicitly. The sentence was true of U19, whose file list genuinely
contained none, and it was reused for U36 where the fact does not hold, in the
document a human adjudicates from.

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

## R-16. What the U36 and U32 merge owes, verified rather than inferred

**Found:** during U36's first review round, 2026-08-02, by running the merge.

**Numbered R-14 on the U36 branch and renumbered to R-16 when U36 merged**, on
the standing rule that residual numbers collide across branches and renumber
sequentially in merge order. U32's R-21 refers to this entry by its branch
number. They are the same entry.

Both branches were merged in a scratch clone and the whole suite was run against
the result. Six tests fail, all of them in `tests/test_restore.py`, and every one
is a merge-resolution item rather than a defect in either branch. Recorded here
so whoever merges is not discovering them one at a time.

1. **`record_cutover` needs `source`.** Four failures. U36 made `source` a
   required keyword-only argument with no default, because the only value it
   could pick is `TAXONOMY` and picking it writes "yes, this tree can be
   rebuilt" about a tree nobody checked into a one-way record. U32 added a
   fixture call afterwards. **Add `source=DerivationSource.TAXONOMY` to
   `_cut_over` in `tests/test_restore.py`.**
2. **`test_the_rebuild_verb_has_no_way_to_declare_a_recovery_intent`.** U32's
   own test, whose docstring says "if that ever changes this reasoning should be
   revisited rather than inherited". It changed: `write_tree_membership` now
   takes an `intent`, so the rebuild is no longer refused by the latch whose
   refusal names it. **Delete or invert that test.**
3. **`test_every_coupled_entry_declares_what_leaves_the_coupled_set`.** U36's
   `tree_convergence` entry cannot name `RollbackEffect` on a branch where U32's
   enum does not exist. **Add `rollback_effects=(RollbackEffect.NONE,)`;** the
   comment at the entry in `config.py` gives the line and the argument.
4. **`test_a_restore_predating_a_cutover_marks_that_tree_unconverged`** asserts
   `reconcile.unconverged_trees(cfg) == ("routing",)`. That is stale against
   U32's own hand-over: `restore._hand_tree_shortness_over` routes the fact to
   `convergence.mark_unconverged` whenever that module is present, and it now is.
   **Assert `convergence.read(cfg).blocking_trees()` instead.** Patched that way
   in the scratch merge, the handoff passes, which is the positive confirmation
   that ownership of tree shortness now sits in one module.

**Also in the merge, and not a test failure**, so nothing will catch it: U32
re-keyed its pending entry to `cratekit.write.tree_rebuild` on the belief that
U36 would ship that filename. U36 ships `src/cratekit/write/rebuild.py`, which is
what issue #36's Files line names, so U32's key can never resolve and its
countdown sits switched off while the suite stays green. **Re-key it to
`cratekit.write.rebuild` in `tests/_pending.py` and `tests/test_pending_units.py`.**
The entry then fires, and discharging it is the commit that removes the fallback
branch in `restore._hand_tree_shortness_over` and the
`reconcile.Kind.UNCONVERGED_TREE` path behind it.

**Re-verified after U36's second review round, 2026-08-02.** The merge was run
again. With items 1 and 4 applied the merged suite is 3390 tests and two
failures, both of them items 2 and 3 above; with all four applied it is 3389
tests, 0 failures, 18 skips. Item 4's fix is the positive confirmation that
ownership of tree shortness now sits in one module: `restore` hands the trees to
`convergence.mark_unconverged` and `reconcile.unconverged_trees` is correctly
empty.

**Closes when:** both branches are on `main` and the six items above are
resolved.

---

## R-17. Two convergence flags that are set correctly and never cleared

**Found:** during U36's second review round, 2026-08-02.

Both are fail-closed, both are inert today, and both accumulate. Recorded rather
than fixed because each needs a surface that has not landed.

**A native tree no caller ever writes to.** `convergence.native_trees` unions the
caller's registry with the one on disk, which is what makes "every
database-native tree is marked" true rather than conditional on what the caller
passed. The consequence is that a tree recorded native on disk, which no workflow
ever names, is marked unconverged by the detection and nothing will ever run a
rebuild for it. Nothing is written against it, so nothing is damaged, but its
flag stands forever. The alternative, marking only what the caller passed, is the
defect the union exists to close, so the union stays. **Closes when** a verb can
enumerate governed trees and rebuild each in turn, which is U20's surface.

**A tree whose tracks were retagged out of a bucket.** The rebuild is additive by
design: a membership somebody made by hand is their data, and deleting it would
be the one operation in this product that destroys work nobody can get back. So
rows the declaration no longer places are reported `UNEXPECTED` and left alone,
`after.converged` is never True, and a flagged tree can never be cleared by
rebuilding. That is intended and R39 names the escape: an explicit, logged
operator disposition scoped to one tree.

**The escape exists in the engine and has no surface on this branch.**
`convergence.clear_unconverged(cfg, tree_id, differences=..., disposition=...)`
takes it and refuses an empty actor, so the mechanism is complete and tested. The
command-line half rides on `cratekit.cli.rebuild`, which is behind the
conformance wall against U20 and is registered in `tests/_pending.py` with that
obligation attached. **Until U20 lands, a library in this state has no
supported exit**, which is acceptable only because no tree has cut over yet:
`tree_registry` starts every tree on the XML bridge and the cutover verb is U20's
too, so the first library that can reach this state is one U20 created.

**Closes when:** U20 ships the disposition surface, at which point both entries
are answerable by a person rather than only by the engine.

---

## R-19. R30's second sentence is computed and never reported

**Found:** during the U32 adversarial review, 2026-08-02. Confirmed against
`src/` before it was recorded.

**Numbered R-19 rather than R-14, and the merge left it there. R-18 IS A
DELIBERATE GAP.** When this entry was written, `main` defined R-14 and R-15,
U27's branch was renumbering its own to R-16, and U16's fix round was adding
R-17. Both of those predictions were wrong: **U36 took R-16 and R-17 when it
merged**, and `main` ended at R-17. U32 brought five entries numbered R-19
through R-23, so the merged file runs R-1 to R-17 and then R-19 onward with
nothing at R-18.

**The gap was kept rather than closed, and the reason is the paragraph below.**
Closing it means renumbering five headings, and every citation of each of them
has to move with it, in prose, in source comments and in docstrings. That repoint
was missed once already at the U36 merge and was caught only by eye. A gap in a
number sequence is visible and harmless; a citation pointing at the wrong finding
is invisible and wrong. Nothing in this repository derives meaning from these
numbers being contiguous.

**And the citations are not all inside this repository's source.**
`docs/wave-state-2026-08-04.md` names "U32's R-21" four times while it is
tracking several branches at once, each carrying its own R-numbers. Keeping these
five where they are is what leaves those four sentences true. Renumbering would
have made them silently name somebody else's finding, which is the same failure
one layer out from the one this entry is about.

That is exactly why `core/restore.py` cites these findings by TITLE rather than
by number, and why `tests/test_restore.py` asserts the titles still resolve. A
number written into source survives a renumber by pointing at somebody else's
finding: the citation still reads correctly and is silently false, which is the
failure already caught once here, where `core/convergence.py` said "See R-15" and
R-15 on the merged tree named a different entry. This file is one another branch
appends to, and two entries sharing a number is the shape where one of them
silently becomes unreadable.

**The unmet sentence, verbatim from R30:** *"the capture store does not sit on
the same filesystem as the database, so that one volume failure cannot take both
the library and every undo for it."*

**Current state, with file and line.**
`core/restore.py:shares_the_database_volume` computes the answer, comparing on
the filesystem identifier rather than on path prefixes, and
`core/restore.py:RetentionPlan.shares_the_database_volume` carries it on every
retention plan. Nothing in `src/` renders it. There is no command-line surface
for retention, no doctor check that reads it, and no session-time warning. The
honest status is **computed, not reported**, and the unit's own prose said
"REPORTED", which overstates what landed.

**Why it is not enforced, and why that decision stands.** The reviewer upheld the
call to report rather than refuse, and the argument is worth keeping because it
is the reason this cannot simply be closed with a guard. The containment rule
pulls `db_path` inside `library.root`, because an atomic commit cannot span
filesystems. So "put captures on another volume" and "keep the database inside
the library root" cannot both be refusals: the preferred install satisfies the
second and therefore violates the first, and a guard that fires on the product's
own default install is a guard people route around. The honest fix is a second
capture location the user chooses, which is configuration U32 did not add.

**The exposure, in one sentence.** On the default install one volume failure
takes the library, the database and every capture together, so the KTD21b undo
does not survive the single failure it is most likely to meet.

**What closes it.** A rendered report, in all three of the places a person would
meet it: `doctor` names it as a check with the two paths and the shared
filesystem identifier; the retention verb prints it beside the plan it is already
carrying it on; and a first destructive session in a new install says it once.
Not a fourth mechanism: `RetentionPlan` already carries the value, so every one
of those is a read.

**Owner: U27.** It lands doctor, it already owns the operator-facing surface, and
it already carries this unit's `cratekit.session.restore_cli` obligation, which
is the surface the retention verb would live on. Recorded here with a number
rather than left in a `core/restore.py` docstring for the reason this unit argues
twice in `tests/_pending.py` about somebody else's markers: an obligation carried
by a marker on a closing unit is owned by nobody the moment that unit closes, and
`scripts/board.py` reads the register and this file, not docstrings.

**What must NOT close it.**

1. **Turning it into a refusal.** That is the version this unit already
   considered and rejected, on the containment argument above. A refusal on the
   default install is worse than the gap, because it is switched off once and
   then never seen again.
2. **Asking once at setup.** A setup-time prompt is answered by somebody who has
   not yet lost a drive, and it is answered once, on a machine whose layout then
   changes. The value is cheap to recompute on every run precisely because it is
   derived from the filesystem rather than from a recorded answer, and a recorded
   answer would go stale the first time somebody moves their library.

---

## R-20. Closing the bare-metal bypass removed the bare-metal write path

**Found:** by the independent verification of U32's first fix round, 2026-08-02.
Recorded here rather than fixed, because the fix is a feature and the bypass had
to close tonight.

**What R-8's third item asked for.** Every gate KTD21 publishes is library-scoped
on purpose, so all three sit on the disk that died and the ordinary restore
refuses by naming a drive that no longer exists. U32 answered that with
`restore.bare_metal_session`, which substitutes one gate at a time against a
replacement target.

**What the first fix round did.** The reviewer found that a `bare_metal_session`
yielded a session that `plan` and `run` accepted for a restore of
`cfg.library.root`, so composing it against a replacement drive rewrote the
library on the volume the identity gate had just refused, with no acknowledgment
and with the library lock held by another process. That is closed: a `Held` now
carries the directory it authorises, and `plan` and `run` refuse one that does not
authorise the path they are about to write.

**The residue, stated plainly.** `plan` and `run` resolve every path from
`cfg.library.root`, and a bare-metal session authorises the replacement target, so
there is now no composition in which a bare-metal session reaches a plan at all.
Neither function takes a `target`, and nothing in `src/` consumes
`bare_metal_session`. The bypass was closed by removing the path rather than by
correcting it, and R-8's third item is unserved again. The honest status of
`bare_metal_session` today is: it validates a target, substitutes three gates,
takes an installation-scoped lock, and hands back a session that can be used for
nothing.

**Why that is the right order anyway.** A recovery path that cannot run is a
missing feature. A recovery path that rewrites the library on a volume the
identity gate refused is data loss with the product's own gates reporting success.
Shipping the first while the second is open is not a trade this unit is entitled
to make.

**What closes it.** `plan` and `run` resolve their paths from the session rather
than from `cfg.library.root`: the `Held` already carries `authorises`, so the
change is to derive the target set from that directory and to build a
configuration rooted at it, rather than to add a `target=` parameter that the two
functions would then have to agree with the session about. The `Held` machinery
this round added is what makes that safe, because the authorisation check then
reads the same field the paths are derived from.

**Owner: U27,** which owns the operator-facing surface and already carries this
unit's `cratekit.session.restore_cli` obligation. The bare-metal verb is the one
place this composition would be made, so the unit that writes the verb is the unit
that finds out whether the derivation above is right.

**What must NOT close it.**

1. **Relaxing the authorisation check for bare metal.** That is the bypass,
   re-opened, with a comment explaining why it is fine.
2. **A `target=` parameter on `plan` and `run` that is trusted without being
   checked against the session.** Two sources for one answer is how the first
   version got here: `assert_recovery_target` validated a target and then dropped
   it, and everything downstream resolved a different one.

---

## R-21. What the U36 merge owes, from this side. Four conflicts, six items, and one thing not to undo

**Found:** by the verification of U32's second fix round, 2026-08-03, against a
real trial merge rather than by inference. **Re-verified during fix round 4**
against a scratch three-way merge of this branch onto `main` at `c114afa` from
merge base `4368171`. Every count below was measured on that merge.

U36 records the same obligation on its own side. It was **R-14 on its branch and
is R-16 on `main` now**, and its own text says so; an earlier version of this
paragraph cited the branch number, which is the same silent-repointing hazard
item 7 is about. Two of the items below were found only from this side and both
are worse than a failing test, so the list is kept on both sides rather than
trusted to one. **U36's entry needs the same additions.**

### The four textual conflicts

`git merge` stops on every one of these, so none is silent. They belong on the
checklist anyway, because a list that omits them reads as "this merges cleanly
and then needs six edits", and that is not what happens.

1. `docs/residual-findings.md`. Both sides append entries at the end.
2. `src/cratekit/core/cause.py`. Both sides add to the same region.
3. `tests/test_layering.py`. **BOTH SIDES MUST SURVIVE.** `main` widened the rule
   to `(r"^cratekit\.core\.(tree_registry|convergence)$", "write")` and this branch
   adds `(r"^cratekit\.core\.restore$", "write")`. Taking either side wholesale
   fails RED, so the resolution keeps both entries rather than picking one.
4. `tests/test_pending_units.py`. Both sides edit `EXPECTED_PENDING`.

### Two of the six are now applied ON THIS BRANCH, and here is why they moved

**Items 2 and 5 were applied in fix round 6, before the merge, because leaving
them for the merge was already costing something today.** `scripts/board.py audit`
exits 2 on this branch RIGHT NOW: issue #36 is closed, U36's module is on `main`,
and this branch's `tests/_pending.py` still owed U36 `cratekit.write.rebuild`. The
repository's own rule for that exit is to reopen the issue or clear the entry, and
U36 is finished, so the entry goes. Clearing it forces item 5 in the same commit,
because `_pending.requires` raises `KeyError` at import for a key that is no
longer in `PENDING`, which is the collection failure item 5 describes.

**Item 3 could not move with them, and that is a property of this tree rather
than a choice.** `src/cratekit/core/convergence.py` does not exist here, so
"import `core.convergence` normally" makes `restore.py` unimportable and takes the
whole suite with it. It stays a merge item.

**What carries item 3 now that its register entry is gone.**
`tests/test_restore.py` grew
`test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build`,
which is ALWAYS ARMED and needs no register key, so no unit closing can orphan it.
It asks what the build it is running in contains: with `core.convergence` absent
it asserts the fallback is present and latched, which is correct here; with
`core.convergence` present it asserts `_convergence_module` and the
`Kind.UNCONVERGED_TREE` filter are gone from `restore.py`, and its failure message
names the three deletions. So item 3 announces itself on the merged tree instead
of waiting to be read off this list.

### ALL SIX ARE APPLIED. This merge happened, and here is what it cost

**The U32 merge landed on `main` and every item on this list is discharged.**
Items 2 and 5 moved early, on the branch, for the reason the section above gives.
Items 1, 3, 4 and 6 were applied at the merge itself. The four textual conflicts
occurred exactly as predicted, all four resolved as unions, and none was
contradictory. Item 1 auto-resolved as predicted: the three-way merge took this
branch's deletion of `cratekit.core.restore` from both files with no conflict.

**Two of the six announced themselves as failing tests rather than as checklist
lines, which is what they were designed to do.** With the conflicts resolved and
nothing else done, the suite failed exactly twice:
`test_every_coupled_entry_declares_what_leaves_the_coupled_set` named the
`tree_convergence` entry for item 4, and
`test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build`
named the three deletions for item 3. Applying item 3 then turned item 6 red with
the `AttributeError` this list predicted for it, in that order.

**Item 3's third deletion was not just a deletion.** Removing the
`Kind.UNCONVERGED_TREE` filter from the RECORD step could not be done by deleting
the filter alone, because the plan was still putting tree markers into the
recorded set and the filter was the only thing keeping them out of the
reconciliation document. The plan now carries effect markers there and tree
markers on `tree_markers` alone, so the two stores hold one fact each rather than
one fact twice. That is what the item meant and the filter was the symptom.

### The six items to apply

**1. Delete the stale `cratekit.core.restore` entry from `tests/_pending.py`.**
Required, and it AUTO-RESOLVES. **Confirmed on the scratch merge:**
`cratekit.core.restore` is still present in `main`'s `_pending.py` and in `main`'s
`EXPECTED_PENDING`, this branch deletes it from both, and the three-way merge
takes this branch's deletion from both files with no conflict. Listed so nobody
re-adds it by hand.

**2. Delete the `cratekit.write.rebuild` entry from `tests/_pending.py` and from
`EXPECTED_PENDING` in `tests/test_pending_units.py`. ALREADY DONE, fix round 6.**
Nothing to apply at the merge. It moved forward because the entry was already a
`board.py audit` exit 2 on this branch, not because the countdown fired.

**3. Remove the fallback branch in `restore._hand_tree_shortness_over` and the
`_convergence_module` helper behind it, and import `core.convergence` normally.**
STILL OWED, and it is the one item of the six that this branch genuinely cannot
write, because the module to import is not on this tree. The register entry that
used to name it is gone with item 2, and what names it now is the always-armed
test described above, which fails on the merged tree until this is applied and
says which three deletions to make.

**4. Add `rollback_effects=(RollbackEffect.NONE,)` to the `tree_convergence`
entry in `core/config.py`.** **Still not writable by U32 alone, re-confirmed:**
`grep tree_convergence src/cratekit/core/config.py` on this branch returns
nothing at all. The `StateFile` entry exists only on `main` and the
`RollbackEffect` enum exists only here, so neither branch can write the line by
itself and it stays a merge item. `main`'s own comment at `config.py:1246-1265`
names the exact line. The three facts that entry holds are about rows in this
database and nothing outside the coupled set, so NONE is the right answer.

**5. Drop the `@requires("cratekit.write.rebuild")` decorator in
`tests/test_restore.py`. ALREADY DONE, fix round 6,** in the same commit as item 2
because item 2 forces it. The decorator and the test under it are both gone; what
replaced the test is described at the top of this entry. Nothing to apply at the
merge, and the paragraphs below are kept because the reasoning is what makes item
2 and item 5 one commit rather than two. **IT IS NOT SILENT, AND THE EARLIER TEXT
HERE WAS WRONG ABOUT BOTH ITS SHAPE AND ITS SIZE.** With items 2, 3 and 4 applied
and this one skipped, `tests/test_restore.py` fails to COLLECT: `_pending.requires` raises
`KeyError` at IMPORT time, at `tests/_pending.py:267`, for a key no longer in
`PENDING`. A plain `pytest` run then EXITS 2 with `Interrupted: 1 error during
collection` and runs NOTHING at all. It does not look like a suite that passed,
it looks like a suite that refused to start. It is invisible only to a run that
was explicitly told to continue past collection errors, or to a subset run that
does not name this file. The magnitude is **every test in
`tests/test_restore.py`, not "roughly two hundred"**.

**THE COUNT MOVES WITH THIS BRANCH'S TIP AND THE FLOOR DOES NOT.** It read "123
tests, collection drops from 3,419 to 3,296", which was measured at `c7a1a7d` and
was already wrong two rounds later, because every round since has added tests to
that one file while the paragraph under "the verified numbers" updated the totals
and left this sentence alone. Stated so it stays true: the loss is the whole of
`tests/test_restore.py`, **132 tests at tip `f37cfae` plus fix round 5**, and what
a person on the checklist should compare against is the FLOOR, **3,298 collected**,
which does not move while this branch's new tests keep landing in that file.

**6. Rewrite `test_the_tree_shortness_handoff_calls_the_module_that_owns_the_gate`
to patch `convergence.mark_unconverged` instead of `restore._convergence_module`.**
Silent in the way item 5 is not: item 3 deletes the attribute the test patches, so
it raises `AttributeError` at setup, and that is one red test.

### The one thing not to undo

**7. The residual-finding citations in `core/restore.py` are by TITLE, and the
merge must keep them that way.** `shares_the_database_volume` and
`bare_metal_session` used to cite **R-19** and **R-20** by number. This branch
adds **five** entries, not three: R-19 through R-23, the last two of which landed
after this item was first written. `main` ends at R-17, so a sequential renumber
moves all five down one, at which point BOTH citations name the wrong finding and
the second one names this checklist.

**MEASURED ON THE TRIAL MERGE: nothing renumbers.** Both sides append, `git
merge` takes both appends, and the merged file runs R-1 to R-17 and then R-19
onward with **R-18 missing**. So the renumber is a hand edit somebody chooses to
make, and the gap is the thing that invites it: a person tidying that gap is the
mechanism this item is about, not the merge. Whoever closes the gap renumbers
FIVE entries and must move every citation of each of them, in prose, in source
comments and in docstrings, which is the repoint that was missed once already at
the U36 merge. Leaving the gap and saying in the file why it is there is the
cheaper answer and is equally correct. **DECIDED AT THIS MERGE: the gap stays,
and R-19 says at its head why.** These two citations survive either decision,
because they now cite
`restore.RESIDUAL_CAPTURE_VOLUME_UNREPORTED` and
`restore.RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH`, whose values are the finding
titles, and `test_round4_the_residual_findings_this_module_names_still_exist`
asserts each title still names a heading in this file. A renumber leaves that
green, which is correct; a retitle turns it red, which is also correct. This is
the shape already caught at the U36 merge, where `core/convergence.py` said "See
R-15" and R-15 on the merged tree was a different finding.

### The verified numbers

**With the four conflicts resolved and NONE of the six items applied:** exactly
**three failures**, each one mapping to an item on this list, and nothing fails
that is not on it.

**With all six applied:** **3,402 passed, 17 skipped, 3,419 collected**, `ruff`
clean, `scripts/scan_repo.py` exit 0. The six are NECESSARY and SUFFICIENT: the
only remaining differences are the two documentation notes recorded below.

**THOSE COUNTS ARE STALE IN BOTH DIRECTIONS AND ARE NOT TO BE DERIVED FROM.** They
were measured against branch tip `c7a1a7d` and `main` at `c114afa`. Both sides have
moved: this branch is at fix round 6, and `main` has taken at least three commits
past `c114afa` in the same session, from other units and from documentation. This
paragraph used to carry an arithmetic extrapolation for each round, which is the
habit the section below forbids, so the extrapolation is deleted rather than
extended. **The next person who needs a number re-runs the scratch merge; nothing
here may be added to.**

**WHAT DID NOT MOVE, re-checked at fix round 6.** The four conflicts are unchanged.
`main`'s `_pending.py` still carries `cratekit.core.restore`, so item 1 stands
exactly as written. Item 4 is still unwritable from either side alone. Items 2 and
5 are applied here, which can only REDUCE the three failures, and item 3 is still
owed. Those are properties of the two sides rather than of a tip.

**AND ONE FAILURE MOVED RATHER THAN DISAPPEARED.** Items 2 and 5 removed the
`board.py` contradiction and the collection error, and the always-armed test that
replaced them fails on the merged tree until item 3 is applied. That is the same
obligation, announcing itself in a test whose message names the fix instead of in
a checklist line, and it is deliberate: item 3 is the one thing on this list that
nothing else can detect.

**Two documentation corrections the merge should also carry.** U36's
`assert_no_latched_restore` docstring says U32's `LATCHING_KINDS` does not include
the tree kind and that its exemption is therefore inert. Fix round 2 put that kind
back, so the premise is false while the derivation it justifies is still exactly
right: the exemption is now LIVE rather than inert. Nothing behaves differently,
because that function subtracts the tree kind by name from whatever the set holds.
The reverse direction is already correct in `reconcile.assert_converged`.

---

## R-22. Two identity generators in one codebase, 16 bits and 64, and only one of them was argued

**Found:** by the independent verification of U32's fix round 4, 2026-08-03.
Recorded rather than fixed, because the file is outside this unit's scope.

**What this branch changed.** `core/snapshot.py:new_stamp` builds a capture stamp
as a timestamp plus `secrets.token_hex(8)`, 64 bits of random tail. It was widened
during this unit's rounds because the stamp keys the pre-restore staging
directory, and two restore attempts landing on one stamp would put the second
attempt's write-ahead log on top of the first attempt's, destroying bytes that are
in no capture. Fix round 5 also made that collision a deterministic refusal in
`restore._stage_companion_aside`, so the width is now a second line rather than
the only one.

**What was left.** `cli/output.py:261:new_run_id` still builds a run identifier as
a timestamp plus `secrets.token_hex(2)`, 16 bits. So the product now has two
identity generators with a 48-bit difference between them, and nothing anywhere
says why they differ.

**Why it is worth a number rather than a shrug.** `new_run_id`'s own docstring
states a consequence at least as serious as the one this branch acted on: *"two
runs can start inside the same second, and a collision would let one run's
decisions answer another run's gate."* A gate answered by the wrong run's
decisions is a person approving one thing and a different thing happening. Sixteen
bits inside one second is roughly a one-in-a-quarter-million chance per colliding
pair, which is small and is not the same as the capture stamp's, and the two
numbers were chosen by different rounds for different reasons that were never
compared.

**The test does not close it either.** `tests/test_cli_contract.py:687` asserts
`output.new_run_id() != output.new_run_id()`, which reads both sides out of the
function under test. It is not vacuous, since it does catch a constant
identifier, but at 16 bits inside one second it is the assertion that flakes
rather than the guard that holds, and it is the only coverage the tail has.
`tests/test_snapshot.py` makes the same shape against `snapshot.new_stamp`, where
64 bits puts the flake rate past caring.

**What closes it.** Either widen `new_run_id` to match, which costs four
characters in a log line and nothing else, or write one sentence in its docstring
saying why a run identifier tolerates a width a capture stamp does not. Either
outcome makes the asymmetry deliberate. The current state is that it is
accidental.

**Owner: whoever next edits `cli/output.py`.** It is one line and one docstring,
and it is recorded here rather than fixed inside a restore unit because a fix
round reaching into a CLI module it was not reviewing is how the next round
inherits an unreviewed change.

**What must NOT close it.** Narrowing the capture stamp to 16 bits for symmetry.
The stamp's width is load bearing for a reason written down beside it, and
symmetry achieved by taking the argued side down to the unargued one is the wrong
direction.

---

## R-23. Three things the occupied-staging refusal leaves standing, each verified safe

**Found:** by the independent verification of U32's fix round 6 and by round 7's
own driving of them, 2026-08-03 and 2026-08-04. **Recorded rather than fixed, and
each one was MEASURED rather than reasoned about**, because a residual that is
silent about a live behaviour reads later as closure.

### 1. `already_staged` lists whatever is in the directory, and calls all of it companions

`core/restore.py:1691-1692` and `:1708`. The refusal names the staging
directory's whole listing, and one of its remediation steps calls that listing
"the live storage-engine companion files already moved out of the way". Those are
two different things wearing one label.

**Measured.** With a user file `holiday-photo.jpg` sitting in the staging
directory beside an earlier attempt's log, the refusal reads "the staging
directory ... already holds holiday-photo.jpg, master.db-wal" and its detail
carries `already_staged: ['holiday-photo.jpg', 'master.db-wal']`, under a step
saying those are companion files this run moved. The photograph is neither.

**Why it is cosmetic rather than dangerous.** The listing is DESCRIPTION, not
decision: what decides the refusal is `os.path.lexists` on the one resting name,
so an unrelated file cannot cause a refusal and cannot suppress one. **Measured:**
with only `holiday-photo.jpg` in the staging directory and no collision at the
resting name, the restore completes and converges. The cost is a sentence that
over claims to somebody already recovering from something.

**What would close it.** Either list only the names this run staged, which the
performing path knows and the preflight does not, or drop the word "companion"
from the step and say plainly that the directory holds these names.

### 2. One rehearsal and run disagreement survives, and it is the safe direction

`core/restore.py:1683-1687`. `os.path.lexists` answers False on ANY `OSError`,
including a permission error, so a staging directory this account cannot search
hides its occupant from the guard rather than reporting it.

**Measured.** Staging directory at mode `0o000` with an earlier attempt's log at
the resting name: `os.path.lexists(resting)` answers False, the guard returns, the
REHEARSAL proceeds and reports all eight steps performed, and the REAL RUN then
refuses `restore-step-failed`. That is the shape this unit has spent two rounds
removing, and this instance of it is safe: `os.replace` is the first thing the
real run tries and it fails before anything has moved. Measured on the same run,
the live log still holds its bytes, the earlier attempt's log still holds its
bytes, and the database is untouched. Nothing ends half done, which is what makes
this different from the round 5 shape.

**Why it is not worth code today.** The product never creates a staging directory
in that mode; `config._mkdir_private` makes it `0o700`. Reaching this needs
somebody to have chmodded it by hand or a filesystem to have lost the mode. The
honest description is absence read as evidence of absence, one layer out from the
two reads this unit already fixed, and the layer it is in is `os.path.lexists`
itself rather than this module.

**What would close it.** Ask `os.lstat` in a `try` and distinguish "not there"
from "cannot tell", refusing on the second. That is a real improvement and it is a
change to the guard's contract, so it belongs to whoever next opens this function
rather than to a fix round closing out.

### 3. The performing backstop, when a race genuinely reaches it, still leaves the half done state

`core/restore.py:1644-1653`. The preflight copy of the staging check is the
primary and the copy inside `_stage_companion_aside` is the backstop for the
window between the check and the rename. If that window is genuinely hit, with
two companions live and the SECOND one's resting name taken in the window, the
first companion has already been renamed out of the live tree when the backstop
raises. The run then stops with the live write-ahead log missing from the library
and the database never replaced.

**This is stated plainly here because the code already states it plainly and a
silent residual would read as though it did not.** The docstring at those lines
says the preflight is what decides, says the backstop exists only for that window,
and says reaching it should be impossible. That is accurate. The refusal reached
this way NAMES the companion it already moved and where it now is, in the message
and in the detail, which is what makes the state recoverable by hand.
`test_round6_the_performing_backstop_names_what_it_already_moved` drives exactly
that path by planting the collision after the first companion has really been
staged.

**What would close it.** Undoing the moves already made before re-raising, which
is a rollback inside a rollback and needs its own failure story. Recorded as the
residual race rather than attempted inside this unit.
## R-24. Four report verbs were owed by a unit that was about to close, and named a module nobody could build

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

## R-25. The review-queue countdown is satisfied by an offer that never runs

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

## R-26. A third copy of the import-graph walk now lives in the reports suite

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

## R-27. The option a person picks is addressed by an identifier a re-import changes

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

## R-28. Two reflection spellings reach a writer past both structural guards

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

## R-29. One reflective call shape stays out of reach, and it is named

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

## R-30. A namespace method with no argument is an unreadable lookup

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

## R-31. Two reflection spellings stay quiet, and each needs a refused import

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

## R-32. A container built by a comprehension binds none of its elements

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

## R-33. A class rebound after its own definition is no longer reachable by name

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

**Not fixed here** for the three wrapper spellings. Closing them means deciding
whether an arbitrary callee hands its argument back, which is the same undecidable
question the residual titled "One reflective call shape stays out of reach, and it
is named" declines to answer for `map(getattr(p, n), items)`. The decorated
spelling that an author actually writes, `@dataclass` above the class, is covered
and has a fixture.

**The word "only" was withdrawn, because it covered five shapes nobody had
measured.** A residual whose wording covers a shape nobody measured is a residual
that cannot be checked, which is this finding's own rule applied one level in.
Five further spellings were quiet and none of them is a wrapper:

```python
Keeper = Keeper or None                  # FIXED, fires
Keeper = Keeper if True else None        # FIXED, fires
Keeper = (Keeper,)[0]                    # still quiet
Keeper = [Keeper][0]                     # still quiet
Keeper = getattr(_m, "Keeper", Keeper)   # still quiet
```

The first two are not undecidable by this finding's own standard. `_bound_value`
already reads `or` and a conditional expression through, on the stated rule that a
value reachable on one path is reachable, and a class object is always truthy
besides. Executed, both leave `Keeper.mod is config` True. `_rebound_to_itself`
reads the ALTERNATIVES of the right hand side now rather than one spelling of it,
and both fire.

**Three remain quiet and are named rather than covered by a word.** A container
literal that is immediately subscripted at a constant index is decidable and is
not read: `_bound_value` renders no key for `(Keeper,)[0]`, because the base of
the subscript is a literal rather than a receiver. `getattr(_m, "Keeper", Keeper)`
is a call, so it stays on the undecidable side of the line this finding already
draws, even though the target's own spelling appears in it as the default.

**Closes when:** either a bounded reading of "this call returns its argument"
exists, or `_bound_value` learns a constant-indexed container literal, or the
remaining spellings are accepted permanently. The natural owner is whichever unit
next widens the binding table.

---

## R-34. A base binding reachable only through a branch is read as unreachable

**Found:** during the U34 round 9 fix, 2026-08-04. It is the stated cost of the
path model that closed round nine's first finding, chosen in the direction that
misses rather than the direction that fires on ordinary code.

An attribute set inside a base class's `__init__` is reachable from a subclass
only when something on the running path actually runs that `__init__`. Round nine
reads two suppliers: an UNCONDITIONAL chaining call in the scope doing the
overriding, and an attribute the class body already binds. Three shapes fall
outside both and go quiet.

**One.** The chaining call lives in the other arm of the same conditional:

```python
class Row(Base):
    def __init__(self, raw):
        if raw:
            self.mod = dict(raw)
        else:
            super().__init__()      # the module IS reachable on this arm

    def go(self, cfg):
        return self.mod.save(cfg)   # quiet, and it is a real write
```

**Two.** The base binds the attribute in a method the subclass calls by some name
other than `__init__`:

```python
class Base:
    def setup(self):
        self.mod = config


class Row(Base):
    def __init__(self, raw):
        super().setup()
        if raw:
            self.mod = dict(raw)
```

**Three.** A `del` of an instance attribute with nothing under it still reports
whatever the constructor bound, because the restore is a FILL rather than an
overwrite:

```python
class Deleter:
    def __init__(self):
        self.mod = config

    def go(self, cfg):
        del self.mod
        return self.mod.save(cfg)   # AttributeError at runtime, reported anyway
```

The third is a false positive rather than a miss, and it is the pre-existing
answer rather than one round nine introduced: the shape reported the same thing
before `del` was read at all. It is named here rather than left silent because the
`del` rule now sits beside it and a later reader would otherwise take the fill
semantics for a judgement about this shape.

**Not fixed here**, deliberately, for the first two. Both need PATH modelling
inside a method rather than a fact about the method: which arm binds what, and
which arm the read is reachable from. The unconditional reading is chosen because
its error is a miss, and a guard that fires on ordinary code is not a lesser
failure than one that misses. The third needs the same modelling from the other
side, since the delete and the read are ordered within one method.

**Closes when:** whichever unit next widens the binding table gives a method body
an ordering rather than a set. All three shapes have a spelling above, so a later
round can drive them without re-deriving them.

## R-35. Two write-path enumerations still read an unreadable node as an absent one

**Found:** during the U34 round 10 fix, 2026-08-09, while looking for the same
shape as this round's classification defect one file over. Both instances are in
`cratekit.write`, on the WRITE path, which this read-only unit does not own.

The reports side is fixed at the classification: `rbxml.node_kind` has three
answers, and `reports.export` refuses a document carrying a node whose kind it
could not read rather than filing it as a folder. Two enumerations in the write
path still ask the question as a positive filter, so a node whose kind is
unreadable simply is not there. Both are measured rather than argued.

**One, and it is the one that decides where a write lands.** `rbxml._tree_node`
infers the enclosing tree when a caller names none, and it refuses when the
playlist root holds more than one folder because the answer would be a guess.
Driven on a document with two root folders:

```
healthy:                      the enclosing tree was not named and the playlist
                              root holds 2 folders, so it cannot be inferred
one root folder unreadable:   BY GENRE + ENERGY
```

Making one of the two unreadable does not make the inference harder, it makes it
succeed. The ambiguity the refusal exists for is invisible, so the write proceeds
into the folder that happened to stay readable.

**Two.** `trees._tree_folders` enumerates a tree's genre folders by the same
positive filter. Driven on a three-folder tree with one folder's `Type`
unreadable, the enumeration returns two of the three, so a sweep over "every
genre folder" walks past one and reports that it changed nothing there, and the
duplicate-name check that follows cannot see the folder it did not enumerate.

**Not fixed here**, and the reason is scope rather than difficulty. Both sites
are one call to `rbxml.node_kind` away from being able to tell the third state,
and neither can be given a REFUSAL from this unit: `_tree_node` and
`_tree_folders` are reached by the tree writers, the vocal sweep and the label
tree builder, all of which belong to other units, and a new refusal on a write
path is exactly where this project has already over-corrected once. The cost is
also asymmetric with the reports one: a report that renders clean over a library
it could not read is a wrong answer nobody can see, while these two produce a
write that lands somewhere defensible and an enumeration that is short.

**Closes when:** whichever unit next touches the tree writers gives both
enumerations the three-valued kind, and decides per site whether an unreadable
node is a refusal or a reported skip. The two probes above reproduce both in a
dozen lines against `tests/xml_fixtures.py`.

## R-36. An extra node close is accepted, and both reports render over a re-parented tree

**Found:** U34 round 10 independent verification, 2026-08-10. Full drive in
`docs/u34-round-10-verification.md`, finding 1.

`rbxml` never round trips through a tree serializer, by documented design, so no
XML parser validates the playlist tree. `matching_close` counts depth forwards
from a node's open tag, so one stray `</NODE>` lands a folder's close early and
everything after it is re-attached to the root.

**Measured cost, on the reports suite's own export with one close inserted.**
`read_export` ACCEPTS the document. The document declares `ROOT Count="2"` while
the walk finds 6, and `INBOX Count="5"` while the walk finds 1. Intake aging
falls from 5 groupings, 3 of them expired, to 1 grouping. The duplicate audit
reports two placements that exist nowhere in the library, and that audit feeds a
queue whose accepted verdict licenses a deletion surface.

**Why it is a residual and not a blocker.** The second floor condition is
withdrawn on reachability. Four producer candidates were driven and none emits
the input: every real splicer on the write path, every persist route, which is
`config.atomic_write_bytes` with `mkstemp` then `fsync` then `os.replace` so a
partial document cannot survive, and rekordbox itself, measured on two real
7.2.17 exports of 56 MB each, both balanced at 28189 paired opens and closes,
zero raw brackets in names, zero declared counts disagreeing across 28250 nodes.

The predecessor's mechanism IS live and was reproduced: `DJ_common.rbxml.remove_folder_node`
bounds an open tag with a `find(b">")` that is not quote aware, and on a child
name carrying a literal `/>` it returns 2 opens against 3 closes. Cratekit's
successor returns a balanced document on the identical input, and both escapers
write the bracket escaped, so neither tool can create the byte.

**Stated as METHOD's first pattern demands:** four driven candidates do not
produce it, which is not the same as nothing produces it. A hand edited export
is the one open route and it is UNMEASURED.

**What closes it:** the check measured in the same report. `read_export` already
runs the identical declared count check on the COLLECTION section. Reading the
same declaration on playlist nodes refuses both stray shapes, costs the suite
zero when ordered after the unreadable kind refusal, and produced zero false
refusals across 28250 nodes on each real export. It cannot land alone: see the residual titled "A create path does not bump the count it invalidates".

## R-37. Half of the new refusal's detail payload is asserted and half is not

**Found:** U34 round 10 independent verification, 2026-08-10, finding 3.

Dropping the `found` key from the refusal detail kills zero on the full suite,
row V18. Its sibling V17, dropping `nodes`, kills 3. Half the payload the
refusal emits is pinned and half is free to change or vanish.

**Measured cost: none on the shipped branch.** No caller reads `found` yet.

**What closes it:** one assertion over the key, or a wire format pin over the
whole detail mapping.

## R-38. The word a write refusal uses for a folder is not pinned

**Found:** U34 round 10 independent verification, 2026-08-10, finding 4.

`KIND_FOLDER`'s value reaches a write refusal and row V09 kills zero. The
composite shows the sentence is load bearing: V39, rewording the whole sentence,
kills 2; V13 kills 1; V10, the same mutation on `KIND_PLAYLIST`, kills 1. The two
constants are symmetric in the code and asymmetric in coverage.

**Measured cost: none directly.** A refusal message a user reads could change
wording without a test noticing.

**What closes it:** assert the folder spelling the way the playlist spelling is
already asserted.

## R-39. The new refusal has no fixture carrying exactly one unreadable node

**Found:** U34 round 10 independent verification, 2026-08-10, finding 5.

Row V50, narrowing the refusal to `if unreadable[:-1]:`, kills zero on the full
suite. The composite V51, never refusing at all, kills 3. Every parametrized case
uses `.replace(old, new)` with no count, so all seven playlists are retyped at
once and the boundary at exactly one unreadable node is never exercised.

**Measured cost: none observed.** The refusal does fire; only its boundary is
unpinned.

**What closes it:** one fixture that retypes a single node.

## R-40. Two membership tests can be widened with the whole suite green

**Found:** U34 round 10 independent verification, 2026-08-10, finding 6.

`has_folder` matching anywhere in a path, row V22, and the grouping filter
reading `path` rather than `path[:-1]`, row V28, both kill zero. The composites
V40, V41 and V42 kill 23, 2 and 5, so both predicates are load bearing while
neither boundary is pinned.

**Measured cost: none observed on this branch.** A widened `has_folder` would
match a folder nested under another of the same name.

**What closes it:** a fixture with a same named nested folder, and one asserting
the grouping filter's last path element.

## R-41. The round's own table was thirty rows against an independent fifty

**Found:** U34 round 10 independent verification, 2026-08-10, finding 7.

The author's table carries 30 rows and 4 zero rows. The independent table carries
50 distinct rows plus 4 untracked composites, and 11 zero rows. Eight of the
eleven are guards the author's own round created and his table did not mutate.

This is the fourth measured instance of the same gap on this project, after 10
against 17, 39 against 49 and 49 against 83. It is recorded as evidence for the
standing rule that an author's table is a draft, not as a defect in this branch.

**Measured cost: none.** Documentary.

## R-42. A create path does not bump the count it invalidates, and it is live on main

**Found:** U34 round 10 independent verification, 2026-08-10, finding 9, while
measuring false refusals for the R-35 fix. Belongs to U18's surface, not U34's:
`f8ac564` landed `write/rbxml.py` and `write/trees.py`.

`insert_empty_subplaylist` inserts a child and calls `_bump_count(folder, +1)`.
`splice_into_subplaylist`'s `create_missing` path inserts the same child and
bumps nothing, leaving the folder declaring one fewer child than it holds. Driven:
`BY GENRE / Deep House` declares 1 while holding 2. `trees.apply_unplaced_changes`
passes `create_missing=True`, so the unplaced routing pass is a live production
caller and this is on `main` today.

The module's own docstring states the rule it breaks: a folder's `Count` is
advisory because rekordbox recounts children on import, and "the writers that add
or remove a whole child do keep it accurate".

**Measured cost to a user today: close to none**, on the docstring's claim that
rekordbox recounts a folder's children. That claim is UNMEASURED here; what was
measured is that rekordbox itself never emits a disagreeing count, 0 of 28250
nodes on each of two real exports.

**The cost that matters is a coupling.** The reader check described in the residual titled "An extra node close is accepted, and both reports render over a re-parented tree" refuses documents whose
declared count disagrees with the walk, so landing it while this stands makes
Cratekit refuse documents Cratekit itself wrote. The two land together, or the
writer lands first.

**What closes it:** bump the folder count on the `create_missing` path, then land
the reader check.

## R-43. Fixed string reading and regex reading are indistinguishable to the suite

**Found:** U34 round 11, 2026-08-10, while measuring the round's own guard. Named
by that round as unmeasured rather than discovered later.

The `-F` flag on the guard's git read is not pinned. Rows C05 and C06 kill 5
each, so no input in the suite distinguishes reading the tag as a fixed string
from reading it as a regular expression.

**Measured cost: none today.** The unit commit tag `(U34)` contains parentheses,
which are regex metacharacters, so a switch to regex reading would change what
the tag matches. Nothing currently produces a tag where the two readings differ.

**What closes it:** one commit tag containing a metacharacter whose two readings
disagree, asserted.
## R-44. Five findings the U24 review accepted, and the reason each stands

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

## R-45. Case folding merges two different releases into one identity

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

## R-46. A recorded location that is not an absolute path is excused from the completeness proof, and `locations` cannot tell two kinds apart

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

## R-47. A square-bracketed mix name never matches the provider spelling of the same version

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

## R-48. A SIGKILL between the move and the tombstone still loses the record, and no handler can catch it

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

## R-49. The Subtitle vocabulary's false negatives collide, and the ISRC tells a collision from a convergence

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

## R-50. A designation filed in the remixer column is spelled unmatchably, deliberately

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

## R-51. An anchor with no active rows through it can still settle a removal off an empty directory

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

## R-52. The active half of the collection walk carries no identity, so nothing can be proved about an active row's version

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

---

## R-53. Three more stored decisions are addressed by a key a later build recomputes, and only the tombstone carries the row that would rescue it

**Found:** the U24 round 10 pattern five sweep, 2026-08-10. The rule is that a fix
round fixes the instance it was handed and reproduces the class one file over, so
after every fix you go looking for the same shape elsewhere.

**The shape.** A decision is written to disk under an identifier derived from an
identity, and a later build re-derives that identifier from the row in order to
find the record. If the derivation moves between the two builds, the record is
orphaned. That is exactly what four rounds of the tombstone recognition question
were about, and it is a property of the whole `review.DecisionStore` model rather
than of the tombstone.

**The three other instances, and what each costs if its derivation moves.**

* `deletion.stores.decline_predicate` recomputes
  `suppression_id_for(row_identity(row))` against the stored identifiers. A
  declined file is offered again. The person answers once more, and the old
  record is still listable and revocable.
* `deletion.run._verdicts` recomputes `item_id_for` over the same row identity to
  find the verdict a person gave. A confirmation is orphaned and the row is
  offered again. Nothing moves.
* `DecisionStore.suppresses`, which is what an acquisition sweep asks per
  candidate, recomputes `version_identity`. This is the one with teeth, since a
  suppression that stops being seen re-acquires a version somebody deleted on
  purpose. It is out of this unit's reach: the consulter holds a provider's title
  and no second field, so it composes nothing, and widening it is what the
  recorder is obliged to do instead.

**Why it is a residual and not a blocking finding.** Under the merge bar a
finding blocks only if it was driven end to end AND has a named user facing cost.
This one is not driven.

**The measurement this entry used to rest on was imprecise, and here it is
corrected rather than restated.** It said the row identity
`removed_file_identity(content_id, recorded)` "was rebuilt at all eleven commits
on this branch and evaluated on one probe row, and it produced a byte identical
answer at every one of them". Re-measured in round 11 by parsing every commit's
blob rather than by running one probe: over the branch's 20 commits the function
takes FOUR distinct forms, changing at `c02a7b4`, `c087439` and `df945fb`. What
is byte identical at all four is the RETURN EXPRESSION. Every change widened the
REFUSAL GUARD:

* through `5cb1ed3`: `not str(content_id)`
* `c02a7b4`: `content_id is None or not str(content_id)`
* `c087439`: adds `.strip()`
* `df945fb`: adds `isinstance(content_id, bool)`

So the conclusion survives for every input that produces an identity at all, and
the set of inputs that produce one shrank three times. A probe row that produces
an identity cannot see that, which is METHOD's fourth pattern: a number taken on
a fixture rather than over the input space. The version identity, by contrast,
moved four times in what it RETURNS, which is why the tombstone was the instance
that bit.

**What the narrowing could cost, and its reachability, measured.** A decline
recorded by a pre-`c087439` build for a whitespace content identifier is now
refused rather than composed, and `decline_predicate` has no handler for the
refusal. Driven: unreachable through the pass, because `candidates.categorize`
asks `identifiable` first and unconditionally and answers UNIDENTIFIABLE, so
`decline_predicate` is never asked about such a row. The only store that could
carry such a record is one written by an unmerged branch tip, and nothing has
shipped.

**What closes it, and the one thing that blocks the same repair.** The tombstone
recognition question was repaired by matching a foreign era's record on the ROW
it names, which works because a tombstone payload has carried `content_id` and
`recorded` since the first commit of this pass, measured across all eleven. The
decline payload carries `recorded` and NOT `content_id`, so the identical repair
cannot be applied to it today. Adding `content_id` to the decline payload is the
enabling change, and it is deliberately not made here: no decline derivation has
drifted, so the change would be a store shape edit with no defect behind it.

**Not fixed here** because the round was scoped to the recognition question, and
because the measurement says the class is present while the instance is not.

---

## R-54. The row coordinate is unmeasurable by construction, and this round widened what reaches it

**Found:** the U24 round 10 independent verification, 2026-08-10. Re-measured in
round 11.

`stores._row_coordinates` is applied to BOTH sides of its own comparison, which
is what makes it correct and what makes it invisible. Four symmetric mutations
kill zero on the full suite: a null path read as the literal word `None`, the
path case-folded, the path dropped from the key, the identifier dropped from the
key. Two composites against the thing it guards, a payload naming a different row
and a payload recording no path, kill zero as well.

**What round 11 changed about it.** The stamp now moves on every change to any
composition rule, so many more records fall to the row lookup than before, and
the lookup is reachable by more futures than the round 10 measurement allowed
for. It is still not reachable today: it needs a record whose stamp is not this
build's, which needs a store written by an earlier build, and nothing has
shipped. The reachability of a future upgrade is unmeasured because there is no
released build to upgrade from.

**Partly closed here.** The guard half of it moved: `_row_coordinates` used to
re-implement `tombstone.removed_file_identity`'s null, boolean and blank tests
verbatim in another module with nothing asserting the two agreed, and it now
delegates to that function. Those three layers are measured there at 4, 4 and 4
deaths. What remains unmeasured is the KEY, which is the pair itself.

**Closes when** a test writes a record under one build's rules and reads it under
another's with the row coordinates deliberately perturbed on one side only, which
needs a fixture that can produce a foreign stamp without planting one.

---

## R-55. Two document format versions are hand set and nothing measures the document against them

**Found:** the U24 round 11 pattern five sweep, 2026-08-10. The sweep looked for
the shape this round repaired, a digest computed over sampled OUTPUTS rather than
over its INPUTS, and found no second instance of it. It found this instead, which
is the instrument `identity_scheme` replaced rather than the defect it had.

`deletion.watermark.WATERMARK_VERSION` and `review.DECISION_STORE_VERSION` are
both `1`, both written into every document those modules persist, and both read
back and compared on load, which is more than the export next door used to do.
Neither is named in any test. Nothing pins the SHAPE of the document against the
number, so adding a field to `Watermark.to_json` or to a stored suppression
without bumping the constant leaves two builds writing different documents under
one version, and the reader cannot tell.

**Why it is a residual.** Both readers recognise positively field by field and
refuse what they cannot recognise, so the failure direction is a refusal rather
than a misread, and the U24 half was not driven. `DECISION_STORE_VERSION` is
U11's and out of this unit's reach.

**Closes when** each version constant is paired with a test that pins the exact
key set of the document it stamps, so a field added without a bump goes red at
the moment it is added rather than at the moment somebody upgrades.
## R-56. Five accepted findings from the U38 reviews

**Found:** during U38's two adversarial review rounds, 2026-08-02 and
2026-08-03. The first three were confirmed against the tree and none of them is
fixed by U38. The last two are limits of the guards U38 ships, stated here and
pinned by tests rather than left to be discovered.

**1. `core.secrets` reaches the boundary as `internal-error` on every path but
one.** `cratekit/acquire/provider_session.py:128` catches
`secrets.CredentialError` and translates it into the adapter vocabulary, which
is correct and is the only conversion there is. Any other caller reaching
`secrets` raises a `CredentialError` that meets `except Exception` in
`cratekit/cli/__init__.py` and becomes reason `internal-error`, exit 1, remedy
`report-defect`. A user who has simply not recorded a credential is told to
report a defect.

The reservation table does not cover it and says so. `core.secrets` carries its
remedy as a CLASS attribute and subclasses per meaning, so its structured cause
is the exception TYPE and no constructor parameter names one, which is outside
what the completeness walk in `tests/test_reserved_causes.py` can see. That limit
is written into the walk's own docstring rather than left implied. The earlier
argument, that config and secrets both "already reach the command line carrying
their own token", is true of config and is not true of secrets.

**Closes when:** the command-line boundary declares a conversion for
`secrets.CredentialError` the way it already does for `config.ConfigError`,
mapping its three tokens onto `credential-missing`, which `core.cause.REASONS`
already reserves at `PRECONDITION`. One except clause.

**2. `core/session.py` discards `exc.remedy` from an unreadable fact file.**
Around line 1026, `_shown_ages` catches `backup_facts.BackupFactsUnreadable` and
raises `refuse(..., remedy=Remedy.REPAIR_BACKUP_FACTS)` with the token written in
by hand. `backup_facts` raises that same exception with either
`REPAIR_BACKUP_FACTS` or `UPGRADE_CRATEKIT`, and the second one is the whole
reason the exception carries a remedy at all: a fact file written by a NEWER
build must not be repaired by hand, because repairing it discards a record this
build cannot read and the newer one can. A user on the older build is currently
told to repair it.

Driven live and confirmed, and confirmed present on `main` before U38 branched.
U38 introduced neither the code nor the defect and touches no file in `core/`,
so it is recorded rather than fixed. U38's table is what makes the fix one line:
`repair-backup-facts` and `upgrade-cratekit` are both reserved at 32 with their
own token, so the conversion has only to pass `exc.remedy` through.

**Closes when:** `_shown_ages` forwards `exc.remedy` instead of naming a token.

**3. The reservation table has no consumer in `src/`.** Only tests import
`cratekit.cli.exit_codes`. All 22 reserved causes still reach `except Exception`
and exit 1 today, and the two source guards forbid a second table rather than
requiring the first one be read. That is consistent with a reservation rather
than a wiring, and the module docstring now states it plainly so nobody reads the
table as live behaviour.

**Closes when:** the command-line boundary converts a module refusal through
`code_for` and `remediation_for`, which is the unit that lands the standalone
utility verbs.

**4. The second-table guard cannot tell a duration from a status for a slug that
IS a cause.** Added during U38's second review round, and pinned by
`test_the_residual_is_pinned_rather_than_discovered` rather than left to be met
in a failing build. `BACKOFF_SECONDS = {"rekordbox-running": 30}` is reported as
a reservation of 30, because by shape alone it is one.

The alternative is matching on the variable's name, and a guard a rename defeats
is not a guard, so this direction was chosen. What keeps it small is the key
rule: a bare integer counts only when somebody DECLARED the string a refusal
cause in the reservation table, in the package-wide derivation, or as an enum
member in the same file, which is twenty two slugs plus whatever a source says
about itself. The tree holds 66 kebab-keyed pairs across `cli/registry.py`,
`core/binaries.py`, `core/cause.py` and `core/naming.py` and not one of them is a
declared cause, so none of them can trip it.

Amended in the fifth round: the key set is eighty two slugs, the closed reason
registry included, and a bare integer in range reserves any of them. The fourth
round narrowed sixty of those keys on the strength of an over fire measured
against a hand written fixture; measured against the real tree the wide rule
reports ZERO offenders outside the two table owners, and the narrowing cost
thirteen of sixteen realistic second-table shapes. The residual
"The tiers were bought with a number that does not exist" carries the
measurement and the reasoning.

So this residual is general rather than small, and it is written down as such.
Two fixtures pin it, one per SPELLING of a key.
`RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS` pins eighteen hits from eleven
ordinary constructs keyed on inline strings.
`RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME` pins eight hits from six constructs
keyed on an enum member, a class attribute or a module constant, which is the
tree's own idiom and which the first fixture contains zero instances of. Both
counts measured in this worktree.

**Closes when:** nothing has to close it. It is a stated limit with two fixtures.
**There is no per-statement escape and the sixth round deleted the one there
was**, so the only escape is `TABLE_OWNERS`, which switches the guard off for a
WHOLE FILE and is pinned to exactly two entries by a membership assertion. That
is strictly wider in blast radius than the per-statement mark it replaced and it
is the trade taken deliberately: the per-statement mark was measured to silence a
one line `def` body, two statements on one reason, and sixty one reservations
from one comment, and its expansion set could be widened in three directions with
only one of them pinned. A wide escape somebody has to argue for in a test is
preferred to a narrow one nobody reviews.

**5. `NOT_A_CAUSE` is a classification a person has to keep making.** Every
package enum reaching an exception's constructor is treated as a refusal cause
vocabulary unless it is listed there with a reason. That is deliberate: the
failure mode is a loud demand to classify a new enum, never silence, and going
silent takes an explicit edit with an argument beside it.

The cost is real and is recorded here so nobody meets it as a surprise. Landing an
exception that carries, say, a new `Portion`-shaped enum will fail
`test_every_structured_refusal_cause_in_the_package_is_reserved` with a demand to
reserve its members, and the fix is one line in `NOT_A_CAUSE` plus a sentence
saying why it is not a cause. `test_every_enum_declared_not_a_cause_exists` keeps
the list from going stale.

**Closes when:** nothing has to close it. Recorded as a maintenance cost that was
chosen over a rule a rename can flip.

---

## R-57. Two copies of one import walk still carry a relative-import defect

**Found:** during U38's third review round, 2026-08-03. Corrected in the fourth
round, 2026-08-03, because the third round's version of this entry was WRONG
ABOUT ITS OWN FILE. Driven and confirmed both times.

`tests/_source_guards.py` asks "does this source reach a named module" in two
classes, and both used the same expression to recognize a relative import:

    node.level > 0 and module.split(".")[-2:] == ["core", "<module>"]

That expression answers for `from ..core.exit_codes import ExitCode` and for no
other relative spelling. `node.module` holds only the TAIL: a SIBLING import
records `exit_codes` and nothing else, and `from . import exit_codes` records
nothing at all, so the one-level forms, which are the natural spelling for a file
sitting beside the module it imports, matched nothing. Confirmed live: a module
inside `cratekit/core/` written as `from .exit_codes import ExitCode` with
`CODES = {"rclone-missing": ExitCode.PRECONDITION}`, a fully reserved cause and
the exact case the guard exists for, reported nothing.

**What the third round got wrong.** It recorded the surviving copy in
`ReviewImports` as living on `main`, as though this branch were not the file it
was describing. Lines 85 to 90 of THIS branch's own committed
`tests/_source_guards.py` were that same expression, and every question the
review guards ask returns early when the walk says a source does not reach the
module, so `from .review import offer` and `from . import review` were answered
"no" rather than answered wrong. Driven twice and confirmed live. Recording a
live defect as somebody else's is worse than not recording it, because the next
reader checks the named place, finds nothing, and stops looking.

**Fixed here, in the fourth round.** Both walks now call one `_import_targets`,
which resolves `node.level` against the importing file's package the way
CPython's `_resolve_name` does when the caller knows that package, and reads the
tail when it does not. `node.module` being None for `from . import X` is handled
as the package it is rather than coerced to an empty string. `ReviewImports`
takes an optional `package`, threaded through `calls_review`, `offers_into`,
`constructs_review` and `methods_on_review_construction`; no production caller
knows a package today, so the fallback is the live path there and both paths are
driven. `REVIEW_PACKAGE` and `EXIT_CODE_PACKAGE` are gone, derived from the
module name rather than spelled twice.

Two copies remain, both on other branches:

- `ImportsOf`, U12's generalization of `ReviewImports`, on U12's branch.
- `SoftDeleteNames`, the conformance branch's third copy.

Unifying the three is deliberately NOT attempted here: eight branches edit this
file and the change is kept minimal and self contained on purpose.

**The reason this is written down rather than left to the merge.** U38's own
docstring already books the collapse into `ImportsOf`. That collapse takes ONE
implementation and deletes the others, so if it takes `ImportsOf`'s relative
handling rather than the fixed one, the defect survives the deduplication and
lands in the single place every guard then reads. A three-into-one merge that
picks the wrong one is silent by construction: every call site keeps working and
every suite stays green, because what was lost was a shape none of them drives.

**Closes when:** the collapse lands and its `ImportsOf` resolves `node.level`
against the importer's package, with a fixture for the sibling form, a fixture
for `from . import <module>`, and the existing two-level fixture still passing.
Reviewing the collapse means checking that specific line, not that the tests are
green.

**2026-08-15. What the U12 merge discharged, and what is left.** U12 merged on
2026-08-14 as `038168a`, so the copy this entry places on U12's branch is now on
`main` in this same file, and one of the two named copies has stopped being a
separate copy. The half of the closing condition that is about RESOLUTION is
done: `ImportsOf` resolves `node.level` against the importing file's package
through `_absolute_module`, and all three fixtures this entry asks for are live
and green in one parametrization at `tests/test_review_queue.py:2196`, the
sibling form, `from . import <module>`, and the two-level form. The merge also
found and fixed a forwarding defect that existed only in the union of the two
sides, written up at `tests/_source_guards.py:258`.

The half that is about the COLLAPSE is not done, and this entry stays open
against it. `main` holds `ImportsOf` and `ExitCodeImports` in one file, so it
holds two relative resolvers, `_absolute_module` and `_relative_module`, the
second reachable only through `_import_targets`. The two were driven against
each other at the merge and agree on every case checked, so the collapse is now
deduplication rather than a defect fix: see R-111 for the measurement.
`SoftDeleteNames` on the parked branch `fix/conformance-3-and-soft-delete-reader`
still matches by dotted tail, read 2026-08-15 at that branch's tip `897ef12`,
unmoved since 2026-08-03.

---

## R-58. One check in this unit is unreachable. The other five were reachable and are now driven

**Found:** during U38's third review round, 2026-08-03, as "six checks, correct,
kept, and unobservable". **Corrected in the fourth round, 2026-08-03**: that
header said each had been "verified to be genuinely unreachable rather than
merely undriven", and for five of the six that was false. Two of them run on
every suite pass. Instrumenting the file and running the suite is what settled
it, rather than reading the code and reasoning about it, which is how the wrong
answer was reached the first time.

A comment asserting unreachability for reachable code is worse than no comment.
It tells the next reader not to look, and the reason it gives is checkable and
wrong, so anybody who does look finds a file that argues with itself.

What the instrumented run actually counted, per suite pass:

1. `resolve_int`'s bool exclusion, `tests/_source_guards.py`. **464 arrivals.**
   `CORRECT_A_RETRY_FLAG_PER_CAUSE` maps one cause to `True` and another to
   `False`, so the comment's reason, that nothing in the tree or the fixtures
   maps a cause to a boolean, was false against a fixture in the same file. It
   changes no OUTCOME, because 1 and 0 are both below the reserved range, which
   is a fact about the range. Now asserted directly by
   `test_a_boolean_is_not_an_integer_here`.
2. `resolve_int`'s `int(...)` branch. **25 arrivals.** `process_status_literals`
   resolves the argument of every single-argument call it walks, so
   `sys.exit(int(code))` arrives here rather than at `status`'s own conversion
   branch. Not defence in depth: a LIVE bypass. Without it,
   `sys.exit(int(PRECONDITION))` resolves to nothing and the bare status guard
   goes quiet. Driven by
   `test_a_status_with_a_conversion_round_it_still_reaches_the_shell`.
3. `status`'s one-argument narrowing on a conversion. Not reached in the
   discriminating case, because no fixture wrote a two-argument call. That is
   UNDRIVEN, not unreachable: a two-argument call is ordinary Python.
   `CORRECT_A_TWO_ARGUMENT_CALL_IS_NOT_A_CONVERSION` writes one now, and
   dropping the narrowing reports it.
4. `names_the_class`'s module-qualified branch. Same shape: undriven, not
   unreachable. `exit_codes.ExitCode(30)` is what a module that imported the
   vocabulary as a module writes.
   `test_a_conversion_is_read_through_the_module_name_as_well_as_the_class_name`
   drives it.
5. `_index`'s band check and its `verb_producible` check,
   `src/cratekit/cli/exit_codes.py`. **THE ONE THAT IS GENUINELY UNREACHABLE.**
   Every `ExitCode` member inside the reserved range sits in a reserved band and
   is verb-producible, and the range check above rejects everything else, so no
   member can reach either raise. Kept because each states a different rule from
   the range: the range is a span of integers and these two are about what the
   span means, so a band renumbered or a meaning changed to non-producible fails
   by name rather than passing because the arithmetic still holds. Unchanged.
6. `structured_refusal_causes`'s inner unimportable assertion,
   `tests/test_reserved_causes.py`. Executed on every call and never true, which
   is a fact about the tree importing rather than about the code. Duplicated by
   `test_every_module_in_the_package_imports_so_the_walk_can_see_it`, which is
   why deleting it stayed green.
   `test_the_derivation_refuses_to_answer_from_an_incomplete_walk` hands the
   derivation a short answer and now kills it.

The `setdefault` branch in `ReservedCodeTable.pairs` is the seventh and its
comment was already accurate: redundant rather than unreachable, because the
catch-all that crosses every call's arguments reaches `setdefault` too. It stays
because it binds the key to ITS value by position instead of crossing them.
Instrumenting counted 5 arrivals, which agrees with the comment.

The `seen` dedupe in `reserved_code_tables` was the eighth and nobody recorded
it. Deleting the set and the membership test killed ZERO tests, because no
fixture anywhere wrote a construct that produces the same line, slug and status
twice. It is code with nothing watching it, which is the exact shape this section
exists to list, and it was not on the list. It is DRIVEN now rather than
recorded: a duplicate key in a second table, which is the first defect this
unit's own suite hunts, reaches the walk as two identical pairs, and
`test_a_duplicate_key_in_a_second_table_is_reported_once` fails without the
dedupe. Reporting one reservation twice makes the count in the failure message
wrong, and the count is what a reader uses to size the problem.

`MAX_HOPS` was on this list and is NOT any more. Its ceiling, that a mutually
recursive pair cannot hang the suite, is driven by
`test_a_mutually_recursive_pair_of_constants_resolves_to_nothing`.

Its FLOOR was still a claim of exactly this kind, and the fifth round deleted it.
The fourth round's docstring said "Lowering it stops the guard resolving the
careful spellings and kills seven tests". Swept across every lower value: 0 kills
nine, 1 kills two, and 2, 3, 4 and 5 each kill NOTHING. No lowering killed seven,
and the constant was over provisioned by four because nothing in the suite needed
more than two hops. It is 3 now, and
`test_the_hop_bound_is_the_depth_of_the_deepest_spelling` asserts the deepest
spelling resolves AT the bound and goes silent one below it.

**And "nothing in the suite needed more than two hops" is defect one again**, in
the sentence that set the value. A coverage constant justified by what no fixture
happened to write is a constant nobody measured the cost of. `MAX_HOPS` is a
COVERAGE DIAL: at 3 the guard reads at most two aliases before the literal, and a
three alias chain is a real evasion that is silent. The sixth round did not raise
it, because the give-up is the same KIND at any finite value and raising only
moves it; it wrote the give-up down instead, pinned in both directions by
`test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up`. The
residual "The tiers were bought with a number that does not exist" has the
shapes.

**Closes when:** nothing has to close it. It is a record of ONE deliberate
retention, plus the correction of a claim that was made about five others, so a
later reader deleting the survivor for being untested knows it was already looked
at and knows what "looked at" was worth the first time.

---

## R-59. Two refusal vocabularies stay outside the second-table guard's key set

**Found:** during U38's third review round, 2026-08-03. Amended in the fifth,
2026-08-03, when the fourth round's two tiers were removed.

The guard reports a second reservation only for a key somebody DECLARED to be a
refusal cause. That set is four declarations wide and one rule wide: the
reservation table, the package-wide derivation, a source's own enums, and the
closed reason registry `core.cause.REASONS`, with a bare integer in the reserved
range reserving any of them. See the residual
"The tiers were bought with a number that does not exist" for why the registry
is carried on the same rule as the rest.

Two vocabularies are still outside it, both deliberately:

**`preflight.MountState`.** Seven states, spelled with underscores rather than
this repository's hyphens, and `core/session.py` converts every one of them into
a slug the registry already reserves before anything refuses. Adding them would
put the bare string `"ok"` into the key set, and `{"ok": 30}` is a mapping
somebody will write for an unrelated reason. Measured cost of leaving them out: a
module mapping `"not_mounted"` to a code of its own is not reported.

**The tokens carried by the refusals in `CONVERTED_ELSEWHERE`.** Twenty one
strings, and most of them are remediation tokens rather than causes:
`fix-config-values`, `switch-adapter`, `retry-later` and their neighbours. Adding
them would widen the fourth item of the residual
"Five accepted findings from the U38 reviews", where a duration in range keyed
by a declared cause reads as a status, from the causes to the remedies, and
`{"retry-later": 30}` is precisely the backoff that residual describes.

Both widenings were driven over the real tree and both find zero offenders today,
so neither is being avoided because it would fail. They are avoided because the
first false positive either one produces is the one that gets the whole guard
suppressed, which is how the armed review guards were switched off once already.

The sixth round measured the ceiling on that argument. Adding EVERY kebab shaped
string literal in the package to the key set, 189 distinct with 108 that are not
keys today, which is far wider than either widening above, still finds ZERO
offenders outside the two table owners. So the exclusions here are a judgement
about future false positives rather than a defence against present ones, and the
guard's headroom is measured rather than assumed.

**Closes when:** nothing has to close it, unless a module lands that genuinely
maps one of those strings to an exit code, in which case the answer is to give
the condition a real slug in the closed registry rather than to widen the key
set.

---

## R-60. The conversion proof shows that a conversion exists, not that it keeps anything

**Found:** during U38's third review round, 2026-08-03.

`test_every_exclusion_names_a_refusal_something_already_converts` checks each
entry in `CONVERTED_ELSEWHERE` against the tree: something in this package
catches that CLASS and uses what it bound. Both halves of that were name matching
once. The class half was fixed in the round before this and the "inspects" half
was not, so it asked whether the bound name appeared with an attribute read
anywhere in the same FILE, which nearly every handler in this package satisfies
because nearly every handler calls its binding `exc`. Removing that half killed
zero tests. It is scoped to the handler now, and driven by
`test_the_conversion_proof_is_scoped_to_the_handler_that_bound_the_exception`.

What it still cannot say is whether the conversion is LOSSLESS, and there is a
live example: `core/session.py:1026` catches `BackupFactsUnreadable`, reads
`exc.path`, and hardcodes `Remedy.REPAIR_BACKUP_FACTS`, discarding the remedy the
exception carried. That is item 2 of the residual
"Five accepted findings from the U38 reviews". That handler satisfies this
proof and should.

The alternative is a rule about WHICH attributes a handler must read, and that is
a rule an ordinary refactor breaks, which puts it in the same family as reading a
role from a parameter name. So the proof answers the question it can answer, and
the losslessness question is answered by item 2 of the residual
"Five accepted findings from the U38 reviews" and by the one line that closes
it.

**Closes when:** nothing has to close it. Item 2 of the residual
"Five accepted findings from the U38 reviews" closes the live instance.

---

## R-61. The tiers were bought with a number that does not exist, so there is one key set again

**Found:** during U38's third review round's verification, 2026-08-03. Answered
with two tiers in the fourth round. **The tiers were removed in the fifth round,
2026-08-03**, because the measurement they rested on was taken against a hand
written fixture rather than against this repository. **The fifth round's own
counts were wrong in four places and its escape hatch was an off switch for the
whole guard; the sixth round, 2026-08-04, measured every number in this section
and deleted the hatch.**

### What was claimed, and what the tree says

The fourth round's argument was that the wide key set over fired: "twenty seven
of twenty eight ordinary constructs keyed on a registry slug were reported". That
twenty eight construct set is not in this repository. It was never in this
repository. Measured under the wide single key set rule against every file
`package_sources()` returns, **51 of them, 43 modules and 8 package
`__init__.py`, none empty**:

**ZERO offenders outside the two files that own a table.**

The fifth round wrote that same set as "all sixty plus real modules in the
package" in two places. It is 51 files and 43 modules, so the sentence overstated
the scope by ten and counted package inits as modules.

**THERE IS NO HEADROOM PROBLEM EITHER**, which is the measurement that settles
what to do about the escape hatch below. Adding every kebab shaped string literal
in the package to the key set, 189 distinct literals of which 108 are not keys
today, still measures **ZERO** offenders outside the two table owners. The wide
rule is not close to over firing here; it has 108 keys of slack.

### The headroom measurement was taken on the key set, and the round moved the resolver

**That measurement is over what counts as a CAUSE. The sixth round changed what
counts as a KEY**, and it deleted the per-statement escape on the strength of the
key-set number. Both halves are re-measured here against the RESOLVER, in this
worktree, on the shipped tree.

What did not change:

* With the resolver ON and the registry key set of 82, the package reports
  **ZERO** offenders outside the two table owners, and 22 and 61 inside them.
* With the resolver ON and every kebab literal added, **190 keys**, still
  **ZERO** outside.

### The two halves of that comparison were measured on two different bases

**Found by the seventh round's verifier, 2026-08-09, and this is the correction.**
The section below used to carry "10 and 14" for the named surface and "25 and 5"
for the literal surface and set them against each other as one comparison. They
were not one comparison. The named figures reproduce only over ALL 51 files, the
two exempt table owners included, with every assignment anywhere counted, which
is WIDER than the resolver that ships. The literal figures reproduce exactly over
the 49 non-owners with the narrow rule. **The conclusion survives and the
symmetry of the argument did not**, so both halves are re-measured here on one
basis and every figure is now recomputed from the tree by
`test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned` rather than
carried in prose.

**THE BASIS, once, for everything below.** The population is the **49 non-owner
files** `package_sources()` returns, the two table owners excluded because the
guard exempts them. The resolver is the shipped `ReservedCodeTable.cause_key`,
asked of every `ast.Name` and `ast.Attribute` in the file, with the file's own
package passed so a relative import resolves exactly as it does in the live scan.

What the distance to an offender is, on that basis:

* **8 modules** hold a name the key side resolves to a cause declared somewhere
  ELSE, in the reservation table, the registry, or the package-wide derivation.
* **13 modules** hold one once each file's own enum declarations are counted,
  which is what `ReservedCodeTable` actually reads. The five that only the own
  declarations reach are `acquire/download.py`, `core/exit_codes.py`,
  `core/review.py`, `core/secrets.py` and `write/routing_pass.py`.
* **4 of those 13** also hold an in-range integer literal, so one ordinary
  mapping in any of the four is what an offender would look like:
  `core/exit_codes.py`, `core/review.py`, `core/session.py` and
  `modules/tools/mastering.py`.
* `src/cratekit/core/exit_codes.py` is the sharpest, and its figures are counted
  over DECLARATIONS rather than over uses, which is the distinction the old text
  did not make: it declares **42** cause-shaped strings in its own `Remedy` enum,
  **6** of which are also keys of the reserved table, it holds **28** in-range
  integer literals, and it is NOT in `TABLE_OWNERS`.
* `TrackOutcome` at `src/cratekit/acquire/adapter.py` is real, and
  `RETRY_SECONDS = {TrackOutcome.UNAVAILABLE_TRANSIENT: 30}` is reported.

**The widening is kept**, and the comparison is now like for like. On the SAME 49
files under the OLD constant-only key rule, **24 modules hold a cause literal and
5 of them also hold an in-range integer**. So the named surface the widening
added, 13, is smaller than the literal surface, 24, that the tree has carried and
the suite has accepted since the fifth round. Every one of those four constructs
already fired in its inline spelling, so the widening added a second SPELLING to
an accepted residual rather than a new class of false alarm. That ordering is
asserted rather than described: if the named surface ever exceeds the literal
one, the pinning test fails and says to re-argue this paragraph or narrow the key
side.

**RE-MEASURED AT TWO LATER MERGES, and the figures above are left standing as
what was measured on the day.** Every number in this section was taken on the
tree of its own round, and rewriting them in place would destroy the record of
what the argument was actually bought with. The re-measurements are appended
here instead, and each one was forced by the pinning test failing, which is the
review those numbers exist to trigger:

* **U38 merge, 2026-08-10.** U24 and U34 landed modules and causes. Named
  surface 13 to 17, literal surface 24 to 36, cause population 82 to 100.
* **U16 merge, 2026-08-13.** `acquire/match.py` is the one module added. Named
  surface 17 to 18, literal surface 36 to 38, cause population 100 to 101 on a
  single appended slug, `intake-list-unusable`.

The comparison this section rests on survived both, and it widened rather than
narrowed each time: 13 against 24, then 17 against 36, now 18 against 38. The
half that would have been evidence of a problem, the modules holding a name
resolving to a cause declared somewhere ELSE, has been **8 through all three
measurements** and no merge has moved it.

Narrowing the key side instead was rejected on a measurement, not a preference. A
narrowing that reads an inline string and not the name holding it puts one
question back to two answers decided by spelling, which is the defect this round
closed in `_branches`. And it would not work: `_declared_enum_values` treats a
cause-shaped value in a source's own enum as a DECLARATION in that file, so
`"unavailable-transient"` is a cause inside `adapter.py` before the registry is
consulted, and the inline spelling of the same key would still fire.

`RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME` is what documents and pins it. The
fixture that already documented this surface,
`RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS`, contains **zero** non-literal
keys measured off the syntax tree, so it covered the half of the residual that
predates the widening. Both fixtures now carry a key-kind assertion, `Constant`
18 for one and `Attribute` 5 plus `Name` 3 for the other, so neither can drift
into the other's spelling without failing.

The over fire the tiers were built to stop does not occur. What the tiers cost is
not hypothetical, and this is the count the fifth round got wrong three different
ways inside one commit. Round four's gate, re-implemented verbatim and run over
`REGISTRY_SLUG_SECOND_TABLES`, the sixteen entry fixture tuple this suite ships:

**the tiers REPORT TWO and are SILENT ON FOURTEEN.**

The two they report are `EVASION_A_NAMED_CODE_FOR_A_REGISTRY_SLUG` and
`EVASION_A_CONVERSION_ON_A_REGISTRY_SLUG`. The fifth round wrote "fifteen of
fifteen reported by the wide rule and NONE by the tiers" in the guard, "sixteen,
thirteen silent" here and in its commit body, "sixteen, thirteen silent" in one
test docstring and "drives fifteen" in another. Four spellings of one
measurement, no two agreeing, and none matching it. Every copy says two and
fourteen now.

### Every number in this section is now recomputed from the tree

**Found by the seventh round's verifier, 2026-08-09.** Six places in this section
carried a population or headroom figure and NOT ONE of them was held by an
assertion. The justification for keeping the key-side widening therefore decayed
silently as the tree grew: a module landing next week could move any of these and
nothing would say so, which is the same defect as a docstring claiming a property
nothing measures, aimed at a document instead of at a function.

`test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned` recomputes
the key set sizes, the kebab literal population, the zero offender result under
the widened key set, both at-risk populations and the `core/exit_codes.py`
figures, and fails naming the number that moved. Its failure message says to
update this section rather than to widen the assertion, because the number
existing to trigger a review is the whole point of writing it down.

### The enum classification was a spelling too, and measurement could not see it

**Found by the seventh round's verifier, 2026-08-09.** `_declared_enum_values` is
what decides that a module has DECLARED a string to be one of its causes, and
everything downstream of that decision rests on how it recognizes an enum. It
recognized one by the spelling of the base, `endswith("Enum")`, under a docstring
that set the rule against a rename-defeatable one: "matched on the BASE being an
enum, which is how Python spells an enum, not on what the class or the variable
holding it was called."

The rule was a spelling and the spelling was defeatable. `from enum import
StrEnum as Vocabulary` binds the base to a name no suffix matches, which is the
one `as` keyword this file complains about in other people's code. And the
measurement could not tell the rule apart from an arbitrary one: **every enum
base written anywhere in `tests/` was `Enum`, `StrEnum` or `IntEnum`**, so
narrowing the suffix to exactly those three names **killed zero of 3379**.

There are two clauses now, and each has a case only it answers. A base BOUND from
the `enum` module in any spelling, which is what an aliased import needs. A base
whose spelling ends in `Enum`, which is what a base defined in another of our own
modules needs, since the subclassing file imports nothing from `enum` at all.
`test_an_enum_is_recognized_by_its_base_and_each_clause_has_its_own_case` drives
both plus the plain class that must stay silent, and
`test_renaming_the_enum_or_the_name_holding_it_changes_nothing` drives the
docstring's own claim across four renames instead of asserting it.

**What is still not read is written down rather than left to be found**: a base
from another module whose name neither ends in `Enum` nor is one the `enum`
module exports. Reading that needs the base's OTHER file, which no question in
`tests/_source_guards.py` opens.
`test_the_static_enum_rule_agrees_with_the_interpreter_over_the_whole_package`
measures the limit against the tree instead of assuming it: every class the
package defines that IS an `enum.Enum` at runtime, 45 of them and 19 declaring a
cause-shaped value, has to be one the static rule found.

### This section was also wrong about the rule it documented

The old text said the second tier accepted "an `ExitCode` member in any import
spelling or a conversion wrapped round one". Measured, for all sixty registry
keys, every one of these was NOT reported:

- `{"config-unusable": ExitCode(30)}`, which IS a conversion wrapped round the
  vocabulary.
- `{"config-unusable": exit_codes.ExitCode(30)}`, which is the fixture the fourth
  round itself added to drive the fourth entry of the residual
  "One check in this unit is unreachable", only ever run with a key the
  narrow tier did not apply to.
- `class Code(IntEnum): PRECONDITION = 30` then
  `{"doctor-check-failed": Code.PRECONDITION}`, a module declaring its own status
  enum, which is the most flagrant second table there is.
- `PRECONDITION = 30` then `{"module-extras-missing": PRECONDITION}`.
- `BASE = 30` then `{"anlz-modified": BASE + 3}`.

### Why the wide rule is the right trade

The two error costs are not symmetric, and the fourth round had them backwards.

- A FALSE ALARM costs one developer one look and either a fix or one annotated
  line. It is loud, immediate, local and reviewable.
- A MISS is a module shipping a second reservation table that silently diverges
  from the registry, which is the entire thing this guard exists to prevent and
  which nothing else in the suite would notice.

For a guard of this shape the loud direction is correct. So `declared_causes()`
is one set of eighty two keys again, with one value rule for all of them, and
`reserved_code_tables` has no second key set parameter at all. The fourth round's
`named_only_causes` defaulted to empty with a docstring claiming a caller that
forgot it "loses coverage loudly"; it did not, because the tree-wide scan asserts
an ABSENCE, so dropping the tier made it quieter and greener. A defaulted
parameter that weakens a guard when omitted is the wrong shape, so there is
nothing to omit.

### The escape hatch was an off switch for the whole guard, and it is deleted

The fifth round answered the residual with `# not-a-reservation: <reason>` on a
line, and made three claims for it: it silences one statement, it is never a
`def` body, and its blast radius is visible from where it is written. **All three
are false, measured against the shipped implementation.**

| The claim | What it measures |
| --- | --- |
| "silences that one statement" | `A = {...}; B = {...}  # not-a-reservation: one reason` reports 2 hits without the comment and 0 with it. One reason, two statements. |
| "never a `def` body" | `def build(): return {"config-unusable": 30}  # not-a-reservation: honest` reports 0. The mark and the body are one physical line, so the line rule covers the body. `pyproject.toml` selects `["E9","F","I"]`, so `E704` is off and a one line `def` passes the battery. The fixture that drove this used the multi line spelling only. |
| "blast radius visible from where it is written" | One comment appended to `src/cratekit/core/cause.py` line 158, `REASONS: Mapping[str, ExitCode] = MappingProxyType(`, takes that file from **61** reported reservations to **0**. The silenced span runs from line 158 to line 372, so the furthest silenced line is 214 below the mark. The exact-membership failure message reported the line and the reason and never how many reservations went quiet. |

**Deleted rather than repaired.** The hatch existed to make the wide rule's false
alarms cheap, and the measurement above says the wide rule has no false alarms
here to make cheap: zero offenders, and still zero with 108 extra keys. It was
never used once. Repairing it means making three claims true at once, one
statement in every spelling, never a function body in any spelling, and a blast
radius reported as a count of silenced reservations, for a mechanism nothing in
the tree needs.

Dropping `TABLE_OWNERS` instead is not the alternative. Each owner's reservations
sit inside a SINGLE statement, so two comments would have covered both files
entirely. That is the third row of the table again, not an escape from it.

What replaces it is nothing, deliberately. The residual is REPORTED and the
answer to a real one is a decision recorded in the suite: either the value is a
reservation and belongs in the table, or the file joins `TABLE_OWNERS` with a
reason beside it and `test_the_table_owner_escape_is_exactly_these_two_files`
updated. That is the review a silenced guard never gets otherwise.
`test_a_comment_cannot_silence_a_reservation` keeps the whole residual fixture
carrying the old comments and asserts every hit still fires.

### The absence was pinned by the deleted hatch's FINGERPRINT, not by the property

**Found by the seventh round's verifier, 2026-08-09, and it is a new and sharp
form of "identity that is not unique to the thing it identifies".**
`test_the_guard_has_no_per_line_off_switch_at_all` asserted that
`_annotated_lines`, `_silenced_lines` and `NOT_A_RESERVATION` are absent and that
`tokenize` is not in the module. Those are the names the DELETED implementation
used. **A fresh per-line escape hatch with a different marker, no `tokenize` and
none of those three names ships green, wired in exactly where the deleted one
was.** Measured: it was written, wired in, and killed nothing.

**Generalise it, because the replacement has to be the general one: a test that
forbids a feature by naming the last implementation's symbols forbids that
implementation, not the feature.**

Three things replace it, and none of them knows a marker.

* `test_a_comment_cannot_change_what_the_guard_reports_whatever_it_says` is the
  PROPERTY. A comment cannot survive a round trip through the syntax tree, so
  every source has a comment-free twin one `ast.unparse` away and the two answers
  have to match whatever the comment said. Driven over the two table owners from
  the real tree, 22 hits and 61, and over five plausible fresh markers appended
  to every line of the residual fixture.
* `test_the_guard_cannot_be_given_a_comment_because_it_cannot_read_the_text` is
  the STRUCTURAL half, so a future hatch is impossible rather than merely
  undetected. A comment can only reach a rule through the RAW TEXT, so the text
  is followed from the `source: str` parameter that receives it through every
  name it is assigned to and every function of the module it is passed to, and
  the only thing it may touch is `ast.parse`. Both directions are driven: the
  shipped module answers clean, and the same module with a fresh hatch wired in
  answers with the hatch's own line.
* `test_the_guard_module_imports_only_what_reading_a_syntax_tree_needs` closes
  the other route by EXACT MEMBERSHIP rather than by naming `tokenize`. The
  module may import `ast` and `re`. Anything that can see a comment costs one
  line there and the review that line brings, which is the review the escape
  hatch never got.

`test_nobody_in_the_package_writes_the_marker_that_was_deleted` keeps the old
fingerprint on purpose and is about PEOPLE rather than about the guard: somebody
who remembers `# not-a-reservation:` and writes it would otherwise be ignored in
silence.

### The residual, written down rather than narrowed away

`RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS` produces **eighteen HITS from
eleven CONSTRUCTS**, keyed on cause slugs with in-range integers: a poll interval
of 30, a display order of 10 20 30, a column width of 40, a schema version of 11,
a retention of 30 days, a share of 50 percent. Every one is REPORTED and the list
is pinned exactly.

Three different numbers describe that one fixture and the fifth round used one
word for all three. Eighteen is the HITS. Eleven is the constructs that produce a
hit, which is what the fixture's own comment says. Thirteen is the node count in
`_construct_shapes`, which also counts the `SENTENCES` mapping and the empty
`DELAYS` literal, both dict literals that produce no hit. The assertion messages
now say which number is which.

The fourth round's version of that fixture said its value was covering eleven
distinct construct SHAPES and asserted only the slugs, the values and the line
numbers, so swapping a construct for a different shape carrying the same data on
the same line left every assertion true: four swaps out of four went undetected.
The shapes are asserted structurally now, off the syntax tree rather than off the
report.

### Not narrowed to the eighteen integers the enum actually uses

Still the rejected alternative, and the rejection is honest now. The fourth round
rejected it because it "blinds the guard to a new module inventing 33", while its
own scheme was blind to `{"tree-registry-unusable": 33}` for sixty of the eighty
two keys. `test_the_alternative_is_not_rejected_for_a_flaw_this_scheme_shares`
drives that input, and the mutation table has the narrowing as a row.

### Seventeen shapes were silent, not three, and the largest was not an import spelling

The fifth round recorded three still-silent import spellings. **Measured, the
number is fourteen and the two largest are not import spellings at all: the guard
resolved the VALUE of a pair through names and never resolved the KEY.**
`cause_key` required an `ast.Constant`, so this was silent while its inlined
spelling was reported:

```python
CONFIG_UNUSABLE = "config-unusable"
CODES = {CONFIG_UNUSABLE: 30}          # SILENT
```

and so was `{Slug.CONFIG_UNUSABLE: 30}`. The package already carries **37 class
attributes whose value is a declared cause**, for example
`TrackOutcome.UNAVAILABLE_PERMANENT` in `src/cratekit/acquire/adapter.py`, so
that is the tree's own idiom rather than an invented one. The fifth round's argument for resolving values, that "a
bare 30 in a mapping tells a reader nothing", is symmetric and was applied to one
side only.

**"One machinery answers both sides now" was written a round early and was
false.** The widening reached FOUR constructs that hold a key in a subtree and
missed TWO, because the `match` arm of `_branches` passed its pattern value into
`cause_key` unfiltered and inherited it while the `if` arm and a dict
comprehension's iterable each pre-filtered their subtree to `ast.Constant` first.
Measured on the shipped tree before this round:

```python
match cause:
    case Slug.CONFIG_UNUSABLE: return 30          # REPORTED
if cause == Slug.CONFIG_UNUSABLE: return 30       # SILENT
if cause == CONFIG_UNUSABLE:      return 30       # SILENT
if cause == "config-unusable":    return 30       # REPORTED, the control
CODES = {slug: 30 for slug in (CONFIG_UNUSABLE, SMOKE)}   # SILENT
CODES = {slug: 30 for slug in ("config-unusable", ...)}   # REPORTED, the control
```

The first pair is one table written two ways and the guard read one of them.
Every construct that finds its keys in a subtree asks `cause_keys_within` now, so
the claim is a structure rather than a sentence: widening what a key can be
widens all of them together or none of them.

Seventeen shapes measured, **nine closed and eight recorded**. The enumeration
was written down as fourteen with six closed and eight recorded; this round found
two more shapes and split one recorded row in half, closing the vocabulary side of
it. It grew by three the round after it was called complete, which is the argument
for writing it down:

| Shape | Now |
| --- | --- |
| a key held in a module constant | CLOSED |
| a key held on a class attribute | CLOSED |
| a list of record dicts, `[{"cause": ..., "code": ...}]` | CLOSED. `_crossed` already read the tuple and the constructor spellings of one record and not the dict one. |
| `getattr(ExitCode, "PRECONDITION")` | CLOSED. `ProcessExits` has recognized `getattr(sys, "exit")` since round two and called it the shape that matters most; this half of the same file did not recognize it. |
| a code reached by `//` | CLOSED. `resolve_int` read `+`, `-` and `*` and not these two. |
| a code reached by `%` | CLOSED. |
| `if cause == Slug.X` and `if cause == CONSTANT` returning a code | CLOSED. The fifteenth shape, found this round, and the direct twin of `case Slug.X`, which was already reported. One method, two arms, two answers. |
| a dict comprehension over NAMED slugs, `{slug: 30 for slug in (CONFIG_UNUSABLE, ...)}` | CLOSED. The sixteenth shape, found this round. The same comprehension over inlined slugs reported both keys. |
| `ExitCode(0)` and `ExitCode(126)`, the vocabulary at a value outside `[10, 60)` | CLOSED. `{"config-unusable": ExitCode.SUCCESS}` was reported and its constructor spelling was silent, because the conversion branch returned only when the inner expression was already a status and `status` answers None out of range. A member and its constructor spelling are one code, so the range cannot gate one of them. Narrowed to an argument that RESOLVES to an integer, so `ExitCode(document["exit_code"])`, which `cli/output.py` writes, reserves nothing. |
| `{"config-unusable": {"code": 30, "remedy": ...}}`, the record dict as the VALUE | recorded, and the reason the round before gave for it was OVERSTATED. It said closing it "pairs a cause with any in-range integer anywhere inside a nested structure". A ONE LEVEL rule, crossing the outer key against the inner dict's values, is bounded, costs one level rather than unbounded depth, and is the exact mirror of the record dict as a KEY set, which IS closed. The honest reason it stays open is that it has no instance in the tree and no test would drive it beyond the fixture that opened it. |
| dataclass field defaults, `cause: str = "config-unusable"` beside `code: int = 30` | recorded, and this is the RISKIEST row in the table rather than the most theoretical. `cli/exit_codes.py`'s own `Reservation` is `cause: str` beside `code: ExitCode`, so a second module copying the house style WITH DEFAULTS is the closest thing in this tree to the defect the whole guard exists for, and it is silent. It stays open because the two defaults are separate statements in a class body with nothing binding them, so pairing them is a proximity rule rather than a structural one, and a proximity rule is what fires on ordinary code. |
| parallel indexed lists, `{SLUGS[0]: CODES[0]}` | recorded. Resolving a subscript into a named sequence is a second evaluator, and `dict(zip(...))` is the spelling anybody actually writes and is already read. |
| a bare integer, a named constant or arithmetic reaching a value outside `[10, 60)` | recorded, and it is the range decision rather than a hole. Widening the bare-integer rule past the reserved range reports every count, width and percent in the package. All three of these produce an INTEGER and nothing else, so all three are governed by the range and all three are SILENT. The round before wrote "an `ExitCode` member, a conversion, a constant or arithmetic reaching an out of range value is still reported", and measured that sentence was false in three of its four clauses: `ExitCode(0)` and `ExitCode(126)` were silent, `BASE = 70` then `{"config-unusable": BASE}` was silent, and since arithmetic can evaluate to nothing but an integer the arithmetic clause was unconditionally false. The conversion clause is true now because the shape above it was closed; the constant and arithmetic clauses are withdrawn. `test_an_integer_outside_the_reserved_range_is_silent_however_it_is_spelled` pins all three. |
| a chain of three or more name aliases | recorded, and it is `MAX_HOPS` at 3. See below. |
| `import cratekit.core` then `cratekit.core.exit_codes.ExitCode.X` | recorded, pre-existing. The walk binds a name to the module or to the class and a partial package import reaches neither. |
| `from cratekit import core` then `core.exit_codes.ExitCode.X` | recorded, pre-existing. Same shape one spelling further out. |
| `from .exit_codes import *` | recorded. `ruff` fails it on F403 and F405, so a module that wrote it never reaches the suite. |

### `MAX_HOPS` is a coverage dial and the docstring did not say what it gives up

The constant is correct at 3 and load bearing in both directions: 2 kills a test,
4 kills a test, 6 kills a test. What was missing is what 3 BUYS and what it
COSTS. The reduction from 6 was justified with "nothing in the suite needed more
than two hops", which is this repository's recurring defect one, absence read as
evidence of absence, applied to a coverage constant.

It is not a correctness constant. Any finite value below the interpreter's
recursion limit stops the hang the bound exists to prevent. The value decides how
long a chain of aliases the guard can read: at 3 it reads at most TWO aliases
before the literal, at round four's 6 it read five, and

```python
A0 = 30; A1 = A0; A2 = A1; A3 = A2
CODES = {"config-unusable": A3}
```

is SILENT at 2 and 3 and reported at 4, 5 and 6, so the boundary sits exactly
between 3 and 4. The two alias chain is reported at every one of those values.
That silence is the price of the number and is pinned in both directions by
`test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up`, so raising
the constant fails a test and demands the new boundary be written down the same
way.

**Closes when:** nothing has to close it. If a real module ever meets the
residual, the answer is a reservation in the table or an entry in `TABLE_OWNERS`
with the membership assertion updated. If one of the recorded shapes above ever
appears in the package, the row that describes it is what says what the walk
needs.

---

## R-62. The mutation table for this unit's guards, written into the repository

**Found:** the fourth round's verifier could not find the fourth round's mutation
table anywhere: not in the worktree, the repository, or any file. Only the
claimed counts existed, so a row by row comparison was impossible. A table that
exists only in a chat message cannot be checked by the next person, so this one
lives here.

**CITE THIS SECTION BY ITS TITLE, never by its number.** Six residual numbers
collide across the branches in flight in this wave, each meaning something
different on each side, so a citation by number silently points at another
subject after a merge. Every citation in this unit's source, tests and guards
names the residual's TITLE, and
`test_every_residual_this_unit_cites_is_cited_by_title` asserts that each cited
title is a real heading in this file and that no file this unit owns has gone
back to citing by number. At merge time this table belongs appended to
`docs/mutation-rows.md`, which carries the convention that a count with no row
definition beside it is not evidence.

### THE HEADLINE CLAIM BELOW WAS AN INSTRUMENT THAT COULD NOT FAIL, and the current table is elsewhere

**Found by the seventh round's verifier, 2026-08-09.** The paragraph that follows
this one closed with "Zero rows would be findings and there are none", over a 49
row table. An independently derived 83 row table over the same tree found SEVEN
unaccounted zero rows. The claim was not false about the rows it listed; it was
a claim about a POPULATION, "every guard, assertion and constant this unit
ships", made by a table that chose its own rows. A completeness claim whose
population is the author's own list cannot fail, which is this session's most
common defect in its own tooling.

**What replaces it.** The eighth round's table is
`docs/mutation/u38-round-8.md`, with the exact substitution and the dying node
ids for every row in `docs/mutation/u38-round-8-reverts.json` beside it. It states
its population as a countable thing rather than as a claim: **162 rows**, derived
mechanically from this unit's diff against the merge base, covering every guard
clause, whitelist entry and constant in `tests/_source_guards.py`,
`src/cratekit/cli/exit_codes.py` and the derivations in
`tests/test_reserved_causes.py`. It reports **fifteen zero rows and accounts for
every one of them**, either as half of a composite pair or as a term measured to
be redundant with another. Sixteen zero rows were found on its first sweep and
eleven were CLOSED by fixtures rather than explained.

**It does not claim to be complete, and that is the correction.** Nothing about
162 rows proves no 163rd row exists. What the file states is what was measured,
over what, and how, so the next person can re-derive it and find the rows this
one missed, which is what the seventh round's verifier did to the table below.

**The table below is the SEVENTH round's and its numbers are stale.** It was
measured at `171e058` and this branch has three commits since, adding 26 node
ids. It is kept as the record the eighth round compared against, row by row, and
nine of its rows reproduce exactly. Read it as history and read
`docs/mutation/u38-round-8.md` as the current state.

Every guard, assertion and constant this unit ships, reverted ALONE, full suite,
deaths counted from a pytest plugin's report objects rather than from parsing the
`FAILED` lines, which cannot be split on `" - "` here because that string appears
inside parametrized ids. Baseline: **3364 passed, 15 skipped**, measured on
`unit/u38-reserved-exit-code-registry-for-module-r` after the sixth round's two
commits. Every number below was measured against THAT tree in that session.

A row NAME does not identify a mutation, so each row has its exact revert written
out below the table. Rows are ONE substitution in ONE file unless stated. Revert
from a snapshot taken before the row was applied, not with `git checkout`, or a
round's uncommitted edits go with the mutation.

**EVERY NUMBER IN THIS TABLE WAS RE-MEASURED IN THIS WORKTREE**, on the shipped
tree at the seventh round's first commit, not carried forward. The `previous`
column is the sixth round's value, kept so a move is visible rather than silent.

**HOW THE MOVES ARE ACCOUNTED FOR, and the sixth round's account of its own moves
was wrong in three ways.** It wrote that "eight of this round's new tests key on
`config-unusable`" and that four use arithmetic or a class attribute, and offered
`25 - 8 = 17` as the decomposition of `round-four-tiers-restored`. Measured by
the verifier: that is NINE node ids from SEVEN functions, so the subtraction does
not reproduce and the measured value is `25 - 9 = 16`. Eight of its twelve moved
rows decomposed exactly, three were off by one consistent with one of the two
tests that round DELETED having died at round five, and
`narrowed-to-the-eighteen-live-integers` was off by four with four of its five
extra deaths being PRE-EXISTING node ids rather than that round's.

So the account here is a SUBTRACTION anybody can reproduce rather than a
sentence. This round adds 15 node ids, from 8 functions, all in
`tests/test_reserved_causes.py`:

    test_a_branch_table_reads_its_key_the_same_way_whichever_branch_it_is   4 ids
    test_a_comprehension_reads_named_slugs_and_inlined_slugs_alike          2 ids
    test_a_constructor_on_the_vocabulary_is_a_code_at_any_value             2 ids
    test_a_constructor_wrapping_a_runtime_value_reserves_nothing            1 id
    test_an_integer_outside_the_reserved_range_is_silent_however_it_is_spelled  3 ids
    test_a_residual_heading_names_exactly_one_finding                       1 id
    test_the_covered_file_set_is_derived_and_reaches_what_the_unit_touched  1 id
    test_ordinary_data_keyed_on_a_NAME_is_the_same_residual_in_the_tree_s_own_idiom  1 id

Every row whose number moved was re-run with those 15 ids DESELECTED, and the
`previous` value reproduced exactly on all nine of the rows the sixth round's
table names as its largest. That is the check, and it is a measurement rather
than an explanation: `key-set-drops-the-registry` 38 becomes 29,
`key-set-drops-the-derivation` 38 becomes 29, `round-four-tiers-restored` 34
becomes 25, `no-module-level-literals` 19 becomes 16,
`narrowed-to-the-eighteen-live-integers` 10 becomes 9, `no-class-level-literals`
8 becomes 5, `no-arithmetic` 5 stays 5, `review-walk-suffix-match` 5 stays 5,
`no-resolution-through-names` 7 becomes 4.

| id | what it reverts | deaths | previous |
| --- | --- | --- | --- |
| `escape-hatch-restored` | the fifth round's `# not-a-reservation: <reason>` escape put back verbatim: `NOT_A_RESERVATION`, `_annotated_lines`, `_silenced_lines`, the `io` and `tokenize` imports, and the `if key.lineno in silenced: continue` filter. The sixth round's replacement comment block above `ReservedCodeTable` is NOT removed by this row and the row does not need it removed, because the block is prose and silences nothing | 2 | 2 |
| `escape-hatch-restored-with-ast-return` | the same restore, plus `ast.Return` added to the statement expansion tuple, so one comment on `return {` silences a whole multi line returned table | 2 | 2. **ZERO on top of the restore**, which is the point |
| `escape-hatch-restored-covering-a-function` | the same restore, plus `ast.FunctionDef` added to the expansion tuple, so one comment on a `def` silences its whole body | 2 | 2. **ZERO on top of the restore** |
| `key-not-resolved-through-names` | `cause_key` reverts to requiring an `ast.Constant`, so a key held in a module constant or on a class attribute resolves to nothing | 7 | 2 |
| `key-not-resolved-through-a-class-attribute` | `_resolved` drops its `ast.Attribute` branch alone, which isolates `{Slug.CONFIG_UNUSABLE: 30}` and the `StrEnum` idiom from the module-constant spelling | 4 | 1 |
| `branch-if-arm-refiltered-to-constants` | the `ast.If` arm of `_branches` goes back to filtering its test to `ast.Constant` instead of asking `cause_keys_within`, so `if cause == Slug.X` is silent while `case Slug.X` is reported | 3 | new |
| `comprehension-iterable-refiltered-to-constants` | the `ast.DictComp` arm of `pairs` goes back to filtering `generator.iter` to `ast.Constant`, so a comprehension over named slugs is silent while the inlined one is reported | 2 | new |
| `constructor-conversion-regated-to-the-range` | the vocabulary-constructor branch of `status` goes back to requiring the inner expression to be a STATUS rather than an integer, so `ExitCode(0)` and `ExitCode(126)` are silent while `ExitCode.SUCCESS` is reported | 2 | new |
| `bare-integer-range-gate-dropped` | `status` drops `not self.low <= value < self.high`, so every integer counts and the reserved range gates nothing. This is the row that says what the range BUYS, which the recorded shape asserts and nothing drove | 8 | new |
| `named-key-residual-fixture-rewritten-as-literals` | every construct in `RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME` rewritten with inline string keys, same slugs, same values, same lines. The hit list is unchanged and the fixture stops covering the spelling it exists for | 1 | new |
| `no-record-dict-crossing` | `pairs` stops crossing a `ast.Dict`'s VALUES, so a record written `{"cause": ..., "code": ...}` is not a record | 1 | 1 |
| `no-getattr-conversion` | `status` drops its `getattr` branch, so `getattr(ExitCode, "PRECONDITION")` is not a code | 1 | 1 |
| `no-floor-division-or-remainder` | `resolve_int` drops its `FloorDiv` and `Mod` branch, so `BASE // 2` and `BASE % 100` resolve to nothing | 2 | 2 |
| `seen-dedupe-dropped` | the `seen` set and its membership test deleted from `reserved_code_tables`, so a duplicate key in a second table is reported twice | 1 | 1 |
| `round-four-tiers-restored` | round four's two-tier rule put back: a key only the registry declares needs an `ExitCode` member or a conversion round one, and a bare integer proves nothing | 34 | 25 |
| `key-set-drops-the-registry` | `declared_causes()` drops `\| frozenset(REASONS)`, taking the registry's sixty slugs out of the key set | 38 | 29 |
| `key-set-drops-the-derivation` | `declared_causes()` collapsed to `return CAUSES`, dropping the derivation and the registry both | 38 | 29 |
| `key-set-drops-only-the-derivation` | `declared_causes()` drops the package-wide derivation ALONE and keeps the registry, which isolates the term that is empty in this tree | 1 | 1 |
| `package-of-collapsed` | `package_of` collapsed to `return "cratekit"`, so every relative import in the tree resolves against the wrong package | 1 | 1 |
| `max-hops-at-2` | `MAX_HOPS` lowered from 3 to 2 | 2 | 2 |
| `max-hops-at-4` | `MAX_HOPS` raised from 3 to 4 | 2 | 2 |
| `max-hops-at-6` | `MAX_HOPS` raised from 3 to 6, which is round four's value | 2 | 2 |
| `no-resolution-through-names` | `_through_names` returns its node unchanged | 7 | 4 |
| `no-resolution-through-module-constants` | `_through_names` reads only a branch's own locals, isolating `CODE = ExitCode.PRECONDITION` beside `{"rclone-missing": CODE}` | 6 | 3 |
| `no-resolution-through-branch-locals` | `_through_names` reads only module constants, isolating `code = ExitCode.PRECONDITION` then `return code` | 1 | 1 |
| `narrowed-to-the-eighteen-live-integers` | the value rule narrowed to the eighteen integers `ExitCode` actually uses, which is the alternative `ReservedCodeTable` rejects | 10 | 9 |
| `no-module-qualified-exitcode` | `names_the_class` drops its module-qualified branch, so `exit_codes.ExitCode(30)` is not a conversion | 2 | 2 |
| `no-constructor-conversion` | `status` drops the vocabulary-constructor branch entirely, so `ExitCode(30)` reads as somebody's call. **The revert is a different edit from the sixth round's**, because the branch was rewritten this round: it is now a deletion rather than a term dropped from a conjunction | 5 | 3, against the old shape of the branch |
| `no-class-level-literals` | `_class_level_literals` returns empty | 8 | 5 |
| `no-module-level-literals` | `_module_level_literals` returns empty | 19 | 16 |
| `no-arithmetic` | `resolve_int` drops its `BinOp` branch entirely | 5 | 5 |
| `table-owners-widened` | `core/session.py` added to `TABLE_OWNERS`, which switches the guard off for a whole file | 1 | 1 |
| `package-sources-narrowed` | `package_sources` from `rglob` to `glob`, so the scan stops at the top level | 3 | 3 |
| `review-walk-suffix-match` | `ReviewImports` reverted to the pre-unification two-element suffix match on `node.module` | 5 | 5 |
| `import-targets-fallback-sibling-dropped` | `_import_targets` drops the bare sibling `tail == [leaf]` clause from its fallback | 3 | 3 |
| `walk-off-the-top-clause-dropped` | `_relative_module` drops the clause that refuses a level exceeding the package depth | 1 | 1 |
| `review-leaf-hardcoded` | `ReviewImports` hard codes `leaf = "review"` instead of deriving it | 1 | 1 |
| `exit-code-leaf-hardcoded` | `ExitCodeImports` hard codes `leaf = "exit_codes"` instead of deriving it | 1 | 1 |
| `exit-code-class-spelled-again` | every `EXIT_CODE_CLASS` use replaced by the literal `"ExitCode"`. **FOUR uses on four lines at three call sites**, not three sites, which is what the sixth round's row said | 1 | 1 |
| `a-byte-identical-duplicate-heading` | a second `## R-` heading appended to this document whose text is byte identical to a cited title | 2 | new |
| `residual-headings-read-into-a-set-of-titles` | `residual_headings` deduplicates by title, which is what reading them into a `set` did | 0 | new, **paired** |
| `duplicate-heading-with-the-headings-read-into-a-set` | both of the two above at once | 0 | new, **paired** |
| `an-invented-title-in-a-covered-file` | one letter changed in a cited title inside `tests/_source_guards.py`, so the citation names no heading | 1 | new |
| `citation-reverse-direction-dropped` | the two reverse-direction assertions deleted from `test_every_residual_this_unit_cites_is_cited_by_title` | 0 | new, **paired** |
| `invented-title-with-the-reverse-direction-dropped` | both of the two above at once | 0 | new, **paired** |
| `owned-sources-hand-listed` | `owned_sources()` replaced by the sixth round's four-entry hand written tuple | 2 | new |
| `shape-swap-column-widths` | `COLUMN_WIDTHS` from a tuple of pairs to a dict literal, same slugs, values and line | 1 | 1 |
| `shape-swap-weights` | `WEIGHTS` from a tuple of pairs to a dict literal, same slugs, values and line | 1 | 1 |
| `shape-swap-comprehension` | `SLOW_DELAYS` from a dict comprehension to a dict literal, same slugs, values and line | 1 | 1 |
| `shape-swap-setdefault` | `DELAYS.setdefault` to a subscript assignment, same slug, value and line | 1 | 1 |

### The four zero rows, and why they are pairs rather than findings

A zero row is normally a finding: a guard nothing watches. These four are not,
and the reason is structural rather than an excuse. Two of the things this round
fixed only bite IN THE PRESENCE of the defect they catch, so reverting the fix on
a clean tree correctly kills nothing. What has to be measured is the PAIR.

* `a-byte-identical-duplicate-heading` kills 2 on the shipped tree. The same
  injection with `residual_headings` deduplicating by title kills **0**. So the
  list is exactly what catches a duplicate heading and the set was exactly what
  hid it, measured in both directions rather than argued.
* `an-invented-title-in-a-covered-file` kills 1 on the shipped tree. The same
  injection with the reverse-direction assertions deleted kills **0**. So the
  reverse direction is the only thing in the suite that catches a citation
  naming a heading that does not exist.

This is the shape the escape hatch rows used: a bare revert whose number means
nothing on its own gets a companion row that isolates what it is responsible for.

### The row definitions

`G` is `tests/_source_guards.py` and `T` is `tests/test_reserved_causes.py`. Each
row is the exact text to find and the exact text to put in its place.

**`escape-hatch-restored`.** Four substitutions in `G`, and it does NOT remove
the sixth round's replacement comment block above `ReservedCodeTable`. That block
is prose explaining why there is no per-line escape; leaving it in place while the
mechanism is restored is the honest revert, because the row measures the
MECHANISM and a comment silences nothing. Restore the imports:

    -import ast
    -import re
    +import ast
    +import io
    +import re
    +import tokenize

Insert above `class ReservedCodeTable:` the fifth round's

    NOT_A_RESERVATION = re.compile(r"#\s*not-a-reservation:\s*(?P<reason>\S.*?)\s*$")

with `_annotated_lines`, which walks `tokenize.generate_tokens` for COMMENT
tokens and maps `token.start[0]` to the matched reason, and `_silenced_lines`,
which unions `range(node.lineno, node.end_lineno + 1)` for every walked
`(ast.Assign, ast.AnnAssign, ast.Expr)` whose `lineno` carries a mark. Then in
`reserved_code_tables`:

    -    table = ReservedCodeTable(tree, causes, code_range, package)
    -    found: list[str] = []
    +    table = ReservedCodeTable(tree, causes, code_range, package)
    +    silenced = _silenced_lines(tree, source)
    +    found: list[str] = []

and

    -        entry = (key.lineno, slug, status)
    +        if key.lineno in silenced:
    +            continue
    +        entry = (key.lineno, slug, status)

**`escape-hatch-restored-with-ast-return`.** All four of the above, plus, inside
the restored `_silenced_lines`:

    -        if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.Expr)):
    +        if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.Expr, ast.Return)):

**`escape-hatch-restored-covering-a-function`.** All four, plus `ast.FunctionDef`
added to the same tuple.

**`key-not-resolved-through-names`.** In `G`, `ReservedCodeTable.cause_key`:

    -        held = self._resolved(node)
    -        if not (isinstance(held, ast.Constant) and isinstance(held.value, str)):
    -            return None
    -        return held.value if held.value in self.causes else None
    +        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
    +            return None
    +        return node.value if node.value in self.causes else None

**`key-not-resolved-through-a-class-attribute`.** In `G`, `_resolved`, delete the
four lines from `if isinstance(node, ast.Attribute):` through
`return node if member is None else self._through_names(member)`, leaving only
`return self._through_names(node)`.

**`no-record-dict-crossing`.** In `G`, `pairs`, replace
`found.extend(self._crossed(list(node.values)))` with `pass`.

**`no-getattr-conversion`.** In `G`, `status`, delete the whole `if (` block whose
condition is `isinstance(held, ast.Call) and _dotted(held.func) == "getattr" ...`
together with its `return as_written`.

**`no-floor-division-or-remainder`.** In `G`, `resolve_int`, delete

    -        if isinstance(node.op, (ast.FloorDiv, ast.Mod)) and right != 0:
    -            return left // right if isinstance(node.op, ast.FloorDiv) else left % right

**`seen-dedupe-dropped`.** In `G`, `reserved_code_tables`, delete
`seen: set[tuple[int, str, str]] = set()` and the three lines
`if entry in seen: continue` and `seen.add(entry)` around `entry = (...)`.

**`round-four-tiers-restored`.** Three substitutions in `G`. In
`ReservedCodeTable.__init__`, after `self.causes = ...`, add the narrow tier the
fourth round carried:

    +        from cratekit.cli.exit_codes import RESERVED_CAUSES as _RC
    +        from cratekit.core.cause import REASONS as _RS
    +        self.narrow = self.causes - (set(_RS) - set(_RC))

Add back the fourth round's `names_a_status` method verbatim, which answers True
for `self.codes.names_a_code(node)` and for a one-argument call whose function is
`int` or `names_the_class` wrapping another status. Then in
`reserved_code_tables`, above `entry = (key.lineno, slug, status)`:

    +        if slug not in table.narrow and not table.names_a_status(value):
    +            continue

**`key-set-drops-the-registry`.** In `T`, `declared_causes`:

    -    return CAUSES | frozenset().union(*derived.values()) | frozenset(REASONS)
    +    return CAUSES | frozenset().union(*derived.values())

**`key-set-drops-the-derivation`.** In `T`, `declared_causes`, replace the two
lines `derived = structured_refusal_causes()` and the return with `return CAUSES`.

**`key-set-drops-only-the-derivation`.** In `T`, `declared_causes`, replace the
same two lines with `return CAUSES | frozenset(REASONS)`.

**`package-of-collapsed`.** In `T`, `package_of`:

    -    return ".".join(["cratekit"] + relative.split("/")[:-1])
    +    return "cratekit"

**`max-hops-at-2`, `max-hops-at-4`, `max-hops-at-6`.** In `G`, `MAX_HOPS = 3`
becomes `MAX_HOPS = 2`, `4` or `6`.

**`no-resolution-through-names`.** In `G`, `_through_names`, replace its whole
body with `return node`.

**`no-resolution-through-module-constants`.** In `G`, `_through_names`:

    -        names = dict(self.constants)
    -        names.update(extra or {})
    +        names = dict(extra or {})

**`no-resolution-through-branch-locals`.** In `G`, `_through_names`, delete
`names.update(extra or {})` alone.

**`narrowed-to-the-eighteen-live-integers`.** In `G`, `status`:

    -        if value is None or not self.low <= value < self.high:
    +        from cratekit.core.exit_codes import ExitCode as _EC
    +        if value is None or value not in {int(code) for code in _EC}:

**`no-module-qualified-exitcode`.** In `G`, `names_the_class`, insert `False and`
as the first term of the returned conjunction.

**`no-constructor-conversion`.** In `G`, `status`, delete the whole
vocabulary-constructor branch:

    -            if self.codes.names_the_class(held.func):
    -                if self._as_int(held.args[0], extra) is not None:
    -                    return as_written

**`constructor-conversion-regated-to-the-range`.** In `G`, `status`, the same
branch with its inner test put back the way it was:

    -                if self._as_int(held.args[0], extra) is not None:
    +                if self.status(held.args[0], extra) is not None:

**`bare-integer-range-gate-dropped`.** In `G`, `status`:

    -        if value is None or not self.low <= value < self.high:
    +        if value is None:

**`branch-if-arm-refiltered-to-constants`.** In `G`, `_branches`, the `ast.If`
arm:

    -                found.extend(
    -                    self._returned(self.cause_keys_within(node.test), node.body)
    -                )
    +                keys = [
    +                    element
    +                    for element in ast.walk(node.test)
    +                    if isinstance(element, ast.Constant)
    +                ]
    +                found.extend(self._returned(keys, node.body))

**`comprehension-iterable-refiltered-to-constants`.** In `G`, `pairs`, the
`ast.DictComp` arm:

    -                    for element in self.cause_keys_within(generator.iter):
    -                        found.append((element, node.value, None))
    +                    for element in ast.walk(generator.iter):
    +                        if isinstance(element, ast.Constant):
    +                            found.append((element, node.value, None))

**`named-key-residual-fixture-rewritten-as-literals`.** In `T`, inside
`RESIDUAL_ORDINARY_DATA_KEYED_ON_A_NAME`, replace every named key with the string
it holds: `TrackOutcome.UNAVAILABLE_TRANSIENT` becomes `"unavailable-transient"`,
`Reason.LOCK` and `Reason.STALE` become `"session-lock-held"` and
`"decision-stale"`, and `CONFIG_UNUSABLE` becomes `"config-unusable"` in all four
of its uses. Same slugs, same values, same lines.

**`a-byte-identical-duplicate-heading`.** In `D`, which is this document, insert
above this section's own heading a second `## R-` heading under an unused number
whose text is byte identical to a cited title, followed by one line of body and a
`---` rule.

**`residual-headings-read-into-a-set-of-titles`.** In `T`, `residual_headings`,
add a `seen` set of titles and `continue` on a title already in it, which is what
reading the headings into a `set` did.

**`duplicate-heading-with-the-headings-read-into-a-set`.** Both of the two above.

**`an-invented-title-in-a-covered-file`.** In `G`, line 36, change the final
letter of the last word of the cited title from `t` to `k`, so the citation names
no heading. The mutated spelling is deliberately not written out here: this
document is inside the covered set, so a broken title quoted after the word
`residual` anywhere in it is a real citation to the scanner and fails the very
check the row exists to drive. That is the rule biting its own record, which is
the right direction.

**`citation-reverse-direction-dropped`.** In `T`,
`test_every_residual_this_unit_cites_is_cited_by_title`, replace the `undeclared`
comprehension with `undeclared = {}` and delete the
`assert set(CITED_RESIDUALS) == set(written)` block.

**`invented-title-with-the-reverse-direction-dropped`.** Both of the two above.

**`owned-sources-hand-listed`.** In `T`, `owned_sources`, replace the derivation
with the sixth round's tuple:

    -    found = {FINDINGS_DOCUMENT}
    -    for relative, text in authored_sources():
    -        if CITATION.search(text):
    -            found.add(relative)
    -    return sorted(found)
    +    return sorted(
    +        [
    +            "tests/test_reserved_causes.py",
    +            "tests/_source_guards.py",
    +            "tests/test_review_queue.py",
    +            "src/cratekit/cli/exit_codes.py",
    +        ]
    +    )

**`no-class-level-literals`** and **`no-module-level-literals`.** In `G`, make each
function return `{}` before its loop.

**`no-arithmetic`.** In `G`, `resolve_int`,
`if isinstance(node, ast.BinOp):` becomes `if False and isinstance(node, ast.BinOp):`.

**`table-owners-widened`.** In `T`, add `"core/session.py"` to the `TABLE_OWNERS`
frozenset literal.

**`package-sources-narrowed`.** In `T`, `package_sources`, `PACKAGE_ROOT.rglob("*.py")`
becomes `PACKAGE_ROOT.glob("*.py")`.

**`review-walk-suffix-match`.** In `G`, `ReviewImports.__init__`, replace the
`_import_targets(node, REVIEW_MODULE, package)` call with the pre-unification
suffix match:

    +                _tail = (node.module or "").split(".")
    +                names_the_module = _tail[-2:] == REVIEW_MODULE.split(".")[-2:]
    +                names_the_package = _tail[-2:] == REVIEW_MODULE.split(".")[:-1][-2:]

**`import-targets-fallback-sibling-dropped`.** In `G`, `_import_targets`:

    -    names_the_module = tail[-2:] == [parent, leaf] or tail == [leaf]
    +    names_the_module = tail[-2:] == [parent, leaf]

**`walk-off-the-top-clause-dropped`.** In `G`, `_relative_module`, delete

    -    if node.level - 1 >= len(parts):
    -        return None

**`review-leaf-hardcoded`.** In `G`, `leaf = REVIEW_MODULE.rpartition(".")[2]`
becomes `leaf = "review"`.

**`exit-code-leaf-hardcoded`.** In `G`,
`leaf = EXIT_CODE_MODULE.rpartition(".")[2]` becomes `leaf = "exit_codes"`.

**`exit-code-class-spelled-again`.** In `G`, all FOUR `EXIT_CODE_CLASS` uses
become the literal `"ExitCode"`. They sit on four lines at three call sites: two
on adjacent lines inside `ExitCodeImports.__init__`, one in `names_the_class` and
one in `names_a_code`. The sixth round's row said three sites and was read as
three uses.

**The four `shape-swap-` rows.** In `T`, inside
`RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS` and NOT inside
`COMMENTED_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS`, which carries the same
constructs with a comment appended and so matches the same anchor text for two of
these four, rewrite one construct as a different construct carrying the same
slugs and values on the same line:
`COLUMN_WIDTHS` and `WEIGHTS` from a tuple of pairs to a dict literal,
`SLOW_DELAYS` from a comprehension to a dict literal, and `DELAYS.setdefault(...)`
to `DELAYS["canary-read-failed"] = 15`.

### What the escape hatch rows say together

`escape-hatch-restored` kills 2. Adding `ast.Return` to the expansion set kills 2.
Adding `ast.FunctionDef` kills 2. **Both widenings kill ZERO on top of the
restore**, which is the finding that decided the hatch's fate: only the
`FunctionDef` direction was ever pinned, so the expansion set could have been
widened in every other direction without a single test noticing. A mechanism
whose blast radius can be enlarged silently, that already silenced a one line
`def` body, two statements on one reason, and sixty one reservations from one
comment, is not repaired by correcting the sentences around it.

### Two rows to read together

`key-set-drops-the-derivation` and `key-set-drops-only-the-derivation` differ by
thirty seven deaths, 38 against 1, measured in this worktree. The difference is
the registry rather than the derivation: the derived set equals `CAUSES` exactly in this tree, so the derived
term is EMPTY. The single death on the isolating row comes from
`test_the_key_set_is_the_union_of_all_three_declarations`, which swaps in a
derivation that finds a cause nobody has declared and asserts it reaches the key
set. That is the only honest way to drive a term the tree leaves empty, and the
fourth round's two assertions in its place were tautologies.

### Corrections to this branch's own record

Three claims this branch wrote about itself are wrong and are corrected here
rather than quietly replaced. All three are the same defect: a claim justified by
a written explanation rather than by a measurement.

**The commit that "corrected" a line number corrected nothing.** `d6398e1`
replaced a reference to `src/cratekit/acquire/adapter.py:137` with the class
attribute name, on the stated ground that the line number had moved. Measured:
`adapter.py:137` is exactly `UNAVAILABLE_PERMANENT = "unavailable-permanent"`,
and `adapter.py` has ZERO commits on this branch, so nothing moved. The reference
that was replaced was accurate. The replacement prose is still better, because a
class attribute name survives an edit to a file this branch does not own and a
line number does not, and that is the reason it should have given.

**"38 was never constructible" is withdrawn.** The sixth round's table carried
round four's claimed 38 deaths for `round-four-tiers-restored` beside a note that
the number could not be reproduced. Whether round four's tree could produce 38 is
not something this branch can measure, so it is not asserted in either direction.
What IS measured, in this worktree: `round-four-tiers-restored` kills **34** on
the shipped tree and **25** with this round's fifteen new node ids deselected.
For scale rather than as an argument, the maximal weakening any tier shaped
revert is a subset of, `reserved_code_tables` returning `[]`, was measured by the
verifier to kill 72, so 38 sits inside the reachable interval and nothing about
it is impossible.

**The sixth round's account of its own moved numbers did not reproduce.** That is
recorded above the table, with this round's decomposition written as a
subtraction anybody can re-run instead.

**Closes when:** nothing has to close it. It is the record the next round
compares against, row by row. The eighth round did exactly that and its own table
lives in `docs/mutation/`, which is where this one belongs at merge and where
every later round's belongs from the start.

---

## R-63. A negative process status is reserved against in prose and was covered by nothing

**Found:** by the seventh round's verifier, 2026-08-09. **Closed in the eighth
round**, 2026-08-09, by the fixtures that can see it.

`src/cratekit/cli/exit_codes.py` argues about negative statuses at length and
its argument is the reason the reserved range is safe for two different readers.
A shell reads `exit(-1)` as 255, which that file closes off by name as "what a
status above a byte truncates to". The job engine re-invokes the command line
through `subprocess` and reads `returncode`, where a negative integer is the
SIGNAL that killed the child, never 128 plus it. So one module writing
`sys.exit(-1)` produces a status that one reader calls the shell's own territory
and the other calls a signal death, and neither is the refusal that was meant.

The unit reasons about negatives in prose and **the only guard watching for a
bare status could be blinded to every one of them by either of two one line
edits, and both were silent**:

* deleting `resolve_int`'s unary minus branch, after which every negative
  resolves to nothing and a status the walk cannot evaluate stays silent;
* widening `_scan_for_exits`'s `status == 0` to `status <= 0`, after which every
  negative is read as success.

Both together were silent too. No fixture anywhere in `tests/` wrote a negative
status, in any spelling.

`test_a_negative_status_is_a_bare_status_too` writes three: the literal, the
signal number held in a name, which is the only fixture in the file that drives
the unary minus THROUGH a name, and the raised exception. It also pins that
negative zero is zero and reports nothing.

**What stays open, and it is a decision rather than a gap.**
`test_a_negative_is_outside_the_reserved_range_on_the_table_side` pins the other
half: a second table mapping a cause to a negative integer is NOT reported,
because the value rule for a bare integer is the reserved range and no negative
is inside it. That is the same rule that keeps 5 and 70 out. It also means the
unary minus branch changes no answer on the reservation side, which is why the
two tests are written to be read together: the row that deletes the branch kills
the bare status test and leaves the table test green.

**Closes when:** nothing has to close it. The bypass is covered and the range
decision is recorded.

---

## R-64. Six of this unit's own rules recognize a builtin by the text of its name

**Found:** in the eighth round, 2026-08-09, by sweeping the unit's files for the
shape the verifier found in the enum classification, which is this wave's second
named pattern: identity that is not unique to the thing it identifies.

`tests/_source_guards.py` binds the modules that end a process by IDENTITY, and
its own comment says why: "a guard that matched the text `ExitCode` would be
satisfied by anybody's class of that name and defeated by one `as` keyword". Six
of its rules then match a BUILTIN by the text of its name:

| where | the text it matches |
| --- | --- |
| `resolve_int` | `_dotted(node.func) == "int"` |
| `ReservedCodeTable.status` | `_dotted(held.func) == "int"` |
| `ReservedCodeTable.status` | `_dotted(held.func) == "getattr"` |
| `ReservedCodeTable.pairs` | `_dotted(function) in {"dict", "OrderedDict"}` |
| `ReservedCodeTable._zipped` | `_dotted(argument.func) == "zip"` |
| `ProcessExits._fetched` | `node.func.id == "getattr"` |

A module writing `from builtins import int as whole` and then
`{"config-unusable": whole(30)}` is not reported. So is a module rebinding
`getattr` or `zip`.

**The cost is measured and it is zero today.** No module in the package rebinds
or aliases `int`, `getattr`, `zip`, `dict` or `OrderedDict`, measured over the 51
files `package_sources()` returns. The shape is real and the instance is not, so
it is recorded here rather than fixed on a guess about which spelling matters.

**It is not the same risk as the enum one, and the difference is worth writing
down.** The enum base was aliased for a legitimate reason, readability, and
`from enum import StrEnum as Vocabulary` is something a person writes without
meaning to evade anything. Aliasing `int` is not. That is why one was closed and
this one is carried.

**Closes when:** either a package module aliases one of these five names, at
which point the guard is silent about a real file and the rule has to bind by
identity, or the six become one helper that resolves a builtin through the same
import walk `ProcessExits` already runs.

---

## R-65. One entry in the not-a-cause whitelist covers an enum the walk never reaches

**Found:** in the eighth round, 2026-08-09, by the mutation table. It is the same
shape this branch has already paid for once: a guard whitelist that can be
widened for free.

`NOT_A_CAUSE` classifies eleven package enums as carrying CONTEXT rather than a
refusal cause, and the completeness walk consults it at exactly one place, where
a declared enum appears in an exception constructor's annotations. Removing the
`cratekit.core.routing.Decline` entry kills **zero** tests, because no exception
in the package annotates a `Decline`.

Measured on the same mapping, so the number means something:

| the revert | deaths |
| --- | --- |
| the `cratekit.core.routing.Decline` entry removed | **0** |
| the `cratekit.core.cause.Scope` entry removed | 6 |
| the whole mapping emptied | 10 |

The mapping is load bearing and that one entry is an exemption for nothing.

**Why it matters rather than being tidy-up.** An entry nothing reaches is how a
whitelist grows a line that later switches a guard off for free. `TABLE_OWNERS`
did exactly that on this branch: adding `core/session.py` to it left the whole
suite green, and only exact membership caught the widening. `NOT_A_CAUSE` has no
equivalent check. `test_every_enum_declared_not_a_cause_exists` proves each entry
names a real enum and says nothing about whether the walk ever asks about it, so
an entry can be correct, reviewed, and inert.

**Why it is not closed here.** The two ways to close it are both decisions rather
than repairs. Deleting the entry discards a classification somebody made
deliberately, and the cost of being wrong is a loud failure the next time an
exception annotates a `Decline`, which is the designed behaviour. Asserting that
every entry is load bearing, by removing each one and requiring the derived set
to change, makes this suite fail whenever an unrelated unit stops annotating an
enum, which is a test that fails for a reason nobody reading it would guess.

**Closes when:** either the entry is deleted with the reasoning above recorded
beside the deletion, or a positive control is added that asserts each entry is
REACHED by the walk rather than merely real, and the failure message explains
what a person is supposed to do about it.

## R-66. Two briefs disagree about whether a missing track is a review item

**Found:** by the U16 adversarial review, 2026-08-02. **Needs its own issue.**

**What the brief requires.** Issue #16 says twice that missing items become
review items with acquisition options, and plan line 271 AE11 agrees.

**What shipped.** U16 reversed that, following U11's register entry instead,
which declares matched and missing as OUTPUTS and only the middle state as the
version match queue. U11 has a countdown registered against this unit for its
reading; the issue text does not. The reversal was recorded nowhere except a
source docstring.

**The original justification was disproved.** That docstring argued that
queueing a missing row would ask a person once per run, forever, to confirm that
a track they put on a list should be acquired, which it called the unconditional
re-prompting the queue exists to end. That is false. `review.offer` is
idempotent: the same identity finds the same item, the verdict is preserved, and
no second row is written. The reviewer proved it against the real store. The
false sentence has been deleted from `src/cratekit/acquire/match_cli.py` rather
than left standing, and what replaces it says what is actually true, which is
that two briefs disagree and the disagreement is a product decision.

**What is fixed here, and it is only the mechanical half.** The docstring
claimed a missing row "carries its acquisition options as DATA in the match
result". It did not: `match.resolve_one` returned a missing row with an empty
candidate list, an empty path list, and no options of any kind, and the test
named `test_a_missing_track_carries_its_options_as_data_rather_than_as_a_question`
asserted a reason slug, a null review item and an empty queue while asserting
nothing at all about options. A missing row now carries an `acquisition` array of
`match.Acquisition` options, most precise first: an ISRC lookup when the list
supplied a code, then a text search. Both name the exact version the list asked
for, because an option meaning "some other cut will do" is the silent
substitution the whole unit exists to remove. A rejected verdict produces a
missing row and carries the same options for the same reason. The test now
asserts them.

**Still open, and reserved for Phillip.** Whether a missing track belongs in the
review queue with those options attached, or stays an output row carrying them as
data, is a product decision and was not taken here. Missing rows were deliberately
NOT moved into the queue and `adjudicate` was deliberately NOT rewritten.

**A related gap with no owner at all.** U11 declared `missing_full.csv` and
`not_acquired.csv` as legacy surfaces. Neither has a producer in any unit that
has landed or is in flight, and no countdown covers them, because
`NEW_SURFACE_OWED_BY` in `tests/test_review_queue.py` is derived from surfaces
that are adjudicated AND carry no legacy file, so a surface carrying one is
excluded by construction. Two declared outputs are therefore owed by nobody and
nothing says so.

**Closes when:** an issue records the decision between the two readings, and
whichever wins is implemented with the legacy surfaces either given a producer or
withdrawn.

---

## R-67. Four accepted findings from the U16 review, recorded rather than fixed

**Found:** by the U16 adversarial review, 2026-08-02.

Numbered after R-66. If a concurrent unit claims R-67 first, renumber this entry
at merge; the content is what matters, not the number.

**1. `match run` exiting PENDING_HUMAN changes the chaining contract.** A run
that produced version questions exits 12, so `crate match run && crate acquire`
stops. That is correct as a state, and it is the silence R11 exists to remove:
a run whose caller reads `missing` and acquires it must not also be told nothing
about four tracks that were a remix away from being right. But it is a change to
how the two verbs compose, nothing declares it, and the acquisition verb has not
landed to have an opinion. **Closes when:** the acquisition unit states whether it
consumes a pending match run's payload or refuses until the questions are
answered.

**2. The three arrays no longer sum to the input list.** A suppressed version is
reported on `warnings` and appears in none of `matched`, `needs_review` or
`missing`, which is deliberate and is argued in the module docstring: counting it
missing is what the brief forbids by name and dropping it is what R36 forbids by
name. The cost is that a consumer reconciling counts against the list it supplied
loses tracks with nothing to notice. **Closes when:** the envelope carries a
count a consumer can reconcile against, or the payload surface is reopened to
carry a fourth array and U5's three-array reservation is revisited deliberately.

**3. The library walk parses every file two or three times per run.**
`match._read_from_disk` calls `tags.read_tag` for the artist, the title and
sometimes the key, and each call opens and parses the container again. Over a
real library that is two or three full mutagen parses per file on every `match
run`, with no cache and no reuse between runs. Nothing here is wrong, it is
simply paid for repeatedly. **Closes when:** the tag layer exposes a
read-all-fields call, or the index is cached against file size and mtime. The
natural owner is whichever unit first walks the library in anger.

**4. R13's URL fetch is deferred with no countdown.** `match run` refuses a web
address with its own sentence and says the intake verbs own provider sessions and
pagination. No intake verb has landed that fetches a playlist, no residual
recorded the deferral, and no handoff entry names it, which Part 4 step 3 of the
seam decisions requires be stated when a requirement is deferred across a unit
boundary. It is stated here. **Closes when:** an intake unit lands the fetch, or
the requirement is re-pointed at a unit on the board.

---

## R-68. Four accepted findings from the second U16 review, recorded rather than fixed

**Found:** by the second U16 adversarial review, 2026-08-03.

Numbered after R-67, which the same unit added. If a concurrent unit claims R-68
first, renumber this entry at merge; the content is what matters.

**1. A candidate at a non-Camelot key is displayed as having no key.**
`match.key_token` parses Camelot and returns the empty string for anything else,
so `"Am"`, `"F#m"` and `"A min"` all fold to nothing. Those files then group with
genuinely unkeyed files, and `Candidate.key` renders null. The invariant the
candidate docstring states, that a candidate shows one key and every path under
it is at that key, is therefore false for exactly the spellings rekordbox writes
by default when a track has not been through this product's naming convention.
It is not a wrong join: an unparseable key and an absent key are already treated
alike by `key_disagreement`, so the STATE is right and only the display and the
grouping are coarse. **Closes when:** the key vocabulary understands the open-key
and musical spellings, at which point `key_token` returns a canonical Camelot for
all of them and the grouping sharpens with no other change. The natural owner is
whichever unit first has to render a key to a person outside this verb.

**2. The dash reader is an English vocabulary, so convergence is English-only.**
`match.split_title` reads a dash-introduced version only when the tail's last
word, or its first, is in a list of English qualifiers. A catalogue spelling its
versions in Japanese or Cyrillic converges through the bracketed reader and not
through this one, so the pair `曲 (リミックス)` and `曲 - リミックス` still produce
two identities. The module docstring says this rather than presenting the dash
pass as fixing convergence outright. Deliberately not fixed here: guessing at a
version qualifier in a script this list cannot check is the wrong-join risk the
vocabulary exists to bound, and the right fix is a per-script vocabulary rather
than a looser rule. **Closes when:** the vocabulary carries the qualifier words
for the scripts the library actually holds, with the same
last-word-plus-multi-word guard.

**CORRECTION, third round.** This entry originally ended "where the English pair
now produces one identity". That was FALSE for a whole class of English pairs and
the sentence hid a live regression. The rule this entry describes refused to read
a BARE ONE-WORD tail, so `Sun Path - Live`, `- Instrumental`, `- Acoustic`,
`- Dub`, `- Demo`, `- Extended` and `- Remix`, every one of them a tail the public
playlist API really ships, stopped converging with the provider row for the
identical record. With `Sun Path (Instrumental)` on the disk the dash form scored
76.4 against a floor of 82 and reported MISSING with an acquisition option, which
is verbatim the defect the round before it had closed. Fixed in the third round:
`split_ambiguous` returns the reading `split_title` declines and the LIBRARY
settles it, taking the split reading only when it holds the head at exactly that
version. What is left English-only is what this entry says, the vocabulary
itself.

**3. `split_version` and `split_title` differ by one word and mean different
things.** Both are exported. The first reads bracketed groups only; the second is
what the readers call and reads both conventions. The docstring that claimed a
dash qualifier is "deliberately not parsed" has been rewritten, since the module
now parses one, and it points at the other function. The names remain a trap.
**Closes when:** the bracketed half stops being public, or is renamed to say that
it is a part rather than the whole. Not done here because it is exported and a
rename is a change other units read.

**4. The export text guard would fire on sixteen correct modules if it were run
over the package.** `tests/test_match_states.py` checks non-docstring string
literals for `.xml`, `rekordbox` and export markup. Applied to this unit's two
modules it is clean and useful, and it covers the one route an import guard
cannot see. Applied package-wide it would fire on an argparse help string
mentioning an export, on the cause slug `rekordbox-running`, on the remedy token
`quit-rekordbox`, on a doctor check name, on
`importlib.import_module("pyrekordbox")`, and, most pointedly, on a guard clause
written to REFUSE an export. It is not red today because it is scoped to two
modules, and it is recorded because the obvious next move, widening it, is the
move that breaks it. **Closes when:** whoever widens it narrows the pattern to a
path-shaped literal in a read call rather than any string mentioning an export,
and keeps a fixture for the refusal clause so the guard cannot block the code
written to enforce the same rule.

---

## R-69. A provider row cannot address a library row that kept a featured credit

**Found:** by the third U16 review, 2026-08-03. Numbered after R-68, which the
same unit added. If a concurrent unit claims R-69 first, renumber this entry at
merge; the content is what matters.

**The gap.** `Wanted.suppression_spellings` now consults the tombstone store
under every spelling a library row carries for one version: the three bracket and
dash conventions, the multi-group form, and the null qualifiers `_NULL_VERSIONS`
already calls equal to no qualifier at all. One spelling stays out of reach from
one source. A row whose Title column reads `Sun Path (feat. Mira) (Nightwave
Remix)` is addressed by any list that spelled the credit, and by no list that
arrived through a provider carrying its version in a separate field, because the
credit is dropped from the matching title as a PERFORMER and a source that never
spelled it has nothing to put back.

**Why it is not closed by widening.** The obvious widening is to compose from the
matching title rather than from the spelling's own head, which is what an earlier
round did, and that consults `sun path` for a listing of `Sun Path (feat.
Mira)`. `tombstone_fold`'s own docstring settles the direction: a missed
suppression re-acquires something and reports it, an over-eager one silently
withholds music somebody wants, and those two costs are not comparable. So the
miss is taken deliberately and named here rather than traded for a silent
withhold.

**THAT PARAGRAPH DESCRIBED A DECISION THE CODE HAD NOT IMPLEMENTED, and the
fourth review is what found it.** The widening was rejected in the design and was
LIVE in the code for three listing shapes, because `_head_of` located the version
as a bracketed SUFFIX and a credit is not always last. `Sun Path (Live) (feat.
Mira)`, `Sun Path [Live] (feat. Mira)` and `Sun Path (feat. Mira) (Extended)
(Remastered)` each fell back to the matching title, which has had its credits
taken off, so the addresses composed were the PLAIN record's. The last of those
composed four of them, one being `Sun Path (Extended) (Remastered)`, a literal row
in this repository's own `REKORDBOX_ROWS`. Deleting that plain row then resolved a
list line naming the credited recording to SUPPRESSED: in none of the three
arrays, at exit zero, with acquisition skipping a track nobody had deleted.

**Fixed in the direction this entry always claimed.** `Wanted.addresses` composes
nothing unless the head still carries every credit the listing spelled, so the
promise is a checked precondition rather than a sentence in a docstring. Where the
head cannot be located the listing is addressed by exactly what it said and by
nothing else.

**AND IT WAS FIXED ON TWO READERS OUT OF THREE, which the fifth review found by
driving the third.** `_from_row` set `spelled` to the empty string for any row
that declared its version in its own field, and `Wanted.listed` then composed the
address from the MATCHING title, which has had its credits taken off. So the
credit was gone before the new precondition could look at it, `_credits_in(head)`
and `_credits_in(spelled)` were both empty, the comparison passed on nothing, and
the provider row `{"title": "Sun Path (feat. Mira)", "version": "Extended
Remastered"}` addressed `Sun Path (Extended Remastered)`, `Sun Path [Extended
Remastered]`, `Sun Path (Extended) (Remastered)` and `Sun Path - Extended
Remastered`, the third of which is a literal row in this repository's own
`REKORDBOX_ROWS`. Deleting that plain row resolved the credited listing to
SUPPRESSED at exit zero. The identical listing through `read_text_lines` or
`read_spotify_items` correctly reported MISSING, and every test pinning this drove
the text reader only.

**Closed by carrying the row's own title, which is the first half of this entry's
own closing condition.** A reader handed a split title and version now composes
`spelled` from the row's TITLE, credits and all, at the point it still has it. The
provider row above is addressed by the four spellings of the CREDITED recording
and by none of the plain one.

**WHAT THIS ENTRY USED TO RECORD AS THE COST WAS THE CHEAP HALF.** The paragraph
here named a missed suppression, a listing whose credit sits after its version no
longer reaching the same version spelled the other way round: `Sun Path (Live)
(feat. Mira)` does not reach a tombstone recorded from `Sun Path (feat. Mira)
(Live)`. That is real and it is still the residual, but it was not the live cost.
The live cost was the over-eager WITHHOLD above, the direction `tombstone_fold`
rejects by name, and an entry that records only the direction it chose is an entry
that cannot be used to check whether the code went the other way.

**Pinned, not assumed.** `UNRECONCILED` in `tests/test_match_states.py` is the
literal list of unreconciled derivations, checked over all seven row spellings and
all three readers on every run. It going empty or growing fails a test rather than
changing behaviour quietly. `CREDIT_OUTSIDE_THE_SUFFIX` in the same file pins the
WHOLE address set for each of the three shapes above, ACROSS ALL THREE READERS, as
literals on every side, because "the plain address is gone" is also true of a
composition that produces some other wrong string, and because a fix verified on
one reader out of three is exactly how this reappeared.

**What is left open.** A provider row that never spelled the credit at all,
`{"title": "Sun Path", "version": "Nightwave Remix"}` against a library row
`Sun Path (feat. Mira) (Nightwave Remix)`, still cannot reach it: there is nothing
to put back. That is the one entry in `UNRECONCILED`.

**Closes when:** the provider readers are handed a row that carries the credit,
which is now enough on this side, or the deletion pass records a second identity
with credits stripped and this side consults it, which is a decision belonging to
whoever owns the tombstone identity rather than to this unit.

---

## R-70. The two tombstone derivations are reconciled only at merge

**Found:** by the third U16 review, 2026-08-03.

**What the drift guard checks now.**
`test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist` is gated on `cratekit.core.tombstone` existing and
arms the day U24 merges. It checks the store key, the kind, the fold over every
pinned input, the identity function over every row spelling, AND the DERIVATION:
for each spelling a library row really carries, the identity that module's own
`version_identity` returns is compared against the identities the three readers on
this side actually produce.

**What it still cannot prove.** U24's RECORDER is not imported by it. The string
the recorder hands `version_identity` is taken from `u24_records` in the same test
file, which is a hand-written imitation of `deletion.stores.version_of` written
from that unit's stated shape, and nothing in this tree checks it against U24's
real code. So the guard compares one real function against one real function, and
one real derivation against an imitated one. The two units are known to fail from
opposite sides of this seam: an independent review of U24 found that its identity
COLLIDES for two different remixes of one recording whenever the mix name sits in
rekordbox's `RemixerName` or `Subtitle` column rather than inside `Title`, because
its reader maps only `ArtistName` and `Title`; this side may compose a title that
side would never have recorded. Neither is visible to a same-string function
comparison, and only the second is visible to the derivation check as written.

**What it already checks against the real rule.** The gated guard calls U24's own
`version_title` for every row shape and asserts the imitation in this file agrees
with it, then composes each identity with the real function and drives it through
the three readers. So the COMPOSITION rule is checked against the real code the
moment both are in one tree, and only the READER that fills the version column is
imitated.

**A GATED GUARD IS NOT A GUARD, and the seventh review measured the cost of
treating it as one.** The imitation of `version_title` in this file went three
rounds stale against U24's real one, using a substring test after the real one had
moved to a bracketed one, and nothing could see it because the only comparison was
behind the merge gate. So the imitation is now pinned TODAY against
`U24_COMPOSITIONS`, eleven literals taken by running U24's module at `81d575c`,
every row a shape the two rules decide differently, and the gated guard asserts
the same literals against the real function once it can import it. An imitation of
another branch's code is a claim about that branch: it is loaded or it is guarded,
and a guard that only runs after the merge is neither.

**The exact check that would close the rest.** Drive U24's own library reader over
a collection row table whose rows put the version in `Title`, in `RemixerName` and
in `Subtitle` in turn, hand each resulting row to U24's own `version_of`, and
assert that every identity it writes appears in `Wanted.suppression_spellings` for
a list naming the same record through all three readers. That is the only form of
this check with no imitation in it on either side. Until it exists, `u24_records`
says in its own docstring what it is and what it cannot prove.

**Closes when:** that test exists, and `TOMBSTONE_KIND` and `version_identity` in
`match.py` have collapsed into imports from `cratekit.core.tombstone`, which is
what this unit's docstrings already say must happen.

---

## R-71. The index reads a file's title one way, so the disk side of the one-word dash stays narrow

**Found:** by the third U16 review, 2026-08-03.

**The asymmetry.** A LIST title whose dash tail is a bare one-word qualifier
carries both readings, and `resolve_one` offers the split one as a QUESTION when
the library holds the head at exactly that version. A LIBRARY FILE named the same
way carries one reading. `match._read_from_disk` calls `split_title` once, so a
file named `08A - 124 - Aurora Bloom - Sun Path - Instrumental.flac` is indexed
under the recording `sun path instrumental` with no version, and a provider row
carrying title `Sun Path` and version `Instrumental` cannot reach it: the row
scores 76.4 against a floor of 82 and reports missing.

**Why it was not fixed with the list side.** The list side needed one extra
reading on one object. The index side needs a file to be reachable under two
recording tokens, which changes what `LibraryIndex.__len__` counts, lets one file
appear twice in one candidate offer under two different recordings, and gives
`_candidates_for` two groups for one path. None of that is hard, and all of it is
a change to the shape three other things read.

**Bounded rather than open.** The exposure is files whose NAME carries a dash
version and whose tags do not carry the title, because a tagged file takes its
title from the tag and a title tag spelling `Sun Path (Instrumental)` indexes
correctly. This product writes the bracketed convention, so the exposure is
material acquired before it, or by hand.

**Closes when:** `Owned` carries the readings of its own title and the index
registers a file under each, with `__len__` counting distinct paths and
`_candidates_for` grouping so that one file is one candidate however many
recordings reach it.

---

## R-72. The recorder keeps the Title column's own shape, so the consulter enumerates shapes

**Found:** by the third U16 review, 2026-08-03, after U24 changed its identity
derivation mid-round.

**What changed on the other side.** U24's recorder no longer hashes the Title
column verbatim. `deletion.stores.version_of` now passes
`tombstone.version_title(row.title, row.version)`, with `row.version` read from
rekordbox's `RemixerName` and then `Subtitle`, and `version_title` composes with
ROUND PARENTHESES. That narrows this seam rather than widening it: a row whose mix
name sits only in the version column is recorded under `sun path (nightwave
remix)`, which is exactly what this side composes for a provider row naming the
same record, and `test_the_recorder_and_the_consulter_compose_the_same_string`
pins it.

**The mechanism that leaves a class open, RESTATED IN THE SEVENTH REVIEW BECAUSE
THE ENTRY DESCRIBED A U24 THAT NO LONGER EXISTS.** This paragraph used to say that
`version_title` short circuits "when the folded version is already contained in
the folded title", and drew from that the conclusion that a Title of `Sun Path -
Nightwave Remix` keeps the dash. Both are false and were checked by loading U24's
real module rather than by reading it. `_already_carries` replaced the substring
test with a BRACKETED one, and U24's own docstring records why: a substring test
reads `Live` as already carried by `Lively Up`, so two rows of one recording
collapse onto one identity and deleting either suppresses both. The delimited
question asks whether a bracketed group of the title NAMES the version, on word
boundaries, skipping any group that opens with a credit marker.

So the short circuit fires for `Sun Path (Nightwave Remix)` and `Sun Path
[Nightwave Remix]`, and does NOT fire for the dash form: a Title of `Sun Path -
Nightwave Remix` beside a version column repeating `Nightwave Remix` is recorded
under `sun path - nightwave remix (nightwave remix)`. The shape a library row
happens to use still survives into the identity where a bracket carries it, so a
consulter still has to ENUMERATE shapes; what changed is that the enumeration also
has to include the recorder's own composition on top of a non-bracketed shape.

**What that cost while this entry was wrong.** This file's imitation of
`version_title` used the substring rule, so the armed derivation guard computed
ONE unreconciled entry and passed. Against U24's real module the same computation
yielded FOUR, silently hiding `('Sun Path - Nightwave Remix', 'text')`, the same
row through `spotify`, and the same row through `tidal`. That is a tombstone U24
records which none of this side's three readers could address: the version
reports missing, acquisition re-fetches it, the deletion is undone, and every
suite stays green. It would have armed RED at merge on that row.

**Closed rather than named.** `_spellings_of` now composes the recorder's own
parenthesised form on top of the dash spelling, gated on the same conservative
read-back the dash form itself is gated on, so all three readers reach it and
`missed` is back to R-69's featured credit alone. The imitation implements the
bracketed rule, and `U24_COMPOSITIONS` pins eleven shapes the bracketed test
decides differently from a substring test against literals taken by RUNNING U24's
module, so a re-drift of either copy fails today rather than at merge.

**What this side enumerates, and where the edge is now.** `Wanted.addresses`
composes round parentheses, square brackets, the multi-group split, the dash form
when this module's CONSERVATIVE reader reads it back, and the recorder's
composition on top of that dash form. What is NOT covered is a bracket shape U24
does not read either, `Sun Path {Nightwave Remix}` being the pinned example, and
any difference INSIDE the version string itself, such as a Title spelling
`Nightwave RMX` against a provider version of `Nightwave Remix`.

The curly edge MOVED with this correction and is sharper for it. U24 does not read
a curly brace as a bracket, so it composes, recording `sun path {nightwave remix}
(nightwave remix)`. A list that spells the curly form as plain text carries no
version this side can parse, so it composes the null-qualifier equivalents and
misses. A source that carries its version in its OWN FIELD hands this side a title
and a version and reaches the recorder exactly, curly braces included. The edge is
therefore a limit of what this side can PARSE out of a spelled title, not a limit
of what it composes.

**The dash gate is the conservative reader and not the ambiguous one.** An earlier
round let `split_ambiguous` satisfy the read-back, which reads a string back only
by declaring that this module CANNOT tell whose record it names. Composing `Sun
Path - Live` on the strength of that addresses a row that may be a composition
genuinely called "Sun Path - Live", so a deletion of that composition would
silently withhold the live cut of "Sun Path". It is the over-eager direction with
extra steps, it was reachable by nothing, and it is gone.
`test_the_dash_spelling_of_a_bare_one_word_version_is_not_composed` keeps it gone.

**THE MIRROR OF THAT GATE WAS WIDE OPEN UNTIL THE FIFTH REVIEW, and it was the
reachable half.** `_spellings_of` refused the composition and `Wanted.addresses`
walked BOTH readings unconditionally, so the list line `Aurora Bloom - Sun Path -
Live` composed `Sun Path (Live)` and `Sun Path [Live]` anyway and a tombstone over
the live cut suppressed it. Same ambiguity, same cost, opposite direction,
defended in one docstring while being rejected by name two functions away. The
policy is now one policy: an undecidable reading never crosses into an address,
either way. `test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one`
drives it at resolution and
`test_neither_reading_of_an_ambiguous_title_composes_the_other_ones_address`
asserts the symmetry on the object.

**What that costs, MEASURED, because the sentence here was an argument and not a
measurement.** It said the version "reports MISSING and acquisition fetches it
back", and that the direction is acceptable "because the run says what it is
about to get". Driven, with the file actually gone from the disk and a tombstone
recorded from the row `Sun Path (Live)`:

| the list spells | exit | arrays | warnings |
| --- | --- | --- | --- |
| `Aurora Bloom - Sun Path (Live)` | 0 | all three empty | `acquisition-suppressed`, naming the suppression |
| `Aurora Bloom - Sun Path - Live` | 0 | `missing / not-in-library` | NONE |

The dash row carries an acquisition query of `Aurora Bloom Sun Path - Live`. So
the run says what it is about to GET and says nothing at all about the DELETION,
and the row is indistinguishable from any other missing track in a 200 row list.
The justification is therefore narrower than it read: the cost is not "a reported
re-acquisition", it is a silent one, and what makes it acceptable is only that
the alternative is an over-eager withhold that is also silent and is worse.
`test_the_dash_spelling_re_acquires_a_deleted_version_and_says_nothing_about_it`
drives both rows and asserts the empty warning array, so the day this stops being
silent is the day that test fails.

**How often, priced here rather than left to another entry.** The class is a list
spelling a version after a dash where the deletion recorded a bracketed one. The
ambiguous-reading residual measures the same spelling class and calls `- Edit`,
`- Mix` and `- Live` "three of the commonest spellings a public playlist ships",
so this is not a rare shape: it is as common as that entry says, and only the
overlap with a standing tombstone narrows it. One entry pricing the class as
ubiquitous while the entry carrying its cost did not price it at all was the gap.

**Not fixed by widening.** Adding shapes is cheap and adding the wrong one is not:
every extra composed spelling is another string a deletion of somebody else's
record could match, and `tombstone_fold`'s docstring settles that direction, an
over-eager suppression silently withholds music somebody wants. The dash form
already carries a read-back gate for exactly this reason. A shape is added when a
library is found to use it, not on the chance that one might.

**Pinned rather than assumed.**
`test_a_title_shape_outside_the_enumerated_ones_is_a_recorded_gap` asserts the
edge is where this entry says it is: the curly form is unreachable from a spelled
listing and IS reachable from a source that keeps its version in a field, so the
limit is what this side can parse rather than what it composes.
`test_the_only_doubled_address_is_the_one_the_recorder_actually_writes` allows the
one doubled address the recorder really writes and forbids a double on any
bracketed spelling, which is the distinction `_already_carries` makes.

**Closes when:** the deletion pass records a normalized identity beside the
verbatim one and this side consults that, which puts one shape on both sides of
the seam and retires the enumeration. That is a decision for whoever owns the
tombstone identity, which is the domain layer and not this unit.

---

## R-73. The one-word dash class cannot converge on state across the three readers

**Found:** by the fourth U16 review, 2026-08-03, as two blocking findings that
turn out to be one decision. Numbered after R-72, which the same unit added. If a
concurrent unit claims R-73 first, renumber this entry at merge; the content is
what matters.

**The two findings.** First, the library decided how an ambiguous title parsed and
`resolve_one` rewrote the wanted track, so every identifier downstream was a
function of the disk: one list line produced two different `match_id` values on
two machines, which is exactly what `crate review export` and `crate review
import` exist to move a decision between, and on one machine renaming the
confirming file flipped the reading, looked a resolved item up under an identity
nobody had ever been asked, offered a fresh question, and left the answer
somebody gave unreachable in the store with nothing reported. `CANDIDATE_GONE` is
the state built for "the library changed under a recorded verdict" and it was
bypassed, because reaching it needs the item to be FOUND first. Second, the
rewritten reading was reported as MATCHED, so a parse this module declares
undecidable resolved to confident: `Long - Live` against a library holding `Long
(Live)` reported ownership, exit zero, and `Long - Live` is in this unit's own
list of legitimate titles whose last word is a version word.

**Why they are one decision.** Both come from letting the library's answer stand
in for a parse. The identity is now derived from the reading the STRING yields
and from nothing else, so it is the same on every machine, and the library's
answer is used for the one thing it is evidence for: which file to OFFER with the
question. `Why.READING_AMBIGUOUS` is that question.

**THAT FIX LANDED ON `match_id` AND LEFT THE REVIEW ITEM, which the fifth review
found by driving the two verbs the property is about.** This entry and the module
docstring both asserted that `Wanted.question` was now the same on every machine.
It was not. `TrackMatch.question_identity` passed `about_the_key=self.asks_about_key`,
and `asks_about_key` was set by whichever branch the LIBRARY took, so one list line
carrying a key opened a KEY question on a machine holding that exact version at
another key and a VERSION question on a machine holding only another version, with
one `match_id` across both. The first machine answered and exported; the second
imported the row with no conflict, then asked the identical question again under
its own identifier, so the answer was imported and ignored with nothing reported.
On one machine, deleting the copy that made it a key question stranded the verdict
under an identity nothing looks up, which bypasses `CANDIDATE_GONE` for exactly
the reason this entry already gives: reaching that state needs the item to be
FOUND first. The key in the item identity is now the LIST's key on every question,
the `about_the_key` argument and the `asks_about_key` field are gone, and
`test_a_verdict_travels_between_two_machines_that_hold_different_versions` drives
the export and the import across the two library states.

**What that costs, recorded rather than found later.** A list line that names a
key and a list line that does not are now two questions and two items, where a
VERSION question used to be one. That is a real loss of convergence between a
provider list carrying keys and the same list pasted as text without them. It is
the cheap side: the alternative is an identity a machine's disk gets a vote in.
The promise R13 actually makes, that the same LINE through the three readers is
one question, is unaffected, and it is asserted beside the cost in
`test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`.

**The trilemma, stated because it is not going away.** For this class, three
things cannot all hold. (1) One identifier per record across the three readers.
(2) An identifier that does not move with the library. (3) An identifier that
names one record. A source carrying its version in its own field has said where
the boundary is; a source that spelled `Sun Path - Live` has not, and no rule over
that string can. Converging the two anyway means either an identity that moves
with the disk, which is finding one, or one identifier standing for both a
composition called "Sun Path - Live" and a live cut of "Sun Path", which is an
identity that is not unique to the thing it identifies. So (2) and (3) are kept
and (1) is given up for this class alone.

**What that costs, and what it does not.** The public playlist row and the pasted
row spell the same characters, so they still agree on the state, the reason, the
identifier and the item; only the provider row differs, and it differs by matching
exactly and asking nothing. So the practical promise, that nobody answers the same
question twice, is unaffected: there is no second question to answer. What is
given up is the literal reading of property 4, that all three produce the same
match result, for the bare one-word dash tail and for nothing else.

**The regression this must not be.** The second round refused this class outright
and a held file was reported MISSING with an acquisition option at exit zero. That
is still gone and is asserted as such:
`test_a_one_word_version_tail_is_asked_about_and_never_re_acquired` asserts no
reader reports the row missing and no reader carries anything to go and fetch.

**Pinned in four places.**
`test_the_identifier_of_an_ambiguous_row_never_moves_with_the_library` drives one
list line against a library holding nothing, holding the file, and holding it at
another key, and asserts one identifier and one item identity across all of them.
`test_a_verdict_survives_the_rename_that_flips_the_reading` answers the question,
renames the confirming file, and asserts `CANDIDATE_GONE` under the ORIGINAL item
identifier rather than a fresh question beside a stranded answer.
`test_an_undecidable_parse_is_never_promoted_to_a_match` drives `Long - Live`
against a library holding `Long (Live)`.
`test_an_ambiguous_reading_is_taken_only_when_the_library_confirms_it` keeps the
reprise class where it was.

**Closes when:** the review store carries the listing's own spelling beside the
identity, so an importing machine can re-derive whatever it needs against its own
library, or a person decides the ambiguous class should carry a mark in the
payload saying this module re-read their line. The first is the smaller change and
belongs with whoever owns `review export`; the second is a surface decision and
belongs on an issue.

---

## R-74. The ambiguous reading class is queued as a question and does not gate the run

**Found:** by the fifth U16 review, 2026-08-03, as a cost the fourth round left
uncosted. Numbered after R-73, which the same unit added. If a concurrent unit
claims R-74 first, renumber this entry at merge; the content is what matters.

**What was measured.** Across the 17 words in `_DASH_VERSIONS` times four library
states, 68 cells, 14 change and all in one direction and one library state:
`MATCHED/EXACT` became `NEEDS_REVIEW/READING_AMBIGUOUS` when the library holds the
confirming file. The words are `acoustic, bootleg, demo, dub, edit, extended,
instrumental, live, mix, remix, reprise, rework, version, vip`. The empty library,
the library holding another version and the library holding the whole title are
all unchanged, and no row reports MISSING or carries an acquisition option, so the
second round's regression stayed closed.

**The consequence nobody had priced.** Any list carrying such a line moved the run
from exit 0 to exit 12 `PENDING_HUMAN`, and `- Edit`, `- Mix` and `- Live` are
three of the commonest spellings a public playlist ships. For a large library run
against public playlists that is a review queue filling faster than a person
empties it, and a gate that fires on almost every run is a gate nobody reads.

**The decision, and why this one.** The class is still a question, because the
defect the fourth round fixed was real: an undecidable parse reported as MATCHED
is ownership of a record nobody checked. What changed is that it does not by
itself make the run `PENDING_HUMAN`. `match_cli.UNGATED` names the one why this
applies to, `_pending` filters it, and `READING_UNSETTLED` reports each such row
on the warning channel with its item identifier and `review.list` as the remedy.

The alternative offered was to narrow the question to cases where the two readings
lead to genuinely different acquisitions. It is not taken, and the reason
originally written here was false and was written as if it had been measured. It
said the two answers "ALWAYS differ in acquisition", because the question is asked
exactly when the library holds the confirming file, so accepting means the library
has the record and rejecting means going and getting it.

**The counterexample, driven.** List line `Aurora Bloom - Sun Path - Live`, the
library holding `Sun Path (Live)`, and a tombstone standing over the reading the
LIST spelled. ACCEPT gives `matched` with one path. REJECT reaches
`apply_verdict`'s tombstone consult and gives `suppressed / tombstoned` with ZERO
acquisitions. The control, the same pair with no tombstone, gives `missing /
verdict-rejected` with one acquisition. So for this class the two answers are hold
versus SKIP rather than hold versus fetch, and a narrowing written on "genuinely
different acquisitions" would drop the class outright rather than leave it
untouched. `test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire`
drives all three.

**What can be measured instead, and it is what the decision actually rests on.**
The narrowing needs a condition evaluated BEFORE the question is asked, and the
only thing available at that point is which spelling the list used and what the
library holds. Neither says what a person will answer, and both of the two answers
are reachable for every row in the class. So the narrowing has no input: it would
have to guess the answer to decide whether to ask the question. That is a
statement about the information available, which is checkable, rather than a
claim about acquisitions that turned out to be false for a whole subclass.

**What is not given up.** The row stays in `needs_review`, so nothing counts it
owned and nothing acquires it. The item is still offered, so the question is
answerable and the answer persists across runs. The run still says so out loud:
R11 forbids a question nobody is TOLD about, not a question that did not stop the
pipeline. And the escape hatch still gates: a row of this class carrying a verdict
this build cannot apply is rewritten by `apply_verdict` into one of `STALLED`,
which is not in `UNGATED`, so it blocks and names `review clear`. That last part
is asserted by
`test_an_ungated_question_still_gates_once_its_verdict_cannot_be_applied`, because
a class that never gates would have hidden the one state that genuinely needs a
person.

**The residual this leaves.** A person who never reads warnings and never opens
the queue never converges these rows. They are visible in three places and acted
on in none, and the run exits 0 while a fraction of the list is unresolved. That
is a real gap and it is the one being accepted, against a gate that fires so often
it stops carrying information.

**Closes when:** the queue can answer a CLASS of question once rather than one row
at a time, so "a bare `- Live` tail in my lists means a live version" is a single
decision that settles every row it applies to, or a person decides this class
should be resolved by a policy setting rather than by a question. Both are surface
decisions and belong on an issue rather than in this unit.

---

## R-75. A question answered on one machine does not settle a different question about the same line

**Found:** by the sixth U16 review, 2026-08-04, as the price of closing that
review's first finding. Numbered after R-74, which the same unit added. If a
concurrent unit claims R-75 first, renumber this entry at merge; the content is
what matters, not the number, and nothing cites it by number.

**What the identity is now.** A review item is addressed by the list line AND by
which question is being asked: `question_identity` carries the recording, the
version token, the list's key and an `asks` field, and `question_shape` derives
that field from the `Why`, reading `KEY_QUESTIONS` for the two whys that are one
question. Nothing about the library reaches any VALUE in it.

**Why the fourth field had to come back.** The round before this one made the
identity purely list derived, which fixed a real defect and collapsed the KEY
question and the VERSION question onto one item. Driven end to end: a list line
asking for `Sun Path` at 03A against a library holding only the extended mix is a
version question; somebody accepts it; the library later gains the plain cut at
`03B`, the RELATIVE MINOR of the key the list asked for; and the next run
reported `matched / verdict-accepted` at exit zero with the 03B file in `paths`
and the extended mix the person had actually pointed at gone from them.
`Why.KEY_RELATIVE` exists, in this module's own words, because 8A and 8B "look
like agreement to anything comparing wheel positions", and it had become
reachable only while nobody had ever accepted anything about that line.

**The cost, which is this entry.** Two machines whose libraries make one list
line ask two DIFFERENT questions now open two items. A machine holding that exact
version at another key asks a key question; a machine holding only another
version asks a version question; an answer exported from the first and imported
into the second lands in the store and does not settle the second machine's
question, which asks again. That is correct, because the second machine was never
asked the first machine's question, and it is still a loss: a person who has
answered "my extended cut is that record" on one machine answers a related
question again on the other.

**The same shape on one machine.** Deleting the copy that made a line a key
question turns it into a version question under a different item, so the key
answer sits resolved and unreachable. That is the stranding `CANDIDATE_GONE`
exists to report, and it is not reported here, because reaching that state needs
the item to be FOUND first and the run is now looking up a different item.

**The sentence that used to end that paragraph was measured false, and correcting
it is the seventh review's first finding.** It claimed the reverse was no longer
possible, an answer being APPLIED to a question nobody asked. The identity does
not deliver that on its own and was never going to: `KEY_DIFFERS` and
`KEY_RELATIVE` both map to `asks="key"` DELIBERATELY, four identities and not
five, so the two key whys are one item by design. Driven through `crate match
run` and `crate review resolve` in both directions: a list line asking for `Sun
Path` at 03A against a library holding it at 08A is a key-differs question; accept
it WITHOUT naming the copy; replace the 08A file with an 03B one, the relative
minor `Why.KEY_RELATIVE` exists to catch; and the run reported
`matched / verdict-accepted` at exit zero with the 03B file in `paths`, nothing
in `needs_review` and nothing in `warnings`. The reverse direction did the same.

Splitting `asks` on the two key whys is NOT the fix, and that is the useful half
of the finding. WHICH of them fires is a function of what that machine's disk
holds, so splitting them would put the library back inside the identity, which is
the defect the round before this one removed. The defect was that the identity is
unique to neither the question nor the candidate: an unspecific acceptance is a
claim about THE CANDIDATE THAT WAS ON OFFER, and it was being read back as a claim
about the question in the abstract. `apply_verdict` now takes the options the item
was stored with and binds an unspecific yes to the single candidate it was given
about; a yes read back against a different candidate is `CANDIDATE_GONE`, with the
warning and the `review clear` remedy that state already carries. Naming the copy
with `--option` was always safe, because `candidate_id` digests the owned key, and
this gives the answer that names nothing the same protection.
`test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another`
drives both directions through the real verbs, including the positive leg where
the unchanged library still applies the answer.

**Why the trade goes this way.** The two costs are not comparable, which is the
same argument `tombstone_fold` makes one layer down. An unasked question asked
again is visible: it is in `needs_review`, in the queue, in the pending action
and in the warning channel. An answer applied to the wrong question is silent: it
is a matched row at exit zero naming a file at a key nobody checked.

**Pinned rather than assumed.**
`test_a_version_answer_never_settles_a_key_question_about_the_same_line` drives
the whole 03B sequence through the real dispatcher and the real store.
`test_a_verdict_travels_between_two_machines_that_hold_different_versions` keeps
the export and import property for two machines asking the SAME question over
different files at different keys.
`test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
drives this entry's cost, so it is a fact somebody measured rather than a
paragraph.

**Closes when:** the review store can record that two items are the same
DECISION, so a person answering one is offered the other rather than asked it
cold, or the queue learns to answer a class of question once. Both are surface
decisions and belong on an issue rather than in this unit.

---

## R-76. One vocabulary lives in two files until the domain module merges

**Found:** by the sixth U16 review, 2026-08-04. Numbered after R-75, which the
same unit added. If a concurrent unit claims R-76 first, renumber this entry at
merge; nothing cites it by number.

**What was wrong.** "Is this word a version designation" was answered by two
lists. `match._DASH_VERSIONS` held 17 words and `cratekit.core.tombstone.VERSION_WORDS`
on U24 held 27. Driven, with the library holding `Aurora Bloom - Sun Path
(<word>)` and the list spelling `Aurora Bloom - Sun Path - <word>`:

| the word | what shipped |
| --- | --- |
| `Unplugged` | `missing / not-in-library`, with an acquisition option |
| `Radio`, `Acapella`, `Original`, `Club` | `needs_review / title-approximate` |
| `Live` | `needs_review / reading-ambiguous` |

The first row is verbatim the defect `_is_a_version`'s own docstring calls "the
other half of the same mistake", still live for eleven words: the run goes and
fetches a file the library already holds, at exit zero, with nothing asked and
nothing warned. The four in the middle are not that failure but are the wrong
question: an approximate hit offers candidates from a DIFFERENT recording, so the
person is asked whether some other record is theirs.

**Fixed by taking the domain layer's list.** `match.VERSION_WORDS` is U24's
frozenset replicated element for element, and `_DASH_VERSIONS` is DERIVED from it
plus this module's own head words, so a word added to either arrives in both.
`rerecorded` is the one deliberate difference and it is a head word: this side
has a leading-word convention because the public playlist API ships "Remastered
2011" and the domain module has no use for one.

**What is still residual.** Two copies exist. U24 is on its own branch, so this
is a replica with a countdown, exactly like `TOMBSTONE_KIND` and
`version_identity` beside it. `tests/_pending.py` carries the obligation,
`test_the_version_vocabulary_is_u24s_element_for_element` pins the membership
against an independently written literal, and the gated drift guard compares it
against the real module the day it merges.

**And the widening is safe in one direction only, which is worth stating because
it is not U24's direction.** Over there a word believed wrongly composes a
parenthetical no provider spells, so a deletion fails to stick. Here a word
believed wrongly makes a one-word tail AMBIGUOUS rather than split, and an
ambiguous reading is taken only when the library holds exactly that head at
exactly that version, so a wrong word costs a question the library already had an
answer for and never a wrong join.

**Closes when:** U24 merges and this becomes `from cratekit.core.tombstone import
VERSION_WORDS`, which is the same line the two tombstone symbols beside it are
waiting for.

---

## A note on citing these entries

**Cite by TITLE, never by number.** Six numbers in this file, in the R-66 to R-72
range, were claimed by two branches at once with DIFFERENT CONTENT on each side,
because two units appended here in parallel. Every citation by number in source
or tests therefore points at a different subject the moment either side
renumbers, and that break is invisible: the sentence still reads perfectly and
cites the wrong finding. U16's source and tests cite by title only, and
`test_no_residual_is_cited_by_number_anywhere_in_this_unit` and
`test_every_residual_this_unit_cites_is_a_heading_that_exists` keep it that way.

## R-77. The suppression warning's code slug is not pinned, so a consumer keying on it would not notice a rename

**Found by** U16's first independent verification pass, round 8, 2026-08-13.
Measured with `scripts/mutate.py`, row `V23c_suppression_code_reworded`.

**Measured cost.** Rewording `match_cli.SUPPRESSED_WARNING` from
`acquisition-suppressed` to a different slug kills **0 tests**, promoted to the
full suite at 3512 collected and still 0. The reason is the shape METHOD names
as a thing a green suite cannot see: all ten assertions on the slug compare
against `match_cli.SUPPRESSED_WARNING` itself, so each one reduces to X equals
X while genuinely exercising the code around it.

**Why this is a residual and not a blocking finding.** The cost falls on a
consumer that reads the warning envelope and branches on its machine readable
code. **No such consumer exists in this repository**, so the input is not
reachable today and the producer could not be driven. Stated precisely because
the distinction is the one condition 3 of the merge bar exists for: zero
in-repository candidate producers were driven, because there are none to drive,
which is not the claim that nothing will ever produce it.

**What holds instead.** The composite pair was run and is R-78's second count:
removing the suppressed rows from the warning channel entirely kills 20 tests,
so R36's presence guarantee is pinned even though the slug naming it is free.

**The closing condition.** The first module that branches on this code pins it,
by asserting the literal slug once rather than the constant, in the same commit
that introduces the branch.

## R-78. The suppression warning's sentence is not pinned, and only its presence is

**Found by** U16's first independent verification pass, round 8, 2026-08-13.
Measured with `scripts/mutate.py`, rows `V23_suppressed_message_reworded` and
its composite `V22_suppressed_warning_omitted`.

**Measured cost.** Rewording the suppression warning's sentence, reworded rather
than appended to because the suite asserts with `in`, kills **0 tests**,
promoted to the full suite at 3512 collected and still 0. So the exact words a
person reads when a version is suppressed can drift with the suite green.

**What the composite shows it does hold.** Removing the suppressed rows from the
warning channel altogether kills **20 tests**. Both counts are measured. The
pair is the evidence the severity floor asks for on a user facing zero row: the
guarantee that a suppressed candidate is REPORTED rather than silently omitted,
which is R36 itself, is pinned at 20, while the sentence carrying it is pinned
at 0.

**Why this is a residual.** The user facing cost is a wording change nobody is
told about, not a wrong answer or a lost track. The state the warning describes
is still reported, still counted, and still correct.

**The closing condition.** One test that asserts the sentence as a literal
rather than through the constant, chosen for the phrase a person would search
for rather than for the whole string.

## R-79. The quiet machine refusal gates an ordinary unit test, and nothing stops the next one walking into it

**Found by** the countdown text session, 2026-08-14, by running the battery on
`main`'s tree while an independent verifier ran its own suites on the same
machine. Not found by any verifier, and specifically not by the harness's own
independent review on 2026-08-13, which read the refusal as a checking path
improvement and did not ask which callers sit behind it.

**Measured cost, and it is a cost to the merge discipline rather than to a
user.** `tests/test_hardware_fixtures.py::test_calibration_round_trips_and_threshold_is_a_multiple`
called `calibrate(repeats=2)` and passed the live payload through
`write_calibration`, whose quiet machine refusal raises when
`relative_spread` exceeds 0.25. With two samples the spread is
`(max - min) / median` over exactly two numbers, so one scheduling hiccup
crosses it.

Measured on this tree, with a verification subagent running concurrently:

| context | repeats | pass | fail |
|---|---|---|---|
| the full suite, before the fix | 3 | 1 | 2 |
| that test alone, before the fix | 10 | 10 | 0 |
| `tests/test_hardware_fixtures.py` alone, after the fix | 15 | 15 | 0 |
| the full suite, after the fix | 3 | 3 | 0 |

Observed spreads on the two failures were 0.266 and 0.277, both just over the
limit. The isolation column is why this was not caught earlier: the natural
check after touching the harness is to run its own file, and its own file
passes.

METHOD's merge discipline is that nothing merges until all three parts of the
battery are clean. A battery that goes red two runs in three for a reason
unrelated to the change under review teaches a reader to discount a red
battery, which is the one signal the discipline is built on. It also lands on
whoever is merging rather than on whoever wrote the harness.

**What was fixed.** Both tests that routed a live measured payload through the
refusal now pin `relative_spread`, exactly as the neighbouring
`test_an_unquiet_calibration_refuses_to_write` already pinned it to 0.5 to drive
the refusal deterministically. The round trip test gained an assertion that the
pinned value survives the round trip, which nothing checked before. The second
site, `test_a_calibration_from_another_machine_is_refused`, had never fired and
was found by looking for the shape one function over rather than by watching it
fail, which is METHOD's fifth pattern.

Every remaining live measured call into the refusal is
`scripts/calibrate_timing.py`, which is the deliberate human act the refusal
exists to gate. That is the correct and only caller for it.

**Why this stays open as a residual.** The two instances are closed and the
class is not. Nothing in the repository prevents the next test that needs a
calibration payload from writing `calibrate(...)` followed by
`write_calibration(...)` and reacquiring the flake, and the failure it produces
names the machine rather than the test, so the next person to meet it will also
start by suspecting their own change. The refusal is a gate on a deliberate act
sitting in a path that ordinary tests share.

**The closing condition.** A guard that fails when a test module calls
`write_calibration` on a payload whose `relative_spread` it did not set, so the
rule is enforced where it is broken rather than remembered. The existing
`tests/test_pending_units.py` AST sweep over the suite is the nearest worked
model for the shape.

## R-80. A write capable probe entered the refusal vocabulary that read only reports import, and the U27 merge cannot resolve it

**Found by** the U27 merge attempt, 2026-08-14. Not found by U27's independent
verification, which passed a full battery on the branch, and not visible on
`main`, which also passes. It exists only on the merged tree, which is this
repository's recurring shape: a rule verified on one surface while a second
surface carries the same coupling.

**The mechanism, driven rather than argued.**

U27 lands `_probe` in `src/cratekit/core/cause.py`. It calls
`os.open(path, os.O_RDWR | os.O_NONBLOCK)` and closes the handle, with no
`O_CREAT` and no `O_TRUNC`, to ask the operating system whether a write would be
permitted rather than guess from a driver level error. It therefore cannot
change a file, and it does open a write capable handle.

`tests/modules/test_reports.py` admits `cratekit.core.cause` on its reports
allowlist, whose stated argument is that nothing it admits can touch a file
except through `pathlib`. Both report modules import `Scope` and `refuse` from
it: `src/cratekit/modules/reports/export.py:71` and
`src/cratekit/modules/reports/aging.py:62`.

`_os_open_reads` already models `os.open` read against write through its flags,
and declines to read this call as a read.

**THE MECHANISM ABOVE WAS WRONG AND IS CORRECTED HERE, 2026-08-14, by driving
it.** This entry originally said the guard declines because one branch of
`os.O_RDWR if writing else os.O_RDONLY` is not a read. **The guard never sees
that expression.** `_os_open_reads` reads the CALL ARGUMENT, and the call is
`os.open(path, flags)`, whose second argument is the bare local name `flags`.
The helper cannot resolve a name back to its assignment, so it answers "flags
this cannot read as a read" and the assignment's shape is irrelevant. Five
rewrites of the assignment were driven and every one stayed red, including
`flags = os.O_RDONLY` with no conditional and no `getattr` in it:

| flag assignment, call left as `os.open(path, flags)` | guard |
|---|---|
| `os.O_RDONLY` | RED |
| `os.O_RDONLY \| os.O_NONBLOCK` | RED |
| `os.O_RDONLY \| getattr(os, "O_NONBLOCK", 0)` | RED |
| `os.O_RDWR \| os.O_NONBLOCK` | RED |
| `os.O_RDWR` | RED |

Inlining the expression into the call is what the helper can actually read, and
it then behaves exactly as designed:

| inlined call | guard |
|---|---|
| `os.open(path, os.O_RDONLY \| os.O_NONBLOCK)` | **GREEN** |
| `os.open(path, os.O_RDWR \| os.O_NONBLOCK)` | RED |

So the guard's objection is **"I cannot tell what this opens"**, not "this
writes". It accepts an inline read only open and rejects an inline write capable
one. Both halves are correct behaviour. The finding is real either way, because
the handle genuinely is write capable, but the reason matters: it opens a
resolution the three below do not name. Recorded because the looser reading
survived a full independent verification and a written learning before anybody
asked the guard what it saw.

**Both remedies the guard offers were driven to their end, and both fail.**

The guard names exactly two: name the writer, or drop the module.

*Name the writer.* The guard propagates a writer to its callers, so each round
surfaces the next layer. The transitive closure over `core/cause.py` was
computed with an AST walk in one pass rather than chased a layer at a time:
eleven names, and it CONTAINS `refuse`, reached through `CratekitError.cause`
calling `classified`. Naming `refuse` was then driven and fires the reports'
own guard: *the reports package can change a file*, at
`modules/reports/aging.py:248` and `modules/reports/export.py:195`.

*Drop the module.* Both report modules import from it, so dropping it fails
their imports.

*The third option nobody offered*, teaching `_os_open_reads` to accept
`O_RDWR`, is widening a guard that is behaving exactly as designed, and this
repository's rule is that a guard is never widened to admit a finding.

**Measured cost.** No user facing cost is claimed and none was found: `_probe`
opens and closes, so no report mutates anything today, and the reports remain
read only in fact. The cost is that a stated invariant is now false, and the one
guard written to catch exactly that has no answer available to it. Under the
merge bar this is a residual rather than a blocking finding, because there is no
named user facing cost. It nevertheless stops the merge, because METHOD's
battery rule is that nothing merges until all three parts are clean, and this
one cannot be made clean without a decision.

**What was preserved rather than discarded.** The merge attempt is committed on
the branch `merge/u27-attempt-2026-08-14`, pushed, and MUST NOT BE MERGED. It
carries the six resolved conflicts, the verified register discharge, the ten
incoming residuals renumbered to R-80 through R-89 in that branch's own file,
the `grant-path-access` reservation, and the re-pinned cause population. All of
that is correct work and none of it should be paid for twice.

**The closing condition, and it is a decision rather than a repair.** One of:
`_probe` moves out of the refusal vocabulary into a module the reports allowlist
does not admit, which is the honest structural answer; or `_probe` establishes
write permission without opening a write capable handle, which changes U27's
behaviour and needs its own driven round; or the reports stop importing from
`cratekit.core.cause`. U27 has fix rounds left under the cap, so sending it back
for one is within the process rather than an exception to it.

**THE FIRST CONDITION AS WRITTEN IS ACHIEVABLE AND FIXES NOTHING. Driven
2026-08-14.** Moving the raw open into `cratekit.core.access_probe`, a module the
allowlist does not admit, and leaving `cause.py` calling it, turns this guard
GREEN while the chain reports to `cause` to `access_probe` to `O_RDWR` is
untouched. The audit walks only the modules named on the allowlist, so a module
it does not admit is never read. A second guard then catches it,
`test_the_package_imports_downward_only`: `cause` is FOUNDATION by an explicit
name in the layer table and a new `cratekit.core.*` module falls through to
INFRASTRUCTURE, so foundation importing it is a KTD23 violation. **That guard is
then satisfied by adding one name to one regex**, after which the full suite is
green apart from the two pre-existing failures below and the reachability is
still exactly as it was. Both structural guards can be satisfied by a relocation
that changes nothing. Any resolution taking this route has to invert the
dependency so `cause.py` does not call the probe at all, not merely move it.

**A fourth resolution, opened by the corrected mechanism.** `_probe` serves two
intents through one variable and one call. Splitting them so the read only
intent calls `os.open` with an INLINE read only flag expression makes the guard
certify it as a read, on the measurement above, leaving only the single write
intent call site, `_from_database_error`, to answer for. It is the smallest of
the four and it is still a decision, because of the next paragraph.

**The write capable handle is pinned by NOTHING. Driven 2026-08-14.** Forcing
the probe to `os.O_RDONLY` always, so no write capable handle is ever opened,
killed **zero** tests: 3 failed, 5030 passed, 11 skipped, 5044 collected, which
is the baseline exactly. So the suite would not notice any of resolutions two,
three or four changing this behaviour, and none of them can be validated by
running it. Whichever is taken needs its own driven evidence.

**The preserved branch is red on THREE guards, not one, and this entry said
one.** Measured on `merge/u27-attempt-2026-08-14` at `01eb6da`, full suite,
2026-08-14: 3 failed, 5030 passed, 11 skipped, 5044 collected. This finding is
one of them. The other two are the branch's own unfinished re-pinning and are
unrelated to it:

- `test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned` pins
  `(256, 156)` kebab literals against a tree measuring `(268, 163)`. The branch
  re-pinned the CAUSE population and did not re-pin this one.
- `test_the_walk_sees_every_shape_a_refusal_is_actually_written_in[expected1]`
  sees `grant-path-access`, which is the reservation that same branch added to
  `src/cratekit/cli/exit_codes.py`, against a fixture expecting
  `{repair-backup-facts, upgrade-cratekit}`.

Both are re-measure and re-pin work, per the standing rule never to widen. They
are recorded here so the next session does not resolve this finding, see two
unexplained reds, and read them as a second collision.

### The fourth resolution was TAKEN, 2026-08-14, and this finding is now one function

`unit/u27-setup-wizard-and-doctor` at `46e04ae`, two commits, pushed. `_probe`
became `_probe_readable` and `_probe_writable`, each spelling its flags inline at
its own call site, which is the only shape the guard can read. The duplication is
forced by that and the reason sits in the source beside it, because folding them
back into one helper taking `flags` is the obvious tidy up and silently restores
the unreadable shape. `os.O_NONBLOCK` is spelled directly, the `getattr` fallback
having been measured unreadable by the same guard.

**Measured on a REAL merge**, not on the branch: a scratch clone, `git merge` of
the branch into `main`, six conflicts, and `src/cratekit/core/cause.py` among the
files that auto merged clean. Running the guard's own `_unnamed_writers` against
the merged file, with `tests/modules/test_reports.py` byte identical to `main`'s:

| tree | the guard reports |
|---|---|
| before | `['_probe']`, covering three call sites, two of which only ever read |
| after | `['_probe_writable']`, one function, one call site |

Two of the three probes are now certified as reads by the guard rather than
argued to be. What remains genuinely does open a write capable handle, so the
finding is honest and it is as small as it can be made without deciding the
question below.

### What the write capable handle buys, driven

Six scenarios, comparing the current probe against the alternative that never
opens write capable and infers from `os.statvfs` `ST_RDONLY`, the existing
`_immutable` helper, and `os.access`:

| scenario | write probe | read probe plus metadata |
|---|---|---|
| ordinary writable file | none | none |
| `chmod 444` | permission | permission |
| `chflags uchg`, Finder Locked | locked | locked |
| ACL denying write, mode still 644 | permission | permission |
| absent file | unclassified errno 2 | unclassified errno 2 |
| real read only mounted volume | read-only | read-only |

**Six were driven and all six agree.** Say it that way rather than "the handle
buys nothing", because the class where they are KNOWN to diverge was not driven:
a network mounted volume, where `os.access` and `statvfs` can answer from the
client while the server is what refuses. No network share was available.

**A reframing worth carrying, because it weakens the objection.** The write probe
is reached only from `_from_database_error` for a driver error that is not
`SQLITE_CANTOPEN`, which means `SQLITE_READONLY` or `SQLITE_PERM`. In those cases
the driver has ALREADY established that a write was refused. The probe is
disambiguating WHY, not predicting whether. Network staleness is a hazard for
predicting a write outcome and much less of one for explaining a refusal that has
already happened. That does not decide it, and it is the argument the next
session should attack first.

### The behaviour is now pinned, which it was not

`test_the_write_probe_classifies_every_way_a_write_is_refused` in
`tests/test_doctor.py`, on the branch. Three live rows, the mode, the immutable
flag and the ACL, each verified to be biting rather than silently skipped, plus a
negative row so they are not passing on a probe that refuses everything. Driven:
with the write handle mutated to read only the test fails and the rest of its
file passes. **The same mutation killed zero of 5044 before this test existed.**

It takes no side. Whichever resolution is taken has to keep it passing, and one
that cannot hold all three rows has changed what the user is told rather than how
it was measured.

### So what is still open

Only this: whether `_probe_writable` keeps its write capable handle. If it does,
the guard stays red on one function and U27 stays blocked on the battery rule. If
it is replaced, the guard goes fully green and the reports' invariant becomes true
again. The evidence above is what that decision now rests on, and it is a decision
about a shipped classification path rather than about a merge.

### DECIDED 2026-08-15. The handle is gone and this finding is CLOSED

`_probe_writable` no longer opens anything. It asks `_probe_readable` first and
then attributes the refusal from metadata: `ST_RDONLY` on the volume, the
per-file immutable flag, and `os.access` with `effective_ids`. Landed on
`unit/u27-setup-wizard-and-doctor` at `4a34a84`, merged 2026-08-15.

**The reframing was attacked first, as this entry asked, and it holds.** The one
caller is `_from_database_error` for a driver error that is not
`SQLITE_CANTOPEN`, so `SQLITE_READONLY` or `SQLITE_PERM`, and both mean the
driver already attempted a write and was refused. The probe attributes an
outcome that has happened rather than predicting one, and all three attributions
this program can act on are readable from metadata.

**Driven, both implementations over the same real arrangements, 12 rows.** An
ordinary file, mode 444, mode 000, `chflags uchg`, an ACL denying write with the
mode still 644, an absent file, a path with an embedded null, a writable
directory, a directory at mode 555, and a real `hdiutil` read only volume in two
shapes plus its mountpoint. **Ten agree. The two that disagree are both
DIRECTORIES**, and a directory cannot arrive here: driven, `sqlite3` answers
`SQLITE_CANTOPEN` both for a directory as the database path and for a new
database inside a sealed directory, and `SQLITE_CANTOPEN` routes to
`_probe_readable`. So the divergence is over an input the one producer cannot
produce, which is this file's own reachability rule applied to a replacement
rather than to a finding.

**Driven end to end as well**, through `access_refusal` on a live read only
volume, a live mode refusal and a live Finder lock, and each gives the same
`AccessRefusal` as the handle did.

**The replacement's own mutation table found two zero rows and both are now
pinned.** Eight rows on the branch. The `ST_RDONLY` branch and the read probe
delegation each killed nothing, both user facing, so neither took a one line
record: `test_the_write_probe_names_the_medium_rather_than_the_account` and
`test_the_write_probe_answers_for_a_path_it_cannot_reach_at_all` were added and
re-measured at 2 and 1 deaths. A third test was added because nothing drove the
ROUTE rather than the answer. The eighth row, `effective_ids`, stays at zero and
is R-127. Tables: `docs/mutation/u27-r80-write-probe-replacement.md` and
`docs/mutation/u27-r80-write-probe-zero-rows-repinned.md`.

**Verified on the merged tree, which is the only place the collision exists:**
`test_the_allowlist_admits_no_writer_this_guard_cannot_name` passes, and
`test_the_write_probe_classifies_every_way_a_write_is_refused` passes unchanged,
which is what it was written for.

**What was given up, and it is unmeasured rather than lost.** A network mounted
volume, where a client can answer from cached metadata while the server is what
refuses. That class was never driven for EITHER implementation and no share was
available, and the direction is not established, because an open on a client
holding cached attributes does not reach the server either. Recorded separately
as R-126 so it is a standing question rather than a footnote inside a closed
finding.
<!-- ------------------------------------------------------------------ -->

## The twenty findings below arrived with the U23 merge, 2026-08-14, and were renumbered

They are U23's, and every one of them carried a different number on that branch.
`main`'s numbers did not move; the incoming side's did, which is the rule.

Branch R-20 through R-39 became R-81 through R-100, in order, a flat shift of
sixty one. All twenty collided, because the branch was cut when `main`'s highest
was R-19 and `main` has since filled R-20 onward with entirely different
findings.

Citations INSIDE these twenty were repointed with them. Citations of R-12
through R-19, and of R-78, were not touched, because those name `main`'s
findings and always did. The cut point is what makes the boundary clean: any
number at or below 19 in this block is a reference outward, any number from 20
to 39 is a reference inward, and nothing in the block sits on both sides of that
line. The same property is what let the U27 attempt be renumbered mechanically
at R-15, and it is worth preserving deliberately rather than by luck.

<!-- ------------------------------------------------------------------ -->

## R-81. Adoption's tag write takes no destructive session and no library lock

**Found:** during U23's review, 2026-08-02. `apply_plan` says so itself, in its
own docstring, and called it "the residue". It was recorded in no residual, no
handoff entry and no `_pending` obligation, which is what makes it a finding
rather than a documented decision: a gap only its own author can find is not
written down.

`cratekit.adopt.apply.apply_plan` writes a genre tag onto a user's file. That is
the one operation outside the database snapshot entirely: no snapshot holds it,
no re-import puts it back, and only the unit's own revert ledger can undo it.
The loop takes no write session and no library lock, so:

- nothing asserts rekordbox is closed, that a backup was acknowledged, or that
  the volume identity still matches, before a file is rewritten;
- two apply runs over one plan both see the same entries outstanding. What stops
  them reaching the DATABASE twice is R31's lock, taken one layer up. Nothing
  stops them reaching the FILE twice.

**Not as bad as it was.** The review's blocking finding here was that the tag
write happened BEFORE the membership write and a refusal from the membership
writer was caught per entry, so a systemic refusal inside the caller's own
destructive session rewrote every file in the plan while zero memberships landed.
Measured at 6 of 6. That is fixed: the recoverable write goes first, and a
refusal whose declared scope condemns more than one item ends the run. So a
caller whose gates refuse now rewrites nothing.

Two concurrent applies over one file are also safe, and measured so: 40 of 40
originals preserved, because the ledger's first-write-wins rule holds and both
the read and the write now sit inside one flock.

**Not fixed here** because the fix is not a line in this module. R29 declares the
destructive-session boundary as ONE SOURCE PER RUN, and this loop is not a run.
`cratekit.write.trees.write_tree_membership` owns its own session for exactly
that reason and refuses a caller-supplied gates factory. Opening a second session
here would give one run two sources, which is the composition R-12 already
records as a unit's decision rather than a merge's.

**Closes when:** `adopt.apply`'s command line lands and opens ONE session around
the whole loop, passing its own open guard down. That is registered in
`tests/_pending.py` against `cratekit.adopt.apply_cli`, so the obligation is
tracked by the file the board audit reads rather than by this paragraph.

---

## R-82. Conformance 3 cannot pass a verb with an explicit gate, and the reason is not the database

**Found:** during U23's review, 2026-08-02, while establishing which half of the
adoption CLI could land.

R-13 records "no destructive database verb can land on a machine without a
database" and says it closes when conformance 3 can run against a disposable
database fixture. **That close condition will not close it**, and this entry
exists because acting on R-13 as written would produce a fixture nobody needs and
leave the wall standing.

The wall is two properties of `test_conformance_3` itself, both established by
elimination:

1. It answers each gate INLINE, with `-d gate=option`, in the same invocation
   that reaches the gate. `Gates.require` correctly refuses an inline answer to a
   gate declared `explicit=True`, because R34 says a blanket affirmative never
   satisfies one. So the test cannot drive any explicit gate to `OK`, and that is
   R34 working rather than failing.
2. It drives once per declared gate, on a FRESH run, answering only that one
   gate. A verb declaring two gates therefore exits `DECISION_REQUIRED` on
   whichever one it was not answering.

`adopt.apply` has both shapes at once: an explicit approval gate plus the shared
cloud-sync gate. Removing `explicit=True` from both still gave exit 10, which is
what rules the database out as the cause: there is no database in either case and
the failure mode does not change.

**What this unblocked already.** `adopt.scan` shared one `module=` string with
`adopt.apply` and was held behind the same wall for no reason of its own. It
declares no gate, writes nothing, and is not destructive, so conformance 3 is an
empty loop for it. Split onto `cratekit.adopt.scan_cli`, it lands and passes
conformance 1, 2, 3, 5, 7 and 8.

**Closes when:** conformance 3 answers an explicit gate the way a person does,
through a recorded decision on the run in a separate act (`crate run decide`),
and drives once with EVERY gate answered rather than once per gate. Both are
changes to the test, not to any verb. The natural owner is U27, which lands
doctor and is the unit that makes a machine ready; a separate branch is
correcting conformance 3 now, so this may be spent before U27 reaches it.

**This entry needs its own issue.** `main` already defines R-14 and R-15, U27 is
renumbering its own to R-16, U16 is adding R-17 and U32 is adding R-19, so R-81
and R-82 are the next free numbers as of this merge.

---

## R-83. The adoption revert cannot recognize its own file after another Cratekit write

**Found:** during U23's third review round, 2026-08-03. It is the residue of a
defect that was fixed twice in the wrong direction first, so the history matters
more than usual.

`revert_tags` will not restore a file whose bytes are no longer the bytes
adoption left there, because restoring onto a replaced file writes one
recording's genre onto another recording's audio, with no record of what it
destroyed. That refusal is correct. What it cannot do is tell a REPLACEMENT apart
from this product's own later write of a different field: `energylevel` is in
`core.tags.FIELDS` for the analysis workflow, so writing one after an adoption is
ordinary, and it changes the file's bytes exactly as a replacement does.

**Two attempts to close it both made things worse, which is why it is a residual
rather than a third attempt.**

1. The first version compared size and modification time only. It refused three
   ordinary libraries: the analysis write above, a byte-identical file whose time
   moved, and an interrupted revert pass retried.
2. The second added "the field still holds the value adoption wrote" as a
   positive recognition and called it proof. It is not proof: the value written
   is a taxonomy bucket's DISPLAY name, shared by most of the library, so a
   stranger's recording whose own genre is that bucket satisfied it. Measured, a
   revert then overwrote the replacement's genre and dropped the record.
3. The inode was considered and rejected on measurement rather than on taste:
   `Path.write_bytes` and `cp` both truncate in place and keep it, so an inode
   match does not mean the content is unchanged.

4. The third version, in the same round that recorded this entry, wrote the
   digest down and then never asked it. It accepted "size and modification time
   unchanged" as its own definitive answer and returned before the digest was
   consulted, so the one piece of evidence a replacement cannot forge sat unread
   while the two it can forge decided. Measured in round 4: different audio
   written to the path, padded to the recorded size and stamped back to the
   recorded time with `os.utime`, restored anyway, `restored: 1  failed: {}`.
   Fixed in round 4, incompletely: round 4 asked the digest whenever one was
   recorded, and left three states in which it was not asked at all.

5. The fifth version, round 5, removed those three. An UNSTAMPED record returned
   "unchanged" before consulting anything, and an ordinary interrupt reaches it
   because the whole mutagen tag write sits between the record landing and the
   stamp. A record whose stamping read had FAILED stored an empty digest that was
   indistinguishable on disk from a document predating digests, and fell back to
   the same forgeable metadata. A CLOUD-EVICTED file skipped the digest to avoid
   a download that the acceptance it produced then performed one line later
   through `restore_tag`. All three are now refusals. There is exactly one
   acceptance left and it is the recorded digest matching the file's bytes.

**A second instance of the same wall, named because the module contemplates it in
writing.** `_key`'s own docstring says adoption may write more than one field to
one file, and the ledger keys on the file AND the field so that it can. It can
record them; it cannot revert the first of them. The second field's write moves
the bytes, so the first record's digest no longer matches and that record refuses
on every pass. Measured with `genre` then `title` through
`write_tag_with_record`: `restored: 1  failed: 1`, and **the failure is always
the field written FIRST**, whose digest the second write invalidates.

This entry previously said the failure was "always the alphabetically first field
because the ledger sorts by key". Both halves of that were wrong and it was
driven in both orders to be sure: writing `(genre, title)` fails `genre`, and
writing `(title, genre)` fails `title`. Alphabetical order was a coincidence of
the one test case that produced the observation, and the ledger's sort decides
the order records are VISITED, not which record's evidence has gone stale. The
mechanism is write order and nothing else.

**How close to shipped it is, precisely.** Not live, and one supported public
call away from being live. The only shipped call that reaches the ledger outside
`revert.py`'s own plumbing is `apply.py:541`, which passes
`field=ADOPTED_TAG_FIELD`, a module constant whose value is `"genre"`, so today
every record in a real ledger is a genre record and no file carries two. But
`cratekit.adopt.__init__` re-exports `write_tag_with_record`, so any caller
inside or outside this package can write a second field to an adopted file
without touching `apply.py` at all. It is latent rather than unreachable, and it
is the same wall as the analysis write above rather than a separate defect.

**Fixed far enough to be safe.** The byte-identical restore is recognized by a
digest recorded at write time, and the digest is the ONLY thing the guard accepts
on. Every other case refuses, names which of the four ways it is, names the
single record it refused, and `force` takes a list of `(path, field)` pairs so
overriding one never touches another.

**One claim in this entry was too strong and is corrected here.** The interrupted
pass is NARROWED rather than eliminated. See R-85.

**Closes when:** the record carries a digest of the DECODED AUDIO rather than of
the file, which a tag write does not change and a replacement does, or every
Cratekit writer that rewrites a file re-stamps any outstanding revert record for
it. The first needs a decoder in the write path and `core.tags` deliberately has
none. The second is a real obligation on whichever unit lands the analysis
writer, and it cannot be wired from here: `core.tags` is below `adopt` in the
layering and must not call up into it.

---

## R-84. Two accepted shapes in the adoption ledger, recorded rather than fixed

**Found:** during U23's third review round, 2026-08-03. Both predate the review
rounds and neither is reachable from any shipped caller today.

**An empty `written` bricks the whole document.**
`write_tag_with_record(written="")` persists a record whose `written` is the
empty string, and `read` then refuses the entire ledger, because it recognizes
`written` positively as a non-empty string. Every other record in that document
becomes unreadable with it, which is the one outcome this reader's positive
recognition exists to avoid. Nothing in `apply_plan` can produce it: `wanted` is
checked for None and a bucket display name is never empty. The two halves are a
writer that does not validate its own argument and a reader that refuses the
document rather than the record.

**Closes when:** `write_tag_with_record` refuses an empty `written` at the call,
which is where the caller can still be told, rather than at the next read.

**An entry whose container this build cannot write can never reach applied.**
`apply_plan` refuses the entry before placing it, which is correct and is the fix
for a worse shape where it landed a membership it could never complete. But the
entry stays outstanding forever, reported identically on every run, with nothing
a person can acknowledge. There is one undocumented escape: a run with
`tag_value=None` never asks the container question at all, so it places the entry
and marks it applied.

**Closes when:** the plan can carry an acknowledged exclusion, which is a review
queue verdict rather than a flag, so a person who knows a `.aac` will never be
tagged can settle it once instead of reading it in every report.

---

## R-85. An interrupted revert pass still strands one record, and round 3 called it eliminated

**Found:** during U23's fourth round, 2026-08-03, by driving the claim rather
than reading it.

Round 3 moved the ledger drop from the end of the pass to immediately after each
record's own restore, and wrote it up in `revert_tags`' docstring and in R-83 as
eliminating the interrupted pass STRUCTURALLY. It does not. It narrows the window
from the whole pass to one record.

A run that dies between a restore landing on disk and that record's drop reaching
the disk leaves one record describing bytes its own successful restore has
already replaced. On every retry that record is refused, because the evidence it
carries is a digest of what adoption left and the file now holds the original
that was put back. Measured: a two record pass, killed at the first ledger write
after the first restore, retries with `restored: 1  failed: 1` forever.

It is a narrowing worth having. Batching was worse by a whole pass, because it
stranded every record the run had already restored rather than one.

**Why it is a residual and not a defect.** The damage is BOUNDED, which is the
whole argument for accepting it. The refused record names itself for `force`, and
forcing it writes the same original onto a file that already holds it, so the
cost of the residue is one override and never a wrong value. That is asserted
rather than argued, in
`test_a_pass_that_dies_BEFORE_THE_LEDGER_WRITE_still_strands_that_one_record`,
which pins the real behaviour so the stronger claim cannot drift back in off a
green suite.

**THAT BOUND COVERS THE WINDOW AFTER THE RESTORE AND NOT THE ONE INSIDE IT, and
the two are different windows.** Round 4 stated the boundedness for a death
BETWEEN the restore landing and the record's drop. A death DURING mutagen's own
rewrite of the container is a separate window with a weaker guarantee, and the
distinction was not characterised until round 5.

What is NOT bounded there is the file. A container caught mid rewrite can be left
truncated or half written, and no undo log can put back bytes a partial write
destroyed. That is true of any interrupted file write and it is mutagen's window
rather than this pass's; this module's contribution is that it does not make it
worse.

What IS still guaranteed is the half this module owns, and it is driven in
`test_a_death_INSIDE_the_rewrite_is_a_different_window_and_a_weaker_bound`. The
record is dropped only after `restore` RETURNS, so a death inside the rewrite
leaves the record on disk with the recorded original still in it. The retry
refuses, because the bytes on disk are neither the recorded ones nor anything the
guard knows, and it refuses with `its bytes are not the ones adoption left
there`. `force` still reaches the original. So the ledger never loses the value;
only the container is at risk, and only for the duration of one `save`.

**Why it cannot be closed from here.** The surviving state after such a crash is
a file whose bytes are not the recorded ones and a record that cannot tell that
apart from a replacement without decoding the audio, which is R-83's wall. Doing
the drop BEFORE the restore is strictly worse: a crash in that window loses the
only copy of the original permanently.

**Closes when:** the pass writes an intent record naming the record it is about
to restore, so a retry can tell "I was in the middle of this one" from "somebody
replaced this file". That is a journal, it belongs with the destructive session
the apply command line opens (R-81), and it is the same unit's work.

---

## R-86. A revert hashes every file it considers, including cloud-evicted ones

**Found:** during U23's fifth review round, 2026-08-03, as the accepted cost of
removing the last shortcut in front of the digest.

`_changed_since_adoption` now accepts on one thing only: the recorded digest
matching the file's bytes. There is no branch that skips the read. Two costs
follow and both are real.

**A library re-tagged by another tool pays a full hash and then refuses
everything.** Driven on a four record ledger whose every file had been re-tagged
elsewhere: 4 whole-file sha256 reads, 0 writes, 4 refusals. Round 4's docstring
claimed "the read costs nothing this pass was not already spending" on the
grounds that an acceptance is followed by a mutagen rewrite that is more
expensive. That is true of the ACCEPTING path and false of the refusing one,
which is the path that dominates exactly when a library has drifted. The prose
is corrected; the read is kept, because without it the refusal is decided by
metadata anybody can forge.

**A cloud-evicted file is now read, which materializes it.** The branch that
skipped the digest for a file carrying `SF_DATALESS` is gone. It was removed
because on the ACCEPTING path it saved nothing: the acceptance calls
`restore_tag` one line later, mutagen opens the file and rewrites it, and the
provider fetches it regardless. Driven with the real writer rather than the stub
the old test used. What the removal genuinely costs is the REFUSING path: an
evicted file whose bytes have changed is now downloaded in order to be refused.

**Why the exposure is small, stated rather than assumed.** `scan.ADOPTABLE` is
`{READABLE}`, so adoption refuses to tag an online-only file at all, and a ledger
record can only name an evicted file that was readable when adoption wrote it and
was evicted afterwards. `SF_DATALESS` is also not settable from userspace and is
0 on Linux and on network mounts, so the population is macOS file-provider
libraries whose tracks were adopted locally and evicted later.

### CORRECTED IN ROUND 6. This entry described the cost as bandwidth and it was worse than that

Round 5 wrote the cost up as "an evicted file whose bytes have changed is now
downloaded in order to be refused", which is true and is the small half. Two
facts were missing and both were driven in round 6 rather than reasoned about.

**The fetch was UNBOUNDED.** `digest_of` had no deadline of any kind, so a file
whose bytes never arrive is a call that never returns.

**It happened under the lock that serializes every apply and every revert in the
library.** `revert_tags` wraps its whole pass in `config._exclusive_lock`, so one
stalled record blocked a concurrent `write_tag_with_record` on a DIFFERENT,
perfectly local, perfectly readable file for as long as the stall lasted.
Measured with a FIFO at the recorded path, which is the same shape a stalled
provider is from Python's point of view: `exists()` answered True, `stat()`
answered instantly, `open()` never returned, the revert child was still running
at 6 seconds, and the concurrent writer was still waiting when it was killed.

**Both are answered rather than documented.** The permissive choice is KEPT: an
evicted file is still read rather than refused, because on the accepting path the
restore materializes it one line later anyway. What changed is where and for how
long.

- `_look_before_the_lock` takes every guard read BEFORE the lock, dates each
  answer with a `stat`, and `_looked_at_still` spends the answer only while a
  `stat` taken under the lock still equals that one. The refusing path, which is
  exactly the case this entry is about, no longer holds the lock at all.
- `digest_of` gives up after `_READ_DEADLINE_SECONDS` and RAISES rather than
  answering the empty string, because `TimeoutError` is an `OSError` and folding
  it into "cannot be read" tells a person their file is damaged when it is
  merely still arriving.
- Anything that is not a regular file is refused from `st_mode` before a
  descriptor is opened, which is what `adopt.scan._probe` already did and this
  module did not. That covers the FIFO, the socket, the device and the
  directory, and it costs one `stat`.

**What is still residual, precisely.** The deadline is asked BETWEEN blocks, so
it bounds a stream that is arriving slowly and NOT a single `read` call that
never returns. A blocking read against a filesystem that has stopped answering is
uninterruptible from Python without a thread, and a thread would leave the read
running after its answer was abandoned. The shapes that genuinely never return
from `open` are all non-regular files and are refused before the open; a regular
file on a wedged mount is the case that remains.

**CORRECTED in U23's seventh round, 2026-08-04: it is now TWO reads per record,
not one.** The pass used to read each file once, before the lock, and spend that
answer under the lock whenever `(st_dev, st_ino, st_size, st_mtime_ns)` had not
moved. Measured on a real FAT image, an in-place rewrite of the same length inside
one modification-time tick moves none of those four, and the restore then ran on
bytes the pass had never read. So the pre-lock read no longer decides anything: it
exists to make a provider materialize the file with no lock held, and the read that
decides is taken again under the lock. Counted rather than estimated, in
`test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway`: two
reads of the same file per record, in that order. The second is served locally
after the first, so the cost is a second sha256 pass and cache pressure rather than
a second download, and that is the honest shape of it.

**Closes when:** the read runs where it can be abandoned, which means a
subprocess or a worker whose result the pass can stop waiting for, or a provider
API that answers "are these bytes local" without the answer being a shortcut past
the evidence. The second is still the better shape and is still a command line
concern: batch the evicted records, tell the person how much would be
downloaded, and let them decide once for the run instead of the guard deciding
per file.

---

## R-87. An interrupted adoption leaves a record only a human can spend

**Found:** during U23's fifth review round, 2026-08-03, as the accepted cost of
closing the widest hole in the guard.

`snapshot_before_write` persists the record, the mutagen tag write runs, and only
then does `_stamped` put the digest on. A run interrupted inside that window
leaves a record with no size, no time and no digest. Round 4 accepted such a
record unconditionally and returned before consulting anything, so a file replaced
months later with a different recording was restored over and reported clean. It
now refuses.

**What that costs.** The file in that window genuinely does carry adoption's
value, and the record genuinely is the only copy of the original. The person has
to name it: `revert_tags`' `force` takes `(path, field)` pairs and the refusal message
prints the exact pair for the record it refused. So the cost is one override per
interrupted record, on a run somebody asked for, versus a file nobody can put
back. That is the trade the module states in its own docstring and this is it
being paid rather than avoided.

**Why the window cannot simply be closed.** The stamp cannot go on BEFORE the
write, because what a later revert needs to recognize is adoption's own output.
It cannot be written in the same operation as the tag write either, because the
tag write is mutagen's and the record is this module's, and they are different
files on different filesystems.

**Closes when:** the record carries a PRE-write digest as well as a post-write
one. A record with a pre-write digest and no post-write digest can then be
compared against the file: matching the pre-write digest proves the tag write
never landed, so the revert is a no-op and can settle the record without asking
anybody. It costs one extra whole-file hash per adopted file at write time, which
is the same cost the post-write stamp already pays, and it belongs with whichever
unit is willing to double that.

---

## R-88. A filesystem that recycles inode numbers can hand one file another file's record

**Found:** during U23's sixth round, 2026-08-03, as the accepted cost of keying
the revert ledger on `(st_dev, st_ino)`. **CLOSED in U23's seventh round,
2026-08-04**, because the cost was measured rather than estimated and it was not
a residual, it was a data loss.

**What this entry got wrong, and both halves were wrong.** It said the exposure
was small because "APFS, which is the volume format this product targets, does
not reuse". APFS was then driven over four thousand create and delete cycles and
did not reuse, so that sentence is true and irrelevant: FAT and exFAT are the
format of every rekordbox export USB drive, and reuse was reproduced directly on
a real MS-DOS FAT image. A file at `st_ino` 9, deleted, and the next file created
came back as `st_ino` 9. The filesystem list omitted the one this product's users
plug in.

It also stopped one step short of the harm. It predicted a MISSING record for the
new file. What actually happened, driven end to end against the code, is worse:
`_record_locked` found the dead file's record by the live identity, found the
dead file's path no longer stat'd, and REFRESHED the record's path to the new
file. The stamp after the write then put the new file's digest into the dead
file's record, so at revert the guard compared the new file against its own bytes,
accepted, wrote the dead file's original onto it, dropped the record, and
reported `restored: 1  failed: {}`. The new file's own genre was in no file and
no record.

**What replaced it.** `identity_of` is no longer a key. A record carries three
claims about which file it is about, and `_record_for` requires them to converge:
the volume and inode, the path, and a digest of the bytes adoption left. A
divergence the BYTES can settle is settled, and every other divergence refuses
with `RecordCannotBeMatched`, which `apply_plan` fails per entry. In particular
the recorded path is never rewritten to a different file's path.

**What the closing choice costs**, because it is a real cost and not zero. A
recycled inode now REFUSES the second adoption instead of silently taking the
wrong record, so an entry fails and is reported per track. So does an
`os.replace` save on an already-adopted file, and so does the crash seam plus a
rename. All three leave the file untouched with its own value in it, which is the
trade this module makes everywhere: refusing costs an override on a run somebody
asked for, accepting costs a file nobody can put back.

**THE SENTENCE THIS WAS CLOSED ON WAS NOT TRUE WHEN IT WAS WRITTEN, corrected in
U23's eighth round, 2026-08-04.** "A divergence the BYTES can settle is settled"
was false in two of the six shapes. Where the identity and the path both named
the file, and where the recorded path was a second hardlinked name for it, the
match returned on the two agreeing ADDRESSES and the digest was never consulted at
all. Driven with no forgery: a recording replaced IN PLACE keeps both the inode
and the path, so the second adoption matched, re-stamped the record with the
replacement's bytes, and reported clean; the revert then wrote the replaced
recording's genre onto the new one and reported that clean too. That is the same
loss this entry closed, reached through the two shapes the closure did not check.
Both shapes now ask, and what they ask is in `_settled_or_refused`: not "did the
bytes move", which every tagging session does, but "is there a value in this field
that nothing has written down". The closure stands; the round it was granted in
did not earn it.

**The birth-time proposal is withdrawn.** This entry named `st_birthtime` as the
fix. FAT stores a creation time with two second granularity and exFAT with ten
millisecond granularity, and neither survives the file being copied, so a second
metadata stamp would have been a fourth thing that correlates with the file and
does not identify it. The bytes were available the whole time.

---

## R-89. A tag write is refused when its file cannot be identified, and one shape of that is ordinary

**Found:** during U23's sixth round, 2026-08-03, as the accepted cost of R-88's
identity.

`identity_of` stats the file, so a file that cannot be stat'd cannot be recorded,
and `write_tag_with_record` raises `AdoptedFileUnidentifiable` rather than
writing a tag with no record behind it. That is the right order: a tag write with
no record is the one operation in this product nothing can undo.

**What it costs.** `apply_plan` catches it per entry, so the run continues and
the entry is reported failed. The ordinary shape that reaches it is a track that
was READABLE in the census and was deleted before the apply reached it, which
previously produced a record for a file that was not there and then a failed
write. The new behaviour is better in substance and different in report text, and
a person who reads "cannot be identified on this machine" about a track they
deleted themselves has to work out that that is what it means.

**THE COST OF RE-ADOPTING AFTER AN ORDINARY TAGGING SESSION, measured in U23's
eighth round on 20 real files per shape, because that is the number this trade is
actually made on.** A tagging session moves the bytes of every file it touches,
and there are two ways to save.

| after a tagging session | in-place mutagen save | `os.replace` save |
| --- | --- | --- |
| second adoption, 20 files | applied=20 failed=0 | applied=0 failed=20 |
| revert after it | restored=20 failed=0 | restored=0 failed=20 |
| the session's own edits surviving | 20 of 20 | 20 of 20 |

**The in-place save is the common one and it costs nothing**, which is deliberate
rather than incidental: a byte change is not evidence of a replacement, so
`_settled_or_refused` accepts when the adopted field still holds a value the ledger
accounts for, and the whole library re-adopts and reverts exactly.

**The `os.replace` save still refuses every file, and that is this entry's
residual.** The inode moves for a file nobody replaced, so only the path and the
bytes are left, and the bytes were rewritten by the save. `_settled_or_refused`'s
question is deliberately NOT extended to this shape, and the reason is that the
evidence is weaker in a way that matters: in the shapes where it IS asked, the
inode proves this is the same file object and only its content moved. Here the
inode has moved, so a completely different track could be at that path, and the
most likely such track is another file from the SAME library already adopted into
the SAME bucket. Accepting on "the path plus the field value" would take a
coincidence that is rare in one shape and make it ordinary in the other.

**Refusing preserves the session; only `force` destroys it.** Nothing is written
by a refused entry, so all 20 title edits survive both columns above. What costs
the session is taking the escape: `revert_tags(force=[...])` writes each recorded
original back over the file the tagging session produced. That is the trade being
made, and it is one override per record on a run somebody asked for.

**Closes when:** the apply re-probes readability for an entry immediately before
writing and reports a deleted track as deleted, which is `scan.probe_readability`
being called from `apply` and is a small piece of work that belongs with the
adopt verb's command line rather than with the ledger. The `os.replace` half
closes with whatever gives a record something about its CONTENT that a save
preserves and a replacement cannot reproduce, which is the same thing R-94 names.

---

## R-90. A single `read` that never returns is not bounded, and neither is the `stat` in front of it

**Found:** during U23's seventh round, 2026-08-04. **Read from the source rather
than measured, and that distinction is the entry.** A stalling NFS, SMB or FUSE
mount could not be produced on this machine, the shape was NOT simulated, and no
number below is a measurement.

`digest_of` gives up after `_READ_DEADLINE_SECONDS`, and the deadline is asked
BETWEEN blocks: `handle.read` returns, the hash is updated, and only then is
`time.monotonic()` compared. A single `read` that never returns therefore never
reaches the comparison. `_look_at`'s first statement is `target.stat()`, with
nothing in front of it, and a `stat` against a mount that has stopped answering
does not return either.

**What is bounded and what is not.** A stream arriving slowly is bounded, which
is the cloud-provider case the deadline was added for and which IS measured, in
`test_the_deadline_ends_a_read_that_keeps_arriving_forever`. A filesystem that
has stopped answering entirely is not bounded anywhere in this module.

**Where it lands.** `_bring_the_bytes_within_reach` reads before the lock, so a
hang there costs the pass and not the library. The guard's own read is under the
exclusive lock, so a hang there holds the lock that serializes every apply and
every revert. That is the same lock the FIFO guard was added to protect, and the
FIFO guard does not help: a FIFO is refused from `st_mode`, and a stalled mount
hangs the `stat` that reads `st_mode`.

**Closes when:** the read runs on a thread with a join deadline and the pass
abandons the answer rather than the thread, or a `statfs`-based liveness probe
refuses a mount that is not answering before any path on it is opened. Both are
bigger than this unit and neither should be written from an argument: the first
step is to produce a stalled mount and measure what actually happens.

---

## R-91. A record with no digest cannot survive a rename

**Found:** during U23's seventh round, 2026-08-04, as the stated limit of the
identity that replaced R-88's.

`_record_for` matches a record to a file when the claims converge. After a rename
the recorded path is wrong; after a rename on a legacy path-digest ledger the key
is wrong too, and then the only surviving claim is the digest of what adoption
left. `_found_by_its_bytes` uses exactly that, and it is what carries a legacy
record through a rename, pinned by
`test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`.

**What is left.** A record with NO digest whose file has been both renamed and
re-inoded has no claim left to answer. Nothing finds it, a new record is written
beside it, and that record's `original` is the value adoption itself wrote. That
is the same data loss R-88 closed, arriving through a door only a digest-less
record can open.

**Why the population is small rather than zero.** A record has no digest in three
cases: a document written before digests existed, a run interrupted between the
tag write and the stamp, and a stamping read that failed. The first is the one
that matters and it exists only in ledgers written by builds inside this unit's
own history, none of which shipped. The other two refuse at revert anyway, so
their originals are already only spendable by hand.

**Why the obvious defence was not taken, measured rather than argued.** The
proposal was to refuse to CREATE a record whenever a stranded digest-less record
for the same field exists and the file in hand already holds the value adoption
is about to write. On a library that was already correctly tagged, every file
holds that value legitimately, so one stranded record would refuse the whole
library. A signal that fires on the ordinary case is not a signal.

**Closes when:** the ledger is migrated forward once, at read time, so no
digest-less record survives into a build that has digests. That is a document
migration and it belongs with whichever unit owns the doctor.

---

## R-92. The refusal's remedy names a verb that has not landed

**Found:** during U23's eighth round, 2026-08-04. **Measured, not read:**

    $ crate doctor
    crate: error: argument <command>: invalid choice: 'doctor'
            (choose from 'profile', 'run', 'job', 'review', 'adopt')

Every refusal `cratekit.adopt.revert` raises carries
`Remedy.RUN_DOCTOR`, and `cli/render.py` renders that remedy to the person as the
literal string `crate doctor`. `cli/registry.py` marks the `doctor` entry
`planned_in="U27"`, so the verb does not exist in any build this branch produces.
Until round 8 the message PROSE said it too, five times, in the form "Run the
doctor over the ledger".

**Half of it is fixed here.** No message in this module tells the person to run
anything any more. Each refusal now states what did not happen and names the
`(path, field)` whose original is still recorded, which is a fact they can act on
today, and `test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`
fails if the instruction comes back.

**Half of it is deliberately NOT fixed here, and this is the dependency.** The
machine readable remedy is still `Remedy.RUN_DOCTOR`. That slug is used at more
than forty call sites across `adopt/apply.py`, `write/routing_pass.py`,
`core/tree_registry.py` and this module, and its rendering is one line in
`cli/render.py` shared by all of them. Re-slugging this module's twelve would
leave the other thirty naming the same absent verb while looking correct, which is
a fix landing on the wrong object. There is one rendering and it is U27's to make
true.

**There is also no `adopt apply` and no `adopt revert` on the command line.** The
registry marks both behind `ADOPT_APPLY_CLI_UNIT`, so today the only way to reach
any of these refusals, or the `force` escape that spends one, is the Python API.
That is not a defect of this module and it is stated here so nobody reads the
refusal messages as a shipped user experience.

**Closes when:** U27 lands `doctor`, at which point `crate doctor` becomes true
for all forty call sites at once and the guard test above must be deleted rather
than adjusted. **Expires if U27 ships without it:** the remedy is then naming a
verb nobody is building, and the correct move is a new slug rendered as the
ledger's own path.

---

## R-93. A record whose whole directory is gone is not searched for by its bytes

**Found:** during U23's eighth round, 2026-08-04, as the accepted cost of closing
a data loss that round 7 introduced.

Round 7 decided a record was STRANDED, and therefore available to be claimed by
whatever else carried its bytes, from `not Path(record.path).exists()` alone. An
UNMOUNTED VOLUME was then read as a DELETED FILE. Driven on a real `hdiutil`
MS-DOS FAT image, attached, detached and reattached, with the line restored:

    adopted the USB track: original=('USB Own Genre',)
    a byte identical backup copy exists elsewhere: True
    volume detached, so the recorded path exists = False
    second adoption over the BACKUP: records=1
      the USB record survived = False
    volume replugged, USB file re-adopted: original=('Adopted Genre',)

The user's own value ended in no file and no record. `_the_recorded_path_is_vacant`
now asks for the record's containing DIRECTORY to be present and answering before
its file counts as gone, which is positive evidence rather than the absence of
some, and the same drive on the same image reports `records=2`, the USB record
surviving, and `('USB Own Genre',)` after the replug.

**What that costs.** A record whose file was renamed AND whose entire containing
directory was then removed is no longer findable by its bytes. A second record is
written beside it and that record's `original` is the value adoption itself wrote,
which is the same shape R-91 describes. A rename WITHIN a directory that still
exists is unaffected, and that is the case the byte search was built for.

**Why the directory rather than the volume.** The honest distinguisher would be
"is the filesystem this record was written on currently mounted", and nothing in
the record answers it: `st_dev` is not stable across a remount, which is the whole
reason `test_a_REMOUNT_does_not_produce_a_SECOND_record` exists. A present
directory is weaker and it fails in the safe direction, which is the direction
that does not hand one file's record to another.

**Closes when:** the record carries the volume it was written on as something a
remount preserves, at which point "that volume is not mounted" and "that file was
deleted" become different answers instead of the same missing path.

---

## R-94. A stranger's field value that coincides with the recorded one is accepted

**Found:** during U23's eighth round, 2026-08-04, stated as the exact limit of the
decision that closed the shape-2 and shape-3 hole.

When the identity and the path both name this file, or when the recorded path is a
second hardlinked name for it, `_settled_or_refused` asks whether the field holds a
value nothing has written down. It accepts when the field holds the record's own
`original`, what the record says adoption wrote, or what this call is about to
write, and it goes to the bytes otherwise.

**The gap is the first of those three.** If a file is replaced in place by a
different recording whose own value in that field happens to equal the string the
record says adoption wrote, nothing unrecorded appears to be at risk, the record
is kept, and a later revert puts the replaced recording's original onto the new
audio. `written` is a taxonomy bucket's DISPLAY name, shared by most of the library
it was written into, so the coincidence is not exotic: it is exactly the
coincidence this module's own `TagSnapshot` docstring names as the reason a field
value is not identity.

**Why it was accepted rather than closed.** The alternative is to ask the bytes on
every shape-2 and shape-3 match, which is a whole-file sha256 per track on the one
pass that touches every track in the library, to catch a case where the value
recovered by refusing is the same string as the value already there. The cheap
question is asked first precisely because its answer decides whether the expensive
one is worth asking, and the population where it answers wrongly is a replacement
that landed on the same bucket name.

**What it does NOT cover, so nobody widens it by accident.** This is not a claim
that the field value identifies the file. It never decides which record belongs to
a file; the two addresses have already done that. It decides only whether this
write can destroy something, and its wrong answer costs the same as round 7 cost
in every case rather than more.

**Closes when:** the record carries something about the CONTENT that is cheaper
than a whole-file hash and that a replacement cannot reproduce, which is the same
thing R-86 wants for a different reason. A decoded-stream fingerprint of the first
few seconds is the candidate and it is a unit of its own.

---

## R-95. Round 8's own refusal message is asserted by nothing

**Found:** by the independent round 8 verifier, 2026-08-14, row
`H1_unrecorded_value_refusal_reworded` of
`docs/mutation/u23-round-8-independent.md`.

`_a_value_nothing_recorded` is the refusal round 8 added, and it is the whole
user surface of the round: it is what a person sees when a file was rewritten
after adoption ran and writing over it would put a value in no file and no
record. Rewording its opening clause kills **0** tests out of 3782.

**The composite, so the zero is read correctly.** `B1_settled_never_refuses`,
which removes the refusal entirely, kills **4**. So the suite pins that the
refusal FIRES and pins nothing about what it says. The message names the
recorded original, the field, the held value and the two causes a person has to
tell apart, and any of that can be deleted or made wrong with a green suite.

**Cost:** the person meeting the one refusal this round exists to produce is the
person least able to check the message against the code. The same shape is R-78
on `main` for a different message, so this is a class rather than an instance.

**Closes when:** one assertion pins the clauses that carry information, in the
shape `test_adoption.py` already uses for its other refusals: the recorded
original, the field name, and the fact that nothing was written.

---

## R-96. The acceptance for a third adoption under a third taxonomy is driven by no test

**Found:** by the independent round 8 verifier, 2026-08-14, row
`B2_settled_drops_the_bytes_acceptance`, and then driven to establish that the
branch it covers is reachable.

`_settled_or_refused` accepts twice: once when nothing unrecorded is at risk, and
once when the bytes are exactly what adoption left. Removing the SECOND
acceptance kills **0** tests. Removing the whole function's refusal
(`B1_settled_never_refuses`) kills 4, so the first acceptance and the refusal are
both driven and only this branch is not.

**It is reachable and it was driven, not argued.** Adopt a file into bucket 1,
then into bucket 2, then into bucket 3. `record.written` is written once and
stays at bucket 1, the field holds bucket 2, and this call is about to write
bucket 3, so no clause of `_nothing_unrecorded_is_at_risk` accounts for the held
value and the bytes are what decide. Measured end to end through
`write_tag_with_record`: the third adoption is ACCEPTED, one record survives, and
its `original` is still the pre-adoption value. The code is right. Nothing tests
it.

**Cost of the branch being wrong in future:** with the acceptance gone, a third
adoption under a third taxonomy is REFUSED, and the refusal tells the person a
different recording was put in place of theirs when nothing of the sort happened.
The existing round 8 test drives the neighbouring clause, a third adoption
writing the SAME bucket the file already holds, which accepts one clause earlier
and cannot reach this one.

**Closes when:** the three-bucket sequence above is a test.

---

## R-97. The vacancy guard's refused-question branch is reachable and untested

**Found:** by the independent round 8 verifier, 2026-08-14, row
`E3_vacancy_oserror_is_vacant`.

`_the_recorded_path_is_vacant` ends in `except OSError: return False`. Changing
that to `return True`, so a directory that refuses the question is read as a
vacant path, kills **0** tests.

**The producer was driven.** `Path.parent.is_dir()` swallows its errors, but
`Path.exists()` does not swallow all of them: on a directory with mode `000`,
`Path.exists()` raises `PermissionError`, which is an `OSError`, and a path long
enough to exceed `ENAMETOOLONG` raises from `is_dir()` too. Both measured on this
machine. So the branch is reached by an ordinary permission, not by a forgery.

**Cost if it is ever inverted:** a record whose file sits in a directory this
account cannot read would be declared stranded, and its record handed to any
byte-identical file anywhere. That is verbatim the loss round 8 closed for the
unmounted volume, arriving through the other door. The current code is correct
and refuses to guess, which is the right answer.

**The composite:** `E2_vacancy_parent_check_inverted` kills 2 and
`E4_vacancy_always_true` kills 3, so the predicate itself is driven and only its
error branch is not.

**Closes when:** one test adopts a file, makes its containing directory
unreadable, and asserts a byte-identical copy elsewhere does NOT take its record.

---

## R-98. The size filter's saved read is pinned by nothing

**Found:** by the independent round 8 verifier, 2026-08-14, row
`F3_byte_search_drops_the_size_filter`.

Removing the recorded-size filter from `_found_by_its_bytes`, so every vacant
record is hashed against rather than only the ones whose recorded size is this
file's, kills **0** tests.

**It cannot change an answer** and the module says so correctly: two different
sizes cannot be the same bytes, so the digest comparison behind it reaches the
same result either way. What it changes is the number of whole-file reads, which
is the only thing this filter exists for. Round 8 landed a read-count assertion
for the ORDER of the filters (`F4_byte_search_reads_before_it_filters` kills 2)
and none for this filter's own saving.

**Cost:** a future edit can delete the saving and leave the round 8 read-count
regression half re-introduced with a green suite. The population is a ledger
holding stranded records of a different size from the file in hand, which is a
reorganised library, so the cost is reads on the pass that touches every track.

**Closes when:** the existing read-count assertion is extended to a ledger
holding one stranded record of a different size, asserting zero whole-file reads.

---

## R-99. A derived list's drift assertion is a tautology, and 38 cases can leave without it failing

**Found:** by the independent round 8 verifier, 2026-08-14, in the "what a green
suite cannot see" sweep rather than in the mutation table, then driven as
`docs/mutation/u23-round-8-independent-hunt.md`.

`tests/test_adoption.py` derives `LEDGER_CONTAINERS = sorted(tags._DIALECT_BY_SUFFIX)`
and parametrises two suites over it. `test_the_container_list_is_the_writers_own`
exists to stop that list and the writer's own table drifting apart, and says so:
"Both lists, against each other, so neither can drift alone (P3)."

Two of its four assertions are `set(LEDGER_CONTAINERS) == set(tags._DIALECT_BY_SUFFIX)`
and `len(...) == len(...)`. Since the list IS `sorted()` of that mapping, both
reduce to `set(sorted(M)) == set(M)` and `len(sorted(M)) == len(M)`, which hold
for every mapping including the empty one. They cannot fail.

The third assertion, that every `Dialect` has a container, is real but coarse:
every dialect in the shipped table has three or more suffixes, so no single
removal empties one.

**Driven, with the number.** Dropping `.aifc` from `AIFF_SUFFIXES` takes the
`test_adoption.py` and `test_tags.py` subset from **653 collected to 615**, so
**38 cases stopped existing**. `test_the_container_list_is_the_writers_own` PASSED.
The only test that died was
`tests/test_tags.py::test_each_container_is_classified_once[.aifc-Dialect.ID3]`,
and it died only because its own parametrisation spells the suffix.

**Cost:** the ledger's container coverage can shrink by a whole container while
the guard named for preventing exactly that reports success. This is the shape
METHOD calls "a test whose expected value comes from the code under test", and
the derivation is what makes it invisible.

**Closes when:** the assertion compares the writer's table against a list spelled
in the test, or against a count spelled in the test, so the derivation has
something outside itself to disagree with.

---

## R-100. One name, two meanings, and both live inside the adopt package

**Found:** by the independent round 8 verifier, 2026-08-14, in the
"one symbol meaning two things in two modules" sweep.

`digest_of` is two unrelated functions and the adoption package uses both:

* `src/cratekit/adopt/revert.py:1557` defines `digest_of(path, *, deadline_seconds)`,
  a bounded whole-file sha256. It is the only unforgeable evidence in the revert
  ledger and the module's own docstrings call it that.
* `src/cratekit/adopt/plan.py:52` imports `digest_of` from `cratekit.cli.output`,
  which is `digest_of(identity: Any)`, a canonical projection of what a gate
  showed the user. It is what `approval.py` compares an approval against.

Both return `str`, so nothing in the type checker separates them, and both are
called simply `digest_of` inside one package. A second instance of the same
shape: `identity_of` is `identity_of(path) -> str` in `adopt/revert.py`, a volume
and inode claim about a FILE, and `identity_of(store, item_id) -> dict | None` in
`core/review.py`, what a review item was addressed by. The arity differs there,
which is why that one is the milder of the two.

**No user cost is claimed and none was driven.** Both call sites are correct
today. This is recorded because METHOD's second recurring defect pattern is
"identity that is not unique to the thing it identifies", and a fix round moving
a line between `plan.py` and `revert.py` would get a compiling, type-checking,
silently wrong digest: an approval compared against a file hash, or a revert
accepting on a plan projection.

**Closes when:** the two are spelled apart at the point of use, for example
`bytes_digest_of` in `revert.py`, or `plan.py` imports the module and calls
`output.digest_of` so the subject is visible at the call.

## R-101. The merge left two helpers answering one question in the same file

**Found by** the U23 merge, 2026-08-14, while resolving `tests/test_review_queue.py`.

**Measured.** `tests/test_review_queue.py` now defines both
`_target_offers_into(target, queue)` at line 2371, which is `main`'s, and
`_package_offers_into(package, queue)` at line 2652, which is U23's. Both answer
whether a landed import target offers into a review queue. `_target_offers_into`
has 4 uses and `_package_offers_into` has 5. Both are exercised and the suite is
green at 5385 passed, 12 skipped.

**How it happened, because the shape matters more than the instance.** Each
branch independently grew the same guard from "the target is in the pending
register" to "the register counts down to it OR it has landed and actually
offers into the queue". They arrived at the same idea, one file apart in time,
and named it differently. Git had no reason to see a conflict, because the two
definitions do not touch: the conflict it DID raise was in the assertion that
calls one of them, and resolving that conflict correctly still leaves both
definitions standing.

**Measured cost.** None to a user, and none to correctness today. The cost is
the fourth item on METHOD's list of what a green suite cannot see, one symbol
meaning two things, in its milder form: two symbols meaning one thing. The next
person to strengthen the check will strengthen one of them, and the other will
go on answering the older question with nothing pointing at it.

**Why this is a residual rather than something the merge fixed.** Unifying them
means choosing which definition survives and re-pointing nine call sites in a
file neither verifier read in full, inside a merge, with no mutation table over
the result. That is how a merge acquires a defect nobody drove.

**The closing condition.** One helper, whichever handles both the package and
the single module shape, with the nine call sites moved to it, and the removal
driven by checking that the surviving helper still answers False for a target
that offers into nothing.

<!-- ------------------------------------------------------------------ -->

## R-102. The reports allowlist audit is one hop deep, so an admitted module can delegate the writing

**Found:** 2026-08-14, while driving R-80's first closing condition. Not found by
U34's own review, which built this guard, and not by U27's independent
verification. It is a property of the guard rather than of any unit, and it is
live on `main` right now.

**The mechanism, driven rather than argued.**

`test_the_allowlist_admits_no_writer_this_guard_cannot_name` walks the modules
`ALLOWED_IMPORTS` names, through `_admitted_repository_modules`, and asserts that
every writer they expose is a name `FILESYSTEM_MUTATIONS` or
`QUALIFIED_MUTATIONS` carries. The stated argument it defends is that nothing the
reports package can reach can touch a file except through `pathlib`.

**The walk stops at one hop.** It reads the source of each admitted module and
nothing that module imports. Nothing anywhere constrains what an admitted module
may import. So an admitted module can hold a thin caller, put the actual write in
a module the allowlist does not name, and the audit reads the caller as ordinary
code because the callee is never opened.

Driven end to end on `merge/u27-attempt-2026-08-14`, using R-80's own subject
because it was already to hand. `cratekit.core.access_probe` was created holding
the raw `os.open`, `cratekit.core.cause` was left importing and calling it, and
this guard went from RED to **GREEN** with the reachability from the reports
package to a write capable handle completely unchanged.

`test_the_walk_is_bounded_to_the_package_and_the_allowlist_covers_the_boundary`
looks like it covers this and does not. It closes the SIBLING hole, a module
beside the reports package that the package could import and the walk would not
scan. This is the hole one layer further out: a module beside an ADMITTED
DEPENDENCY. The two have the same shape and only the first is asserted.

**What partially covers it today, and why partially is the finding.**
`test_the_package_imports_downward_only` caught the specific relocation above,
because `cratekit.core.cause` is FOUNDATION by explicit name in the layer table
while a new `cratekit.core.*` module falls through to INFRASTRUCTURE. That is a
layering rule doing an allowlist's job by coincidence of where the code landed.
**It was then defeated by adding one name to one regex**, after which the tree
was green apart from two unrelated pre-existing failures. It also does not cover
the general case at all: an admitted module delegating SIDEWAYS, to another
module already at its own layer, violates no import direction and is invisible to
both guards.

**Measured cost.** No user facing cost, and nothing in the tree does this today.
Under the merge bar this is a residual: the input is a future diff and no
producer exists to drive. The cost is that the guard's argument is weaker than
its comment claims in a way the comment does not disclose, and the comment is
unusually careful about exactly this, since it already records an earlier version
of itself being false. This is the same class again, one hop out.

**Why it is worth having a number.** The guard is the load bearing one for R12,
and its whole value is that the argument is falsifiable and gets rebuilt when
falsified. A hole that a reasonable relocation walks through, while both
structural guards report green, is the shape that gets introduced by somebody
doing tidy up rather than by somebody evading a rule.

**The closing condition.** The audit follows imports out of an admitted module
into any first party module and audits those too, transitively, with the closure
computed in one pass rather than a layer per run. The cheaper alternative, a
guard asserting that an admitted module imports only from the allowlist itself,
is stricter than the tree can currently satisfy and would need measuring first.
Either way the fix is driven by planting the delegating module above and
confirming the audit now reports it.

<!-- ------------------------------------------------------------------ -->

## The twelve findings below arrived with the U12 merge, 2026-08-14, and seven were renumbered

They are U12's. `main`'s numbers did not move; the incoming side's did, which is
the rule.

Branch R-14 through R-20 became R-108 through R-114, in order, a flat shift of
ninety four. Six of the seven collided outright, because the branch was cut when
`main`'s highest was R-13 and `main` has since filled R-14 onward with entirely
different findings. **R-18 did NOT collide**, because `main` has a gap there, and
it was moved with its siblings anyway: leaving one finding of a coherent block
behind, seated between `main`'s unrelated R-17 and R-19, is how a number comes to
read as belonging to a sequence it has nothing to do with. Gaps are not tidied
and `main`'s R-18 gap stays open.

R-103 through R-107 arrived from the independent verification and did NOT
collide, `main`'s highest having been R-102, so they keep the numbers they were
filed under.

**Nothing inside the twelve cited any of the moved numbers**, checked rather than
assumed, and no branch file outside this one cited them either. The one token
that looks like a citation and is not is `R23` in R-108's successor, which is a
plan REQUIREMENT identifier rather than a residual, as are R29, R31 and R34
elsewhere in this file. A renumber that treated those as residuals would have
repointed four requirements at findings.

<!-- ------------------------------------------------------------------ -->

## R-103. The analysis countdown is silent on a plan widened without naming PoolPlan

**Found:** during U12's first independent verification, 2026-08-14, driving the
countdown rather than reading it.

`analysis_sizing_violations` in `tests/test_pool_sizing.py` is the whole of R23's
enforcement for the package U25 will ship. Its call-site half,
`unplanned_map_workers`, accepts a plan that arrives as a parameter or off an
attribute, and its docstring says why: "the guard above forbids any module in the
shipped tree from having constructed one, which is what makes accepting it sound
rather than generous."

That premise is false for two shapes, and both were driven through the real
function rather than argued. A two module fixture whose second module reads

    wide = dataclasses.replace(plan, workers=9)
    return pool.map_workers(wide, analyse, items)

returns `[]`. So does one that reads

    wide = type(plan)(9, plan.items, plan.bound, plan.worker_bytes, None, None)

Neither names `PoolPlan`, so `pool_plan_constructions` never fires, and neither
is a construction the walk can credit to the fabricated set, so
`unplanned_map_workers` reads the argument as a plan that arrived from somewhere
legitimate. The countdown reports the package as correctly sized while a pool of
nine model loading children is handed to the runner, which is the exact kill U12
exists to prevent.

For contrast, the third fixture driven in the same run, a module reading the core
count through a rebound alias, `counter = os.cpu_count`, IS caught, because the
core count half of the countdown matches names used anywhere rather than an
import graph.

`dataclasses.replace` is not an exotic shape. `PoolPlan` is a frozen dataclass,
and `replace` is the language's own way to derive one from another.

**Why this is a residual and not blocking.** The producer does not exist. There
is no `cratekit.analysis` package on this branch or on main, it is registered in
`tests/_pending.py` against U25, and the guard is decorated `@requires` so it has
never executed against a real tree. Zero candidate producers were available to
drive, which is a different statement from "nothing produces it": the shape is
reachable the moment U25 writes it, and that is precisely when a green countdown
would be read as proof.

**Closes when:** U25 lands, or sooner. The narrow fix is to treat any call whose
callee resolves to `dataclasses.replace`, or to `type(...)` applied to a name the
walk already knows is a plan, as a construction. The wider and better fix is to
invert the premise: require that every plan reaching `map_workers` be traceable
to a `plan_pool` call in the same module, rather than forbidding the
constructions somebody thought of.

---

<!-- ------------------------------------------------------------------ -->

## R-104. The in-module deadlock guard sees only a bare constructor name

**Found:** during U12's first independent verification, 2026-08-14, driving the
guard's own walk against four spellings.

`test_the_executor_constructor_is_never_written_with_a_recycle_counter` is the
source half of the deadlock guard, and it is the only source level guard on the
deadlock inside `src/cratekit/core/pool.py`, because the repository wide walk
`test_no_module_outside_the_sizing_module_builds_a_process_pool` deliberately
excludes the sizing module and `test_the_sizing_module_would_fail_its_own_guard`
exists to say so out loud.

The walk selects with `getattr(node.func, "id", "") != "ProcessPoolExecutor"`,
which is a bare `ast.Name` and nothing else. Driven against four sources, each
building an executor with `max_tasks_per_child=100`:

| spelling | guard fires |
| --- | --- |
| `ProcessPoolExecutor(...)` | yes, line 2 |
| `futures.ProcessPoolExecutor(...)` | no |
| `process.ProcessPoolExecutor(...)` | no |
| `PPE(...)` after `import ... as PPE` | no |

This is the pattern of a test that forbids the last implementation rather than
the feature. It forbids the way this module happens to spell the constructor
today.

The same shape one file over is the interesting half, and it is the reason this
is worth recording rather than shrugging at. The guard's immediate neighbour,
`test_every_context_this_module_builds_is_written_as_spawn_in_the_source`,
derives its name from `node.func.attr` when the callee is an attribute and from
`node.func.id` when it is not, so it does NOT have the hole. The repository wide
`process_pool_constructions` derives its import shapes rather than listing them
and does not have it either. One guard out of three, sitting between two that do
it correctly.

**Why this is a residual.** Maintainer facing. The runtime half,
`test_no_plan_at_any_recycle_setting_hands_the_counter_to_an_executor`, still
covers every executor built through `executor_arguments`, which is every executor
this module builds today. What is unguarded is a SECOND executor written later
with an attribute spelling and the counter set, which is a defect that has to be
introduced before it can be missed.

**Closes when:** the walk reads `node.func.attr` as well as `node.func.id`, or
better, when it reuses the derived shapes `process_pool_constructions` already
computes.

---

<!-- ------------------------------------------------------------------ -->

## R-105. The relative-import climb guard in the shared source walk kills no test

**Found:** during U12's first independent verification, 2026-08-14, as the one
genuine zero row in a 45 row table.

`_absolute_module` in `tests/_source_guards.py` refuses a relative import whose
dots climb past the top of the package tree with `if level - 1 > len(parts):
return None`. Removing that line kills zero tests, confirmed on the full suite at
3448 collected. Driven, the removal matters for exactly one band of inputs: at a
package of `cratekit.analysis` and level 4, `parts[: 2 - 3]` slices negatively and
returns `cratekit.pool` where the guard returns None. At level 3 and level 5 the
existing `if not base` check catches it and both forms agree. Every input in the
band is an import the interpreter itself refuses, so no importable file can
produce one. Recorded rather than fixed.

---

<!-- ------------------------------------------------------------------ -->

## R-106. The reaping band's reference is a sleep, and the real release it stands in for is twenty four times cheaper

**Found:** during U12's first independent verification, 2026-08-14, by measuring
the thing the fixture stands in for.

`_PROBE_REAP_SECONDS` is bounded by an exact band, `[2.0, 3.0]` times
`_RELEASE_SECONDS`, and `_RELEASE_SECONDS = 0.4` is a `time.sleep` the test file
chose. Round 6 made that literal honest in the only way it could from inside the
file: `test_the_release_the_fixture_declares_is_what_the_ladder_was_timed_paying`
times the terminate-to-exit leg and fails if the fixture stops paying what it
declares. Independently confirmed here over 25 reaps, minimum 0.4025s, median
0.4122s, maximum 0.4152s, and all five disjoint minima of five inside the stated
[0.3600, 0.5000] window. That test does what it says.

What nothing measures is whether 0.4 seconds resembles the thing it stands in
for. The constant's own note says the fixture is "faithful in cost and not in
kind" and that a real release is allocator and kernel work. It does not say what
a real release costs, because nobody had measured one.

Measured now, on this tree, on the shipped ladder. A spawned child allocates 300
megabytes, touches every page so the pages are resident rather than promised,
installs a SIGTERM handler that frees the allocation and exits with the same
arbitrary code the suite's own cooperative child uses, and is reaped by
`pool._reap` through the same `_WatchedChild` wrapper the tests use. Over 15
reaps, all 15 exiting cleanly through the handler: terminate-to-exit leg minimum
0.0119s, median 0.0168s, maximum 0.0189s.

So the real release is 0.042 times the declared one. The shipped budget of one
second is 2.48 real-fixture releases and 59 real-allocation releases.

**What this does and does not mean.** The direction is safe: the fixture is
twenty four times MORE expensive than the closest measurable real release, so
the band demands a budget larger than the evidence requires and nothing is
racing anything. A bytearray is also not a model, and a native runtime's teardown
of memory-mapped weights, device contexts and worker threads can cost far more
than an allocator free, so 0.4 may yet be the better estimate of a real model.
What is established is narrower and still worth having: 0.4 was never measured
against anything on this tree, the one thing on this tree that can be measured
disagrees with it by a factor of twenty four, and the band's ceiling argument,
that a budget above three releases is "a stall in front of a kill that was always
going to land", is stated against a reference that may be twenty four times too
large.

**Why this is a residual.** No user facing cost was measured. The cost of being
wrong in this direction is up to three seconds of reaping per abandoned probe,
once per pool sizing, on a machine already declared too tight to run the pool it
asked for. Nobody loses data and nobody is told anything false.

**Closes when:** the first heavy pass lands and a real model loader exists to
reap. At that point `_RELEASE_SECONDS` should be re-derived from a reap of the
real thing, and this entry is the measurement to compare it against. Until then
the honest record is that the band is exact arithmetic over a number nothing on
this tree corroborates.

---

<!-- ------------------------------------------------------------------ -->

## R-107. Three wall clock assertions on this branch are absolute numbers

**Found:** during U12's first independent verification, 2026-08-14.

`tests/test_pool_sizing.py` asserts `elapsed < 60` at line 2201, `elapsed < 8` at
line 2225 and `elapsed < 15` at line 2517. Each is a bare second count compared
against a `time.monotonic` delta.

`main` now carries `tests/_hardware.py`, whose `time_repeated` and
`threshold_seconds` express a timing bound as a multiple of a calibrated
reference workload, with a stored calibration at
`tests/fixtures/timing_calibration.json`. This branch forked 156 commits before
that landed and has neither file, which is why the three literals are literals
rather than an oversight by their author.

Measured rather than asserted: the 15 second literal was driven 25 times with
`main`'s own harness and passed 25 of 25, median 0.0860s, worst 0.1205s, which is
124 times under the bound. Expressed in the harness's units that literal is
`threshold_seconds(220.5)` on this machine. None of the three is close to biting
here.

**Why this is a residual.** No failure was produced and the headroom is two
orders of magnitude. What it costs is consistency: after the merge these will be
the only timing assertions in the repository not written in the units the
repository adopted for exactly this purpose, and the next person to see one will
not know whether it was considered or missed.

**Closes when:** the branch is merged and the three are rewritten as
`time_repeated(..., threshold_seconds=threshold_seconds(m))`, which is a
mechanical change once `tests/_hardware.py` is present in the tree.

<!-- ------------------------------------------------------------------ -->

## R-108. A pool is sized once and then runs for as long as the work takes

**Found:** during U12 round 2 verification, 2026-08-03.

`plan_pool` takes one reading of available memory and one reading of pressure,
and the plan it returns is spent by `map_workers` over every generation of the
run. At the shipped defaults a ten thousand track folder is fifty generations,
each one a fresh set of children and a fresh model load per child, and every one
of them is built at the width decided before the first child started.

The module's own first brake is described as the one that "adapts to what the
machine is doing right now, which none of the others can see". That is true of
the moment the plan is made and of no moment after it. A machine that had five
gibibytes free when the run was planned and has half a gibibyte an hour later
keeps building two model-loading children per generation, and nothing in the
module looks again.

**Not fixed here, deliberately.** Re-reading between generations is not a
one-line change, it is a change to what a plan IS. Today a `PoolPlan` is the
record of the decision that governed a run, and a width that moves mid-run makes
it the record of the decision that started one. Both `PoolPlan.generations` and
the deadlock reasoning that fixes a generation at `workers * max_tasks_per_child`
are written against a fixed width. Doing this properly means a seam that returns
a new plan per generation, and a caller that can say which plan a result came
from.

**Closes when:** the first heavy analysis pass lands in U25 and can say whether a
run is long enough for the machine to have changed under it. If it is, the seam
is a per-generation re-plan with the narrowing bounded so a transient reading
cannot collapse a run to one worker.

---

*Filed on the U12 branch as R-14, renumbered to R-108 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-109. The work items are the one thing map_workers does not refuse

**Found:** during U12 round 2 verification, 2026-08-03.

`map_workers` refuses a function, an initializer, and now an initializer
argument that could not be sent to a child, on both paths, so that the same call
does not mean two different things depending on how much memory the machine had.
The ITEMS are not held to that rule. A plan of one worker calls
`function(item)` on whatever object it was handed and a plan of two pickles every
item to a child, so a run over unpicklable items still succeeds on a tight
machine and fails on a roomy one, which is precisely the divergence the refusal
exists to close.

**Not fixed here, deliberately.** The refusal costs one pickle per value, which
is nothing for a function and an initializer and is a full serialization pass
over the whole workload for the items. The pooled path pays that pass anyway, so
the cost falls entirely on the in-process path, which is the path a TIGHT machine
takes. Paying a full pickle of every item on the machine with the least memory,
to catch a shape nobody has written yet, is a fix aimed at the wrong machine.

**Closes when:** U25 says what its items are. If they are paths and identifiers,
this is unreachable and the entry closes as not applicable. If any pass wants to
map over objects, the check goes in at that call site where the cost is known.

---

*Filed on the U12 branch as R-15, renumbered to R-109 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-110. A probe child can outlive a parent that dies between start and reap

**Found:** during U12 round 2 verification, 2026-08-03.

`_spawned_probe` starts a real child, waits for its answer, and reaps it with an
escalation that terminates and then kills. That covers every way the PROBE
fails. It does not cover the parent itself being killed in the window between
`Process.start()` and `_reap`, which leaves a child loading a model with nobody
left to end it, on a machine that this module had already decided was tight.

**Considered and rejected here:** marking the probe child a daemon, so the
interpreter's own shutdown ends it. It closes this and it costs more than it
buys: a daemonic process is not allowed to create children of its own, so a
loader that spawns anything internally would fail inside the probe, and a probe
failure returns the floor silently. Trading a rare orphan for a silent
under-measurement of the exact case this module exists to size is the wrong
trade, and it is the shape of a fix that is too restrictive rather than wrong.

**Closes when:** a probe run is cheap enough to supervise from outside, or the
first real loader is known well enough to say whether it spawns.

---

*Filed on the U12 branch as R-16, renumbered to R-110 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-111. The import walk to keep, and the argument the collapse must carry

**Found:** during U12 round 2 verification, 2026-08-03. Fixed in round 3, and
recorded here because the DECISION outlives this unit.

Three files ask the same question about how one source file reaches one module:
`tests/_source_guards.py` holds `ImportsOf`, which `tests/test_review_queue.py`,
`tests/test_cli_contract.py` and `tests/test_pool_sizing.py` all read, and two
sibling copies of the same walk exist elsewhere, one on `main` under the name
`ReviewImports` and one on another branch. Collapsing the three into one is
booked as follow up work and is not done here.

**The verdict, so the collapse does not have to re-derive it.** Keep
`ImportsOf`. It was driven against 18 true positive shapes and 13 false positive
probes and it handles all 18, including every shape the first version of this
unit was blind to, with no false positive on any absolute shape. The reason is
structural rather than lucky: it DERIVES the import shapes from the target
module's own dotted name instead of listing them, so an ancestor package, an
alias, a submodule under another name and a direct symbol import are all one
rule. A listed set of shapes is a set somebody has to remember to extend, and
the two sibling copies are listed.

**The one thing that had to be fixed first, and now is.** The five false
positives it did produce were all relative imports: a file in an UNRELATED
package writing `from .pool import PoolPlan`, `from . import pool`,
`from . import core`, `from .core.pool import PoolPlan` or
`from .. import cratekit` all fired. The cause was inherent to the signature.
`ImportsOf` was handed source TEXT and a target module NAME and nothing else, so
it could not know which package the importing file sat in, and it matched a
relative import by dotted tail. Harmless in this repository today, verified:
there are zero relative imports anywhere under `src/cratekit`.

The importing file's package is now an argument, and a relative import is
RESOLVED against it rather than tail matched, which makes that half exact rather
than heuristic. The data was already there: `repository_modules()` yields `Path`
objects and every caller threw the path away at `read_text()`. All five shapes
are silent with a package, all four that can genuinely reach the module still
bite from the package that owns them, and the fifth cannot reach it from
anywhere, because a relative import may not climb above the top of a package
tree.

**What the collapse must carry.** The `package` argument, at every call site
that walks real files. Without it the walk falls back to the tail heuristic,
which is deliberate so that inline fixtures with no package still work, and the
five false positives come back in the single place every guard reads. That is
strictly worse than three copies each wrong in its own corner, because one wrong
answer would then be everybody's answer.

**Closes when:** the three-way collapse lands. It should keep this walk, thread
`package_of(path, root)` from every walk that holds a path, and carry the
fixtures that prove both directions. The two sibling copies were deliberately
not read while this was decided, so the collapse still owes them a comparison.

**2026-08-15. What the U12 merge discharged, and what is left.** One of the two
comparisons this entry says the collapse owes has been done. At the merge on
2026-08-14 both resolvers were reimplemented in a scratch script and driven over
the same inputs rather than read against each other: 5 packages of 1 to 5 parts,
levels 1 through 7, and 4 module tails including the empty one `from . import X`
produces. 140 cases, 0 disagreements. `main`'s `_relative_module` and this
walk's `_absolute_module` reach the same answers by differently spelled guards,
including the climb off the top of the package tree, so keeping either one
reinstates nothing. The full table is in
`docs/solutions/workflow-issues/a-rewrite-is-not-a-re-measurement-of-the-claim-inside-it.md`.
Both functions are byte identical at head to what was measured, checked
2026-08-15 against `038168a`.

The prediction in "What the collapse must carry" was correct and was paid for.
The merge dropped exactly that `package` forward in the two line `ReviewImports`
subclass, nothing raised, and three tests in `tests/test_review_queue.py` were
driven red to prove it before it was fixed. This entry was on the branch and was
not read at the merge, which is the point of the same solutions document.

What is left: the three-way collapse itself, and the second comparison. The
third copy, `SoftDeleteNames` on the parked branch
`fix/conformance-3-and-soft-delete-reader`, has still not been driven against
this walk. It was read on 2026-08-15 at tip `897ef12` and still matches by
dotted tail, which is a claim about its source rather than about its behaviour.

---

*Filed on the U12 branch as R-17, renumbered to R-111 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-112. The cgroup mount point is read at an assumed location

**Found:** during U12 round 3, 2026-08-03, while fixing the nested cgroup path.

`cgroup_memory_headroom_bytes` now reads `/proc/self/cgroup` to find WHICH
cgroup this process is in, and walks from there up to the mount, which closes
the systemd case where a capped unit sits several levels below the root. What it
still assumes is WHERE the hierarchy is mounted: `/sys/fs/cgroup` for version
two and `/sys/fs/cgroup/memory` for version one.

That is the documented location and it is right on every ordinary host. It is
not guaranteed. The mount points are published in `/proc/self/mountinfo`, and a
host that mounts the hierarchy somewhere else, or mounts only some controllers,
reads as having no cap at all and falls back to the host's own memory reading.
That is the same failure shape this unit exists to close, one layer further out.

**Not fixed here, deliberately.** Reading `mountinfo` means parsing a fourth
kernel format and deciding what to do when a controller is mounted more than
once, which is a real case. The fallback when it goes wrong is the behaviour
this module had before the container fix at all, so the cost of being wrong here
is a pool sized as it was two commits ago rather than a pool sized against
nothing. That is a much smaller hole than the one closed, and closing it
properly is a unit rather than a line.

**Closes when:** a real deployment target is known. If Cratekit ships in a
container image with a fixed layout this closes as not applicable; if it ships
onto hosts nobody controls, the mount points get read rather than assumed, with
the same injection seam the two path constants already have.

---

*Filed on the U12 branch as R-18, renumbered to R-112 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-113. The unlimited sentinel is a benign zero row, and the commit that said otherwise was wrong

**Found:** during U12 round 4, 2026-08-03, correcting a claim rather than the code.

`_CGROUP_UNLIMITED_ABOVE` is four exbibytes, and a published cap at least that
large is read as the kernel saying "no limit". Round 3's commit message put it in
a list of constants "pinned by consequence". It is not, and the measurement is
unambiguous: moved to `1 << 47`, one hundred and twenty eight tebibytes, the
whole suite stays green, and moved to `1 << 50`, one pebibyte, it stays green
too.

A previous version of this paragraph offered `1 << 62`, the shipped value
itself, as the second of those two measurements. Moving a constant to the value
it already has cannot kill anything, so that was a no-op restated as evidence,
which is the exact defect this document exists to record rather than commit.
The replacement above is a real move, and the bottom of the zero range is now
bracketed as well.

**Why it is not being fixed.** The constant cannot move far in either direction
without dying, and the zero row sits in the middle of a range no machine can
reach. Downward it is held tightly, and the edge is exact: `1 << 47` and
`1 << 44` kill nothing and one test respectively, so the floor of the zero range
sits between sixteen and one hundred and twenty eight tebibytes; below that
`1 << 40` kills two and `1 << 35` kills five, because the suite drives real caps
at thirty two gibibytes, a tebibyte and sixty four tebibytes and asserts every
one of them is still a cap.
Upward it is held by the version one unlimited literal: `1 << 63` kills two,
because the number the older kernels actually write must read as no limit rather
than as an absurd cap. What is left unpinned is the span between one hundred and
twenty eight tebibytes and four exbibytes, and nothing publishes a cap in it. A
cgroup limit is a number an administrator sets on hardware that exists, and the
largest machine anybody sells is already covered by a live test.

Writing a test whose only purpose is to kill a mutation in that span would be
inventing a machine to justify a number. The honest record is that this row is
zero, that it is zero for a reason, and that the claim of consequence in the
round 3 commit was overstated.

**Closes when:** it does not. This is recorded rather than fixed. It reopens as
real work only if a kernel or a runtime starts publishing caps above one hundred
and twenty eight tebibytes, at which point the sentinel needs a source rather
than an estimate, and `/proc/self/mountinfo` in the entry titled "The cgroup
mount point is read at an assumed location" is the same kind of answer: read
what the kernel says instead of assuming a bound.

---

*Filed on the U12 branch as R-19, renumbered to R-113 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-114. Containment in the cgroup walk is checked and then read, not read atomically

**Found:** during U12 round 5, 2026-08-04, while closing the symlink escape.

`_cgroup_directories` and `_headroom_in` now resolve every level and every limit
file and keep only what lands inside the resolved mount, which is what closed a
walk that returned a cap from a directory outside the mount entirely. The check
and the read are still two operations. A component swapped from an inside target
to an outside one between them is read, and nothing here holds a descriptor
across the gap.

**Not fixed here, deliberately.** Closing it properly means opening the mount
once and walking down it with `openat` and `O_NOFOLLOW`, which is a different
reader: `Path.read_text` cannot express it, so the whole file access layer that
the pathological-input tests cover would be rewritten to close a window that
requires an attacker who can already write inside the cgroup mount this process
reads. A real cgroupfs permits no symlinks at all, so on every machine this ships
to the window does not exist; it exists because the mount point is an injected
argument, which is the same seam the entry titled "The cgroup mount point is read
at an assumed location" records.

**Closes when:** it does not, unless the mount point stops being injected and
starts being read from `/proc/self/mountinfo` as that entry proposes, at which
point the `openat` walk is the natural shape of that rewrite and this closes with
it.

**Cited by title, never by number.** Residual numbers are assigned per branch and
six of them already collide across this wave with different subjects on each
side, so a citation by number points at whatever entry ends up in that slot after
a merge. Every reference this unit writes, in source, in tests and here, names
the title instead.

---

*Filed on the U12 branch as R-20, renumbered to R-114 at the merge.*

<!-- ------------------------------------------------------------------ -->

## R-115. CI cannot pass on main and has not, so a red CI carries no information

**Found:** 2026-08-14, immediately after the U12 merge, by looking at the run
list rather than at a run. Nothing to do with U12, and it is not a regression.

**The measurement.** Every CI run on `main` in the visible history is a failure,
back through `f2f8d5b`, `01eb6da`, `4b34a81`, `6bff237`, `b4c9b45`, `1ac0cac`,
`4c432cd` and `be7b6e9`. Ten consecutive runs, spanning merges by different
units on different days, while the local battery was clean for every one of them.

**Why, and the reason it is not a bug in any unit.** The workflow runs Linux with
Python 3.13. This product targets macOS and its proofs say so out loud:

- `tests/test_hardware_fixtures.py` and `tests/test_adoption_hardware.py` require
  `hdiutil` and **fail rather than skip** when it is absent, deliberately, because
  "a skipped hardware proof is indistinguishable from a passing one in every
  summary anybody reads". That decision is right and it is what makes these
  tests unpassable off macOS.
- `tests/test_hardware_fixtures.py::test_committed_calibration_loads` refuses a
  calibration captured on a different machine, correctly: 11 CPUs and Python
  3.12.5 against the runner's 2 CPUs and 3.13.15.
- `tests/test_restore.py` needs `rclone`, absent on the runner.
- One deletion test asserts on a path and receives `OS linux not supported!`.

**Measured cost.** No user facing cost, and no correctness cost. The cost is that
a signal exists, is consulted by nobody, and cannot change state: a run that is
red when the tree is perfect is red when the tree is broken, so it distinguishes
nothing. That is the same defect the countdown discharge and the flaky battery
both had, in the shape this repository is least likely to notice, because the
thing giving no information is OUTSIDE the battery rather than inside it. METHOD
rests the entire merge discipline on three locally run commands and never
mentions CI, which is why ten red runs went unremarked.

**Not blocking anything**, and it is not a merge's work to fix.

**The closing condition, and it is a choice rather than a repair.** One of: the
workflow runs on a macOS runner, which is what the proofs were written for and
costs runner minutes; or the hardware and calibration proofs are marked so the
Linux job selects against them by name, which reintroduces exactly the "skipped
reads as passing" hazard those tests were written to refuse unless the job also
asserts that it deselected a known count; or the workflow is deleted, on the
argument that a check nobody can read is worse than no check. Whichever is taken,
say in METHOD what CI is for, because at the moment it is for nothing.

<!-- ------------------------------------------------------------------ -->

## The ten findings below arrived with the U27 merge, 2026-08-15, and were renumbered

They are U27's, and every one of them carried a different number on that branch.
`main`'s numbers did not move; the incoming side's did, which is the rule.

Branch R-16 through R-22 became R-116 through R-122, and branch R-79 through
R-81 became R-123 through R-125, in order. Two shifts rather than one, because
the branch numbered its first seven when `main`'s highest was R-15 and its last
three later, when `main`'s highest was R-78. Both blocks collided: `main` has
since filled R-16 onward and R-79 onward with entirely different findings.

Citations INSIDE these ten were repointed with them. Citations of R-13, R-14 and
R-15 were NOT touched, because those name `main`'s findings and always did, and
the branch's own text says so in the notes it wrote about its numbering.

Each entry carried a `NUMBERING.` paragraph addressed to this merge, saying which
numbers collided and who moves at it. Those are gone, because the merge they were
addressed to has happened and a standing instruction that has been carried out
reads, to the next person, as one still outstanding. What they recorded is above.

<!-- ------------------------------------------------------------------ -->

## R-116. Three read-modify-write cycles over one document, none of them locked

**Found:** during U27, while hunting the shape the last two waves both shipped.
**One of the three is CLOSED here. Two remain, and they are the two the
reasoning below actually covers.**

`core/config.py` ships an `fcntl.flock` class whose docstring names this exact
hazard, and the two units that ignored it lost real records. Three cycles in
landed code had the same shape. None of them was new to this unit, and U27's own
verbs sit on top of all three, which is why it is recorded here rather than
carried in somebody's head.

**Closed here: the credential presence index.** `secrets.set` and
`secrets.delete` now hold an exclusive lock across the read and the write, and
`credential_index_lock` is declared in `STATE_FILES` beside the file it guards,
in the shape `core/jobs.py` and `core/review.py` already use. Three things made
it separable from the two below rather than part of them: it is in a different
file that no unit in this wave is editing, its cycle contains no prompt, and it
is four lines. What made it the URGENT one is that its loss makes a report LIE.
`secrets.exists` is doctor's `credential_recorded` probe, so an entry lost to a
race becomes `credential.provider: not recorded` for a credential the keychain is
holding, and the remedy sends the user to record it again. Measured before the
fix: two processes recording one credential each left the keychain holding both
and the index naming one in 23 of 25 trials, with both calls returning normally;
three concurrent adds lost at least one in 40 of 40.

**STILL OPEN, and both are the same document:**

1. **`crate setup`.** Read the configuration, ask, write it back.
   `cli/setup.py:201` reads through `config.load`, `cli/setup.py:778` writes
   through `config.save`, and the questions are in between. Two concurrent
   wizards each read the same document and the second write erases the first set
   of answers while reporting success.
2. **`crate profile set`.** The same cycle over the same file, landed in U5:
   `cli/verbs/profile.py:40` reads through `config.load` and
   `cli/verbs/profile.py:156` writes through `config.save`. A lock taken by setup
   alone would not help, because the two verbs would have to agree on the lock and
   only one of them would be holding it. That is what makes `config.save` the
   placement rather than either caller.

The call sites are given with file and line so the closing unit does not re-run
the hunt. They will drift; the two functions will not.

**Why not fixed here.** The right lock is around `config.save`'s whole cycle
rather than around one caller, and that is a change to a foundation file three
units are editing in this wave. The loss rate is comparable to the two defects
that shipped in the last wave rather than worse than them.

**A REQUIREMENT ON THE FIX, not a note about it.** `config.save` may not hold the
lock across the wizard's prompt. Setup reads, asks a person questions, and then
writes, so a lock spanning that cycle blocks a second process on somebody typing,
for as long as they take. The closing change is therefore the decide-outside,
re-decide-under-the-lock shape that `core/config.py:load_from_path` already uses
and documents at length: answer the caller from the first pass, then take the
lock, re-read what is actually on disk, and re-decide from that. Any fix that
holds one lock from the first read to the final write satisfies the letter of
this finding and is not shippable.

**How likely, honestly.** Both are foreground interactive acts on a single-user
installation. The damage is real and the window is small, which is exactly the
profile of the two defects that shipped.

**Closes when:** the configuration read-modify-write goes through one locked
helper that every writer uses, in the re-decide-under-the-lock shape above, with
a test that drives two writers over one document and asserts neither set of
answers is lost.

**No unit owns this.** Deliberately not assigned: inventing an owner for an
obligation nobody accepted is the inference R-13 spent a wave undoing. It needs
an issue of its own.

---

## R-117. Three answers that claim slightly more than the check observed

**Found:** during the third review of U27, 2026-08-03. Recorded rather than fixed
by decision of that review: none is a false green, each is a sentence that is
true of the common case and wider than the thing actually measured.

**1. A library root that exists as a FILE now derives an identity.** The derive
guard asks whether the walk crossed a directory a volume would fill. A path that
exists as a regular file crosses nothing, so an identity is read, and it is the
right volume's identity, which is why this is not a safety regression: the run
then fails later when something tries to create a directory under it. The earlier
"the root must be a directory" rule refused it up front, which is better service.
**Closes when:** the wizard validates that `library.root` is a directory or is
absent, separately from the volume question, and says which of the two is wrong.

**2. `library.db_containment` says more than path containment proves.** Its OK
detail reads "library.db_path sits under library.root, so a snapshot commits
atomically with a rename", and the check is a pure textual containment test. A
filesystem mounted at or under `db_path` puts the two on different filesystems
while the paths still nest, so the rename is a copy and the inference is wrong.
Rare, and it is a real shape: a database on its own volume mounted inside the
library tree. **Closes when:** the check compares `st_dev` for the two paths, or
the sentence stops claiming the consequence and states the containment it
measured.

**3. `keychain.reachable` states an observation it did not make.** Its OK detail
reads "a keychain backend that can store a credential is available", and the
probe is `secrets.backend_available`, whose own docstring calls it a heuristic
about a backend CLASS rather than an observation about a call: it asks keyring
which backend it would choose and reads that backend's priority. A backend that
resolves and then fails on write reports green here, which is exactly why
`secrets.set` verifies its write by reading it back. **Closes when:** the detail
says what was asked, or the check performs a real round trip against a scratch
entry, which is a decision about whether a health check may write.

---

## R-118. Five places where "I could not look" is still not said out loud

**Found:** during the fourth review of U27, 2026-08-03, while closing the four
that were blocking. Recorded rather than fixed because each needs a decision or a
platform this run could not drive, and none of them reports a false GREEN: they
either err toward a refusal or are loud.

**1. Windows has no row in the mount-location table, so the derive refuses
nothing there.** `preflight._VOLUME_MOUNT_LOCATIONS` declares macOS and Linux.
`volume_mount_locations` answers with an empty tuple everywhere else, and the
caller reads that as "nothing to refuse", which is right for a platform nobody
has described and wrong for Windows specifically: `windows_volume_identity`
exists, so an identity IS recorded there, and it is recorded off whatever the
walk finds with the drive detached. The reason it is not fixed here is that a
Windows volume is a drive root rather than a directory under a mount directory,
so the row is a different shape, and inventing an untested shape for the one
platform this machine cannot drive is how the guard becomes a no-op that reads
as coverage. **Closes when:** somebody with Windows adds the row and drives it,
or the derive refuses outright on a platform with an identity adapter and no
mount-location row.

**2. A volume hand-mounted somewhere the table does not name is accepted while
it is unmounted.** The rule only asks about slots it knows about, so a volume
mounted at a path of the user's own choosing has no slot, and the identity read
with it detached is its parent's. Stated in `identity_source`'s own docstring.
**Closes when:** the wizard offers to record the mount location it observed, or
the table is read from configuration.

**3. An ancestor this account cannot traverse. CLOSED 2026-08-04, by the SIXTH
review, having been reported closed by the fourth and the fifth.** ~~The wizard
exits with a traceback, which is loud rather than wrong.~~

**READ THE LAST PARAGRAPH OF THIS ITEM FIRST.** It was closed three times at six
call sites and found again three times, and the reason is recorded there: a fix
per call site is a fix the next call site does not have.

The entry above is struck out because it was wrong about the fact and wrong about
the severity, and the error was load bearing: it is the whole argument for having
deferred the item. Driven end to end, `crate setup --library-root <sealed>/lib`
produced no traceback at all. The dispatcher's blanket at `cli/__init__.py`
caught the `PermissionError` and rendered

    setup: failed (INTERNAL)
    internal-error: PermissionError: [Errno 13] ...
    fix: this is a defect; report it with the cause identifier below

and exited 1. So the product CLASSIFIED THE USER'S OWN FILESYSTEM PERMISSION AS A
CRATEKIT DEFECT and sent them to file a bug report, in the one verb whose entire
job is getting a fresh clone to a first write. And the trigger is routine on the
platform this ships for first: on macOS a library root under Documents, Desktop,
Downloads or an external volume raises EPERM from `stat` for any interpreter
without Full Disk Access, and `Path.exists` re-raises EPERM rather than answering
False. That is a normal first-run state rather than a sealed-directory curiosity.

**How it is closed.** `cause.REASONS` declares `library-root-unreachable`, on the
reserved `LIBRARY_UNAVAILABLE` code, and `exit_codes.Remedy` declares
`GRANT_PATH_ACCESS`, which is a different act from mounting a volume: nothing is
missing and nothing needs plugging in. `cli/setup.py:_resolve_volume_id` raises
that refusal, naming the path and both ways out, and `_seed_taxonomy` writes it
as a finding rather than raising, because the configuration is already saved by
the time it runs and the report is what the user reads. Doctor's behaviour was
already right, exit 30 with every check answered, and is now pinned so the two
cannot drift apart.

**And the same collapse one screen lower, which the first pass moved rather than
closed.** Handling the mount question at the top of `_seed_taxonomy` left two
more filesystem calls unhandled at the bottom of the same function. `path.exists`
over a `.cratekit` directory this account cannot traverse re-raises, and
`config.atomic_write_bytes` raises for a state directory it may not write in and
for a library volume mounted read only. Both escaped into the same blanket and
were rendered as the same defect report, over a library root that is perfectly
reachable, so nothing above them refused first. They are handled as two findings
rather than one, because "could not look at the path" and "reached the path and
was refused the write" are different acts, and the second is a routine state for
anyone whose library sits on a volume mounted read only. The one-line advice on
`GRANT_PATH_ACCESS` was widened to "cannot reach or write" for the same reason:
as written it asserted a directory could not be opened, which is false of the
whole write half, and each finding names its own act in its own detail.

**AND SITE BY SITE GUARDING FAILED THREE ROUNDS RUNNING, WHICH IS WHAT ACTUALLY
CLOSED IT.** The paragraphs above describe six call sites, closed across two
rounds, and the sixth review found three more: doctor's own check runner attached
`REPORT_DEFECT` to the permission for four checks at once, `_probe_db_path`
stat-ed a path nobody had guarded and took the whole verb down with it, and
`os.path.ismount` swallowed the permission and reported an attached volume as an
absent one. One `crate setup` report said "this is not a defect, grant this
interpreter access" from the wizard's note and "this is a defect; report it"
three lines below from four checks, over one path and one permission.

The rule is now a CLASSIFICATION rather than a handler. `cause.permission_denied`
answers "is this an `OSError` whose errno is EACCES or EPERM, here or on its
declared `__cause__` chain", `cause.access_remedy` turns that into a token, and
the two blankets that exist for what nobody guarded both ask: the dispatcher in
`cli/__init__.py` and the check runner in `cli/doctor.py`. So a site nobody has
converted still comes out as a permission the user can grant, and what is left
for a call site is a better SENTENCE, never the difference between a defect and a
permission. `cause.REASONS` declares `path-permission-denied` on the reserved
`PRECONDITION` code for the generic case; `library-root-unreachable` stays for the
refusal that knows the path was the library's.

The trigger for the whole class is one standard-library behaviour worth naming
once: `Path.exists` and `Path.is_dir` RE RAISE under EPERM rather than answering
False, so every line in the package that reads like a question is a line that can
throw.

**AND THAT CLOSE WAS ALSO WRONG, FOR THE FOURTH TIME, AND THE SEVENTH REVIEW SAYS
WHY.** "A site nobody has converted still comes out as a permission" was true and
irrelevant. An AST walk over `src/cratekit` counts nineteen `except OSError` sites
that raise a STRUCTURED refusal, and eighteen of them never reach either blanket,
because a blanket only ever sees what nobody caught. Three of the eighteen hard
coded the wrong answer, and one of those rendered a refusal as "no session is
recorded with the identifier x", which reads absence out of a read that never
happened. The hole had moved from unguarded lines to converted ones, which is the
same shape as the three closes before it.

The decision now lives in `cause.classified`, called from `CratekitError.cause`,
which is the constructor every structured refusal in the package passes through.
It reads the DECLARED cause chain, which is what `raise ... from exc` sets, so
nothing is inferred from the call stack and a handler that recovers and later
raises something unrelated is not re-labelled. Three further gaps closed with it:
the classification answered for the `OSError` family alone and this program keeps
its own state in SQLite, whose refusals carry no errno and no filename; EROFS was
not classified at all, so a read only volume was sent to Full Disk Access; and a
kernel refusal with no path was claimed as a path, producing "grant access to the
path named below" with nothing below it.

**4. `secrets.exists` answers False for a presence index it could not read.**
`_index_read` catches `OSError` and `ValueError` alike and returns an empty set,
so an index this account cannot open reads as "nothing recorded". It errs toward
a FAIL that tells the user to record a credential the keychain may already hold,
which is the loop R-116 measured, reachable from a permission rather than from a
race. **Closes when:** the reader tells a missing index from an unreadable one
and doctor says which it saw.

**5. Two answers from R-117 still claim more than they observed.**
`library.db_containment` infers an atomic rename from pure path containment, and
`keychain.reachable` states an observation when its probe is a heuristic about a
backend class. Both were judged in round three and the judgement stands; they are
repeated here so that a reader of the newest entry sees the whole set.

---

## R-119. A hand-mounted volume at `/mnt/<name>` is now accepted while detached

**Found:** during the fifth review of U27, 2026-08-03, as the deliberate cost of
closing the over-restriction the same review found.

`preflight._VOLUME_MOUNT_LOCATIONS` no longer declares `("/mnt", 1)` for Linux.
Every row in that table is a claim that an empty directory there is evidence of
an absent volume, and the rule built on it refuses a slot with nothing mounted
in it. The claim holds for a location a mounter creates and removes around a
mount. It is false for `/mnt`, which the filesystem hierarchy standard reserves
for mounting by hand, so the directory is made by hand and stays whether or not
anything is mounted.

What the row cost was total: Linux has no identity adapter, so every mount
outcome there is `IDENTITY_UNAVAILABLE` and the write leg always goes through
`root_can_be_created`, which the row made permanently False for a library at
`/mnt/<name>/music` on an ordinary root filesystem. The wizard refused to write
the active template, doctor read for it, found nothing, and answered
`taxonomy.active` FAIL with run-setup, so the user re-ran setup forever with no
way out, `--volume-id` included.

What losing it costs is what R-118 item 2 already records for every hand-mounted
location: a drive mounted at `/mnt/<name>` is accepted while it is detached, and
the identity read with it detached is its parent's. On Linux that identity is
never recorded automatically, because there is no adapter to read one, so what
remains is a taxonomy copy landing on the root filesystem instead of on the drive.
**Closes when:** the wizard offers to record the mount location it observed, or
the table is read from configuration, which is the same close as R-118 item 2.

---

## R-120. Two rescues that are kept without being covered

**Found:** during the fifth review of U27, 2026-08-03, while driving the twenty
handlers a verifier's sweep found covered by nothing.

Both are argued in the source beside the handler rather than only here, which is
the standard the review set: a handler nobody exercises is a claim nobody has
checked, so it either gets driven or it says out loud why it cannot be.

**1. `doctor._run_findings` rescues an `OSError` from `Path.glob` that CPython
does not raise.** Measured on this interpreter: `glob` swallows `PermissionError`
inside its own scandir walk, and answers with an empty result for a run directory
somebody replaced with a plain file. Neither shape reaches the handler through a
real filesystem. It is kept because the swallowing is an implementation detail
rather than a documented promise, and losing the whole `crate status` verb to a
future change of mind would be worse than a handler that never fires.

**Narrowed by the sixth review.** The unmeasurable thing is the TRIGGER, and that
was being used to excuse leaving the CONTRACT unwritten, which is how it sat as a
rescue no test exercised. The contract is assertable whatever CPython does: a
walk that refuses costs the report its run records rather than the verb.
`tests/test_doctor.py` now states it by handing `_run_findings` a run directory
whose `glob` raises, and the `# pragma: no cover` came off. What is still
residual is only that no arrangement of a real filesystem produces the raise.
**Closes when:** the standard library documents the behaviour either way, or the
walk is done with `scandir` here so the failure is this module's to catch.

**2. `Finding.cause` is not carried into the diagnostic payload.** A check that
refuses under a declared reason now keeps its reason, remedy, steps and reserved
exit code, and all four travel in the envelope's `cause`. The per-check entries
in `data.checks` are unchanged, so a consumer reading only that array sees the
refusal's message and remedy but not its slug. The envelope is where a machine
consumer reads a reason, and adding a key to every check entry for a field that
is None on all of them is a schema change for one case. **Closes when:** a second
check refuses structurally and a consumer needs to tell which one did.

---

## R-121. Three edges of the permission classification, stated rather than closed

**Found:** during the sixth review of U27, 2026-08-04, while making "a permission
the user can grant is not a defect in this program" one decision instead of six
handlers.

**1. The classification reads `__cause__` and deliberately does not read
`__context__`.** An explicit `raise X from exc` is a statement that this failure
IS that failure, so a wrapper cannot hide a permission underneath it. An implicit
context is only "this happened while handling that", which is exactly what a
handler that catches a permission and then raises a real defect produces, and
reading it would file that defect under a permission the user is told to grant.
The cost is the mirror case: a wrapper that re-raises without `from` hides the
permission, and its failure is reported as an internal defect. Chosen because the
two errors are not symmetric. Reporting a defect as a permission sends a user to
change filesystem permissions that were never the problem and leaves the defect
unreported; reporting a permission as a defect is the state this whole item
records, and it is caught by the two blankets for anything that reaches them
unwrapped. **Closes when:** a real wrapper in this package is found re-raising an
`OSError` without `from`, at which point the fix is the `from`, not the reader.

**2. `config._read_raw` still calls a permission a corruption.** A configuration
file that is present and that this account may not open raises `ConfigCorrupt`,
whose remedy token is `repair-config-file`. It is the same shape as the
`backup.age` finding this round closed, one module over, and it is NOT reached in
the arrangement that matters most: `config.load` stats the file first, so a
SEALED ANCESTOR raises before this line and is classified correctly. What reaches
it is a config file whose own mode is unreadable under a readable parent. It is
recorded rather than fixed because `core/config.py` belongs to U2 and its five
error types are a declared vocabulary with their own suite; changing which one a
permission maps to is that unit's decision rather than a fix smuggled in under
this one. **Closes when:** U2 splits "could not be read" from "could not be
understood", which is the same split this unit made in four other modules.

**PARTLY CLOSED IN ROUND SEVEN, at the three hops this unit owns.** The scoping
above is still right about `core/config.py` and was being used to leave the same
shape standing in files that are not U2's: `cli/setup.py` gave
`repair-config-file` for its own second read of a sealed document, `doctor`'s
`config.present` check read the remedy straight off the error class, and the
dispatcher's `ConfigError` branch did the same at the last hop. All three now ask
the classification first, so a document that is byte for byte intact is not
called unrepairable, and a `ConfigCorrupt` raised by `core/config.py` itself gets
the right ACT at every surface a user reads even though its type is unchanged.
What is still open is the type, which is U2's to change.

**3. `_names_one_path` compares paths, not directories, and is named for it.** It
was `_names_one_directory` and never asked whether either side was a directory:
two spellings of one regular file, and a FIFO compared with itself, both answered
True under a name that promised otherwise. The name is now honest and the
behaviour is unchanged, because the caller compares an ancestor against a
DECLARED mount directory, so the directory-ness belongs to the declared row. A
version that stat-ed for `is_dir` would refuse a first run into a mount slot that
does not exist yet, which is the over-restriction rounds three and four both
produced. **Closes when:** the declared rows are validated where they are
declared, so the comparison never has to.

---

## R-122. Four edges of the round eight classification, measured and left open

**Found:** during the eighth review of U27, 2026-08-04, while closing the two
channels a refusal travels: the exception a site raises, and the finding a site
reports.

**1. A read only volume names the atomic writer's temporary file.** Driven on a
real `hdiutil attach -readonly` HFS+ image, `crate setup` answers `path-read-only`
with `remount-writable`, which is the act, and the path it names is
`.../coupled/tmpXXXX.tmp` rather than the destination beside it. The write fails
while the TEMPORARY file is being created, so the kernel's error carries one
filename and that filename is the temporary one; the destination-first rule in
`_refused_path` exists for the `os.replace` half, which never runs here. The
volume is the actionable content and the volume is right, and the destination is
named in the same sentence by the wizard's own words, so the report is
actionable and the path line is momentarily confusing rather than wrong. Fixing
it means a second hand-off like `name_the_database`, at
`config.atomic_write_bytes`, so the destination travels with a refusal that
happened before any destination was touched. **Closes when:** the guarded writer
grows that hand-off, or `atomic_write_bytes` reports the destination as
`filename2` on the way out.

**2. The open side of `open_db` records a path that nothing drives.** The mutation
row `M8-02-open-path` kills zero, and the reason is measured rather than guessed:
`Rekordbox6Database` does not connect while it constructs, so every failure it
raises there is a Python level error or an `OSError` carrying its own filename,
and both are already classifiable without a recorded path. The case the recording
exists for is a driver level `sqlite3.Error` at construction, which only an
eagerly connecting binding produces. It is kept because the slug on that handler
shares the canary's exit band and therefore its `restore-from-snapshot` default.
**Closes when:** the binding connects while it constructs, at which point the row
starts killing the sealed-database test, or the binding is replaced.

**3. `os.link` and `os.symlink` appear nowhere in `src/cratekit`.** The measured
pick between two named paths is therefore correct and unexercised by production
code today: it is driven from a real `os.link` out of a sealed directory in the
suite, and the shape it protects against is equally reachable from `os.rename`
whenever the SOURCE side is what the kernel refused, which no writer in this
package currently arranges. **Closes when:** a writer links or renames with a
source it does not control, at which point the row stops being latent.

**4. The probe does not cover a mount that has stopped responding.**
`_probe` opens with `O_NONBLOCK`, which returns immediately for a FIFO with no
writer and does NOT cover a blocking wait inside the virtual filesystem layer, so
a hung network mount would still block there. This was not measured, because no
stalled mount was available to drive it, and it is recorded as unmeasured rather
than claimed either way. **Closes when:** a stalled mount can be arranged in the
suite, or the probe grows a deadline.

## R-123. Four reporting sites inside doctor use round eight's mechanism at none of them

**Found:** by the independent verification of U27 round eight, 2026-08-14, driven
rather than read.

Round eight added `error` to `doctor.Finding` and classified at construction, so
that "a failing refusal reaches the envelope as one instead of as N checks are
failing with a null remedy". It wired the parameter at three sites, all of them
in `cli/setup.py`. `cli/doctor.py`, which DECLARES the field, passes it at zero
of its own six `access_remedy` sites, four of which build a `Finding` from a
caught exception: `_check_config`, `_check_taxonomy`, `_check_commit_hook`, and
the unstructured leg of `answer`.

**Measured, not argued.** A library whose active template sits under a directory
this account cannot open, which is the state `cli/doctor` names in three separate
docstrings as the routine macOS first run shape, arranged with `chmod 000` on the
coupled directory and driven through `doctor.run` on the green machine:

| what | measured |
| --- | --- |
| `taxonomy.active` status | `fail` |
| `taxonomy.active` remedy | `grant-path-access`, which is right |
| `taxonomy.active` cause | `None` |
| envelope reason | `doctor-check-failed` |
| envelope remedy | `None` |
| envelope detail | `{"failing": [...]}`, carrying no path |

The same exception handed to a `Finding` as `error=` answers `path-permission-denied`
with `grant-path-access` and a detail carrying the path. So the mechanism works
and the module that owns it does not call it.

**Why this is a residual and not a block.** The exit code does not move:
`doctor-check-failed` and `path-permission-denied` both map to PRECONDITION, code
30. The finding level remedy is correct, so the rendered steps line carries the
fix a person reads. What is lost is the machine readable half of one refusal:
the reason slug a caller branches on, and the path in `detail`. Nobody loses
data, nobody is told anything false, no verb is blocked, and the report is red
rather than falsely clean.

The asymmetry is the sharp end. Over ONE path and ONE permission, `crate setup`
now reports a structured `path-permission-denied` and `crate doctor` reports
`doctor-check-failed` with a null remedy. That is this project's own recurring
shape: a fix that lands on the sites it was handed and reproduces the class one
file over.

**Closes when:** the four `Finding` building handlers in `cli/doctor.py` pass
`error=exc`, or `answer` classifies centrally for every check the way the
dispatcher's blanket does.

## R-124. The interpreter ceiling guard forbids the current number rather than the declared one

**Found:** by the independent verification of U27 round eight, 2026-08-14, in the
hunt for a test that forbids a feature by naming an implementation.

`tests/test_packaging.py::test_the_doctor_reads_the_installed_bound_rather_than_a_constant`
walks every string constant in `src` and fails if one contains both `3.14` and
`<`. The property it exists for is "the interpreter ceiling is declared once, in
`pyproject.toml`, and never repeated in the package". The literal `3.14` is not
read from `pyproject.toml`; it is typed into the guard.

The consequence is silence rather than a failure. Raise the ceiling to `<3.15`
and the guard keeps passing while forbidding a string nothing writes any more,
so the day somebody does repeat the new ceiling in `src` is the day nothing says
so. Its sibling in `tests/test_doctor.py::test_the_declared_bound_is_read_from_packaging_rather_than_repeated`
does NOT have this shape, because it asserts the bound is present in
`pyproject.toml` first and would go red on the same bump; that one is a guard
that fails loudly when it goes stale, which is the difference.

**Cost:** one guard silently stops guarding at the next version bump. Nothing
user facing today.

**Closes when:** the ceiling is parsed out of `pyproject.toml`'s
`requires-python` and the scan looks for whatever it finds there.

## R-125. Seventeen of forty two independently derived mutation rows kill nothing

**Found:** by the independent verification of U27 round eight, 2026-08-14. The
full table is `docs/mutation/u27-round-8-independent.md`; this records what the
zeros mean so a later reader does not re-derive them.

Forty two rows, twenty five deaths, seventeen zeros, null control zero, no
collection drift on any row. Every zero was promoted to the full suite before
being reported as one. The zeros cluster into six families, and in every family
something IS pinned, measured in the same batch rather than argued:

| family | unpinned, kills 0 | pinned, and by how much |
| --- | --- | --- |
| the two path measurement | candidate ORDER (`C4`), probe MODE (`C5`), and measuring the EROFS side at all (`C7`) | dropping the measurement kills 1 (`C6`), dropping the both paths precondition kills 22 (`C8`), and classifying a read only volume as a permission kills 3 (`C7_composite_kind`) |
| the copytree classification | the class name half of the identity check (`C9`), probe MODE (`C11`), and its position ahead of the errno rule (`C12`) | asking the destination instead of the source kills 1 (`C10`) |
| the database probe | the read versus write mode chosen from `SQLITE_CANTOPEN` (`C14`) | a probe that answers None for every refusal kills 3 (`C14_composite_probe_blind`) |
| the canary's file | which SOURCE the path comes from (`W2`), the `detail` payload it builds (`W4`), `handle_path` itself (`W1`), and `open_db` supplying one (`W6`) | dropping the hand off kills 1 (`W3`), rewording the sentence kills 1 (`W5`), and naming the WRONG file kills 1 (`W2_composite_wrong_file`) |
| the finding's classification | building a cause for any status (`D3`), OVERWRITING a cause the branch already built (`D4`), and the `compare=False, repr=False` on the field (`D5`) | not classifying at all kills 2 (`D1`), not overruling the hard coded remedy kills 2 (`D2`), and a wrong reason slug on the constructed cause kills 2 (`D4_composite_reason`) |
| the wizard's hand off | the mount resolution branch (`S4`) and the already there probe branch (`S5`) | the branch that WRITES to the library volume kills 1 (`S2`), the closing clause kills 5 (`S1`), and the hard coded sentence kills 2 (`S3`) |

Two of these are worth naming on their own.

`C12` is inert rather than untested: `shutil.Error` is an `OSError` subclass
carrying `errno` None, so the errno rule answers None for it whatever the order,
and asking the copy rule first is a statement of intent rather than a behaviour.

`D4` is the one a later reader should look at first. Nothing pins that a cause a
branch built for itself survives construction, so a future branch that supplies
its own cause AND an exception has no guard saying which one the report carries.

Three rows were considered and not run at the forty five cap, and five
composites were considered and not run; all eight are logged in the table's own
`Dropped` section with the reason each was ranked below the cap.

**Closes when:** each family's unpinned half acquires an assertion, or the
family is deliberately declared as intent rather than behaviour in the code.

<!-- ------------------------------------------------------------------ -->

## R-126. The write probe's one undriven class is a network mount, and it is undriven for both designs

**Found:** at the U27 merge, 2026-08-15, while deciding R-80. Recorded rather
than resolved, because the arrangement it needs was not available.

`_probe_writable` attributes an already refused write from metadata:
`os.statvfs` `ST_RDONLY`, the per-file immutable flag, and `os.access`. Twelve
real arrangements were driven against the write capable handle it replaces and
every one that its producer can reach agrees.

A network mounted volume is the class where they COULD diverge and neither was
driven there. On a share whose server refuses the write while the client holds
cached attributes, the metadata reading answers from the client and reports
nothing, and the classification falls through to an unclassified errno.

**Say it as a symmetry, not as a loss.** An `os.open` on that same client does
not necessarily reach the server either: whether it does depends on the protocol
and on the attribute cache, and SMB and NFS differ. So the honest statement is
that the class is unmeasured for both designs, and that the write handle's
advantage there is an argument rather than a measurement. The reframing in R-80
weakens it further: the probe runs only after the driver established the write
was refused, so client staleness costs an attribution rather than a prediction.

**Measured cost.** None observed. The failure mode when nothing attributes the
refusal is an unclassified error, which is honest rather than false: the user is
told the program did not anticipate it, not told to perform an act that cannot
work. Nobody loses data and nobody is told anything untrue.

**Closes when:** a network share can be arranged in the suite and the two designs
are driven over it, or the product declares that a library on a network share is
out of scope and the probe says so where it answers.

<!-- ------------------------------------------------------------------ -->

## R-127. The write probe asks for the effective identity and nothing on this machine can tell

**Found:** by the write probe's own mutation table at the U27 merge, 2026-08-15.

`_probe_writable` calls
`os.access(path, os.W_OK, effective_ids=os.access in os.supports_effective_ids)`.
Asking for the effective identity is right, because the write the driver made
used it and `os.access` otherwise answers for the real one.

**Row W6, measured: forcing that argument to False kills ZERO tests.** Promoted
to the full suite before being reported as a zero, per METHOD.

**Why, measured rather than argued.** This process runs `uid=501 euid=501
gid=20 egid=20`, and `os.access` answers the same both ways on a file at mode
464, so nothing on this machine separates the two. Separating them needs a
setuid binary, and this program is never setuid.

**Maintainer facing, so it gets this line and no composite**, which is METHOD's
rule for a zero row whose severity floor means it can never block. The argument
is kept because it is the correct question to ask, not because a test holds it.

**Closes when:** an arrangement exists where the real and effective identities
differ, or the argument is dropped with the reason recorded that it can never
matter here.

<!-- ------------------------------------------------------------------ -->

## R-128. The remedy correction landed on the raising path and the consuming path still replaces it

**Found:** at the U27 merge, 2026-08-15, while reserving `grant-path-access`.

U27 added `GRANT_PATH_ACCESS` to `backup_facts.Remedy` so that a directory this
account cannot open stops being reported as a damaged fact file. That is the
right correction and the raise site's own comment explains it at length.

`src/cratekit/core/session.py:1042` catches EVERY `BackupFactsUnreadable` at one
site and re-raises it as the cause `backup-facts-unreadable` with
`remedy=Remedy.REPAIR_BACKUP_FACTS`, without reading the exception's own remedy
at all. So a person whose directory is unreadable is told to repair or reset the
very record the raise site was changed to stop blaming.

**This is defect pattern 3 from METHOD**, a fix that lands on the performing path
while the checking path keeps the old answer, and it is worth naming as that
rather than as a one off.

**Measured cost.** The exit code does not move. `grant-path-access` is reserved
at `ExitCode.ACK_REQUIRED`, 32, and so are `repair-backup-facts` and
`upgrade-cratekit`, so a caller branching on the code sees the same integer
either way. What is lost is the remedy TOKEN a machine consumer reads and the
sentence a person reads, on one refusal. Nobody loses data and no verb is
blocked, so it is a residual.

**Why the reservation was made at 32 anyway.** The table's rule is to agree with
the landed conversion rather than with the intended one. Reserving anything else
would reserve a conversion that does not happen, and would make the registry
describe a build nobody has.

**Closes when:** the session site reads the exception's own remedy instead of
naming one, or the two refusals are separated so an unreachable directory and a
damaged record are different causes rather than one.
