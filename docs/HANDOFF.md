# Handoff: where Cratekit stands

Written 2026-08-01 so a session with no memory of the build can pick it up.
Revised the same day, twice: once after the three pending branches merged and
the U7 hardening landed, and again after U8 and U17. Revised 2026-08-02 after
U18, again the same day after U11 and U19 landed together, and again after U21.

## The work is tracked on a board now

`docs/BOARD.md` names it: https://github.com/users/philgutowski/projects/2

All 37 units, the 11 residual findings, and the attended items are issues on
`philgutowski/cratekit`, and the issue number matches the unit number. Each unit
issue carries its full brief from the plan, so a unit can be picked up without
the plan document. Eight units are Ready, twelve are Blocked, and the board says
which blocks which. Read BOARD.md for what to update when a merge lands.

## State

`main` carries U1 to U8, U10, U11, U13, U14, U15, U17, U18, U19, U21, U31 and
U35, plus the W1 through W6 hardening, the A4 whitelist addition, and U9's
verdicts. Pushed to the private remote. **3164 passed, 16 skipped**, ruff clean,
`scan_repo` clean.

**There are no unmerged branches and no worktrees.**

## What U23 changed

**Library adoption: a census nothing falls out of, an approval nothing stands in
for, and an undo that is exact.** `adopt/scan.py` classifies every collection row
into one of six named categories and one of five dispositions, so an unreadable
or cloud-backed file is a REPORTED fact rather than a row that quietly failed to
appear (AE12). `adopt/plan.py` carries every scanned row, including the ones it
will never touch, which is what makes "nothing was dropped" a set comparison
instead of a count. `adopt/approval.py` refuses every blanket affirmative at
runtime (R34). `adopt/apply.py` applies one entry at a time and resumes by entry
IDENTIFIER rather than by position. `adopt/revert.py` is the undo log for the one
write that sits outside the database snapshot entirely.

**`adopt scan` ships as a command line; `adopt apply` does not.** The census
verb queues its work through the job engine and reports a `job_state` envelope,
which needs no database, so it lands and the conformance suite drives it. The
apply verb is destructive, declares two gates, and stays behind the wall R-13
describes. The two used to share one `module=` string, which is what held the
census back.

### What round 1 of the adversarial review fixed

Eleven blocking defects. The four that mattered most:

**The unit would have silently no-opped against a real library.** The census
passed rekordbox's raw `Location` column to `resolve_recorded_path`, which
correctly refuses anything that is not a path. A real `Location` is a
percent-encoded file URL, so every row in a real library classified as
`not-a-path` and was excluded, while `covers()` reported that nothing had fallen
out of the plan. The arithmetic that was supposed to catch this compares content
identifiers, so it is a proof about PRESENCE and says nothing about correctness.
Every test around it built its rows from bare filesystem paths. The fix is one
`location_to_path` call; what would have caught it is a test using the shape
rekordbox actually writes, which now exists.

**The revert ledger recorded a corrupted copy of the original.** `read_tag`
strips whitespace, folds an empty value into absence, and returns the first of
several values. For a router asking a file what genre it claims to be, all three
are right. For an undo log they are three silent edits: a stripped value comes
back stripped, a value the ledger recorded as absent comes back DELETED, and a
second value comes back not at all. `core/tags.py` grows an EXACT pair,
`read_tag_values` and `write_tag_values`, beside the convenient one rather than
changing it, because the stripping is pre-existing behaviour four other callers
depend on.

**A gate refusal rewrote every file in the plan.** The tag write happened before
the membership write and a refusal from the membership writer was caught per
entry, so one systemic refusal inside the caller's destructive session produced
one irreversible file write per entry with zero memberships landed. The
recoverable write goes first now, which is the whole fix: a refusal costs no file
write at all, so the loop can go on reporting it per entry the way U19 requires.
Round 2 briefly also stopped the run on it, and see below for why that was wrong.

**A revert issued during an apply lost the original permanently.** The lock
covered each document's read-modify-write and nothing about apply against
revert. `write_tag_with_record` holds one lock across the record and the write,
and `revert_tags` holds the same lock across its whole pass.

The rest: the census died mid-generator on a permission error or a null byte and
took every later row with it; an unsupported container raised out of `apply_plan`
so the plan could never complete; mutagen's default ID3v1 handling destroyed a
legacy genre byte the ledger never recorded; the block-count probe called sparse
files and whole FUSE mounts cloud-backed; a stale `.icloud` stub hid a readable
file; the collision question was asked and nothing consumed the answer.

### What round 2 fixed, which was mostly round 1's own damage

**The flagship guard could not fail.** The 35-case exactness test defined its
expectation by calling the reader it was verifying, so both sides of every
assertion moved together. A mutant restoring all three of the losses the round
exists to close left the whole suite green. The expectation is now the
parametrised literal, cross-checked against an oracle that reads the container
directly and shares no code with the reader. Verified: that mutant now kills 50
cases across two test functions. `probe_readability`'s own totality wrapper had
the same shape, covered only by a second catch downstream, and is now driven
directly.

**Two regressions round 1 introduced, both in code it rewrote.** Breaking the
apply loop when a refusal's scope was wider than one item ended the pass on an
ORDINARY per-track refusal, because `cause.refuse` defaults to `Scope.RUN` and
nothing in `write/` declares `ITEM`. That is the per-track versus per-pass
failure U19 paid for, so the break is gone: the ordering was always the whole
fix. And decoding the recorded location made a NULL `Location` raise
`AttributeError` out of the census generator, one line above the probe that had
just been hardened against exactly that.

**One over-correction.** The revert's size and mtime check refused three
legitimate libraries: a later write of any other field this module owns, a
byte-identical file whose mtime moved, and an interrupted revert pass retried.
The record already carried direct evidence the guard was not consulting, so the
field's own value is asked first and the stamp only decides when that is
inconclusive. `revert_tags` gains `force`, because a heuristic over somebody
else's file with no override is a heuristic that decides.

**One smaller one.** Asking about the container after `place` meant an
unsupported container got its membership, was failed, and could never reach
applied, so every re-run placed it again. The question is now asked before
anything happens for the entry.

### What round 3 fixed, which was round 2's own over-correction

**The loosened revert guard defeated itself in the likeliest case.** Round 2
accepted "the field still holds what adoption wrote" as proof the file was
adoption's own output. The value adoption writes is a taxonomy bucket's DISPLAY
name, shared by most of the library, so a stranger's recording whose own genre is
that bucket satisfied it exactly. Measured: the revert then wrote one file's genre
onto another file's audio, destroyed the replacement's own genre with no record,
and dropped the ledger record. The round 2 test that claimed the guard still bit
had picked the one replacement genre that dodged the branch.

The guard was rewritten around size and time unchanged, or a digest recorded at
write time. The inode was measured and rejected, because `write_bytes` and `cp`
both truncate in place and keep it. Each record is now dropped from the ledger as
its own file is restored rather than at the end of the pass. The one remaining
legitimate refusal, a later write of another field this product owns, is residual
R-22 with the fix named.

**And the same commit that took a per-track-versus-per-pass failure out of
`apply_plan` put one into the undo log.** A record naming a field this build does
not know made the whole revert raise before the lock released, so nothing settled
and every retry died on the same record. The loop body is guarded per record now.

Also: `force` takes a list of `(path, field)` pairs, because a refusal printed per
record must not hand out a pass-wide override; a `Path`-valued `recorded` resolves
instead of excluding the whole library; and the container list under test is
derived from the writer's own table, which grew it from seven suffixes to eleven.

### What round 4 fixed, which was round 3's own two over-claims

**Round 3 recorded the digest and then never asked it.** Its acceptance order was
"size and time unchanged" FIRST, returning before the digest was consulted, so
the one piece of evidence a replacement cannot forge sat unread while the two it
can forge decided the answer. `st_mtime_ns` is metadata: `os.utime`, `touch -r`,
`cp -p`, `rsync -a`, `tar -x` and every tag editor with a preserve modification
time option set it to whatever they are told. Measured: different audio written to
the path, padded to the recorded size and stamped back to the recorded time,
restored anyway, `restored: 1  failed: {}`, the replacement's genre destroyed and
the record dropped. That is verbatim the harm the refusal message names, reached
past definitive contrary evidence already in the record.

Round 4 made the digest the answer whenever there was one, and left three states
in which there was not one. Round 5 removed all three; see below.

**And "the interrupted pass is eliminated structurally" is a stronger claim than
the code makes.** Dropping each record as its file is restored narrows the window
from the whole pass to one record; it does not close it. A run that dies between a
restore landing and that record's drop reaching the disk strands exactly that
record, refused on every retry. Written down as residual R-24 and pinned by a test,
because the damage is bounded (forcing it writes the same original onto a file
that already holds it) but the claim was not.

Also: the deleted-file refusal now asserts its REASON rather than only its key,
which is what made the existence check kill zero tests. Round 3's mutation table
would have caught all three: the size-and-time acceptance, the cloud-eviction
check and the existence check each killed zero tests out of 3705.

### What round 5 fixed: the same shape, a fourth and fifth time

The unit had one recurring defect and it appeared four times in one function:
**taking something that is not identity for identity.** Round 3 took size and
mtime. Round 4 fixed that and left three more doors, and all three were doors
that stepped around the digest rather than reading it.

**An unstamped record accepted any file at all, and an ordinary Ctrl C reached
it.** `snapshot_before_write` persists the record, the mutagen tag write runs,
and only then does the stamp go on. The whole tag write sits in that window and
it is the slowest part of the operation. The guard returned "unchanged" from a
record with no size, no time and no digest BEFORE consulting anything. Driven
with no forgery and no I/O error: interrupt in the window, replace the track
months later with a different recording of a different size, and the revert wrote
the old genre onto the stranger's audio, destroyed the replacement's own genre
and dropped the record. It now refuses and `force` spends it.

The 115 parametrisations that died when that branch was mutated were not coverage
of it. They all rode one fixture that took the record half and wrote the tag
separately, so every one of them traversed the widest branch in the guard without
being about it. They go through `write_tag_with_record` now, which is what
`apply_plan` uses.

**A failed stamping read silently downgraded the guard to forgeable metadata.**
`digest_of` answered `""` on `OSError` and `_stamped` stored it without comment,
producing a record indistinguishable on disk from a document predating digests.
The two are not the same thing: one is a file this build wrote seconds earlier
where the read could be retried. `DigestState` makes them three named states, the
read is retried once, and a record that still cannot produce a digest refuses.

**The eviction branch skipped the digest to avoid a download the accept path then
performed one line later.** Driven with the real writer instead of the stub the
old test used: `restore_tag` opens the file with mutagen and rewrites it, so the
provider fetches it either way. The branch is gone. The cost that remains, a
whole-file hash on the refusing path, is recorded honestly as R-25 rather than
argued away as free.

**Four zero-death guards, three of them round 4's own new code.** Round 4's
report said "no zero-death guard remains", which was false. The eviction
branch's `untouched` half, the two refusal constants it introduced ("named once
so a report and a test cannot spell them apart", which nothing spelled), and
`scan.DATALESS_FLAG` itself, which survived being set to `0x1`.

**And the self-referential assertion that hid the last one.** Two tests set
`st_flags = adopt_scan.DATALESS_FLAG` and then asserted the behaviour that
constant produces. That reduces to X equals X: the flag could be `0x1` and both
tests would pass while every file carrying `UF_NODUMP` took the eviction branch.
Both fixtures now spell the literal `0x40000000` from `sys/stat.h`, and a test
pins the constant to it. The same treatment is applied to every refusal message:
the suite asserts the literal string in the report, never the constant the report
is built from.

**Net:** one acceptance where there were three, and it is the recorded digest
matching the file's bytes. Everything else refuses, names which of the four ways
it is, and names the `(path, field)` pair that overrides it.



**The per-field metadata policy, and the registration that inverts it.**
`write/metadata.py` is the only place feature operation names appear. U17 had
already landed the decision layer in core, generalized so no core module names a
feature, so this unit is the registration side rather than a second
implementation. Three operations declare their fields, and
`rb_writer.content_writable_columns` becomes the union of what is enabled. A slim
install with no metadata features enabled has no writable content column at all,
which is R14 implemented rather than described.

**The key field is refused at registration, not merely absent.** Absence already
yields `skip_unowned`, which is correct and fragile: one plausible looking entry
in a later unit undoes it, and the person adding it would not know what they
undid. `UNWRITABLE_FIELDS` refuses `KeyID`, `ColorID` and `Commnt` before a
policy can reach the registry, each with its argument attached. A4 proved
rekordbox leaves an externally authored lookup row completely untouched across a
launch cycle, but that permission is a ceiling and not a licence, so no resolve
then create path for keys exists to be widened later.

**The countdown walks the syntax tree, and the negative control earned its
keep.** The first version of the guard checked `ast.Name`, `ast.Attribute` and
`ast.alias`, and passed every positive control except `def resolve_key_id(...)`,
which is a `FunctionDef`. The brief's words are that the shape "does not exist",
and a module can define one without ever naming it again. The lesson from U18's
docstring countdown holds here twice over: this module documents at length why it
never authors a key value, so a source-text check would be green for the wrong
reason forever.

**Two fixes not asked for by the brief.** The genre lookup returns the first
ACTIVE row rather than the first row, because a soft-deleted namesake sorts ahead
often enough to matter and the source's shape reports "no such genre" for a genre
the library plainly has. And padding runs through `naming.pad_head` rather than a
fourth hand-rolled regex; the source's two copies disagreed with each other, and
one prepended a second head onto titles that already had one.

**Its verification gate is DEFERRED, not passed.** The brief asks for key padding
run database-direct against a snapshot, passing the live rekordbox gate. The
library volume has been offline since 2026-08-01. Everything landed is pure or
duck-typed and needs no database, but that is not the same as having run.

**Two registry entries were repointed.** `name.apply` and
`metadata.mytags-vocals` carried `planned_in="U21"` while the brief and the plan
both name only two files, neither a CLI shell. They now name U37 and U25, each
beside a neighbour already marked for that unit. Both modules stay absent and the
contract suite still asserts they are, so the countdown survives against the
units that now genuinely owe them.

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
| U24 | Track deletion and tombstones | Unblocked by U11. U11 registered the declines and tombstones countdown against it. |
| U34 | Read-only library reports | Unblocked by U11. |
| U36 | Tree rebuild and convergence check | Still unblocked, still unwritten. Must exist before the first cutover. |
| U21 | Metadata writers | Rescoped by A4: the writer may never author a key value. |
| U27 | Setup wizard and doctor | Closes R-1, R-4 and R-7, and unblocks U28. |
| U30 | DJ_tools overlap changes | Owns moving the old system's lock, which is the real half of AE19. |
| U32 | Restore, retention, reconciliation | U8 registered three items against it, and R-12 proposes a fourth. |

U12 was already unblocked by the job engine and still is.

Still blocked: U20 on U30 and U36; U22 on U16; U25 on U12; U26 on U16, U22 and
U24; U28 on U27; U33 on U21 and U24; U37 on U16.

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

U23 cleared its own `cratekit.adopt` entry and added `cratekit.adopt.apply_cli`
in its place, which is the same mechanism at a finer grain: the engine landed,
so the engine's countdown expired, and the CLI obligation it left behind now has
a target of its own instead of being owned by a `planned_in` marker on a closing
issue. That last shape is R-13's failure and is live three times over already.

| Unit | Target | Owes |
|---|---|---|
| U16 | `cratekit.acquire.match_cli` | the needs-review state becomes queue items; matched and missing stay a plain match result |
| U20 | `cratekit.write.routing_cli` | the routing CLI, plus closing through `close_run` and converging after a rename. See R-13: U20 is an inference, not a decision |
| U24 | `cratekit.deletion.cli` | declines and tombstones go through the revocable decision store |
| U27 | `cratekit.adopt.apply_cli` | the apply shell, and the destructive session and library lock `apply_plan` says it does not take (R-20). See R-20 for what the wall in front of it actually is, which is not what R-13 says |
| U27 | `cratekit.cli.doctor` | a database acknowledged outside the library root is reported every run |
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
