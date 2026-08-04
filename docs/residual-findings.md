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

## R-17. Two briefs disagree about whether a missing track is a review item

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

## R-18. Four accepted findings from the U16 review, recorded rather than fixed

**Found:** by the U16 adversarial review, 2026-08-02.

Numbered after R-17. If a concurrent unit claims R-18 first, renumber this entry
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

## R-19. Four accepted findings from the second U16 review, recorded rather than fixed

**Found:** by the second U16 adversarial review, 2026-08-03.

Numbered after R-18, which the same unit added. If a concurrent unit claims R-19
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

## R-20. A provider row cannot address a library row that kept a featured credit

**Found:** by the third U16 review, 2026-08-03. Numbered after R-19, which the
same unit added. If a concurrent unit claims R-20 first, renumber this entry at
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

## R-21. The two tombstone derivations are reconciled only at merge

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

## R-22. The index reads a file's title one way, so the disk side of the one-word dash stays narrow

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

## R-23. The recorder keeps the Title column's own shape, so the consulter enumerates shapes

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
`missed` is back to R-20's featured credit alone. The imitation implements the
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

## R-24. The one-word dash class cannot converge on state across the three readers

**Found:** by the fourth U16 review, 2026-08-03, as two blocking findings that
turn out to be one decision. Numbered after R-23, which the same unit added. If a
concurrent unit claims R-24 first, renumber this entry at merge; the content is
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

## R-25. The ambiguous reading class is queued as a question and does not gate the run

**Found:** by the fifth U16 review, 2026-08-03, as a cost the fourth round left
uncosted. Numbered after R-24, which the same unit added. If a concurrent unit
claims R-25 first, renumber this entry at merge; the content is what matters.

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

## R-26. A question answered on one machine does not settle a different question about the same line

**Found:** by the sixth U16 review, 2026-08-04, as the price of closing that
review's first finding. Numbered after R-25, which the same unit added. If a
concurrent unit claims R-26 first, renumber this entry at merge; the content is
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

## R-27. One vocabulary lives in two files until the domain module merges

**Found:** by the sixth U16 review, 2026-08-04. Numbered after R-26, which the
same unit added. If a concurrent unit claims R-27 first, renumber this entry at
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

**Cite by TITLE, never by number.** Six numbers in this file, in the R-17 to R-23
range, were claimed by two branches at once with DIFFERENT CONTENT on each side,
because two units appended here in parallel. Every citation by number in source
or tests therefore points at a different subject the moment either side
renumbers, and that break is invisible: the sentence still reads perfectly and
cites the wrong finding. U16's source and tests cite by title only, and
`test_no_residual_is_cited_by_number_anywhere_in_this_unit` and
`test_every_residual_this_unit_cites_is_a_heading_that_exists` keep it that way.
