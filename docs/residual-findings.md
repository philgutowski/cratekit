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
