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
matching title rather than from the spelling's own head, which is what the
previous round did, and that consults `sun path` for a listing of `Sun Path (feat.
Mira)`. `tombstone_fold`'s own docstring settles the direction: a missed
suppression re-acquires something and reports it, an over-eager one silently
withholds music somebody wants, and those two costs are not comparable. So the
miss is taken deliberately and named here rather than traded for a silent
withhold.

**Pinned, not assumed.** `UNRECONCILED` in `tests/test_match_states.py` is the
literal list of unreconciled derivations, checked over all seven row spellings and
all three readers on every run. It going empty or growing fails a test rather than
changing behaviour quietly.

**Closes when:** either the provider readers carry the row's full title alongside
its split fields, so the credit survives into `spelled`, or the deletion pass
records a second identity with credits stripped and this side consults it, which
is a decision belonging to whoever owns the tombstone identity rather than to this
unit.

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

**The exact check that would close it.** Once both modules are in one tree, drive
U24's own library reader over a collection row table whose rows put the version in
`Title`, in `RemixerName` and in `Subtitle` in turn, hand each resulting row to
U24's own `version_of`, and assert that every identity it writes appears in
`Wanted.suppression_spellings` for a list naming the same record through all three
readers. That is the only form of this check with no imitation in it on either
side. Until it exists, `u24_records` says in its own docstring what it is and what
it cannot prove.

**Closes when:** that test exists, and `TOMBSTONE_KIND` and `version_identity` in
`match.py` have collapsed into imports from `cratekit.core.tombstone`, which is
what this unit's docstrings already say must happen.

---

## R-22. The index reads a file's title one way, so the disk side of the one-word dash stays narrow

**Found:** by the third U16 review, 2026-08-03.

**The asymmetry.** A LIST title whose dash tail is a bare one-word qualifier now
carries both readings, and `resolve_one` takes the split one when the library
holds the head at exactly that version. A LIBRARY FILE named the same way does
not. `match._read_from_disk` calls `split_title` once, so a file named `08A - 124
- Aurora Bloom - Sun Path - Instrumental.flac` is indexed under the recording `sun
path instrumental` with no version, and a provider row carrying title `Sun Path`
and version `Instrumental` cannot reach it: the row scores 76.4 against a floor of
82 and reports missing.

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
