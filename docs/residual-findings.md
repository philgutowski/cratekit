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

## R-14. Five accepted findings from the U38 reviews

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
thirteen of sixteen realistic second-table shapes. R-19 carries the measurement
and the reasoning.

So this residual is general rather than small, and it is written down as such:
`RESIDUAL_ORDINARY_DATA_KEYED_ON_REGISTRY_SLUGS` pins eighteen ordinary
constructs that ARE reported.

**Closes when:** nothing has to close it. It is a stated limit with a fixture, and
the escape for a module that genuinely needs it is one `# not-a-reservation:
<reason>` comment on the statement, which silences that statement and nothing
else. `TABLE_OWNERS` remains the whole-file escape and remains pinned to exactly
two entries.

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

## R-15. Two copies of one import walk still carry a relative-import defect

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

---

## R-16. One check in this unit is unreachable. The other five were reachable and are now driven

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
`test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up`. R-19 has
the shapes.

**Closes when:** nothing has to close it. It is a record of ONE deliberate
retention, plus the correction of a claim that was made about five others, so a
later reader deleting the survivor for being untested knows it was already looked
at and knows what "looked at" was worth the first time.

---

## R-17. Two refusal vocabularies stay outside the second-table guard's key set

**Found:** during U38's third review round, 2026-08-03. Amended in the fifth,
2026-08-03, when the fourth round's two tiers were removed.

The guard reports a second reservation only for a key somebody DECLARED to be a
refusal cause. That set is four declarations wide and one rule wide: the
reservation table, the package-wide derivation, a source's own enums, and the
closed reason registry `core.cause.REASONS`, with a bare integer in the reserved
range reserving any of them. See R-19 for why the registry is carried on the same
rule as the rest.

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
them would widen R-14.4, the residual where a duration in range keyed by a
declared cause reads as a status, from the causes to the remedies, and
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

## R-18. The conversion proof shows that a conversion exists, not that it keeps anything

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
exception carried. That is R-14.2. That handler satisfies this proof and should.

The alternative is a rule about WHICH attributes a handler must read, and that is
a rule an ordinary refactor breaks, which puts it in the same family as reading a
role from a parameter name. So the proof answers the question it can answer, and
the losslessness question is answered by R-14.2 and by the one line that closes
it.

**Closes when:** nothing has to close it. R-14.2 closes the live instance.

---

## R-19. The tiers were bought with a number that does not exist, so there is one key set again

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

### R-19 was also wrong about the rule it documented

The old text said the second tier accepted "an `ExitCode` member in any import
spelling or a conversion wrapped round one". Measured, for all sixty registry
keys, every one of these was NOT reported:

- `{"config-unusable": ExitCode(30)}`, which IS a conversion wrapped round the
  vocabulary.
- `{"config-unusable": exit_codes.ExitCode(30)}`, which is the fixture the fourth
  round itself added to drive R-16's fourth entry, only ever run with a key the
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
carrying the old comments and asserts every hit still fires, and
`test_the_guard_has_no_per_line_off_switch_at_all` asserts the token-stream
helpers stay gone, so any per-line escape coming back fails rather than passing
quietly.

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

### Fourteen shapes were silent, not three, and the largest was not an import spelling

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
`src/cratekit/acquire/adapter.py:137`, so that is the tree's own idiom rather
than an invented one. The fifth round's argument for resolving values, that "a
bare 30 in a mapping tells a reader nothing", is symmetric and was applied to one
side only. One machinery answers both sides now.

Fourteen shapes measured, **six closed in this round and eight recorded**:

| Shape | Now |
| --- | --- |
| a key held in a module constant | CLOSED |
| a key held on a class attribute | CLOSED |
| a list of record dicts, `[{"cause": ..., "code": ...}]` | CLOSED. `_crossed` already read the tuple and the constructor spellings of one record and not the dict one. |
| `getattr(ExitCode, "PRECONDITION")` | CLOSED. `ProcessExits` has recognized `getattr(sys, "exit")` since round two and called it the shape that matters most; this half of the same file did not recognize it. |
| a code reached by `//` | CLOSED. `resolve_int` read `+`, `-` and `*` and not these two. |
| a code reached by `%` | CLOSED. |
| `{"config-unusable": {"code": 30, "remedy": ...}}`, the record dict as the VALUE | recorded. Closing it means reading a status out of a container held as a value, which pairs a cause with any in-range integer anywhere inside a nested structure. That is a wider residual than the one this guard already accepts, and it has no instance in the tree. |
| dataclass field defaults, `cause: str = "config-unusable"` beside `code: int = 30` | recorded. The two defaults are separate statements in a class body with nothing binding them, so pairing them is a proximity rule rather than a structural one. |
| parallel indexed lists, `{SLUGS[0]: CODES[0]}` | recorded. Resolving a subscript into a named sequence is a second evaluator, and `dict(zip(...))` is the spelling anybody actually writes and is already read. |
| a code outside `[10, 60)` | recorded, and it is the range decision rather than a hole. Widening the bare-integer rule past the reserved range reports every count, width and percent in the package. An `ExitCode` member, a conversion, a constant or arithmetic reaching an out of range value is still reported. |
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

is reported at 6 and SILENT at 3. That silence is the price of the number and is
pinned in both directions by
`test_the_hop_bound_is_a_coverage_dial_and_this_is_what_it_gives_up`, so raising
the constant fails a test and demands the new boundary be written down the same
way.

**Closes when:** nothing has to close it. If a real module ever meets the
residual, the answer is a reservation in the table or an entry in `TABLE_OWNERS`
with the membership assertion updated. If one of the recorded shapes above ever
appears in the package, the row that describes it is what says what the walk
needs.

---

## R-20. The mutation table for this unit's guards, written into the repository

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

Every guard, assertion and constant this round added or changed, reverted ALONE,
full suite, deaths counted. Baseline before the round: 3323 passed, 15 skipped.
Baseline after: 3354 passed, 15 skipped. Zero rows would be findings, and there
are none.

| Mutation | What it reverts | Deaths |
| --- | --- | --- |
| `review-walk-suffix-match` | `ReviewImports` reverted to the pre-R-15 two-element suffix match on `node.module`, which cannot see `from .review import` or `from . import review`. This row was ZERO before this round. | 5 |
| `round-four-tiers-restored` | round four's two-tier rule put back: a key outside the twenty two reserved causes needs an `ExitCode` member or a conversion round one, and a bare integer proves nothing | 38 |
| `key-set-drops-the-registry` | `declared_causes()` drops `| frozenset(REASONS)`, taking the closed registry's sixty slugs out of the key set entirely | 21 |
| `key-set-drops-the-derivation` | `declared_causes()` collapsed to `return CAUSES`, dropping the package-wide derivation and the registry both. This row was ZERO before this round. | 21 |
| `key-set-drops-only-the-derivation` | `declared_causes()` drops the package-wide derivation term ALONE and keeps the registry, which isolates the term that is empty in this tree | 1 |
| `package-of-collapsed` | `package_of` collapsed to `return "cratekit"`, so every relative import in the tree resolves against the wrong package. This row was ZERO before this round. | 1 |
| `max-hops-at-two` | `MAX_HOPS` lowered from 3 to 2, one below the depth of the deepest spelling the guard promises to read. Every value from 2 to 5 was a ZERO row before this round. | 1 |
| `no-resolution-through-names` | `_through_names` returns its node unchanged, so an `ExitCode` member held in a constant, or assigned then returned, resolves to nothing | 3 |
| `no-resolution-through-module-constants` | `_through_names` ignores this source's module-level constants and reads only a branch's own locals, which isolates `CODE = ExitCode.PRECONDITION` beside `{"rclone-missing": CODE}` | 2 |
| `no-resolution-through-branch-locals` | `_through_names` ignores a branch's own locals and reads only module constants, which isolates `code = ExitCode.PRECONDITION` then `return code` | 1 |
| `narrowed-to-the-eighteen-live-integers` | the value rule narrowed to the eighteen integers `ExitCode` actually uses, which is the alternative `ReservedCodeTable` rejects, so `{"tree-registry-unusable": 33}` stops being reported | 4 |
| `no-module-qualified-exitcode` | `names_the_class` drops the module-qualified branch, so `exit_codes.ExitCode(30)` stops being a conversion | 2 |
| `no-constructor-conversion` | `status()` drops `names_the_class` from its conversion test, so `ExitCode(30)` reads as somebody's call rather than as a code | 3 |
| `no-class-level-literals` | `_class_level_literals` returns empty, so a module's own `IntEnum` member and a code held on a class resolve to nothing | 4 |
| `no-module-level-literals` | `_module_level_literals` returns empty, so `PRECONDITION = 30` beside a cause resolves to nothing | 12 |
| `no-arithmetic` | `resolve_int` drops its `BinOp` branch, so `BASE + 3` resolves to nothing | 3 |
| `annotation-ignored` | `_silenced_lines` always returns empty, so the `not-a-reservation` comment silences nothing and the residual has no answer | 1 |
| `annotation-needs-no-reason` | the `NOT_A_RESERVATION` pattern stops requiring a reason, so the bare marker silences a construct with no explanation attached | 1 |
| `annotation-covers-a-function` | `_silenced_lines` expands a `def` to its whole body, so one comment silences every reservation inside a function | 1 |
| `annotation-covers-one-line-only` | `_silenced_lines` drops the statement expansion, so an annotation beside `POLL_SECONDS = {` cannot reach the keys on the lines below | 1 |
| `annotation-used-in-the-package` | a `not-a-reservation` comment added to a real package file, which is the guard switched off for a line with nobody reviewing it | 1 |
| `review-leaf-hardcoded` | `ReviewImports` hard codes `leaf = "review"` instead of deriving it from `REVIEW_MODULE`. This row was ZERO before this round. | 1 |
| `exit-code-leaf-hardcoded` | `ExitCodeImports` hard codes `leaf = "exit_codes"` instead of deriving it from `EXIT_CODE_MODULE`. This row was ZERO before this round. | 1 |
| `exit-code-class-spelled-again` | every `EXIT_CODE_CLASS` use replaced by the literal `"ExitCode"`, which is the four spellings of one fact the constant deleted. This row was ZERO before this round. | 1 |
| `shape-swap-column-widths` | `COLUMN_WIDTHS` swapped from a tuple of pairs to a dict literal, same slugs, same values, same line number. This row was ZERO before this round. | 1 |
| `shape-swap-weights` | `WEIGHTS` swapped from a tuple of pairs to a dict literal, same slugs, same values, same line number. This row was ZERO before this round. | 1 |
| `shape-swap-comprehension` | `SLOW_DELAYS` swapped from a dict comprehension to a dict literal, same slugs, same values, same line number. This row was ZERO before this round. | 1 |
| `shape-swap-setdefault` | `DELAYS.setdefault` swapped for a subscript assignment, same slug, same value, same line number. This row was ZERO before this round. | 1 |

Two rows deserve reading together. `key-set-drops-the-derivation` and
`key-set-drops-only-the-derivation` differ by twenty deaths, and the difference is
the registry rather than the derivation: the derived set equals `CAUSES` exactly
in this tree, so the derivation term is EMPTY. The single death on the isolating
row comes from
`test_the_key_set_is_the_union_of_all_three_declarations`, which swaps in a
derivation that finds a cause nobody has declared and asserts it reaches the key
set. That is the only honest way to drive a term the tree leaves empty, and the
fourth round's two assertions in its place were tautologies: `derived <=
declared_causes()` and `CAUSES <= declared_causes()` cannot fail when
`declared_causes()` is a union containing both.

**Closes when:** nothing has to close it. It is the record the next round
compares against, row by row.
