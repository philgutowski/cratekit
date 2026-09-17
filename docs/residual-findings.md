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

**Widened 2026-08-02: the closing condition names one hook type and there are
now two.** `pre-commit install` writes `.git/hooks/pre-commit` and nothing else.
The closing check added on `fix/conformance-3-and-soft-delete-reader` is on the
`commit-msg` stage, which needs `--hook-type commit-msg` on top of it, so a clone
can have a perfectly good `.git/hooks/pre-commit` and no `.git/hooks/commit-msg`
at all. **U27 as specified will not close that gap**, because it checks the file
this entry names. The install line in `.pre-commit-config.yaml` now asks for both
types, and CI runs the closing check independently so the hook is not load
bearing, but the doctor check should look for **every** hook type this
repository configures rather than the one it happened to have when this was
written.

**Closed 2026-09-10 on `relay/38`, both halves.** `repo.commit_hook` in
`src/cratekit/cli/doctor.py` reads the configuration the pre-commit hook
dispatches to and derives every hook type it names: each hook's `stages`,
`default_stages` and `default_install_hook_types`, legacy spellings mapped,
`manual` dropped. Each installed hook is held to the same dispatch requirements
the pre-commit hook already was, and to naming the same configuration. Every
remedy is the exact line, `pre-commit install --hook-type pre-commit --hook-type
commit-msg`, carrying `--config` when the configuration is not the default. A
configuration it cannot read, parse, or understand is a FAIL with a sentence,
never a fall back to the one type the check used to know.

Driven on the primary checkout the same day, it FAILs: `.git/hooks/commit-msg`
is absent there, so the closing check has never run locally. That is the gap
this entry described, measured on the tree rather than on a fixture. Twenty five
mutation rows, every one killing, are in `docs/mutation/r-1.md`. The one
conservative call it made is R-333.

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

**Closed 2026-09-10 on `relay/40`, and closed by refusal rather than by
reading.** The closing condition was already met on the tree: U13 landed on
2026-08-02, the downloader is committed unpacked at
`src/cratekit/_vendor/tidal_dl_ng/` with its provenance in `vendor/README.md`,
and `git ls-files` lists no archive and no binary of any kind. What held it was
nothing. `_read_text` returned `None` for a compressed file and `scan_tree` moved
on, so an archive committed later would have scanned clean over bytes nobody
read. `archive_violations` in `scripts/scan_repo.py` now refuses a tracked
archive by suffix, case folded, and by the header every extractor reads, so a
renamed archive is refused too. An archive aware reader was not built: the
policy is that third-party code ships unpacked, and refusing is the check that
holds that policy. The built in review drove eight formats the first list
missed, and they are covered. That the list is still closed is R-334. Fifteen
mutation rows are committed in `docs/mutation/r-3-rows.toml` and unmeasured,
for R-329's reason.

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

**Closed 2026-09-10 on `relay/41`, both halves.** The closing condition was
already true on the tree: each of the nine toggles gates at least one landed
verb and none of those verbs carries `planned_in`. The only markers left are
U25's two vocals entries, and `vocals` is not one of the nine. What was not
true is "exercised end to end", so
`test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off` in
`tests/test_cli_contract.py` now drives every toggle that gates a landed verb,
thirteen on the tree, through the real resolver and the real parser: off in
slim, on with that toggle alone, off again when subtracted from full. The
parametrisation is derived from the registry, and a second test stops it
shrinking silently.

The still open half was sharper than the entry said. `Entry.extras` is the text
the missing extra stub prints as the install command, and nothing tied it to the
entry's own module, to `EXTRAS_BACKED`, or to pyproject. Driven: an entry giving
`setbuilder` an extras group registered cleanly and printed `pip install
'cratekit[setbuilder]'` for a group pyproject does not declare, with
`tests/test_config.py` still green. `Entry.__post_init__` now refuses an extras
group that is not the verb's own `module_id` and one `EXTRAS_BACKED` does not
carry, and `tests/test_config.py` already holds `EXTRAS_BACKED` equal to
pyproject, so the chain from a verb to the file pip reads is closed. The built
in review found no defect. Six mutation rows are committed in
`docs/mutation/r-4-rows.toml` and unrun, for R-329's reason.

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

**Closed 2026-09-10 on `relay/42`.** The closing condition was already true on
the tree. U11 and U27 are both closed, and neither assertion is an existence
check any more. Conformance 4 offers a review item under every adjudicating
verb's own handler key, resolves it through the real `review resolve` command
line, and reads the verdict back from a fresh open of the store. Conformance 8
runs the doctor twice over one configuration, once on a healthy machine and once
on a broken one, and requires every declared precondition to pass on the first
and refuse with a remedy on the second; a third test drives three stub doctors
against that guard. No `@requires` names `cratekit.core.review` or
`cratekit.cli.doctor`, and `PENDING` in `tests/_pending.py` holds no entry.

What had stopped being true is the paragraph above headed "What is honestly NOT
covered". Measured against the registry on 2026-09-10, twenty two of the twenty
four destructive entries have landed, the two left being U25's vocals verbs,
and every adjudicating entry has landed. The docstrings of conformance 4 and 6
said the same stale thing and are corrected. The gap that paragraph described is
still real, because neither assertion invokes a landed verb through the
dispatcher, and it is R-335. No guard was added or changed, so there is no
mutation table.

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

**Closed 2026-09-11 on `relay/43`.** Measured against the registry, not read off
a record: sixty four entries are declared and sixty two have landed. Conformance
1, 2 and 3 parametrise over `LANDED` in `tests/test_cli_contract.py`, so they
drive sixty two verbs rather than four, and conformance 7 and 8 read all sixty
four. The sample this entry worried about is the whole landed surface now.

The two markers left are `analyze.vocals` and `metadata.mytags-vocals`, both
`planned_in="U25"`. That tail is R-324's, and U25 is an open issue again, so it
is not carried here as well: one fact with two records is how the two come to
disagree. The forcing function this entry names still stands unchanged,
`test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`, and it will
go red the moment U25's modules exist.

The title's four verbs keep the argument surface their jobs need: `profile set`
takes a profile name, `run show` a run, and `run decide` a run, a gate, an
option and an actor. The docstring of `cratekit.cli.verbs` said the package held
exactly those four; it also holds `login`, and it is corrected. No guard was
added or changed, so there is no mutation table.

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

**Closed 2026-09-11 on `relay/44`.** The closing condition was already true on
the tree. U27 landed `backup.remote` in `cratekit.cli.doctor`, which reads
`rclone config dump`, looks the configured remote up by name, and FAILs a
trashing provider whose per remote option is not set, naming the option and the
value. `crate setup` ends by running doctor and exits on its verdict, so the
wizard reports it too. The Drive case this entry was written about is
`test_a_remote_whose_provider_trashes_on_delete_is_reported`.

Read against rclone 1.74.3's own backend help, two rows of that check were
wrong, and both are corrected here. Dropbox's row named a `permanent_delete`
option the Dropbox backend does not have, so every Dropbox remote failed with a
fix nothing could apply. It is an option-less row now, like Box and pCloud.
OneDrive's `hard_delete` is honoured on business drives and document libraries
only, and a personal remote with it set read green. `TrashPolicy.applies_when`
gates the option on `drive_type`, and a remote outside those values, an unset
one included, is a note. Whether `config dump` passes a key rclone does not
know through was not measured, because the scratch configuration run was
refused in this session; the Dropbox test drives that input either way.

What is still open sits in two new entries. R-336 is the quota sentence on the
option-less rows, which nobody measured. R-337 is five providers rclone gives a
delete option that the table has no row for. Six mutation rows are committed in
`docs/mutation/r-7-rows.toml` and unrun, for R-329's reason.

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

**2026-09-16, the attended U29 sitting: the remote is configured and the dry
run ran. The real run was launched and its outcome is recorded below when it
completes.** the Drive remote with `use_trash` set to false, destinations
the mirror folder, the archive folder and the database snapshot root,
the layout the source system's `backup.sh` already used, so the product took
over the existing mirror. The verb's own dry run succeeded in four seconds
because the first configuration named bare folders and rclone read them as
local paths, which is R-345, and because the verb's report reaches nobody,
which is R-349. The mirror command run by hand with `--dry-run` against Drive
took fifty one minutes to list both sides and reported 52 copies of about 1 GiB,
1139 moves into the dated archive (992 analysis files and 141 tracks gone from
the volume since the 2026-08-03 mirror), 0 deletes and 0 errors. rclone accepted
every argument vector, which was the one uncovered surface. The real run is job
`2026-09-16T16:30:43Z-4c99`, resumed as a detached worker.

**2026-09-16, the real run ended succeeded.** `crate job show` on job
`2026-09-16T16:30:43Z-4c99` reports state `succeeded`, attempts 1, two items
done and none failed, queued 16:30:43Z and last updated 17:38:27Z. Because the
verb's report reaches nobody (R-349), the state alone was not taken as the
outcome, and the Drive side was read back. The configured destinations all
carry the `gdrive:` remote, so the R-345 local path trap was not in play. The
dated archive folder `2026-09-16T163043Z` holds 1139 objects, 6.911 GiB,
which is exactly the 1139 moves the hand dry run predicted. The database
snapshot `2026-09-16T173512Z` holds 82 objects, 504 MiB, and its `master.db` is
281153536 bytes with modification time 2026-08-26 09:10:16, the same size and
time as the live database on the library volume. Not measured: a full
`rclone check` of the mirror against the volume, which would repeat the fifty
one minute listing. **Still open:** the restore rehearsal to a scratch
directory, the second of the two gates this entry names, has not run.

**CLOSED 2026-09-16, both gates run, in the second attended U29 sitting.** The
restore rehearsal ran to a scratch directory under `/private/tmp`, database
half only, through `session.restore_cli.restore_under_one_session` with its
`target` seam, because no shipped verb restores anywhere but the live library
root (R-368). It passed the real gates: the backup acknowledgment the author
minted from a Terminal window at 01:11Z, the library lock and the volume
identity. rclone pulled `master.db` from snapshot `2026-09-16T173512Z`,
281153536 bytes, MD5 `954ac500d282bbe607755918407893b4` on both sides, and it
opens through `rb_writer.open_db` with the library key, `pragma
integrity_check` answers `ok` and `djmdContent` holds 17341 rows. The live
database and its directory were not touched, same size and time before and
after, and the recovery session `2026-09-17T01-11-54Z-bf81` closed abandoned
with the lock released, because the plan's second command failed: the restore
copies `master.db-wal` unconditionally and the snapshot holds none, which is
R-367. So both argument vectors run and are accepted where the file exists,
the database restores intact, and the verb as shipped reports the whole
restore failed after doing so. The mirror half was not pulled, hundreds of
gigabytes, and is the one thing this entry leaves unmeasured. Issue #46 can
close back to this entry.

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

**Closed 2026-09-11 on `relay/47`.** The closing condition is met as written.
`rb_writer.add_memberships` takes one playlist and many content ids, reads the
content ids the playlist already holds in one `get_playlist_songs(PlaylistID=...)`
query, inserts each absent id, and returns the ids it inserted. Each insert joins
the presence set, so an id named twice in one call lands once and its second
mention counts as present, which is what the per track read answered while the
first insert was pending. `add_membership` is a one id call into it, so the rule
still lives in one module. `write_tree_membership` makes one call per plan entry.
`test_the_batch_membership_primitive_reads_presence_once_and_inserts_what_is_absent`
counts the reads at the binding and asserts the rows afterwards.

The second half did not close with the batch primitive, since a folder lookup is
not a membership. It closed in the caller instead. Every folder hangs off the one
anchored root, so the display name alone keys a map held for the session, and
entries sharing a folder resolve it once. `ensure_playlist` was already one call
per entry, because plan keys are unique. That half is pinned by
`test_entries_sharing_a_folder_resolve_it_once_and_insert_once_per_playlist`.

What remains per inserted track is the binding's own work inside
`add_to_playlist`: a content lookup by id and a count of the playlist's rows for
the track number. That cost falls on new tracks only, not on a re-run over tracks
already in place, and removing it means bypassing the binding's insert. It was not
measured here and is not filed. Eight mutation rows are committed in
`docs/mutation/r-10-rows.toml` and unrun, for R-329's reason.


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

**Worked 2026-09-11 on `relay/48`. Two findings closed, two stay open here.**

The absorption closed, and the count above was wrong. Three writers absorb a
LEAD break: `insert_root_playlist`, `remove_folder_node` and
`insert_intake_playlist`. `insert_catalog_folder` absorbs the TRAILING break
after a node it replaces in place, which is a different operation over a block
rather than a lead-broken node, so it was left as it is and the helper's
docstring says why. The three now call `rbxml._absorb_lead_break`.
`tests/test_rbxml.py` and `tests/test_xml_splice_golden.py` pass unchanged, and a
helper that absorbs nothing kills two of them.

The watch closed as written.
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session` in
`tests/test_tree_writer.py` plants a real ANLZ file under the library root, names
that root, rewrites the file from inside `rb_writer.add_memberships`, and asserts
the `anlz-modified` refusal naming it. Arming the session with no roots inside
`write_tree_membership` kills it. Before this test nothing did, since every other
membership write in that file names `root/Music`.

`apply_rating_changes` is still kept. Read 2026-09-11, the `trees` wrapper is
still one `dict` coercion and nothing else, so the condition for revisiting it
has not arrived.

The real label is untouched and still open. Its closing condition is the
author's decision about D1's intent, which a session does not make.

Six mutation rows are in `docs/mutation/r-11-rows.toml`. Two were checked red
first by hand on a subset, and the table is unrun for R-329's reason.

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

**Partially driven 2026-08-17, on U24's leftover shell.** `delete.review` now
exits OK after R34's two acts against the disposable fixture. That verb only
READs the collection. Verbs that WRITE the database (restore, adopt.apply, a
routing apply that opens a native tree) still sit behind part 3, because
succeeding on a synthetic schema is not the same proof as succeeding on a
write.

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

**Closed 2026-09-11 on `relay/52`.** Read against the tree, nothing in `src`
joined `AnalysisDataPath` to anything, and U23 reads no analysis of its own
(`adopt/plan.py` says so). What did exist was seven call sites arming the analysis
watch over the library root alone, and a backup that carries the share only when
it happens to sit under that root. Both are right in the external volume layout
and both miss every grid when the database sits outside the root, which is an
acknowledged configuration and the platform default.

`core.analysis_store` now owns the join. `share_root` is the directory beside
the configured database, `analysis_file` joins a stored value to it and refuses
one containing `..`, and `watch_roots` is the library root plus the share when the
share sits outside it. The seven sites take `watch_roots`. The backup plan, its
outcome and the verb's envelope carry `analysis-share-not-carried` when the share
sits outside the root. Carrying it is R-338. Two fixtures that planted their grid
in the export cache now plant it in the share.

Pinned by `tests/test_analysis_store.py`: the join over a volume holding both
trees, where the library root join is shown to find nothing, and an AST guard
refusing a hand listed watch root anywhere in `src`. The watch is driven through
`adopt.apply` with an outside database in `tests/test_adopt_apply_cli.py`, and the
warning through the dispatcher in `tests/test_backup_cli.py`. `analysis_file` has
no caller in `src` yet. Its first caller owns it, and that caller is whichever unit
first needs a row's grid.

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

**Closed 2026-09-11 on `relay/53`.** Measured on this tree first: a sixth
permitted table and a bookkeeping column swapped for a content column, applied
together with a widened content column, gave one failure in the full suite, and
that one was the content column's. The table and the swap killed nothing.
`tests/test_whitelist_membership.py` now pins all three as exact sets. The
content allow list is registry derived here rather than a constant, so it is
pinned at baseline, per metadata operation with its ownership mode, and fully
enabled. The bookkeeping set had a count, which misses a swap. The same shape one
file over is pinned too: `GRIDLESS_ON_CREATE_COLUMNS` and the unwritable metadata
fields are deny lists, where the widening is a removal. Ten widening rows, each
checked red by hand on the pin file, are in `docs/mutation/r-15-rows.toml` and
`docs/mutation/r-15.md`.

The related half landed as the AST audit this entry asked for, and it resolves
aliased imports and refuses a bare reference. One correction to the text above,
read from the pinned binding: `db_dir` also sets the `share` directory analysis
paths resolve under, so a `db_dir` only open mixes live rows with the copy's
share. Checking which file the connection actually opened is R-339.
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
`docs/history/wave-state-2026-08-04.md` names "U32's R-21" four times while it is
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

**Item 2 closed by U48, 2026-09-02.** `_shown_ages` now writes
`remedy=Remedy(str(exc.remedy))`, the way `cli/doctor.py` and the backup shell
already did, so the session is the third consumer of that exception rather than
the one that flattened it. All three tokens are driven through `read_facts` in
`tests/test_write_session.py` rather than through hand built exceptions, because
the finding is that a field is discarded and a hand built exception can carry a
field the code path never produces: a permission error answers
`GRANT_PATH_ACCESS`, a damaged file still answers `REPAIR_BACKUP_FACTS`, and a
newer `schema_version` answers `UPGRADE_CRATEKIT`, which is the case this entry
argues from first. R-201 records the same defect from the permission side and
was written later without noticing this one; it closes on the same commit, and
the two are one finding rather than two. The rest of R-56 is untouched.

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
* **U22, 2026-08-17.** Four slugs appended to the closed reason registry:
  `sync-watermark-unusable`, `sync-source-lookups-failed`, `sync-marks-blocked`,
  `sync-artifacts-unusable`. Cause population 108 to 112, non-reserved half 85
  to 89, reserved half unchanged at 23. Kebab literals 282 to 286, all four new
  literals being those four keys, so the non-key half stays 175. Literal
  holders 45 to 50: the five new modules are the sync package
  (`artifacts.py`, `cli.py`, `marks.py`, `run.py`, `watermarks.py`). The
  also-holds-an-integer half stays 14.
* **U20, 2026-08-17.** Six slugs appended to the closed reason registry:
  `cutover-open-run`, `cutover-xml-pending`, `cutover-export-missing`,
  `cutover-snapshot-missing`, `rebuild-actor-required`,
  `rebuild-tree-not-native`. Cause population 112 to 118, non-reserved half
  89 to 95, reserved half unchanged at 23. Kebab literals 286 to 292, all
  six new literals being those six keys, so the non-key half stays 175.
  Literal holders 50 to 52: the two new modules are `cli/rebuild.py` and
  `write/routing_cli.py`. The also-holds-an-integer half stays 14.
* **U26, 2026-08-17.** Five slugs appended to the closed reason registry:
  `label-intent-unusable`, `label-name-invalid`, `label-unknown`,
  `label-watermark-unusable`, `label-playlist-unreadable`. Cause population
  121 to 126, non-reserved half 98 to 103, reserved half unchanged at 23.
  Kebab literals 299 to 305, five of the six new literals being those keys,
  the sixth being `harvested-label`. Literal holders 63 to 66: the three
  new modules are `label/cli.py`, `label/marks.py` and `label/registry.py`.
  The also-holds-an-integer half stays 15. The without-own half is still 8.
* **U33, 2026-08-17.** Two slugs appended to the closed reason registry:
  `outbound-ledger-unusable`, `export-playlist-unknown`. Cause population
  126 to 128, non-reserved half 103 to 105, reserved half unchanged at 23.
  Kebab literals 305 to 307, both new literals being those two keys, so
  the non-key half stays 180. Literal holders 66 to 69: the three new
  modules are `export/cli.py`, `favorites/cli.py` and
  `modules/outbound/ledger.py`. The also-holds-an-integer half stays 15.
  The without-own half is still 8.

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

**CLOSED 2026-09-11 on `relay/54`, taken from the board as issue #54 and run as
relay task 54.** The first option, the closure. `_admitted_closure` in
`tests/modules/test_reports.py` follows every first party import out of the
allowlist in one worklist pass, reading import statements, `__import__` and
`importlib.import_module`, and returns what it could not follow instead of
dropping it. The audit walks the closure and refuses an unfollowed import.

**Driven on the real tree**: the relocation above, `cause` calling a planted
`access_probe` holding the raw `os.open`, reads `{}` to the one hop walk and turns
the audit red. Planted trees drive the same loop for the delegated down case,
the sideways case two hops deep with a cycle, a delegation out of `review`, both
`import_module` spellings, and a relative import in a three level package.

**The closure is eighteen modules, not eight, and it reaches the write path**:
`rbxml` imports `tree_registry`, which imports `session`, which imports
`rb_writer`. Forty nine writers the audit had never read are now named in
`QUALIFIED_MUTATIONS`, measured to a fixed point in five rounds, most of
`rb_writer`'s only because they call `config.load`. The cheaper alternative was
measured too and is as strict as predicted: `config`, `review`, `taxonomy` and
`rbxml` each import a first party module the allowlist does not name.

**What the closure does not follow**, on purpose: implicit parent package
initializers, since importing `cratekit.cli.output` runs `cratekit/cli/__init__.py`
and following it would pull the whole command line in, and a binding of
`import_module` to a variable. Naming a writer protects the package only if a
report calling it is caught, and one reached through another module's attribute
is not. That is R-340.

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

### DECIDED 2026-08-15, by a fourth option, and this finding is CLOSED

None of the three. The workflow keeps the checks that CAN pass and stops running
the suite at all. `docs/METHOD.md` now carries a section, "What CI is for", and
the rule in it is one sentence: a step in the workflow must be able to pass, and
a check that cannot belongs in the battery.

Concretely: `scan` is unchanged. `test` is renamed `portable` and runs the slim
install assertion and ruff on 3.12 and 3.13, with no pytest. `cold-install`
becomes a matrix over both interpreters rather than 3.12 alone.

**Nothing is deselected.** The second option, marking the macOS proofs so a Linux
job selects against them, was rejected on its own stated hazard: a job that skips
a hardware proof reads as one that ran it, which is the thing those tests exist to
refuse. A job that does not claim to run the suite cannot mislead that way. The
first was rejected because a macOS runner does not make it green either: the
committed calibration refuses a calibration captured on a different machine, and
a hosted runner is a different machine.

**What is lost, said plainly: nothing now proves the suite passes on 3.13.** That
is a real loss rather than an oversight. `cold-install` on both interpreters buys
back the cheap half.

### THIS ENTRY'S OWN ACCOUNT OF THE CAUSE WAS INCOMPLETE, corrected by driving it

It named five causes and every one is platform. It also says, in its first line,
that it was filed "by reading the run list rather than a run". The real failure
set on the last red run is larger, and part of it is not about Linux at all:

- Five in `tests/modules/test_reports.py` are a SHALLOW CHECKOUT.
  `actions/checkout@v4` fetches one commit; those guards derive their file list
  from `git log --grep`, and one commit of history derives almost nothing.
  **Driven on macOS, 2026-08-15**, on a `--depth 1` clone of this repository: the
  same five fail, 344 pass. `git fetch --unshallow` and all 349 pass. Nothing
  about it is the platform, and it would have been a one line workflow fix.
- Two in `tests/test_adoption.py` and two in `tests/test_deletion.py` are about
  one file in two Unicode composition forms, which APFS normalises and ext4 does
  not. Platform, and NOT DRIVEN, because no Linux machine was available.
- Four in `tests/test_pool_sizing.py` are U12's cgroup reader meeting a real
  cgroup filesystem. Platform, and NOT DRIVEN, for the same reason.

The four platform attributions above are read from a log rather than driven, and
they are recorded as read. That distinction is the entire lesson of this
correction and the reason it is written out rather than folded into the decision.

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

## R-129. Folder-level XML import appends children, and rekordbox parses masterPlaylists6.xml on every play

**Found:** 2026-08-15, diagnosing a rekordbox spinning wheel on the source
library. Attended, live, after a scratch-copy rehearsal.

The A2 verdict quoted in `write/trees.py` says XML playlist import replaces
unconditionally. That is the playlist-node half. Importing a FOLDER node that
already exists merges the folder by name and appends every child playlist as a
new row, so each whole-tree re-import doubles the children. Nine label year
playlists reached 3,072 copies each. Separately, macOS spin reports show
rekordbox re-parsing `masterPlaylists6.xml` on the UI thread on every
play-history write, so the duplicated tree (28,249 nodes, 3.2 MB) was a hang on
every track load. Both facts are in
`docs/solutions/integration-issues/folder-level-xml-import-appends-children-and-the-playlist-xml-is-parsed-on-every-play.md`.

**Measured cost.** None to Cratekit today: no Cratekit writer emitted the
payload or ran the import, and the library was repaired outside this repo. The
cost is to the guard model, which reasons about the bridge from one failure
mode when there are two, and to any future writer that adds `djmdPlaylist`
rows without weighing the per-play parse it buys.

**Why not fixed here.** It is a documentation refinement plus two guards
nobody has written; the guards need a unit with tests, not a ledger edit.

**Closes when:** `write/rbxml.py` refuses a payload with duplicate sibling
NODE names, and a snapshot-time reading (duplicate sibling playlists in
`djmdPlaylist`, or a `masterPlaylists6.xml` node count out of proportion to
the library) is a red flag before any write.

## R-130. U22 queues increments and proves the engine; it does not yet drive a real source

**Found:** at the U22 review, 2026-08-17. Accepted rather than held.

`crate sync all` freezes the configuration and queues one job per enabled
source. `cratekit.sync.run.increment` is the engine those jobs will call:
most-recent-N plus owned-dedup, watermark as audit, one `{run_id}_synced.xml`
per run, crash debris excluded from intake. The CLI does not invoke the
engine. Labels land with U26, favorites still have no module, and playlists
have no listing yet. A later worker that uses each job id as the run id
would produce one importable file per source and break R29. That obligation
is not in the pending register.

`sync.favorites` still carries `planned_in="U22"`. The module is absent, so
the countdown stays green, and `cratekit.favorites.cli` is not in
`tests/_pending.py`, so the planned_in versus PENDING check never sees it.
After this unit closes, that verb is owed by nobody.

The intake XML the engine writes is a `TRACK Name` listing, not a Fresh
Export splice. Importing it would be wrong. U37 owns the real emitter.

The unit's live verification, two consecutive real syncs, was not run.

**Measured cost.** None to a library today: the verb only queues. The cost is
to the next worker, which can multiply import files or leave favorites
unowned, and to anyone who treats the stub XML as importable.

**Why not fixed here.** A real source is U26 and the favorites module. A
shared run id across queued jobs is a contract those workers must take, and
inventing the worker here would pretend a listing exists.

**Closes when:** a source worker calls `increment` with one run id per
`sync.all` invocation, `sync.favorites` is remounted onto the unit that
lands `cratekit.favorites.cli`, and the intake file is the U37 emitter.

## R-131. U20 lands the cutover machinery; it does not flip a live tree

**Found:** at the U20 review, 2026-08-17. Accepted rather than held.

The unit's automated half is in the tree: a precheck that refuses an open
run, pending intake XML, a missing Fresh Export, or a missing snapshot;
`flip` and `revert_cutover`; the emitter guard still blocking a flipped
tree while an unflipped sibling accepts a splice; the four `route.*` verbs
closing through `routing_pass.close_run`; a re-run after a destination
rename converging through U36's node map; and `crate rebuild` taking a
typed actor and never naming the clearing call.

The unit's verification, each flipped tree rendering in rekordbox with no
integrity prompt and one full sync landing new tracks without a manual
playlist import, was not run. The live rekordbox database stays off limits
for an unattended session. The execution note is attended, one tree per
session, lived with through at least one normal sync before the next.

Three verbs are a surface without a worker. `route.inbox` answers its
apply gate and writes nothing. `route.unplaced` always reports an empty
plan. `route.resort` and `rebuild` queue a job with no item list, and no
worker in this build calls `rebuild_tree`. `route.pending` does call the
U19 engine when a tree is native and intents are outstanding.

Only `genre_energy` is rebuildable from the shipped taxonomy. `inbox`
stays on the XML bridge (R16). `record_labels` is a catalogue crawl and
cannot flip (R39).

**Measured cost.** None to a library today: no registry record was written
against a live database. The cost is to the operator who still has to run
the attended flip, and to anyone who reads a landed U20 as meaning the
library is already database-native.

**Why not fixed here.** Opening rekordbox, or the live master, is a
standing refusal. Inventing a flip against a disposable copy would not
satisfy the live gate the brief names.

**Closes when:** one live tree has been prechecked, flipped, opened in
rekordbox with no integrity prompt, and has taken one post-cutover sync
that placed new tracks without a manual playlist import.

**The agent half is done as of U53, 2026-09-10, and the entry stays open on
its attended half alone.** The three verbs named above are no longer surfaces
without a worker: `route.inbox` applies on the confirmed branch, `route.unplaced`
reports the rows no governed tree holds rather than a constant, and `rebuild`
and `route.resort` queue one item per governed tree and drive them, both through
`rebuild_governed_tree`, which is the first caller of `rebuild_tree` anywhere in
`src`. Every one of those is driven against a disposable database copy in a
temporary directory. What is unchanged is the sentence this entry exists for:
none of it has run on a live tree, and the closing condition above is still the
whole of what is left.

---

## R-132. U37 lands the emitter and the pipeline; it does not drive a live set

**Found:** at the U37 review, 2026-08-17. Accepted rather than held.

The unit's automated half is in the tree: `build_track_xml` emits no tempo
child and no real average BPM, including the adversarial inizio-and-no-energy
case; a path with a space and a bang synthesizes a Location through
`locations.location_url`; a U22 stub listing is refused as a splice target;
identification-only writes a tracklist and downloads nothing; a file already
on disk ingests without a network call; a missing recognition key refuses
before the identifier is called; path repair offers into
`Queue.PATH_REPAIR` and is idempotent on a name that already fits; routing
intents are recorded at placement; intake never calls `close_session`.

The unit's verification, one real set URL and one real tracklist each
reaching the library through the new pipeline, was not run. The live
rekordbox database stays off limits for an unattended session, and this
build does not bind a live ACRCloud identifier. `intake.set`,
`intake.playlist`, and `tag.folder` queue a job. No worker in this build
calls the pipeline for those verbs. `sync.run` still appends a U22 stub
listing; remounting that writer onto this emitter is R-130, not a second
unit.

**Measured cost.** None to a library today: no live set was ingested and no
registry record was written against a live database. The cost is to the
operator who still has to bind recognition and drive one real URL by hand,
and to anyone who reads a landed U37 as meaning mix intake is already
unattended end to end.

**Why not fixed here.** Opening rekordbox, or the live master, is a
standing refusal. Binding a live recognition key and spending it is an
attended act. Inventing a flip against a disposable copy would not satisfy
the live gate the brief names.

**Closes when:** one real set URL and one real tracklist have each produced
an importable `*_inboxed.xml` through this pipeline, that file has been
imported into rekordbox, and the no-beatgrid suite is still green against
the same builder.

**U57 closed the agent half, 2026-09-09.** The build binds an identifier:
`intake/acrcloud.py` sits behind the seam, reads the two recognition keys through
`core.secrets` at call time, carves and posts through injected seams, knows the
call count from the duration before the first call, refuses to spend past a per
run cap under `intake-recognition-spend-bound`, and folds adjacent answers to one
row per track. `intake.set` identifies at the queue and its worker runs, so the
two intake verbs no longer reconcile forever. What stays open is exactly this
entry's attended half: no live key has been bound and no paid call has been
made, so the response table has met no real answer (R-300) and the closing
condition above, one real set through to an importable file, is untouched.

---

## R-133. U25 lands the two-pass pools; it does not drive a full library

**Found:** at the U25 authoring pass, 2026-08-17. Accepted rather than held.

The unit's automated half is in the tree: both passes plan through
`plan_pool` and run through `map_workers`; a vocal loader that raises
degrades to vocal-inactive and still returns key and energy; chunked
inference matches the unchunked path on a fixture and actually splits the
signal; a Camelot-prefixed name is skipped on resume; a missing analysis
extra names `pip install 'cratekit[analysis]'`; tempo is computed as
`rate` and never written as a grid or a tempo tag. The author's light
table killed 4 of 4 guards, 6016 collected, null control 0.

The unit's verification, a default-configuration full-library run that
completes within memory on an 18GB machine, was not run. The live library
volume is off limits for an unattended session. `analyze.vocals` and
`metadata.mytags-vocals` stay planned: they name `cratekit.vocals.cli` and
`cratekit.write.metadata_cli`, which this unit did not create, because
one module string is one `planned_in` expiry. keyfinder-cli is not
bound. PANNs is not loaded in this environment.

**Measured cost.** None to a library today: no live folder was analysed
and no tag was written against a live file. The cost is to the operator
who still has to install the extras and drive one real folder by hand,
and to anyone who reads a landed U25 as meaning unattended analysis is
already proven on 18GB.

**Why not fixed here.** Opening the live library is a standing refusal.
Installing torch and a 300 megabyte checkpoint, then running the whole
collection, is an attended act. Inventing a memory figure from a fixture
would not satisfy the live gate the brief names.

**Closes when:** a default-configuration run over a real library folder
has completed on an 18GB machine without an out-of-memory kill, and
`analyze.vocals` has either landed beside this package or been reassigned
to a unit that owns `cratekit.vocals.cli`.

**U58 closed the agent half, 2026-09-07.** The path this entry describes as
landed could not produce a score: `vocals.analyse` read a `wav` key nothing
in the package set, so a loaded model scored every track `voxlevel=0,
voxgender="U"`. The vocal pass now decodes the partial's path itself, at the
model's rate, through a bound decoder, and a fake model driven through it
yields a nonzero level and the model's gender call. `analyze.run` and
`analyze.restamp` have workers and a queued job runs pending to done through
the real resume. The attended half is unchanged: no real folder has been
analysed and the 18GB run has not happened. `analyze.vocals` is still
planned, and R-277 records what its absence now costs.

**U25 landed the shells, 2026-09-11.** `analyze.vocals` and
`metadata.mytags-vocals` exist, R-277 is closed, and the 18 GB full-library
run is still the whole of what this entry says. It stays attended.

**CLOSED 2026-09-17, the third attended sitting.** Both conditions hold.
`analyze.vocals` landed with U25, and a default configuration run of it
completed twice over a real library folder of 36 tracks on the 18 GB
machine, 102 and 100 seconds, 1.3 GB peak resident, no out of memory kill,
every score within one point of what DJ_tools stamped. It took two fixes to
get there, R-370 and R-371, both driven and both landed in the sitting.
The full library pass, 343 folders, is R-376 and stays attended.

---

## R-134. The first delete.review drive baselines before the confirm gate

**Found:** at the leftover U24 shell review, 2026-08-17. Accepted rather than held.

`run.plan` writes the first-run watermark inside the same call that
builds the plan. `delete.review` has to plan before it can digest the
confirm gate, so the first `crate delete review` accepts prior removals
as history before anyone can refuse. Abort then reports `no_op`. R35
wants that baseline so a whole library of old removals is not dumped as
new work. The gate's prompt is about trashing files, not about accepting
history, and the review_set schema has no field for `baselined`.

**Measured cost.** No file moves. The cost is a person who aborts the
first run believing nothing was recorded, then never seeing those
removals offered. Driven from the engine's existing first-run tests plus
the CLI call order, not from a new library-with-history-plus-abort
process.

**Why not fixed here.** Undoing the watermark on abort, or moving the
write to after a recorded trash decision, changes R35's first-run rule
and would present the historical set. That is a product decision, not a
shell defect.

**Closes when:** the first-run watermark is either visible on the refuse
envelope, or written only after a recorded decision that names history
as the thing being accepted.

**CLOSED by U60, 2026-09-10, on the first condition, commit `a5a2e33`, and the
schema cost measured was ZERO fields rather than one.** The brief expected a
field on `review_set/1`, which declares `additionalProperties: False`. The refuse
envelope is not that payload. It is the `decision-required` cause, and the gate
already carries a display context onto it: `gates.Gates.require(context=...)`
lands as `cause.detail.shown` on both refusals, and `render.render_gate` prints it
for a person, which is the channel `session.ack` already uses. So `review_removals`
passes `{baselined, accepted_as_history, offered}` and `review_set/1` and its lock
hash are untouched. The context is not read by `_plan_digest`, so the first run's
recorded decision is not stale on the resume that no longer baselines.

**Driven through the shipped verb, measured:** a library with one prior removal,
first run, the refusal shows `baselined: true, accepted_as_history: 1, offered: 0`,
abort, the resume reports `no_op` and moves nothing; a second run's refusal shows
`baselined: false, accepted_as_history: 0, offered: 0`, and confirming it returns
ok with `items: []` and the file still in place. So the removal IS history after
an abort, exactly as before; what changed is that the person was told so before
answering. `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
holds it. The second closing condition, writing the baseline only after a
recorded decision, is a change to R35's first-run rule and stays a product
decision nobody has asked for.

---

## R-135. An empty label listing is treated as a verified empty catalogue

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

The review named an increment that called `Source.list_recent` with no
limit and, on an empty album list, wrote a per-label watermark at
`year=this_year`, so the next increment would skip that label until the
year rolled. That increment is not in the tree. Labels consume U22's
`cratekit.sync.run.increment` (`src/cratekit/sync/run.py:95`). An empty
processed set with no errors returns `shortfall="empty"` and does not
advance the source watermark (`src/cratekit/sync/run.py:132-138`).
`cratekit.label.marks.advance` is never called from the increment path.

The remaining hole is the same class, absence read as evidence of
absence. `LabelSource.list_recent` never raises `run.LookupFailure`
(`src/cratekit/label/sweep.py:173-189`). `crawl.releases` returns
`listing.artist_releases` (`src/cratekit/label/crawl.py:15-17`). That
wrapper returns `[]` when neither listing method exists
(`src/cratekit/acquire/listing.py:235-236`) and `paginate` treats a
missing or empty first page as exhaustion
(`src/cratekit/acquire/listing.py:123-126`). Increment then reports a
verified empty catalogue. A later successful page is not skipped by a
year watermark, because there is no year floor. It is still reported as
empty rather than as a listing that could not be read.

Reachability of a first-page failure that returns `[]` rather than
raising was not re-driven this session. The empty-page and missing-method
producers are in the listing source.

**Measured cost.** A labels increment can report `shortfall="empty"`
when the provider was unreadable. No per-label year skip is in the tree.

**Why not fixed here.** Rewriting the increment to raise on `[]` would
change U22's empty-catalogue contract, and distinguishing a verified
empty label from a failed first page needs a signal the listing wrapper
does not currently return. That is a later unit, not a silent rewrite
of U26.

**Closes when:** a listing that cannot be read raises `LookupFailure` or
an equivalent refusal, and only a crawl that actually exhausted the
provider is reported empty.

**Two of the three producers now refuse, U52, 2026-09-02, and this entry stays
open for the third.** `sweep._crawl_or_refuse` is the one place that asks, and it
sits on the checking path rather than in each caller that reports a result
(`src/cratekit/label/sweep.py:89-128`). An artist object exposing NONE of the
listing methods now raises `run.LookupFailure`, by way of `crawl.can_list`
(`src/cratekit/label/crawl.py:32-52`, asked at `sweep.py:116-121`). Any exception
out of the crawl raises the same (`sweep.py:122-128`), which covers
`listing.fetch_with_retry` re-raising the provider's own error once its retry
ladder is spent and `listing._paged_caller` raising `ListingNotPaginated` for a
method that exists and cannot page. `run.increment` converts `LookupFailure` into
`sync-source-lookups-failed`, so an unreachable provider surfaces as the item's
cause and never as `shortfall="empty"`.

**The third producer stays, and it is deliberately not fixed.**
`listing.paginate` treats a `None` first answer as exhaustion
(`src/cratekit/acquire/listing.py:123-126`). Stated plainly, because it is the
half of this entry that a later reader is most likely to get wrong: AN EMPTY
FIRST PAGE FROM A METHOD THAT EXISTS IS NOT A PRODUCER AT ALL. That is a
genuinely exhausted crawl and it has to keep reporting empty, or every quiet
label becomes an error and R-135 has been traded for its mirror image. What
remains open is the `None` answer alone, which those four lines cannot tell apart
from a page of zero rows.

**Two more instances of the same shape closed with them, and this entry named
neither.** `LabelSource._artist_for` returned nothing for a label the catalogue
could not resolve and `list_recent` skipped it with a bare `continue`, so the
sweep offered nothing and reported that it had looked. `LabelSource._verifier`
had the same silent path for a source built with neither a verification callable
nor a catalogue: every release it listed would be dropped as unconfirmed and the
run would read as a label with nothing new. Both now raise `run.LookupFailure`
(`src/cratekit/label/sweep.py:239-301`).

**The post-merge review of U52 found `_verifier`'s half only half closed, and it
is closed now, 2026-09-02.** The paragraph above describes the scenario
`_verifier` exists to prevent, a sweep that verifies nothing reading as a label
with nothing new, and the guard it shipped covered only the case where no
verification callable OBJECT exists. Two live producers of that same scenario
were left open, and both were driven end to end through the real dispatcher,
queue, handler resolution and driver before being fixed. A catalogue whose
verification endpoint answers and CONFIRMS NOTHING, which is what a degraded or
rate limited endpoint does and what a catalogue crediting a distributor does,
made `list_for_label` drop every release, gave the increment no candidate and no
error, and produced `shortfall="empty"`: exit 0, job SUCCEEDED, no cause, over
forty releases read and discarded. `LabelSource` now accumulates the dropped
population across the labels one listing pass read
(`src/cratekit/label/sweep.py:303`, filled at `sweep.py:447`) and the worker
refuses `label-sweep-incomplete` when the increment reports empty and that
population is not (`src/cratekit/label/cli.py:844`). The refusal is keyed on the
DROPPED population and never on an empty candidate list, so an all tombstoned
label and an exhausted crawl keep succeeding, which is the mirror image this
entry warns about directly above. Separately, `_verifier` returned
`self.catalogue.search_release` bare while `_artist_for` wrapped its seam call,
so a raise from verification escaped `increment`'s `except LookupFailure` and
failed the item as `internal-error` with a remedy of report a defect. It is
wrapped now (`src/cratekit/label/sweep.py:402`), a `CratekitError` passing
through unchanged so an adapter's own `credential-missing` is not flattened into
"this source could not list".

---

## R-136. The increment path drops discarded and suppressed

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

`list_for_label` computes `dropped` (unconfirmed) and `suppressed`
(tombstoned) and returns them on `LabelListing`
(`src/cratekit/label/sweep.py:105-134`). Owned identities are skipped
with no record. `LabelSource.list_recent` extends only
`listing.candidates` (`src/cratekit/label/sweep.py:181-187`).
`run.increment` returns `IncrementResult` with `processed`, `errors`,
and `shortfall` (`src/cratekit/sync/run.py:53-60`). A caller that needs
the discarded or suppressed populations for a report, or for a later
unit, has no way to get them. The brief named both.

**Measured cost.** No acquisition is wrong. The cost is to a report or a
later unit that needs those two populations and has to recrawl to
rebuild them.

**Why not fixed here.** Widening `IncrementResult` is a U22 contract
change. Returning the two tuples only from `list_for_label` is already
true and does not help the increment caller. Filing rather than
rewriting U26.

**Closes when:** the increment result, or a labels-specific report
beside it, carries the discarded and suppressed sets the sweep already
computed.

**Half of it is reachable now and the entry stays open, 2026-09-02, from the
post-merge review of U52.** The sentence above, that a caller has no way to get
the discarded population, is no longer true of the DISCARDED half.
`LabelSource.list_recent` accumulates `listing.dropped` across the labels it
lists and exposes it on the source (`src/cratekit/label/sweep.py:303` and
`sweep.py:447`), because the worker needs it to tell a catalogue that confirmed
nothing from a label with nothing new. It was not bought the way this entry
proposed and that is deliberate: `IncrementResult` is untouched, so the U22
contract change this entry calls out is still unpaid, and a caller reads the
population off the source object it constructed rather than off the result. The
suppressed and owned populations are still dropped on the floor, and a caller
that wants either still has to recrawl.

---

## R-137. LabelSource takes newest-N before owned-dedup

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

`list_for_label` itself drops owned, then takes newest N of what remains
(`src/cratekit/label/sweep.py:125-129`). The increment path does not
call it that way. `LabelSource.list_recent` passes no `owned` and no
`limit`, so the per-label cap is `registry.effective_limit` and owned
releases stay in `candidates` (`src/cratekit/label/sweep.py:181-189`).
It then sorts by recency and slices `found[:n]`. `run.increment` feeds
that already sliced list to `scope.scoped`, which drops owned and takes
the limit of the remainder (`src/cratekit/sync/scope.py:36-41`).

A label whose newest N albums are already owned therefore returns empty
even when older unowned albums exist in the same year. The brief said
drop owned, then take newest N of what remains. The unit's own
acquisition-set test passes `owned` into `list_for_label` directly
(`tests/modules/test_labels.py:338-347`) and never drives
`LabelSource.list_recent` through increment with an owned newest-N.

**Measured cost.** A sweep of a label whose recent catalogue is already
owned reports nothing and skips older unowned releases that the brief
said to take.

**Why not fixed here.** Passing `owned` through `list_recent` is a
source-protocol change (U22's `Source.list_recent` takes only `n`), or
else `LabelSource` has to learn owned itself. Either is a later unit.

**Closes when:** the increment path drops owned first, then takes newest
N of what remains, and a test drives that order through
`LabelSource.list_recent` rather than only through `list_for_label`.

**Not fixed by U52, 2026-09-02, and the reachability that keeps it below the
merge bar is a MEASUREMENT rather than an assumption.** The worker U52 bound is
the first shipped caller this path has ever had, and it passes `owned=set()`
(`src/cratekit/label/cli.py:673`). What was measured, rather than reasoned about:
every declaration in `src` outside the vendored tree that takes a set of owned
identities. There are five, and all five are consumers rather than producers.
They are `sync.scope.scoped` (`src/cratekit/sync/scope.py:24`),
`sync.run.increment` (`src/cratekit/sync/run.py:127`),
`sync.run.run_independent` (`src/cratekit/sync/run.py:218`),
`label.cli.run_increment` (`src/cratekit/label/cli.py:582`) and
`label.sweep.list_for_label` (`src/cratekit/label/sweep.py:138`). The chain the
worker actually drives is four of those five, `handle` to `run_increment` to
`run.increment` to `scope.scoped`, and no frame in it constructs a set;
`LabelSource.list_recent` calls `list_for_label` with no `owned` argument at all
(`src/cratekit/label/sweep.py:303-315`).

Thirty one files in `src` outside the vendored tree contain the word owned, and
the four that could plausibly build such a set were read and rejected by name.
`acquire.match`'s index answers owned VERSIONS of a wanted recording and needs a
match index and a wanted list to be asked at all.
`modules/tools/setbuilder.find_in_index` answers one owned track for a set
builder. `modules/reports/export.read_export_file` reads the hand made collection
export R-227 records the outbound verbs taking. `core/review`'s `owned.csv` is a
legacy filename on the review queue rather than a producer of anything. The label
package imports none of the first three, checked by reading every import line in
`src/cratekit/label/`. So the correct statement is that N candidates were driven
and none of them produces an owned identity set on this path, not that nothing in
the product could ever produce one.

**The LARGER consequence of the same fact, which this entry does not name.** An
empty owned set does not merely put the ordering defect out of reach. It puts
ownership filtering out of the product on this path entirely, because
`scope.scoped` and `list_for_label` both filter only on membership in the set
they are handed (`src/cratekit/sync/scope.py:36-41`,
`src/cratekit/label/sweep.py:176`), and `scope.scoped`'s own docstring says it
does not treat an empty owned set as a special case. So this is not ownership
filtering happening in the wrong order, it is ownership filtering not happening,
and a sweep offers releases the library already holds. Reordering two steps that
both filter on an empty set would change nothing. That is R-259, filed separately
because satisfying this entry's closing condition would not close it.

---

## R-138. The 400 cap is albums, not tracks

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

`registry.DEFAULT_TRACK_LIMIT` is 400 and is named as a track limit
(`src/cratekit/label/registry.py:21,52-56`). `list_for_label` applies
that number as a cap on confirmed release candidates
(`src/cratekit/label/sweep.py:103,128-129`). `LabelSource.list_recent`
then slices the combined album list again (`src/cratekit/label/sweep.py:189`).
No path counts tracks. A 400-album increment can be thousands of
tracks. The brief cap is 400 tracks.

**Measured cost.** A single-label import or a labels increment can queue
far more audio than the named cap. The review-queue and the intake file
then look like a bounded run that was not bounded in tracks.

**Why not fixed here.** Counting tracks means hydrating each album's
track list before the cap, which is a listing-shape change and a
performance change. Filing rather than rewriting U26.

**Closes when:** the cap is applied to tracks, or the field is renamed
and reported as an album cap so the number means what it does.

**Not fixed by U52, 2026-09-02, and its two arms are answered separately because
they no longer stand or fall together.** This branch is the first caller ever to
apply either number as the operative cap: the worker it bound passes
`limit=labels.effective_limit(entry)` into `run_increment`
(`src/cratekit/label/cli.py:598-680`), so the 400 reaches `scope.scoped` on a
path a person can actually drive.

**The counting arm loses its motivation.** `LabelSource.acquires` is False and
`run.increment` returns before the intake append for an offering source
(`src/cratekit/sync/run.py:182-194`), which is R-140's fix. The cap therefore
bounds rows in the label-release review queue and never bytes of audio. This
entry's cost sentence, a run that queues far more audio than the named cap, is
not reachable through this path, because nothing on it downloads anything. What a
person can still be handed is 400 albums' worth of releases to decide on, which
is a review burden rather than an acquisition one, and it is a smaller thing than
the one recorded above.

**The naming arm survives that and is declined for its own reason.**
`LabelEntry.track_limit` is a PERSISTED registry field: it is written into the
favourite label document at `src/cratekit/label/registry.py:75` and read back at
`:115`. Renaming it is therefore a migration over a file already on disk rather
than a rename, and U52 carries no migration. The number still means albums under
a name that says tracks, and the closing condition above is unchanged.

---

## R-139. The harvest CLI always reports the playlist unreadable

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

The review named a `HarvestResult` with no `readable` field and a CLI
that defaulted `getattr(result, "readable", False)`. That type is not
in the tree. The shipped handler is stronger and worse:
`harvest_playlist` raises `label-playlist-unreadable` on every call and
never lists the playlist (`src/cratekit/label/cli.py:224-232`). The
harvest engine (`cratekit.label.harvest.from_tracks`) is reachable only
from tests. The unit test for this path asserts the refusal
(`tests/modules/test_labels.py:450-467`). A successful harvest cannot
be reported, because the verb never harvests.

**Measured cost.** `crate label harvest` always tells the person the
playlist could not be listed. Feature row harvest is a command that
cannot succeed.

**Why not fixed here.** Wiring the CLI to `listing.playlist_tracks` and
`harvest.from_tracks` is the rest of the verb, not a one-line report
fix. Filing rather than rewriting U26.

**Closes when:** a reachable playlist is listed through
`listing.playlist_tracks`, verified names are offered, and only a
playlist that could not be read raises `label-playlist-unreadable`.

**Still open after U52, 2026-09-02, and this is stated so the rebuild is not read
as a closure.** The closing condition above is met in the CODE and is not met for
a person, and both halves are this entry.

**What is met.** `harvest_playlist` resolves a catalogue through the seam before
it touches anything, lists the named playlist through `listing.playlist_tracks`
by way of `harvest.playlist_tracks`, offers the verified names into the
label-release queue and emits a `review_set/1` envelope
(`src/cratekit/label/cli.py:507-575`). `label-playlist-unreadable` is now raised
in exactly one place, `_playlist_tracks_or_refuse`
(`src/cratekit/label/cli.py:449-490`), and only after a bound provider was asked
and failed to answer. An empty playlist is a success reported as `NO_OP` rather
than a refusal, so a playlist with nothing in it stays distinguishable from one
that could not be read. The false sentence is gone: nothing tells a person their
playlist could not be listed over a provider that was never contacted.

**What is NOT met is the thing this entry's cost sentence names.** No shipped
build fills the catalogue seam, so `catalogue.resolve` raises
`credential-missing` or `label-catalogue-unbound` on every real invocation, and
`crate label harvest` still cannot succeed for a person. R-258 records that gap
and it is the whole of it. The success branch is driven only under a seam
substituted in process, which is a test and not a build.

**What actually changed is WHICH refusal a person gets**, from a false statement
about their playlist to a true statement about the build. That is the smaller
half of this entry and it is the honest version of it, but it is not the half the
closing condition is for.

---

## R-140. LabelSource.process treats offer as an acquisition

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed. **CLOSED 2026-09-02, by U52.**

The review named `process()` in `harvest.py` reporting
`acquired=len(accepted)` after `review.offer()`. `harvest.from_tracks`
calls `review.offer` and returns `HarvestReport(offered, dropped)`
(`src/cratekit/label/harvest.py:73-83`). It does not claim an
acquisition. The live hole is the increment source:
`LabelSource.process` calls `offer_release`, which is `review.offer`
(`src/cratekit/label/sweep.py:191-203`, `:137-152`). `review.offer` is
the U11 review-queue seam: it queues an item and returns the item, not
an acquisition (`src/cratekit/core/review.py:1141-1152`).
`run.increment` treats a process call that does not raise as processed,
appends those identities to `{run_id}_synced.xml`, and advances the
source watermark (`src/cratekit/sync/run.py:124-157`). The harvest CLI
never reaches this path (R-139). The labels increment does.

**Measured cost.** A labels increment reports processed identities and
writes an intake file after only offering the releases for review. A
person who imports that file, or who reads the watermark as "these
landed", is told something the tool did not do.

**Why not fixed here.** Making process download, or making increment
wait for a review decision, is a later worker. U26's brief said the
sweep's review output is a review-queue item, not a file, and the
increment engine still writes the file.

**Closes when:** increment records an acquisition only after a review
decision that accepts the release, or the intake file and the watermark
are not written from an offer.

**How it is closed, and it is the SECOND arm of the condition above.** The
condition is disjunctive and U52 took the second arm. The first arm, an
acquisition recorded only after a review decision that accepts the release, is
not what landed and is not owed by this entry.

`cratekit.sync.run.Source` gained an `acquires` attribute
(`src/cratekit/sync/run.py:38-66`). It is declared on the SOURCE rather than
passed to each call, because whether a completed `process` call means the item
landed in the library or means it was offered for a decision somebody has yet to
make is a property of the source and not of the call site. Both shapes complete
without raising, so a process call that did not raise cannot tell them apart.
`increment` reads it as `getattr(source, "acquires", True)`, so a source written
before the attribute existed still means acquisition, which is what every one of
them did.

The branch itself is `src/cratekit/sync/run.py:182-194`, and it RETURNS rather
than guarding the three writes one at a time. That is deliberate: the intake row,
the artifact registration and the watermark advance are three statements of the
same claim, and a fourth writer added later lands below that return where an
offering source can never reach it. Three separate guards is how one of them gets
forgotten.

`cratekit.label.sweep.LabelSource.acquires` is False
(`src/cratekit/label/sweep.py:218`), which is correct for the reason this entry
already gives: its `process` calls `offer_release`, which is `review.offer`, and
that queues an item and hands it back with a verdict of `None`
(`src/cratekit/label/sweep.py:191-203`). So a labels increment now appends no row
to `{run_id}_synced.xml`, registers no artifact and advances no labels watermark.
The intake file and the watermark are not written from an offer, and the
watermark a person reads as "these landed" is no longer moved by one.

---

## R-141. Harvest does not persist harvested labels on the playlist row

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

`harvest.from_tracks` offers verified names and writes nothing back onto
a playlist record (`src/cratekit/label/harvest.py:50-83`). There is no
playlist store call in `src/cratekit/label/`. U27 owns the playlist
store. A later harvest of the same playlist rediscovers the same names.

**Measured cost.** None to a library today: the harvest CLI never
reaches this engine (R-139). The cost is to the first caller that does,
which will re-offer names already harvested from that playlist.

**Why not fixed here.** Persisting on the playlist row is U27's store.
Writing a side file from U26 would be a second store for the same fact.

**Closes when:** a completed harvest is recorded on the playlist row
U27 owns, and a second harvest of the same playlist does not re-offer
the same names.

---

## R-142. Harvest walks only the tracks it is given

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

The review named a `harvest()` that did not inspect `Playlist.tracks`,
so a playlist whose tracks were never hydrated harvested nothing.
There is no playlist-shaped `harvest()` in the tree.
`harvest.from_tracks` iterates the sequence it is handed
(`src/cratekit/label/harvest.py:62-83`). `harvest.playlist_tracks`
delegates to `listing.playlist_tracks` (`src/cratekit/label/harvest.py:45-47`)
and no production caller uses it. The CLI refuses before listing
(R-139). A caller that passes an empty unhydrated `playlist.tracks`
list therefore harvests nothing, and nothing says the playlist was
unread.

**Measured cost.** Latent until R-139 closes. Then an unhydrated
playlist and a playlist with no label credits look the same: zero
offers.

**Why not fixed here.** The hydration path already exists as
`harvest.playlist_tracks`. The CLI does not call it. Wiring that is
R-139, not a second engine.

**Closes when:** the harvest verb lists through `listing.playlist_tracks`
and refuses when that listing cannot be read, rather than iterating a
raw `.tracks` attribute.

---

## R-143. Harvest does not pass through per-row unreadable

**Found:** at the post-merge U26 correctness review, 2026-08-17. Accepted
rather than held. Issue 26 stays closed.

`from_tracks` has two outcomes per name: offer if verified, or
`HarvestDrop` if the verdict is not confirmed
(`src/cratekit/label/harvest.py:69-72`). A track the extractor cannot
read, a track whose copyright field is unreadable, and a track that
simply has no label credit all become "no name" and disappear. There is
no per-row unreadable channel on `HarvestReport`.

**Measured cost.** Latent until R-139 closes. Then a playlist with
unreadable rows reports only the names that parsed, with no count of
rows the tool could not read.

**Why not fixed here.** Adding the channel is a harvest-report change
and needs a producer that can mark a row unreadable. The CLI does not
harvest yet.

**Closes when:** `HarvestReport` carries the unreadable rows, and the
harvest verb reports them separately from unconfirmed names.

---

The following P2s from the same review do not hold against
`src/cratekit/label/` on 8101c90 and are not filed:

* increment date-floor uses `this_year` even when `watermark.year` is
  older. `list_for_label` deletes `last_pulled` and does not read it
  (`src/cratekit/label/sweep.py:93-98`). Marks are audit records
  (`src/cratekit/label/marks.py:1-4`). Driven by
  `test_increment_does_not_use_the_watermark_as_a_date_floor`.
* increment never paginates. `crawl.releases` goes through
  `listing.artist_releases` (`src/cratekit/label/crawl.py:15-17`).
* `_recent_unverified` in `crawl.py` is defined and unused. The symbol
  is not in the file. `crawl.py` only defines `releases`.

---

## R-144. U33 lands the outbound discipline; it does not drive a live account

**Found:** at the U33 authoring pass, 2026-08-17. Accepted rather than held.

The unit's automated half is in the tree: playlist export reports unmatched
tracks and asks its own confirm gate; a re-export of the same playlist key
updates the recorded remote playlist; hearts ignore every remove-shaped
flag and the package defines no remove write; deletion imports none of
the outbound packages; an interrupted export or heart-back resumes on the
recorded remote id without creating a second playlist or a second heart.
The author's suite is 6060 passed, 2 skipped.

The unit's verification, a real export and a real hearts sweep leaving
the remote account in the reported state and nothing else, was not run.
The live provider account stays off limits for an unattended session.
Both verbs queue a job. No worker in this build calls
`cratekit.modules.outbound.export.apply` or
`cratekit.modules.outbound.hearts.heart_back` for those verbs. Forward
acquisition of unowned hearts, and the local colour and tag write the
favorites verb still declares, are not driven here.

**Measured cost.** None to a library today: no live account was written
and no registry record was written against a live database. The cost is
to the operator who still has to bind a provider session and drive one
real playlist and one real hearts sweep by hand, and to anyone who reads
a landed U33 as meaning outbound writes are already unattended end to
end.

**Why not fixed here.** Opening a live streaming account, or the live
master, is a standing refusal. Inventing a remote state from a fixture
would not satisfy the live gate the brief names.

**Closes when:** one real library playlist has been exported and one real
hearts sweep has run through these engines, the remote account matches
the reported added and unmatched sets, and a second run of each updates
rather than duplicates.

## R-145. The report verbs resolve the SHIPPED taxonomy, never the library's ACTIVE copy

**Found by** the U27 review, by two independent reviewers who reached
opposite severities, which is why the number and the disagreement are both
recorded here rather than settled quietly.

`cratekit.cli.reports` resolves `taxonomy.default_taxonomy()` in three of
its four handlers. S6 makes a library self-describing by copying the
chosen template into the library's own state root at setup, and
`cli/doctor._check_taxonomy` reads exactly that copy. Nothing else does.
Ten consumers in this tree resolve the shipped default, so a person who
edits the active copy so their tree is named something else gets a
coverage report that refuses for a tree that is present under another
name, an aging report that refuses for an intake flow that is present,
and library statistics that count against buckets they do not have.

**Measured cost.** None on any machine this product can produce. Exactly
one template ships, `cli/setup` and `cli/doctor` both refuse a configured
name the shipped set does not contain, and the product has no verb that
edits the active copy. The divergence requires hand-editing a file the
software only ever writes once, which is a producer that was named and
NOT driven, so this fails the merge bar's third condition.

**Why not fixed here.** It is systemic rather than U27's. Fixing it in
one unit's four verbs would give this repository two answers to "which
taxonomy is in force", which is the defect P2 names, and the half that
did not move would be the half nobody looks at.

**Closes when:** one function owns resolving the active template with the
shipped one as its fallback, every consumer asks it, and a library whose
active copy declares a differently named tree is driven end to end
through routing, a report, and doctor.

## R-146. A playlist may reference a track the collection does not carry, and nothing checks it

**Found by** the independent cross-model review of U27.

`modules/reports/export.read_export` validates the collection's own
declared entry count and refuses a duplicate collection identifier. It
does not check that a playlist's `TrackID` resolves to a collection
entry. U27's coverage engine now counts only identifiers that resolve, so
its per-folder rows and its placement count always reconcile, but the
underlying document is still accepted with a dangling reference and any
later reader of the same view is free to trust it.

**Measured cost.** None measured. Whether rekordbox can export a playlist
row pointing at a collection entry it did not write is unmeasured, and no
candidate producer was driven. The engine-level arithmetic is pinned
against a view constructed directly, which is why the fix is safe to hold
without the reachability answer.

**Why not fixed here.** The check belongs at the export boundary, which
is U34's module and its suite's business, and refusing a whole export
over one dangling reference is a product decision rather than a repair.

**Closes when:** an export carrying a dangling playlist reference has
been produced by rekordbox or ruled out, and the reader either refuses it
by name or records that it cannot occur.

## R-147. A partitioned pytest run cannot see a dangling `@requires` decorator

**Found by** the independent cross-model review of U27. **Pre-existing**,
and older than this unit: the mechanism is U6's.

`tests/test_pending_units.py` compares the declared register against
`EXPECTED_PENDING`. It never looks for `requires("...")` call sites. The
protection against a deleted register entry whose decorator survives is
that `requires` raises `KeyError` at import, which takes the guard's whole
file out of collection. That protection only fires when the guarded module
is collected, so a run scoped to a subset of `tests/` passes while a
decorator names a key nothing declares.

**Measured cost.** None to this repository today. The discharge in U27
was verified by grep before the deletion and the full battery collects
every module, so no dangling decorator exists. The cost is to a future
session that runs a scoped invocation and reads green.

**Why not fixed here.** The repair is an AST sweep over `tests/`
asserting every literal `requires` key appears in `PENDING`. It is cheap
and it belongs to the countdown mechanism rather than to a report verb;
landing it inside U27 would widen a unit that is already large.

**Closes when:** an AST-derived check asserts every `requires(...)` key in
`tests/` is declared, and is driven against a deliberately dangling one.

**CLOSED 2026-09-17, the fourth attended sitting.** Both engines ran against the
live account, twice each, after R-355 was fixed in the same sitting, because
before that the rows carried no ISRC and matched nothing.

**The export, twice.** `crate export playlist` over a four track library
playlist created ONE remote playlist across a four item job, added the two rows
the account matched, and reported the other two unmatched. The account was read
back independently: the remote playlist holds exactly the two identifiers the
report names. The second run created nothing, added nothing, and reported both
matched rows as already present, and the account still holds one playlist of that
name with two tracks. That is the update rather than duplicate condition, driven.

**The hearts sweep, twice.** `crate sync favorites` swept the 109 row favourites
playlist: 18 hearted, 41 already, 50 unmatched, 0 coloured, no failed item. All
18 are present on the account when every page of the favourites listing is walked
by hand. The second pass hearted NOTHING, reported all 59 matched rows as already
hearted and the same 50 unmatched, which is the add only property driven on the
live account. The local colour and tag write this verb declares is still unbound, and
the forward acquisition of unowned hearts is still not composed, so those two
halves of the entry above stay open as their own residuals rather than under this
number. The hearted and already split is not trustworthy in principle, for the reason
R-383 records: the shipped favourites listing stops early, so a track already
hearted can be reported as newly hearted. Nothing is written wrongly by that,
because a heart is add only and idempotent, and the second pass shows the
listing's ordering keeps it from biting in practice.

**The unmatched rows are R-356, measured.** Of the export's two, both carry an
ISRC the provider answers with several tracks: three releases for one, two for
the other.

---

## R-148. Adoption's memberships are collected and never written, because no unit lands a collection reader

**Found by** U27, 2026-08-23, while landing `cratekit.adopt.apply_cli` and
discharging its countdown entry. It is the RIDER of that entry, named here rather
than deleted with it, because an obligation carried only by a marker on a closing
unit is owned by nobody the moment that unit closes (P5).

R-81 is closed by this unit. `apply_outstanding` opens ONE destructive session
around the whole `apply_plan` loop, with the volume identity asserted, the backup
acknowledgment asserted, the whole-run lock held, and the analysis watch armed on
the library root. All four are driven in `tests/test_adopt_apply_cli.py` against
a real file's bytes rather than argued from the call order.

**What is still absent is the other half of an apply.** The `place` handed down
to the loop COLLECTS each entry's destination and writes nothing, so an adoption
run today rewrites the genre tag and records the applied ledger while no
membership row reaches the database. Two reasons, and only the first is a
decision:

- **Sessions do not nest, and that is enforced.**
  `cratekit.core.session.session_lock` raises `SessionComposition` when one is
  opened inside another in the same process, and
  `cratekit.write.trees.write_tree_membership` owns its own session and refuses a
  caller-supplied gates factory (U8's decision, reinforced by U32). So R-81's
  close condition as written, "opens ONE session around the whole loop, passing
  its own open guard down", cannot be met with `write_tree_membership` as the
  `place`. The composition is driven in
  `test_a_nested_session_is_refused_rather_than_deadlocking` so the argument is a
  measurement rather than a reading of the source.
- **There is no input.** Turning a rekordbox library into
  `cratekit.adopt.scan.CollectionRow` values needs a collection reader, and no
  unit in this build lands one. `adopt.scan` shipped in the same position and says
  so in the same words. So the census is empty, the plan is the empty plan, and
  nothing is outstanding for the missing membership write to have written.

**Measured cost.** None on any machine today, and the reason is the second bullet
rather than the first: with an empty census nothing reaches the loop at all.
`test_the_census_is_empty_because_no_unit_lands_a_collection_reader` drives that
and fails the day a reader lands, which is the point at which this residual stops
being theoretical and the tag write starts landing without its membership.

**Why not fixed here.** The fix is not a line in this module. It is either a
collection reader, which is a unit, or a change to `write_tree_membership`'s
refusal of a shared session, which is U8's and U32's decision and carries the hole
U32 already registered: a caller supplying its own factory can supply one that
names no analysis roots. Neither is U27's to take.

**Closes when:** a collection reader lands and the memberships this loop collects
are written, in a second session opened after this one closes rather than inside
it, with the ordering between the ledger mark and the membership row argued.

**CLOSED by U55, 2026-09-02, and the closing condition was met in the exact shape
it names.** `cratekit.adopt.collection` is the reader.
`cratekit.adopt.apply_cli.handle` writes the memberships through
`write_tree_membership`, in that function's own session, which opens after the
apply loop's has closed rather than inside it, so the composition this entry
describes never arises.

**The ordering was argued and then MEASURED, and the measurement reversed the
first answer.** The obvious order is apply, then write memberships. Driven on
2026-09-02 against a library whose taxonomy tree had not been cut over, the
applied ledger came back holding every entry while the database held no
membership row at all, and the next run then found nothing outstanding, so the
gap was permanent. The recoverable write goes first, which is the order
`apply_plan`'s own comment already argues for the tag write, and the mapping is
derived from `plan.applicable()` rather than from what the run applied, so a kill
between the membership write and the ledger mark costs one re-run that reports
every row as `already_present`. Both directions are driven in
`tests/test_adopt_workers.py`.

**What is left is narrower and has its own number, R-235.** The write refuses on
any library whose tree has not been cut over, which is every library adoption is
for, and no shipped verb can perform a cutover. R-236 records the shape mismatch
this wiring found between `membership_plan` and `write_tree_membership`.

---

## R-149. `delete.review` declares a queueing contract its shell does not implement

**Found by** the queued-resume contract guard added on 2026-08-23, which derives
its population from the registry rather than from a list of verb names and so
caught a verb nobody was looking at.

The entry declares `long_running=True` and names `delete_argv` as its
`argv_builder`. That pair IS the queueing contract: it says this verb produces
work a job driver re-invokes as a subprocess. The shell does not do it.
`review_removals` reads the collection, offers, honours the confirm gate, and
calls `run.apply` inline; it never calls `jobs.enqueue`, and `build_review`
declares no `--job` argument for a resume to use.

**Measured cost: none today, and the reason is the mismatch itself.** No job is
ever created under that handler key, so `delete_argv` is never called by
anything, and the resume defect the guard exists to catch cannot be reached. That
is why it is recorded rather than blocking: the input is not reachable, and
`docs/METHOD.md`'s third condition is not met.

**What was fixed anyway, because it was one lookup.** `delete_argv` now reads
`jobs.GATE_RUN_KEY` and emits `--run` when a gate run is present. If somebody
makes this verb enqueue, the payload is already read correctly rather than the
undriveable-resume defect shipping a second time. Its docstring previously said
"the run id and the recorded gate travel on the invocation" while returning a
list carrying neither, which is now corrected.

**What is NOT fixed.** Either the entry should drop `long_running` and its
`argv_builder`, or the shell should queue. Deciding which is U24's call about
what `delete.review` is meant to be, and it is a design question rather than a
defect: a deletion pass that queues would need its own `--job` surface, a worker,
and a decision about whether trashing files belongs in a detached subprocess at
all. Guessing here would either delete a declared capability or invent one.

**Closes when:** the entry and the shell agree, in whichever direction U24
chooses, and the derived guard in `tests/test_queued_resume_contract.py` keeps
holding whichever verb remains in its population.

**CLOSED by U60, 2026-09-10, in the direction this entry left open: the entry
dropped the queueing contract, commit `a5a2e33`.** `delete.review` no longer
declares `long_running` or an `argv_builder`, `delete_argv` is deleted, and the
verb left `HANDLERS_NOT_YET_BOUND`. The rejected direction was a queued deletion
pass with its own job surface; it was rejected because the gate is explicit and
its digest is the plan, and a detached child would rebuild a plan nobody
digested. The derived guard still holds: `tests/test_queued_resume_contract.py`
now parametrises over one verb fewer, and every remaining case passes. What
stops this recurring is new and derived rather than named:
`tests/test_cli_contract.py::test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues`
parses every landed long-running verb's module for an `enqueue` call, with
`job.resume` exempt by role, and it failed on `main` for `delete.review` alone.
Its one limit is R-328.

---

## R-150. A mirror restore runs inline, holding the lock and the terminal for the whole transfer

**Found:** while landing `cratekit.session.restore_cli` under U27, 2026-08-23.

`restore.run` declares neither `long_running` nor an `argv_builder`, so the verb
performs the whole restore in the invocation that was typed. For the capture
half that is right: it replaces a rekordbox database and its coupled state from
a local directory, which is a file copy measured in seconds. For
`--include-mirror` it is not. That option pulls the music and everything else
the off-machine mirror carried, which the backup module's own documentation puts
at hundreds of gigabytes, and every byte of it moves inside one `subprocess`
call under the held library lock.

**Measured cost.** The terminal is held for the length of the transfer, and so
is the library lock, so nothing else can write while it runs, which is correct
but has no progress surface and no resume. A process killed part way leaves the
restore latch set, which is the designed behaviour and refuses ordinary writes
until a restore completes, so the recovery from an interrupted mirror pull is to
run it again from the beginning.

**Why it is not fixed here.** Queueing it is the obvious answer and it does not
work in this build. Every long-running verb's `--job` path calls
`jobs.reconcile` and performs nothing, uniformly, across ten shells; a queued
restore would therefore be a job nothing ever performs, which is strictly worse
than a slow one. Making the resume perform work is a change to a build-wide
convention rather than to this unit, and R-149 is the neighbouring finding about
the same seam from the other direction.

**Closes when:** either the job resume performs the work it was queued for, at
which point this verb declares `long_running` with an `argv_builder` and freezes
its gate run in the payload the way `adopt.apply` does, or the mirror half grows
its own progress and resume without the queue.

---

## R-151. The restore listing's `review_set` names a queue no queue table declares

**Found:** while landing `cratekit.session.restore_cli` under U27, 2026-08-23.

`restore.list` declares `output_schema="review_set/1"`, whose payload carries a
`queue` string and an `unresolved` count. The listing is not an adjudication
surface: nothing in it awaits a verdict, and `review.Queue` cannot gain a member
for it, because `tests/test_review_queue.py` holds the enum and the surface table
to being the same set in both directions and every declared queue is an
adjudicated one. So the verb emits the literal `"restore"` as its queue and a
constant zero as its unresolved count.

**Measured cost.** A consumer that groups review sets by queue sees a value
`review.adjudicated_queues()` does not list, and would find nothing if it looked
the value up. The count is honest, because reporting the number of recorded
sessions as a backlog would tell a person they have work they do not, which is
the argument `deletion.tombstone_cli` makes for the same field. Nothing consumes
either today: the only readers of the payload are the renderer and the
conformance suite, and both check the shape rather than the values.

**Why it is not fixed here.** The two candidate fixes are both bigger than this
unit. Either `review_set` grows a way to say "this set is a listing rather than a
queue", which is a schema change every emitter would have to be re-read against,
or the entry emits a different surface, which changes a registry declaration U32
made and which nothing has yet complained about.

**Closes when:** the schema distinguishes a listing from a queue, or the entry
names a surface that fits without one.

---

## R-152. The confirmation digest is over the restore's identity, not over its steps

**Found:** while landing `cratekit.session.restore_cli` under U27, 2026-08-23.

**Corrected 2026-08-23** after an independent review measured this entry's own
claim. It said the off-machine half is in the digest, which is true of WHETHER
the mirror is pulled and false of WHICH SNAPSHOT is pulled. That second half is
now R-153 rather than being folded in here, because they close differently.

`restore.run`'s explicit gate declares `digest_source="plan"`, and what the
handler digests is the identity of the restore: the session being restored, its
recorded change summary, the sessions being discarded, and whether the
off-machine mirror is being pulled first. It is not the step list.

**Why the step list is unavailable.** `core.restore.plan` refuses to build one
without an open recovery session, and the session cannot be opened before the
gate: the gate is `explicit`, so the invocation that discovers it exits, and a
library that has never acknowledged a backup refuses the session before the
question is ever asked, which would make the verb unreachable on exactly the
machine a restore is for.

**Measured cost.** A person approves a restore described by what it targets
rather than by the individual file operations it will perform. The property a
digest exists for still holds and is driven: a later session committing between
the offer and the answer moves the recorded change summary, so the digest moves
and the decision is refused as stale. What is genuinely lost is that a change
which alters the STEPS without altering the identity, a companion file appearing
beside the database between the two acts, does not move the digest.

**Why that is survivable rather than a hole.** The step list is derived under the
lock and every step is checked against the disk before the first destructive one
is taken, and `restore._assert_override_names_them` refuses independently when
the discard set does not name what the restore would actually destroy. Nothing
rests on the digest alone.

**Closes when:** either the registry's `digest_source` gains a vocabulary that
can say "the decision's inputs" as distinct from "the artifact", or a plan shape
exists that can be computed without the destructive session.

---

## R-153. The newest off-machine snapshot can move between the two acts, and the digest does not

**Found by** the independent adversarial review of `cratekit.session.restore_cli`,
2026-08-23, driven end to end.

`_offer` digests `snapshot or "newest"`. When a person does not name a stamp, the
literal string `newest` is what enters the digest, so which snapshot will actually
be pulled is not part of what they approved. Measured: offer and answer while the
remote listed `2026-08-01T000000Z`, digest `2773db78d299ff13`; a second snapshot
appeared; the resumed drive kept the same digest and pulled
`2026-08-22T235959Z`.

**The producer was driven and it is an ordinary backup.** `backup.plan_backup`
emits `copy <db> remote:database-snapshots/<stamp>/db/` into a new dated directory
per run, so the set the resolver picks from grows every time anybody takes a
backup, including a scheduled one.

**Measured cost.** A person approves restoring from the snapshot that is current
when they are asked, and a backup landing between the two acts silently changes
which one arrives. Both are this library's own snapshots, so the damage is
bounded: they get a NEWER database than the one they approved, not a foreign one.

**Why it is not fixed here.** Putting the resolved stamp in the digest means
resolving it at offer time, which is a network call to the remote before the gate
is asked, on a path that currently touches nothing. That is a real design change
to when the verb reaches the network, and it makes the offer fail on an
unreachable remote for a restore that may not even use the mirror.

**Closes when:** the offer resolves and shows the stamp it is offering, and the
digest carries it.

---

## R-154. Nothing asserts a pulled snapshot belongs to this library

**Found by** the independent adversarial review, 2026-08-23, driven.

`--snapshot` reaches the remote path by string interpolation with no validation.
Measured: `--snapshot ../another-library-snapshots/2020-01-01T000000Z` produced
`copy remote:database-snapshots/../another-library-snapshots/2020-01-01T000000Z/db/master.db <lib>/db/`,
with no listing call, no validation, and exit 0.

**Measured cost, stated precisely.** This is a person typing a path into their own
configured remote, so it is not a privilege boundary being crossed. What it buys
is restoring a DIFFERENT library's database onto this library's volume while
every gate passes, because the volume identity assertion is about the disk being
written to and says nothing about the provenance of what is written onto it.

**Why it is not fixed here.** The narrow half is cheap, refusing a stamp that is
not the shape `backup.stamp_for` produces, and it does not close the finding: a
well formed stamp from another library's snapshot directory is still accepted,
and nothing in a captured database says which library it came from. Recording a
library identity in the snapshot and checking it on restore is the real fix and it
is a change to the capture side.

**Closes when:** a snapshot carries the recorded volume identity of the library it
was taken from, and the restore refuses one that does not match.

---

## R-155. A restore's session log cannot tell a mirror pull from a capture restore

**Found by** the independent adversarial review, 2026-08-23, measured with a spy
on `core.session.assert_gates` across the dry run, the wet run and the refusal
path.

`core.restore.CAPTURE_RESTORE_WORKFLOW` and `modules.tools.backup.RESTORE_WORKFLOW`
are two labels landing in one log field, and that separation exists so the two
kinds of restore stay distinguishable afterwards. Handing the off-machine half the
already open guard means `backup._restore_gates` returns that guard rather than
opening a session of its own, so `RESTORE_WORKFLOW` never reaches the log on any
path. Only `capture-restore` is ever recorded.

**Measured cost.** Reading the session log afterwards, a run that pulled hundreds
of gigabytes off the network is indistinguishable from one that spent a local
capture. Nothing is lost that another surface holds: the report the verb emits
names both halves, and the reconciliation record is unaffected.

**Why it is not fixed here.** One acquisition and two labels are mutually
exclusive, and this unit chose the acquisition, which is what the register asked
for. A second label would need the session record to carry a list of what happened
under it rather than one workflow string.

**Closes when:** a session record can name more than one kind of work, or the
restore records the mirror pull some other way the log can see.

---

## R-156. Two of the eight backup refusal slugs duplicate slugs already declared

**Found by** the independent adversarial review, 2026-08-23.

`database-absent` duplicates `library-database-missing`, and `library-root-absent`
duplicates `library-directory-missing`. Both pairs carry `LIBRARY_UNAVAILABLE`,
and each pair names one fact with two slugs.

**Measured cost.** A consumer branching on `cause.reason` has to know both
spellings for one condition, and this is exactly the "one symbol meaning two
things" shape inverted: two symbols meaning one thing. No duplicate KEYS exist in
either table, which was checked; the duplication is semantic.

**Why it is not fixed here.** The duplication is not this unit's invention. Both
slugs were already declared in `cratekit.cli.exit_codes`, deliberately, and its
own note for `database-absent` argues for them: "Same code as the root being
absent because the class of answer is the same, and its own slug because the file
portion of a backup can still run". This unit mirrored a decision that was already
made rather than making a new one. Collapsing them means deciding that the backup
module's vocabulary folds into the library's, which is a call about two modules
that this unit does not own.

**Closes when:** the two vocabularies are reconciled deliberately, or the
reservation table's argument for keeping them apart is re-affirmed and this entry
is closed as intended behaviour.

---

## R-157. A person answering the confirmation is never shown the offer it is digested over

**Found by** the independent adversarial review, 2026-08-23. Pre-existing and
platform wide rather than this unit's.

`ctx.gate.require` raises before the handler reaches `ctx.envelope(data=offered)`,
so what a person sees when a gate refuses is the prompt and the gate name. The
offer the digest was taken over, which for a restore is the session, its change
summary and the discard set, is computed and then discarded.

**Measured cost.** The digest does its job, refusing a stale answer, but the
person answering cannot see what they are answering about from the refusal alone.
They can reach it through the run.

**Why it is not fixed here.** All eight `gate.require` call sites in `src` share
the shape, so this is the gate contract rather than one verb, and changing it
changes every gated verb's refusal envelope at once.

**Closes when:** the gate carries its offer into the refusal envelope, for every
verb at once.


---

## R-158. A `path:` countdown key is coupled to a location the register cannot see

**Found:** while landing the operator skills under U28, 2026-08-23.

`tests/_pending._is_absent` resolves a `path:` key against the REPOSITORY ROOT.
The key `path:skills` therefore asked whether `<repo>/skills` exists, which
encoded a guess, made when the countdown was opened, about where a later unit
would put the skills.

U28 put them somewhere else, and had to. R7 says the skills ship with the
package, and `[tool.setuptools.package-data]` can only name paths under the
importable tree, so a repository-root directory would be present in a checkout,
absent from every wheel, and the install verb would have nothing to copy on the
one machine that matters. They live at `src/cratekit/skills/assets/` for the same
reason `cratekit.core.taxonomy` keeps its templates inside the package.

**Measured cost, and it is the opposite of the usual one.** The countdown did not
go red and stay red, which is the failure mode the register's own header warns
about. It stayed GREEN. The unit landed the thing the entry was waiting for, the
entry went on saying U28 owed it, and `tests/test_pending_units.py` would have
agreed, because the path it was watching was still absent and always would be.
Nothing in the repository could see the disagreement. The entry was discharged by
hand in the landing commit, so the register is correct today; what is unfixed is
the mechanism that let it be wrong.

**Why it is not fixed here.** The obvious repair, re-keying to the real path, is
worthless: the register is now empty, so there is no key to re-point, and the
next `path:` key will be opened by whoever needs one, against a location that has
not been decided yet. That is the actual defect and it is in the shape of the key
rather than in any one value. A module key does not have it, because a dotted
module path is the same string wherever the unit puts the file.

**Closes when:** a `path:` key names something the landing unit cannot move, or
the meta test cross-checks the key against the unit's own declared files so a
landed unit with an unfired countdown is a contradiction the repository can see.

---

## R-159. Rule (g) reads only lines whose first token is the entry point

**Found by** the independent adversarial review of U28, 2026-08-23.

`_verb_problems` returns early unless the line starts with `crate`, after
stripping a `$ ` or `% ` prompt marker. A line reading `sudo crate ...`, or one
where the invocation is the right hand side of an assignment, or one inside a
`for` loop body, is not checked at all.

**Measured cost.** None today: no shipped skill writes an invocation in any of
those forms, verified by reading all twelve. The cost is that the rule's coverage
is a property of how the skills happen to be written rather than of the rule.

**Why it is not fixed here.** Every widening is a guess about shell syntax, and
the rule already parses with a real parser rather than pattern matching, so the
tempting fix is to find `crate` anywhere on the line and parse from there. That
fires on prose inside a fenced comment and on a path containing the word, which
is the false positive shape P7 says gets a guard suppressed.

**Closes when:** the rule extracts invocations with a shell parser rather than by
looking at the first token, or the house style forbids the other forms outright.

---

## R-160. The taxonomy rule substring matches and cannot see a comment

**Found by** the independent adversarial review of U28, 2026-08-23.

Rule (h) asks whether a display name appears anywhere in a fenced block or an
inline code span. It is a substring test over the whole span, so a name that is a
prefix of a longer word matches, and it does not distinguish a command from a
comment inside the same fence.

**Measured cost.** A false positive on an inline span that happens to contain a
band name as a prefix, and a false positive on a fenced comment discussing the
taxonomy rather than hardcoding it. Neither occurs in the twelve shipped skills,
checked. The cost is the P7 one: a rule that fires on a correct file is a rule
somebody works around.

**Why it is not fixed here.** Word boundary matching is not obviously right
either, because several display names contain spaces and punctuation, and the
fence splitter that separates command text from comment text already exists and
is used by rule (b). Wiring rule (h) through it is a small change made carelessly
under time pressure at the end of a unit, which is the wrong moment.

**Closes when:** rule (h) reads the command half of a fence rather than the whole
span, and matches on boundaries rather than on substrings.

---

## R-161. A destination that is a symlink or a file refuses as an internal error

**Found by** the independent adversarial review of U28, 2026-08-23.

`crate skills install --into` a path whose per skill destination is an existing
FILE, or a symlink to somewhere else, raises rather than refusing cleanly. The
verb reports it through the internal error path, which tells a person to report a
defect for a condition that is theirs to fix, and the run stops part way with
some skills written and the rest not.

**Measured cost.** A misleading remedy plus a partial install. Reachable only by
pointing the flag at a directory that already holds a file named after a shipped
skill, which is not a state the verb creates.

**Why it is not fixed here.** The clean refusal wants its own reason slug and a
decision about whether a partial install should be rolled back or reported as
partial, and rolling back means deleting directories the verb has just written,
which is the exact operation the blocking finding above was about. Doing that
carelessly is how a fix relocates a hole.

**Closes when:** the verb checks every destination before writing any of them, and
refuses with a typed cause naming the path.

---

## R-162. Package data ships only SKILL.md, so a second file in a skill never ships

**Found by** the independent adversarial review of U28, 2026-08-23, by rebuilding
the wheel and unpacking it.

`[tool.setuptools.package-data]` names `assets/*/SKILL.md`. A skill directory
holding a second file, which `_files` walks and `install_one` copies, exists in a
checkout and is absent from every wheel. The twelve shipped skills hold one file
each today, so nothing is currently lost.

**Measured cost.** None today, measured rather than assumed: the wheel was built
and unpacked and carries all twelve `SKILL.md`. The cost arrives the first time
somebody adds a second file to a skill and it works locally.

**Why it is not fixed here.** Widening the glob to `assets/*/*` ships whatever
anybody drops in that directory, including editor backups and operating system
metadata, and the honest fix is a declared manifest per skill rather than a
wider glob. That is a shape decision for whoever adds the second file.

**Closes when:** a skill needs a second file, and the packaging declares what a
skill may contain rather than matching everything.

---

## R-163. An empty skill directory installs and reports success

**Found by** the independent adversarial review of U28, 2026-08-23.

`shipped_names()` walks directories and `_files` walks the files inside one, so a
directory with no `SKILL.md` is a shipped skill with nothing in it. The install
verb creates the destination, writes a stamp, and reports `ok`.

**Measured cost.** None in a wheel, where package data can only place a directory
that has a `SKILL.md` in it. Reachable in a checkout, and it was reached during
this unit's own development: the authoring agents created their directories
before writing their files, and two tests failed against that state.

**Why it is not fixed here.** The lint already reports `missing SKILL.md` for
exactly this, so the condition is caught before it can ship. What is unfixed is
that the install verb does not also refuse it, which matters only for somebody
running the verb from a checkout mid edit.

**Closes when:** `shipped_names` requires a `SKILL.md`, or the verb reports an
empty skill as a failure rather than as an installed one.

---

## R-164. The sample-argument comment claims a hazard the fixture already prevents

**Found by** the independent adversarial review of U28, 2026-08-23.

`tests/test_cli_contract._sample_arguments` passes `--into` for `skills.install`
with a comment saying a bare drive would write into the real home directory of
whoever runs the suite. The suite's autouse isolation fixture already redirects
`HOME` to a temporary directory, so the drive was never going to reach a real
home.

**Measured cost.** None to any person. The cost is to a reader: the comment
justifies a correct decision with a reason that is false, and the next person to
touch that line will either believe it or have to disprove it.

**Why it is not fixed here.** Passing `--into` explicitly is still right, because
it makes the destination somebody's choice rather than a default, and the fix is
to rewrite the reason rather than the code. It is filed rather than done because
it is prose in a test comment and the merge bar does not hold a unit for one.

**Closes when:** the comment says the true reason, which is that a verb writing
outside the library should be driven at a named destination.

## R-165. The rekordbox Name half of the padding convention has a planner and no caller

**Found by** U39, 2026-08-24, reconciling `name.apply`'s registry claim with
`CUT.md`.

The padded Camelot convention lives on four surfaces. U39 makes the naming
engine write the padded form on two of them, the filename and the title tag,
and `name.apply` repairs existing files to that form. The third surface, the
rekordbox Name field, has `write/metadata.plan_title_padding`: finished,
tested, riding `naming.pad_head`, and called by no verb. The fourth, the
`initialkey` tag, is stamped at acquisition, read at five sites, rewritten by
no padding pass in either system, and every reader normalizes the unpadded
form through the one canonical parser.

**Measured cost.** A library whose rows predate the convention keeps unpadded
Name fields until a person pads them elsewhere, and rekordbox then sorts 1A
after 10A in any Name ordered view. Nothing is lost and no report is false.
The `initialkey` tag costs nothing that any driven consumer can see.

**Why it is not fixed here.** Wiring the planner was offered on 2026-08-24 and
declined: the sweep is a database write over existing rows, the write-time
default removes the need for it on everything Cratekit names from now on, and
the file surfaces are repairable on demand with `name.apply`.

**Closes when:** a verb or the attended U29 cutover drives
`plan_title_padding` against a disposable database copy and a person applies
the result to the live library, or the decision is revisited and the planner
is deleted with its tests.

## R-166. The CUT.md reconciliation has no guard against drifting back apart

**Found by** the independent adversarial review of U39, 2026-08-25.

U39 existed partly to fix a live contradiction: `name.apply`'s registry entry
claimed `dj-pad-camelot` through `source_scripts` while `CUT.md` simultaneously
listed that script as not ported. The fix moved the row out of the cut table
into a paragraph naming where each of the four padded surfaces lives.

`tests/test_cli_contract.py::test_every_source_entry_point_is_either_mapped_or_written_down_as_cut`
is the nearest test, and it asks only that a script be claimed by some entry's
`source_scripts` OR named somewhere in `CUT.md`. That is an inclusive or, so
the reconciled state and the contradictory state both satisfy it equally. The
test cannot tell them apart in either direction.

**Measured cost.** None to any person today, and the two records currently
agree. The cost is that the exact defect class this unit was built to fix is
unguarded against returning, on either side. `CUT1_prose_contradicted` restores
the pre-U39 contradiction word for word and kills 0 of 6254, promoted to a full
suite run before being reported.

**Why it is not fixed here.** It is maintainer facing, so METHOD's severity
floor says it can never block, and the fix is a new test asserting an exclusive
relationship rather than a change to any shipped behaviour. Writing that test
means deciding what the exclusive rule actually is for scripts that are partly
ported, which is a question about the cut ledger's semantics rather than about
this unit.

**Closes when:** a test distinguishes a script that is claimed by a verb from
one written down as cut, rather than accepting either.

## R-167. The Camelot regex's end anchor has zero test coverage

**Found by** the independent adversarial review of U39, 2026-08-25, in the
existing-guard sample rather than in the round's own diff.

`core/naming.py`'s `_CAMELOT_RE` is matched with `.match()`, which anchors only
the start, so the pattern's trailing `$` is the only thing stopping a value
like `1Axyz` from validating as `1A` with the junk ignored. `E3_camelot_anchor_dropped`
removes the anchor and kills 0 of 6254, promoted to a full suite run.

**Measured cost.** None today. The shipped anchor is correct and was driven
directly: `is_camelot("1Axyz")` returns False and `parse_camelot("1Axyz")`
returns None on this tree. The cost is that a regression removing the anchor
would be invisible, and the values that would then validate are keys, which
reach filenames and tag fields.

**Why it is not fixed here.** It pre-dates this unit, this unit does not touch
the expression, and the guard is currently correct. It is recorded because the
sample surfaced it and METHOD says to record what a sample finds.

**Closes when:** a test drives a Camelot code with trailing junk through
`is_camelot` and `parse_camelot` and pins both refusals.

## R-168. name.apply truncates the body to the title tag, and the library keeps the artist in the filename

**Found by** compounding U39's learning, 2026-08-25, when a prior session's
claim about filename bodies was driven instead of repeated.

`write/naming_cli.py:_spec_for` takes the body from the title tag,
`stem = naming.strip_head(title, template=template)`. The library's filenames
carry more than the title. The convention is `KEY - BPM - Artist - Title` or
`KEY - BPM - Title - Artist - Album`, and the title tag holds the title alone,
already head padded by the live system. So a rename replaces the body with the
tag's shorter form and the artist and album text is gone.

**Measured cost, and it is the whole library.** 149 of 150 randomly sampled
files from `Music/` change body under a rename, out of 9867 audio files. Driven
end to end through the real dispatcher against copies of real files in a
temporary directory, with the volume read only and no database opened:

    FROM: 10A - 122 - Sweep - Sébastien Léger, Lost Miracle - Ramses  Sweep_PN.flac
      TO: 10A - 122 - Sweep.flac

    FROM: 5A - 101 - Infiltrator - LTJ Xperience, Anduze - Deepening of A Groove_PN.flac
      TO: 05A - 101 - Infiltrator.flac

This meets all three conditions of the merge bar. It is recorded here rather
than fixed because the fix is a design decision, what the body is for and how a
corrected tag should move a file, and that belongs in a brief. **U41 owns it.**

**It predates U39 and U39 did not cause it.** Before U39 the verb built its
spec from tags alone, rendered no head at all, and renamed the same file to
`Sweep.flac`, which is the same truncation plus the head. U39 repaired the head
and left the body untouched. What U39 changed is that the verb now works well
enough that somebody would run it, and the padding sweep over the existing
library is exactly its intended use, so the cost moved from unreachable to
imminent.

**Why no test holds it, and why none should yet.** Every fixture in
`tests/test_naming_apply_cli.py` gives a file the same body on both surfaces,
so nothing separates the two sources. A test asserting the tag wins was written
on 2026-08-25 to close the mutation row `R8_stem_source_swapped` and was removed
the same day, because it pinned the truncating answer. That row is a zero death
row again and stays one until the design is settled.

**Closed 2026-08-25 by U41.** The head is derived and the body is carried:
each surface renders from its own source, so the filename keeps the filename's
body and the title tag keeps the tag's. Driven over sixty copies of real library
files, truncation to the title tag went from almost every rename to none. The
mutation row that guards it, `R8`, is a killing row again and is killed by tests
asserting the decided rule rather than tests matching current behaviour.

## R-169. A renamed file is opened four times, and the sweep is the slow case

**Found by** the U41 simplification pass, 2026-08-25.

`write/naming_cli._spec_for` reads two tags, and `core/tags.read_tag` calls
`mutagen.File` per call, so building one spec opens and parses the container
twice. `_plan_for` builds a spec for every audio file under the root, and
`name_apply` builds it again for every file the plan proposes to move, so a
renamed file costs four opens and an unchanged one costs two.

**Measured cost.** Not measured in seconds, and the report says so. The shape
is known: the padding sweep over the library is 9867 files, which is roughly
twenty thousand container opens for the plan alone, against an external USB
volume. That is the exact workflow this verb exists for, so the slow path is
the common path rather than an edge.

**Why it is not fixed here.** It predates U41, which changed what `_spec_for`
computes and not how often it is called. The obvious fix is wrong: caching the
spec from the plan pass into the apply pass carries it across the confirm gate,
which is an unbounded human pause during which a tag can be edited or a file
removed. `name_apply` already re-checks `path.is_file()` for that reason, and a
cached spec would reintroduce the plan and apply disagreement U39 closed. A
correct fix reads the container once per file rather than once per tag, which
is a change to `core/tags`, not to this verb.

**Closes when:** a spec is built from one container read per file, with the
plan and apply passes still reading independently.

## R-170. The engine normalizes twice, and the shell adds a third strip

**Found by** the U41 simplification pass, 2026-08-25, and CORRECTED the same day
by the U41 code review, which showed the first version of this entry blamed the
wrong layer.

`_spec_for` calls `naming.strip_head` on both surfaces before building the spec.
`naming.build` then calls `fit_to_budget`, which opens with `normalize_spec`
(`core/naming.py:767`), and then `render_all`, which calls `normalize_spec`
again (`:743`). So a head is stripped three times on the way to a name, and
twice inside the engine alone.

**Measured cost.** For every shape driven, none. A body carrying ONE leading
head renders identically whether the shell pre-strips or not, including the over
budget case that carries a truncation hash. A body carrying TWO stacked heads
loses both either way, because two normalizations already saturate it. So the
shell's strip is redundant and the engine's second strip is the one that
amputates, which is the reverse of what the first version of this entry said.

**Why it is not fixed here.** Removing the shell's strip is the tidy change and
it fixes nothing, because the double normalize inside `build` survives it. The
real question is which of the two engine calls should go, and `render_all`'s is
the one the crash window relies on for idempotency, so the answer is probably
`fit_to_budget`'s. That is a change to the engine every naming caller shares,
it wants its own mutation coverage, and the library volume was disconnected
before it could be driven against the tree. `docs/METHOD.md` names a fix
justified on fixtures rather than on the tree as its most dangerous defect
pattern.

**Closes when:** `build` normalizes exactly once, the stacked head case is
pinned by a test, and the result is driven over real library files.

## R-171. An empty title BODY makes the tag inherit the filename body

**Found by** the U41 code review, 2026-08-25, driven through the real
dispatcher.

`core/naming.py:745` reads `body_tag = spec.title if spec.title else spec.stem`.
That is a truthiness test, so a title tag that is PRESENT but whose body strips
to empty, a head with nothing after it, takes the same branch as a title that
was never supplied, and the tag is rendered from the FILENAME body instead. A
file named `1A - 124 - Artist Name - Song Title.flac` whose title tag reads
`1A - 124 -` has its tag rewritten to `01A - 124 - Artist Name - Song Title`.

**Measured cost.** Small, and smaller than what it replaced. The fallback was
inert while `stem` and `title` were the same string, and U41 made the two
surfaces differ, so this is the one door by which a filename body can reach the
tag. Driven on the same input, `origin/main` produced the filename
`01A - 124 - .flac`, which is a name with no body at all, so U41 is strictly
better here and the tag gains text rather than losing it. The population of
head-only title tags in the real library is UNMEASURED: 499 of 500 sampled tags
carried a head and a body, and the volume was disconnected before the degenerate
case could be counted.

**Why it is not fixed here.** The fix is one character of intent,
`if spec.title is not None`, in the engine that every naming caller shares, and
it changes what a blank tag renders to. That is a decision about what an empty
title MEANS rather than a repair, and it belongs with R-170's normalize question
in a unit that owns the engine.

**Closes when:** the engine distinguishes an absent title surface from a present
but empty one, or a decision is recorded that it should not.

## R-172. A rename the plan promised can be skipped while the run reports ok

**Found by** the U41 code review, 2026-08-25, driven end to end.

Two files whose rendered names collide leave the plan promising two renames and
the apply pass performing one. `write/naming_cli.py` calls `naming.claim_target`
and `continue`s when the claim fails, and the envelope still returns `ok`.
Driven: two files that dedupe onto `05A - 120 - Song - Artist.flac` produce a
two item plan, one rename, one file untouched, exit 0 and outcome ok.

**Measured cost.** An operator sweeping the library is told a rename happened
when it did not, with nothing in the report naming which file stayed put. That
is the "shown a clean report over state the tool could not act on" shape the
merge bar names.

**Why it is not fixed here, and why U41 improves it.** It predates U41 and this
unit makes it LESS likely rather than more. While the body came from the title
tag, any two files sharing a key, a tempo and a title rendered to one name;
carrying the artist and the album into the name separates most of those. The
collision path itself, and the silent `continue`, are untouched by this diff.
The fix belongs in the plan pass, which should detect two paths rendering to one
target before the gate rather than discovering it during the rename.

**Closes when:** a collision is detected while the plan is built, or the apply
pass reports a skipped rename as something other than ok.

## R-173. Closed on discovery: the central guard passed on an empty plan

**Found by** the U41 independent adversarial pass, 2026-08-25. **Fixed the same
day rather than filed**, and recorded here because the shape is worth keeping.

`test_a_rename_never_replaces_the_body_with_the_title_tag` was the test the
brief asked for by name and the one mutation row `R8` is killed by. Its entire
body was a loop over the planned moves with no assertion outside it, so an
implementation whose plan pass proposed nothing satisfied it. Driven by the
reviewer with a plugin replacing `_plan_for` with an empty plan: the test
passed. Its own sibling asserts `len(moves) == 1` and it did not.

**Why it is recorded although it is fixed.** Four reviewers read this test
before the independent pass and none saw it, including two that examined its
assertions closely enough to argue about whether the first one was redundant.
A guard that runs zero times reports the same green as a guard that holds. The
fix is one line, `assert len(moves) == 3`, and it was verified by re-running the
reviewer's own empty plan plugin and requiring a failure.

**Closes when:** closed 2026-08-25, in the same round it was found.

## R-174. Nothing pins the collision guard, and removing it destroys audio

**Found by** the U41 independent adversarial pass, 2026-08-25.

`naming.claim_target` is what stops two files renaming onto one name. Removing
it kills 0 of 6266. The reviewer drove the mutated tree: two 8430 byte files
became one 8430 byte file and both originals were gone. Composites on the same
loop kill 7 and 4, so the loop is held and this specific guard is not.

**Measured cost.** None today, because the guard is present and correct. The
cost is that its removal is invisible to the suite, on the one code path in this
verb that can destroy a track rather than merely misname it.

**Why it is not fixed here.** It predates U41 and this diff neither adds nor
widens it. A test needs two files that render to one name, which is the same
fixture R-172 needs, and both belong in a unit that owns the collision path.

**Closes when:** a test drives two files onto one target and fails when
`claim_target` is removed.

## R-175. A head only name is now a fixed point

**Found by** the U41 independent adversarial pass, 2026-08-25, driven on both
halves.

The pre U41 verb could produce a filename that is a head and nothing else,
`01A - 124 - .flac`, when the title tag's body was empty. The reviewer restored
that code in memory and confirmed it produces exactly that. Handed such a file,
the reviewed verb proposes nothing, because the body now comes from the filename
and the filename has no body. The tag may still hold the title, and the verb no
longer reads it for the body, so the file cannot be healed by this pass.

**Measured cost.** A file already damaged by the old behaviour stays damaged.
Whether any such file exists is UNMEASURED: the population would have to be
counted on the library volume and it was disconnected before this was found.
The verb never creates this state, so the population is bounded by whatever the
pre U41 code did before anybody ran it, which on this machine is likely zero.

**Why it is not fixed here.** Healing it means reading the body from the tag
when the filename has none, which is a narrow exception to the decision this
unit just took, and it should be taken deliberately rather than bolted on. It
also cannot be justified until the population is known.

**Closes when:** the population is counted with the volume mounted, and either a
recovery path is added or the count is recorded as zero.

## R-176. Two more shell layers are fully masked by the engine, and R-170 is narrower than filed

**Found by** the U41 independent adversarial pass, 2026-08-25.

Rows `A3`, `A4` and `A7` each kill 0 of 6266 and each is byte identical to the
shipped tree on every input driven. They are the two `strip_head` calls in
`_spec_for` and the `or path.stem` title fallback. This is R-170's class
reproduced twice more: the shell does work the engine repeats.

**It also corrects R-170.** That entry says the shell's strip is redundant. The
reviewer drove stacked heads and found the claim holds at one and two and FAILS
AT THREE, where the shell's strip and the engine's two normalizations do not
reach the same fixed point. R-170 stands as a redundancy finding and its
"identical on every shape" wording is too strong.

**Measured cost.** None driven. Three stacked heads is not a shape any producer
in this repository creates.

**Why it is not fixed here.** Same reason as R-170: the fix belongs in the
engine, wants its own mutation coverage, and the volume is disconnected.

**Closes when:** the engine normalizes once, and the shell stops repeating it.

## R-177. dedupe_stem's two structural guards mask each other

**Found by** the U41 independent adversarial pass, 2026-08-25.

`dedupe_stem`'s structural rule has two conditions. Rows `D2` and `D5` remove
one each, both kill 0, and neither alone changes any output. Applied TOGETHER
the reviewer drove `"Song - Song"` collapsing to `"Song"`.

**Measured cost.** None today. The pair is what METHOD's "remove each guard
layer alone" rule is written for, and it is the case that rule cannot catch:
each layer is covered by the other, so single layer mutation reports both as
untested and the composite reports them as held.

**Why it is not fixed here.** `dedupe_stem` is engine code this unit does not
touch. It became reachable here, which is why the reviewer scoped it in.

**Closes when:** a test drives the two condition case, or the rule is written so
one condition carries it.

## R-178. Four more write path guards kill zero, each with a driven difference

**Found by** the U41 independent adversarial pass, 2026-08-25.

Rows `C5`, `E2`, `E6` and `D4` each kill 0 of 6266, and the reviewer drove each
to a real behavioural difference rather than accepting the zero: a failed rename
leaves a zero byte phantom track, two stems that dedupe alike hash alike, a
truncation cut lands on a trailing space before the tilde, and a stem that both
starts and ends with the separator loses its tail.

**Measured cost.** None today; every one is a correct guard with nothing
watching it. The phantom track is the one worth a person's attention, because it
leaves a file on disk that no plan will ever mention again.

**Why it is not fixed here.** All four are pre existing engine and write path
guards, untouched by this diff.

**Closes when:** each has a test, or the ledger records a decision not to.

## R-179. A mutation table is a measurement of one commit

**Found by** the U41 independent adversarial pass, 2026-08-25.

`docs/mutation/u41-author-full.md` was measured at `fe47197` and states a
baseline of 6262 collected. The unit's tip is `79b172f` and collects 6266,
because a later round added four tests and changed an assertion in a test the
table credits with a kill. At the tip, `R8` kills 8 rather than the 5 the table
records.

**Measured cost.** A reader takes the table's numbers as describing the unit and
they describe its first commit. The solutions doc inherited the same five and
has been corrected to eight with the reason.

**Why it is not fixed here.** Re-measuring the author's table at the tip would
overwrite a real measurement with a later one and lose the record of what was
true when it was taken. The independent table at the tip is committed alongside
it and is the current number.

**Closes when:** a mutation table names the commit it was measured at in its own
header, so the two cannot be confused.

## R-180. The measurements that decided this unit cannot be re-derived

**Found by** the U41 independent adversarial pass, 2026-08-25.

The 53 and 25 and 1 percent grammar split, the 149 of 150 sample, and the sixty
file end to end drive are the evidence the whole design rests on, and they ship
as prose in a docstring, a commit message and a ledger entry. No script and no
raw output is committed, and the volume is disconnected, so none of it can be
re-derived or checked this session.

**Measured cost.** Nobody can audit the numbers that decided what the body is
for. They were real when taken and there is no artifact proving it.

**Why it is not fixed here.** The scripts name the library volume by absolute
path, which `scripts/scan_repo.py` refuses in a shipped artifact, so committing
them as written would redden the battery. This entry proved that on its own
first draft, which named the volume in this very paragraph and failed the scan.
Committing them properly means taking the library root from configuration, which
is a small piece of work rather than a copy.

**Closes when:** a committed script takes the library root from config and can
reproduce the grammar survey, and its output is committed beside the numbers.

## R-181. A genre lookup is resolved once per row rather than once per name

**Found by** U40's own review of the seam it became the first caller of,
2026-08-26.

`write/metadata.plan_genre_retag` calls `resolve_genre_id` inside its loop, so a
sweep over N rows issues N `get_genre` queries even when every row wants one of
five genres. `tagging/retag.plan_library` is the first caller and inherits it.
The three sibling planners in that module do not have the shape, because neither
`plan_title_padding` nor `plan_rating_backfill` performs a lookup at all.

**Measured cost.** None observed. It is a query count on a local SQLite file, so
the cost is proportional to the sweep rather than to the library, and a person
retagging a folder is retagging tens to hundreds of files. Nothing incorrect
happens.

**Why it is not fixed here.** The fix belongs in `plan_genre_retag`, which is a
shipped function this unit calls rather than one it wrote, and memoizing it
changes nothing a person can see. Under the merge bar this is a residual by the
severity floor rather than by reachability: it IS reachable and it IS this
unit's, and there is no user facing cost to name.

**Closes when:** `plan_genre_retag` resolves each distinct genre name once, or
somebody measures a sweep large enough for the difference to be visible.

## R-182. A review item is addressed by the file's absolute path

**Found by** U40 while designing the identity, 2026-08-26, and recorded rather
than solved because there is nothing better available at that layer.

`tagging/retag.identity_for` returns `{"path": str(path)}`, and
`review.item_id_for` hashes that into the item identifier. Move the library, or
rename a folder above the file, and every open item about it is orphaned: the
next run offers a fresh question and the person's earlier answer stays in the
queue attached to a path that no longer exists.

**Measured cost.** A person who adjudicated a batch and then reorganised their
folders is asked the same questions again, and the old items linger unresolved.
Nothing is written wrongly and nothing is lost.

**Why it is not fixed here.** A bare audio file carries no identifier this pass
could use instead, and the pass deliberately runs before any library row is
matched so that a folder with no rows at all can still be corrected. Keying on a
content id would make the verb useless on exactly the arrivals it exists for.
The deletion and path-repair queues address items the same way, so this is the
queue's shape rather than this verb's.

**Closes when:** the review queue can re-address an item whose path moved, which
is one mechanism serving at least three producers.

## R-183. Nothing in `src` executes a queued job's work, and this unit adds another

**Found by** U40 while wiring the long-running shape, 2026-08-26.

`crate tag retag` queues a job exactly as `tag.folder`, `route.resort`,
`export.playlist` and every other long-running verb does. `jobs.spawn`
re-invokes the CLI with the resume argv, the handler sees `--job` and calls
`jobs.reconcile`, and the job is reported. No code path in `src` claims a job
item and runs the engine behind it: `git grep -n "next_claim\|claims(" src`
outside `core/jobs.py` returns nothing, and `jobs.claim` at
`src/cratekit/core/jobs.py:769` has no caller in the package. So
`tagging.retag.retag_folder` has no caller in `src`, exactly as
`tagging.tag.tag_folder` has none.

**Measured cost.** A person who confirms a retag gets a job identifier and a
queued state, and the work does not happen. The same is true of every other
queued verb today, so this is the product's state rather than a regression this
unit introduces.

**Why it is not fixed here.** Building the worker is a unit of its own and it is
one worker for the whole queued family, not one per verb. Building it inside
this unit would either bind it to one handler key, which is the wrong shape, or
expand this unit into the job execution layer, which no brief assigns to it.

**Closes when:** a worker claims job items and dispatches by handler key, and
every long-running verb's engine has a caller in `src`.

**Measured on U46, 2026-09-01, and this entry stays OPEN.** The first clause is
met: `cratekit.cli.handlers.run_job` claims a job's items through `jobs.drive` and
dispatches by handler key. The second is not, and one binding cannot meet it. One
of twenty landed queued verbs has an engine with a caller in `src`; the other
eighteen are `R-203` and `job.resume` is exempt by role. Recorded here rather than
by rewriting the closing condition, because the condition is right and it is the
progress that is partial.

**Re-measured on U56, 2026-09-03. The half this entry names about `tag.retag` is
now MET and the entry still stays open.** This finding was raised over that verb
in particular, and its own sentence, that a person who confirms a retag gets a
job identifier and a queued state and the work does not happen, is false as of
this unit: `tag.retag` and `tag.folder` both have workers in `cratekit.cli.handlers.HANDLERS`
and both run their items from `pending` to `done`. Seven of the twenty landed
queued verbs are bound now. The closing condition asks for EVERY long-running
verb's engine to have a caller, eleven still do not, and those eleven are
`R-203`.

## R-184. `plan_genre_retag` drops a row whose wanted genre is empty with no skip

**Found by** U40's first-caller drive of `write/metadata`, 2026-08-26.

`plan_genre_retag` reads `wanted = genres.get(content_id)` and `continue`s on a
falsy value with no `Skipped` entry. A row absent from the mapping and a row
present with an empty string are therefore indistinguishable in the plan, and
both read as "this row was not part of the operation".

**Measured cost.** None today, and the reason is what makes this a residual
rather than a finding: `retag.plan_library` is the only caller and it builds the
mapping from `outcome.written`, whose `written` field is non-empty by
construction wherever it is set. The empty-string input is not reachable from
any producer this unit ships, which is condition 3 of the merge bar failing
rather than the severity floor.

**Why it is not fixed here.** Distinguishing the two would mean deciding whether
an empty wanted value is a caller defect worth raising on, and that decision
belongs with a caller that can actually produce one.

**Closes when:** a second caller can produce an empty wanted value, or
`plan_genre_retag` refuses one at the boundary.

## R-185. The file write and the database plan are two acts with nothing spanning them

**Found by** U40 while splitting the pass from the plan, 2026-08-26.

`retag_folder` writes each corrected genre onto the file as it goes.
`plan_library` and `apply_library` run afterwards over what was written, and the
commit is the caller's. A run interrupted between the two leaves files corrected
on disk and rows still pointing at the old genre.

**Measured cost.** The library disagrees with the files until the next run. That
next run does converge: the files now carry specific genres, so the selection
skips them and the database half is not re-planned either, which means the rows
stay wrong until somebody re-runs a routing pass over them.

**Why it is not fixed here.** Making the two atomic means holding a database
write session open across a network lookup per file, which is the opposite of
what the guarded writer's session rules are built for, and it would hold the
lock for the whole length of a long sweep. The ordering is deliberate: the file
is the durable record a person can see, and the row is derived from it.

**Closes when:** the pass records what it wrote to a resumable ledger the
database half reads, so an interrupted run can finish the second act without
re-running the first.

**Driven on U56, 2026-09-03, and this entry stays OPEN.** The unit that gave this
verb a worker is what made the shape reachable, so it was measured rather than
argued. A three file retag was interrupted after one file was corrected: the file
on disk carries the new genre, nothing planned or wrote a library row, and a
second full run over the same folder selects nothing, because the corrected file
is no longer too coarse. The row stays wrong until a routing pass moves it, which
is exactly what this entry predicted.

**What that measurement also found is the answer to the closing condition's own
question.** The condition asks for a resumable ledger the database half can read,
and one already exists: `jobs.drive` commits a per item artifact before it flips
the row to done, and this worker's artifact carries the path, the PREVIOUS genre
and the written one. That is the population, durable by construction and written
in the order the corrections happened. The deferred half does not need a new
register; it needs a caller that reads those. Recorded here rather than by
rewriting the condition, because the condition is still what closes this and the
artifact is only how.

## R-186. The genre lookup defaults the soft-delete marker, and U40 is what gave it a caller

**Found by** U40's first-caller sweep of `write/metadata`, 2026-08-26, and filed
rather than fixed because `docs/METHOD.md`'s do-not-touch section names this
line and assigns it to the parked conformance branch.

`write/metadata.resolve_genre_id` at `src/cratekit/write/metadata.py:195` reads
`getattr(row, "rb_local_deleted", 0)`. Zero is the PERMISSIVE answer, so a genre
row that cannot report the marker is treated as live. That is the exact shape
`write/trees.ContentRow.deleted` refuses by having no default, and whose one
implementation is `trees.soft_delete_marker`, which raises rather than assuming.
Two readers of the same column in one repository, one refusing and one
defaulting.

**Driven, and the two halves are different measurements.** The MECHANISM was
driven on 2026-08-26 against the real function with two stand-in bindings: a
genre row with no `rb_local_deleted` attribute at all, and one carrying `None`.
Both resolve to the row's identifier, so both would be linked as a live genre.
The PRODUCER was not driven. Whether pyrekordbox can hand this function a genre
row that omits or nulls that column is unmeasured here, and the live database is
off limits by standing constraint, so this session could not find out. Saying
"nothing produces it" would be the wrong sentence; nothing was driven that
produces it, and nothing was tried.

**What U40 changed about it.** Nothing in the line. `plan_genre_retag` was
`resolve_genre_id`'s only caller and itself had no caller anywhere in `src`, so
the defect was dormant. `tagging/retag.plan_library` is now a caller a person
reaches through `crate tag retag`, which is the condition the corpus entry
"adding the first caller makes you the owner of its unreviewed defects" turns
into ownership. It is filed rather than acted on only because condition 3 of the
merge bar is unmet: the input's producer could not be driven.

**Measured cost if the producer exists.** A track is linked to a genre row the
user deleted. Routing then places it by a genre that is not in the library's
live taxonomy, and the retag reports success.

**Why it is not fixed here.** METHOD's do-not-touch section names
`write/metadata.py:195` as the parked branch's, and that branch is out of scope
until Phillip says otherwise. Landing a second fix on the same line from a
different branch is how the two come to disagree at the merge.

**Closes when:** `resolve_genre_id` reads the marker through
`trees.soft_delete_marker`, or somebody drives a binding that omits the column
and the finding is promoted or dismissed on the measurement.

---

## R-187. The engine's fuzzy anchor lookup cannot tell a title from that title plus a version suffix

**Found by** U43 while deciding the setbuild verb's positional argument,
2026-08-26. Filed rather than fixed because its input is not reachable from any
shipped verb.

`setbuilder.find_in_index` at
`src/cratekit/modules/tools/setbuilder.py:705` matches with
`fuzz.token_set_ratio`, which scores a subset at 100. So an exact query naming a
track scores identically against that track and against any longer title
containing its tokens, and `process.extractOne` returns whichever it met first,
which is index order. `MATCH_THRESHOLD` is 90 and does not help: both candidates
are at 100.

**Driven, 2026-08-26.** An index holding `Alder - Anchor Work (Extended Mix)`
followed by `Alder - Anchor Work`, queried with the exact string
`Alder - Anchor Work`, returns the Extended Mix. The engine's own comment on
that threshold says building a set around the wrong anchor is worse than
refusing to build one, because every pick after it is internally consistent and
therefore looks right. This is that failure, reached without a typo.

**The producer was NOT driven, and the reachability is what keeps this a
residual.** `find_in_index` has one caller, `resolve_anchor`, which has one
caller, `build_set`. Measured with `git grep -n "build_set\|resolve_anchor" --
src` on 2026-08-26: no module under `src` calls either. `crate setbuild`
deliberately resolves its anchor by path against the index and composes
`build_pool`, `rank` and `build_plan` itself, so nothing a person can type
reaches this code. Two candidate producers were driven and neither produces it;
that is a different sentence from "nothing produces it", and only the first one
was measured.

**Closes when:** either a caller for the fuzzy lookup ships, at which point this
becomes blocking and needs a tie break that prefers an exact match on the
comparison key before falling back to the fuzzy score, or the lookup is deleted
along with the web-enrichment seam it exists to serve.

---

## R-188. A declared state file has no writer, so every set costs a full library scan

**Found by** U43, 2026-08-26, as the consequence of the cache decision that
unit's brief asked to make explicitly.

`config.StateFile(key="setbuilder_index_cache")` at
`src/cratekit/core/config.py:1622` declares a library-scoped cache whose own
`why` says the whole-library tag scan it avoids "costs minutes per run on a
library of this size". `build_index` accepts the `cache_path` that would fill
it. Nothing in `src` passes one.

**Why this unit did not fix it.** `Entry.__post_init__` in
`src/cratekit/cli/registry.py:184` makes anything declaring
`writes={"files"}` destructive by definition, and the destructive-session gates
bind to that flag. Passing a cache path would either be a `files` write from a
verb whose entry declares none, which is the divergence, or would require
declaring one, which binds a read-only recommender to the library lock, the
backup acknowledgment and the volume identity assertion. Neither is a shell
unit's call.

**Measured, not estimated as a cost:** unmeasured. No timing was taken against a
real library, because the live library is off limits by standing constraint and
the fixture libraries here hold single-figure track counts. The state file's own
text is the only claim about the size of this, and it is the source system's
claim rather than this product's measurement.

**Closes when:** somebody decides whether a state-file write is a `writes`
surface at all. A `state` member alongside `files` would let a read-only verb
declare a cache without inheriting the destructive gates, and that is a registry
decision rather than a verb's.

---

## R-189. Six sites build the name template from config independently

**Found by** U43 while writing the sixth, 2026-08-26.

`core.naming` takes configuration as parameters and imports none, which is
deliberate and stated in its own module docstring. The consequence is that every
consumer constructs its own `NameTemplate` from `cfg.naming.lossy_marker`.
Measured on 2026-08-26 with `grep -rn 'MarkerRule(field="lossy"' src`: six sites,
in `write/naming_cli.py`, `cli/reports.py`, `intake/repair.py`,
`intake/ingest.py`, `acquire/match_cli.py` and now `setbuilder/cli.py`.

**The cost is a class rather than a live defect.** A field added to the declared
name shape, or a second marker rule, reaches whichever of the six the author
remembered. Nothing compares them, and a template that differs by a marker
parses a marked title differently, which U43's own H4 mutation row measures: with
the marker declared a clean title is `Anchor Work`, without it the title keeps
the marker and the match key gains a token. No two of the six were found to
disagree today.

**Closes when:** the construction lives in one place both halves read, most
plausibly a `template_for(cfg)` in `core.naming`, which is a same-layer import
and would not violate the rule that keeps configuration out of that module's
own logic.

---

## R-190. The plan surface has no field for the input a plan was computed for

**Found by** U43, 2026-08-26, while fitting a set plan into `plan/1`.

`output._PAYLOAD_FIELDS["plan"]` declares exactly `digest`, `items`, `totals`
and `chunk`, and `payload_problems` rejects any fifth key. A set plan's most
important fact after the recommendations is the anchor they were computed for:
what was resolved, whether the library owns it, its key and its tempo. It is not
an item, because it is not a recommendation. `totals` is the surface's only
plan-level object, so `setbuild` carries the anchor inside it, beside three
counts.

**The cost is legibility rather than correctness.** Nothing is lost and nothing
is wrong; a consumer reading `totals` finds an object that is mostly counts and
one thing that is not. Every other plan-emitting verb in the product answers
about a scope that needs no naming, so none of them has met this.

**Closes when:** either `plan/1` gains a `subject` field and a major bump, which
`output.py` says in its own error text is a decision rather than an oversight, or
a second verb meets the same shape and the pair makes the case.

---

## R-191. The queueing path exits OK on a recording that is not there

**Found by** U44 while writing the handler, 2026-08-27, and filed as a
consequence of `R-183` rather than as a decision of this unit's own.

`crate master <path>` freezes the path into the job payload and never stats it.
That is deliberate and the handler's comment says why: queueing needs neither
the file nor ffmpeg, and a stat in the handler would refuse on a machine where
the work would have run fine later, which is the split R3 asked for. The engine
does check, `mastering.master` refuses `source-missing` at PRECONDITION as its
first act, and `tests/test_master_cli.py` drives that on the work path.

**Measured, 2026-08-27, against a configured library with no database, an
empty PATH and no such file.** `crate master Music/REC0001.WAV --output json`
exits 0 in 199 ms with `state: queued`, a job identifier, and `cause: null`.
The path was confirmed never statted. So a person who mistypes a path is told a
job was queued, and because nothing in `src` claims a job item (`R-183`), the
refusal the engine would raise is never raised by anything. The person learns
of the typo when they go looking for a master that does not exist.

**Why it is not fixed here.** The refusal exists and is on the right path. What
is missing is the worker that would reach it, and that is `R-183`'s closure, not
this verb's. Adding a stat to the handler would repair the symptom for one verb
by breaking the property every queued verb shares, and would still leave a
mistyped path on a machine whose volume is not yet mounted refused at queue
time for a run that would have succeeded.

**Closes when:** `R-183` closes and a job over an absent recording reports the
engine's `source-missing` as its cause. The test to write on that day asserts
the reported cause rather than the queueing exit status.

**Measured on U46, 2026-09-01.** The second half is now driven:
`tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
queues a recording that does not exist, re-enters the verb with `--job`, and reads
`source-missing` off the ITEM's row. The job's own cause is
`unavailable-transient` and the envelope carries `no-evidence`, each wrapping it,
which is where a reader looking for the slug on the job would not have found it.
This does not close the entry: it turns on `R-183`, which U46 narrows and does not
close, so this stays open on its first clause alone.

---

## R-192. `encoder-missing` is reachable from the shell and no test drives it

**Found by** U44 while closing its verification list, 2026-08-27.

`mastering.Refusal` has seven members. Six are raised by a test on this
branch: `source-missing`, `source-unsupported`, `output-exists`,
`archive-holds-a-different-recording`, `encoder-failed` and, since round two,
`archive-verify-failed`. The seventh, `encoder-missing`, is raised at
`src/cratekit/modules/tools/mastering.py:555` when `binaries.resolve` cannot
find ffmpeg or ffprobe, and again at `:716` for the join. No test in
`tests/test_master_cli.py` or `tests/modules/test_tools.py` reaches either
site; `tests/test_reserved_causes.py` only checks that the slug reserves
PRECONDITION.

**It is reachable, and the drive is cheap.** An empty PATH with no
`CRATEKIT_BIN_FFMPEG` set makes `binaries.resolve` raise, and `run_master`
would translate the member through the same `except` that
`C4_refusal_not_translated` measured at eight kills. The reason it was not
written is sequence rather than difficulty: the gap was noticed after the
mutation tables were measured, and a test added after a table is a test the
table never saw. It is recorded here so the next round measures it rather than
inheriting an assumption.

**Cost, stated.** If the translation ever stopped covering this member, a
machine without ffmpeg would be told to file a defect against this program
rather than to install an encoder. Today nothing distinguishes the members
inside the `except`, so the exposure is to a future edit rather than a live
defect.

**Closes when:** a test drives `encoder-missing` through `run_master` with an
empty PATH, and a mutation row that removes the `binaries.resolve` guard
reports a kill.

**Half measured on U46, 2026-09-01.** The first clause is driven, through the
override the resolver actually reads rather than by replacing the resolver:
`tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
points `CRATEKIT_BIN_FFMPEG` at a path that is not there, drives a queued job, and
reads `encoder-missing` off the item's row. The mutation row is not written, so
this stays open on its second clause.

---

## R-193. A split recording has no route through this verb, and its predecessor is invisible

**Found by** U44 while settling the verb's input shape, 2026-08-27, and
deferred as an open product question rather than decided.

The XDJ-RX3 splits a long set into several files, and the source system's
`master_set.sh` ships `--concat` for exactly that case. The engine has
`concatenate` at `src/cratekit/modules/tools/mastering.py:683`, and since U44 it
reads its own output. Nothing in `src` calls it: `git grep -n "concatenate("
-- src` returns its definition and three `np.concatenate` calls in
`analysis/vocal.py`, which are a different function. `crate master` takes one
positional, so a person whose set arrived as three files gets three masters and
keeps using the script, while Feature Inventory row 30 reads as covered.

**Two facts make the gap invisible from inside the repository.** The entry
declares no `source_scripts`, where `backup.run` declares `backup.sh`, and
`master_set.sh` is absent from `tests/fixtures/dj_tools_scripts.txt`, whose
second block exists for workflows that are not console scripts. So no test can
notice that this verb has a predecessor, let alone that the predecessor did
something this verb does not.

**Why it is not fixed here.** Adding `--concat` widens the declared surface,
which the tracker told this unit not to redesign, and the planning
recommendation was to keep this verb at one positional and give the join its
own verb. That is Phillip's call and it has not been made.

**Closes when:** either a join verb ships and `concatenate` gains a caller, or
the decision is recorded that split recordings are joined outside this product.
Whichever way it goes, the entry should name `master_set.sh` as its
`source_scripts` and the fixture should list it, so the next gap of this shape
is visible.

---

## R-194. The loudness target is not exposed, so a person who needs a different one edits source

**Found by** U44 while settling the flag surface, 2026-08-27, and deferred as
the second open product question.

`Settings.target_lufs` defaults to minus fourteen at
`src/cratekit/modules/tools/mastering.py:124`, and the engine's own comment
records that this suits general playback while a louder target suits platforms
that normalise upward. `Settings` is constructed exactly once in `src`, as
`DEFAULT_SETTINGS`, and `crate master` passes nothing into it. The source
system's script ships `-t` for this.

**Cost, stated.** A person mastering for a platform with a different target has
no route but editing the module. Nothing is wrong with the master that is
produced; it is produced to a target the person could not choose.

**Why it is not fixed here.** The same reason as `R-193`: it widens the declared
surface, and the recommendation on the table is to expose `--target-lufs`
alone, freeze it in the payload and carry it in `master_argv`, leaving the other
four knobs at their defaults. That is a decision rather than a fix.

**Closes when:** the flag ships with its payload key and argv round trip driven
by the resume contract, or the decision is recorded that one target is the
product's position.

## R-195. The adapter never tells the downloader where ffmpeg is, so a lossless run lands lossy with doctor reporting green

**Found by** A1, the attended smoke test of the vendored downloader,
2026-08-28.

`crate doctor` reported `[ok] binary.ffmpeg: /opt/homebrew/bin/ffmpeg`, and the
first track still landed as a 320k AAC `.m4a`. The vendored tool does not look at
`PATH`. It consults only its own `path_binary_ffmpeg` setting, whose factory
default is the empty string, and when that is empty `Download.__init__`
(`src/cratekit/_vendor/tidal_dl_ng/download.py:162`) flips `extract_flac` and
`video_convert_mp4` off and logs one warning through a logger the adapter
discards. `tool_settings()` in `src/cratekit/acquire/vendored.py:74` pushes
`quality_audio`, `download_base_path` and `format_track`, and nothing else, so a
real Cratekit run degrades the same way. Setting the key by hand and downloading
again produced the FLAC.

**Cost, stated.** Doctor answers a different question from the one the tool
asks. Doctor asks whether ffmpeg exists on this machine; the tool asks whether it
was told the path. The two agree only on a machine where somebody has already
run the vendored CLI's `cfg` by hand, which is how this machine looked until the
test reset it, and which is exactly the state that would have hidden the defect.

**Why it is not fixed here.** A1 is an attended verification, not a unit, and
the fix belongs to the adapter's settings mapping with a test that pins the
fourth key. The value to push is the one `core/binaries.py` resolves, so doctor
and the tool answer from one lookup.

**Closes when:** `tool_settings()` carries `path_binary_ffmpeg` from the
binaries resolver, `verify_applied` checks it, and a test asserts the pushed set
has four keys.

**Closed by U47, 2026-09-01, on its own stated terms.** `tool_settings()` takes
the resolver as a keyword parameter defaulting to `binaries.resolve` and pushes
the fourth key; `verify_applied` covers it by it being pushed rather than by a
second list; and the test asserts the pushed SET rather than three names, because
a missing key in a mapping nothing counted is the whole of this finding. An
unresolvable ffmpeg now refuses the run with `INSTALL_ADAPTER` instead of pushing
the empty string, since empty is exactly the value the tool reads as
do-not-extract-FLAC, so an absent encoder would otherwise have arrived as a
successful lossy download.

## R-196. The provider serves lossy audio to the device-flow client, and neither the vendored tool nor the adapter can log in any other way

**Found by** A1, 2026-08-28, and it reaches past this repository.

With `path_binary_ffmpeg` set, the same track still came down as AAC. The
account is PREMIUM with `highestSoundQuality: HI_RES`. The session asked for
`LOSSLESS` through `config.quality`, and `playbackinfopostpaywall` answered
`HIGH` every time, for `LOSSLESS` and for `HI_RES_LOSSLESS` alike. The live
DJ_tools token, issued 2026-08-01 against the same `tidalapi` 0.8.11 and the same
client id, got `HIGH` for the same track in the same minute. The newest FLAC the
live pipeline ever produced is dated 2026-07-09.

A PKCE login on the same account, same track, same minute, was served
`LOSSLESS` as a 16 bit 44.1 kHz FLAC over a DASH manifest, and the vendored
`Download` class landed it. So the cause is the client, not the account, the
settings, or the patches: the provider now gates lossless behind the PKCE client
that `tidalapi` documents as the route to hi-res, and the device-linking client
both tools use has been quietly demoted to lossy at some point after July 9.

Three facts make this a code problem rather than a login problem. The vendored
CLI has no PKCE path; `Tidal.login()` in `config.py` calls `login_oauth_simple`
and carries the PKCE call as a comment. `token_persist()` writes four keys and
drops `is_pkce`, so a PKCE token written by that code would be reloaded as a
device-flow one and refreshed against the wrong client. And the adapter calls
`login_token()` with PKCE off (`src/cratekit/acquire/vendored.py:217`).

**Cost, stated.** Every download through the current path is lossy and nothing
says so. The lossless rule is enforced at the setting and never at the file, so
the product's central promise fails silently. The live system has been failing
it since July.

**Why it is not fixed here.** It is a unit's worth of work across the adapter,
the vendored token persistence, and the login verb's contract, and it is a
decision about which login the product offers. The one-line guard that IS cheap,
refusing to accept a landed file whose codec is not lossless when the policy is
lossless, belongs beside it.

**Closes when:** the adapter authenticates through PKCE, or through a session
file that records `is_pkce`, and a post-landing check refuses a lossy file under
a lossless policy. The DJ_tools note is separate and is owed to that repository.

**Closed by U47, 2026-09-01. Both halves, and the DJ_tools note is still owed.**
PKCE is the product's only login path, decided by Phillip and not litigated in
the unit. Three vendored patches, all declared in `scripts/revendor_downloader.py`
and applied through it: the `Token` model gains `is_pkce`, `token_persist` writes
it, and `Tidal.login` mints through `login_pkce`. No PKCE handshake was added to
the vendored tree; `tidalapi` already ships one and upstream already carried the
call as a comment beside the one it used. The adapter calls
`login_token(do_pkce=True)` and refuses a stored non-PKCE session outright rather
than downloading lossy audio with it. The post-landing codec check is in
`landed_file`, at the acceptance rather than at the request.

Two things the unit found that this entry does not say. `token_persist` cannot
write the flag through `set_option`: that method calls `.lower()` on the incoming
value whenever the existing one is a bool, and `is_pkce` is the token model's
only bool field, so the obvious edit raises `AttributeError`. And the source must
be the SESSION's flag, not the `Tidal` object's, because `login()` calls
`login_token()` first and that assigns `self.is_pkce` from its own defaulted
argument before any PKCE handshake runs, so reading it there would record every
fresh PKCE session as a device flow one.

What this closure COSTS, and it is not free: every session in the keychain before
this merge was minted by the device flow, so the refusal is what an existing
installation meets first. The re-authorisation is two attended commands and is
written down in `docs/adapters.md`, because a refusal whose remedy has no
procedure behind it is worse than the lossy download it replaces.

## R-197. The adapter's fetch constructs the downloader without the events and progress it requires, so the first real call crashes

**Found by** A1, 2026-08-28, while driving `Download` directly to land the FLAC.

`_VendoredSource.fetch()` at `src/cratekit/acquire/vendored.py:254` builds
`Download(tidal_obj, path_base, fn_logger)`. The vendored CLI builds it with
`event_abort`, `event_run`, `progress` and `progress_overall` as well
(`cli.py:250`). Without the events, `Download.item()` dies on its first line,
`self.event_abort.is_set()` on `None`. With the events and without the progress
objects it returns `(False, path)` and logs nothing, because the progress bar is
touched inside the download and the failure is swallowed. With all four it
downloads.

**Cost, stated.** `fetch` is the one method the offline suite cannot exercise
and is marked `pragma: no cover` for that reason, which is also why this
survived every green battery. The adapter has never fetched a file.

**Why it is not fixed here.** Same as R-195: an attended item records, a unit
fixes. The fix is small and the test for it is the hard part, since it needs a
fake `Download` that asserts the constructor's keyword set.

**Closes when:** `fetch` passes both events and a disabled `rich` `Progress`
pair, and a test pins the constructor call.

**Closed by U47, 2026-09-01, with one correction to this entry's own text.**
`fetch` passes all seven keywords the vendored CLI passes (the CLI passes eight;
`skip_existing` stays at its `False` default because this product always
downloads). Three tests pin it: a fake downloader records the keyword set, an AST
walk reads what the module writes so bypassing the seam is caught too, and a
third asserts every keyword exists on the real `Download.__init__`.

The correction: this entry says the missing events make `item()` "die on its
first line", and that is true of `item()` but not of the constructor.
`Download.__init__` declares all four with `None` defaults, so it accepts any
subset silently. A test asserting the constructor REFUSES a missing argument
therefore cannot be written, which is why the test asserts what `fetch` passes.

A hazard this entry does not name and which cost a design round to find:
`event_run` must be passed already SET. `Download._download_segment` runs
`self.event_run.wait()` inside its worker pool when the event is clear, and the
vendored `HandlingApp.__init__` is the only thing in that tree that sets it. A
fresh unset `Event` blocks every segment worker on something nothing will wake,
so the failure is a HANG rather than an error and no message names its cause.
Passing the keyword is not enough; its state is the requirement, and there is a
test for that alone.

## R-198. Nothing calls the job driver, so every long-running verb queues work the product never runs

**Found:** during U42, 2026-08-28, while landing the two acquisition shells and
asking what "row 6 is covered" actually buys.

`cratekit.core.jobs.drive` is the loop that claims a job's items, runs a handler
against each, commits artifacts and records failures. It has NO CALLER ANYWHERE
IN `src`. Verified with `git grep -n "drive" -- src`, which returns its own
definition at `core/jobs.py:1181`, two strings naming it in causes it raises, and
nothing else. The only driver that ever calls it is `tests/job_worker.py`.

The path a person actually takes ends one step short of it. A long-running verb
enqueues and reports. `crate job resume <id>` reconciles, then `jobs.spawn`
launches the child that `argv_builder` describes. That child re-enters the same
verb with `--job <id>`, takes the `if ctx.args.job:` branch, reconciles, reports
the job, and exits.

SIXTEEN resume branches across fifteen modules, and NONE of them calls `drive`.
Measured by walking the package with `ast` and reading each `if` whose test names
`ctx.args.job`, rather than by reading the first two and generalising: the first
draft of this entry said twelve, named a list from memory, and was wrong in both
the count and the membership. The sixteen are in `acquire/cli.py` (this unit),
`adopt/apply_cli.py`, `adopt/scan_cli.py`, `analysis/cli.py` (two),
`cli/rebuild.py`, `export/cli.py`, `favorites/cli.py`, `intake/cli.py` (two),
`label/cli.py`, `master/cli.py`, `sync/cli.py`, `tagging/cli.py`,
`tagging/retag_cli.py` and `write/routing_cli.py`. So a queued job cycles between
reported and respawned and its items stay `pending` for ever.

**Why it is filed under this unit rather than under the fifteen.** U42 is the unit
that cleared Feature Inventory rows 6 and 7 from the cutover backlog, and row 6
is "vendored concurrent downloader". `tests/test_cutover_parity.py` now says the
row has a covering verb, and it does: `acquire.download` is landed, reachable
from the command line, and declares the row. What the parity table asserts is
that a verb exists for the row, which is exactly what it was built to assert and
is a weaker claim than the cutover needs. The downloader itself is still not
reachable end to end, and neither is tagging, analysis, export, or adoption.
Recording it here is what keeps the difference between the two claims visible
when U29 reads the table and sees every row green.

**Not fixed here, deliberately.** The missing half is a handler registry: a map
from `handler_key` to the function `drive` should call per item, plus the site
that calls `drive` with it. That is a seam decision about where handlers are
declared and how they are imported lazily, and KTD26's whole scheme rests on the
supervisor validating a key without importing the module, so the registry has to
be a third thing rather than an import. It is a unit, not a fix, and it is one
that touches all sixteen sites at once. Doing it inside a shell unit for two of
them would land the seam in the wrong place and by the wrong author.

**What is genuinely at stake, stated rather than left implied.** This is a
cutover blocker and not a cosmetic gap. U29 requires each replacement workflow to
run correctly on the live library at least once, and no queued workflow can run
at all today. The parity table will not catch it, because the parity table
measures verbs.

**A consequence worth naming, because U42's brief expected otherwise.** That
brief made this unit "the first caller of everything in `src/cratekit/acquire/`
except `match.py`" and asked for a driven failure path on an engine function the
unit newly reached. It reached none. The grep it asked for was run and found
three functions with exactly a definition and an export line and no caller at
all, `download.acquire_paced`, `adapter.dispatch_invocation` and
`adapter_names`, plus `download.acquire_concurrently` whose only caller is
`acquire_paced` and is therefore dormant behind it. `acquire_paced` is precisely
the function an acquisition worker would call.

The shell does not call it, because the shell freezes and queues and the brief
itself says the worker binds the live adapter. So the first-caller obligation did
not transfer to this unit; it transfers to whoever lands the handler binding this
entry is about, and `acquire_paced` stays a shipped, never driven function until
then. Said here rather than left as a quietly unmet test scenario, because "no
engine failure path was driven" reads as an omission unless the reason is
recorded.

**Closes when:** a unit lands the handler binding and one verb's queued work runs
to completion through `crate job resume`, driven rather than asserted. That unit
inherits the first-caller reading of `acquire_paced` and
`acquire_concurrently` described above.

**Measured on U46, 2026-09-01. This entry is CLOSED.** `src/cratekit/cli/handlers.py`
declares `handler_key` to `"module:function"` as inert strings, resolves one with
a single lazy import, and holds the one call to `jobs.drive` in the package,
asserted by an `ast` walk rather than a text search. `crate master` queues one
item and re-entering the verb with `--job` runs it to `done`, read back from the
store. The branch count in this entry was also wrong by the time it was read: an
`ast` walk finds seventeen branches in fifteen modules, because `backup/cli.py`
joined when U45 landed. The population that matters is the registry's twenty
landed `long_running` entries rather than the branches, and the eighteen that stay
unbound are `R-203`. The first-caller obligation this entry transfers did NOT
transfer, because U46 binds `master` rather than acquisition, and the reason is
`R-204`.

## R-199. `Entry.destructive` is read by nothing, and its own validation message says the gates bind to it

**Found:** during U42, 2026-08-28, while deciding whether `acquire.download`
should declare a confirm gate.

`registry.Entry.destructive` is validated against `writes` at
`cli/registry.py:184`, and the refusal it raises reads: "anything that writes
files or deletes is destructive by definition (KTD24); the destructive-session
gates bind to that flag, so a verb that lies here runs without them." The second
clause is not true of this build. `git grep -n "\.destructive\b" -- src` returns
exactly one hit, that validation line itself. No dispatcher, no context, and no
gate consults the flag.

What actually happens is sound and is a different mechanism: the modules that
touch the volume open a session themselves. `write/trees.py`, `write/
routing_pass.py`, `deletion/run.py` and `adopt/apply_cli.py` each call
`core.session` directly, so the acknowledgment and the backup age are asserted by
the code doing the destruction rather than by the declaration describing it.

The cost is not a hole in the gates, it is a sentence that will be believed. A
person reading that message concludes the flag is load bearing and that declaring
it buys protection. It buys a consistency check against `writes` and nothing
else. This repository has now recorded twice that a false claim in a place every
reader trusts is its own failure class, and a refusal message is exactly such a
place.

**Not fixed here, deliberately.** The honest repair is one of two things and
neither belongs to a shell unit: either bind the flag to something, by having the
dispatcher assert the session for a destructive verb, which is a real behavioural
change across every destructive verb in the product; or reword the message to say
what is true, that the flag is a declaration the registry checks for consistency
and that the session is opened by the code that touches the volume. The second is
a one line change and is still not this unit's to make unilaterally, because the
first is the option somebody may prefer and rewording it forecloses the question
quietly.

**Closes when:** either the flag is consulted by the code that opens a session,
or the message stops claiming that it is.

---

## R-200. A failed archive prune reaches no report, so dated folders can accumulate with nothing saying so

**Found:** during U45, 2026-08-29, while becoming the first caller of
`run_backup` in `src` and asking what its returned `PortionOutcome.results`
carries that the shell does not read.

`run_backup` reads every return code that DECIDES a portion: each transferring
command's result is compared against zero and the portion stops on the first non
zero, which is what `ran` then reports. The archive prune is the one class it
deliberately does not fail on, and `_prune_archive`'s docstring argues that
correctly: by the time it runs, the mirror in the same portion has completed, so
the backup the person asked for exists, and a stale folder using remote space is
a smaller problem than reporting a completed backup as failed and having them run
the whole transfer again.

What that argument does not cover is REPORTING. `run_backup`'s prune branch does
`results += _prune_archive(...)` and then `continue`, so the listing's return code
is never compared to anything, and `_prune_archive` returns early on a failed
listing having pruned nothing. The results are carried on `PortionOutcome.results`
and `outcome_payload` does not render them, so `cratekit.backup.cli` has nothing
to report even if it read them. A person whose remote refuses `lsf` gets a
successful backup and a fresh published age, both of which are true, and no
indication that the rotation has stopped. Dated archive folders then accumulate
for as long as the condition lasts.

**Why it was not fixed here.** Failing the portion from the shell would overrule
the engine's decision from the wrong layer, which is METHOD's pattern 3 inverted.
Reporting it needs a new key in `outcome_payload`, and that payload belongs to
`cratekit.modules.tools.backup` rather than to this unit's shell. The shell
records why it drops `results` in a comment at the call site instead, which is
what the first-caller learning asks of a returned value nobody inspects.

**Cost, stated rather than measured:** unbounded remote storage growth with no
signal. NOT DRIVEN, and this line is the measurement discipline rather than
modesty: driving it means an rclone stand-in that fails `lsf` and succeeds at
`sync`, and the finding is about the absence of a report rather than about a
behaviour a drive would show.

**Closes when:** `outcome_payload` carries the prune's outcome per portion, or
`run_backup` reads the listing's return code and records a warning the shell can
render.

**Closed by U48, 2026-09-02, taking the SECOND condition and not the first.**
The recorded warning is what landed; `outcome_payload` renders it and does not
derive it. Saying which one was taken matters because taking both is how one
condition acquires two reports that drift apart.

The classification moved one level further in than the condition's own wording
suggested. It reads "have `run_backup` read the listing's return code", and
`run_backup` is the wrong place: `_prune_archive` already reads that return code,
in the branch deciding whether to purge at all, and it is the only function that
knows which of its results is the listing. Re-reading it in `run_backup` would
have been a second read of one code, identifying the listing by its position in
a returned list, which is METHOD defect pattern 2. So `_prune_archive` returns
its results and at most one warning, `run_backup` records what it is handed, and
`outcome_payload` stays a renderer.

TWO CODES, `archive-listing-failed` and `archive-purge-failed`. A listing this
account cannot get is a remote or credential problem and nothing was removed; a
purge that failed on a folder the listing named is that folder, and the rest of
the rotation happened. Two conditions with different fixes, so one code over
both would leave the difference in the message, which is the only part nothing
can branch on. Neither is a refusal cause: every member of `Refusal` is a reason
one portion will NOT run, decided before anything is attempted.

**The drive this entry recorded as NOT PERFORMED has now been performed**, at
both layers. A stand-in rclone that fails `lsf` and answers everything else
gives a report whose files portion carries the rotation warning, `ok` true, and
a published age that is genuinely fresh, with the mirror asserted to have run
from the program's own invocation log. Measured at `docs/mutation/u48-author.md`:
dropping the listing classification kills 4, dropping the purge classification
kills 1, collapsing the two codes into one kills 1, not recording the warning on
the portion kills 5, and dropping the key from the payload kills 3.

**One thing this entry did not name, swept for and found.** The rehearsal branch
ran the listing and read nothing, three lines from the code this entry is about,
so a preview whose remote refused `lsf` described a rotation it had already
discovered it could not perform. It is folded into the same call behind a purge
flag, so there is one prune path and one reading of it.

---

## R-201. The destructive session fixes the unreadable-fact remedy at repair, discarding the permission answer the exception carries

**Found:** during U45, 2026-08-29, while writing `published_ages` and reading
`core.session._shown_ages` beside it to make sure both answer from one source.

`backup_facts.Remedy` declares THREE members, and its own docstring says why the
third exists: "a file this account may not open and a file whose contents are
damaged are two conditions with opposite fixes, and one token over both told a
user to repair or reset the record of when their music was last protected in
order to fix a permission". `read_facts` raises `GRANT_PATH_ACCESS` for a
permission error and `REPAIR_BACKUP_FACTS` for a damaged one, and it distinguishes
them at the raise site.

Three consumers read that exception. `cli/doctor.py:1600` carries the remedy
through with `Remedy(str(exc.remedy))`. `cratekit.backup.cli.published_ages`, new
in this unit, does the same. `core/session.py:1046` does not: it writes
`remedy=Remedy.REPAIR_BACKUP_FACTS` unconditionally, so a person whose
configuration directory this account cannot traverse is told to repair or reset a
file that is very likely intact, in the refusal standing immediately before the
riskiest operation in the product.

**Why it was not fixed here.** This unit is not the first caller of anything on
that path: `session` and `doctor` both read `backup_facts` on `main`, so the
finding does not become reachable because of this branch and the merge bar's third
condition does not turn it into a blocker. It is a one line change in `core` on a
branch whose diff is otherwise a new package, and folding it in would put a core
session edit inside a commit nobody would look for it in.

**Closes when:** `core/session.py`'s `_shown_ages` carries `exc.remedy` the way
its two sibling consumers already do.

**Closed by U48, 2026-09-02, and it was already recorded once.** R-56 item 2 is
the same defect, filed at U38 from the newer-build angle rather than the
permission one, and neither entry cites the other. Both close on this commit and
both say so. That two independent reviews found one line and neither found the
other's note is the more useful half of this record: a ledger this size does not
prevent a rediscovery, so a fix should search it by symbol before assuming it is
the first.

`_shown_ages` now writes `remedy=Remedy(str(exc.remedy))`, verbatim from
`cli/doctor.py` and `backup.cli.published_ages`. Nothing was added to either
`Remedy` enum or to the reservation table, because all three tokens were already
declared and `grant-path-access` was already reserved.

**Driven through `read_facts` rather than through a hand built exception**, which
is the distinction this finding turns on: an exception built by hand can carry a
field the code path never produces, so it would prove the refusal renders a
token rather than that the token reaches it. The permission case makes a real
`PermissionError` at the file boundary and asserts that precondition rather than
assuming it, since an account the mode bits do not restrain reads the file and
the guard would pass over a refusal that never occurred.

**All three tokens, not one.** The carry moves every remedy `read_facts` raises,
so the damaged file keeping `REPAIR_BACKUP_FACTS` and a newer `schema_version`
answering `UPGRADE_CRATEKIT` are guards in their own right; a fix measured only
on the permission case would leave two thirds of it asserted. Measured at
`docs/mutation/u48-author.md`: hard coding the repair token again kills 2, and
hard coding the permission token over every condition kills 2, which is the same
defect mirrored and is why both directions are driven.

Two prose sites this entry made false are corrected with it. The conversion
proof's docstring cited this handler as its live example and now marks it
historical while restating the hole, which did not close. The
`grant-path-access` reservation measured its exit code from the flattening
itself; the code has not moved and the reasoning under it has.

---

## R-202. `BackupOutcome.ok` can only ever be true in a report the backup shell emits

**Found:** during U45, 2026-08-29, while closing mutation row `E5_outcome_ok_widened`,
which widened the property from `all` to `any` and killed zero tests.

`outcome_payload` renders `ok` into the payload `cratekit.backup.cli.perform_backup`
returns, and `perform_backup` calls `refusal_for` before building that payload.
`refusal_for` raises whenever any portion has `ran=False` with no refusal on it,
which is exactly and only the condition that makes `BackupOutcome.ok` false: `ok`
is `all(p.refusal is not None or p.ran ...)`, so a portion that refused satisfies
it and a portion that ran satisfies it, leaving the failed portion as the sole
falsifier. Every report that survives to be returned therefore carries `ok: true`,
and a consumer reading that field learns nothing it did not already learn from the
call not raising.

**Why it was not fixed here.** Two remedies and neither is this unit's. Dropping
the key means editing `outcome_payload`, which is the ENGINE's report shape and is
also rendered by nothing else today, so removing it is a change to a public payload
made from a shell. Reporting a partial run as `ok: false` instead of refusing means
reversing `refusal_for`'s decision, and that decision is argued: a person told a
backup succeeded stops looking, so a failed portion earns an exit code rather than
a field.

**What it is NOT.** Not a wrong value. Every `ok: true` this shell emits is true.
The finding is that the field is not load bearing, so a reader who trusts it as
the run's verdict is trusting the exit code twice.

**Cost:** a consumer that branches on `data["ok"]` rather than on the exit status
has a branch that never runs, and would keep passing if the classifier broke.
Driven only as the mutation row: nothing in `src` or `tests` reads the field.

**Closes when:** either the key leaves `outcome_payload`, or something reachable
can produce a report carrying `ok: false`.

---

## R-203. Eighteen queued verbs still have no worker, and the one that does now makes that visible

**Found:** during U46, 2026-09-01, while binding the first handler.

`registry.ENTRIES` holds twenty landed `long_running` entries. `master` is bound
by this unit and `job.resume` is exempt by role, since it is the verb that spawns
the child rather than a verb whose work is queued. The other eighteen remain what
R-198 described: a queue with nothing behind it. They are `acquire.download`,
`adopt.apply`, `adopt.scan`, `analyze.restamp`, `analyze.run`, `backup.run`,
`delete.review`, `export.playlist`, `intake.playlist`, `intake.set`,
`label.import`, `rebuild`, `route.resort`, `sync.all`, `sync.favorites`,
`sync.labels`, `tag.folder` and `tag.retag`.

**The population above is the one U46 measured and it is now five entries out of
date, corrected here rather than rewritten.** U50 bound `backup.run`, U51 bound
`export.playlist` and `sync.favorites`, and U55 bound `adopt.scan` and
`adopt.apply`, so THIRTEEN queued verbs have no worker as of 2026-09-02: the list
above minus those five. The count in this
entry's title is left at eighteen deliberately, because it names what was true
when the entry was written and the closing condition below is what decides when
the entry is done. Nothing in the repository derives from this prose;
`tests/test_handlers.py` derives the population from `registry.ENTRIES` and fails
the day a queued verb is in neither table, which is why this correction is a
record rather than a repair.

**The population is the registry, not the resume branches, and the two are
genuinely different.** An `ast` walk finds seventeen `if ctx.args.job` branches in
fifteen modules. `sync/cli.py` carries one branch serving three handler keys, and
`delete.review` is a landed queued entry with no branch at all, which is R-149.
The first draft of this unit's plan sized the exemption list from the branch count
and was wrong by three. Anything that quantifies over queued verbs derives the set
from `registry.ENTRIES`.

**Not fixed here, deliberately.** Binding the rest is not mechanical, which is the
claim worth recording because the shape of the seam invites the opposite
conclusion. The call site is one line and every verb already has it available
through `Context.run_job`. What is not one line is the two decisions each verb
owes: what its items ARE, and what its per item worker does. Only `analysis/cli.py`
and now `master/cli.py` pass `item_ids` to `enqueue` at all, so sixteen of the
eighteen would queue a job with nothing to claim and drive would report an empty
success over work it never did. And several have no worker to write yet at all:
`adopt.scan` needs a collection reader that has not landed, `acquire.download`
would newly reach an adapter that R-195, R-196 and R-197 say has never fetched a
file, and `sync.all` carries R-130's unregistered obligation about run identity.
U55 landed the reader `adopt.scan` was waiting for, which is what made both adopt
verbs bindable; the claim that binding the rest is not mechanical is unchanged by
it, and U55 is a worked example of why, since deciding what an apply's items are
turned out to be a decision about which resume mechanism owns the run.

**U56 bound `tag.folder` and `tag.retag`, so ELEVEN queued verbs have no worker
as of 2026-09-03**: `acquire.download`, `analyze.restamp`, `analyze.run`,
`delete.review`, `intake.playlist`, `intake.set`, `label.import`, `rebuild`,
`route.resort`, `sync.all` and `sync.labels`. The count in this entry's title
stays at eighteen for the reason the correction above gives.

**U56 is the third worked example of the claim, and the sharpest.** Binding the
two tagging verbs was not one line each. It needed a backend that did not exist,
a searcher over three public catalogues with its rate limiting and its four way
per source outcome; it needed the fill-if-empty engine split so a job item was
reachable; and it surfaced a permanent stall the binding itself created, because
`tag.retag` rebuilt its confirm digest from a fresh walk of the folder and the
first file a worker corrects shrinks that walk. Every respawn after a partial run
met `DecisionStale` for ever. That defect was unreachable while nothing wrote,
which is the general form of what this entry is about: for several of the eleven,
the binding is the thing that makes their own defects reachable.

**U58 bound `analyze.run` and `analyze.restamp`, so SEVEN queued verbs have no
worker as of 2026-09-07**: `acquire.download`, `delete.review`,
`intake.playlist`, `intake.set`, `rebuild`, `route.resort` and `sync.all`.
The count in this entry's title stays at eighteen for the reason the first
correction gives. U58 is the fourth worked example of the claim: the two
analysis verbs were the only ones that already passed items at enqueue, and
the binding still needed the item identifier changed from an absolute path to
a filename, the frozen folder resolved absolute, a resume that finds a file
the finalize renamed before its row moved, and two engine defects fixed
before a worker could produce a true value at all.

**Cost:** the same as R-198's for eighteen verbs, with one change. `crate job list`
and `crate job show` now carry a `worker` field derived from the declaration table
without importing anything, so a queued job that will never run says so. Before
this unit every queued verb was equally broken, which at least taught a person
that queues do not run; one working verb and eighteen silent ones would have
taught the opposite.

**Closes when:** every landed `long_running` entry is in `HANDLERS` and
`HANDLERS_NOT_YET_BOUND` is empty. `tests/test_handlers.py` fails the day a new
queued verb is in neither, so this cannot quietly grow.

**The correction above is itself now two entries out of date, corrected in the
same register, 2026-09-02, by U52.** This unit bound `sync.labels` and
`label.import` to one worker in `src/cratekit/label/cli.py`, so THIRTEEN queued
verbs have no worker. Measured, not subtracted: `HANDLERS_NOT_YET_BOUND` in
`src/cratekit/cli/handlers.py` holds fourteen keys, one of which is the
`job.resume` exemption this entry already describes, leaving `acquire.download`,
`adopt.apply`, `adopt.scan`, `analyze.restamp`, `analyze.run`, `delete.review`,
`intake.playlist`, `intake.set`, `rebuild`, `route.resort`, `sync.all`,
`tag.folder` and `tag.retag`. `HANDLERS` now holds six keys, two of which share
one worker function because the sweep and the import differ in how many labels
they queue and in nothing about how one is swept, and the two tables sum to the
twenty landed `long_running` registry rows. The count in this entry's title stays
at eighteen for the reason the paragraph above gives, and the closing condition
is what decides when the entry is done. Nothing in the repository derives from
this prose: `tests/test_handlers.py` derives the population from
`registry.ENTRIES` and fails the day a queued verb is in neither table, which is
why this is a record rather than a repair.

`sync.all` is on that list and stays on it rather than being filed as anything
new. Binding `sync.labels` does not make `crate sync all` execute a thing,
because `src/cratekit/sync/cli.py` queues its job under `ctx.entry.handler_key`,
which is `sync.all`, and that key still has no worker. It also still carries
R-130's run identity obligation, exactly as the paragraph above says.

**U57 bound `intake.set` and `intake.playlist`, so FOUR queued verbs have no
worker as of 2026-09-09**: `delete.review`, `rebuild`, `route.resort` and
`sync.all`. Measured, not subtracted: `HANDLERS_NOT_YET_BOUND` holds five keys,
one of which is the `job.resume` exemption. The count in this entry's title
stays at eighteen for the reason the first correction gives. U57 is the fifth
worked example of the claim, and the one where the items did not exist until
money was spent: a set's items are the tracks recognition names, so the paid
identification moved to the queue, and the verb needed an identifier behind a
seam that had carried an injection point and nothing else since U37 (R-132),
a spend bound with its own cause, a coverage rule so a set nobody answered is
not reported as a set nobody recognised, and a worker that resolves and offers
and never acquires, because a recognised track carries no provider identifier
and the adapter contract has no search.

**U53 bound `rebuild` and `route.resort`, so TWO queued verbs have no worker as
of 2026-09-10**: `delete.review` and `sync.all`. Measured, not subtracted:
`HANDLERS_NOT_YET_BOUND` holds three keys, one of which is the `job.resume`
exemption. The count in this entry's title stays at eighteen for the reason the
first correction gives. U53 is the sixth worked example of the claim, and the
one where the two verbs shared an ENGINE without sharing a worker: both re-derive
the declaration through `rebuild_governed_tree`, and neither could import the
other's module because one is a CLI verb and one is a write-layer verb, so what
they share had to move down to the engine rather than sideways. The items were
the decision, as the paragraph above predicts: a rebuild's item is a tree, and a
library that has flipped no tree therefore files no job rather than an empty one.

**U60 removed `delete.review` from the population, and NOT BY GIVING IT A
WORKER, 2026-09-10.** It left by ceasing to be queued: its entry dropped
`long_running` and its `argv_builder` (R-149, closed), because the verb was
always inline and never enqueued anything. So ONE queued verb has no worker as of
2026-09-10, `sync.all`. Measured, not subtracted: `HANDLERS_NOT_YET_BOUND` holds
two keys, one of which is the `job.resume` exemption, and the registry holds
nineteen landed `long_running` entries where it held twenty, seventeen of them
bound, with `analyze.vocals` declared and not yet landed. Read the count
honestly: this unit bound nothing, and the closing condition below is met by one
more binding, not by one more drop. A drop is legitimate only where the verb
genuinely does not queue, which
`tests/test_cli_contract.py::test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues`
now checks by parsing each shell for an `enqueue` call. `sync.all` calls it, so
it cannot leave this list the way `delete.review` did.

**U61 CLOSED THIS ENTRY, 2026-09-10, relay task 79, in commit `0afe75d`.** The
last key left by COMPOSITION, and the paragraph above is right that it could
not leave the way `delete.review` did: the work is still queued. What changed is
WHERE. `crate sync all` no longer queues anything under `sync.all`. It calls each
enabled source's own queueing path under that source's own handler key,
`sync.favorites` and `sync.labels`, whose workers already existed, so a pass's
jobs run through bound workers and the entry's `long_running` and
`argv_builder` went because nothing is ever queued under its key to resume.
Measured, not subtracted: `HANDLERS_NOT_YET_BOUND` holds ONE key, the
`job.resume` exemption this entry has described since U46, which was never one of
its lines, and the registry holds eighteen landed `long_running` entries,
seventeen of them in `HANDLERS` and `job.resume` exempt by role. The closing
condition above says the table is empty; read with the exemption the entry
always carried, it is met, and every line this entry ever listed is gone. The
count in the title stays at eighteen for the reason the first correction gives.
U61 is the seventh worked example of the claim: binding the composition needed a
way for a queued favourites job to carry a gate run its own resume can load,
because the dispatcher refuses a run owned by another verb, which is
`Gates.hand_off` and is R-331's subject.

---

## R-204. The acquisition first caller obligation did not transfer, and why

**Found:** during U46, 2026-09-01, while choosing which verb to bind.

R-198 recorded that `download.acquire_paced`, `adapter.dispatch_invocation` and
`adapter.adapter_names` ship with a definition and an export line and no caller,
that `download.acquire_concurrently` is dormant behind `acquire_paced`, and that
the first caller obligation for all four transfers to whoever binds the handler.
Re-run on this branch, `git grep -n` for each still returns definitions, export
lines and docstring mentions only. This unit does not bind `acquire.download`, so
the obligation stays where R-198 left it.

**Why acquisition was not the verb bound.** It is what issue #64 suggested. R-197
records that `AcquireAdapter.fetch` is marked `pragma: no cover`, has never
fetched a file, and dies on its first line because the downloader is constructed
without the events it requires; R-195 records that the adapter never tells the
downloader where ffmpeg is, so a lossless run lands lossy with doctor reporting
green; R-196 records that the provider serves lossy audio to the only login flow
either the vendored tool or the adapter can perform. All three are recorded as
residuals precisely because nothing calls that path. Binding the acquisition
handler makes their input reachable, and under `docs/METHOD.md`'s merge bar a
residual whose reachability a branch creates is blocking on that branch. That is
three critical findings this unit would have had to fix to merge, which is a
different unit.

**What DID transfer, and was discharged.** `master_cli.run_master` had no caller
in `src` either, and binding `master` made this unit its first. Its failure paths
were read rather than assumed and three are now driven end to end through the
queue: `source-missing`, `output-exists`, and `encoder-failed`, the last of which
R-192 records as reachable and undriven. Reading its return value produced two
findings, both fixed: the handler read the recording from the job payload rather
than from the item the driver claimed, which made every item of a multi item job
master the same file, and it carried a check the engine already makes.

**Cost:** `acquire_paced` and the three functions behind it stay shipped and never
driven, and the widest workflow in the product still cannot run.

**Closes when:** a unit binds `acquire.download`'s handler, and takes R-195,
R-196 and R-197 with it.

**Still open after U47, 2026-09-01, and this is stated so the three closures are
not read as satisfying it.** U47 took R-195, R-196 and R-197 and did NOT bind the
handler. That is half of this entry's closing condition, and it is the half that
does not discharge it: `acquire.download` still has no worker, so
`acquire_paced` and the three functions behind it remain shipped and never
driven, and the widest workflow in the product still cannot run.

What did change is the size of what the binding unit inherits. The three findings
that made this unit's own bar unreachable are fixed, so the unit that binds the
handler is making an already-corrected path reachable rather than a broken one.
It still owns whatever it finds, per the doctrine this entry cites.

---

## R-205. No test sees the whole `crate job resume` path in one piece

**Found:** during U46, 2026-09-01, while writing the end to end proof.

The path a person travels is `crate job resume <id>`, which reconciles, retries a
terminal job, and calls `jobs.spawn` with the argv `argv_for` builds. `spawn`
starts that child with `start_new_session=True` and its output goes to a log, so a
test cannot observe the child's effect on the queue as part of the parent's call.

Both halves are proved and the join is not. `tests/test_jobs.py` proves the spawn
happens and carries the built argv; `tests/test_master_cli.py` proves that argv,
re-entered in process, drives the job from `pending` to `done` with the item row
read back from the store. What nothing asserts is that one `crate job resume`
invocation ends with a done item.

**Why it was not fixed here.** Closing it means either waiting on a detached child
from a test, which makes the suite depend on a timeout, or adding a foreground
mode to `spawn`, which is a change to the KTD26 seam made for a test's benefit.
Neither belongs to the unit that binds the first handler.

**Cost:** a defect that lives only in the join, such as `argv_for` building a
command line the verb no longer accepts, would pass this suite.
`tests/test_queued_resume_contract.py` narrows it: it feeds the real `argv_for`
output back through the real dispatcher for every gated queued verb. The uncovered
strip is exactly the process boundary.

**Closes when:** one test drives `crate job resume` and then reads a done item
from the store, or the seam grows a foreground mode a test can call.

---

## R-206. The mastering handler's staging directory is never removed once the job succeeds

**Found:** during U46, 2026-09-01, by the simplification pass over this unit's own diff.

`master_cli.handle` encodes into
`<destination parent>/.cratekit-master-staging/<job_id>/<ordinal>/` and returns a
`Produced` naming the file inside it. `jobs.commit_artifact` moves the file out
with `os.replace` and nothing removes the directory. So every mastered recording
leaves one empty hidden directory tree beside itself, for ever.

**Measured cost, and it is two different sizes.** After a job that SUCCEEDS the
leftover is an empty hidden directory tree, which is untidiness and nothing else.
After a job that is killed and then abandoned rather than resumed, the leftover is
that attempt's partial encode, and a mastered set is measured in gigabytes. The
second case is the one worth the entry. Nothing is lost and nothing is misreported
either way, and the directory is dot prefixed so it does not appear in an ordinary
listing, which is also why nobody would find it. Recorded as a residual rather than
held as a finding because it was not driven to a named user facing cost of the kind
the merge bar asks for: no test fills a disk.

**Why the obvious fix is not obvious.** The handler cannot do it: it returns
BEFORE the commit, so at the moment it could delete the directory the file is
still in it. Cleaning the whole staging root instead is not safe, because two jobs
can drive concurrently under different driver locks and both can write into one
destination folder, so a sweep of the root would delete another job's in flight
encode. Cleaning only this job's earlier ordinals is safe and is a half measure: it
leaves the last item's directory behind and adds a second place that reasons about
the layout.

**Closes when:** the commit side removes an emptied staging directory, which puts
the decision with the code that knows the file has moved, or the engine grows a
staged-output mode that needs no directory of its own. Either remedy has to reclaim
an ABANDONED job's tree as well, which the commit side never reaches, so the
abandoned case probably wants a sweep somewhere a person can invoke.

---

## R-207. A signal during a foreground resume is recorded as an item failure, not an interrupt

**Found:** during U46's adversarial review, 2026-09-01. Reasoned from the source
rather than driven, which is why it is here.

`jobs.drive` checks its interrupt flag between items and again before a commit,
and both checks sit AFTER the two `except` arms that handle a raising handler. A
signal delivered while a handler is running therefore reaches the handler's own
subprocess first: `mastering.subprocess_runner` does not start a new session, so a
Ctrl-C at the terminal goes to ffmpeg too, the encode dies, and the handler raises
`encoder-failed`. `drive` records that as the ITEM's cause and moves on, so the
row says the encoder failed when what happened is that a person pressed Ctrl-C.

**Why it is a residual rather than a finding.** Both remedies are edits to
`jobs.drive` or to the engine's subprocess launch, and neither belongs to the unit
that adds the first caller: the loop's shape is the contract this unit was told not
to reimplement or amend. It was also not driven. `tests/test_job_seam.py` kills
with SIGKILL, which by construction can never reach an interrupt checkpoint, so no
test in this repository has ever delivered a real SIGINT to a driver running a real
handler. Under the merge bar that is condition 1 failing, and "it was not driven"
is the honest reason rather than a severity judgment.

**Newly reachable, and that is why it is recorded now.** Before this unit no verb
called `drive`, so no person could be inside it to interrupt.

**Cost:** an interrupted master is reported as an encoder failure with the
encoder's remediation, which sends a person to check their ffmpeg install for
something they did themselves. The item is resumable either way.

**Closes when:** `drive` consults the interrupt flag before treating a handler
exception as an item failure, and a test delivers a real SIGINT to a driver
running a real handler.

---

## R-208. Two jobs mastering one recording race on an archive slot the job id does not scope

**Found:** during U46's adversarial review, 2026-09-01. Reasoned from the source.

The staging directory this unit adds is scoped by job id and item ordinal, so two
drivers cannot collide there. `mastering.archive_source` is not: it copies the
source to `<source parent>/<ARCHIVE_DIRNAME>/<source name>` and verifies the copy's
digest, and that path is a function of the recording alone. Two jobs queued for one
recording can be driven concurrently under two different driver locks, and both
will write that one slot.

**Why it is a residual.** The fix is in the engine, `archive_source`, which would
have to publish atomically the way `config.atomic_write_bytes` already does in this
repository: copy to a sibling temporary name, verify, then `os.replace`. That is an
engine change on a branch whose diff is otherwise a new seam. It was also not
driven: nothing in the suite runs two drivers over one recording.

**Cost, bounded honestly.** The archive is a copy of a source that is never
modified, and each writer writes the same bytes, so the realistic outcome is
wasted work rather than a corrupt archive. The bad case is a reader that sees a
partially written copy and fails its digest verification, which refuses the run
rather than losing anything.

**Closes when:** `archive_source` publishes atomically, and a test drives two
concurrent jobs over one recording.

---

## R-209. A crash between the artifact commit and the row flip strands a master behind output-exists

**Found:** during U46's review, 2026-09-01.

`jobs.drive` commits an artifact and then flips the item's row to done, in that
order and deliberately: a row that flips first and a machine that dies second
would claim an artifact that does not exist. The window on the other side is real
too. A crash between `commit_artifact` returning and `complete_item` committing
leaves the mastered file at its destination and the item still claimed. The next
resume redoes that item, `master_cli.handle` finds the destination occupied, and
refuses `output-exists`, telling the person that replacing it would discard a
master they may have kept, when the file is this job's own completed work.

**Why it is a residual.** Closing it needs the queue to know which job produced a
given final path, which nothing records. The remedies are a provenance marker
written atomically with the rename, or a wider transaction across the commit and
the row flip, and both are changes to `core/jobs.py`'s ordering contract rather
than to this unit's handler. It was not driven: no test kills a process inside
that window.

**Cost:** the person is told something false about a file, and must pass
`--overwrite` or move the file to finish a job that had already done the work.
Nothing is lost. The window is one `os.replace` plus one sqlite commit wide.

**Closes when:** a resumed item can tell its own completed output from a file
somebody kept, and a test kills a driver inside that window.

---

## R-210. The attended smoke test U47 could not run, and the control it needs

**Found:** during U47, 2026-09-01, as the thing that unit could not prove.

U47 fixed the whole chain offline. Every guard it added is driven by the battery
and none of them needs an account. What no offline test can show is that a real
PKCE session, against the real provider, actually downloads a real FLAC through
the shipped adapter. That needs Phillip's credentials, a browser, and a network,
and it was explicitly not this unit's to attempt.

**What is unproven, stated plainly.** That `login_pkce` completes against the
live provider through the patched vendored login. That the minted token survives
the two-command hop into the keychain and is accepted by `login_mode`. That
`login_token(do_pkce=True)` refreshes against the PKCE client rather than the
device-flow one. That the provider serves LOSSLESS to that session. That the
downloader, given the seven arguments and the ffmpeg path, lands a FLAC. And that
the landed file carries no tempo tag, which is R17's only end-to-end check.

**The control this check must include, and why it is not optional.** The
diagnosis that lossless is gated behind the PKCE CLIENT rests on the A1 session
of 2026-08-28, which compared two aged persisted device-flow tokens against a
freshly minted PKCE one. That varies token vintage alongside the client. If the
real gate is vintage or refresh state rather than client type, a PKCE session
still lands a FLAC, this check still passes, and R-196 will have foreclosed a
device-flow path that would have worked. So the attended run must also mint a
FRESH device-flow session on the same account and track and record whether it is
served lossy. It is one extra step in the same sitting, and it cannot be
recovered once the device flow is gone from the tree.

**Cost:** the product's central promise is proven by construction and not by
observation. Every guard is pinned; the thing the guards are about is not.

**Closes when:** an attended run records both observations, the PKCE landing with
no tempo tag and the fresh device-flow control.

**CLOSED 2026-09-16, both observations recorded, in the attended U29 sitting.**
The PKCE session minted that day through the vendored login survived the two
command hop into the keychain, was accepted by `login_mode`, and refreshed
through `login_token(do_pkce=True)`. The first real download died inside the
tool, because the adapter handed it a function where it calls a logger (#82,
fixed and merged the same sitting). After the fix `acquire download` landed
Tidal track 341726337, Mood II Swing, Chicago Blues, as a 38 MB FLAC, 16 bit,
44.1 kHz, with title, artist, album, ISRC, date and embedded art, and no tempo
or BPM tag in any block. The control ran in the same minute against the same
account and the same track: a device-flow session minted through
`tidalapi.Session.login_oauth` and never persisted was served `HIGH`, codec
`MP4A`, through a BTS manifest, where the PKCE session was served `LOSSLESS`,
codec `FLAC`, through DASH. The gate is the client, not the token's age, and
R-196's decision stands on observation now. The probe script and both answers
are not committed, since they hold nothing a test could re-run without an
account; the numbers here are the record.

---

## R-211. Under `allow_lossy_marked` an unmarked lossy file is still reachable

**Found:** during U47's review, 2026-09-01.

U47's codec check refuses a lossy landing under `strict`. Under
`allow_lossy_marked` it computes the landed file's real codec and then discards
the answer, because `acquire_one` builds the ACQUIRED result's `lossless` from
the provider's OFFER. So a lossless offer that lands lossy is recorded as
lossless with `requires_lossy_marker` False.

**Name it for what it is.** That is an unmarked lossy file in the library, which
`acquire/adapter.py` calls unconstructable by type and `docs/adapters.md`
repeats. The type forbids the combination it can see; it cannot see a file whose
codec nobody read. This is the surviving half of the silent failure R-196
describes, not a classification nicety.

**What bounds it.** `core/config.py` defaults the lossless policy to `strict`,
where the refusal fires and no such result is built. Only an installation that
has deliberately relaxed the policy is exposed.

**Why it is not fixed here.** Closing it means `TrackSource.fetch` returning what
it landed rather than a path, which is a change to the contract in
`acquire/adapter.py` and to both shipped adapters. That is a unit, not a clause
in this one.

**Closes when:** the landed codec reaches the `TrackResult`, so the marker
decision is made from the file rather than from the offer.

---

## R-212. The re-authorisation hop leaves a live refresh token in a plaintext file

**Found:** during U47's review, 2026-09-01.

R-196's closure makes every existing installation re-authorise, and the procedure
`docs/adapters.md` now documents is three steps: mint through the vendored login,
which writes the tool's own `token.json`; copy it into the keychain with `crate
login provider-session --from-file`; erase the original.

Step three is documented and nothing enforces it. `crate login --from-file`
copies the file, it does not consume it, so a user who stops after step two has a
live refresh token sitting in `~/.config/tidal-dl-ng/token.json` indefinitely.
`provider_session.py` argues in its own docstring that a `0600` file inside a
directory nobody checked is not protected, and promises that between invocations
there is no provider token on disk. During this hop that promise is false.

**Cost, bounded honestly.** One file, on the user's own machine, created by an
attended act they performed deliberately, and the documented procedure tells them
to remove it. It is a gap between a documented step and an enforced one, not an
unannounced leak.

**Closes when:** the ingest erases its source, or doctor reports a provider token
found on disk outside a live invocation.

---

## R-213. The alternative adapter never reads the file it landed

**Found:** during U47's code review, 2026-09-01.

U47 put the codec check in `vendored.landed_file`, so the vendored adapter
refuses a landing whose codec is not lossless under a strict policy.
`streamrip.py` has no equivalent. Its `fetch` returns the path its client
reports and nothing reads the bytes, so the alternative adapter still answers the
losslessness question from the provider's OFFER alone, which is precisely the
arrangement R-196 records as having failed silently since July.

**Why this matters more than a missing feature.** `acquire/adapter.py` exists so
the two adapters are substitutable, and `docs/adapters.md` now describes the
codec check as though it were a property of acquisition. It is a property of one
adapter. Someone who switches adapters because the vendored one broke, which is
the exact scenario the contract was written for, silently loses the guard at the
same moment.

**Why it is not fixed here.** The probe would have to move somewhere both
adapters can reach and `streamrip`'s own quality vocabulary would have to be
mapped onto it, and this unit's scope was the vendored path. Widening it without
being able to drive the alternative, whose tool is not installed on this machine,
would be a fix measured on a fixture.

**Cost:** one of two shipped adapters enforces the product's central promise at
the file. The contract's docstring now says which, so the gap is visible rather
than assumed away.

**Closes when:** the codec probe is reachable from both adapters and the
conformance suite drives a lossy landing through each.

---

## R-214. Nothing drives the adapter's own login refusal

**Found:** during U47's code review, 2026-09-01.

`login_mode` is a pure function and is tested exhaustively. The line that CALLS
it, in `_VendoredSource.authenticate`, is not driven by anything. Every test in
the suite injects `session=`, which returns from `authenticate` before the
vendored classes are constructed, so the refusal's wiring is proven only by the
pure function plus an AST assertion that `do_pkce=True` appears in the source.

**Why it was left.** Reaching that line offline means letting `authenticate`
construct the vendored `Tidal`, and `Tidal.__init__` reads `path_file_token()`,
the real user's `~/.config/tidal-dl-ng/token.json`, before the adapter overrides
`file_path`. `conftest.py` redirects Cratekit's own state roots and not that one,
so a test driving this path would read, and on a bad day rewrite, a real
credential file. `Tidal` is also a `SingletonMeta`, so the first construction in
a process wins. Writing the test without first isolating the vendored tool's
config directory would trade a coverage gap for a test that touches a live token.

**Cost:** two lines of wiring between a proven decision and a proven refusal are
unproven. A refactor that dropped the `login_mode` call while keeping the
function would pass the whole battery.

**Closes when:** the vendored tool's config directory is redirected in
`conftest.py`, and a test drives `authenticate` against a device-flow token file
with no session injected.

---

## R-215. An abort cannot reach a download that is already running

**Found:** during U47's code review, 2026-09-01.

`fetch` builds a fresh `event_abort` per call and drops it. Nothing outside that
call holds a reference, so nothing can set it. The concurrent driver in
`core` checks its own stop flag between attempts but cannot interrupt an
in-flight `acquire_one`, which means a provider block observed by one worker does
not stop the requests its siblings already started.

**This is not a regression and that is why it is recorded rather than fixed.**
Before U47 the adapter passed no abort event at all and the download crashed on
its first line, so nothing was interruptible then either. What changed is that
downloads now run, which makes an existing gap reachable for the first time.

**Why it is not fixed here.** The fix threads a run-scoped stop event through
`TrackSource.fetch`, which is a signature change to the contract and to both
adapters. The vendored `Download.item()` already declares an `event_stop`
parameter for exactly this, so the shape exists; the plumbing is a unit.

**Cost:** a run that should stop keeps downloading until every in-flight track
finishes. Bounded by the concurrency cap, not by the queue length.

**Closes when:** a run-scoped stop event reaches `Download`, and a test proves an
in-flight fetch observes it.

## R-216. Two verbs a closed unit declared and never landed, and the revoke that is still missing

**Found:** during U49, 2026-09-02, verified against `main` at 32420a9.

U8 closed with `session.ack` and `session.release` declared in
`src/cratekit/cli/registry.py` against `module="cratekit.session.cli"`, carrying
`planned_in="U8"`, and that module never existed. `record_acknowledgment` had no
caller anywhere in `src` or `scripts`, so nothing a person could type produced
the record `assert_backup_acknowledged` demands, and every destructive path in
the product refused: five call sites pass through that gate, in `write/trees.py`,
`deletion/run.py`, `adopt/apply_cli.py`, `core/restore.py` and
`modules/tools/backup.py`. `release_stale_lock` was in the same state, so a lock
left by an installation that is gone could only be cleared by editing a file.

**The suite was green for eleven units and could not see it.** Tests mint
acknowledgments by calling the core function, so every guard resting on that
record was measured in a world where its premise could not fail. That is the
shape
`docs/solutions/workflow-issues/a-guard-safe-only-because-its-subject-is-unimplemented-expires-when-it-lands.md`
names, and `tests/_pending.py` owed nothing against the module, so no countdown
was watching. This is the U45 shape: an engine landed without its shell, and the
remedy was a new unit rather than a reopened one.

**Closed for the session half by U49, 2026-09-02.** `src/cratekit/session/cli.py`
ships both verbs, both markers came off in the commit that created the file, and
a real destructive verb is driven to completion through the dispatcher on an
acknowledgment minted through the CLI.

**The vocals half is still open.** `registry.py` declares `analyze.vocals` and
`metadata.mytags-vocals` with `planned_in="U25"` against
`cratekit.vocals.cli` and `cratekit.write.metadata_cli`. Those are different
module strings, so nothing U49 created expires them, and they belong to the
analysis worker batch.

**And no verb withdraws an acknowledgment.** Board issue #67 described
`session.release` as releasing what `ack` recorded. The registry describes it as
releasing a stale library lock, its gate prompt says "Release the lock held by
another installation?", and `release_stale_lock` is the engine that answers
that, so U49 implemented the registry: the registry is what the dispatcher
reads and the issue is a description of it. The consequence is that a person who
acknowledges and then discovers the backup was bad has no command that takes it
back, and hand editing the state file is the only route until the twelve hour
window lapses.

**Cost:** the session half cost every destructive feature in the product being
unreachable while its suite reported the guards protecting them as tested. What
is left is a missing revoke, bounded by `DEFAULT_ACK_VALIDITY`.

**Closes when:** the vocals markers expire against modules that exist, and
somebody decides whether an early withdrawal is wanted. A withdrawal is a NEW
registry entry with its own name, not a change to `session.release`.

**THE ENGINES UNDER THE VOCALS HALF ARE REAL NOW, U58, 2026-09-08.** The two
verbs are still planned and their markers still stand, by the brief's
decision that they deserve their own unit. What changed underneath: the
vocal pass scores a real level through a decoder at the model's rate, the
calibrate verb writes the vocal cut, and R-277 records what the missing
re-score verb now costs, a track finalized while the model was unavailable
is never scored again. The unit that lands `analyze.vocals` finds its engine
waiting rather than having to fix it first.

## R-217. A recorded gate answer is replayable, so one run id re-mints forever

**Found:** during U49's document review, 2026-09-02, and confirmed against the
landed verb.

`crate session ack` mints on every answering invocation. The decision a person
records with `crate run decide` is written into the run record and nothing
consumes it, `cli/__init__.py` saves that record after a successful handler, and
nothing in `src` prunes `gates.run_dir()`. So `crate --run R session ack` can be
driven again at any later time and each drive restarts the twelve hour window,
with no second deliberate act by anybody.

`DEFAULT_ACK_VALIDITY`'s own docstring is the standard this falls short of: an
unbounded acknowledgment is "a permanent affirmative wearing a timestamp, and
R34 exists to forbid exactly that". The window is what makes the record an
answer about now rather than a setting.

**This is narrower than it was.** U49 also found and fixed a worse form on the
same path: `Gates.require` refused an inline answer to an explicit gate only
while nothing was recorded, so once any decision existed a `-d` flag was
preferred over it and `--run R -d session.ack.backup=acknowledged` minted over a
recorded `abort`. That is fixed and driven. What remains is replay of an answer
the person genuinely gave.

**Cost while it stood:** an actor holding one run id extended the
acknowledgment indefinitely without asking anybody again.

**CLOSED by U49 itself, 2026-09-02, during its own code review.** The entry was
written when the only fix considered was in `Gates.require`, which would have
changed what a recorded answer means for every explicit gate in the product and
was rightly out of one verb's scope. The review found the narrower fix that the
first reading missed: `record_ack` pops its own decision off `ctx.run.decisions`
after the mint returns, and the dispatcher persists that. The authorisation is
therefore single use because THIS VERB decided its own is, which is a property
of what it mints rather than of the gate machinery, and no other gate's
resolution moves. A later drive of the same run refuses `decision-required` and
needs a fresh `crate run decide`.

The record is kept rather than deleted because the reasoning is the transferable
part: **a shared-seam objection to a fix is an objection to that fix, not to the
finding.** The scope argument was sound and the conclusion drawn from it, that
the defect had to be deferred, was wrong, because it was reached without asking
whether the same property could be bought inside the caller.

**Closes when:** closed. Driven by
`tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`,
which asserts the replay refuses and that a fresh deliberate act still works, so
the guard cannot be satisfied by a verb that simply stopped minting.

## R-218. The ages in the refusal and the ages in the record are two reads

**Found:** during U49's document review, 2026-09-02.

`session.ack` reads the published ages before it asks the question, so the
refusal can name what the person is deciding over. `record_acknowledgment` reads
them again through `_shown_ages` when it writes the record. Those are two calls
at two moments in two processes, and nothing bounds the interval between them: a
portion can move from `never-recorded` to backed up, or the reverse, between the
question and the answer.

`ShownAge`'s docstring states the property the record is supposed to have,
"Recorded rather than recomputed, because the question a person answered was
given this, proceed? and re-deriving the number later answers a different
question". The record can therefore attest to a showing that did not happen.

**Both reads answer from one source and that is not the same thing.** Both go
through `backup_facts.ages` and read one file, so they cannot disagree about
where the numbers came from. They can disagree about when.

**Why it is not fixed here.** Carrying the shown ages from the refusing
invocation into the answering one means either putting them in the run record or
passing them to `record_acknowledgment`, and that function deliberately has no
parameter a caller can use to say what a person saw. Changing its signature is
out of U49's scope for the reason the signature exists. A digest over the ages
was considered and rejected: they move with every passing second, so every
recorded answer would be stale before it could be spent.

**Cost:** an acknowledgment's `shown` list is evidence of what the recording
process read, not of what the person read.

**Closes when:** the record carries the ages the refusal displayed, or the
claim in `ShownAge`'s docstring is narrowed to what the code does.

## R-219. The release prompt asserts a holder that may not be there

**Found:** during U49's document review, 2026-09-02.

`session.release.confirm` reads "Release the lock held by another
installation?", and it is asked on every drive including one where the verb has
already established that no lock is recorded. Conformance 3 holds every declared
gate to firing, and skipping the question on the quiet path would make the case
that needs asking least the only one exempt, so the prompt fires over a claim
that does not exist. The refusal does carry the holder it found, or `None`, so
the person is not misled once they read it; the prompt line above it still
asserts something the verb knows is false.

**Why it is not fixed here.** U49's whole discipline was to implement what the
registry declares and change none of it. A unit that lands a declared module and
edits the declaration in the same commit cannot say afterwards which half its
tests were measuring, and a prompt is part of that declaration.

**Cost:** one misleading sentence on a verb's quiet path.

**Closes when:** somebody rewords the declared prompt so it does not assert a
holder, in a commit that changes nothing else about the entry.

## R-220. The actor on a gate decision is caller supplied, and this unit made it load bearing

**Found:** during U49's code review, 2026-09-02, by two reviewers independently.

`crate run decide` takes `--actor` as free text defaulting to `cli`
(`src/cratekit/cli/verbs/runs.py`), and `gates.record` writes whatever it is
handed into the run record as the actor who made the decision. The
acknowledgment file itself is not affected: `record_acknowledgment` has no actor
parameter and derives the account from the process identity, which is R34's
sharpest clause and is intact.

**What changed is what that decision now authorises.** Before U49 no landed verb
reached an explicit gate that minted anything, so the actor on a gate decision
was a label on a record nobody spent. It is now the audit trail for the act that
unlocks every destructive write in the product, and it can say anybody.

**This is pre-existing and the fix is not this unit's to make.** Deriving the
actor in `run decide` changes the recorded meaning of every gate answer in the
product, which is the same shared-seam objection R-217 raised and, unlike
R-217, there is no narrower version available inside one verb: the decision is
recorded by a different verb entirely.

**Cost:** the run record can name someone who did not answer. The
acknowledgment record, which is what the destructive gate actually consults,
still names the derived account.

**Closes when:** `run decide` records the derived identity as the actor for an
explicit gate, keeping any supplied string as a separate annotation, and a test
drives an arbitrary `--actor` against `session.ack.backup` and asserts what the
record claims.

## R-221. The queued backup reports its ages and nothing else the run learned

**Found:** during U50, 2026-09-02, while binding the backup worker.

The resume envelope carries `published_ages` and the job report. It does not
carry the per portion `ran` flags, the archive rotation warnings U48 taught the
engine to stop swallowing, or the `dry_run` flag. `perform_backup` builds all
three and `handle` discards the report, because `jobs.drive` keeps only a
handler's `Produced` and a backup produces nothing to commit.

**The `master` symmetry is what this was first argued from, and it does not
carry.** That verb's resume also reports only the job, and the difference is that
its discarded report describes a file the person can go and look at. A backup
leaves nothing local, so the report is the only account of what happened.

**The specific cost is the rehearsal.** `crate backup run --dry-run` queues a job
whose resume drives every portion with each transfer neutralised, and the
envelope for that run is byte for byte the shape of a real one: two items done, a
succeeded job, and ages read from a fact file the rehearsal never touched. The
ages are the same ages the previous real run published, so they are true, and
nothing on the queued path says the run that just finished copied nothing. The
`dry_run` flag exists in the report precisely because a rehearsal and a real run
are otherwise indistinguishable, and the queued path is where it does not reach
anybody.

**Cost:** a rehearsal driven through the queue reads as a backup. The rotation
warnings reach nobody on the queued path.

**Closes when:** the resume envelope carries the outcome the worker built, which
needs a way for a handler to return a report alongside its `Produced`, and a test
drives a queued rehearsal and asserts the envelope says so.

## R-222. A retried portion takes the last rotation slot, and the default keeps one

**Found:** during U50, 2026-09-02, while binding the backup worker.

`DEFAULT_ARCHIVE_KEEP` is 1. Each item builds its own plan at claim time, so each
attempt at a portion stamps its own dated archive folder, and the prune that runs
after a successful mirror keeps one. So a mirror that failed partway, wrote its
archive folder, and is then retried to success deletes that folder: the versions
the failed attempt overwrote before it died have their only remaining copies
there.

**This unit is what makes it reachable.** Nothing in `src` drove a backup before
today, so no attempt could be retried. R11's per portion retry is the point of
the item ledger, and it is also the first thing that can create two dated folders
for one portion.

**Not fixed here.** Freezing one archive stamp per item and reusing it across
attempts is the fix, and the stamp is decided inside `plan_backup`, which is
board unit U45's file and is out of this unit's scope. The narrower version, a
stamp frozen into the payload at enqueue time, was considered and rejected on its
own merits: a resume days later would then write into a folder dated for the day
the job was queued.

**Cost:** the safety net for one failed attempt is deleted by the attempt that
succeeds. Only files the failed attempt had already overwritten are affected.

**Closes when:** a retried portion reuses its earlier attempt's dated folder, or
the rotation counts attempts of one job as one slot, with a test that fails a
mirror, retries it, and asserts the first attempt's archive is still there.

## R-223. Two backup jobs against one destination, and nothing says no

**Found:** during U50, 2026-09-02, while binding the backup worker.

`crate backup run` queues unconditionally. It prints a job identifier and appears
to have done nothing, which is exactly the shape that invites typing it again, and
the second invocation files a second job. Both can now be driven. Each takes its
own driver lock, which is per job, so the locks do not see each other, and both
run `rclone sync` against the same destination with different dated archive
folders. At a keep of 1 each portion's prune then deletes the other run's archive.

**Not fixed here.** Reporting the open job instead of queueing a second is a
change to what the verb does when asked, which is a decision about the verb rather
than about the worker this unit binds. `master` queues the same way and is not
exposed to it, because two masters name two different recordings while two backups
name one destination.

**Cost:** two concurrent backups interleave against one remote and prune each
other's archive.

**Closes when:** `backup_library` reports the open backup job rather than filing a
second, with a test that runs the verb twice and asserts one job.

## R-224. A portion that refuses can only be recorded as failed

**Found:** during U50, 2026-09-02, while reversing this unit's first design.

`ItemState.SKIPPED` is declared and `jobs.progress` counts it as settled, and
nothing produces it: `jobs.drive` completes or fails an item and has no third
branch, `complete_item` writes only `done`, and no writer exists for the state at
all. So a portion the engine refused before attempting anything, which is neither
a completed copy nor a transfer that came back non zero, has to be recorded as one
of the two.

This unit records it as failed, which is the recoverable half of a bad pair:
`jobs.retry` re-arms it, so quitting rekordbox and resuming finishes the backup,
where `done` would be permanent. The cost is that a library backed up without
quitting rekordbox first reports a failed job, which is louder than the whole run
verdict in `refusal_for` calls the same state.

**Not fixed here.** A skip path is `core/jobs.py`: a writer, a rule in `drive`
about what a skipped item does to the job's verdict, and a decision about whether
`retry` re-arms one. That is the engine, and this unit is a caller of it.

**Cost:** the ordinary "backed up with rekordbox open" run reports failure rather
than a partial success, and the item ledger cannot distinguish a portion that was
skipped from one whose transfer broke.

**Closes when:** a handler can record an item as skipped, `drive` says what a
skipped item does to the job's state, and this verb uses it for a refusal.

## R-225. A resume that half failed exits OK for every verb except backup

**Found:** during U50, 2026-09-02, by driving the seam rather than reading it.

`jobs.drive` raises only when every attempted item failed. A job where one item
completed and another did not returns a `DriveResult` normally with the job
recorded FAILED, so a resume branch that reports the job and returns its envelope
exits 0 over a run that half failed. Measured on this branch: a backup whose
mirror completed and whose database snapshot came back non zero exited
`ExitCode.OK` with the job state reading `failed` in the same envelope.

U50 fixes it for `backup.run` by re-raising the job's own cause, and
`src/cratekit/master/cli.py` still has it. `master` is the only other bound verb,
so the exposure is exactly one verb, and it will be inherited by every verb bound
against R-203 that copies the same resume branch.

**Not fixed here.** `master/cli.py` is board unit U46's file and changing another
verb's exit code from this unit is a second opinion about a surface this unit does
not own.

**Cost:** `crate master --job ID` exits 0 over a mastering job that failed. A
script reading the exit code stops looking.

**Closes when:** the resume branch that raises on a closed failed job lives in one
place both verbs reach, or `master` grows the same three lines, with a test
driving a partially failed job through each bound verb and asserting the exit
code.

---

## R-226. No streaming provider adapter ships, so both outbound workers end at the seam

**Found:** during U51, 2026-09-02, by binding the two handlers.

`export.playlist` and `sync.favorites` now queue real items and a driver runs
them. On any machine this build ships to, every one of those items ends at
`modules/outbound/account.resolve`, which raises `credential-missing` when no
provider session is stored and `outbound-account-unbound` when one is: no
implementation of `modules/outbound/service.RemoteAccount` exists anywhere in
`src`, verified by grep as a definition, two imports and four parameter
annotations.

**Measured cost.** Nothing is written to any account, and nothing is lost. What a
person gets is a job that ends FAILED with a named cause instead of one that sits
pending for ever, which is smaller than a working export and is the honest
version of it. The queued envelope carries the warning before they confirm, so
nobody is asked to approve a write this build cannot perform without being told.

**The substitution the tests use does not reach a real run.** A test replaces
`account.resolve` on the module and the workers pick it up because they resolve it
at call time. The child `crate job resume` spawns is a fresh process and inherits
nothing, so there is no supported way to bind an account outside an in process
test until an adapter lands.

**Why not fixed here.** Opening a live streaming account is a standing refusal for
an unattended session, which is the same reason R-144 has stayed open since
2026-08-17.

**Closes when:** an adapter implements `RemoteAccount`, `account.resolve` returns
it, and one real playlist and one real hearts sweep run through these two verbs
against a live account. That is also R-144's closing condition, which this unit
advances and does not claim.

**Agent half CLOSED by U63, 2026-09-16, on `relay/85`.**
`modules.outbound.tidal_account.TidalAccount` implements `RemoteAccount` over a
client `acquire.provider_session.client_session` logs in from the stored session,
`account.resolve` returns it once a session is recorded and holds it for the
process, and `bound()` answers whether that module imports. Driven against a fake
client injected at `provider_session.CLIENT_FACTORY` in
`tests/test_outbound_tidal_account.py`, including a hearts sweep and a playlist
export through the real workers to done with the ledger recording every write.
**Those two drives give the rows an ISRC by substitution, and the shipped rows
carry none, which is R-355: a live sweep today matches nothing.** The live half
stays open with R-144, recorded in `docs/cutover.md`. `outbound-account-unbound`
survives only for a build whose adapter does not import.

---

## R-227. The library both outbound verbs read is an export the operator makes by hand

**Found:** during U51, 2026-09-02, as the cost of KTD1.

Neither verb can see the live rekordbox database: it is off limits outside the
backup feature, and no collection reader against it has landed, which is the
reason R-203 gives for `adopt.scan` being unbound too. So both verbs take
`--export PATH` and read a rekordbox collection export through
`modules/reports/export.read_export_file`.

**Measured cost, and it is an operator cost rather than a data one.** The source
system's favourites sweep reads the database and runs as one command. Here the
operator opens rekordbox, exports the collection, and then types the verb, so the
path to a sweep is one manual step longer than the thing it replaces. A sweep is
also only as fresh as that export, and NOTHING WARNS WHEN IT IS STALE: an export
taken last month resolves, queues, and writes, and the run reports success over a
library that has moved.

**No configured default export path is offered**, deliberately, for the reason
`cli/reports.py` already gives about its own positional argument: a default makes
a stale document the silent answer to every question, and a report that is
confidently wrong is worse than one that refuses.

**Closes when:** a collection reader against the live database lands, or the
verbs learn to refuse an export older than some declared age.

---

## R-228. A pink row outside the named playlist is not swept

**Found:** during U51, 2026-09-02.

`modules/outbound/hearts.py` opens by describing its input as "pink local
favourites", and in the source system pink is the operator's standing signal that
a row should be hearted. `sync.favorites` cannot see pink. A rekordbox collection
export's `CollectionEntry` carries `track_id`, `name`, `artist`, `location` and
playlist membership, and no colour, so the verb sweeps membership of a named
playlist instead, defaulting to `All Favorites`.

**Measured cost.** A row the operator coloured pink by hand, and which is not in
that playlist, is never hearted at the provider. The two populations overlap
heavily in the live library because the forward pass files hearted tracks into
that playlist, which is exactly why this is easy to miss: the sweep looks correct
on every row that arrived through the forward pass and silently omits the ones
the operator marked themselves.

**Why not fixed here.** Carrying the colour would mean adding a field to
`CollectionEntry` in `modules/reports/export.py`, which two report engines and a
golden suite already read, and that is a change to a shared module rather than to
this unit's files.

**Also not driven here:** the local colour and My Tag write the verb's registry
entry still declares. `heart_back` takes a `LocalColors` writer and this shell
passes `None`, because colouring a row is a write to the live database and belongs
behind the guarded write session. R-144 recorded that; it is still true.

**Closes when:** `CollectionEntry` carries the track colour and the derivation
offers pink rows as candidates, or the verb reads the live database inside a
guarded session.

---

## R-229. The ledger key is a display path, so a rekordbox reorganisation forks the remote playlist

**Found:** during U51, 2026-09-02, while choosing what to freeze.

`modules/outbound/ledger` keys a recorded remote playlist on the `playlist_key`
its caller supplies, and this unit supplies the resolved DISPLAY PATH, joined with
`/`. A rekordbox collection export carries no stable playlist identifier, so the
path is the only identifier there is.

**Measured cost.** Rename a crate, or drag it into a folder, and the next export
resolves a different key, finds no record, and creates a SECOND remote playlist
rather than updating the one this library already made. Nothing warns. The first
playlist stays on the account holding the tracks it had, and the person now has
two playlists for one crate and has to work out which is current.

**Why not fixed here.** The fixes all need something the format does not have. A
content based key would fork on the first track added; matching the remote
playlist by name would adopt a playlist somebody else made; asking the person is a
gate this verb does not have a shape for.

**Closes when:** the ledger records enough to recognise a renamed crate, or the
verb offers to adopt a recorded remote playlist whose key no longer resolves.

---

## R-230. One ledger rewrite per track, and one remote listing per track

**Found:** during U51, 2026-09-02, by the efficiency pass over the binding.

An item is one track, which is what makes the engine's resume guarantee worth
anything and what makes the zero item rule enforceable. The cost is that
`modules/outbound/export.apply` runs once per track, and each call takes the
ledger lock, reads the whole JSON document, writes it back, and asks the account
to list the remote playlist's current contents.

**Measured cost, reasoned rather than driven.** A five hundred track export
performs five hundred lock, read, serialize and write cycles against a document
whose `added` array is growing, so the bytes moved are quadratic in the playlist
length, plus five hundred remote listing calls against a rate limited service. No
export of that size has run, because no adapter ships, so this is a shape rather
than a measurement.

**Why not fixed here.** The fix is a job scoped ledger session that holds one lock
across the item loop, which changes the engine's transaction boundary and would
need its own unit. Making the per item shape cheaper by batching items would
undo the two properties it exists for.

**Closes when:** the ledger offers a session a driver can hold across a job's
items, and `apply` reads the remote playlist's contents once per job.

---

## R-231. A create the ledger cannot record still orphans one remote playlist

**Found:** during U51, 2026-09-02, by the review, and fixed to the point the
window is narrow rather than closed.

`export.apply` used to read the recorded remote id without a lock, create a
playlist when there was none, and only then take the lock to record it. A ledger
that could not be locked or written failed at that last step with a playlist
already made and nothing remembering it, and under the per item shape EVERY
SUBSEQUENT ITEM created another one. Driven during this unit's review against a
state directory the account could not write: one three track export produced
three remote playlists.

`ledger.reserve_playlist` now takes the lock BEFORE the create, so an unwritable
ledger refuses `outbound-ledger-unusable` with the account untouched, which is
the driven case and is closed.

**What remains.** The lock is held and the write itself then fails, from a full
disk or a device error between `_locked` and `_write`. One remote playlist is
orphaned and unrecorded, and the next attempt makes another.

**Measured cost of the remainder.** Undriven. It needs an I/O failure in the
window between acquiring a lock file and completing an atomic write to the same
directory, which this unit could not produce.

**Why not fixed here.** Closing it needs a create the provider itself can make
idempotent, or a two phase record that writes an intent before the create and
resolves it after. The first depends on an adapter that does not exist; the second
is a ledger format change.

**Closes when:** a create that cannot be recorded leaves something the next
attempt can find, or the provider offers a create keyed on a caller supplied
identifier.

---

## R-232. Four copies of the same config-unusable wrapper

**Found:** during U51, 2026-09-02, by the simplification pass.

`modules/outbound/shell.load_config` wraps `config.ConfigError` into a
`config-unusable` cause with the shell's own origin. `master/cli.py`,
`backup/cli.py` and this one are the same thirteen lines differing only in the
origin tuple. U51 removed two of the copies by giving the two outbound verbs one;
two remain.

**Measured cost.** None to a library. The cost is that a change to how an unusable
configuration is reported has to be made in three places, and the copy that is
missed reports it differently.

**Why not fixed here.** The shared home for all four is `core.config`, and both
remaining copies live in other units' files.

**Closes when:** one function owns the wrap and every shell asks it.

---

## R-233. Two verbs declare write surfaces their workers cannot reach

**Found:** during U51, 2026-09-02, by the review of the registry declarations.

`sync.favorites` declares `writes={"db_tree", "db_metadata", "xml", "files",
"remote"}` and the doctor checks `rekordbox.closed` and `rekordbox.pins`. Its
shipped worker writes the remote account and a JSON artifact under the queue root
and nothing else, because the local colour write is R-228.

**Measured cost. NONE, and it was measured rather than assumed.** `entry.writes`
and `entry.destructive` are read nowhere in `src` outside `registry.py`, and
`doctor.requires_check` is an `any()` across every entry, so `rekordbox.closed` is
already required by `adopt.apply`, `rebuild`, `restore.run` and the routing verbs
in every profile. No health report changes and no gate changes.

**Why not fixed here.** Narrowing `writes` also drops the obligation to declare
the cloud sync gate and lets `destructive` fall to False, which is a judgement
about whether a remote only write should hold the library lock. That judgement
belongs with the unit that lands the local colour write, since it will need the
declarations back.

**Closes when:** the local colour write lands and the declaration is true again,
or the entry is narrowed with the destructive question answered.

---

## R-234. `adopt.apply`'s declined payload fails its own declared schema

**Found:** during U51, 2026-09-02, while fixing the same defect in two other verbs.

`cli/output` closes each declared payload surface with `additionalProperties:
false` and requires every field. `adopt.apply`'s abort branch returns
`{"job_id": None, "state": "declined", "cause": None, "progress": {}}`, and
`payload_problems` reports `'job_id' should be string, got NoneType` for it. The
same branch in the two outbound verbs carried a different violation and is fixed
in this unit.

**Measured cost.** A consumer generated from `tests/schemas/job_state.v1.json`
rejects the envelope `crate adopt apply` emits when somebody declines the
confirmation. Nothing in the product reads it that way today, so the cost is to a
consumer that does not exist yet.

**Nothing validated it, which is why it shipped.** The schema fingerprint hashes
the DECLARED fields rather than an emitted payload, and the golden envelope is a
hand written literal. `tests/cli_drive.drive` now validates every envelope the
suites that use it drive, which is what caught the outbound instances; the adopt
verb is not driven through that helper.

**Why not fixed here.** It is U23's file and this unit does not own its surface.

**Closes when:** the branch emits `""` rather than `None`, or the verb is driven
through a helper that validates its envelope.

**CLOSED by U55, 2026-09-02, in both halves.** `apply_adoption`'s abort branch
emits `""`, and the verb is now driven through `tests/cli_drive.drive`, which
validates every envelope it returns. The same shape is used for the two new no-op
payloads on `adopt.scan` and on an apply whose plan has nothing applicable, so the
verb's other zero paths cannot reintroduce it.


---

## R-235. Adoption cannot write membership on a library nobody has cut over, and no verb can cut one over

**Found:** during U55, 2026-09-02, by driving the apply worker against a library
whose taxonomy tree the registry has no record for.

This is R-148's successor and it is narrower. R-148 said adoption's memberships
were collected and never written, for two reasons: sessions do not nest, and no
unit landed a collection reader. Both are discharged. The reader landed, and the
membership write happens in a second session opened after the apply loop's has
closed, which is exactly the shape R-148's closing condition asked for.

**What replaces it.** `cratekit.write.trees.write_tree_membership` calls
`tree_registry.anchored_root`, which refuses a tree still on the bridge, and
`Registry.mode` returns `Mode.XML` for a tree with no record at all, so an
unrecorded tree IS on the bridge. Nothing under `src` calls
`tree_registry.record_cutover` or `tree_registry.flip`: measured by grep on
2026-09-02, every reference outside `core/tree_registry.py` itself is in a test.
So no shipped verb can move a library into the mode the write requires, and the
refusal a person meets names a remedy nobody can perform.

**Measured cost.** `crate adopt apply` on any real library queues, drives, refuses
`tree-unconverged` on its one item, and ends FAILED. Nothing is marked in the
applied ledger, nothing is written to the database, and no file is touched, so
the run costs a snapshot capture and time. The person is told the tree has not
been cut over, which is true and is not something they can act on today.
`tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable`
drives it.

**Why not fixed here.** The cutover is U29, which is attended and requires the
live library. The alternative, an XML bridge membership writer so adoption can
serve a pre-cutover library through the document rekordbox imports, is a second
writer over `cratekit.write.rbxml` and its own unit.

**Closes when:** a shipped verb can record a cutover, or adoption gains a bridge
membership writer for the pre-cutover case.

---

## R-236. `membership_plan` groups content identifiers and its consumer decodes locations

**Found:** during U55, 2026-09-02, while wiring the first caller that hands one to
the other.

`cratekit.adopt.apply.membership_plan` groups `entry.content_id` per destination.
`cratekit.write.trees.write_tree_membership` passes every value of its `plan`
through `match_indexed_rows`, which decodes each one as a recorded LOCATION and
looks it up in an index keyed on resolved paths. A content identifier decodes to
nothing, so every entry comes back `UNRESOLVED`, `added` stays 0, and
`MembershipReport` reports a session that ran over a write that landed nothing.

`apply_cli._collector`'s docstring asserted the two were one shape, in these
words: "what comes back is the mapping `membership_plan` produces and
`write_tree_membership` consumes". That sentence was false when it was written and
nothing could see it, because no caller had ever handed one to the other.

**Fixed on this side, recorded on the other.** U55's collector groups
`entry.path`, and `apply_cli.membership_locations` is `membership_plan` with the
location where that function has the identifier. `membership_plan` itself is
untouched: it is `cratekit/adopt/apply.py`'s function with its own contract, and
changing what it groups from a command-line module would be a second opinion
about a surface U55 does not own.

**Measured cost.** None today, and the reason is that the only caller is now
correct. `membership_plan` has no other caller in `src`, measured by grep on
2026-09-02. The cost is to the next author who reaches for it expecting the
mapping the tree writer takes, and to a reader of its docstring, which still says
it produces "the mapping both tree writers take".

`tests/test_adopt_workers.py::test_the_membership_write_needs_locations_and_not_content_identifiers`
drives both directions against a real index, so this entry is a measurement rather
than a reading of the source.

**Closes when:** `membership_plan` either takes the location or says in its own
docstring which consumer it is for.

---

## R-237. An applied ledger record cannot say what the apply actually wrote

**Found:** during U55, 2026-09-02, by the review of what the no-tag decision costs.

`cratekit.adopt.apply.outstanding` computes a run's work as `plan.applicable()`
minus the entry identifiers the applied ledger holds, and `entry_id` folds the
tree, the content identifier, the bucket and the sub. It folds nothing about what
was written.

U55's apply writes a membership row and NO tag, deliberately: the tag write is
the one act no snapshot undoes, the registry declares no `adopt.revert` verb, and
seven ledger findings against the revert path (R-83, R-84, R-89, R-90, R-91,
R-93, R-94) are unreachable today precisely because nothing writes a tag. So every
entry U55's apply marks is membership-only, and the ledger cannot tell that record
from a fully adopted one.

**Measured cost.** None today, because nothing writes a tag at all. It arrives the
day somebody supplies a `tag_value`: that unit's apply will find nothing
outstanding for any track a previous adoption already placed, so those tracks are
never tagged and nothing reports it. The remedy at that point is a re-derivation
rather than a re-run, which is more expensive than adding the field now.

**Why not fixed here.** The field is a change to the ledger's persisted shape,
which needs a migration for records already written, and the decision about what
it should record belongs with the unit that lands the tag write, since that is the
unit that knows what distinctions matter.

**Closes when:** the applied ledger records what an apply wrote, or a `tag_value`
supplier lands and its unit re-derives rather than resumes.

---

## R-238. One capture per apply job, and the item shape is what bounds it

**Found:** during U55, 2026-09-02, while choosing the apply's item shape.

`cratekit.write.trees.write_tree_membership` runs `snapshot.capture(cfg, db=db)`
followed by `snapshot.assert_verified` inside its own session, and `capture`
copies the whole rekordbox database and its companion files into a new dated
directory. So every membership session is a full copy of the library's database.

U55's apply queues ONE item, the plan, so an apply of any size takes exactly one
capture. `tests/test_adopt_workers.py::test_one_capture_per_apply_job_whatever_the_entry_count`
pins it, which is what stops an item-per-entry shape creeping back later: that
shape would take one full copy of the database per track.

**Measured cost.** The cost recorded here is what the shape gives up rather than
what it spends. A one item job cannot report per track progress, and a kill
partway through is recovered by the applied ledger rather than by the queue, so
`crate job show` says one of one pending for the whole run however many tracks it
is placing. `core/snapshot.py` also does not prune, so a person who runs several
adoptions accumulates one full database copy per run.

**Why not fixed here.** Bounding the capture store is `snapshot`'s decision and
R30 already separates pruning from the write session. Reporting per track progress
without per track items would need a progress surface the job engine does not
have.

**Closes when:** the queue can report progress inside one item, or the capture
store is pruned.

---

## R-239. Three spellings of the encryption probe, and two of them are wrong on a real library

**Found:** during U55, 2026-09-02, while giving the collection reader one.

Whether the database file is encrypted decides the `unlock` argument
`rb_writer.open_db` passes the binding, and a constant answer is wrong in one
direction or the other: `unlock=True` fails against a disposable database a test
just built, `unlock=False` fails against a real library, which is encrypted.

`cratekit.core.rb_writer.unlock_needed` is U55's answer and both of this unit's
opens ask it. Three sites do not:

- `cratekit.deletion.cli._needs_unlock` asks the same question with its own copy,
  reading the first sixteen bytes through `read_bytes`, which pulls the whole
  database into memory to look at fifteen characters, and spelling the bound as a
  bare integer in a module that also names causes, which widens the surface
  `tests/test_reserved_causes.py` watches.
- `cratekit.write.routing_cli` and `cratekit.cli.converge` both pass
  `unlock=False` unconditionally. On a real encrypted library both fail to open.

**Measured cost.** Unmeasured on a real library, and said that way rather than
claimed either direction: this branch drove no encrypted database, because the
live one is off limits and no supplied snapshot was present for this run. What is
measured is that the two `unlock=False` sites cannot supply a key, and
`open_db`'s docstring says plainly that "the live database is encrypted and
reading it with the key off simply fails".

**Why not fixed here.** All three are other units' verbs, and changing what a
shipped destructive verb does on an encrypted database is a decision this unit
does not own. Rewiring them would also pull `delete.review` into a diff no test in
U55 covers.

**Closes when:** one function answers the question and every open asks it.

**The mutation table measured the gap rather than arguing it.** Two rows in
`docs/mutation/u55-collection-reader.md` make the probe answer "not encrypted",
and both read ZERO in two rounds. Every database in this suite is a disposable
one built from the binding's own schema and none of them is encrypted, so the
correct answer and the mutated one agree on every input the suite has. Supplying
`CRATEKIT_TEST_DB` pointing at a real snapshot is what would give those rows an
input; this run had none.

---

## R-240. A second copy of the job artifact helper, differing only in two directory names

**Found:** during U55, 2026-09-02, when the adopt workers needed one.

`cratekit.adopt.artifacts` and `cratekit.modules.outbound.artifacts` are the same
five functions. Everything in either one is generic to the job engine: stage under
the queue root, commit through `jobs.commit_artifact`, read the committed reports
back in item order, resolve the root from the FROZEN configuration rather than
from `jobs.store_dir()` with no argument. The only difference is the two directory
names, `adopt-artifacts` and `adopt-staging` against `outbound-artifacts` and
`outbound-staging`.

**Measured cost.** None to a library. The cost is that the ordering rule the
module exists to enforce, that an artifact is durable before the item's row flips
to done, now has two homes, and the copy that is missed enforces it differently.
The frozen-configuration rule has the same shape and the same exposure.

**Why not fixed here.** The honest home is one module in `core` taking the two
names as arguments, and moving the outbound one there is a change to U51's file.

**Closes when:** one module owns the staging and commit pair and both feature
packages name their own directories through it.

---

## R-241. A fifth copy of the prefix map comprehension

**Found:** during U55, 2026-09-02, by counting before adding one.

`[locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()]`
now appears in `write/routing_pass.py`, `write/rebuild.py`, `write/trees.py`,
`deletion/run.py` and `adopt/collection.py`.

**Measured cost.** None. Every copy is one line and they agree. The cost is that
a change to how a configured prefix becomes a resolver rule has to be made in five
places, and the copy that is missed resolves a person's older volume name
differently from the other four, which is the S1 failure the map exists to
prevent.

**Why not fixed here.** The shared home is `core.locations` and four of the five
copies are in other units' files.

**Closes when:** one function builds the rules and every caller asks it.

---

## R-242. The reconcile guard on `adopt.apply` weakened when its branch started driving

**Found:** during U55, 2026-09-02, while repairing the suite the new worker broke.

`test_a_resume_reconciles_a_claim_a_dead_driver_left_behind` put a job into
RUNNING with no driver holding the lock and asserted the resume reported QUEUED,
which is what `jobs.reconcile` derives and what `jobs.get` would not. That
assertion was sharp precisely because nothing ran: the reported state was the last
thing the branch touched.

The branch now drives. `jobs.drive` releases orphaned claims itself, and a RUNNING
job with no claim drives to a terminal state under either spelling, so swapping
`reconcile` for `get` in that branch may no longer kill this test. The test now
asserts the terminal state and the item's own state instead, which is true and is
weaker.

**Measured cost.** None to a library. The cost is to the next mutation table: a
row reverting the reconcile call in `adopt/apply_cli._resume` may read zero and be
dismissed as an inert mutation when it is a real gap. Recorded so the zero has an
explanation attached to it in advance.

**Why not fixed here.** The property needs an observation between the reconcile
and the drive, which means either a seam this module does not have or a test that
reaches inside the branch.

**Closes when:** the resume branch's reconcile has a driven observation of its own.

---

## R-243. The apply's write intent open is half covered by the session below it

**Found:** during U55, 2026-09-02, by the mutation table refusing to die.

`apply_cli._write_memberships` opens its handle with `require_closed=True`, which
is the open a write is supposed to make. Reverting that flag to False killed ZERO
tests in both rounds, including after a test driving the two-process refusal was
added and passing.

**The reason is the one `docs/METHOD.md` names.** A guard covered by another
guard is a guard nothing covers. `require_closed=True` does two things at the
open, and the two-process refusal is asserted a second time inside the session:
`core/session.py:1820` asserts rekordbox closed before it verifies a commit. So
reverting the flag still refuses, just from one layer down and with the database
already open.

**What the flag holds ALONE is the application pin**, and that half is now
covered. `assert_app_version` runs only inside `open_db`'s `require_closed`
branch, and nothing else on the membership path asks it, so a rekordbox that has
updated itself since the pin was recorded would reach the commit with the flag
off. `test_the_application_pin_is_what_the_write_intent_open_uniquely_holds`
drives that refusal directly. It was written after round two measured the row, so
the zero stands as measured and the composite is what says what the flag is for.

**Measured cost.** None. The refusal a person meets is the same refusal either
way; what differs is how far the run gets before meeting it, and with the flag on
it is before anything opens.

**Why not fixed here.** There is nothing to fix in this unit. What would close it
is deciding whether the duplicated two-process assertion belongs at the open, in
the session, or in both deliberately, and `core/session.py` is another unit's
file.

**Closes when:** the two-process refusal has one owner, or the duplication is
stated at both ends as deliberate.

---

## R-244. An apply retry overwrites the artifact that recorded which entries failed

**Found:** during U55's code review, 2026-09-02, reasoned from the artifact paths
rather than driven.

An apply is one item, so its artifact is always ordinal zero, and
`artifacts.staged_path` clears the staging directory on every attempt. A second
attempt therefore replaces the committed report of the first. The summary
`crate adopt apply` reports is read back from that one file, so it describes the
LAST attempt rather than the job.

**Measured cost.** None to a library: the applied ledger, not the artifact, is
what decides what a re-run does, and it is append only. The cost is to a person
reading the report after a partial failure, who sees the second attempt's
entries and not the first's, and to anybody diagnosing why an adoption took two
runs.

**Why not fixed here.** The fix is either an ordinal per attempt, which
`jobs.Item` does not carry, or folding `already_applied` into the reported set,
which changes what the envelope's `applied` field means. Both are decisions about
the reporting surface rather than about this unit's writes.

**Closes when:** an apply's report survives its own retry, or the envelope is
explicit that it describes one attempt.

---

## R-245. No catalogue page shape was verified against a live site, and no gate here can be

**Found by** U56 while landing the searcher, 2026-09-03.

`cratekit.tagging.searchers` parses Beatport's `__NEXT_DATA__` payload,
Traxsource's track rows and Bandcamp's search listing and track tags. Every
shape was read from `DJ_tools/src/dj_tools/DJ_tagging/scrape.py`, whose own last
verified run against those sites is undated. No request left this machine during
the unit, because a live catalogue call is attended and out of scope, and every
test feeds synthetic page text through the injected fetch seam.

**Measured cost.** The battery proves the SHAPE of the searcher and cannot prove
it returns a real hit. A wholly broken parser and a working one produce the same
green suite, so `crate tag folder` could ship tagging nothing and the first
person to learn it would be the person whose folder came back untagged. The
design bounds the damage rather than the risk: a page that parses to nothing
recognizable is `catalogue-parse-broken`, whose remedy names the parser rather
than the network, so the failure at least says what it is.

**Why it is not fixed here.** A live call is attended by standing constraint.
An agent can prepare for it and cannot perform it.

**Closes when:** one lookup per source has been run against the live site with
its result recorded, or the captured pages are shipped as dated fixtures so a
later reader can tell how old the shape evidence is.

---

## R-246. The retag's database half still has no caller, while the registry says it writes one

**Found by** U56 while binding `tag.retag`, 2026-09-03. Driven.

`retag.plan_library` and `retag.apply_library` have exactly one file naming them
after this unit, their own module. The worker corrects the file on disk and
nothing plans the `GenreID` write. `registry.ENTRIES` declares `tag.retag` as
`writes=frozenset({"files", "db_metadata"})`, so the declaration names a surface
the shipped path does not touch.

**Measured cost.** A person who confirms a retag sees the files corrected and
rekordbox still showing the old genre, because rekordbox reads the row. R-185 is
the same fact from the other side and this entry is the registry's half of it.
Nothing derives from the `writes` set today, so the cost is a declaration a
reader would trust.

**Why it is not fixed here.** Holding a database write session open across a
network lookup per file is what R-185 already argues against, and the fix is the
deferred half rather than a change to this unit's writes.

**Closes when:** the database half has a caller, or the registry entry stops
claiming `db_metadata`.

---

## R-247. An unmapped source genre has nowhere to become an alias

**Found by** U56, 2026-09-03, driven through `crate tag folder`.

When a catalogue answers with a genre the declared taxonomy cannot resolve, the
searcher declines and `tag_one` reports `unmapped-genre` with the raw string.
R24 puts the distinct strings and their counts in the verb's report, so a person
learns which words their taxonomy is missing. Nothing takes them any further.
The declared taxonomy is a packaged template, and there is no verb that adds an
alias to it.

**Measured cost.** The file stays untagged for ever and every run re-pays a
paced lookup on it, because the answer is deterministic. The person is told what
is missing and has no way to act on it inside this product.

**Why it is not fixed here.** `tag.retag` already offers its unanswerable cases
into `review.Queue.GENRE`, so the surface exists, and routing `tag.folder`'s
declines into it would make an unattended verb attended. That is a product
decision about what `crate tag folder` is, not a repair.

**Closes when:** an unmapped source genre reaches a queue a person answers, or a
verb writes an alias into the active taxonomy.

---

## R-248. A third copy of the queued verb shell, and a third of the artifact helper

**Found by** U56, 2026-09-03.

`cratekit.tagging.shell` is `adopt/shell.py`'s three functions with tagging's
words, and `cratekit.tagging.artifacts` is `adopt/artifacts.py`'s five with two
different directory names. `modules/outbound` holds the other copy of each. Every
rule in all three is the same rule.

**Measured cost.** None today. The cost is the one R-240 already names for the
artifact helper: three copies of a fix is two copies that do not get it. The
R-225 predicate is now written out in three files, and it took two units to get
right in the first place.

**Why it is not fixed here.** The honest home is one module in `core` taking the
names as arguments, and moving the other two there is a change to two other
units' files. Reaching into `adopt` from `tagging` would put an adoption name on
a tagging rule, which is the same defect wearing a shorter diff.

**Closes when:** one module owns the queued verb shell and one owns the artifact
helper, with each feature package naming its own values through them.

**A FOURTH AND A FIFTH COPY, found at the U52 review, 2026-09-07.** The merge
brought `tagging/shell.advance` and `adopt/shell.advance` in beside
`label/cli._resume`, and the three are one function: reconcile, refuse a job
with no items, run the job, re-read it, re-raise a closed job's cause outside
the `is_open` branch. `backup/cli.py` and `modules/outbound/shell.py` are the
other two spellings and `master/cli.py`'s resume branch has neither the
itemless refusal nor the re-raise, which is R-225. Two more facts joined at
this review and belong to the same entry: the itemless refusal's machine
readable remedy is `report-defect` in every copy while its sentence says the
job is stale rather than defective, so tooling keyed on the token files a bug
over a documented migration shape, and the guard itself belongs one layer
down in `jobs.drive` beside its terminal state refusal, where one line would
replace five. U52 added the cancel step to its own copy's remediation and
nothing else, for the reason above: the honest home is one module, and
`label` cannot import a sibling feature package to share it.

**A SIXTH COPY OF THE TAIL AND A FOURTH OF THE HELPER, U58, 2026-09-08.**
`analysis/cli.py` carries `_advance`, `_reported` and `_no_op`, and
`analysis/artifacts.py` is the five function staging helper with two directory
names changed. R-274 records why the unit copied rather than reached across.
One fact joined at the second review: U58's round fixed the helper's
`committed()` in the analysis copy only, so a stray non ordinal `.json`
beside the reports no longer raises out of the sort key THERE, and the adopt,
outbound and tagging copies still do. That is the cost this entry predicted,
landed: a fix in one copy is three copies without it.

---

## R-249. A second pacing implementation, and it is deliberately not the first

**Found by** U56, 2026-09-03.

`searchers.Pacer` is a minimum interval, a jitter fraction and an injected sleep.
`acquire/download.Pacing` is the same three plus a backoff policy, a retry hint
ceiling and an attempt cap, and it is consumed by a bounded concurrent pool bound
to the adapter contract.

**Measured cost.** None. The two have different shapes because they solve
different problems, and the searcher is sequential where the downloader is not.
The cost is that the words "jitter fraction" and "minimum interval" now mean the
same thing in two modules that share no code, so a later change to one is a
question about the other that nothing asks.

**Why it is not fixed here.** Importing the acquisition pacing into tagging would
bind a genre lookup to the download adapter's settings type, and generalising it
is a change to another unit's file.

**Closes when:** one pacing policy serves both, or the two are stated as
deliberately separate at both ends rather than at one.

---

## R-250. The retag worker reads the whole genre review queue once per item

**Found by** U56 while binding the worker, 2026-09-03.

`retag.decided_index` reads every item this pass has ever offered, which is one
query for a whole folder sweep and one query PER ITEM in the worker, because the
worker runs one candidate per call.

**Measured cost.** Unmeasured and believed small. The queue holds only
coarse-genre questions this pass has asked, so it is bounded by the size of that
backlog rather than by the library, and a retag over a download folder is tens of
files rather than thousands. No timing was taken.

**Why it is not fixed here.** The cheap fix is a targeted read, and
`core.review.get` refuses rather than returning None for an absent identifier, so
a targeted read means either catching a refusal as control flow or adding a
non-refusing sibling to `core.review`, which is a foundation file this unit does
not own.

**Closes when:** a measurement says it matters, or `core.review` grows a lookup
that answers absence without raising.

---

## R-251. The vanished tagging file reuses `source-missing` rather than a slug of its own

**Found by** U56, 2026-09-03.

Both tagging workers refuse an item whose file is gone between the queueing and
the drive, and both raise `source-missing`. Their two siblings each took a slug
of their own for the same shape: `adopt-item-absent` for a collection row the
scan job queued, `outbound-item-absent` for a track a frozen export no longer
carries.

**Measured cost.** None to a run. `source-missing`'s reserved remediation already
says nothing was read and nothing was written, which is exactly what the refusal
promises, and the message names the file. The cost is that a person filtering job
causes cannot tell a tagging item's vanished file from any other missing source.

**Why it is not fixed here.** It is a judgement about how wide a slug should be,
and the argument runs both ways: the two siblings say a third, and this
vocabulary's own record says twice that a second slug meaning the same thing
makes a person read a different sentence depending on which verb noticed.

**Closes when:** somebody decides, and the reserved population is re-pinned with
the answer.

---

## R-252. A file added to a folder between the queueing and the drive is never tagged

**Found by** the U56 document review, 2026-09-03, reasoned rather than driven.

`crate tag folder` derives its items at enqueue and the job runs later. A file
dropped into the folder in between is in no item, so the worker never sees it and
the job reports SUCCEEDED over a folder that still holds an untagged file. R15
covers only the file that disappeared.

**Measured cost.** Unmeasured. The window is between the queueing and the resume,
which for an attended run is seconds and for a queue left overnight is hours. The
next run over the same folder does tag it, so the state converges; what does not
converge is the report, which said the folder was done.

**Why it is not fixed here.** The cheap answer is a count comparison in the final
report rather than a new item, and deciding whether that is a warning or a
refusal is a decision about what a queued sweep promises.

**Closes when:** the report names the difference between what was queued and what
the folder now holds, or a decision is recorded that a frozen item set is the
whole promise.

---

## R-253. `tag.folder`'s unnamed folder is a warning where its sibling refuses

**Found by** U56, 2026-09-03. Driven: before the branch existed, `crate tag
folder ""` exited ok with a job queued over the current directory.

An empty string is a valid argument to a positional, and `Path("")` is the
current directory. `tag.retag` refuses that argument under
`tag-retag-folder-unknown`, which is a declared slug of its own. `tag.folder`
reports a NO_OP with the warning `tag-folder-unnamed` instead, because a refusal
needs a slug in `cause.REASONS` and reusing the correction verb's would put that
verb's name on this one's failure.

**Measured cost.** None to a library: both stop before writing anything. The cost
is that two sibling verbs answer one mistake with two different exit codes, so a
script wrapping them has to know which is which.

**Why it is not fixed here.** Adding a slug is a `cause.py` edit and a re-pin of
the reserved population, and this unit already moved that population twice.

**Closes when:** `tag.folder` refuses an unnamed folder under its own slug, or a
decision is recorded that the two verbs answer it differently on purpose.

---

## R-254. The retag reports two zeroes where its sibling reports three

**Found by** U56, 2026-09-03.

`crate tag folder` tells a folder holding no audio apart from a folder that is
not there. `crate tag retag` folds "every genre here is already specific" and
"this folder holds no audio at all" into one warning,
`tag-retag-nothing-coarse`, because its selection walks once and cannot tell them
apart.

**Measured cost.** Small. A person who mistypes a subfolder name under a real
library gets the folder-absent warning either way, since that case IS
distinguished. What is folded is two shapes of "nothing to correct", and the next
move after both is the same.

**Why it is not fixed here.** Telling them apart means a second walk of the same
folder purely to count audio files, which is the cost this verb's selection
already paid once.

**Closes when:** the selection reports what it walked as well as what it took.

---

## R-255. A retag over a folder with nothing to correct still spends a person's decision

**Found by** U56, 2026-09-03, and REVERSED INTO on purpose.

The first draft of `tag.retag` derived its selection before raising the confirm
gate, so an empty plan reported NO_OP without asking anybody. Conformance 3
reported it as an unreachable gate within minutes, because that rule holds every
declared gate to firing, and `adopt/apply_cli` had already answered the same
question the other way. The gate now fires first and the zero item rule is
enforced after it.

**Measured cost.** A person running the verb over a clean folder meets
DECISION_REQUIRED and has to record a decision through `crate run decide` before
being told there was nothing to do. That is a real cost and it is the accepted
side of the trade.

**Why it is not fixed here.** Both answers are defensible and only one can be
right for both verbs at once. Consistency with the sibling and with the shipped
conformance rule won.

**Closes when:** a decision is recorded that an empty plan should not raise its
gate, and both verbs and the conformance rule move together.

---

## R-256. `scripts/mutate.py` exited 0 with a mutant still on disk

**Found by** U56's mutation pass, 2026-09-07. Observed, not explained.

The forty row pass returned exit code 0 and printed every row. After it
returned, `src/cratekit/cli/handlers.py` still carried `R40`'s mutation, which
deletes the `"tag.retag"` entry from `cli.handlers.HANDLERS`. The tree was clean
before the run, and the file's mtime sits seven seconds before the driver's own
table and sidecar writes, so the driver was the last writer.

**Measured cost, and it is the whole point of this entry.** The next thing a
session does after a pass is run the battery and merge. That battery would have
run against a tree with `tag.retag` unbound, and the merge would have shipped it.
The verb would have been queueable and would never have run, which is precisely
the R-203 state this unit exists to leave, and the mutation table in the same
commit would have been asserting that thirteen tests kill that exact change.
Nothing in a green suite says which tree it was green on.

**What is NOT damaged.** `R40` is the last row, so every measurement in the
table was taken before the contamination. The null control killed zero on the
full suite, no row drifted its collected count, and an independent two row rerun
killed 10 and 14 where the pass recorded 10 and 13.

**Why it is not fixed here.** It did not reproduce. The same two mutations
against the same file on a clean tree restored correctly. The driver has two
writes to a target, both inside a `finally` that restores from an in-memory
snapshot and then compares the file to `git show HEAD:` and RAISES on a
mismatch, and that error is re-raised rather than swallowed. The source says
this cannot happen and it happened, so the cause is somewhere the source does
not show, and a fix aimed at a guessed mechanism is the fourth recurring defect
pattern in `docs/METHOD.md`.

One nearby thing was found while looking and is worth naming, because it makes
the record read stronger than it is: the sidecar's `head_verified` field is set
from the driver's input flag rather than from the verification result, so it
says HEAD verification was REQUESTED, not that it passed.

**The mitigation, which costs one command and is now written down**: run
`git status --porcelain` after every `scripts/mutate.py` return, before the
battery and before trusting a row, and restore from `git show HEAD:<path>`.
`docs/solutions/workflow-issues/a-mutation-driver-can-exit-clean-and-leave-a-mutant.md`
carries it.

**Closes when:** the mechanism is reproduced and fixed, or the driver verifies
every target against HEAD once more after its last row and refuses to exit 0
otherwise, which is a check that would have caught this one whatever caused it.

---

## R-257. A completed sweep reports item counts and no offer counts

**Found:** during U52, 2026-09-02, as the stated cost of KTD7.

Both label verbs declare `output_schema="job_state/1"`
(`src/cratekit/cli/registry.py:1248-1265` and `:1308-1325`), and `cli/output`
closes that surface with `additionalProperties: false` over exactly four fields,
`job_id`, `state`, `cause` and `progress` (`tests/schemas/job_state.v1.json`).
`_reported` fills those four (`src/cratekit/label/cli.py:37-43`) and `progress`
is `jobs.progress`, which groups the job item ledger by item state and returns
counts plus the totals a progress display needs
(`src/cratekit/core/jobs.py:524-542`). The worker returns `None` and commits no
artifact, as `backup/cli.py`'s does. So a sweep of five favourite labels that
offered two hundred releases reports five items done, and the number two hundred
appears nowhere in the envelope the verb emits.

**Measured cost.** A person who runs `crate sync labels` and reads its output
learns that every label was swept and nothing at all about what was found. To see
the offers they run a second command against the label-release review queue,
which is the product's actual and durable record of what was offered. No count in
the envelope is wrong; a count is absent, and the absence is loudest on the run
where a sweep found a great deal.

**Why not fixed here.** Per verb detail added beside `progress` is exactly the
undeclared key U51 had to remove from the two outbound verbs, so adding one here
would reintroduce a schema violation that branch paid to fix. The alternative is
a second artifact store for a fact the review queue already holds, which is two
records of one thing and is how the two come to disagree about what a sweep
offered. KTD7 chose neither and recorded the cost instead.

**Closes when:** `job_state/1` grows a declared surface for per verb detail that
every queued verb can fill, or a verb built to read the review queue reports what
a named sweep put there.

---

## R-258. No catalogue adapter ships, so no label workflow can run outside a test

**Found:** during U52, 2026-09-02, by binding the two workers and rebuilding
harvest on the seam.

`crate sync labels`, `crate label import` and `crate label harvest` all reach a
provider through one module, `src/cratekit/label/catalogue.py`. `bound()` returns
a constant `False` (`:110-121`), and `resolve` raises `credential-missing` when no
provider session is recorded and `label-catalogue-unbound` when one is. Two
refusals rather than one, because they are undone by different acts and
collapsing them would send somebody to a login screen over a gap in the build.

No implementation of the `Catalogue` protocol exists anywhere in `src`, measured
by reading every reference to the name outside the vendored tree. There are six:
the class definition (`catalogue.py:50`), the return annotation on `resolve`
(`catalogue.py:124`), the `__all__` line (`catalogue.py:158`), one import
(`src/cratekit/label/sweep.py:23`) and two parameter annotations
(`src/cratekit/label/sweep.py:227`, `src/cratekit/label/cli.py:449`). Six
references, zero implementations.

**Measured cost, and it is the whole remaining distance between this branch and a
label workflow the single real user can run.** Every queued label item ends FAILED
with a named cause rather than sitting pending for ever, and harvest refuses
before it contacts anything. Nothing is written wrongly and nothing is lost. Both
queueing verbs warn at enqueue, because `bound()` can be asked without raising
and `_queue` asks it, so nobody confirms a sweep this build cannot perform
without being told first. What a person cannot do is sweep a label.

**This is R-226's shape on a second seam, and the two are deliberately separate
seams rather than one.** That entry records the same condition for
`modules/outbound/account.RemoteAccount`. `RemoteAccount` is add only writes
against an account and this is reads against a catalogue, so the two share a
credential and not a capability, and a build could plausibly gain one and not the
other. A person asked to sweep their favourite labels who was told the streaming
ACCOUNT was unbound would go looking at the wrong half of the product. The test
substitution carries the same limit R-226 states: a test replaces `resolve` on
the module and the in process callers pick it up because they look it up at call
time, while the child a resume spawns is a fresh process that inherits nothing.

**Why not fixed here.** Opening a live provider session is attended work and a
standing refusal for an unattended session, which is the reason R-144 has stayed
open since 2026-08-17. The plan's Scope Boundaries put the adapter on the board
as a follow up unit rather than in this ledger alone, because it is the whole
remaining distance and a residual is a register of what was accepted rather than
a queue. No issue for it exists yet, checked against all seventy six issues on
the board.

**Closes when:** an adapter implements `Catalogue`, `resolve` returns it,
`bound()` stops being a constant, and one real label sweep and one real playlist
harvest run against a live provider.

**Agent half CLOSED by U62, 2026-09-16, on `relay/84`.** `label.tidal_catalogue`
implements `Catalogue` over a client `acquire.provider_session.client_session`
logs in from the stored session, `resolve` returns it once a session is recorded,
and `bound()` answers whether that module imports. Driven against a fake client
injected at `provider_session.CLIENT_FACTORY` in
`tests/test_label_tidal_catalogue.py`, including `crate intake playlist` end to
end and the download verb accepting the resulting document. **The live half stays
open**: one real label sweep and one real playlist harvest are the next attended
sitting's, recorded in `docs/cutover.md`. `label-catalogue-unbound` survives only
for a build whose adapter does not import.

---

## R-259. The labels path applies no ownership filtering at all

**Found:** during U52, 2026-09-02, as the second consequence KTD9 names.

The worker passes `owned=set()` (`src/cratekit/label/cli.py:673`) and
`LabelSource.list_recent` calls `list_for_label` with no `owned` argument
(`src/cratekit/label/sweep.py:303-315`). Both filters are membership tests
against the set they are handed, `scope.scoped` at
`src/cratekit/sync/scope.py:36-41` and `list_for_label` at
`src/cratekit/label/sweep.py:176`, and `scope.scoped`'s own docstring says it
does not treat an empty owned set as "everything is new" in any special way: an
empty owned set simply keeps the first `limit` items. An empty set therefore
filters nothing.

**Measured cost.** A sweep offers releases the library already holds. Each one
becomes a row in the label-release review queue that a person has to read and
decline, so the cost is paid in review time on every sweep, and it grows with how
much of a label the library already has rather than with how much is new. A
person sweeping a favourite label they have followed for years pays the most.

**This is NOT R-137, and the distinction is why both entries exist.** R-137 is
about the ORDER, newest N taken before owned dedup, and its closing condition is
satisfied by reordering two steps. Reordering two steps that both filter on an
empty set changes nothing at all. Closing R-137 would leave this entry open, and
closing this entry is what makes R-137's defect reachable for the first time.
R-137's own amendment carries the measurement that no producer of an owned
identity set exists on this path.

**Why not fixed here.** Building the producer is either a collection reader
against the live rekordbox database, which has not landed and is the reason R-203
gives for `adopt.scan` being unbound too, or a read of the hand made collection
export R-227 describes, which carries library tracks rather than label release
identities and would need a mapping between the two that nothing in `src` has.
Either is a unit, not a line in a worker.

**Closes when:** the labels path is handed a real set of owned release
identities, and a sweep of a label whose catalogue the library already holds
offers nothing.

---

## R-260. `IncrementResult` no longer says whether the intake file was written

**Found:** during U52, 2026-09-02, as the caller obligation KTD3 creates.

Before `Source.acquires`, a non empty `processed` tuple with `shortfall` of
`None` meant the run's `{run_id}_synced.xml` held those identities and the source
watermark had moved. It no longer does: an offering source completes in exactly
that shape and writes neither (`src/cratekit/sync/run.py:182-194`).
`IncrementResult` carries `source_id`, `processed`, `errors` and `shortfall` and
no field a caller could ask (`src/cratekit/sync/run.py:69-90`), and
`run_independent` hands back a dictionary keyed by source id whose values are
those same results or an error, with no per source signal beyond them
(`src/cratekit/sync/run.py:215-241`). A caller that needs the distinction has to
read `source.acquires` off the source object it passed in. That is stated in the
type's own docstring rather than left for a reader to infer, which is the whole
of what this branch did about it.

**Measured cost. NONE today, and it was measured rather than assumed.**
`run.increment` has exactly one caller in `src`, `label.cli.run_increment`, and
`run_independent` has none at all, checked by grep across `src` outside the
vendored tree. The one caller knows its source offers, because it constructed the
source. The cost falls entirely on the first caller that runs an acquiring source
and an offering source in one pass and then reports what the pass did.

**`sync.all` is the caller that will need it first.** `src/cratekit/sync/cli.py`
is the orchestrator that runs several sources under one run id, and a report
saying "these landed" over a set holding both a playlists download and a labels
offer would be wrong about half of what it named. `sync.all` has no worker yet
and is one of R-203's thirteen, so this is an obligation waiting for a unit
rather than a live defect, and the unit that binds it inherits this entry.

**Why not fixed here.** Widening `IncrementResult` is a U22 contract change, and
R-136 already records it as one for the discarded and suppressed populations.
Two widenings of one frozen dataclass belong in a single unit that answers what
the result type is for, not in a branch that binds two workers.

**Closes when:** `IncrementResult`, or whatever replaces it, says whether the run
recorded an acquisition, and `run_independent` says it per source. R-136 is the
other half of the same widening and should close with it.

---

## R-261. A client exposing one of two listing methods yields a half catalogue reported as a complete crawl

**Found:** during U52, 2026-09-02, while closing two of R-135's three producers.

`listing.artist_releases` walks two method names, `get_albums` and
`get_ep_singles`, and skips one the client does not expose, individually and
without raising (`src/cratekit/acquire/listing.py:234-236`, inside the function
at `:219-246`). `crawl.can_list` refuses only an artist exposing NONE of them
(`src/cratekit/label/crawl.py:32-52`), and `sweep._crawl_or_refuse` asks that
question and no other before it is willing to believe an empty answer
(`src/cratekit/label/sweep.py:116-121`). So a client exposing `get_albums` and
not `get_ep_singles` returns the albums, skips the second listing in silence, and
the increment reports a crawl that read the catalogue.

**Measured cost.** A label whose catalogue lives mostly in extended plays and
singles, which is where `artist_releases`'s own docstring says a label catalogue
lives, is swept for its albums alone. Nothing warns. The sweep reports success,
no watermark moves because an offering source moves none, and the releases that
were never listed are indistinguishable from releases that were listed and found
to be nothing new. This is the R-135 defect class at half strength: not an
unreadable catalogue read as empty, but an unread half of one read as absent.

**Why not fixed here, and this entry records a consequence rather than proposing
a change.** The skip is a deliberate tradeoff the wrapper defends in its own
docstring: the two method names have moved between client versions, and losing
one listing is a smaller failure than refusing to crawl at all. `crawl.can_list`
repeats that reasoning and says explicitly that the decision of what an absence
MEANS belongs to the caller about to report it, which is why it is a separate
function rather than a raise inside `releases`. Turning the skip into a refusal
would make the next client version bump refuse every sweep in the product. What
is missing is not a refusal, it is a report: nothing carries the fact that one of
two listings was skipped up to any place a person reads.

**Closes when:** a crawl that skipped a listing method says so in something a
person sees, or both listings are read through a client contract that cannot be
half present.

---

## R-262. Two more verbs declare write surfaces their workers cannot reach

**Found:** during U52, 2026-09-02, and it is R-233's shape on a second pair of
verbs.

`sync.labels` and `label.import` each declare `writes=frozenset({"xml",
"files"})`, `adjudicates=True` and `destructive=True`
(`src/cratekit/cli/registry.py:1248-1265` and `:1308-1325`), along with the
doctor checks `library.mounted` and `credential.provider`. The worker U52 bound
writes neither declared surface. It offers into the label-release review queue
and returns `None`, and `LabelSource.acquires` is False so `run.increment` writes
no `{run_id}_synced.xml` and registers no artifact
(`src/cratekit/sync/run.py:182-194`). Nothing on the path downloads a file.
`label.harvest` is not affected: it declares no write surfaces at all.

**Measured cost. NONE, and it was measured on this branch rather than inherited
from R-233.** `entry.writes` and `entry.destructive` are read nowhere in `src`
outside `registry.py`, where the only two reads are the entry's own self
validation (`src/cratekit/cli/registry.py:177-184`), checked by grep across `src`
excluding the vendored tree. `doctor.requires_check` is an `any()` across every
registry entry rather than a per verb lookup
(`src/cratekit/cli/doctor.py:506-523`), and the two checks these verbs declare
are declared by twenty two and seven entries respectively, counted from
`registry.ENTRIES`, so dropping them from these two would change neither. No
health report changes and no gate changes.

**Why not fixed here, and it is the reason R-233 already gives.** `writes` is a
declaration of what the verb is FOR rather than of what today's build can reach,
and narrowing it also lets `destructive` fall to False, which is a judgement
about whether a verb that will download audio the day an adapter lands should
hold the library lock in the meantime. R-258 is the only thing standing between
these declarations and being true, and the unit that closes it needs them back.

**Closes when:** the catalogue adapter lands and these two verbs write the
surfaces they declare, or the entries are narrowed with the destructive question
answered, which is the same fork R-233 leaves open for the two outbound verbs.

---

## R-263. A labels sweep that succeeds still reports the source has never run

**Found:** at the U52 code review, 2026-09-02. Accepted rather than fixed.

R-140's fix is what creates this. `run.increment` returns before
`watermarks.advance` when the source does not acquire
(`src/cratekit/sync/run.py:182`), and `LabelSource.acquires` is `False`
(`src/cratekit/label/sweep.py:264`), so nothing in `src` ever writes the
`labels` source watermark. `run.py:201` is that function's only caller.

The reader was not updated with the writer. `watermarks.status_rows` unions
`sources.DECLARED`, which always contains `labels`, and renders a source with no
record as `state: never` with the detail `no clean increment has completed`
(`src/cratekit/sync/watermarks.py:197`). `crate doctor` prints that row. So a
person who has just run a fully successful five label sweep, whose releases are
sitting in the review queue waiting on them, is told the labels source has never
completed a clean increment.

**The absence changed meaning and its one consumer did not.** Before this branch
a missing record meant only "never completed cleanly". It now also means
"structurally never records one, by design", and those are different facts with
different answers.

**Measured cost.** One false row in `crate doctor` and in any status view built
on `status_rows`, on every installation that sweeps labels. No acquisition is
wrong and no data is lost.

**Why not fixed here.** Distinguishing the two absences means giving
`sources.SourceSpec` an `acquires` flag, or having `status_rows` read it off the
source, and then adding a third state to a surface every other source shares.
That is a contract change to the watermark reporting surface, which is a
different unit from the one that stopped writing the record.

**Closes when:** a declared source that records no cursor by design reports that
in `status_rows` rather than reporting that it never ran. R-260 records the
`IncrementResult` half of the same split; this entry names the reader.

---

## R-264. An interrupt cannot reach a label item mid crawl

**Found:** at the U52 code review, 2026-09-02. Accepted rather than fixed.

`jobs.drive` checks its interrupt flag BETWEEN items and never inside one
(`src/cratekit/core/jobs.py:1240`). That is a deliberate property of the shared
job engine and it predates this branch. What this branch changes is that it is
now reachable with a long tail: the label worker is the first bound handler
whose single item runs a paginated crawl through `listing.fetch_with_retry`,
whose ladder is five tries with a thirty second ceiling, per page.

So a person who interrupts a slow or flaky label sweep waits for the current
label's crawl to finish before the interrupt is honoured. The other bound
handlers, `backup.run`, `master`, `export.playlist` and `sync.favorites`, do no
multi page retrying provider read per item, which is why nothing measured this
before.

**Measured cost.** A delayed response to an interrupt, bounded by one label's
crawl. Nothing is corrupted: the interrupt is honoured at the next item boundary
and the job stays resumable.

**Why not fixed here.** Making the flag visible inside an item means either
passing it into the handler, which widens the handler contract every bound verb
shares, or threading a cancellation token through `acquire.listing`. Both are
changes to code this branch's stop conditions put out of scope, and neither is
the label worker's to make alone.

**Closes when:** a long running item can observe the interrupt flag, or the
listing retry ladder takes a deadline the driver sets.

---

## R-265. `crate doctor` and `board.py` cannot see a unit the relay has moved to In review

**Found:** at the U52 record, 2026-09-07, by the audit this file's session
contract requires before ending.

The board's Status field carries an `In review` option and the relay runner
moves a card there as its first tracker write. `scripts/board.py` orders five
statuses in `STATUS_ORDER` and `derive_status` preserves exactly one of them
across a recomputation, `In Progress`, on the reasoning that a unit on a branch
must not be recomputed back to Ready. `In review` is not in that list, so the
audit reports a unit under review as drift ("should be Ready") and `sync` would
carry out the flip the comment in `derive_status` exists to prevent.

**Measured cost.** `board.py audit` exited 1 on #70 during this record, and a
session obeying the contract's "sync repairs it" would have moved a card the
runner owns. The audit also reported #78 and #79 as not on the board at all;
those are two units added to the tracker during this run and are somebody's to
add, not this unit's.

**Why not fixed here.** `board.py` is the operator's tool and the relay's status
vocabulary is the runner's; which of the two owns the word is a decision. The
conservative call was to leave the board untouched and record the exit code.

**Closes when:** `derive_status` treats `In review` as it treats `In Progress`,
or the runner uses a status the script already preserves.

**Observed again on 2026-09-10, on #81, and this is a confirmation rather than a
new finding.** `board.py audit` printed `#81 status is In review, should be
Ready` and exited 1. Recorded here rather than as a fresh number, because the
session that hit it had drafted a new entry before finding this one, and a second
copy of a fact is how the two come to disagree. What the second sighting adds is
that it is now the ONLY thing the audit reports: with issue #25 reopened the
contradiction is gone, so this drift is the whole of the audit's output at the
end of a relay run, and the printed remedy is a `sync` that would undo the
runner's first tracker write.

---

## R-266. Every label job in this build ends `no-evidence`, retryable, over a refusal that says never retry

**Found:** at the U52 review, 2026-09-07, by two angles independently.

`catalogue.resolve` refuses on every item in this build, so every driven label
job fails all of its items, and `jobs.drive` then raises `no-evidence` with the
item's `label-catalogue-unbound` nested as `inner`: exit INTERNAL, remedy
`retry-later`, `retryable` true. `core/cause.py` classifies the seam's slug as a
PRECONDITION on the stated reasoning that a missing adapter is a limitation and
not a defect to retry, and the top level cause contradicts that on every drive.
A resume then calls `jobs.retry`, which re-arms the failed items, and the child
fails identically; nothing on the resume path repeats the one sentence that
would stop the loop.

**Measured cost.** A person or a script keyed on the top level `retryable`
re-drives a job that cannot succeed in this build. The same shape holds for
both outbound verbs behind R-226, so this is the engine's verdict over an
unbound seam rather than the label worker's.

**Why not fixed here.** `evidence_or_raise` is the shared engine's whole run
verdict, and teaching it to promote a unanimous PRECONDITION inner cause to
the top is a change to the one function every queued verb runs through.

**Closes when:** a job whose every item failed with one non retryable cause
reports that cause at the top, or an adapter lands and the case stops being
every run.

---

## R-267. `bound()` and `resolve()` answer one question from two constants, and the suite already shows them disagreeing

**Found:** at the U52 review, 2026-09-07.

`label/catalogue.bound` returns a literal `False` and `resolve` raises
unconditionally after the credential check. The day an adapter lands both have
to move together and nothing ties them: edit one and the queueing verb warns
that a sweep will fail at the seam while the worker runs it, or the reverse.
The suite is already in the first state, because a test substitutes `resolve`
and `bound()` stays `False`, so `crate sync labels` under a fake catalogue emits
`label-catalogue-unbound` as a warning on the exact run that then sweeps
successfully. `modules/outbound/account.py` has the identical shape.

**Measured cost.** None for a person today; both constants agree in a shipped
build. A false warning in every driven test, and one lockstep edit owed.

**Why not fixed here.** The clean form, one module level adapter slot that
`bound()` reads and `resolve()` calls, puts the credential check before the
adapter, and the suite's fakes carry no stored session, so every driven test
would have to fake the credential too. That is a change to the substitution
contract three docstrings state, and R-258 already records the closing shape.

**Closes when:** one value answers both, on both seams.

---

## R-268. A provider's own authentication failure is not a `CratekitError`, so the passthroughs do not see it

**Found:** at the U52 review, 2026-09-07.

The three seam boundaries in `label/sweep.py` and the two in `label/cli.py` now
let a `CratekitError` through and flatten only a foreign exception. That is
right for an adapter that refuses `credential-missing` itself, and it is no
help for the shape the vendored client actually raises: `listing.fetch_with_retry`
re-raises the provider's raw exception once its ladder is spent, a rejected
session arrives as that raw exception, and `acquire/vendored.py` already carries
`is_authentication_failure` and `raise_if_session_dead` to tell it from a
listing failure. Neither is asked on the label path, so an expired session in a
future adapter that does not translate it is reported as an unreadable playlist
or a source that could not list, and the person is sent to check a playlist
that is fine.

**Measured cost.** None today, because no adapter ships (R-258). The cost is
the adapter's, and this entry says which side owns it.

**Why not fixed here.** Asking the vendored predicate inside five boundaries
binds the label package to the vendored client's exception shapes before an
adapter has chosen them. The adapter that closes R-258 owns raising this
product's refusal at the seam, and these boundaries now pass it through.

**Closes when:** the adapter translates its client's authentication failure
into `credential-missing` at the seam, or the boundaries ask the predicate.

---

## R-269. Harvest reports a clean `NO_OP` over a playlist whose every name the catalogue refused to confirm

**Found:** at the U52 review, 2026-09-07. A judgement recorded rather than a
defect fixed.

`harvest_playlist` emits `outcome=no_op` and exit 0 whenever nothing was
offered, including a playlist of forty tracks whose twenty five distinct names
were all answered `unconfirmed` by a degraded verification endpoint. The sweep
worker refuses the same shape as `label-sweep-incomplete`, so the two verbs in
one module disagree about what an all unconfirmed pass means.

**Measured cost.** A person reading `outcome` alone sees a no op. A person
reading the envelope sees `unresolved: 25` and `items: []`, which is the whole
truth, and it is why the two verbs differ: the sweep's `job_state/1` envelope
cannot carry a count (R-257) and so must refuse to be honest, while harvest's
`review_set/1` carries the count and can report instead. Nothing is written
wrongly.

**Why not fixed here.** Refusing here would make a playlist of names the
catalogue genuinely does not know indistinguishable from an outage, which is
the collapse in the other direction, and the envelope already says what
happened.

**Closes when:** the two verbs state one rule for an all unconfirmed pass, or
`outcome` gains a value between OK and NO_OP for "read, confirmed nothing".

---

## R-270. The credential presence check is spelled three times

**Found:** at the U52 review, 2026-09-07.

`label/catalogue.resolve` and `modules/outbound/account.resolve` each ask
`secrets.exists` for the provider session and each raise `credential-missing`
with `Remedy.AUTHENTICATE_PROVIDER`, `Scope.RUN` and a `credential` detail, and
`cli/verbs/login.py` is the third. `acquire.provider_session` declares itself
the sole owner of the credential under R4 and neither seam calls into it.

**Measured cost.** None. A change to the remedy, the detail key, or the
predicate is three edits, and the third is the one that is missed.

**Why not fixed here.** One `require_provider_session` in the credential owner
is a change to that module and to the outbound seam, which are two other
units' files. R-232 records the same shape for the configuration wrapper.

**Closes when:** both seams ask the credential owner and keep only their own
`-unbound` refusal.

---

## R-271. A fourth hand written snapshot of the suppression identity rule

**Found:** at the U52 review, 2026-09-07.

`sweep._suppression_reader` builds a set of `suppression_id` values from
`DecisionStore.suppressions()` and tests `review.suppression_id_for(...)`
membership. `acquire/match_cli.suppression_view` and the two predicates in
`deletion/stores.py` do the same. The one real difference is that this reader
is lazy and the others read at construction, which is a property this branch's
suite pins (an unreadable store must not fail a label with nothing to ask).

**Measured cost.** None. If the identifier scheme ever needs a store side
adjustment, the deletion module's `identity_scheme` stamp says it might, four
closures have to be found.

**Why not fixed here.** The home is a method on `DecisionStore`, which is
`core/review.py`, and this branch binds a worker rather than reshaping the
store. The lazy wrapper would stay around whatever the store offered.

**Closes when:** `DecisionStore` hands out the snapshot once and the four
callers take it.

---

## R-272. The increment's lookup refusal carries the exception kind only in prose

**Found:** at the U52 review, 2026-09-07.

`run.increment` converts a `LookupFailure` into `sync-source-lookups-failed`
with `from exc` and no `inner` and no `kind` in its detail, so the job ledger
holds the flattened sentence and nothing structured. Every raise site in
`label/sweep.py` chains the underlying exception and puts its type name in the
message, so the fact is readable and not addressable. The harvest boundary in
`label/cli.py` records `detail["kind"]`.

**Measured cost.** A `ListingNotPaginated` from a client that dropped its
pagination arguments lands in the item row as "every listing call failed",
with a remedy to retry when the provider is reachable, and no retry fixes a
client version mismatch. The kind is in the sentence for a person and not in
the detail for a tool.

**Why not fixed here.** `sync/run.py` is the shared increment engine and its
refusal is every source's; changing its detail is a contract for all of them.

**Closes when:** the increment's refusal carries the underlying kind in its
detail, or the inner cause when the underlying exception was one.

---

## R-273. The mutation driver's record attributes a forty five row cap to METHOD, which states twenty five

**Found:** at the U52 review, 2026-09-07, by the conventions angle.

`scripts/mutate.py` carries `ROW_CAPS = {"light": 25, "full": 45}` and its
"considered and dropped" template writes "METHOD caps a full pass at 45 rows"
into every table it emits. `docs/METHOD.md` states one hard cap of twenty five
rows and one pass per unit per session, and `CLAUDE.md` repeats it. U52's forty
row table and U56's both carry the sentence, and both overruns are recorded as
explicit decisions in `RESTART-cratekit.md`. What remains is the sentence: a
future reader takes the tool's number for the rule.

**Measured cost.** One false attribution per emitted table.

**Why not fixed here.** `scripts/mutate.py` is on `main` and outside this
branch's diff, and the cap is a policy the operator set on 2026-09-07 rather
than the driver's to restate. The zero row re-measure this session ran nine
rows and emitted the same sentence.

**Closes when:** the driver's caps and its template say what METHOD says, or
METHOD names the two pass kinds.

---

## R-274. The analysis package carries the sixth resume tail and the fourth artifact helper

**Found:** at the U58 review, 2026-09-07, by the reuse and altitude angles.

`src/cratekit/analysis/cli.py` carries `_advance`, `_reported` and `_no_op`,
the three functions `cratekit.tagging.shell` already parameterized so a fourth
verb would not need them again, and `src/cratekit/analysis/artifacts.py` is the
fourth copy of the five function staging helper beside adoption, outbound and
tagging. The unit copied rather than reached across for the reason the earlier
copies give, that a tagging name on an analysis rule is the wrong name, and it
did not move either to `core`, which is the honest home and is other units'
files. R-248 records the same shape for the resume tail; this entry adds the
sixth copy and the fourth helper to its count.

**Measured cost.** None to a user today. The next change to the closed and
carrying a cause predicate, or to the ordinal named staging rule, lands in the
copies somebody remembers.

**Why not fixed here.** A core module taking the two directory names and the
two refusal strings as arguments is a small change and it is not U58's, and
migrating the three older copies is three other units' files.

**Closes when:** one module in `core` owns both and the analysis package calls
it, with R-248's count reduced by the same move.

---

## R-275. `analyze.restamp` writes the file tag only, under a declaration that names the database too

**Found:** at the U58 authoring pass, 2026-09-07, and sharpened by the altitude angle.

The registry entry for `analyze.restamp` declares `writes` of `files` and
`db_metadata`, a doctor check on `rekordbox.pins`, and the cloud sync gate,
after the source system's two scripts, `energy_restamp` for the file tag and
`energy_rerate` for the star rating. `handle_restamp` writes the `energylevel`
tag and nothing else. The gap is visible rather than silent: every item report
carries `db_written: false`, and the queueing envelope and every resume
envelope carry the warning `db-metadata-not-written`. The doctor check and the
gate still stand for a write that does not happen, which is the source system's
own shape, since its restamp was file tag only and its re-rate a separate
deliberate step.

**Measured cost.** A person who restamps a back catalogue and reads the item
count as the whole of what the source system's pair did. The warning is the
mitigation and it was driven.

**Why not fixed here.** The re-rate is a guarded database write with the
manual rating rule behind it, `write/metadata.plan_rating_backfill` exists for
it, and it is a second worker's worth of decisions this unit did not have the
bound for.

**Closes when:** a re-rate lands beside the restamp and the warning goes, or
the declaration narrows to `files` and drops the database preconditions.

---

## R-276. The vocal calibration is written and nothing in this build reads it

**Found:** at the U58 review, 2026-09-07, by the altitude angle.

`crate analyze calibrate` fits the vocal cut by Otsu over the voxlevel tags a
folder's files carry and writes `vocal_calibration.json` under the library
state directory. `cli/converge.py` passes `vocal_threshold=None` to the rebuild
with a comment saying nothing reads the calibration file yet, and no other
reader exists. The check's detail says so in its own text.

**Measured cost.** A person who calibrates, rebuilds, and finds no track under
"with vox". The detail line is the only thing that tells them why.

**Why not fixed here.** The reader belongs to the routing and rebuild workers,
which are U53's files, and D7 wants the threshold handed to the router by its
caller rather than imported, so the reader is that caller's.

**Closes when:** a `load_vocal_threshold(cfg)` beside `energy.load_calibration`
is what the converge and rebuild callers pass, driven.

---

## R-277. A track finalized while the model was unavailable is never scored again

**Found:** at the U58 review, 2026-09-07, by the line by line angle.

`handle_run` skips any file whose name already carries the head, which is the
resume marker the source system used and the one this package documents. A
track analysed on a machine with librosa and no model is renamed with its head
and tagged with no voxlevel, and every later `analyze run` skips it as
finished. `analyze.restamp` rescores energy only. The verb that would re-score
vocals, `analyze.vocals`, is the planned one U58's brief put out of scope, and
the source system's `dj-vocal-restamp --force` is the behaviour it owes.

**Measured cost.** Driven on the fixture: a model that fails to load reports
`vocal-model-unavailable`, the file is finalized, and a second run reports
`skipped-prefixed`. The calibrate verb then reports the vocal cut skipped for
want of scored tracks, which is true and offers no way forward.

**Why not fixed here.** The re-score is the planned verb's whole job, and a
force flag on `analyze run` would re-run key and tempo detection on every
finished file to reach the one pass that is missing.

**Closes when:** `analyze.vocals` lands with a path that scores files already
carrying the head.

**CLOSED by U25, 2026-09-11.** `cratekit.vocals.cli.handle` scores a
Camelot-prefixed file and writes the three vocal tags. `analyze.run` still
skips the same name. Driven through the dispatcher on a fixture.

---

## R-278. The calibrated head decodes and measures twice, and no feature vector survives

**Found:** at the U58 review, 2026-09-07, by the efficiency angle. Not measured on the tree.

`handle_run` decodes each track once at 22050 for key and tempo and again at
32000 for the model, sequentially in one process, which is the two pool
design's answer applied where the pool boundary does not exist. On the
calibrated path `detect.analyse_file` runs a harmonic separation and an onset
envelope for tempo, and `energy.features_from_samples` runs both again on the
central slice. Neither worker persists the feature vector, so `calibrate` and
`restamp` re-measure every track from the audio, and the `energy_feature_cache`
state file `core.config` declares is not written by anything.

**Measured cost.** Unmeasured. The reviewer's estimate was one to two seconds a
track on the calibrated path and a full re-decode per track on every restamp,
which on a two thousand track library is the difference between minutes and an
hour. No number here was taken on the tree, and the entry says so.

**Why not fixed here.** Sharing samples across the head and the model changes
the detect seam's signature, sharing the separation changes the measurement the
restamp must reproduce exactly, and the cache is a state file with a snapshot
role that a writer has to honour. Each is a decision, none was in the bound.

**Closes when:** one decode feeds both passes in the worker, or the cache is
written and read and a restamp after a re-weighting costs a lookup per file.

**NARROWED AT THE SECOND REVIEW, 2026-09-08.** The double measurement was also
a DIFFERENT measurement: the head handed its whole track integer tempo into
the vector and the restamp measured its own from the slice, so the two paths
scored one file against one calibration with two tempo readings. That half
is fixed, the vector measures its own tempo everywhere. The window difference
between a sliced full decode and an offset decode is R-287, and the per item
re-read of the calibration is R-286.

---

## R-279. `analyze.calibrate` measures a folder inline, in the shell process

**Found:** at the U58 review, 2026-09-07, by the efficiency angle.

The calibrate verb walks the folder, measures every track through the bound
extractor, and fits the calibration, all in the process that ran the command.
The module's first line says the heavy passes are queued and never run inline
(KTD26, R22), and this verb is the one exception in the package: no job, no
pool, no resume. A kill at the last track discards everything.

**Measured cost.** None on the fixture. On a real folder the cost is the whole
measurement, once per interruption.

**Why not fixed here.** A calibration is one value fitted over many
measurements, so its job shape is a map then a reduce, which none of the
existing workers has needed; a pool without a job keeps the inline shape and
adds the spawned child seam problem `light.init_pass` already records.

**Closes when:** the measurement is a queued job whose items are the tracks and
whose reduce fits the calibration from the committed reports.

---

## R-280. Three decode sites, a sixth name template builder, and a second rename tail

**Found:** at the U58 review, 2026-09-07, by the reuse angle.

`detect.analyse_file`, `energy.features_from_path` and `vocal.decode` each
carry the librosa import guard, the load call and the broad except returning
None. `analysis/cli.py` builds the `NameTemplate` and `NameBudget` from
`cfg.naming` by hand, as `write/naming_cli.py`, `intake/repair.py`,
`setbuilder/cli.py`, `cli/reports.py` and `acquire/match_cli.py` already do,
and its claim then rename then release sequence in `_finalize` is
`naming_cli`'s line for line. The analysis rename and the naming verb's rename
agree about the template only because both copied the same two lines.

**Measured cost.** None to a user today. A decode level fix, a duration cap or
a resample argument, has to land three times; a second marker rule has to land
six.

**Why not fixed here.** `core.naming` has no constructor from the naming
section by design, to keep naming free of a config import, and adding one is a
change to five other modules' call sites.

**Closes when:** one decode helper with a rate argument serves all three sites,
and `naming` owns a template and budget builder over the naming section that
the six sites call.

---

## R-281. `analyze.validate` says nothing was scored, and nothing can be

**Found:** at the U58 authoring pass, 2026-09-07.

The validate verb reports one check, status `unavailable`, no remedy, saying no
validation scorer ships in this build. That is the honest version of the
`awaiting` check with a report defect remedy it replaced, and it is still a
verb that does nothing. The source system's harness scored detected keys
against an incumbent's tags on a library that carried them; this build has no
labelled set format and no incumbent to score against.

**Measured cost.** None. A person who runs it is told the truth.

**Why not fixed here.** A labelled set format is a decision about what ground
truth looks like for this product, and the analysers it would score have not
run over a real folder (R-133).

**Closes when:** a labelled set format exists and the verb scores the
analysers against it, or the entry is withdrawn from the registry and the
parity table.

---

## R-282. The head still folds a missing extra into a keyless track inside the detector

**Found:** at the U58 review, 2026-09-07, by the altitude angle. Partly fixed.

`detect.analyse_file` returned one None for three states: the extra absent, the
file undecodable, and no key found. U58 gave the undecodable file its own
terminal, `skipped-undecodable`, and guards the absent extra in the worker with
`detect.heavy_available` before the detector is asked. Inside the detector the
first and third are still one None, so a caller other than the worker, the
batch entry point `run_batch` for one, reads a slim install as a folder of
keyless tracks.

**Measured cost.** None through the worker, which is the only caller in `src`.

**Why not fixed here.** The vocal pass's shape, a named reason per absence, is
the fix, and applying it to the detector means the light pass and the batch
result grow a reason field the unit's bound did not cover.

**Closes when:** the detector returns a terminal for the absent extra as it
does for an undecodable file, and the worker's separate guard goes.

---

## R-283. `analyze.restamp` has no rename recovery, and the rule the run uses cannot give it one

**Found:** at the U58 review over the whole branch, 2026-09-08, by the removed behaviour angle.

`handle_restamp` resolves its file through `_item_path` and refuses a missing
one as `source-missing`. A restamp queued over a folder of unheaded downloads,
then an `analyze run` driven over the same folder first, renames every file
under its head before the restamp resumes, and every restamp item fails. The
run's own recovery does not transfer: it reads the rename intent its OWN
attempt wrote before its rename, and the restamp's file was renamed by another
job, which wrote nothing the restamp can see. Matching a headed file by its
stripped stem is the guess the run stopped making in the same round, because
it reported a deleted source as analysed when an older twin sat beside it.

**Measured cost.** A failed restamp job with a remedy that works, since queueing
the restamp again over the folder takes the headed names. Driven on the
fixture for the run; the restamp shape is read from the same code path.

**Why not fixed here.** An item identity that survives a rename is a change to
what the queueing verb records, and the honest shape is probably a restamp that
refuses at the queue a folder holding files with no head, which is a decision
about what a restamp is for.

**Closes when:** a restamp item is a headed name by construction, or the item
carries an identity a rename does not change.

---

## R-284. `run_batch` binds the seams in the parent and the pool children start unbound

**Found:** at the U58 review over the whole branch, 2026-09-08, by the removed behaviour angle. Pre-existing for the detector, extended to the decoder by U58.

`analysis.run.run_batch` binds the detector, the vocal loader and now the
decoder as module state in the calling process, and `light.run` and
`vocals.run` spawn children with no initializer. On a pooled plan a child
imports `light` fresh with nothing bound, runs the real `analyse_file`, and
the vocal children report every partial as model unavailable. A caller's fake
detector, model and decoder are ignored and the batch reports skipped or
unscored tracks in their place.

**Measured cost.** None from any verb. The two workers run per item in the
driver's own process and never enter `run_batch`, and `run_batch` has no caller
in `src` beyond its own module. Not driven on a pooled plan.

**Why not fixed here.** A pool initializer that re-binds fakes across a spawn
boundary is R-226's limit again, and the batch entry point is not on the path
either worker takes.

**Closes when:** the pool carries an initializer that binds the seams in each
child, or `run_batch` is retired in favour of the per item workers.

---

## R-285. The detector seam carries state the worker has to recognise

**Found:** at the U58 review over the whole branch, 2026-09-08, by the altitude and simplification angles.

`analysis/cli.py` keeps `_BOUND_DETECT`, a shadow of `light._DETECT`, so
`_fake_detect_bound` can tell the module's own partial from a test's, and it
reads `light._DETECT` one line after using the `light.bound()` accessor the
unit added to avoid naming it. The calibration is re-read from disk and a new
partial bound on every item. `_finalize` and the report accept both `rate`
and `bpm` as the tempo key with the opposite precedence from `run._as_result`,
and a detector result carrying a key and no tempo raises `TypeError` in the
worker, which the item boundary reports as a defect to file rather than as a
named shape.

**Measured cost.** None to a user through the shipped detector, which always
returns `rate`. The next seam needing per job state, the vocal threshold for
R-276 or a device choice for the loader, copies the identity trick or breaks
it, and R-282's cleanup of `_require_heavy` cannot land while the worker still
has to know which detector is bound.

**Why not fixed here.** Passing the calibration through `light.analyse` changes
the seam's signature for every caller including the batch fakes, and the
tempo key normalisation belongs in the same change.

**Closes when:** `light.analyse` takes the calibration as an argument and
normalises the detector's result to one tempo key, and the shadow binding and
its identity check go.

---

## R-286. The undo log is read and rewritten whole for every restamp item

**Found:** at the U58 review over the whole branch, 2026-09-08, by the efficiency angle. Not measured on the tree.

`energy.record_previous` takes the lock, parses the whole undo log, adds one
entry and atomically rewrites the whole file, once per item. Over a job of n
tracks that is n reads and n rewrites of a file that grows to n entries, and a
second restamp over the same folder pays the same again to record nothing.
The calibration JSON is likewise re-read and re-parsed per item on both
workers, which the docstring justifies by a calibration written between two
jobs driven by one process.

**Measured cost.** Unmeasured. The reviewer's estimate over a five thousand
track library was several million entry serialisations and five thousand
fsynced replaces. No number here was taken on the tree.

**Why not fixed here.** A line per entry log is a format change to a state
file `core.config` declares as the only surviving copy of every pre restamp
value, and a reader of the old format has to survive the change; a per job
batch means the log is not durable per item, which the per item design chose.

**Closes when:** the log is appended a line at a time under the lock and read
whole only by whatever restores from it, and the calibration is cached on its
modification time.

---

## R-287. The run and restamp paths still decode different windows of one file

**Found:** at the U58 review over the whole branch, 2026-09-08, by the cross file angle. The tempo half was fixed in the same round.

`detect.analyse_file` decodes the whole file and `energy.features_from_samples`
slices the central segment of those samples, while `energy.features_from_path`
asks the decoder for the central segment by offset and duration. For a lossless
file the two windows are the same samples; for a lossy one the offset decode
lands on a frame boundary and the slice does not, so the two vectors differ at
the edges. The tempo feature no longer differs, since U58's second round made
the vector measure its own on both paths, but the calibration is fitted from
the restamp path and scores the run path's window.

**Measured cost.** Unmeasured. A track near a decile cut could take one level
under `analyze run` and its neighbour under `analyze restamp` with nothing
changed, and the undo log would record that as a previous value. No fixture in
the suite decodes real audio, so the size of the edge difference is not known.

**Why not fixed here.** One decode serving both passes is R-278's closing
condition, and it changes the detect seam's signature.

**Closes when:** R-278 closes, or a test over a lossy fixture shows the two
windows produce one level.

---

## R-288. `_audio_in` and `tagging.tag.audio_files` derive different item sets from one folder

**Found:** at the U58 review over the whole branch, 2026-09-08, by the reuse angle.

`analysis/cli._audio_in` walks one level with `iterdir` and returns names;
`tagging.tag.audio_files` walks recursively with `rglob` and returns paths.
Both filter on `AUDIO_EXTS`, and the analysis one now also drops dotfiles. So
the same folder queues different item sets under `tag folder` and `analyze
run`, and a nested download folder is fully tagged and only its top level
analysed. The same review found the locked JSON read, modify, write spelled a
fifth time in `energy.record_previous`, beside `label/marks`, `outbound/ledger`,
`sync/watermarks` and `deletion/watermark`, and the calibrate verb's two hand
built zero envelopes already drifted in status, `skipped` against `failed`,
with nothing making the difference deliberate.

**Measured cost.** None driven. A person who tags a nested folder and then
analyses it finds the sub folders untagged by the second verb and has to
learn which verb recurses.

**Why not fixed here.** Whether analysis should recurse is a decision the
source system did not make either way, and the one helper with a `recursive`
argument is `tagging`'s file, which is U56's.

**Closes when:** one helper in `core` derives a folder's audio items with the
recursion and dotfile rules as arguments, and both verbs call it; the locked
JSON update joins `core.config` beside the atomic writer.

## R-289. The acquisition staging tree is a dotfile, and `tagging.tag.audio_files` walks dotfiles

**Found:** at U54's review, 2026-09-08, by the reuse angle, and driven.

`ACQUIRE_STAGING_DIRNAME` is a dotfile, and the comment above it says that is
safe because "the folder walks that queue tagging and analysis skip dotfiles".
Half of that is true. `analysis/cli._audio_in` does skip them, and it walks one
level with `iterdir` so it would never descend into the tree anyway.
`tagging.tag.audio_files` walks with `rglob("*")` and filters on extension
only. Driven: `audio_files(d)` over a directory holding
`.cratekit-acquire-staging/<job>/0/1.mp3` returns that file.

**Measured cost.** `crate tag folder <download_staging>` queues partial
downloads left by a killed attempt and files `checked_landing` refused and
deliberately left as evidence. Nobody has run it, so the cost is the reachable
shape rather than an incident.

**Why not fixed here.** The fix lands in `tagging/tag.py`, which is U56's file
and not this unit's, and the alternative, moving the staging tree out from
under `download_staging`, moves where the adapter is pointed. R-288 already
records this walker's asymmetry from the analysis side; this entry is the
acquisition consequence of the same shape.

**Closes when:** `audio_files` gains the dot skip its neighbour has, or the
acquisition staging tree moves outside the configured download root.

## R-290. A blocked job reports outcome `ok` and exits 0, in every queued verb

**Found:** at U54's review, 2026-09-08, on the park path this unit added.

`drive` returns normally with the job `BLOCKED`, and the shell then builds the
envelope with the default `outcome=Outcome.OK, code=ExitCode.OK`. The block is
legible only inside `data.cause`. `Outcome.BLOCKED` exists for exactly this.

**Measured cost.** Anything wrapping the verb, a sweep or the sync layer, reads
a clean success while the provider may have just walled the account. Driven
through the park test, which asserts `ExitCode.OK` today.

**Why not fixed here.** It is not this unit's defect and not this unit's to
change. `master`, `adopt` and `tagging` all report a closed job the same way,
and `ctx.envelope` has no cause parameter, while `output.envelope_problems`
requires a top level cause exactly when the outcome is not a success. Reporting
`BLOCKED` honestly therefore means changing the envelope contract for every
queued verb at once, which is a unit rather than a line.

## R-291. Per item staging directories are created and never removed

**Found:** at U54's review, 2026-09-08.

`staging_dir` clears a directory on the NEXT attempt at the same job and
ordinal. After a successful commit the emptied directory stays, and a refused
landing's file stays inside it, deliberately, since the refused file is the
evidence for diagnosing the next demotion. Nothing ever sweeps either.

**Measured cost.** Unbounded growth under `download_staging`, one directory per
item of every job ever run, and with R-289 unbounded growth of files a tagging
sweep would pick up.

**Why not fixed here.** The worker cannot clean up after itself: the engine
commits the staged file AFTER `handle` returns, so the only correct sweep point
is in the engine or in a maintenance verb, and neither is this unit.

## R-292. An unreadable file under a permissive policy is committed unmarked

**Found:** at U54's fix round, 2026-09-08, as the gap the fix deliberately left.

`lossy_landing` asks the probe whether the landed file is lossy, and a file the
probe cannot read answers nothing. It is not called lossy on a failed
measurement, so it is committed unmarked, which is what happened before the fix
too. Under STRICT the same file is refused as transient.

**Measured cost.** A truncated download under `allow_lossy_marked` is committed
as if it were a lossless landing. The library gains a file that is neither.

**Why not fixed here.** Refusing an unreadable file under a policy whose whole
purpose is to keep files is a different decision from the one the fix made, and
it is the person's to make, not a session's. Conservative option taken: keep
the pre-existing behaviour rather than widen a refusal nobody asked for.

**Closes when:** somebody decides whether the permissive policy refuses a file
that cannot be read at all, or keeps it.

## R-293. A broken adapter is rebuilt and re-authenticated once per item

**Found:** at U54's fix round, 2026-09-08, and driven at five for a five item job.

The fix parks the run on `AUTH_FAILED` only. `ADAPTER_BROKEN` still fails its
item, so the driver claims the next one, and the worker builds a fresh adapter
and enters a fresh session scope for it. A fifty track list against a broken
tool is fifty constructions and fifty session scopes.

**Measured cost.** Wasted work rather than harm, which is the whole reason the
two outcomes were separated: repeated failed LOGINS are what triggers a
lockout, and a broken tool does not log in successfully either. Bounded by the
list length.

**Why not fixed here.** The unit's brief asks for a mid batch adapter refusal
to fail its item and leave the job resumable so the resume redoes only that
item, and parking on `ADAPTER_BROKEN` would end a fifty track sync on one bad
file. The asymmetry is asserted by a test so it cannot be flattened by accident.

## R-294. `acquire_paced` names two exceptions, and the first caller owns the rest

**Found:** at U54, 2026-09-08, discharging R-204's first caller obligation.

`acquire_paced` wraps the session scope and the source hook in a try that
catches `AdapterAuthFailed` and `AdapterBroken` and turns them into a failed
invocation. Anything else out of `_session_scope` or `_source` propagates. The
worker does not catch it either, so it reaches `jobs.drive`'s item boundary and
becomes `internal-error` through `_internal_item_cause`.

**Measured cost.** An item fails with a defect report rather than a named cause
and a remedy. Not driven: no candidate producing a third exception from those
two hooks was found, so the reachability is UNMEASURED. Two candidates were
read and neither produces one.

**Why not fixed here.** Naming the third exception means deciding what it is,
and the honest answer is that the vendored adapter has never been driven
against a live account inside this suite. R-132's attended smoke test is where
that is learned.

## R-295. R-204 is discharged by half: two of its four symbols still have no caller

**Found:** at U54, 2026-09-08, re-running R-204's own measurement.

R-204 transferred the first caller obligation for `download.acquire_paced`,
`download.acquire_concurrently`, `adapter.dispatch_invocation` and
`adapter.adapter_names` to whoever bound the acquisition handler. This unit
bound it and called the first two, the second through the first. `git grep -n`
for the other two over `src` still returns a definition and an export line
each, and nothing else.

**Measured cost.** None yet. The obligation simply has not moved: two exported
functions still ship with no caller, and their failure paths are unreviewed.

**Why not fixed here.** `dispatch_invocation` and `adapter_names` belong to the
alternative adapter path and the doctor's inventory respectively, and calling
one to discharge an obligation would be a caller written for the obligation
rather than for the product.

## R-296. A seventh copy of the resume tail, and a third of the zero item guard

**Found:** at U54, 2026-09-08. An amendment to R-248.

`acquire/cli.py` carries its own `_reported`, `_no_op` and inline resume
branch, which is the seventh spelling of the shape R-248 records.
`adopt/shell.advance` and `tagging/shell.advance` are line for line identical
to each other, parameterised on `origin` and `nothing_to_run`, and this unit's
fix round added the same zero item refusal inline as a third copy rather than
importing either.

**Measured cost.** The fix round is the cost, measured: the guard `adopt` and
`tagging` have had for units went missing here precisely because it lives in a
copy this file does not import, and a review found it rather than the compiler.

**Why not fixed here.** Extracting the shared tail touches four shells at once,
which is R-248's own reason and unchanged by this unit.

## R-297. One request per call, so `concurrency` above one cannot be expressed

**Found:** at U54, 2026-09-08, and recorded in the worker's docstring.

The engine claims one item at a time, so the worker hands `acquire_paced` a
single request. Every request is still paced through the frozen delay, so a
fifty item job is fifty paced requests. What the item granularity cannot
express is the configured `concurrency` above one.

**Measured cost.** A configuration naming `concurrency: 4` acquires serially and
says nothing about it. Nobody is told the setting is inert on this path.

**Why not fixed here.** Honouring it means either a job level worker that
claims a batch, which is a different engine contract, or a warning the shell
raises at queue time, which is a decision about what the setting means.

## R-298. `output-exists` is only reachable after the download has been paid for

**Found:** at U54, 2026-09-08, recorded in the code at the raise site.

The destination name is the tool's to decide and is known only once the file
has landed, so the collision is detected after a full fetch. The landed copy
stays in this attempt's staging directory until the next attempt clears it.

**Measured cost.** A duplicate track costs a whole download and the pacing
delays that went with it, and provider side that is the expensive half.

**Why not fixed here.** Predicting the name before the fetch means reproducing
the tool's naming, which is the coupling the vendoring exists to avoid.

## R-299. `staging_dir` reaches into `config` for a private helper

**Found:** at U54's review, 2026-09-08.

`config._mkdir_private` is called from `acquire/cli.py`. It is the right
behaviour, a directory created with private permissions, and it is a private
symbol of another module, so nothing stops `config` from changing it.

**Measured cost.** None. Maintainer facing.

**Why not fixed here.** Promoting it to a public name is a `config` change and
every other caller of it is inside `config` itself, so the promotion wants
doing once for all of them rather than for this one.

---

## R-300. The ACRCloud status table is the source system's, corrected twice, and has met no live answer

**Found:** at U57's review, 2026-09-09.

`intake/acrcloud.py` classifies the service's status codes into families. The
families are the ones `DJ_setid/acr.py` used, with two corrections made on the
strength of the vendor's published table as remembered at review: 3015, which
the source system counted as a second quota code, is read as a miss, because
the table names it "could not generate fingerprint", a fact about one chunk's
audio; and 3100, "QpS limit exceeded", is read as transient. Neither the
source's table nor the corrections have been checked against a real answer,
because no live key is bound (R-132). 2004 is read as a miss on the same
recollection.

**Measured cost.** None today. If 3015 is a quota code after all, a spent
account is paid into chunk by chunk until the streak stop at five ends the run
under the failure slug rather than the spend slug, and a person reads "cannot
reach the service" for "out of quota". If 3100 is not transient, a rate limited
run stops after five answers with the same wrong sentence.

**Why not fixed here.** The first attended run is where the table is checked,
and it is Phillip's, not a session's.

**Closes when:** one live run has met each family at least once and the table
has been corrected or confirmed against what came back.

---

## R-301. The region host and the monthly bound are constants; a recognition config section is the home

**Found:** during U57, 2026-09-09.

`acrcloud.HOST` names one region's identify endpoint and an account belongs to
one region. `Budget.monthly` exists and nothing in the shipped path sets it, so
in production the ledger counts and never refuses: the per run cap of 400 is the
only bound a person meets. Both belong in a `[recognition]` section of the
configuration, frozen with the job like everything else the worker reads, and
neither was built here because a configuration section is a change to
`core/config.py`, its migration guards and its documentation, and the attended
binding is where the region is first discovered.

**Measured cost.** A person in another region gets an HTTP answer this build
reads as transient, five times, and a failure naming the host; a person with a
small plan is bounded only by the service's own quota code, which the source
system measured at 565 calls before anyone noticed.

**Closes when:** a config section carries the host and the monthly bound, the
budget is built from the frozen configuration, and the two constants are gone.

---

## R-302. The intake worker resolves and offers; it does not acquire, and the registry says it writes

**Found:** during U57, 2026-09-09.

A recognised track carries no provider identifier, `TrackSource.offer` and
`fetch` take a key and there is no search, so there is nothing to ask a provider
for. The worker resolves each frozen track against the frozen library, offers a
needs review row to the review queue, and commits a report that says owned,
offered or missing and never acquired. A playlist row does carry an identifier,
and acquiring it is the acquisition verb's job over a list document rather than
a second copy of that worker here. The registry entries for both verbs still
declare `writes={"xml", "files"}` and `destructive=True`, which describe the
source system's pipeline and not what this build's worker touches, which is a
report under the queue root and a review queue row.

**Measured cost.** `crate intake set` ends with tracks it cannot fetch and a
person carries the missing ones to `match.run`'s acquisition options by hand.
Anything that reads the writes and destructive flags describes a verb that in
this build touches nothing under the library.

**Why not fixed here.** Acquisition by ISRC needs a search the adapter contract
does not declare, and R-140 records why a worker must not claim an acquisition
it only offered. The registry flags are a decision about what the verb will do
once acquisition exists, and changing them twice is worse than once.

**Closes when:** a search lands in the adapter contract and the worker acquires
a missing track through it, or the registry flags are brought down to what the
worker writes.

---

## R-303. A mix URL is refused at the queue, and nothing drives the downloader

**Found:** during U57, 2026-09-09.

`intake.set` and `intake.identify` accept a recording on this machine and refuse
a web address with `intake-list-unusable`, and the help text and the registry
summary say so. `core/binaries.py` knows the downloader's install hint and
nothing in the package invokes it. The source system fetched the mix first; the
feature row still names a URL.

**Measured cost.** The dj-pipeline door that takes a SoundCloud or Mixcloud
address is a manual download away from working.

**Closes when:** a fetch step lands ahead of identification, under its own
binary check, and the URL is accepted at the queue again.

---

## R-304. Identification at the queue is un-resumable spend

**Found:** during U57, 2026-09-09.

The items are the identified tracks, so identification runs inline at the queue
and before the job exists. A crash mid set, or a spend refusal on the two
hundredth chunk, loses every answer already paid for: the ledger has counted
the calls and nothing has kept the matches. The source system wrote a raw
document per chunk and could resume from it.

**Measured cost.** Up to one full set's calls repeated after a crash.

**Why not fixed here.** A per source cache of chunk answers keyed by the
recording's digest and the offset is a new state file with a root and a
snapshot role to decide, and the honest first measurement of how often it is
needed is the attended run.

**Closes when:** identification can resume from the answers already paid for.

---

## R-305. The per drive library view is a module global standing in for a setup seam the job engine lacks

**Found:** at U57's review, 2026-09-09.

`intake/cli.py` caches the library index and the tombstone view per drive in a
module level dict keyed by the job and its attempt, with a public
`reset_cache` for the suite, because the engine's handler contract is per item
and `handlers.run_job` offers no per drive hook. `adopt/collection.py` solved
the same gap with a different key and its own reset. The next worker that
needs a per drive view will write a third.

In the same family: the zero item guard is now in its eighth resume tail while
`jobs.evidence_or_raise` still calls an itemless job a genuine no-op, and
`_refuse_an_itemless_job` in the label shell records that the check belongs to
`drive`. Both are R-248's shape.

**Measured cost.** None to a run. The suite reaches into a reset hook per
module rather than into one engine seam.

**Closes when:** `run_job` calls an optional `prepare(job, cfg)` once per drive
and passes its result to the handler, and the engine refuses an open job with
zero items in one place.

---

## R-306. The recognition ledger counts attempts the service never received, up to the streak stop

**Found:** at U57's review, 2026-09-09.

A call is recorded before its answer is read, so a crash between the two leaves
it counted. A transport that raises before any bytes leave the machine is
counted the same way, because the identifier cannot tell a refused connection
from a timeout after the send. The streak stop bounds it: five unanswered
attempts in a row end the run, so an offline machine costs five phantom calls
and not a set of them.

**Measured cost.** Five calls a month of drift per offline attempt, against a
ledger the module already calls advisory. A configured monthly bound (R-301)
would count them.

**Closes when:** the ledger distinguishes a call that was sent from one that
was not, or the monthly bound is reconciled against the account.

---

## R-307. One ffmpeg process per chunk, and the carve waits for the network

**Found:** at U57's review, 2026-09-09.

`FfmpegCarver.carve` spawns one process per chunk, writes a WAV to a fresh
temporary directory and reads it back, and the next chunk is carved only after
the previous post has answered. On a two hour set that is 288 spawns and 288
disk round trips in series with 288 network calls. A single decode sliced in
memory, or carving one chunk ahead while the post is in flight, are the two
shapes that remove it.

**Measured cost.** Unmeasured. Tens of seconds on a long set by estimate, and
the estimate was made on nothing this repository has run.

**Closes when:** the attended run measures it and it matters, or does not.

---

## R-308. `core.artifacts` landed and the four feature copies are not migrated onto it

**Found:** during U57, 2026-09-09. Extends R-240.

`core/artifacts.py` is the generic per item report helper the copies in
adopt, outbound, tagging and analysis each describe as their honest home, with
the directory names as parameters so core names no feature. Intake is its first
caller. The four copies stand, each now pointing at it, because migrating one
is a rename that moves where a committed report is read from, and the outbound
copy still sorts by filename text rather than by ordinal, so its migration is
also an ordering change past item 9999.

**Measured cost.** None to a run. Five spellings of one helper until the four
are moved.

**Closes when:** the four copies call `core.artifacts` and are deleted.

---

## R-309. `acrcloud` and `core.artifacts` reach into `config` for private helpers

**Found:** at U57's review, 2026-09-09. R-299's class.

`config._mkdir_private`, `config._exclusive_lock` and `config._CAN_SET_MODE` are
called from `intake/acrcloud.py` and `core/artifacts.py`. Each is the right
behaviour and a private symbol of another module. `outbound/ledger.py` and the
tagging artifacts copy already do the same, so promoting them wants doing once
for every caller, as R-299 says.

**Measured cost.** None. Maintainer facing.

**Closes when:** R-299 closes.

---

## R-310. `frozen_rows` and `acquire.frozen_tracks` freeze a `Wanted` by hand, differently

**Found:** at U57's review, 2026-09-09.

`intake/cli.py` freezes nine fields of a `Wanted` and thaws them back;
`acquire/cli.py` freezes three. The review found the intake freezer had dropped
`other_reading`, which is the exact defect a single serializer prevents, and the
acquisition freezer still carries no version or spelling. Both refuse a provider
row without an identifier by position with slightly different sentences.
`Wanted` has no `to_json` or `from_json` while `Candidate`, `Acquisition` and
`TrackMatch` do.

**Measured cost.** None driven. The acquisition worker never thaws a row, so its
narrower freeze costs nothing today.

**Closes when:** `Wanted` serializes itself and both freezers call it.

---

## R-311. Nothing ties a verb's doctor checks to the gate it actually runs

**Found:** at U57's review, 2026-09-09.

`intake.set`'s registry entry declared `binary.ffmpeg` and `credential.provider`
while its gate refused on ffmpeg, ffprobe and the two recognition keys, and the
suite was green: doctor derives its per verb readiness from the declaration and
the verb derives its refusal from `recognize.BINARIES` and the credential
names, and no test compares the two. This unit corrected the entry by hand and
pinned it in one test; the general guard does not exist.

**Measured cost.** A machine doctor calls ready refuses at the verb, for any
verb whose gate and declaration drift.

**Closes when:** a test derives each gated verb's required binaries and
credentials from the gate and asserts the registry declares them.

---

## R-312. The resort is additive, so a genre change leaves the track in two places

**Found:** during U53, 2026-09-10, while binding the `route.resort` worker.

`route.resort` re-derives the declaration and writes back what the database
lacks, through the same engine the rebuild uses. That is the whole of what a
re-place can be in this build, because
`cratekit.write.trees.write_tree_membership` is additive by construction and
nothing in the package removes a membership row from the database. The XML half
has `apply_playlist_changes` and `apply_unplaced_changes`; the database half has
no counterpart.

So after somebody changes a bucket assignment or an energy band, the resort puts
the track in its new sub and leaves it in the old one. The engine's convergence
report names the leftovers as `unexpected` differences, so the state is visible,
and the verb's registry summary, "re-place already-routed tracks after a genre
or energy change", promises more than the verb performs.

**Measured cost.** A track appears in two subs after a resort, and the tree
stays unconverged for the duration. Nothing is lost and nothing is silent: the
convergence check reports each leftover by identifier.

**The options, and the conservative one taken.** Removing the stale membership
needs a database delete, which is a new capability against a whitelist that
today permits only additions, on the one path that would let a defect in a
derivation delete a person's playlist contents. Recorded rather than built.

**Closes when:** either a governed removal path exists and the resort uses it,
or the registry summary is reworded to say the verb is additive and the
convergence check is what names what is left over.

---

## R-313. `route.unplaced` declares that it writes and it only reports

**Found:** during U53, 2026-09-10.

The registry entry carries `writes={"db_tree"}` and `destructive=True`. The verb
opens the database read only, walks each governed tree, and reports the active
rows no tree holds. It takes no session, no lock and no acknowledgment, and it
writes nothing.

The declaration is what doctor derives its per verb readiness from and what
conformance 6 quantifies over, so the over-claim costs a person three health
checks they do not need for a report, and it puts a read only diagnostic in the
population of verbs a reader would call dangerous.

**Measured cost.** A person is told to close rekordbox before running a report
that would have been safe with it open.

**Closes when:** the entry drops `writes` and `destructive`, or the verb gains
the sweep the declaration describes. The name argues for the second: the source
system's `dj-sort-unplaced` MOVED tracks, and this build's `route.inbox` is
where that act now lives.

---

## R-314. Nothing in the suite reaches the addressability refusal, composite included

**Found:** at U53's mutation table, 2026-09-10, measured twice.

`rebuild.assert_addressable` refuses three shapes: two declared destinations on
one display pair, two on one node, and one display pair carried by two nodes.
Deleting the CALL to it from `plan_destinations` killed zero tests over the full
suite, 7136 collected. The composite METHOD asks for on a user facing zero was
run and is also zero: disabling the duplicate node refusal INSIDE the function
killed nothing either, 7140 collected.

So the guard is not held by one call site that happens to be untested. Nothing
anywhere in the repository produces a destination set that collides, and every
assertion about this function is about the code rather than about its effect.

**Measured cost.** Unmeasured, and that is the finding. The refusal's own
docstring names what it costs when it does not fire, tracks written into two
playlists at once and a node map that makes it permanent, and this unit could
not produce the input, so the reachability is unmeasured rather than absent.

**Not this unit's to fix, and this unit is why it is visible.** `plan_destinations`
is an extraction: the call sat inline in `rebuild_tree` and had the same zero
coverage there. Lifting it is what made the row measurable.

**Closes when:** one test builds a taxonomy where two declared destinations
resolve to one display pair, drives a rebuild over it, and asserts the refusal,
with a second for the node collision.

---

## R-315. The rebuild's actor is frozen on the payload and read by nothing

**Found:** during U53, 2026-09-10.

`crate rebuild` refuses an empty `--actor`, freezes it on the job payload, and
`rebuild_argv` rebuilds it onto the resume command line. No worker reads it. The
one place the engine records a decision against a person is the convergence
disposition, which a rebuild does not write, and handing a frozen string to a
call that records an assertion is exactly what R34 forbids.

So the flag is a required input whose only effect is that it is recorded on the
job row and reproduced on the resume.

**Measured cost.** None to correctness. A person is required to name themselves
for a value nothing consults, which is the shape that eventually gets defaulted
by somebody who notices it does nothing.

**Closes when:** either the actor reaches a record that keeps it, or the verb
says plainly in its help that the name is recorded on the job and nowhere else.

---

## R-316. Neither new worker derives the vocal dimension, and no surface says so

**Found:** during U53, 2026-09-10.

`rebuild_governed_tree` passes `vocal_threshold=None`, which is the same answer
the convergence report gives and for the same reason: nothing in this build
reads the calibration file. `derive_from_taxonomy` then names `vocal` in its
gaps tuple and `declared_membership` returns it, and the rebuild worker drops
that tuple on the floor. The `route.inbox` apply drops it too.

So a library whose taxonomy declares the additive vocal sub-playlist gets a
rebuild that never writes it, and the envelope reports the write as ordinary.
The engine did its part: it said what it did not compare. The two callers this
unit added are where that sentence stops.

**Measured cost.** A person with vocal playlists declared runs a rebuild, sees
a clean job, and the vocal dimension is not filed. The convergence check names
it under `not_compared`, so the answer exists in a verb they have not been told
to run.

**Closes when:** both workers carry the gaps into their envelope as a warning,
which is the wording `handlers.drift_warnings` already establishes for
"something about this run is not what you would assume".

---

## R-317. A confirmed intake plan does not say which trees it will be written into

**Found:** during U53, 2026-09-10.

`route.inbox` offers a plan whose items are the files in the intake folder and
whose digest is over exactly those items. The apply then writes into EVERY tree
the registry records as native. On today's shipped taxonomy that is one tree, so
the two agree; on a library with several, a person confirms a list of files and
gets writes into trees the plan never named.

The digest deliberately does not cover the trees, because a decision bound to
the registry would be refused as stale for a reason that has nothing to do with
the offer the person read. So the fix is to SHOW the destination rather than to
widen the digest.

**Measured cost.** Unmeasured today: no shipped taxonomy declares two routing
trees, and the registry cannot hold a native record for a tree the taxonomy does
not declare. One candidate was driven, the shipped template, and it produces one.

**Closes when:** the plan's totals name the trees the apply would write into.

---

## R-318. The apply counts what it skipped and never says which files

**Found:** during U53, 2026-09-10.

`write_tree_membership` returns a `skipped` tuple of `RowMatch` values, one per
declared file that reached no single active row: not imported, claimed by two
rows, or a path no prefix maps. `apply_inbox` reduces that to a count.

The intake folder is exactly where the interesting case lives. A person drops
twenty files in, imports none of them, confirms the plan, and is told
`added: 0, skipped: 20` with no reason and no file names, which reads as a
failure of the verb rather than as a step they have not taken yet.

**Measured cost.** A confirmed apply over an unimported intake folder gives a
person a number and no next act.

**Closes when:** the totals carry a reason per skipped file, the way
`routing_pass.resolve_placements` already does for the deferred pass, whose six
placements are the vocabulary this should reuse rather than invent.

---

## R-319. A stray file in the intake folder is offered a placement it can never receive

**Found:** during U53, 2026-09-10.

`_inbox_items` lists every file in the intake folder that is not a dotfile,
whatever its suffix. The apply reads tag truth for each one, and `read_truth`
never raises for an unreadable file: an absent reading routes to the declared
fallback. So a text file, a cover image or a partial download is offered a
destination in the plan, and then reaches no collection row and lands in the
skipped count of R-318.

`library_truth` does not have this problem, because it filters on
`tags.SUPPORTED_SUFFIXES`, derived from the tag module's own table. This lister
predates that and filters on nothing.

**Measured cost.** Plan noise, and a skipped count inflated by files that were
never candidates. Nothing is written and nothing is lost.

**Closes when:** `_inbox_items` filters on the same suffix table `library_truth`
derives from, so the two agree by construction about what a track is.

---

## R-320. Two records of the pending work, and nothing compared them

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
`owed_by_unit` and a network-free `closing` check that refuses a message closing
a unit either register still owes, wired three ways. `contradictions()` now reads
both registers. Rule A refuses a register key naming a command-line module no verb
declares, because such a key can never be satisfied and its unit's close becomes a
permanent exit 2.

**The check recognizes every keyword GitHub acts on, not the one the contract
uses.** The first version matched `^Closes #n$` anchored to a line and reported
clean on `Fix`, `Fixes`, `Fixed`, `Close`, `Closed`, `Resolve`, `Resolves`,
`Resolved`, the colon form, trailing punctuation, a comma list, and the inline
form, every one of which closes the issue and cascades. Git's own comment lines
and the `commit --verbose` diff are stripped first, or a template line would
refuse a commit that closes nothing.

**It caught its own author, which is the only evidence worth having.** Two
commits on this branch documented the closing keywords by listing them with a
real issue number, so their bodies contained twelve live closing references
between them. Merged to `main`, GitHub would have closed two unrelated units and
cascaded every unit waiting on either. `board.py closing --since main` refused
the branch, the example numbers were replaced with a non-numeric placeholder, and
the trees are byte-identical before and after. A check written that afternoon
caught a defect its own author shipped the same afternoon, in the one shape
nobody thinks to look at: prose about the rule is subject to the rule.

**Residual in the hook path, stated rather than hidden.** The commit-msg hook is
handed the message BEFORE git's cleanup, so it removes git's comment lines and
cuts at git's scissors line. That is right for the editor path, where a template
comment would otherwise refuse a commit that closes nothing. It is wrong for `-m`
and `-F`, whose cleanup mode is `whitespace`, defined as "same as strip except
#commentary is not removed", and **two** shapes are lost there rather than one: a
real trailer on a `#`-leading line, and a real trailer below a genuine
git-shaped scissors line, because under `whitespace` git does not cut at a
scissors line at all. Both reach history and close the issue while the hook
reported clean.

Detecting the cleanup mode from inside the hook means reading the same
configuration git is about to apply, which is not worth it, so **the hook is
best-effort against those two shapes and CI is authoritative**. The CI path reads
post-cleanup messages and now strips nothing at all, so it catches both.

Two more, pre-existing and recorded rather than fixed. `re-fixes #NN` fires,
because the lookbehind rejects a keyword preceded by `/` or a word character but
not by `-`; GitHub's own behaviour there is ambiguous, so the refusal is not
clearly wrong. And with `core.commentChar` set to anything but `#`, both the
comment pattern and the scissors pattern miss, so the hook scans the entire
verbose diff. Neither is new.

**Merge order: the gap was never a silent miss, and the fix is a better message.**
An earlier draft of this entry said Rule B catches the U36 and U32 key
disagreement only if U32 merges first. That was wrong, and wrong in the
reassuring direction. `pending_units()` keeps a unit owed for as long as its
entry sits in the register, so if U36 merges first and lands a differently named
module, U32 is **still owed** and Rule B refuses U32's close in either order. The
failure was always loud.

What order changes is only WHEN the diagnosis arrives, and a substring rule that
asserted the mismatch was measured and rejected: `cratekit.core.restore` is U32's
LIVE key today, so such a rule would eventually go red against a unit that did
nothing wrong, which is a bad trade for moving a diagnosis earlier.

Taken instead, with no heuristic surface: when Rule B refuses, the message names
the sibling modules present in the key's parent package. A person reading a
permanent exit 2 is told "cratekit.write.rebuild is absent and write already
contains tree_rebuild" rather than guessing. Verified to produce that note for
the simulated case and **no** note for `cratekit.core.restore`, which has no near
miss in its package.

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

---

## R-321. What the soft-delete guard cannot see, and two gaps in the gate contract

**Found:** 2026-08-02, by the second adversarial review of
`fix/conformance-3-and-soft-delete-reader`. **Needs its own issue.**

Three unrelated things, filed together because all three are "the assertion is
correct and its reach is narrower than a reader would assume".

### The guard's known blind spots

`tests/_source_guards.py:permissive_soft_delete_reads` catches a falsey default
at the call site however the column and the default are spelled, an alias chain
of any depth, a splatted argument pair, and three routes that launder a correct
read one line later. Verified against fourteen evasions and nine correct shapes.

**Not caught, and each needs inference this does not have:**

1. **A row subclass with a falsey class-level default** plus a plain attribute
   read. `class Row: rb_local_deleted = 0` makes `row.rb_local_deleted` answer
   "active" for a row that never said so, and the read looks exactly like the
   correct one. Needs type inference to know what `row` is.
2. **The column arriving from a call, a class attribute, or a dictionary
   lookup.** `getattr(row, COLUMNS["soft_delete"], 0)` and
   `getattr(row, spec.column, 0)` are invisible. One hop through a named binding
   is resolved; a hop through a container is not.
3. **A computed attribute name.** `getattr(row, "rb_" + suffix, 0)` cannot be
   read statically at all.

Recorded rather than chased because each fix widens the analyzer toward
evaluating the module, and an analyzer that guesses fires on correct code, which
is how a guard gets switched off. The pin on `SOFT_DELETE_READERS` is the
backstop: all three shapes still have to live in a module, and a new module
reading the column at all turns the pin red.

### `_MARKER_ABSENT` is defined twice and will be three times

`write/routing_pass.py` and `write/metadata.py` each define their own sentinel,
with the same name and the same purpose, and U24 adds a third alongside
`trees.soft_delete_marker`. One symbol meaning one thing in three modules is the
shape the session contract names as what a green suite cannot see. **Closes with
the U24 reconciliation**, which collapses the readers into one implementation and
should take the sentinel with them.

### The gate contract, two gaps neither assertion catches

Both are **pre-existing on `main`** and neither is introduced here, but the
assertions rewritten on this branch pin the current behaviour, so they are
written down rather than left implied.

**The actor is supplied, not derived.** `crate run decide --actor` takes the
actor as a caller-supplied argument, and conformance 3 now asserts that the
recorded decision carries it. `core/session.py:derive_actor()` says R34's
sharpest clause is that the actor must be DERIVED and never named by the caller,
precisely so an agent driving the command line cannot mint a human's assertion.
The CLI's decision path takes the weaker form and the new assertion pins it.
Which is right is a decision above this branch: the flag is what makes a decision
answerable by a second person in a later session, which is R33's whole point, so
the two rules are in genuine tension rather than one being simply wrong.

**A second run inherits the first run's decisions.** A run resumed under `--run`
carries its recorded decisions, which is correct. Nothing asserts what happens
when a decision recorded against one run is reachable from another invocation of
the same verb, and a probe confirms the whole suite stays green either way.
Neither the old assertion nor the new one covers it.

**Closes when:** the three guard blind spots are either covered or explicitly
declined in the guard's own docstring with the same reasoning; the sentinel is
single-sourced by the U24 reconciliation; and somebody rules on derived versus
supplied actors, with conformance 3 asserting whichever survives.

---

## R-322. `contradictions()` is driven by nothing, and the composite proved it

**Found:** 2026-09-10, U59, by the mutation table over the merged tree.

`scripts/board.py:contradictions` is the function that reports a board claiming
work landed that the repository says did not. It is the whole point of the audit
exiting 2, and no test in the suite executes it.

**Driven, and both halves are measurements rather than an argument.** Row
`B5_contradictions_by_number` restored the unit-number-as-issue-number indexing
this unit fixed and killed zero, promoted to the full suite. That alone is
ambiguous, because a zero can mean the guard is redundant. So it was paired with
`B5_composite`, which deletes the `node["closed"]` test entirely and makes the
function report a contradiction over every OPEN unit as well. That killed zero
too, on the full suite. The pairing is what turns the first zero from a question
into an answer: the function has no driver at all, so nothing it does can be
measured by mutating it.

**Measured cost.** The two things it can be wrong about both cascade. Reporting
a contradiction that does not exist teaches a session to ignore exit 2, which is
the failure R-115 bought a rule for. Missing one lets a close move dependent
units to Ready over work the repository says is unfinished, and `sync`
deliberately will not repair that afterwards.

**Why it is not fixed here.** `contradictions` takes the graph, and the graph
comes from `gh`. A test needs a hand-built graph, which is a fixture, and this
unit's own table shows what a fixture-shaped measurement is worth. The
neighbouring functions this unit did drive, `units_by_issue_number` and
`unresolved_closes`, are pure and testable, and both are now pinned. The one
that consumes them is not, and closing that means deciding whether a graph
double is acceptable here.

**Closes when:** a test drives `contradictions()` over a graph with a closed
owed unit and an open one, and `B5_composite` becomes a killing row.

**Closed 2026-09-10 on `relay/81`, on the terms above and measured the same
way.** Both rows were re-run verbatim from `docs/mutation/u59-rows.toml`, subsets
included, so the comparison is two measurements of one experiment rather than
two experiments: `B5_contradictions_by_number` goes from 0 to 1 and
`B5_composite` from 0 to 1. `docs/mutation/u81.md` is the table and
`docs/mutation/u81-notes.md` is the reading.

**The decision this entry asked for, taken: a double is acceptable, and WHERE it
sits is the whole answer.** Not a hand-built graph. Every derived key on a node
would then be typed beside the test rather than produced by `build_graph`, which
is this project's fourth defect pattern, a measurement taken on a fixture
authored alongside the fix. The double is the `gh issue list --json` PAYLOAD and
`build_graph` runs on it for real, so the fixture sits at the one boundary a test
here cannot cross and everything downstream of it stays measured. The drift that
shape leaves open, a payload that stops resembling what `load_issues` asks gh
for, is closed by reading the field list out of that function's syntax tree and
comparing it against the double's keys.

`contradictions` also takes the owed register as an argument now, exactly as
`unresolved_closes` does, for the reason this file gives elsewhere: a test keyed
to whatever `main` owes today passes for a reason unrelated to the code and goes
red the day somebody discharges a marker.

**Two things the closing round found that the entry did not predict.** The fix
reproduced this finding's own shape one frame up, since every driver supplies a
register and `cmd_audit` supplies none, so the default read was undriven until a
row measured it. And `cmd_audit` itself was recorded here as unreachable without
a token, which is false: every name it calls is module level and replaceable.
Both are driven now, and the false claim is corrected in the notes rather than
edited out of the row file it was written in. What remains undriven after this
is `reconcile` and the board writes under it, which is R-327.

---

## R-323. The closing check reads an issue number as a unit number when nothing maps them

**Found:** 2026-09-10, U59, by the review round, and fixed only halfway on
purpose.

A closing trailer names an ISSUE. Both registers name a UNIT. `CLAUDE.md`
already states that these usually match and are not guaranteed to.

**Measured on 2026-09-10.** Twenty four units carry an issue number that differs
from their unit number: U38 is issue #51, and U39 through U61 are issues #57
through #79. None of those twenty four was owed a module that day, which is
exactly why nothing had ever surfaced it, and it is the reason this is recorded
rather than held as a blocker. The merge bar's third condition is unmet: the
input is real and nothing currently produces it.

**What was fixed.** `contradictions()` resolves the mapping through
`units_by_issue_number`, reading the unit number off the issue title, which is
the only place it is written down. `unresolved_closes` takes the mapping when a
caller has one.

**What is left, and it is a limit rather than an oversight.** The mapping lives
on GitHub. The value of the network-free check is precisely that it runs in a
commit-msg hook on a machine with no token, so it cannot go and fetch it. It
therefore reads the reference as a unit number and SAYS SO in the refusal, which
is the honest version of a guess, not a fix for it. Against a mismatched owed
unit it still misses.

**Closes when:** somebody rules on which of the two it should be. Either the
repository carries the mapping locally, which is a third register and this
project already has two too many, or the hook accepts that it is best effort
against this one shape and the authoritative answer is `audit`, which resolves
it correctly today.

---

## R-324. U25 is closed while the verb registry still owes it two modules

**Found:** 2026-09-10, U59, on the first `board.py audit` run after this merge
armed the second register.

Issue #25 is CLOSED. `src/cratekit/cli/registry.py` carries `planned_in="U25"`
on two entries naming `cratekit.vocals.cli` and `cratekit.write.metadata_cli`,
and neither module exists: there is no `src/cratekit/vocals/` directory at all.

**This is the new check working rather than a regression.** Before this merge
`contradictions()` read one register and there are two, so the board had never
said a word about it. The moment the second register is read the contradiction
becomes visible, which is the whole reason the branch existed.

**Measured cost.** `board.py audit` exits 2 from this merge onward, and
`CLAUDE.md` tells every session to run it before ending. An exit 2 that is
always there is an exit 2 nobody reads, which converts a real guard into noise
and is how the check gets deleted.

**Why it is not fixed here.** `CLAUDE.md` gives two remedies and both are
decisions somebody has to take rather than repairs a session can perform. Either
U25 is not finished and its issue reopens, or the two verbs were re-pointed or
dropped and the markers come off. Re-pointing another unit's verbs is that
unit's judgement, which is the same reason R-320 gives for leaving seven other
markers alone, and reopening a closed issue from inside an unattended run is a
board write this session had no mandate for.

**Closes when:** somebody answers the question for U25, in either direction, and
the audit exits 0.

**One of the two remedies was taken, by somebody other than this entry's author,
and it is measured rather than assumed.** As of 2026-09-10, issue #25 is OPEN
with a state reason of REOPENED, so `contradictions()` returns nothing about it
and `board.py audit` no longer exits 2. Driven directly on the live board while
closing R-322, not read off a report:
`contradictions(build_graph(load_issues()))` is empty and `owed_by_unit()` still
answers `{25: ['cratekit.vocals.cli', 'cratekit.write.metadata_cli']}`.

So the LOUD half is discharged and the substantive half is not. The registry
still owes U25 two modules and U25 is now an open unit that owes them, which is
the register working rather than the board contradicting the repository. Issue
#80 is still open and this entry is left open with it, because whether that is
the answer for U25 or merely the quieter state is the judgement #80 exists to
make, and the session that closed R-322 did not take it.

**Closed 2026-09-11, on the terms above.** U25 is not finished. That is the
answer #80 existed to take, and it is the same answer the 2026-09-10 reopen
already wrote on #25. What was still missing was a brief a session can build
against: the issue body still described the DSP port, which is in the tree.
The body now names the two remaining shells, `analyze.vocals` and
`metadata.mytags-vocals`, the engines they sit on, R-277 as the cost of the
missing re-score, and R-133 left attended. #80 closes. The modules existing is
U25's close, not this entry's.

---

## R-325. Four maintainer facing zeros in U59's table, each with what it means

**Found:** 2026-09-10, U59's mutation table, twenty five rows.

METHOD gives a maintainer facing zero one line rather than a composite. Four of
them, and every one reads as the author could not kill it, which is the sentence
this project uses on purpose because there was no independent verifier.

- **`M7_scope_narrowed`.** Narrowing the unreadable-marker refusal from
  `Scope.RUN` to `Scope.ITEM` kills nothing on the full suite. Reclassified from
  user facing to maintainer facing during the pass, with the reason: the scope
  reaches a person only if the refusal does, and R-186 records that the producer
  of an unreadable marker was never driven. What IS pinned is the refusal
  itself, `M2_refusal_removed` kills four.
- **`M8_column_literal`.** Replacing `rb_writer.SOFT_DELETE_COLUMN` with the
  string it holds kills nothing, which is expected and still worth recording:
  the constant exists so a reader is resolvable through the import graph rather
  than being a string somebody typed, and that is a property no runtime test can
  see. `M9_column_repointed` kills eleven, so the constant's VALUE is pinned
  even though its use as a name is not.
- **`G5_reader_pin_widened`.** Turning the exact-membership reader pin into a
  subset check kills nothing, because no test adds a reader. That is the pin's
  own design: it catches a WIDENING that has not happened yet. `G6` shows it is
  live, since restoring the pre-merge membership kills one.
- **`B7_title_anchor_dropped`.** Matching a unit number anywhere in an issue
  title rather than at its start kills nothing, because no fixture title carries
  a stray unit-shaped token later in the line. `B6` shows the map is otherwise
  pinned.

**Closes when:** nothing. This is a record of a measured gap, not work.

---

## R-326. Two of the parked branch's eleven commits were already on `main`

**Found:** 2026-09-10, U59, while reconciling the collected count before the
merge.

U59's brief describes eleven commits, the first and fourth of which are the
conformance 3 work: "conformance 3 asserted the inverse of R34 and could not
drive two gates" and "conformance 3 stopped asserting that a declared gate is
ever REACHED". Both were already on `main` when this unit was taken up.
`tests/test_cli_contract.py` is byte identical between `main` and the merged
tree, and all seven of the functions those commits introduce sit at identical
line numbers on both sides.

**How it was found, and it was nearly not.** The collected count reconciled by
identifier showed zero lost ids and fifty one gained, none of them in
`test_cli_contract.py`, against a branch whose diff adds four hundred and one
lines to that file. A total-only check would have shown a healthy rise and said
nothing. This is the second time that rule has paid for itself here.

**Why it matters to a reader of the brief.** The brief says the branch carries
"five conformance and board guards" and the merge arms them all. Three of the
five land. The conformance half of this unit was a no-op, and a session reading
the brief afterwards would otherwise conclude that this merge is what armed
those assertions.

**Closes when:** nothing. Recorded so the brief and the tree do not disagree
silently.

---

## R-327. `reconcile` and every board write under it are driven by nothing

**Found:** 2026-09-10, on `relay/81`, while closing R-322 and correcting a false
claim in that task's own row file.

R-322 was the audit's DETECTOR being undriven. Closing it drove
`contradictions`, `units_by_issue_number`, the residual repoint check, and
`cmd_audit`'s exit codes. What that leaves is the other half of the audit:
`reconcile`, `project_context`, `project_items`, and the four `gh project
item-edit` writes they compose, none of which any test executes.

**The distinction is real rather than a technicality, and it is why this is a
residual rather than the next unit.** `cmd_audit` was recorded as unreachable
without a token and was not: every name it calls is module level and
replaceable, which is what made a driver possible in an afternoon. `reconcile`
is a different case. It reads a USER-OWNED PROJECT, which a repository-scoped
token cannot see at all, and `audit --labels-only` exists precisely because CI
running as `GITHUB_TOKEN` gets nothing back. So a driver for it is a double of
the GitHub project API rather than of one JSON payload, and R-322's own answer
about where a double belongs, at the producer boundary with everything
downstream measured, does not obviously transfer: there is no local function
between the API and the writes for a payload double to feed.

**Measured cost, and it is smaller than R-322's.** `sync` is idempotent and
derives everything from closure state and the graph, so a wrong write is
repairable by running it again, which is the property `board.py`'s own module
docstring names. The unrepairable half of the board, the contradiction that
`sync` refuses to touch, is the half R-322 closed. What is left is a status label
that could be wrong until the next sync, plus one shape that is not repairable
by a re-run: `reconcile` decides whether an issue is ADDED to the project at
all, and an item never added is an item no later sync sees.

**Two candidate producers were considered and neither was driven**, so the
reachability here is unmeasured and this entry says so rather than claiming
nothing produces it. `gh project item-add` failing silently, and an option id
recreated on the Status field, which `board.py` already declines to pin for
exactly that reason.

**Closes when:** somebody decides the board's write half is worth a double, and
says what shape keeps it honest given that there is no payload seam to build it
at. Recorded rather than fixed because it did not meet the bar to hold a merge.


---

## R-328. The queueing guard accepts an `enqueue` call anywhere in a verb's module

**Found:** by the `/code-review` pass on U60, 2026-09-10. Recorded rather than
fixed.

`tests/test_cli_contract.py::test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues`
parses each landed long-running verb's MODULE for a call to `enqueue`. It does not
follow the verb's own handler. So two verbs sharing a module pass on one call:
`sync.labels` and `label.import` live in `cratekit.label.cli`, and if one of them
stopped queueing while the other still did, the guard would stay green over the
false claim R-149 was.

**Measured cost: none today.** Every landed long-running verb except the
`job.resume` exemption has an `enqueue` call in its module, measured on this
branch, and the shared-module pairs share a worker too, so both halves of each
pair genuinely queue. The bar is stated in the guard's docstring: several shells
enqueue from a helper rather than from the handler, so following the handler's
own call graph would be a larger guard than the class it catches today.

**Closes when:** the guard follows each verb's handler, the function its builder
binds as `_handler`, through to an `enqueue` call, or a shared-module pair is
split so the module bar becomes a per-verb bar.

---

## R-329. The mutation driver cannot finish a batch inside a ten minute foreground call

**Found:** by U60, 2026-09-10, running its table as relay task 78.

`scripts/mutate.py` runs a full suite baseline on EVERY call, `--resume`
included (`scripts/mutate.py:957`), and `--resume` reuses finished rows only. The
full suite is 358 seconds on this tree. The null control runs on the first Python
row's derived importer subset, which is the full suite again when nothing
imports that module. A relay task runs every command in the foreground under a
600 second ceiling, and METHOD forbids a backgrounded driver. Two attempts, both
stopped by SIGINT at 570 and 575 seconds, measured zero finished rows and left
the tree clean. `docs/mutation/u60-notes.md` holds both measurements.

**Measured cost.** U60 lands with no mutation table, not even the author's. Its
rows are committed and ready. Every later unit run as an unattended relay task
meets the same wall, because the baseline alone is sixty percent of the ceiling
and grows with the suite. And promoting a zero needs a second full run inside
the same call, so a zero could never be confirmed there even if the preflight
fit.

**Options, none taken here**, because each changes the driver or how a unit is
run, and that is Phillip's decision:

1. `--resume` reuses a stored full baseline when it was taken on the same HEAD.
   Cheapest. It relaxes the check that catches a red baseline, so the sidecar
   has to carry the sha the baseline was measured on.
2. A row file names the null control's subset rather than deriving it.
3. The table runs attended, or as a runner step outside the task session, where
   no ten minute ceiling applies.

**Closes when:** U60's committed rows are measured by any route, and the route is
one a relay task can take.

**U61's correction and measurement, 2026-09-10, relay task 79. THE NULL CONTROL
DOES NOT RUN ON A DERIVED SUBSET.** `measure_batch` passes `None` and
`"full suite"` for the control at `scripts/mutate.py:1002`, whatever the first
row targets and whatever subsets the rows name. The paragraph above,
`docs/mutation/u60-notes.md` and the learning all said the control runs on the
first Python row's derived importer subset, and U60's second attempt moved a row
on that reading. The code does not do it, so that attempt could not have fit, and
option 2 above is a driver change rather than a row file change. Measured by
sampling the driver's pytest children every three seconds: the full baseline ran
from 3 to 363 seconds, the control started at 366 seconds as a second full suite
run, and SIGINT arrived at 570 seconds with the control still running. The
preflight is TWO full suite runs, about 720 seconds on this tree, before any row
and before any promotion, which no ten minute call can hold. U61's twenty one
rows are committed in `docs/mutation/u61-rows.toml` and unmeasured, and
`docs/mutation/u61-notes.md` holds the sampling. Options 1 and 3 stand as
written.

**A third table waits on it, 2026-09-10, relay task 40.** R-3's fifteen rows over
the scan's archive tier are committed in `docs/mutation/r-3-rows.toml`, each with
its expected kill written in the description, and not run, following the
learning rather than spending ceiling length calls. The tier's own tests run in
under five seconds, so the table is cheap the moment the preflight is.

---

## R-330. A job queued under `sync.all` by an older build stays in the queue with no worker and no way out but a cancel

**Found:** by U61, 2026-09-10, at its review.

Before U61 `crate sync all` queued one itemless job per enabled source under
`sync.all`. U61 took the key out of both handler tables, because nothing can
queue under it now. A queue written by an older build can still hold those rows.
`job list` and `job show` report their worker through `handlers.unbound_reason`,
which for a key in neither table says the job was queued by a different build or
under a verb that has since been removed, and a resume refuses at
`handlers._declaration` with `internal-error` and a report defect remedy. Nothing
cancels them.

**Measured cost.** Argued from the source, not driven. The producer is the pre
U61 build, and whether any real queue holds such a row is unmeasured. The rows
held no items and had no worker, so no work is lost. The cost is a stale row that
reads as a defect until somebody runs `crate job cancel` on it.

**Not fixed here** because cancelling jobs by handler key on upgrade is a queue
migration, and the refusal already says what happened.

---

## R-331. A handed decision carries no record that it was handed

**Found:** by U61, 2026-09-10, while writing `Gates.hand_off`.

`hand_off` copies the answer recorded on `sync.all.favorites.confirm` onto a new
run owned by `sync.favorites`, under `sync.favorites.confirm`, keeping the option,
the actor, the time and the digest. `Decision` has no field for provenance, so
`crate run show` on the handed run shows the person's name against a gate they
were never shown by that name, and nothing in the run record links it to the
`sync.all` run they actually answered. The job payload holds both runs, the
intake `run_id` and the gate run, so the link is recoverable from the job and not
from the run record.

**Measured cost.** An audit reading run records alone cannot tell a handed
decision from one given directly. Nothing reads run records for that today.

**Not fixed here** because a provenance field is a run record schema change,
`RUN_SCHEMA_VERSION` 1 to 2, which every reader of that file owes a migration
for.

---

## R-332. A pass that queued nothing because two sources refused names one remedy

**Found:** by U61, 2026-09-10.

When every built source refuses for itself, `sync all` raises the FIRST refusal
in declared order, with the whole per source report under `detail.sources`. On a
full profile with neither an export nor a registered label, the person is told
`outbound-export-required` and its remedy, and the label registry's refusal
rides the detail only. The human rendering prints the first cause.

**Measured cost.** Driven by
`tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`,
whose refusal reason is the favourites one. A person who fixes the export meets
the registry refusal on the next pass.

**Not fixed here** because a cause carries one reason and one remediation by
contract, and a composite cause is a vocabulary change.

---

## R-333. A checkout without the dev extra fails the commit hook check with every hook installed

**Found:** closing R-1, 2026-09-10.

The hook types are read from `.pre-commit-config.yaml` with PyYAML, which arrives
with the `dev` extra through pre-commit and is not a runtime dependency. A
checkout whose interpreter cannot import it gets FAIL at `repo.commit_hook`,
naming `pip install -e '.[dev]'`, even when both hooks are installed and
pre-commit itself runs from somewhere else, a pipx or Homebrew install.

**Measured cost.** Driven by
`tests/test_doctor.py::test_no_yaml_reader_is_unknown_rather_than_one_hook_type`,
and `crate doctor` exits non zero over it. Reachability on a real machine is
unmeasured: no checkout without the dev extra was driven.

**The decision is Phillip's.** (a) Keep the FAIL, the conservative call taken
here, because every alternative can report green over the gap R-1 exists to
close. (b) Report INFO when PyYAML is missing and both default hook files exist.
(c) Read the stages with a narrow text reader and no parser, which misses block
style lists and so under reports.

**A smaller second leg.** When the default configuration cannot be read at all,
the fresh clone install line falls back to naming only the pre-commit type,
which is the one line trap R-1 was widened over. The check reports the
configuration itself as soon as that hook exists, so the gap lasts one run.

---

## R-334. The scan still reads a binary it does not recognise as clean

**Found:** by the built in review on `relay/40`, 2026-09-10, closing R-3.

R-3's fix refuses an archive the scan recognises, by suffix or by header. The
list is closed. The review drove a `.tar.lz4` holding a session file through the
first version and it scanned clean, and that format and seven more are now
covered, but the shape survives for anything still off the list: a raw `.lzma`
stream renamed to a neutral name (its header is three bytes that ordinary data
can start with, so it is deliberately not matched), binary cpio, a disk image.
And it survives one file over, for binaries that are not archives at all. A
tracked `.db` or `.sqlite` file can hold a live token in plain bytes, and
`_read_text` returns `None` for it exactly as it used to for a tarball.

**Measured cost today, none.** `git ls-files` on `relay/40` lists 626 paths and
not one binary, so no producer exists on the tree. The cost is to the next
commit that adds one, which gets a clean report.

**The conservative call taken here** was to extend the list and record the
class, because the general fix changes what the scan accepts:

1. Refuse every tracked file the reader cannot decode, unless its exact path is
   in `ALLOWED_EXACT` with a comment saying who decided. Fail closed, and every
   future image or font costs one reviewed line.
2. Keep the closed list and add formats when one is met.

**Closes when:** Phillip picks one. Option 1 closes it; option 2 closes it back
to the ledger as accepted.

---

## R-335. Conformance 4 and 6 drive the shared surface and not the landed verbs

**Found:** closing R-5 on `relay/42`, 2026-09-10.

Both assertions were written when no adjudicating and no destructive verb had
landed, so each drives the shared machinery once per declared verb, under that
verb's own name, rather than the verb. That was the strongest thing available
then. It is not now: every adjudicating verb and twenty two of the twenty four
destructive verbs have landed, and the two assertions still drive only the
shared layer.

What each one cannot see:

1. Conformance 6 drives `session.assert_gates` directly. A landed destructive
   verb whose handler writes before it enters its session, or never enters one,
   passes it. adopt.apply's three refusals are driven in
   `tests/test_adopt_apply_cli.py` through `apply_outstanding`, and the backup
   restore's in `tests/test_write_session.py`, both below the dispatcher. No test
   derived from the registry drives a lock held elsewhere, a missing
   acknowledgment and a wrong volume through `cli.run` for a landed verb.
2. Conformance 4 offers the review item itself. A landed adjudicating verb that
   decides without offering anything to the queue passes it. Only its static
   half, which walks the verb's own module for a comma separated writer, reads
   the verb at all.

**Measured cost today, unmeasured.** No candidate verb was driven to find one
that writes before its session or decides without offering. The evidence that
exists is per verb suites, which are not derived from the registry and so do not
grow when a verb lands.

**Why it was not built here.** Driving each landed verb through `cli.run` as far
as its session needs an argument surface and fixtures per verb, twenty two of
them, and each verb also declares doctor preconditions and explicit gates a
drive has to account for. That is a unit, not a residual close.

**Closes when:** conformance 6 invokes every landed destructive verb through the
dispatcher with each of the three gates broken in turn and asserts the code and
an unchanged filesystem, and conformance 4 asserts that a landed adjudicating
verb's run leaves an item in the queue under its own handler key.

---

## R-336. The option-less trash rows state a quota consequence nobody measured

**Found:** closing R-7 on `relay/44`, 2026-09-11.

Dropbox, Box and pCloud each have a row with no option, and the note they share
says a pruned archive "keeps counting against the quota until the provider's
own retention expires". That is a claim about each provider's billing, not about
rclone, and rclone's backend help does not make it. Whether deleted files count
against the quota was not measured for any of the three. If one of them does not
count them, a person is told a prune reclaimed nothing when it did.

**Measured cost today, unmeasured.** The finding is INFO, so it refuses nothing
and fails nothing. Its only cost is a sentence that may be false.

**Why it was not settled here.** Measuring it means a real account per provider
or the provider's own documentation, and neither was available unattended.

**Closes when:** each option-less row carries a quota sentence measured against
its provider, or the shared sentence is reworded to claim only what rclone
states, that the provider keeps deleted files.

---

## R-337. Five providers rclone gives a delete option have no row

**Found:** closing R-7 on `relay/44`, 2026-09-11.

rclone 1.74.3's backend help lists a per remote delete option for `mega`
(`hard_delete`), `b2` (`hard_delete`), `jottacloud` (`hard_delete`), `yandex`
(`hard_delete`) and `pikpak` (`use_trash`). None has a row in
`_REMOTE_TRASH_POLICY`, so each reads "no row, nothing asserted", which is
honest and is not the instruction R-7 asked for. A person on one of them who
never set the option is not told it exists.

**Measured cost today, unmeasured.** No remote of those five types was driven.
The answer is INFO, never a false green.

**Why it was not built here.** Each row asserts a default and a sense, true or
false, that was only read from help text, and `b2`'s is a hide rather than a
trash, whose quota behaviour depends on the bucket's lifecycle rules. Asserting
all five from help text is the one-provider guess R-7 was about, repeated five
times.

**Closes when:** each of the five has a row whose default and sense are checked
against rclone's source or a real remote, or is named in
`_NON_TRASHING_REMOTE_TYPES` with the same evidence.

---

## R-338. An analysis share outside the library root is in no backup, and no restore puts it back

**Found:** closing R-14 on `relay/52`, 2026-09-11.

The analysis share is the `share` directory beside the rekordbox database, and
it holds every beat grid. The mirror carries it only because it normally sits
under the library root. With the database outside the root, which
`library.db_outside_root_acknowledged_on` permits and which is where rekordbox
puts it by default, the share is outside too. The mirror never sees it, the
database snapshot copies the database file and its sidecars, and the settings
directory the snapshot also copies, `Application Support/Pioneer/rekordbox6` on
macOS, does not hold it. A dead drive restored from that backup brings back every
row without its analysis, and the rows look fine.

**Measured cost.** Driven in `tests/test_analysis_store.py` and
`tests/test_backup_cli.py`: no command in the plan names the share, and the plan,
the outcome and the verb's envelope each carry `analysis-share-not-carried`. The
envelope warns at queue time and at resume. A resume whose database portion
refused raises the refusal instead of building an envelope, so that one drive
shows no warning, and the queue time warning is what that person has seen.

**Options, none taken here**, because each spends a person's storage or changes a
destructive path:

1. The share rides the database portion into each dated snapshot, as the
   settings directories do. Simplest, and it inherits the right gate, since
   rekordbox writes the share while it analyses. The source library's share
   is 3.4 GB, and a dated snapshot copies whole, so every run uploads it again.
2. The share is mirrored to one stable destination with its own dated archive,
   as the library is. Cheap per run, and it needs a fourth configured
   destination, so setup changes.
3. Either way a restore needs a matching half, and it must be planned from a
   listing. The restore clears the database's sidecars before its first
   transfer, so a copy from a snapshot that holds no share fails after the
   clearing, which is the refusal `_ran` describes.

**Closes when:** a backup in the outside layout carries the share, a restore
from it puts the share back beside the restored database, and the warning code
has no producer left.

---

## R-339. The open pins the argument, and nothing checks which file the connection opened

**Found:** by R-15, 2026-09-11, on `relay/53`.

R-15's related half landed as an AST audit in `tests/test_whitelist_membership.py`:
every `Rekordbox6Database` call in `src` passes an explicit, non empty `path=`.
That is the argument. The entry's own general form says why it is the cheap half:
refusing the live path as an argument is not the same as not reading it. The
binding decides what to open from `path`, and falls back to the rekordbox
configuration's `db_path` when `path` is empty, so a value that is present in the
source and empty at run time still opens the live library. The audit refuses only
a literal empty value. Read from the pinned binding, it also does not connect
while it constructs, so the file is chosen at the first query.

**Measured cost.** None driven. `core/rb_writer.py` refuses a missing target
before it constructs, so no producer of an empty `path` at run time was found,
and none was driven. One candidate was read and none produces it.

**Options, none taken here**, because each changes the write open path, and the
brief asked for the AST assertion:

1. After construction, compare the engine's database file with the target, and
   refuse the session on a mismatch. Cheap, and it checks the binding's
   intention rather than the connection.
2. After the canary's first query, ask SQLite which file it attached
   (`PRAGMA database_list`) and compare that. The connection that actually
   opened, which is the check R-15 names.

**Closes when:** an open whose connection is not the target file is refused by a
check on the connection, and a test drives that refusal.

---

## R-340. A report reaching a writer through another module's attribute is not caught

**Found:** by R-102, 2026-09-11, on `relay/54`.

R-102 closed with the allowlist audit following imports to their closure, and
the audit's argument is that every writer the closure reaches is a name
`FILESYSTEM_MUTATIONS` or `QUALIFIED_MUTATIONS` carries, **so a report calling it
is caught**. The second half is `filesystem_mutations`, and it resolves a
receiver to a module only when the report bound that module itself. An admitted
module's own imports are its attributes, and a chain through one is not read.

**Driven on the tree after the naming**, five report sources, each read by
`filesystem_mutations` and `forbidden_imports`:

| Report line | `filesystem_mutations` | `forbidden_imports` |
| --- | --- | --- |
| `config.save(c)`, `config` imported | caught | clean |
| `taxonomy.config.save(c)` | nothing | clean |
| `review.config.save(c)` | nothing | clean |
| `rbxml.tree_registry.write(x)` | nothing | clean |
| `rbxml.tree_registry.session.rb_writer.write_session_lock(p)` | nothing | clean |

The last one takes the rekordbox write lock from a read only report with both
structural guards green. `config` through `taxonomy` predates R-102, so the hole
is not new. What R-102 changed is that the closure made its size visible: every
module past the allowlist is reachable this way, `rb_writer` included.

**Measured cost.** None to a user. No report module spells an attribute chain
into an admitted module today; five candidates were driven and none is in the
tree. The cost is that `QUALIFIED_MUTATIONS` now names forty nine writers a
report can reach without the name check seeing the call.

**Options, none taken here**, since R-102's brief was the audit:

1. Resolve an attribute chain rooted at an admitted module through the
   closure's own import table, so `rbxml.tree_registry` resolves to
   `tree_registry` and the qualified check applies. Closes the class.
2. Refuse, in a report, any attribute read on an admitted module that names a
   module rather than a function or a class. Cheaper, and strict: it would need
   measuring against the three report modules first.

**Closes when:** a report calling a named writer through another admitted
module's attribute is reported by `filesystem_mutations`, and a planted report
drives it.

---

## R-341. Thirteen user facing zeros in U25's table, none with a composite

**Found:** 2026-09-11, U25's mutation table, twenty five rows, measured by
`scripts/mutate.py` in 6131 seconds. Eleven killed, thirteen zero on the
full suite, one refused.

METHOD accepts a user facing zero only with a composite. The cap was
spent, so none of these has one. Every zero here reads as the author
could not kill it.

The ones that are backstops of a killing row, so a composite would have
been cheap and was not run:

- **`G2_worker_extra`.** The worker extras check. `G1` already kills the
  queue check, which is the path a slim install meets. The worker copy
  is for a resume after the extra disappeared, and nothing in the suite
  queues with the extra and then unbinds it.
- **`G23_failed_job_ok`.** Re-raising a job cause. The extras refusal
  happens at the queue, so a failed item is not how the slim path ends.

The rest are unreached producers, not missing assertions about a path
the suite already drives:

- **`G5_inactive_still_writes`.** No fixture scores inactive then asserts
  the tags stayed absent.
- **`G7_foreign_job`** and **`G8_empty_resume`.** No test resumes a
  vocals job that belongs to another verb, or one with no items.
- **`G9_default_cut_zero`.** The fixture's track is at voxlevel 80, above
  both 12 and 0. `G10` already kills ignoring the cut on the unit table.
- **`G14_open_without_closed`.** Tests patch rekordbox closed, so the
  flag cannot fail.
- **`G16_no_verified_capture`** and **`G17_no_rollback`.** The apply
  path's happy tests never fail the capture or the write.
- **`G18_include_deleted`** and **`G19_unresolved_as_file`.** No deleted
  row and no unresolved path in the apply fixture.
- **`G21_dotfiles_queued`** and **`G22_folder_absent_as_empty`.** No
  sidecar and no missing folder in the vocals tests.

`G25_message_reword` refused: the old text as typed was not in the file,
so the row never ran. The extras message is still driven by `G1` and
`G3`.

**Measured cost.** None of these zeros was a silent user facing hole on
a path the suite already takes. The cost is the untested resume, the
untested missing folder, and the untested tombstone, each still possible
on a real library.

**Why not fixed here.** Two fix rounds are spent. Adding tests now would
not re-measure the table.

**Closes when:** each zero either has a composite, or a test that kills
it, or is reclassified maintainer facing with the reason.

---

## R-342. A corrupt vocal calibration is read as the default cut

**Found:** 2026-09-11, U25 review, by the absence pattern.

`vocal_cut` returns 12.0 when the calibration file is missing, which is
honest, and also when the file is unreadable, which is not. Energy's
loader refuses a corrupt calibration so a restamp cannot proceed as if
the library had never been calibrated. This one would tag from a cut
nobody fitted.

**Measured cost.** Unmeasured on the tree. `energy.write_json` is atomic,
so the producer the calibrate verb uses does not leave a half written
file. A hand edited or truncated state file would.

**Why not fixed here.** A new cause slug is pin churn, and no existing
slug names a vocal calibration. The default on absence is the product
decision the plan path needs so conformance 2 can drive an uncalibrated
fixture.

**Closes when:** an unreadable vocal calibration refuses by name, and a
missing one still defaults.

---

## R-343. A mutation driver run wrote 343 files into the real state directory

**Found:** 2026-09-16, first act of the attended U29 sitting, on this machine.

the installation state directory held a config, 16 jobs and 326 run
records, every one written at 07:20 on 2026-09-09, which is inside U54's
mutation driver run. The config pointed the library root at a pytest temporary
directory that no longer existed and named the `fake` adapter. Every run record
was `acquire.download`. One pytest process, under one mutant, defeated the
`_isolate_state_roots` redirect for its whole life and wrote to the real home.

**What is known and what is not.** The full suite run on 2026-09-16 on the
clean tree touched nothing under that path, so the leak is not live in the
current tree. Which mutant defeated the redirect was not established. The
conftest sets `HOME`, the four XDG variables and both `CRATEKIT_*` overrides,
and `platformdirs` honours `HOME`, so a mutant in `config_dir()` alone should
not have reached the real path; the answer is somewhere the sitting did not
look. `G19_frozen_config` in `docs/mutation/u54-rows.toml`, which swaps a
frozen configuration for a fresh `_load()`, is the row nearest the symptom.

**Cost.** Setup could not run until the directory was deleted, since the leaked
config is what every verb loaded. On a machine that had been set up for real
first, the same leak would have overwritten a real configuration with a
pytest one.

**Why not fixed here.** The sitting was attended and the driver is a script;
finding the mutant means re-running U54's rows under a watch on the real
directory, which is a session's work and not a sitting's.

**Closes when:** the mutant is named, the driver refuses to run a row while the
real state directory is writable by the child, or the redirect is proven to
hold under every row in the committed tables, whichever is cheapest.

---

## R-344. The volume identity is compared case sensitively and the wizard accepts diskutil's spelling

**Found:** 2026-09-16, first `crate setup` of the attended U29 sitting.

`diskutil info` prints the volume UUID in uppercase. Passed to `--volume-id`
as printed, setup recorded it as typed, and `preflight` then compared it with
`==` against the lowercase it observes through `getattrlist`, so the very
volume the wizard had just been pointed at was reported `foreign_volume`,
`library.mounted` and `library.identity` failed, and the taxonomy was not
written. A second run with the UUID lowercased passed every check.

**Why not fixed here.** A sitting fix on the identity compare is a change to
the guard every destructive verb asserts, and it belongs in a session with the
mutation table that guard already has.

**Closes when:** the recorded identity and the observed one are compared case
folded, or the wizard folds the case at record time, and a test drives an
uppercase UUID through setup and the mount check.

**Closed 2026-09-16 on `relay/83`, taking the FIRST condition and not the
second.** `preflight.same_identity` folds the case on both sides and both
compares in `resolve_mount_state` go through it, the configured mount and the
mounted elsewhere sweep. Setup still records the identity as given, on purpose:
the recorded value is also the `library_id` that jobs and watermarks are stamped
with and matched on exactly, so folding it at record time would orphan them on a
re-run that spelled it differently. The setup side test drives an uppercase UUID
through `_resolve_volume_id`, the mount check and the taxonomy write the sitting
could not make. The first mutation table caught the preflight tests asserting a
fold over an all digit identity, which is its own uppercase; they now use
lettered hex, and `docs/mutation/r83-round-2.md` shows all three compares killing.

---

## R-345. The backup destinations are used verbatim as rclone targets and nothing validates them

**Found:** 2026-09-16, first backup dry run of the attended U29 sitting.

`BackupConfig` says every field is wizard supplied and the wizard never asks
for any of them, so the four values are typed into the TOML by hand. `dest`,
`archive_root` and `db_dest_root` are passed to rclone exactly as typed and
`remote` is read only by the refusal for an unset value and by the doctor's
trash check. Typed as bare folder names, the plan was
`rclone sync <library root> <bare folder name>`, a local relative path, and
the dry run succeeded in four seconds because listing a folder that does not
exist is instant. A real run under that configuration would have copied the
library into a folder beside whatever the detached worker's working directory
was, and published a backup age for it.

**Why not fixed here.** The validation belongs in `core/config` beside the
containment rule, with the wizard question beside the others, and both are a
session's work.

**Closes when:** each destination is refused unless it names a configured
rclone remote with a colon, `remote` is derived from them or checked against
them, and the wizard asks for the four values when the backup module is on.

---

## R-346. The prompter never flushes, so a real terminal shows no question

**Found:** 2026-09-16, the first interactive `crate setup` ever run.

`cli/prompt._write` prints the question to standard error with `end=""` and
no flush, then `_read_line` blocks on standard input. Python line buffers
standard error, and a question with no newline never leaves the buffer, so the
wizard sat at a black prompt waiting for an answer to a question it had not
shown. Every test injects the writer, so no test could see it, and every
earlier run was non interactive, where the buffer drains at exit. The
workaround that carried the sitting is `PYTHONUNBUFFERED=1`.

**Why not fixed here.** One flush, and it was not made in the sitting because
the sitting was mid cutover and the rule is one unit per session.

**Closes when:** `_write` flushes after every question, and a test drives the
prompter through a real pipe rather than an injected writer.

**Closed 2026-09-16 on `relay/83`.** `_write` flushes. The test starts a real
interpreter over real pipes with `PYTHONUNBUFFERED` removed and requires the
question on standard error before it sends the answer; the unflushed writer
kills it (`docs/mutation/r83.md`, P1).

---

## R-347. A credential offered, accepted and left empty fails the whole wizard

**Found:** 2026-09-16, the second interactive `crate setup` of the sitting.

Answering yes to "Record the credential provider-session now?" and then
pressing Enter at the secret prompt is recorded as `setup.credential` FAIL and
the verb exits `PRECONDITION`, although the pin and the config were written
and every other check was ok. The person had nothing to type: the value is a
session blob that only the login step produces. The note path for a no answer
is INFO; the empty answer should be the same fact.

**Closes when:** an empty secret at that prompt is recorded as the same INFO
note as a no, and the exit code follows the doctor's own verdict.

**Closed 2026-09-16 on `relay/83`.** `Prompter.secret` raises `NothingEntered`,
a subclass of `PromptUnavailable`, for an empty value, and the credential offer
records it as the INFO note a no gets. An unreadable prompt still fails. Driven
end to end through the dispatcher: with the offer accepted and left empty, the
only failing check is `rekordbox.pins`, the one a clean machine owes doctor.

---

## R-348. An AttributeError inside the vendored tool is classified as a transient outage

**Found:** 2026-09-16, the first real download through the adapter, before #82.

`'function' object has no attribute 'info'` raised inside the wrapped tool
was reported as `unavailable-transient`, `retryable: true`, remedy
`retry-later`, and the run said the provider was unavailable. It was a code
defect in this repository, and a job that retried it would have retried it
forever. The classification reads the exception's text for provider signals
and treats everything else as transient, which is the honest choice for an
unknown provider error and the wrong one for a Python error class that a
provider cannot raise.

**Closes when:** `AttributeError`, `TypeError`, `NameError` and their kin
raised from inside the tool are classified as `AdapterBroken` with remedy
`report-defect`, and a test drives one through the loop.

**Closed 2026-09-16 on `relay/83`.** `adapter.raise_if_defect` escalates the
three classes, and `UnboundLocalError` through `NameError`, from an offer or a
fetch to `AdapterBroken` with the new adapter token `report-defect`. Driven
through both adapters' sequential loop and through the paced pool the download
verb runs, with every unlanded track still queued. The vendored source asks the
same question before its authentication heuristic, which reads the word token
anywhere. R-365 and R-366 are what this left open.

---

## R-349. The backup verb's per command report reaches nobody

**Found:** 2026-09-16, the attended U29 sitting, reading a dry run that
succeeded in four seconds.

`run_backup` returns a `BackupOutcome` with every command's argv and return
code, and `handle` returns nothing to the engine. The detached worker's log
holds `backup.run: ok` and a run id. The foreground `--job` envelope holds the
job's counts and the published ages. There is no place a person can read which
rclone commands ran, what each returned, or what a dry run would have
transferred, which is why R-345's misconfiguration was only visible by running
the command by hand.

**Closes when:** the outcome payload is persisted with the job, the foreground
envelope carries it, and `job show` prints it.

---

## R-350. A token refresh after the catalogue opens lives only in memory

**Found:** during U62, 2026-09-16, writing `provider_session.client_session`.

The factory logs the client in inside `materialised_session` and writes the
session's tokens back before the scope closes, so a refresh performed DURING the
login reaches the keychain. The scope then closes and the client is returned. A
refresh the client performs later, in the middle of a long crawl, updates only the
in memory client. **Measured cost: none observed and unmeasured live.** The stored
refresh token stays valid, so the next invocation logs in again from it. It costs
something only if the provider rotates refresh tokens on use, which nobody has
measured against this provider.

**Closes when:** a live sitting records whether a refresh rotates the refresh
token, and if it does, the catalogue writes the client's tokens back when its
work ends.

---

## R-351. A seed artist cannot be pinned by identifier, so a shared name blocks a label

**Found:** during U62's code review, 2026-09-16.

`TidalCatalogue.artist_for` resolves the label name and every seed by exact
folded name, and refuses the label when two provider artists carry that name
exactly, because crawling the first could offer an unrelated act's releases and
verify none of them. `registry.LabelEntry.seed_artists` holds names only, so a
person whose seed shares a name with another act has no way to say which one
they mean. **Measured cost:** that label refuses on every sweep with a message
naming the collision, and the person's only move is to remove the seed. Driven
against a fake with two artists of one name; how often real names collide is
unmeasured.

**Closes when:** a seed can be recorded by provider identifier and the adapter
reads it without searching.

---

## R-352. The adapter's roster is narrower than the source system's discovery

**Found:** during U62, 2026-09-16, reading `DJ_tools` `label_playlists.discover`.

The source system seeded a crawl from album searches for the label name and its
numbered compilations, kept albums whose copyright matched, and then walked every
credited artist breadth first. `artist_for` crawls the label's own artist page,
when one is named exactly for the label, and the registry's seed artists, and
nothing else. **Measured cost, by reading and not by a live run:** a label whose
releases are credited to artists outside that roster is offered only the part the
roster released, and a label with no artist page and no seeds refuses by name
rather than returning a partial answer. The refusal is honest; the narrower
coverage is a silent shortfall against the source system on labels whose seeds
are incomplete.

**Closes when:** the attended sitting compares one real sweep against the source
system's discovery for the same label, and either the gap is measured as
acceptable or discovery is ported behind the same seam.

**Measured 2026-09-17, the fourth attended sitting, and the gap is large.** All
47 labels from the source system's `favorite_labels.json` were carried into the
registry, with their match needles and track limits. Not one of them carries a
seed artist, which the source system's document has no field for in practice, so
the roster is the label's own artist page alone. `crate sync labels` over the 47:
**15 labels swept, 32 failed.** 31 of the 32 failed as `LabelUnresolvable`, the
provider having no artist named exactly for the label and the registry naming no
seeds, and the 32nd, Freerange, read one release and could not confirm it. The 15
that swept offered 98 releases from 12 of them, and 3 swept clean with nothing
new. The refusal is honest, and two thirds of a carried over registry refusing is
the shortfall this entry predicted, now with a number on it.

**Closes when, restated:** discovery is ported behind the same seam, or the
registry gains seed artists for the labels whose artist page is not named for
them, and a sweep of the 47 refuses materially fewer.

---

## R-353. The login classification is read off a fake's shape, not a live rejection

**Found:** during U62's review fix round, 2026-09-16.

`provider_session._rejected` reads a rejected session as a response status of
400, 401 or 403 anywhere in the exception's cause chain, or an exception class
named `AuthenticationError`, and everything else as `ProviderUnavailable`. The
client source shows `raise_for_status` re-raising an HTTP error that carries its
response, which is what the fake models. **What a live expired session actually
raises was not observed**, and a shape the classification does not read would be
reported as `unavailable-transient` with retry later, telling a person to wait on
a session that will never work again. METHOD's pattern four applies: the
justifying shape was authored alongside the fix.

**Closes when:** the attended sitting records what a revoked session raises and a
test pins that shape.

---

## R-354. The playlist reference refuses the app scheme and embed URLs

**Found:** during U62, 2026-09-16, writing `tidal_catalogue.playlist_id`.

The parser accepts a bare identifier, an `http` or `https` URL on `tidal.com`,
`www.tidal.com` or `listen.tidal.com` whose path ends `playlist/<id>`, and that URL
with a query string. It refuses `link.tidal.com` short links by name, and it
refuses everything else generically, including an app scheme link and an embed
URL. **Measured cost:** a person who pastes one of those is told it is not a
playlist reference, and nothing is listed wrongly. Which shapes the provider's
share sheet produces today was not observed.

**Closes when:** the attended sitting records the share sheet's actual output and
the parser accepts every shape it produces.

**Observed 2026-09-17, the fourth attended sitting.** The provider's share sheet,
on the desktop application, produced `https://tidal.com/playlist/<uuid>` with no
query string, which the parser already accepts, and both `crate label harvest`
and `crate intake playlist` took it unchanged. The app scheme and embed shapes
were not produced and so are still unobserved.

---

## R-355. The bound account matches nothing, because no shipped row carries an ISRC

**Found:** during U63, 2026-09-16, driving the adapter through the real workers.

`TidalAccount.match_track` takes an ISRC naming exactly one provider track, then
an identity that is an exact provider track URL, and returns `None` otherwise, as
`modules/outbound/account.py` requires: never a text search, never a bare number
read as a provider identifier. The rows both outbound workers hand it come from
`modules/outbound/source.local_tracks` and `heart_candidates`, which set no ISRC
because a rekordbox collection export carries none, and whose identity is the
rekordbox `TrackID`, a bare number. **Driven, not argued:**
`test_the_shipped_rows_carry_no_isrc_so_a_sweep_matches_nothing` queues a sweep
over a client that knows both tracks, and the job ends succeeded with every row
unmatched and no call made to the provider.

**Measured cost.** Nothing wrong is written: an unmatched row is reported, not
guessed. What a person gets from a live `crate sync favorites` or
`crate export playlist` today is a clean job that hearts nothing and adds nothing,
with every track listed as unmatched. The attended R-144 sitting would meet this
first.

**Why not fixed here.** The ISRC has to come from somewhere the export does not
carry, most plausibly the audio file's own tag at the row's `Location`, and that
is a change to the outbound source and to R-227's reading of the library, which
the brief placed out of scope. Both choices are Phillip's: read the file tag in
`source`, or wait for a live database reader that carries the provider id.

**Closes when:** the rows the outbound workers build carry an ISRC or an exact
provider reference for a track that has one, and a live sweep matches it.

**CLOSED 2026-09-17, the fourth attended sitting, by fixing it.** The rows both
outbound workers build now carry the ISRC the row's own audio file holds.
`source.isrc_for` resolves the row's `Location` through the configured prefix
map, the same resolver R-372 added the rule for, and reads the new `isrc` field
in `core/tags.py`, which is `TSRC` in ID3, the `isrc` Vorbis comment, and the
iTunes freeform atom. A value that is not twelve characters of ISRC shape reads
as none, because the account queries the provider with exactly this string.
**Measured on the live export:** 103 of 109 favourites and 8246 of 9937
collection rows carry one, where every row carried none before. The six
favourites without one are AIFF files, which is the container the sample found
untagged. A live `crate sync favorites` then matched 59 of 109 rows and a live
`crate export playlist` matched 2 of 4, so R-144's two live runs could happen at
all. The review of the fix found that an unmounted volume would read as a library
of untagged files and report a clean unmatched sweep, which is this same defect
by a second route, so the row builders now refuse `library-volume-unmounted` when
the root is not a directory.

---

## R-356. An ISRC several provider tracks carry is unmatched rather than resolved

**Found:** during U63, 2026-09-16, writing `TidalAccount.match_track`.

One recording is commonly on the provider several times, as a single, an album cut
and a compilation track, each with its own identifier and the same ISRC. The
adapter returns `None` when the ISRC answer holds more than one distinct
identifier, because which release gets the heart is not something the ISRC
decides, and the brief forbids a first result. **Measured cost: unmeasured live.**
Every such track is reported unmatched and is not hearted. How many of a real
library's recordings the provider carries more than once was not observed.

**Closes when:** a rule that picks among same ISRC releases without guessing is
decided, for example the one already in the favourites, and pinned by a test.

**Measured 2026-09-17, the fourth attended sitting, on both verbs.** In the four
track export, two rows were unmatched and BOTH were this: one ISRC the provider
answers with three tracks, a single, an EP and a ten year compilation, and one it
answers with two, a single and an album. In the 109 row favourites sweep, 50 rows
were unmatched, of which 6 carry no ISRC at all and the rest are this shape or an
ISRC the provider does not know. On a real library this is not an edge case, it is
half of a small playlist.

---

## R-357. The held account answers from what it read at open, for the life of the process

**Found:** during U63, 2026-09-16, making `account.resolve` hold one adapter.

The workers resolve the account once per item, so the seam holds the first adapter
for the process and the adapter holds the favourites it read once and each
playlist's membership it read once, updated by its own writes. A heart removed or
a track taken off a playlist from another device during a run is still read as
present. **Measured cost:** that item is reported as already present and nothing
is written, so an add only sweep can under write and cannot over write. A detached
resume is its own process and reads afresh. A rejected session drops the held
adapter, so a login made meanwhile is picked up. `export.apply` still asks
`playlist_tracks` once per item, which is now memory rather than a listing.

**Closes when:** a run that must see concurrent edits is a requirement, or never.

---

## R-358. A swept playlist is never marked on the account, so the source system sweeps it again

**Found:** during U64, 2026-09-16, building the deferred mark step.

`sync/marks.py` renames a provider playlist only after the importable file exists
and a recheck holds. Neither half is available to the playlists source.
`modules.outbound.service.RemoteAccount` declares six add only members and no
rename, so there is nothing to apply the `DOWNLOADED ` prefix through; and the
intake worker a sweep composes writes no importable file, because it resolves
tracks and does not acquire them. `sync.playlists` therefore reports
`"mark": "unbound"` on every pass and the cursor is the only record a sweep
leaves. **Driven:** every playlists test in `tests/test_sync_all.py` reads the
block, and `test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run`
asserts the value.

**Measured cost.** Cratekit itself does not sweep a recorded playlist twice. The
source system does not read Cratekit's cursor, so while DJ_tools and Cratekit both
run against one account, a playlist Cratekit swept is new to DJ_tools' next
`dj-sync`. Not observed live.

**Why not fixed here.** A rename is an account write, and U63's adapter is add only
by type. Adding one is a change to the outbound seam the brief placed out of scope.

**Closes when:** the account seam can rename a playlist it did not create, and a
sweep that produced an importable file marks through `marks.apply_deferred`.

---

## R-359. A playlist is recorded as swept once its tracks are resolved, not once they are acquired

**Found:** during U64, 2026-09-16, deciding what clean completion means.

The brief makes the cursor advance on clean completion, and the only job a sweep
queues is `intake.playlist`, whose worker reports each track OWNED, OFFERED or
MISSING and acquires nothing. `sync.playlists.reconcile` records a playlist when
that job SUCCEEDED, which is every item resolved. **Measured cost:** a playlist
holding tracks the library does not own is recorded as swept, and the next pass
excludes it as `recorded`, so its missing tracks are reported once, in that job's
per item reports, and never offered by a later sync. That is R-140's shape one
level up: a completed resolution read as a completed intake.

**The conservative call made here.** Follow the brief: record on success, because
the alternative, holding the cursor until every MISSING item is acquired, needs an
acquisition step the sync pass does not compose yet. The options are Phillip's:
record only a playlist with no MISSING item, or compose `acquire download` over
the missing rows and record after it.

**Closes when:** swept means the library holds what the playlist held, or the
report says in words that it does not.

---

## R-360. The playlists cursor moves only when a pass runs, not when the job finishes

**Found:** during U64, 2026-09-16.

`reconcile` runs at the start of `crate sync all`. A playlist whose job succeeded
an hour ago is still `never` in the watermark status rows until the next pass, and
that pass reports it under `recorded_now`. **Measured cost:** a status read
between the job finishing and the next pass undercounts what was swept. Nothing
is swept twice, because the open job excluded it as `in-flight` and the next pass
records it before deciding.

**Closes when:** the job completion path records the cursor, or the status verb
reconciles before it reports.

---

## R-361. The source system's label run debris is swept as ordinary playlists

**Found:** during U64, 2026-09-16, reading `DJ_sync/plan.py`'s filter.

`filter_account_playlists` in the source system also dropped playlists named
`<label> LIBRARY`, the throwaway playlists its label batch leaves behind, and any
playlist id a manifest registered as run created. `sync.playlists` excludes the
swept prefix, the cursor, the favourites placeholders, open jobs and empty
playlists, and nothing else, because the brief named those. **Measured cost:
unmeasured live.** Any such playlist still on the account is queued as intake, and
its tracks are resolved and reported. Nothing is written to the library or the
account.

**Closes when:** the attended sitting reads the live account's playlist names and
either finds no debris or a rule is decided for it.

**Observed 2026-09-17, the fourth attended sitting, and the debris is real.** A
live `crate sync all` listed 599 playlists on the account and queued 18 as intake,
of which **11 are source system label run debris**: `Rebellion LIBRARY`, `Do Not
Sit On The Furniture LIBRARY`, five playlists all named `Sol Selectas LIBRARY` and
four all named `Colorize LIBRARY`, about 1600 tracks between them. The duplicates
are the source system having left one per run. Nothing was written: the jobs were
left queued and unresumed.

---

## R-362. The favourites placeholders are recognised by the source system's names alone

**Found:** during U64, 2026-09-16, writing `favorites/placeholders.py`.

Cratekit's favourites source creates no placeholder playlists. The pattern
`Favorites YYYY-Qn` or `Favorites (undated backlog)` is the source system's, and
the source system records their ids in its own run state, which Cratekit does not
read. **Measured cost:** a placeholder a person renamed is swept by the playlists
source as well as by the source system's favourites run. The review's one finding
was the backlog name this pattern first missed, fixed and driven in the same unit.

**Closes when:** Cratekit's favourites source owns its placeholders by id, or the
source system is retired.

---

## R-363. Two passes started together can each queue the same playlist

**Found:** during U64, 2026-09-16, by the built in review.

The in flight check reads the queue, and the enqueue is a later transaction per
playlist, so two `crate sync all` runs whose planning overlaps both see a playlist
as new. **Measured cost: unmeasured, not driven.** The second job resolves the same
tracks again and reports them again. No write to the library or account follows.

**Closes when:** the check and the enqueue share a transaction, or concurrent
passes are refused.

---

## R-364. The handler key filter on the playlists source's jobs kills nothing

**Found:** during U64, 2026-09-16, mutation row C3.

`sync.playlists.source_jobs` filters by handler key, `source_id` and library.
Removing the key filter killed zero tests on the subset and zero on the full suite,
7523 collected, because no producer queues a job carrying `source_id` `playlists`
under another key. Maintainer facing. Kept as defence.

**Closes when:** a second key carries this source's jobs, or the filter is removed.

---

## R-365. A TypeError from a malformed provider response now stops the batch

**Found:** 2026-09-16, `/code-review` of `relay/83`. Not driven.

R-348's closing condition makes every `TypeError`, `AttributeError` and
`NameError` under an offer or a fetch an invocation failure. The class alone
cannot tell a defect in this repository from the vendored tool or the provider
client tripping over one track whose response is missing a field, for example
`'NoneType' object is not subscriptable`. Before, that one track was transient
and the batch carried on. Now the run stops with `report-defect`, every unlanded
track stays queued, and a re-run stops on the same track again, so the batch
never passes it.

**Reachability unmeasured.** The reviewer read the client's track parsing, which
checks for a missing album, and the vendored downloader, which catches most
errors itself, and found no producer. No real response was driven.

**Why not fixed here.** The ledger condition names these classes, the cost is a
visible stop naming the class and the message rather than a silent retry, and
narrowing it needs a real malformed response to decide against.

**Closes when:** a real run observes the shape and the per track path learns to
tell a malformed provider record from a defect, or a sitting of real downloads
shows the shape does not arise.

---

## R-366. Defect classes are escalated only inside the acquisition loop

**Found:** 2026-09-16, the hunt for R-348's shape one file over, on `relay/83`.
Read, not driven.

`raise_if_defect` runs under `acquire_one` and at the top of the vendored
source's `raise_if_session_dead`. Three neighbours still translate any exception
into a provider answer. `_VendoredSource.authenticate` and the streamrip source's
login wrap everything in `AdapterAuthFailed` with `reauthenticate-provider`, so a
defect at login sends a person to log in again. `label.catalogue.resolve` and
`modules.outbound.account.resolve` report an `AdapterBroken` from opening as
`credential-missing`, and `modules.outbound.account.provider_failure`, which
every `TidalAccount` provider call goes through, reads anything that is not an
authentication failure as `unavailable-transient` without the defect question.

**Why not fixed here.** Outside the four residuals this unit closes, and each
site has its own cause vocabulary to decide against.

**Closes when:** each of those paths asks the defect question before reading a
failure as a session or a provider answer, with a test per path, or the entry
records why a path is exempt.


---

## R-367. A restore from a snapshot taken with rekordbox closed always reports failure

**Found:** 2026-09-16, the restore rehearsal of the second attended U29 sitting.

`plan_database_snapshot` copies each SQLite sidecar only when it is present,
and its comment says why: a checkpointed database legitimately has none.
`plan_restore` builds a copy of `master.db-wal` unconditionally for every
sidecar marked `restored`, and `run_restore` reads any non zero rclone exit as
a failed transfer. The snapshot verb refuses while rekordbox or its agent runs,
so every snapshot it takes is of a closed database, and a closed, checkpointed
database has no write ahead log. Driven today: `2026-09-16T173512Z/db/` holds
`master.db` alone, the first restore command landed it byte for byte, the
second ran `rclone copy <snapshot>/db/master.db-wal <target>/`, exited 3,
directory not found, and the run raised `BackupRefused` saying the transfer
exited 3, the restore did not complete, and the live companion files were
cleared and not put back.

**Cost:** the person is told a restore failed after the database arrived
intact, and told to run it again rather than open the library, and the rerun
fails the same way. Against the live root that is a restore the product cannot
complete from the only kind of snapshot it takes, and a person who follows the
message never opens rekordbox. The measured cost today was one failed
rehearsal into a scratch directory; the live root was not the target.

**Why not fixed here.** An attended sitting runs one workflow and files what
it finds. The fix is a unit's: list the snapshot folder before planning and
copy only the sidecars it holds, or treat a source not found on an optional
sidecar as skipped rather than failed, with a test that restores from a
snapshot holding the database alone, which is the only kind the product takes.

**Closes when:** a restore from a snapshot holding `master.db` alone completes
and reports the database transferred and the sidecar absent, with a test that
pins it.

---

## R-368. No verb restores anywhere but the live library root, so a rehearsal needs a script

**Found:** 2026-09-16, the same sitting.

`crate restore run --from-backup` has no target option, and
`restore_under_one_session` says why: its `target` parameter is a seam for
tests, and recovering onto a different volume is a different verb with
different gates, which is what `core.restore.bare_metal_session` exists for.
That function has no caller in `src`, verified with
`git grep -n bare_metal_session -- src`, which returns its definition and the
docstrings that name it. So the rehearsal R-9 asked for, a restore to a
scratch directory, cannot be run by any shipped command, and this sitting ran
it from a script in the session scratchpad calling the engine with `target`
set, under the real gates and real rclone. The script is one call and is not
committed. The recovery session still took the library lock and wrote a
session record on the live volume for a restore that touched nothing on it,
which is right for the gates and odd for a rehearsal.

**Cost:** the only restore the person can run is the destructive one. The
rehearsal that would tell them a restore works before they need it is a
session's script, and nothing in the product offers it.

**Closes when:** a verb restores a named snapshot into a named directory,
database only by default, under gates that fit a target that is not the
library, or the decision is recorded that rehearsal is out of scope and R-9's
second gate is read as satisfied by this sitting's script.

---

## R-369. An acknowledgment run can be answered from a shell that can never continue it

**Found:** 2026-09-16, the same sitting.

`crate session ack` stops at `session.ack.backup` naming a run, `crate run
decide` records the answer, and the continuation with `--run` mints the
record. The mint refuses without a controlling terminal, by design, so a
detached job cannot acknowledge. Driven today: the run was opened and answered
from the operator's shell, the continuation was run from the session's own
shell, which has no terminal, and it failed `ACK_REQUIRED` with
`fix: crate session ack`, the run was marked failed, and nothing was written.
The same three commands from a Terminal window succeeded. `decide` cannot know
where the continuation will run, so this may be a message rather than a code
change.

**Cost:** one wasted round and a run left failed, with a fix line that sends
the person back to the command that opened the run. No data cost. Recorded so
the next session does not spend the same round: the acknowledgment is the
person's, minted from a real terminal, and a session cannot mint it.

**Closes when:** the no terminal refusal says that the recorded answer stands
and the continuation must come from a terminal, or the ack verb checks for a
terminal before it opens a run.

---

## R-370. The shipped vocal loader could not score a track, and the scorer read speech, not singing

**Found:** 2026-09-17, the third attended U29 sitting, the first real
`crate analyze vocals`. **Fixed in the sitting on `sitting/r133-vocal-restamp`.**

Driven with the vocals extra installed and the checkpoint the source system
scored the library with at `~/panns_data/Cnn14_DecisionLevelMax.pth`:
`vocal.default_loader` built PANNs `AudioTagging`, which defaults to a
different checkpoint, `Cnn14_mAP=0.431.pth`, and whose answer to a missing
checkpoint is `os.system("wget ...")`. This machine has no wget, so the shell
printed `wget: command not found`, `torch.load` raised `FileNotFoundError`,
`vocals._load` recorded the failure, and every track came back
`vocal-model-unavailable` with a warning saying to install the extra that was
installed. Had the checkpoint been fetched, `AudioTagging.inference` returns
a clip level pair and no frame output, so `infer_frames` would have failed
on it too. Under both, `infer_frames` read columns 0, 1 and 2 of the label
table, which are Speech, Male speech and Female speech. The source system
reads Singing, Male singing and Female singing, columns 27, 32 and 33. A
scratch drive of the frame wrapper with the speech columns scored four known
tracks 0, 0, 2 and 7 with male calls where DJ_tools had stamped 11, 10, 0
and 0; with the singing columns it scored 13, 11, 0 and 1 and matched every
gender call.

A third shape sat under the first two: importing `panns_inference` at all
executes its config module, which shells out to wget for a label table it
cannot find under HOME and then raises opening the file it did not fetch.
`extra_available` imported it to answer installed or not, so on a home with
no model files, which is every test's home, the queue check turned into an
internal error the moment the extra was installed.

**Measured cost.** A full library restamp on the shipped code would have
written nothing and told the person to install what was installed. Every
fake driven test was green, because no test ever instantiated the wrapper
and every fixture filled the first three columns.

**Fixed.** The loader builds `SoundEventDetection` from the named checkpoint
and redirects the wrapper's stdout chatter away from the JSON envelope.
`vocals.missing_requirement` names the first thing the model cannot do
without, in the order the loader needs them: torch imported for real, since
an installed torch that will not load is the case a lookup cannot see; the
extra installed; the label table on disk, checked BEFORE the extra is
imported because the import reads it; the checkpoint on disk and not
truncated. The queue asks it and refuses a job that could score nothing,
naming the missing file. `class_indices` resolves the three columns by name
from the model's own label table, once at load beside the model, and a model
with no table or a table that does not name a target is a failed load with
its reason kept, never a read by number. The one summary warning both
verbs emit is shared and names the first missing requirement or the
recorded failure, so nobody is told to install what is installed. The
review of the branch drove ten findings against the first cut of this fix
and nine hold and are applied; the tenth is R-377. The real folder then
scored 35 of 36 within one point of the source system, and the 36th is
R-371.

---

## R-371. A tail chunk shorter than the network can pool failed the whole track

**Found:** 2026-09-17, the same sitting, the first real run's one failure.
**Fixed in the sitting on `sitting/r133-vocal-restamp`.**

`infer_frames` walks the signal in eight second pieces and sent the last
piece whatever its length. `08A - 123 - Satellite - Ashibah - Forever.flac`
is 7,176,000 samples at 32 kHz, which leaves a tail of 8,000 samples, a
quarter second. CNN14 pools its time axis by two five times, so that tail
pooled to `(1024x0x2)` and the forward pass raised `Output size is too
small`. The scorer's boundary caught it as `vocal-inference-failed` and the
track kept its previous tag, so nothing was lost on a restamp, but a new
track of that length would never receive a score. One in thirty six on this
folder. DJ_tools never chunked, so it could not have hit this.

**Fixed.** A tail shorter than one second is folded into the piece before
it, a lone clip shorter than that is padded with silence to the floor on the
chunked and the unchunked path alike, and the frames the padding added are
trimmed off again so a short clip scores on its own length. Tests pin the
fold at the real chunk size, that a three second tail stands alone, the pad
on both paths, the trim, and that an exact multiple still walks in equal
pieces. The second real run scored the track 3 F and left the other 35
unchanged.

---

## R-372. Setup wrote no location prefix rule for rekordbox's renamed drive, and the My Tags plan read clean over 9770 rows it could not resolve

**Found:** 2026-09-17, the same sitting, the first real `crate metadata mytags-vocals`.

rekordbox records nearly every row of this library under the drive's old
volume name and maps it to the current mount at runtime
through its `BaseDBDrive` and `CurrentDBDrive` registry entries. The source
system verified that on 2026-08-01 and carries the old name as a constant.
Cratekit's designed answer is `library.location_prefix_map`, and setup wrote
it empty. Driven: the plan reported `count 0, active 9937, unresolved 9937`,
outcome ok, no warning. That is a clean report over state the tool could not
read: an apply on it would have written nothing and reported success.
`crate doctor` reported no failing check before or after.

**Cost.** Bounded to this sitting because the author knew the old name. A
person who did not would read the empty plan as a library with no vocals.

**Worked around in the sitting** by adding the rule to the config by hand:
`location_prefix_map = [{ from = "/Volumes/<old name>", to = "/Volumes/<current name>" }]`.
With it the plan resolved 9770 rows and left 167 unresolved, which are 14
streaming rows, 137 Tidal catalogue paths and 16 rows under two home
directories.

**Closes when:** setup reads the two registry entries from the database and
offers the rule, or the plan and the doctor warn when unresolved rows are
the majority of active rows rather than reporting ok.

---

## R-373. Forty three Vocals associations the source system wrote sit on files that carry no voxlevel today

**Found:** 2026-09-17, the same sitting, comparing the plan to the database.

Before the apply the database held 1935 Vocals associations and the plan
held 1896. Of the 43 the plan lacked, every one resolves to a file on the
volume that reads no `voxlevel` at all today, 24 `vox`, 11 `female vox`, 8
`male vox`. The apply is add only, so they stand. Nothing here says which
side is right: the file may have been replaced since it was scored, or the
tag may have been lost in a rewrite.

**Closes when:** those files are restamped and the associations either
confirmed by a fresh score or reviewed by hand.

---

## R-374. No verb sets the with-vox cut by hand, so the source system's 5.0 was carried by writing the state file

**Found:** 2026-09-17, the same sitting, before the My Tags plan.

`crate analyze calibrate` fits an Otsu cut over a folder and refuses when
the clusters do not separate. The source system's `dj-vocal-calibrate` took
`--threshold`, and the library's cut is 5.0, hand set after the author
reviewed named tracks because Otsu's 16.5 was too tight. With no calibration
recorded, `metadata.mytags-vocals` uses 12.0, so a plan on Cratekit alone
would have tagged fewer tracks than the source system did. The sitting wrote
`.cratekit/local/vocal_calibration.json` by hand with `threshold 5.0` and a
note naming its origin.

**Closes when:** `analyze calibrate` accepts a threshold, or a documented
verb carries a cut over.

---

## R-375. A gated write leaves no session record, and the gate's docstring says the workflow is recorded in the session log

**Found:** 2026-09-17, the same sitting, after the My Tags apply.

`session.assert_gates` says its `workflow` argument "is recorded in the
session log". It is not: `open_session` writes the records under
`history/sessions/`, and only ingest and restore call it. `metadata_cli`,
`trees`, `deletion`, `adopt` and the backup module assert the gates and
write nothing there. Driven: after `mytags-vocals --apply` wrote four
associations to the live database, the sessions directory held last night's
rehearsal alone, and the write's only trace is the snapshot it captured
first, `history/snapshots/2026-09-17T114753Z-2736227cd932636e`.

**Cost.** Low. The doctor's unresolved session check has nothing to report
because nothing was left open, and the database change is real and
committed. What is lost is the ledger the docstring promises.

**Closes when:** the docstring stops claiming a record, or the gate writes
one.

---

## R-376. The vocal restamp is one folder per invocation, and the library is 343 folders

**Found:** 2026-09-17, the same sitting, measured on the real run.

`crate analyze vocals` scores one folder, not recursively. `Music/` holds
9868 audio files in 343 leaf folders under `Processed_Tracks`. Measured on
the first real folder, 36 tracks in 102 seconds, 1.3 GB peak, so the full
library is about 7.7 hours of scoring across 343 invocations, each a queue
and a resume by hand. The source system's `dj-vocal-restamp` walked the
whole library in one skip idempotent, resumable command.

**Closes when:** the verb takes many folders or walks a tree, or a scripted
full pass is run and recorded.

---

## R-377. The chunk floor is a rounded cover for the network's real floor, clamped by the caller's chunk size

**Found:** 2026-09-17, the same sitting, the review of the R-371 fix.
Plausible, not driven on a real track.

`MIN_CHUNK_SAMPLES` is one second, 32000 samples. The network's own floor
is 32 frames after five pool by two stages, about 9920 samples at a hop of
320, and the constant is a cover for that rather than derived from it. On
the chunked path the floor is clamped to the caller's chunk size, so a
caller passing a chunk under the floor lowers the floor with it, and a
chunk of 8000 samples reproduces R-371 exactly. Today the only caller uses
eight second chunks and the unchunked path applies the floor in full, so it
is latent.

**Closes when:** the floor is a model property applied whatever the chunk
size, or a chunk size under it is refused.

---
## R-378. The harvest prints nothing a person can read

**Found:** during the fourth attended sitting, 2026-09-17, the first real
`crate label harvest`.

The verb ran on a real playlist and printed `label.harvest: ok` and a run id, and
nothing else. The four labels it found and the six tracks it could not resolve
are in the envelope and reach a person only through `--output json`. The human
renderer has no case for a `review_set/1` payload's items, so the whole answer of
a read only verb is invisible in the output a person gets by default.

**Measured cost:** the verb is unusable as documented without a second
invocation in another output mode. Nothing is wrong in what it computed.

**Closes when:** the human rendering of `review_set/1` names the harvested
labels and the unresolved count, and a test drives the rendered text.

---

## R-379. Every offered release records its artist as a Python object address

**Found:** during the fourth attended sitting, 2026-09-17, reading the review
queue the first real label sweep filled.

The 98 rows the sweep offered carry, in their payload, `"artist": "<tidalapi.artist.Artist object at 0x10b77ec00>"`.
The provider's object was stringified into the record rather than its name being
read off it. The identity, label and title fields are correct, so this is a
display field carrying a memory address.

**Measured cost:** every release a person reviews shows an address where the
artist belongs, and a review record written today is not readable tomorrow, since
the address means nothing outside the process that wrote it. 98 rows on the live
library already carry it.

**Closes when:** the offer records the artist's name, a test pins that a provider
object never reaches a stored payload, and the rows already written are migrated
or discarded.

---

## R-380. A job whose failures are permanent reports itself as transient and resumable

**Found:** during the fourth attended sitting, 2026-09-17, when 32 of 47 labels
failed.

The inner cause is exact and final: `sync-source-lookups-failed`, `retryable:
false`, because the provider has no artist named for the label. The cause the job
wraps it in is `unavailable-transient`, `retryable: true`, with the remedy
`resume-job` and the step "retry this source when the provider is reachable". The
provider was reachable throughout; 15 labels swept in the same pass.

**Measured cost:** a person is told to retry work that cannot succeed, and the
resume costs another full crawl of the 15 that already worked. The honest reading
is in the inner cause, which is only visible in JSON.

**Closes when:** a job whose every item failure is non retryable reports itself
non retryable, and a mixed job says which half is which.

---

## R-381. An accented label name yields a mangled identifier

**Found:** during the fourth attended sitting, 2026-09-17, carrying the source
system's registry over.

`registry.slug` folds anything outside `[a-z0-9]` to a hyphen, so `Sueño` becomes
`sue-o` and `Voll Schön` becomes `voll-sch-n`. The source system's own keys for
those two are `sueno` and `voll-schoen`, so the same label has two identifiers
across the two systems, and every watermark keyed on one is invisible to the
other.

**Measured cost:** two of 47 labels on the live registry. Nothing collides today,
and a slug is stable once created, so this is a migration and a legibility cost
rather than a correctness one.

**Closes when:** the slug transliterates before folding, and a carried over
registry produces the identifiers the source system used.

---

## R-382. A playlist intake run on its own is not recorded, so the next sync queues it again

**Found:** during the fourth attended sitting, 2026-09-17.

`crate intake playlist` ran to done over a real account playlist, ten items, every
one resolved. `crate sync all` in the same sitting then listed that same playlist
as new and queued a second `intake.playlist` job for it. The playlists cursor is
written by `sync.playlists.reconcile` over the jobs THAT SOURCE queued, and a job
queued by the standalone verb carries no source id it recognises.

**Measured cost:** duplicated work rather than wrong data, and it compounds with
R-358: a playlist a person imports by hand is neither marked on the account nor
recorded in the cursor, so it is new to every future pass of both systems.

**Closes when:** a completed playlist intake records the playlist whichever verb
queued it, or the cursor is stated to be the sync source's private bookkeeping and
the verbs say so.

---

## R-383. The favourites listing stops at the first short page, so it reads a fraction of the account

**Found:** during the fourth attended sitting, 2026-09-17, verifying the hearts
the first real sweep wrote.

`listing.paginate` ends its walk when a page comes back shorter than the page size
it asked for. That rule is wrong for this provider's favourite tracks listing,
because the provider serves a WINDOW of a counted collection and omits from it the
tracks it will not serve, so a full window arrives short.

**Cause corrected by U65.** This entry originally said the CLIENT drops the
unplayable tracks. It does not. Read against tidalapi 0.8.11, `Favorites.tracks`
hands the response to `map_json`, which maps every item with no filtering, and the
`Track ... is unavailable` line visible during the sitting comes from
`session.track()`, a per identifier lookup off the listing path. The omission is
the API's, and `Favorites.get_tracks_count` documents the other half of it, that
the total it reports "also includes track that may not be available for playback".
The measurements below are unchanged. Walked by hand at the same moment,
the account holds **197 favourite tracks; the shipped read returned 93** and
stopped at the second page. The same read is what `TidalAccount.has_heart`
answers from.

**Not every listing.** Measured in the same sitting: the account's playlists read
599 both ways, and a 197 track playlist's membership read 197 both ways, so this
is the listings the client filters rather than the pagination helper being wrong
everywhere.

**Measured cost, and it is a reporting one that mostly does not bite.** A track
already hearted is read as not hearted, so the sweep hearts it again. The write is
add only and idempotent, so the account ends correct. The listing is ordered
newest first, which is why the damage is bounded: the 93 rows it does return are
the most recent hearts, so the second sweep in the same sitting read all 59
matched rows as already hearted and wrote nothing. What is unreliable is any
question about an OLD heart, and the first sweep's 18 hearted against 41 already
cannot be trusted as a split for that reason. `favorites.placeholders` exclusions and anything else keyed on the
favourites read are affected the same way.

**Why not fixed here.** One rule governs every listing in the product, including
the label crawls and the playlists source, and removing the short page stop makes
a listing whose offset parameter is broken walk forever. That is a unit with a
test per listing, not a late change inside an attended sitting. Phillip's call,
2026-09-17.

**The code half is done, by U65.** Every shape declares its own stop rule and its
own request budget. The favourites read ends on `get_tracks_count`, a count the
provider publishes for the same collection its windows are cut from, so no page
shape ends that walk any more. The unit's own review found that stopping on an
empty page, which was U65's first fix, only moved the boundary: a window whose
every counted item is unservable comes back empty mid collection. Two shapes with
no published count are narrowed rather than closed and carry R-385.

**Still open, and it is the live half.** Nothing here has read the real account
under the new rule, and a live provider call is attended. The closing condition
below is deliberately unchanged.

**Closes when:** the favourites read returns the account's full set on the live
library, 197 both ways at the numbers this entry records, or whatever the account
holds on the day.

---

## R-384. Every listing now pays one extra request, and on artist releases that is doubled

**Found:** by U65, in its own P6 pass, asking what depended on the old stop rule.

Two of the four shapes end on a count the provider declares, and they pay nothing
for it: the count replaces the request the walk would have spent on the page that
ends it, and for a playlist the count is already parsed onto the object, so
`playlist_tracks` got one request CHEAPER. The other two publish no count and end
on an empty page, which costs one request per walk that the short page rule did
not.

**The arithmetic, and it is not flat.** `account_playlists` is read once per sync,
so the cost is one request. `artist_releases` is read once per release METHOD per
ARTIST, and there are two methods, so a label crawl over A artists pays 2A extra
requests. Almost every artist fits inside one page, which is why the cost is very
nearly the full doubling of that crawl's request count rather than a fraction of
it. The sitting of 2026-09-17 crawled 15 labels of the 47 it swept, and the artist
count behind those labels was not recorded, so the absolute number is unknown.

**Measured cost: none, and that is the point of filing it.** This was reasoned
from the code and the request shape, not observed. No live sweep has run under the
new rule. `fetch_with_retry` already backs off on a rate limit with capped
exponential backoff, so the predicted outcome is a slower sweep rather than a
failed one, and that prediction is also unmeasured.

**Why not fixed here.** The alternative is keeping a page shape rule on
`artist_releases`, which is the shape whose early stop would silently shorten a
label catalogue, and that is this product's core job. Slower beats wrong.

**Closes when:** a live label sweep runs under the new rule and its request count
and wall clock are recorded next to the sitting of 2026-09-17, or the provider
exposes a release count the walk can end on, which would remove the cost entirely.

---

## R-385. Two listings are narrowed rather than closed, because their provider publishes no count

**Found:** by U65's own review, which found that the fix it had just written moved
R-383's boundary instead of closing it.

No page SHAPE can say where a filtered collection ends. The provider omits items it
will not serve from a window while still counting them in it, so a short page is
not the end and neither is an empty one: a window whose every counted item is
unservable comes back empty in the MIDDLE of a collection. Only a count the
provider declares for the collection it is serving closes the class.

`favorite_tracks` and `playlist_tracks` have one, `get_tracks_count` and
`numberOfTracks`, and they end on it. The other two do not:

* `account_playlists` serves `playlistsAndFavoritePlaylists`. The near miss is
  `Favorites.get_playlists_count`, and it must not be used: it counts the root
  collection folder through `my-collection/playlists/folders`, a different
  collection that excludes the playlists the account merely follows. A count of
  the wrong collection is a wrong answer arriving with a confident number.
* `artist_releases` has no count on either release listing.

Both therefore end on an empty page, which is safer than a short one and is not
safe.

**Measured cost: none observed, and the input is not known to be reachable.** It
takes a run of consecutive unservable items one page long to break: 50 for account
playlists, 100 for artist releases. Nothing has been driven that produces such a
run on either shape. On the favourites listing the producer is plausible, since
that listing is ordered by date added and a label catalogue is hearted in one
batch, which is why that shape was the one worth closing properly. Two shapes were
checked for a producer and neither was driven.

**Closes when:** the provider exposes a count for either collection and the shape
ends on it, or a producer is driven that builds a page length run of unservable
items on one of these two shapes, which would turn this from a narrowing into a
measured defect.

---

## R-386. One member of the listing guard's method set is carried and never tested

**Found:** by U65's mutation table, row `F2_the_structural_guard_loses_a_method_name`,
confirmed zero on the full suite at 7584 collected.

`acquire.listing.GUARDED_METHODS` names the four provider listing methods no
module outside the wrappers may call. Removing `get_ep_singles` from that set
kills nothing. The structural guard would stop catching a hand written
`get_ep_singles` pagination loop and the suite would stay green, because every
test that drives the guard drives it through `tracks` or
`playlist_and_favorite_playlists`.

**Measured cost: none today, and the shape is the point.** The guard exists for
call sites nobody has written yet, which is where this defect came from all three
previous times in the source system. A member of the set that no test exercises
is a member that can be deleted in a refactor with a green suite, and the loss
shows up only when somebody writes the call it was there to catch.

**Not fixed here** because U65's two fix rounds were spent, one on the review's
finding that the empty page rule narrows rather than closes R-383, and one on the
refusal that was being slept on for 31 seconds. The fix is small: a case in
`test_the_guard_catches_a_hand_written_pagination_loop` per guarded method name,
driven from `GUARDED_METHODS` itself so adding a name arms its own case.

**Closes when:** every member of `GUARDED_METHODS` has a case that fails when that
member is removed from the set, and the parametrisation is derived from the set
rather than written beside it.

---
