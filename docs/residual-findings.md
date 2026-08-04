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

## R-14. A pool is sized once and then runs for as long as the work takes

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

## R-15. The work items are the one thing map_workers does not refuse

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

## R-16. A probe child can outlive a parent that dies between start and reap

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

## R-17. The import walk to keep, and the argument the collapse must carry

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

---

## R-18. The cgroup mount point is read at an assumed location

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

## R-19. The unlimited sentinel is a benign zero row, and the commit that said otherwise was wrong

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

## R-20. Containment in the cgroup walk is checked and then read, not read atomically

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
