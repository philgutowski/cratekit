# Handoff: where Cratekit stands

Written 2026-08-01 so a session with no memory of the build can pick it up.
Revised the same day, twice: once after the three pending branches merged and
the U7 hardening landed, and again after U8 and U17. Revised 2026-08-02 after
U18, again the same day after U11 and U19 landed together, and again after U21
and U24.

## The work is tracked on a board now

`docs/BOARD.md` names it: https://github.com/users/philgutowski/projects/2

All 37 units, the 11 residual findings, and the attended items are issues on
`philgutowski/cratekit`, and the issue number matches the unit number. Each unit
issue carries its full brief from the plan, so a unit can be picked up without
the plan document. Eight units are Ready, twelve are Blocked, and the board says
which blocks which. Read BOARD.md for what to update when a merge lands.

## State

`main` carries U1 to U8, U10, U11, U13, U14, U15, U17, U18, U19, U21, U24, U31
and U35, plus the W1 through W6 hardening, the A4 whitelist addition, and U9's
verdicts. Pushed to the private remote. On `main` as this branch left it,
**3252 passed, 15 skipped**, ruff clean, `scan_repo` clean. This branch's own
battery is **3281 passed, 15 skipped** out of 3296 collected, ruff clean,
`scan_repo` clean. Quote the PASS count here, never the collected total: they
differ by the skips, and an earlier line in this file and one commit trailer both
quoted the collected number as if it were passes.

## What U24 changed

**Track deletion and tombstones, plus one verb.** `src/cratekit/deletion/` is seven
modules and the split is by what each one can be WRONG about: `library` reads the
collection and writes nothing (KTD15); `candidates` decides from the filesystem
rather than from a string comparison whether a removed row's file is genuinely
unreferenced (R37); `trash` performs the only destructive act R18 permits on a
music file and refuses when the volume has no Trash rather than falling back to
an unlink; `stores` records declines and tombstones on U11's revocable decision
stores; `watermark` remembers how far this library has been read, bound to the
database identity it was measured against; `run` is the order those are used in,
which is the unit; and `tombstone_cli` is `crate tombstone list`, the one verb of
this feature a person can reach.

**The proof is the point.** A candidate is deletable only when its device and
inode match no active row's resolved file AND its size matches the size the
removed row recorded. That covers a case-only difference, a composition-form
difference, a hard link, a symbolic link and a path later reclaimed by a
different track, without knowing about any of them. The reference set must be
COMPLETE before any of it means anything: an active row that will not resolve or
will not stat contributes no inode, so the proof would pass on absence of
evidence, and the run refuses instead of offering a smaller set.

**`cratekit.core.tombstone` is a new domain module, in a slot the layering rules
had already reserved.** It owns the version identity both halves of R36 need: the
deletion pass records a suppression, an acquisition pass consults it, and neither
may import the other because deletion is a toggleable module and a slim install
without it still has to be able to ask. The ISRC is deliberately NOT in the
identity, because a row usually has one and a provider candidate usually does
not, and an identity may only contain fields both sides always have.

**HALF THE CLI LANDED, and the half that did not is one wall rather than two.**
`tombstone.list` ships as `cratekit.deletion.tombstone_cli`. It declares no gate,
writes no surface, is not destructive and opens no database, so nothing about the
conformance wall was ever in front of it; it was withheld only because it shared
a module with its sibling. R36 says a tombstone is listable AND revocable, both
words are about a person, and until this verb existed the feature shipped with no
surface for either.

`delete.review` genuinely cannot land yet. It declares an EXPLICIT gate, R34
makes that answerable only by a separate recorded act against the run, and
conformance 3 drives the inline answer and then requires exit `OK`, so no
explicitly gated verb in the registry can land as that assertion is written. It
does NOT refuse on a missing database, and an earlier note here saying it did was
wrong: it declares `files` and no database surface, takes no cloud-sync gate, and
names no database doctor check. `cratekit.deletion.cli` is registered in
`tests/_pending.py` against **U24**, which is where it belongs; an earlier
re-point to U27 is reverted, because U27 ships no deletion domain, proved on the
same evening that it could not carry an explicitly gated verb, and closes in this
same wave, so the re-point moved a contradiction rather than resolving one. See
R-13 and R-16 in `docs/residual-findings.md`, including the choice a human still
has to make about closing #24 with that entry outstanding.

U24's other countdown is DISCHARGED: the guard that declines and tombstones go
through the revocable stores is armed and now runs over the whole package.

**THE FIX ROUNDS CHANGED THREE THINGS THAT MOVE FILES OR LOSE DECISIONS.** A
prefix rule whose target directory does not exist used to make every active row
answer "the file is missing", which left the reference set empty, `complete`
true, and every removed row proved unreferenced against nothing at all: omitting
a rule refused loudly and adding a wrong one proceeded silently. The split is now
at the ANCHOR, the library root or the rule's target, and a row under an anchor
that is not there refuses and names the directory. Separately, a declined row
used to report `handled`, so the watermark passed its sequence and R35's
revocability clause was dead on arrival: `HANDLED` is `{GONE}` alone now, and
revoking a decline also clears the review item that carried the rejection.

The second round found the third. Revoking wrote the STORE first and the QUEUE
second, with no transaction across them and no compensation, so a queue write
that failed for any reason left the decline lifted with the rejection that
re-creates it still armed, and the very next apply put the decline straight back.
The order is inverted now, deliberately, because one of the four intermediate
states is going to be reachable and only one of them is safe to be interrupted
in: queue first leaves the decline standing, which is exactly what the person
asked for last time, and re-running the revoke finishes it. A review item that is
simply not there is treated as already reopened rather than as a refusal, since a
revoke that finds nothing holding the file shut has succeeded.

**WHAT THE ANCHOR SPLIT DOES NOT DO** is check that an anchor is RIGHT, only that
it is THERE, so a rule aimed at an existing but wrong directory still reproduces
the original defect. That is recorded as R-16 Open 4 with its reproduction, and
what ships against it is `ReferenceSet.suspect_anchors` plus a per anchor
WARNING, because every refusal rule for it needs a threshold and every threshold
also refuses libraries that are fine. R-16 Open 5 records the availability this
cost: a mapped volume that is not plugged in now refuses the whole pass, which is
a library that used to run.

**One rule that had two producers now has one implementation.**
`trees.soft_delete_marker` is the single read of rekordbox's soft-delete marker,
beside the field whose missing default it defends. The routing pass and the
deletion pass ask opposite questions of that column, and one of the two
directions they could disagree in trashes a live file.

**THIS WAVE HAS TEN OTHER WORKTREES OPEN, and the earlier claim here that there
were none was wrong when it was written.** `git worktree list` shows branches for
U12, U16, U23, U24, U27, U32, U34, U36, U38 and `fix/conformance-3-and-soft-delete-reader`,
all landing together. Three of them matter to this unit:

- `fix/conformance-3-and-soft-delete-reader` is correcting the conformance 3
  assertion that makes an explicitly gated verb unlandable, and is shipping the
  source guard for the third permissive `rb_local_deleted` reader in
  `write/metadata.py`. Neither is touched here.
- U16 is changing `acquire/match.py` to delegate to `core.tombstone`, which is
  the settled resolution of the two incompatible `version_identity`
  implementations. U24's placement wins because `core/tombstone.py` sits below
  both deletion and acquisition, and both are toggleable modules, so an identity
  inside either is absent exactly when the other needs it.
- U27 lands doctor, which is where `deletion.trash.probe` is owed a check. That
  obligation was appended inside the `cratekit.cli.doctor` register entry, which
  the countdown forces this same wave to delete. It has been moved onto the
  long-lived `cratekit.deletion.cli` key so it outlives tonight.

## What U11 and U19 changed

**U11, the review queue and decision stores.** `core/review.py` is one persisted,
addressable adjudication surface replacing fourteen hand-edited files. An item
carries a stable identifier, a kind, a payload, candidates and a verdict, and it
survives process exit, so a decision reached in one process is seen by another
and is never re-asked. `core/jobs.py` is the pattern it mirrors, which is why the
two share `SCHEMA_VERSION`, `open_store`, `queue_path` and `store_dir` as one
idea specialised per module. The decision stores for declines and tombstones
share the storage shape and are revocable.

**U19, deferred routing.** `write/routing_pass.py` persists each track's intended
routing at the moment it is decided, and a track becomes routed only after the
commit and after its smoke expectations pass. That order IS the unit. The reverse
strands memberships permanently, and a crash in the window re-runs and converges
on membership deduplication. Routing-pending is derived from per-track status
rather than a stored flag, and the readiness signal is database row presence, so
running the verb before an import resolves nothing and marks nothing.

## What the reviews found, because the pattern held again

Two units, two independent reviewers, **twenty-one defects, three of them
blocking, none visible to a green suite.** Both units passed their own author's
battery first. That is four waves in a row.

**The two reviewers converged on one shape without seeing each other's unit: an
unlocked read-modify-write over a JSON document.** U11's decision stores lost 122
of 200 decisions recorded by eight real processes, and every losing call returned
a record reporting success. U19's ledger let a concurrent writer erase a fully
recorded intent, after which nothing was outstanding and the run closed clean
over a track that had been decided and never written down. `core/config.py`
already shipped an `fcntl.flock` class whose docstring names this exact hazard,
one package away from both. Both hold it now, and both locks live in their own
declared `NEVER_RESTORED` state entry, because a lock beside the document it
guards has its inode swapped by a restore.

**U11's worst was a reader that could not tell a wrong document from an empty
one.** Only `json.loads` raising was caught, so a top-level list, a scalar, a null
`decisions` field, or records under a newer version's key all read as an empty
store. The next `record` then wrote that empty document back and permanently
deleted every prior decline. The module had been stamping a `version` into every
document and never reading it, while both of its sibling readers refuse on a
version mismatch. It recognizes positively field by field now, and refuses
everything else.

**U19's worst was a ledger keyed by file while the close gate asked per session.**
A second run deferring the same file took ownership of the first run's record, so
the first closed reporting a placed track that reached no playlist, and released
its capture. Marking matched on track alone, so run B could mark run A routed to
a destination B never wrote. A record is identified by the pair of session and
track now.

**One lesson generalizes past both units.** U11's two new countdown guards matched
bare attribute NAMES with no binding to the review module, so a module that
hand-edited a CSV and never touched the queue satisfied all three, through one
dead reference and an unrelated `.offer()` method. `import csv as spreadsheet`
also defeated `_constructs_a_csv_writer`, which was ARMED over every adjudicating
verb at the time; its self-test checked `import csv` and `from csv import
DictWriter` and never the alias. In the other direction, correct code written as
`from cratekit.core.review import offer` FAILED the countdown, which is P7 and is
how a guard gets switched off. **Running a guard against correct code is half the
job. The other half is running it against the evasion, and that is the half that
keeps getting skipped.** All of them bind through the import graph in four import
shapes now and ship fixtures for both directions.

**And one caller quietly opted out of a guard the previous unit had built.** U18
gave `trees.ContentRow.deleted` no default on purpose, because a default of False
means active, which is the permissive answer for a soft-delete marker. U19's
`content_rows` handed that default straight back through
`getattr(row, "rb_local_deleted", 0)`, so a track deleted in rekordbox would be
placed, marked routed, and closed over. A required field is only required where
somebody constructs it directly, and a producer with a defaulting accessor is
outside that protection.

## What U18 changed

**The bridge half.** `write/trees.py` collapses the five splice implementations
the source system carried across four files, plus its two copies of the rating
writer, into one module. All nine goldens matched on the first pass and have
matched through every fix since, which is the evidence the collapse changed no
bytes. Two emitters U17 had not shipped went into `rbxml` rather than being
hand-rolled at the call site: an empty sub-playlist, which no other writer can
emit and which the vocal routing has nowhere to write without, and a populated
catalog folder, the only write that creates its own tree. Hand-rolling either
would have made U17's coverage claim false in its first consumer.

**The database half.** Membership for rows that already exist, reaching the
medium check through `tree_registry.anchored_root` rather than spelling it
again, matching rows on the active-row rule with both sides normalized through
the shared primitives and the volume prefix map, and skipping and surfacing two
active rows on one location rather than writing to both.

**The catalog tree is declared taxonomy now.** R19 forbids a playlist display
name below the modules layer, so the tree a catalog import writes into sits in
the template beside the routing tree and the intake flow. Optional: a template
declaring none refuses by name rather than inventing a folder in a library.

## What the review found, because the pattern is the point, again

Seven reviewers. **Nine defects, none visible to a green suite**, and the two
worst were both a guard that was never armed rather than a guard that failed.

**The emitter guard was disarmed at the two entry points that build their own
tree.** `add_vox_playlists` and `insert_record_labels_tree` defaulted to
`rbxml.Tree(display=...)`, which carries no id and no registry and is therefore
UNGOVERNED, and the guard returns on its first line for an ungoverned tree
because most playlists in a real library are somebody's own. Reproduced against
a registry marking the routing tree native: the governed call refused, the
default call wrote. Under A2 that export replaces the database-native tree on
import. **The lesson is narrower than "check the guard fires": naming a tree
without the registry that governs it is naming nothing, and a test that asserts
a `tree=` keyword is present cannot tell the two apart.**

**The adopted root was asserted and then ignored.** `anchored_root` refuses a
tree whose root the library lacks, and the write then resolved its folder
globally by name, so the assertion held while the folder was created at the
database root beside the tree. That is the silent parallel tree the registry
exists to prevent, arriving through the check meant to prevent it.

The rest, shorter: `_first_child_offset` handed back a position OUTSIDE a
self-closed node, because its body start lands past the closing slash and the
bytes there are the break ending the node's own line; the vocal sweep
enumerated direct children and then wrote by a body-wide search, which resolves
to a nested namesake; the row index was rebuilt per plan entry, which is an
N times M walk and, worse, silently matches nothing after the first entry when
the caller's rows are a database cursor; every emitter warning was dropped; a
mid-loop failure left objects pending on the caller's handle to ride out on
whatever committed next; a declared-but-empty `[catalog]` table is falsy, so a
truthiness check skipped the validation its own comment promised; and a
hand-rebuilt `Taxonomy` in a test silently zeroed its four derived indexes.

**One shape is worth carrying forward on its own.** A countdown test this unit
armed asserted that three tokens appeared in `trees.py`'s SOURCE TEXT. The
module's own docstring explains why it calls all three, so the test passed and
would have kept passing with every call deleted. **A docstring that satisfies
the test written to check the docstring's claim is not a countdown; it is the
softening path wearing the guard's clothes.** It walks the syntax tree now, like
its sibling in `test_tree_registry.py` already did. When you arm a pending
guard, check what it actually asserts before believing it.

The battery is:

    .venv/bin/ruff check src tests scripts
    .venv/bin/python -m pytest
    .venv/bin/python scripts/scan_repo.py

## What U8 and U17 changed

**U8, the destructive-session boundary.** `core/snapshot.py` is the KTD21b
capture, deriving every path from the state inventory and spelling no file
suffix anywhere. `core/session.py` is the boundary: three gates in one order,
and the order is the property. Volume, then acknowledgment, then lock, because
the first two are read-only and the lock is the only gate that creates a file,
which is what makes "a refused session writes nothing" true on the disk rather
than approximately true.

It closed three pieces of standing debt. R-8, so both halves of the backup
restore now run inside the gates. R-5's quarter, so conformance assertion 6 is
behaviour rather than an existence check. And the runtime half of W4, which
fingerprints every analysis file a session could touch and refuses if one moved,
because the source scan sees only the symbols this package spells and cannot see
a grid rewritten through a handle the binding already returned.

**U17, the tree registry and the XML bridge.** `core/tree_registry.py` records
per tree the mode, the cutover date, and the adopted root's identifier. All trees
start on the bridge. `write/rbxml.py` ports the byte writer whole, with two
changes: indentation is derived from node depth rather than pinned, and the
byte-level LOCATES are consolidated rather than only the writes. Thirteen
distinct locate shapes were inventoried across the two byte engines and the eight
call sites in the source system, and each is named against the primitive that
covers it. Without that, "the guard lives inside the shared byte-writer
primitives" is a coverage claim that is simply false, because a guard in the
writers sees nothing a call site finds for itself.

## What the review found, because the pattern is the point

Both units passed their own author's battery. Three independent adversarial
reviewers per unit then found twenty-three defects that survived judgment, and
two of them were blocking. Neither was visible to a green suite.

**U8: the committed-unverified latch condemned its own remedy.** A session whose
post-commit read-back disagrees refuses with `restore-from-snapshot`. A restore
is itself a destructive session. So the product told the user to restore and then
refused the restore. The fix is `session.Intent`: a RECOVERY session is exempt
from that one latch and from nothing else, with volume, acknowledgment and lock
all still asserted. The second half surfaced only while fixing the first: the
session log is `SURVIVES_ROLLBACK`, so the condemning record outlives the restore
that answers it, and without `resolve_unverified_session` a user who did exactly
what the refusal asked would find the next write still refused with the remedy
already spent.

**U17: one unescaped angle bracket un-anchored the whole document.**
`matching_close` and `depth_of` bounded a NODE open tag with a plain search for
the next `>`, which is the exact shape the module's own comment says neither tag
can be bounded by. A display name carrying an angle bracket made `root_node`
return None, so every emitter reported "ROOT node not found" while writing
nothing, and a splice that still reported success landed in a different folder.
Both walks now use the quote-aware matcher `node_at` already had.

Three more from U17 could lose data outright: three writers picked the child to
replace or delete by display name alone, so a root-level playlist named after a
tree replaced that entire tree and returned success; `patch_attribute` would
write a track's average tempo, which the R17 source scan cannot see because the
attribute name arrives as a call argument; and the splice's create-missing path
never deduplicated, so whether a duplicate survived depended on whether the
sub-playlist happened to exist yet.

Two from U8 failed OPEN, which is the direction that matters:
`assert_no_unresolved_session` read the log through the tolerant reporting
scanner, so a bumped schema version on one file made an unresolved commit vanish
and admitted the next destructive session; and `holder_alive` judged a live
process dead whenever the platform would not report its start time, so
`release_stale_lock` would clear a running session's claim.

**The lesson to carry:** an author's own battery is not a review. Every one of
these passed 2600 tests written by the person who wrote the defect.

## Finish a merge like this

Merge one branch at a time, and after each one run the full battery on the
COMBINED tree before touching the next. A clean auto-merge is still not evidence
of compatibility.

Then hunt what a green suite cannot see. The two shapes this repository keeps
producing are a duplicate key in a mapping that several branches all appended to,
and one symbol meaning two things in two modules. For the first, parse the dict
or set literal and compare its element count against the runtime length, because
every other test iterates the runtime object and is blind to an entry collapsed
at parse time. For the second, walk the package and look for a name defined in
more than one module, then JUDGE each hit rather than trusting the list: most are
one idea correctly specialised per module.

That hunt earned its keep this wave. It found `"cratekit.core.session"` written
twice in `EXPECTED_PENDING`, which a set made harmless and which nothing else
could see. U8 removed it and added
`test_the_intended_pending_set_has_no_duplicate_element`, so the shape cannot
return silently.

One arithmetic check is worth doing and is cheap: the merged counts should be
exactly additive against the two branches. This wave went 2602 to 2812 passed
(+115 and +95) and 76 to 29 skipped (-24 and -23), which are exact. A number that
does not add up means a test was lost or double-counted by the merge.

**A note on worktrees.** Do NOT symlink `.venv` into a worktree. The editable
install names the MAIN checkout's `src`, so a worktree runs its own tests against
the main tree's package: a worker verifies code it cannot see and gets false
results in both directions. `pyproject.toml` carries `pythonpath = ["src"]` under
`[tool.pytest.ini_options]`, which resolves from pytest's rootdir and fixes it
FOR PYTEST ONLY. An ad-hoc `python -c "import cratekit"` in a worktree still
imports the main tree, so set `PYTHONPATH=src` for those. Symlinking the venv is
also what committed a `.venv` symlink and destroyed the real virtualenv when a
merge replaced the directory with a self-referential link.

## Where the reasoning lives

Everything that shaped these decisions is in the source repository, because it
quotes that system's paths and this repository's portability guard rejects those
by design:

- `DJ_tools/docs/plans/2026-08-01-001-feat-dj-product-reengineering-plan.md`, the plan
- `DJ_tools/docs/migration/00-SEAM-DECISIONS.md`, **authoritative** over any brief
- `DJ_tools/docs/migration/`, the six unit briefs and the wave prompts
- `DJ_tools/docs/runbooks/`, the U9 attended gate and its results
- `DJ_tools/docs/solutions/integration-issues/`, the A1, A3 and A4 verdicts

Read the seam decisions before implementing anything. Part 5 in particular is
seven failure shapes learned the expensive way, and they apply to every unit.

## What the U9 gate changed

**A1 is CLEAN, CONDITIONAL, and it moved a boundary.** rekordbox accepts,
renders, auto-analyses and stably keeps a database-inserted gridless row. The
single condition is `djmdContent.ContentLink`, which must equal the mode of that
column over the target library's live rows. pyrekordbox hardcodes `645482`, and a
row whose value differs renders and analyses perfectly and **cannot be loaded to
a deck**, so it fails at the gig rather than at write time. New-track intake can
therefore leave the XML bridge. KTD2 and R16 are rescoped in the plan.

**A4 is TOLERATED**, so `djmdKey` is in `PERMITTED_ROW_TABLES`. The permission is
a ceiling and not a licence: the writer may never author a key value, per the
decision recorded in the A4 solutions entry, and U21 is rescoped to it.

**A3 is INFERRED**, with no staleness check needed. The cross-check is deleted.

## What is unblocked, and what is not

Ask the board rather than this table, because the board recomputes and this does
not:

    .venv/bin/python scripts/board.py next

U11 and U19 between them unblocked four units. **U16 is the one to take next**:
it is the only unblocked unit that gates a whole phase, since U22, U26 and U37
all wait behind it.

| Unit | Title | Note |
|---|---|---|
| U16 | Three-state match and missing review | Unblocked by U11. Gates U22, U26 and U37. U11 registered a countdown against it: the needs-review state becomes queue items, and matched and missing stay a plain match result. |
| U23 | Library adoption | Unblocked by U11. U11 registered the adoption surface against it. |
| U34 | Read-only library reports | Unblocked by U11. |
| U36 | Tree rebuild and convergence check | Still unblocked, still unwritten. Must exist before the first cutover. |
| U27 | Setup wizard and doctor | Closes R-1, R-4 and R-7, and unblocks U28. It now also owes the deletion CLI shell and, underneath it, R-13's conformance-3 wall. |
| U30 | DJ_tools overlap changes | Owns moving the old system's lock, which is the real half of AE19. |
| U32 | Restore, retention, reconciliation | U8 registered three items against it, and R-12 proposes a fourth. |

U12 was already unblocked by the job engine and still is.

Still blocked: U20 on U30 and U36; U22 on U16; U25 on U12; U28 on U27; U37 on
U16. **U24 unblocked U26 and U33**, and U26 still waits on U16 and U22.

**U19 is now the first production caller of `write/trees.py`, and U26 will be the
second.** Two contracts are worth knowing before you write against it: the bridge
entry points take a `registry` and will refuse to guess, and
`write_tree_membership` owns its own session, because R29 declares the boundary
as one source per run and a caller-supplied gates factory would reopen the
analysis-roots hole U8 registered against this unit.

`tests/_pending.py` is the register. Each entry names the unit that owes the
work, so a gate that cannot run today is a countdown rather than a hole. It is
also the file `scripts/board.py audit` reads to catch a contradiction, meaning an
issue closed while the repository still says that unit owes a module, so an entry
here is the one check on the board's single unverified input.

U11 cleared its own entry, which is the countdown firing as designed. Eleven
entries remain, and the growth is the mechanism working rather than debt piling
up: U11 and U19 between them added five, each one an obligation that used to live
in a docstring.

| Unit | Target | Owes |
|---|---|---|
| U16 | `cratekit.acquire.match_cli` | the needs-review state becomes queue items; matched and missing stay a plain match result |
| U20 | `cratekit.write.routing_cli` | the routing CLI, plus closing through `close_run` and converging after a rename. See R-13: U20 is an inference, not a decision |
| U23 | `cratekit.adopt` | the adoption review surface |
| U27 | `cratekit.cli.doctor` | a database acknowledged outside the library root is reported every run |
| U27 | `cratekit.deletion.cli` | the deletion CLI shell. RE-POINTED from U24, which landed the engine and could not land a verb with an explicit gate (R-13) |
| U28 | `path:skills` | the shipped skills tree |
| U32 | `cratekit.core.restore` | the restore verb, and the three obligations U8 registered against it |
| U34 | `cratekit.modules.reports` | the duplicates review surface |
| U37 | `cratekit.intake`, `cratekit.intake.collection_xml` | record routing intents at the decision, close through `close_run`, and never emit a `<TEMPO>` element |
| U38 | `cratekit.cli.exit_codes` | the reserved exit-code registry |

## Open items that are not code

1. **The rekordbox application pin is deliberately not bumped.** The mechanism is
   correct and S2 is satisfied: an unset pin refuses, a drifted pin refuses and
   names its remediation, and the wizard may propose but only an explicit named
   decision records. Re-validating a pin against a real write is the author's
   deliberate act and never a number an agent edits.
2. **The vendored downloader has never been smoke-tested end to end.** Clone,
   install, authorize, download one track, confirm the file carries no tempo tag.
   That last check is the only end-to-end proof of the beatgrid patch, and the
   upstream wrote a tempo tag in three containers before it was patched. It needs
   Tidal authorization at the machine, so it is an attended step.
3. **Naming decisions recorded rather than resolved.** `authenticate-provider`,
   `reauthenticate` and `reauthenticate-provider` may be one idea; all three keep
   their original slugs because a slug is persisted inside a stored cause.
   `Decision` means two different things in `core/rb_writer.py` and
   `cli/gates.py`, and `FEATURES` means two different things in `cli/registry.py`
   and `modules/tools/__init__.py`.

   **Three more joined the list this wave, and two of them are cheap to resolve
   in a way the first three are not**, because nothing outside this repository
   has ever seen them:

   - `Gates` now means a resolver with a `require` method in `cli/gates.py` and a
     frozen value object in `core/session.py`. Both are exported, and both
     modules are ABOUT gates, so the module prefix does less disambiguating work
     here than it does elsewhere. Recorded rather than renamed for consistency
     with `Decision`, which is the same collision between the same two areas.
   - `STATE_KEY` means an inventory key in `core/backup_facts.py` and a record
     field name in `core/session.py`. Deliberately not renamed: session's spelling
     mirrors `RunStateVocabulary.state_key`, which is the field it populates, and
     breaking that mirror to fix a name would trade a real correspondence for a
     cosmetic one.
   - `Band` means a decade of the exit-code vocabulary in `core/exit_codes.py`
     and an energy band in `core/taxonomy.py`. Pre-existing, not from this wave.

   Judged and NOT defects, listed so the next hunt does not re-litigate them:
   `TERMINAL_STATES`, `lock_path`, `log_path` and `path_for` are each one idea
   correctly specialised per module, as are `load`, `save`, `get`, `record` and
   `show`. `Remedy` in six modules is the S4 subset pattern and is asserted as
   such. `rekordbox_processes_running` exists in `core/processes.py` returning a
   tuple with an injectable lister and in `core/rb_writer.py` returning a
   comma-joined string from its own probes; the divergence is deliberate and
   `tests/test_process_guard.py` asserts both, but note the return types differ,
   so a caller importing the wrong one gets a string where it expected a tuple
   and `", ".join(...)` on it produces character-joined output rather than an
   error.
4. **The ANLZ guard's honest gap is closed on both halves now.**
   `read_anlz_files` stays legal and returns live objects, so the name scan also
   forbids the tag setters. The runtime half landed with U8.
5. `docs/residual-findings.md` carries the recorded items with what closes each.

## Four verification gates need the library volume

Deferred by design, not dropped, per seam decision Part 4. Each is written
complete and gated on its fixture rather than deleted.

| Unit | Gate | Needs |
|---|---|---|
| U3 | parity against the live library's genre tag values | a fresh XML export |
| U4 | the parser handles every name shape in the live library | the same export |
| U31 | every active row in a snapshot resolves to a real file | a database snapshot copy |
| U7 | database integration, and both writers' dry-run paths | a database snapshot copy |

The conventions are `CRATEKIT_TEST_DB` for a database snapshot and
`CRATEKIT_TEST_REKORDBOX_SETTINGS` for a settings directory. Both SUBSTITUTE
rather than skip: the battery runs either way and a supplied fixture strengthens
it.

## Hazards worth carrying forward

**Autoflush in the guard path.** Giving the cloud canary a real predicate turned
it from reading nothing into running a query, and an ORM query autoflushes: a
caller's pending write was flushed out of the session and the additive whitelist
approved a commit it could no longer see. The guard would have passed a forbidden
write *because* the canary started working. W6 removed the query at the root, and
W2 made the guard resilient rather than merely unflushed by reading the binding's
update buffer as well. `_no_autoflush` stays regardless: deleting the containment
because its current occupant left is how the next probe inherits the hazard with
the fix already gone.

**Inspecting a transient instance poisons the process.** Reading a not-yet-flushed
object through the object mapper forces mapper configuration, and a failed
configuration is CACHED process-wide, so every later mapper use raises including
in code unrelated to the guard. Catching the exception does not undo it. Read the
instance dictionary instead. This cost twenty-three database tests in files the
change never touched.

**The binding's update buffer is process-global.** It is a class attribute, not a
per-session one. Reading it without an open handle attributes another caller's
writes to yours, and a guard that refuses correct code is one people route around.

**Closing a database does not release it.** The binding closes the session and
leaves the engine's pooled connection open, so the process still holds the file
and both sidecars. Restoring over them then produces a disk input-output error
against a database that is perfectly intact, which is a terrifying message at
exactly the wrong moment. Fixed here by disposing the engine; still live in the
source.

**A gate that reads its own state through a tolerant reader fails open.** U8's
`assert_no_unresolved_session` swallowed four exception types because it shared a
scanner with a REPORTING path, where dropping an unreadable record is correct.
For a gate it is not: an unreadable record is a record that has not been cleared.
One scan now returns both halves, and the two callers disagree on purpose.

**A liveness question and an identity question are not the same question.** U8's
`holder_alive` returned False when the platform would not report a process start
time, conflating "this holder is gone" with "I cannot tell". Three answers, not
two: False clears the lock, None refuses to.

**A byte writer cannot bound a tag by searching for the next angle bracket.**
Attribute values contain them. U17's depth walks did exactly what the module's
own comment forbids, and one display name would have un-anchored every emitter at
once while they all reported success.

**A self-closed node has no body, and the arithmetic does not notice.** Its body
start lands just past the closing slash, and the bytes there are the break ending
the node's OWN line, so an offset computed from it succeeds and points OUTSIDE the
node. U18's catalog writer would have written a whole tree beside a childless
playlist ROOT and reported success. Every new offset helper needs the
self-closing question asked of it explicitly, because nothing about the
arithmetic raises.

**Two writers that resolve the same name differently will disagree about which
node they mean.** U18's vocal sweep enumerated the tree's DIRECT folder children
and then wrote to each through a search over the tree's whole body, which resolves
a shared name to whichever node carries it first in document order. The
enumeration and the write have to use one locate or they are two locates.

**An iterable consumed once and reused looks like an empty library.** U18's row
index was rebuilt per plan entry. Handed a list it was merely quadratic; handed a
database cursor, which is the natural way to pass every content row, entry one
consumed the whole thing and every entry after it reported its tracks absent while
the run reported clean.
