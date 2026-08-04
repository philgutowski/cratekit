# Residual findings

Findings that are accepted but not yet fixed. The Definition of Done requires
this file to be current before each merge, so a known problem is a recorded
decision rather than something a future reader has to rediscover.

Each entry says what was found, why it was not fixed here, and what closes it.

---

## R-1. The commit hook is off by default on a fresh clone

**Found:** during U6 verification, 2026-08-01. **CLOSED 2026-08-02, by U27.**

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

**How it is closed.** Doctor's `repo.commit_hook` check resolves the git
directory that owns the checkout, looks for `hooks/pre-commit`, and refuses when
it is absent or does not dispatch to this repository's pre-commit configuration,
naming the command that fixes it.

**That last claim was prose before it was code, and the review said so.** The
test was `"pre-commit" in body`, which a hook whose entire content is the comment
`# pre-commit` satisfies, and so does a hook dispatching to a completely
different repository's configuration. Both reported green while nothing scanned
the commit, which is the state this finding exists to end. Three positive
requirements now: the body invokes pre-commit's own `hook-impl`, it carries
`--hook-type=pre-commit` so it is the stage it claims to be, and the
configuration file it names resolves INSIDE this checkout and exists. Each is
driven against a hook that passes the old substring and runs nothing.

**The third requirement is read with `shlex`, because the line was written with
`shlex`.** `pre_commit` builds that argument vector with `shlex.join`, which
quotes any path carrying a shell-special character, so a regular expression over
non-space characters stops at the space in `my config.yaml` and reports that a
file called `my` does not exist. That is a refusal aimed at a developer whose
hook is installed and working, and it drives the whole health report to exit 30.
The tightening and the false alarm arrived in the same commit, which is the
usual shape: a guard made stronger against its evasion, and weaker against the
real thing it was guarding.

Two more details are worth carrying, because both are ways the same check gets
written wrongly:

- **It follows a worktree pointer.** A worktree's `.git` is a FILE naming a
  per-worktree git directory, and that directory names the COMMON one, which is
  where hooks actually live. A check that looked only for `.git/hooks` would
  report every worktree as unhooked while the hook was installed and running,
  and a guard that fires on correct setups is one people route around (P7).
- **It says nothing at all on an installed package.** The answer is derived from
  whether a `.git` sits beside the source tree, so a user who installed a wheel
  gets an `info` line rather than a red report about a developer tool they do
  not have. Noise is what stops a report being read.

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

**Three of the four are now closed.**

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

*U27's is closed here (2026-08-02), and the first attempt at closing it was
itself an existence check in disguise.* Assertion 8's second half was
`declared <= set(doctor.CHECK_KEYS)`, an existence check over a table that would
have passed with every check function deleted. Replacing it with "run the doctor
and require every declared key to come back with an answer" changed nothing:
`CHECK_KEYS` is derived from `CHECKS`, `run` returns one finding per check, and
every check returns its own key, so the set of keys answered is the set of keys
declared, always, on every machine. The replacement was the same lookup computed
the expensive way, and a stub doctor emitting one empty `Finding` per key passed
both halves while observing nothing.

**What it asserts now is a comparison between two runs.** The same configuration
is driven against two machines that differ only in their seams: one where nothing
is broken, and one where every precondition is. Every key some verb declares must
answer with a real title and a real detail on both, must NOT refuse on the
healthy machine, and MUST refuse, with a remedy, on the broken one. That is this
product's own sentence, "a check that cannot fail is not a check", applied to the
exact set of keys a verb has declared it depends on. A check that always answers
OK fails the second half, one that always refuses fails the first, and an empty
finding fails both. The guard is driven against all three of those stubs in
`test_conformance_8_rejects_a_doctor_that_answers_without_working`, because a
guard exercised only against correct code proves nothing about what it catches.

**What is still honestly not covered:** 9 of the doctor's 23 keys are declared by
some verb, so 14 are outside this assertion entirely. Their behaviour is asserted
in `tests/test_doctor.py` per check, but nothing forces a NEW check to be
reachable or refusable unless a verb declares it.

**Still open:** U11's assertion remains an existence check against the review
store.

**Closes when:** U11 lands. The unit that lands the module owns turning its
assertion from existence into behaviour, in the same commit that removes the
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

**Found:** during U35, porting the backup script. **CLOSED 2026-08-02, by U27.**

The source system's prune passes a Google Drive option so the deleted archive
folders bypass the provider's trash and stop counting against the quota
immediately. Without it, on Drive specifically, a pruned folder keeps occupying
the quota for thirty days, which defeats the point of pruning on a library this
size.

**Not carried across, deliberately.** The remote is configuration now, and that
flag is meaningless on most providers and wrong on some. Baking a
one-provider option into a command built for every provider is the shape this
port exists to remove.

**How it is closed.** Doctor reports rather than the wizard asking, and the
difference is deliberate: the wizard would ask once, at the moment a user is
least likely to have configured a remote at all, while doctor asks the question
again every time the answer could have changed.

The `backup.remote` check reads rclone's OWN configuration through
`rclone config dump`, looks the configured remote up by name, and refuses when
its type is one that trashes on delete and the per-remote no-trash option is not
set. Reading the dump rather than `listremotes` is the part that makes it a real
check: the question is not only whether the remote exists but how it is set up,
and `listremotes` cannot answer that.

**The first version of that table had one row and the check said OK for
everything not in it**, which is the same defect wearing R-7's own clothes: every
provider with a recycle bin that nobody had gotten around to adding, OneDrive,
Box, pCloud and Dropbox among them, reported green over the exact condition this
exists to find. The table is declared in both directions now. A type is either
declared to trash, with the option that disables it AND the value that means
disabled, because Drive's `use_trash` must be false while OneDrive's
`hard_delete` must be true; or declared not to trash at all; or it has no row,
and then the answer is "not asserted" rather than "fine". Two providers are
declared to trash with no per-remote escape at all, which is a note naming the
consequence rather than a refusal the user cannot act on.

**Three states that are not failures**, because a check that fires on correct
installs is one people learn to ignore (P7): the backup module switched off, no
remote configured at all, and rclone absent or its configuration unreadable. The
first two are notes; the third is a note here and a failure under
`binary.rclone`, which is the check that owns it.

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
`db_tree` must declare the cloud-sync gate, so a destructive database verb could
not pass conformance. That was read at the time as a property of the product. It
is not; see below.

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
requires a landed gated verb to exit `OK` once its gate is answered, and it
answers with `-d <gate>=<option>` on the same invocation that hit the gate. Every
verb writing `db_tree` declares the cloud-sync gate, which is `explicit`, and R34
says an explicit gate is answerable only by a separate recorded act and never
inline. **So the assertion asks for a thing R34 forbids**, and it does so on any
machine, with or without a database.

That is a defect in the assertion rather than a wall in the product: the product
behaves exactly as R34 says it must, and the drive is written against a rule that
predates it. Naming it "a wall no destructive database verb can pass" was the
wrong diagnosis, and it matters which one is recorded, because a wall gets worked
around and an assertion gets fixed. U21, U24 and U32 all queue behind it either
way.

A separate branch is correcting `test_conformance_3` on exactly that reading. The
DATABASE half of the wall is real and is unchanged: a destructive database verb
still needs a disposable database to be driven end to end, which is what the
`CRATEKIT_TEST_DB` convention substitutes for.

**U27 met it and did NOT close it, and found the second half above
(2026-08-02).** `doctor.repair-paths` was declared against module
`cratekit.cli.doctor` with `planned_in="U27"`, so landing doctor would have
forced that verb to land too: the countdown that expires a `planned_in` marker
keys on the MODULE, not on the verb. It could not land, and a database fixture
would not have been enough, which is how the assertion defect above was found.

`CLOUD_SYNC_UNREADABLE_GATE` is `explicit` and **every verb writing `db_tree`
carries it**, so this is not one verb's problem. What has to change is the drive:
it must record the decision through `crate run decide` and re-run, which is the
mechanism R34 declares and which nothing exercises end to end today.

**What U27 did instead.** `doctor.repair-paths` now names module
`cratekit.intake.repair_cli` and `planned_in="U37"`, through the
`REPAIR_CLI_MODULE` and `REPAIR_CLI_UNIT` constants, on the reasoning that
`tests/_pending.py` already registers path repair against U37 and
`cratekit.intake`: splitting the verb from the obligation that governs it would
have left two units owning one Feature Inventory row.

**Closes when:** conformance 3 can drive BOTH halves. The database half is the
`CRATEKIT_TEST_DB` convention that already SUBSTITUTES rather than skips, so the
battery runs either way and a supplied fixture strengthens it. The gate half is
the assertion recording the decision through `crate run decide` and re-running
with `--run`, which is the mechanism R34 declares and which nothing exercises
end to end today. The natural owner is now U20, the first unit that must ship a
destructive database verb regardless.

---

## R-16. Three read-modify-write cycles over one document, none of them locked

**Found:** during U27, while hunting the shape the last two waves both shipped.
**Renumbered from R-14 on 2026-08-02**, because `main` already carries an R-14
and an R-15 from a commit this branch predates, and two findings under one
number is a reference that resolves to the wrong thing. Nothing in the repository
parses this document, so nothing caught the collision.

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

## R-17. Three answers that claim slightly more than the check observed

**Found:** during the third review of U27, 2026-08-03. Recorded rather than fixed
by decision of that review: none is a false green, each is a sentence that is
true of the common case and wider than the thing actually measured.

**NUMBERING.** `main` carries R-14 and R-15; this branch adds R-16 and this
entry. A merge that finds another R-17 renumbers whichever arrives second, and
the collision is worth watching for, because nothing in the repository parses
this document and R-16 was already renumbered once for exactly that reason.

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

## R-18. Five places where "I could not look" is still not said out loud

**Found:** during the fourth review of U27, 2026-08-03, while closing the four
that were blocking. Recorded rather than fixed because each needs a decision or a
platform this run could not drive, and none of them reports a false GREEN: they
either err toward a refusal or are loud.

**NUMBERING.** `main` carries R-14 and R-15; this branch adds R-16, R-17 and this
entry. A merge that finds another R-18 renumbers whichever arrives second.

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
which is the loop R-16 measured, reachable from a permission rather than from a
race. **Closes when:** the reader tells a missing index from an unreadable one
and doctor says which it saw.

**5. Two answers from R-17 still claim more than they observed.**
`library.db_containment` infers an atomic rename from pure path containment, and
`keychain.reachable` states an observation when its probe is a heuristic about a
backend class. Both were judged in round three and the judgement stands; they are
repeated here so that a reader of the newest entry sees the whole set.

---

## R-19. A hand-mounted volume at `/mnt/<name>` is now accepted while detached

**Found:** during the fifth review of U27, 2026-08-03, as the deliberate cost of
closing the over-restriction the same review found.

**NUMBERING.** `main` carries R-14 and R-15; this branch adds R-16 through R-20.
A merge that finds another R-19 renumbers whichever arrives second.

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

What losing it costs is what R-18 item 2 already records for every hand-mounted
location: a drive mounted at `/mnt/<name>` is accepted while it is detached, and
the identity read with it detached is its parent's. On Linux that identity is
never recorded automatically, because there is no adapter to read one, so what
remains is a taxonomy copy landing on the root filesystem instead of on the drive.
**Closes when:** the wizard offers to record the mount location it observed, or
the table is read from configuration, which is the same close as R-18 item 2.

---

## R-20. Two rescues that are kept without being covered

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

## R-21. Three edges of the permission classification, stated rather than closed

**Found:** during the sixth review of U27, 2026-08-04, while making "a permission
the user can grant is not a defect in this program" one decision instead of six
handlers.

**NUMBERING.** `main` carries R-14 and R-15; this branch adds R-16 through R-21.
A merge that finds another R-21 renumbers whichever arrives second.

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

## R-22. Four edges of the round eight classification, measured and left open

**Found:** during the eighth review of U27, 2026-08-04, while closing the two
channels a refusal travels: the exception a site raises, and the finding a site
reports.

**NUMBERING.** `main` carries R-14 and R-15; this branch adds R-16 through R-22.
A merge that finds another R-22 renumbers whichever arrives second.

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
