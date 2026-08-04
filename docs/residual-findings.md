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

**Closes when:** conformance 3 can be satisfied against a disposable database
fixture, on the `CRATEKIT_TEST_DB` convention that already SUBSTITUTES rather
than skips, so the battery runs either way and a supplied fixture strengthens it.
The natural owner is U27, which lands doctor and is the unit that makes a machine
ready.

---

## R-19. R30's second sentence is computed and never reported

**Found:** during the U32 adversarial review, 2026-08-02. Confirmed against
`src/` before it was recorded.

**Numbered R-19 rather than R-14, and it WILL move again at the merge.** When
this entry was written, `main` defined R-14 and R-15, U27's branch was
renumbering its own to R-16, and U16's fix round was adding R-17. Both of those
predictions were wrong: **U36 took R-16 and R-17 when it merged**, and `main` now
ends at R-17. So the three entries this branch adds renumber sequentially at the
merge, to **R-18, R-19 and R-20**, and all three of these headings move.

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
`bare_metal_session` used to cite **R-19** and **R-20** by number. `main` now ends
at R-17, so this branch's three entries renumber sequentially to R-18, R-19 and
R-20 at the merge, at which point BOTH citations name the wrong finding and the
second one names this checklist. They now cite
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
