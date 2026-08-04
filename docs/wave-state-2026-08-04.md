# Wave state, snapshot taken 2026-08-04

**This is a snapshot and it goes stale.** It supersedes
`wave-state-2026-08-03.md`, which is now wrong in several named places listed
below. Trust `git log`, the branch tips, and `board.py next` over anything
written here. This file exists only because the per branch review state is not
recorded anywhere else.

This session ran out of budget mid flight. Eight agents were killed in place.
**Read the cleanup gate before running anything.**

## What is on main

`c114afa`, pushed, clean. Two merges:

- `3269ab1` the conformance 3 correction, alone.
- `c114afa` U36, `Closes #36`, the only unit merged so far.

Battery on main: ruff clean, **3278 passed, 17 skipped, 3295 collected**,
`scan_repo.py` exit 0.

`board.py audit` returns **exit 1, drift**, naming #52 and #53, the two live
fire findings not on the board. That drift predates this session and is
unrelated to U36. Exit 1 is the repairable failure mode. Nobody has run `sync`.

## THE CLEANUP GATE, do this first

Six worktrees were left dirty by killed agents. **Nothing in any of them is
committed work.** Two different causes, and they need different handling:

**Leaked mutations. RESOLVED 2026-08-04.** These three worktrees held VERIFIER
agents, which are report only and must never modify a file except to run one
mutation and restore it. A dirty file there is a mutation that never got
restored:

    .worktrees/u12   tests/_source_guards.py
    .worktrees/u24   src/cratekit/deletion/library.py
    .worktrees/u34   tests/modules/test_reports.py

All three restored themselves when their drivers unwound. Re checked after the
session limit: **all three worktrees are clean and their tips are unchanged**,
so nothing leaked into a commit. No action needed. Kept here because the
failure mode is real and will recur: a killed verifier can leave a mutation on
disk, and the next agent to enter that worktree would verify the mutant.

**Unfinished fix rounds. Uncommitted, unverified, no mutation table, no
battery.** These three held FIX agents partway through a round:

    .worktrees/u16   docs/residual-findings.md, acquire/match.py,
                     acquire/match_cli.py, tests/test_match_states.py
    .worktrees/u27   docs/residual-findings.md, cli/doctor.py, cli/render.py,
                     cli/setup.py, core/cause.py, core/exit_codes.py,
                     core/preflight.py, tests/test_doctor.py
    .worktrees/u38   docs/residual-findings.md, tests/_source_guards.py,
                     tests/test_reserved_causes.py

A half written fix round is worth less than none, because it looks like work
that was checked and was not. Default to discarding and re running the round
from its brief below. **One exception, and it matters: U27's round 5 was
essentially finished** and reported a complete 45 row mutation table with no
zero death guards before it died. See the salvaged findings section. Keep that
diff, finish it, and put it through an adversarial verify. U16 and U38 were
early enough that re running is cheaper than auditing.

`.worktrees/u23` and `.worktrees/u32` are clean. So is
`.worktrees/conformance` at `897ef12`.

## The eight unit branches

None merged. Every one has had implementation, adversarial review, and between
three and five fix rounds. **Sixteen verifications completed this session and
every single one came back blocking**, which is why the merge lane is still
empty behind U36.

| Branch | Tip | Rounds | State |
|---|---|---|---|
| `unit/u12-...` | `646a464` | 3 | round 3 committed, verification was IN FLIGHT and is lost |
| `unit/u16-...` | `6cf5d67` | 3 | round 3 verified BLOCKING, round 4 was in flight, uncommitted |
| `unit/u23-...` | `d5776bd` | 5 | round 5 committed, verification was IN FLIGHT and is lost |
| `unit/u24-...` | `b8fde7d` | 4 | round 4 committed, verification was IN FLIGHT and is lost |
| `unit/u27-...` | `830275d` | 4 | round 4 verified BLOCKING, round 5 was in flight, uncommitted |
| `unit/u32-...` | `bf01251` | 5 | round 5 committed, verification was IN FLIGHT and is lost |
| `unit/u34-...` | `7215ce3` | 3 | round 3 committed, verification was IN FLIGHT and is lost |
| `unit/u38-...` | `70c160f` | 3 | round 3 verified BLOCKING, round 4 was in flight, uncommitted |

Each worktree has its own venv. Run its battery from inside it, and note the
invocation, which is not what the 08-03 snapshot implied:

    cd .worktrees/u36 && ./.venv/bin/python -m pytest --tb=no

**Never pass your own `-q`.** `pyproject.toml` already sets `addopts = "-q"`,
so `pytest -q` resolves to `-qq`, which SUPPRESSES THE SUMMARY LINE ENTIRELY.
The run prints dots, then `[100%]`, then nothing: no pass count, no fail count.
Every mutation table depends on counting deaths off that line. Use
`pytest --tb=no` for counts and `pytest --collect-only -o addopts=` for the
collected count.

## Corrections to the 2026-08-03 snapshot

1. **`match.TOMBSTONE_KIND` and `match.version_identity` do not exist.** The
   real surface is `cratekit.core.tombstone`, exporting `DECLINE_STORE_KEY`,
   `KIND_REMOVED_FILE`, `KIND_VERSION`, `STORE_KEY`, `describe`, `fold`,
   `removed_file_identity`, `version_identity`, and `version_title` which U24
   added this session.
2. **U36's R-14 and R-15 became R-16 and R-17 on merge**, because main already
   held its own R-14 and R-15 from the live fire findings. U32's R-21 refers to
   the entry by its old branch number and says so in its own text.
3. **R-21's item 5 is not silent.** With items 2, 3 and 4 applied,
   `tests/test_restore.py` fails to COLLECT and a plain `pytest` run exits 2
   with `Interrupted: 1 error during collection` and runs nothing. It looks like
   a suite that refused to start, not one that passed. The magnitude has been
   restated twice and is tip dependent.
4. **R-21 was missing four textual conflicts**: `docs/residual-findings.md`,
   `src/cratekit/core/cause.py`, `tests/test_layering.py` and
   `tests/test_pending_units.py`. `test_layering.py` is a BOTH SIDES MUST
   SURVIVE resolution, verified empirically: both kept gives 48 passed, main's
   side wholesale gives 1 failed, the branch's side gives 2 failed.
5. **`_package_offers_into` is not U23's.** It is pre existing on main as a one
   liner without the fallback. U23 extended it; U34 independently added
   `_target_offers_into` doing the same job. At merge, keep
   `_package_offers_into`, delete `_target_offers_into`, repoint U34's call
   site. Verified equivalent for every input the registry table can produce.

## Phillip's decisions, standing

**U27 merges WITHOUT a closing trailer for issue 27** (decided 2026-08-03).
Still correct, and now better supported. U32's `session.restore_cli` writes the
database and is genuinely behind the surviving half of the wall, so U27 cannot
close regardless of the other two obligations.

**U24 merges WITHOUT a closing trailer for issue 24** (recommended
2026-08-04, unopposed, not yet confirmed by Phillip). Driven twice
independently: the R34 half of the wall is DOWN, an explicitly gated verb
refuses resumably and proceeds after `run decide`, but `delete.review` then
fails at exit 22 `LIBRARY_UNAVAILABLE`, which is genuine because a verb that
reads the collection cannot exit OK without a rekordbox database.
`board.pending_units()[24]` still owes `cratekit.deletion.cli`, and `cmd_audit`
returns 2 for any unit closed while owing a module.

**Do not touch:** U30's board state, U20, U29, R-9, A1, A2.

## A trap that nearly cost the wave

**GitHub matches a closing keyword ANYWHERE in a commit body, not only in
trailer position.** U24's fix agent wrote the literal keyword and issue number
inside a sentence explaining that the trailer must not exist. That would have
closed the issue on merge and made `board.py audit` return exit 2 permanently,
which is the exact outcome five rounds of work established must not happen.

**Before committing any merge, scan the body:**

    git log -1 --format=%B | grep -inE '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[[:space:]]*#[0-9]+'

For U24 and U27, that must return nothing. Spell it around: "without a closing
trailer for issue 24". Main is currently clean; the only match in its history
is the intended one on the U36 merge.

## Merge order and the traps

1. **U24 before U16.** After both, U24 must delete the
   `cratekit.core.tombstone` entry U16 added, which is what arms U16's cross
   copy drift guard. That guard is gated by `@_pending.requires` and is in the
   skip list until U24's module lands.
2. **U32 next, with the SIX items in R-21**, now that U36 is on main. Two fail
   silently rather than red. R-21 has been verified against a real `git merge`
   in a scratch clone: the six are necessary AND sufficient.
3. **U27 and U24 without closing trailers.**

**Silent trap:** `tests/_pending.py` between u23 and u34 is a false conflict in
**two** hunks, and the two DELETIONS ARE ADJACENT so their context overlaps.
u34 deletes main's `cratekit.modules.reports` entry, u23 deletes the
`cratekit.adopt` entry immediately below it, and both append a new entry at the
same anchor. Correct resolution: delete BOTH old entries, append BOTH new ones.
The same shape repeats in `tests/test_pending_units.py`.

**Residual numbering now collides three ways.** Main holds R-16 and R-17 from
U36. U24 carries R-16 through R-20. U16 defines its own R-17, different from
main's, and `match.py` cites it. Renumber sequentially in merge order and
verify:

    grep "^## R-" docs/residual-findings.md | sort | uniq -d   # must be empty

**A renumber silently repoints source citations.** This bit once already: U36
merged carrying `core/convergence.py` saying "See R-15", which on the merged
tree named a completely different finding. U32 solved it properly and the
solution is worth copying everywhere: hold the finding TITLE in a module
constant, cite the constant from the docstring, and add a test that parses the
`## R-N. Title` headings out of `docs/residual-findings.md` and asserts every
cited title still resolves. A renumber stays green, a retitle or a deletion
goes red.

Use git's merge algorithm only. `diff3 -m` silently produces a broken merge of
`tests/_pending.py`. `git merge-file` per file does not exercise rename
detection; use a scratch clone and real `git merge`.

## What each branch needs next

Every branch below has a completed verification report naming its findings. The
reports themselves are lost with the session, so the findings are summarised
here at the level a fix round needs.

**U12, `646a464`.** Round 3 committed, never verified. It rewrote the cgroup
reader to walk `/proc/self/cgroup` properly, threaded the importing file's
package through the import walk, and pinned the reap ladder rung by rung.
Verify round 3, attacking: the malformed `/proc/self/cgroup` surface, the
ancestor versus leaf cap chain, whether a namespaced container and a machine
with no cgroup file behave exactly as before, and whether the two signal tests
are timing dependent flakes.

**U16, `6cf5d67`.** Round 3 verified BLOCKING, four findings. Round 4 was in
flight and is unfinished. (a) `Wanted.addresses` composes credit stripped
addresses, so deleting a plain record silently withholds the credited one;
round 3 made the multi group case worse, four credit free addresses where round
2 had one. (b) Four zero death guards, all in round 3's new code, at
`match.py:500`, `:504`, `:548` and `:755`. (c) The library now decides how a
string parses, so one list produces different `match_id`s on two machines,
which breaks `crate review export`/`import`, and on one machine moving the
confirming file flips the reading and strands a resolved item invisibly,
bypassing `CANDIDATE_GONE`. (d) An undecidable parse is promoted straight to
matched with no question, against the module's own stated property.

**U23, `d5776bd`.** Round 5 committed, verification in flight and lost. Round 5
closed the unit's recurring shape at the root: `_changed_since_adoption` now
has exactly one acceptance, the recorded digest matching the bytes, and five
named refusals. `DigestState` makes "could not be computed" distinguishable on
disk from "was never recorded". Verify round 5, and drive the case nobody has:
**evicted AND offline**, where reading the digest must fetch bytes that cannot
be fetched.

**U24, `b8fde7d`.** Round 4 committed, verification in flight and lost. Verify
round 4, attacking the new closed vocabulary in `_reads_as_version`, which is a
whitelist and therefore the shape main's R-15 forbids: find the real mix names
it misses. Trial merge measured 3440 passed, 3456 collected.

**U27, `830275d`.** Round 4 verified BLOCKING, five findings. Round 5 was in
flight and is unfinished. (a) `_is_a_volume_mount_location` compares path parts
case sensitively on a case insensitive volume, so a lowercase `/volumes/...`
records the BOOT DISK as `library.volume_id`. (b) `_seed_taxonomy` reports an
unreadable packaged directory as a template that does not ship, the fourth
handler of a collapse round 4 fixed three of. (c) An unreadable `.git` marker
reports as "names no git directory" at INFO, so doctor exits 0. (d)
`is_mount_point`, the one fact the whole round 4 rule turns on, is covered by
nothing: hardcode True and the suite is green, hardcode False and it is green.
(e) A zero death guard absorbed by `answer()`, ten lines below the one round 4
found and fixed.
**R-18 item 3 is wrong in a load bearing way and must be fixed rather than re
filed.** The wizard does not traceback; the dispatcher renders the user's own
filesystem permission as `internal-error ... this is a defect; report it`. On
macOS a library root under `~/Documents`, `~/Desktop`, `~/Downloads` or an
external volume raises EPERM from `stat` without Full Disk Access, and
`Path.exists` re raises rather than answering False. That is a routine first
run state, not a curiosity.

**U32, `bf01251`.** Round 5 committed, verification in flight and lost. Round 5
was the highest quality round of the session. Verify it, attacking the one new
source change: a deterministic refusal in `_stage_companion_aside` so a staged
companion is never overwritten. A new refusal on the destructive path is where
this project over corrects, so check whether a legitimate retry after a partial
failure now refuses. Also reconcile its collected count, which nets only +2
despite adding several tests.

**U34, `7215ce3`.** Round 3 committed, verification in flight and lost. Round 3
narrowed the reflection flag correctly and introduced a receiver qualified
`QUALIFIED_MUTATIONS`. Verify it, attacking the receiver resolution through
imports, which is where aliasing defects live: aliased imports, a local
variable shadowing a module name, a receiver from a function return.

**U38, `70c160f`.** Round 3 verified BLOCKING, three findings. Round 4 was in
flight and is unfinished. (a) The widening of the key set from 22 to 82 strings
genuinely over fires, 20 of 28 ordinary shapes, because the reserved range 10
to 59 is exactly the band ordinary timeouts and levels live in. **And the test
certifying it safe is vacuous**: its fixture values are all outside the range,
so it passes with an empty key set. (b) Comments assert unreachability for code
that is reachable, with false reasons; R-16's header claims all six were
verified unreachable and only one is. (c) The off the top guard reverts with
zero deaths, and the assertion whose comment claims to cover it passes without
it.
**R-15 on that branch is wrong about its own file**: it records the defective
import walk as living on main, and lines 85 to 90 of U38's own committed file
are that same defective expression.

## The parked branch

`fix/conformance-3-and-soft-delete-reader` at `897ef12` is untouched and clean.
It still carries the live `write/metadata.py:195` permissive reader fix, and
**that defect is still live on main**. Out of scope for this session by
Phillip's framing. Its guards took defects in three consecutive rounds, so only
the conformance third was ever lifted out.

## The method, and what actually worked

The instruction that produced almost everything: **require a mutation table
from every fix round.** Revert each new guard one at a time, run the full
suite, count the deaths. A guard that kills zero tests is a finding.

Three refinements this session earned:

**An author's own mutation table is a draft, not a result.** Every fix agent
ran the table honestly and still missed guards its own round created, because
it mutates what it believes it changed. U12 round 2 claimed zero zero death
rows and shipped eight. U16 round 3 claimed 17 rows and no zero deaths; an
independent 33 row sweep found seven. Only an agent that did not write the code
re derived the table correctly. The separation is doing the work.

**Sweep with an AST walk, not a grep.** The highest yield defect is a test
whose expected value comes from the code under test, which reduces the
assertion to X equals X while genuinely exercising the code, so it is invisible
to every other technique. U32 parsed every `assert` in `tests/` and found four
real instances among 75 candidates that every grep based pass on every branch
had missed. It appeared in at least five units.

**Mutate constants to a REALISTIC nearby value, not only an absurd one.** U32
shipped a constant that died at 0.0 and survived 1.0. The absurd value proves
nothing; the value a real person would actually change it to is the test.

Also load bearing, and cheap:

- **A guard covered by another guard is a guard nothing covers.** Remove each
  layer alone. U27 found one instance, named the class, fixed the instance, and
  left its sibling ten lines below.
- **Check the collected count on every mutation row**, not just the pass count.
  A test file that fails to COLLECT takes its tests with it and the run still
  looks green.
- **Run mutation rows synchronously in the foreground.** Two agents lost turns
  backgrounding a driver and polling it, and one left a mutation applied on
  disk when its driver was killed mid row. A killed driver is exactly how a
  leaked mutation reaches a commit.
- **Never let a driver invoke git.** `git checkout` silently discards
  uncommitted edits. Snapshot and rewrite file text, and verify the restore
  against the git object database rather than against a scratch copy, since a
  contaminated scratch copy certifies itself.

## The through line

The 08-03 snapshot named two patterns worth carrying anywhere. Both held all
session, and a third emerged.

**Absence read as evidence of absence.** "I could not observe" folded into
"there is nothing there." U27 is the epicentre and it has now produced four
distinct shapes of it across four rounds.

**Identity that is not unique to the thing it identifies.** U16 and U24 fail
from opposite sides of one seam: U24 under distinguishes by reading only the
title column, U16 over distinguishes by composing. The drift guard built to
catch exactly this was structurally blind to it, because it compared the two
functions by handing both the same string when the real risk was different
derivations.

**And the new one: fix rounds fix the instance they were handed and reproduce
the class one file over.** Round 4 of U32 condemned the self referential shape
in its own commit message, fixed that instance, and wrote the identical shape
into the test it added for a different constant. U27 round 4 named the guard
covered by guard class in prose and left a sibling ten lines away. U38 round 3
fixed one import walk and left the broken one 250 lines above it in the same
file, then filed a residual saying the broken copy lived on another branch.

## Findings salvaged from the killed agents

Four agents got a partial result out before the session limit cut them off.
These are unverified fragments, not results, but each names a specific address
worth going straight to rather than rediscovering:

- **U16, fix round 4.** "M8 came back zero death. My R-22 fix now reaches that
  address by a second route, masking it." A fix that makes an existing guard
  untestable is the relocation failure, not a repair. The round 4 brief must
  treat M8 as unresolved.
- **U24, verify round 4.** "24 of 27 vocabulary words unpinned on the subset."
  Concrete and damning against the new `_VERSION_WORDS` closed vocabulary:
  almost the whole vocabulary can be removed with the suite still green, so the
  list is asserted nowhere. Go straight there.
- **U27, fix round 5.** "All 45 rows covered, no zero death guards. Final
  battery." Round 5 was all but finished and its mutation table was clean. The
  uncommitted diff in `.worktrees/u27` is that round. It is still unverified by
  anyone but its author, so it needs an adversarial pass, but discarding it
  throws away a complete 45 row table.
- **U12, verify round 3.** "Two zero death rows already." Round 3 has at least
  two guards covered by nothing. Not yet identified which.

## Verifications from the 2026-08-04 recovery session

Three verifications completed after the session limit was lifted. All three
came back BLOCKING. Recorded here because these are the highest value output
of the wave and they exist nowhere else.

### U23, the worst finding of the wave, and it destroys user data

`revert.py:154`. **Adoption identity is a digest of the PATH, so two recorded
locations that name ONE file on disk produce two ledger records.** Two shapes,
both driven end to end with real FLAC and the shipped `genre` field:

- a hardlink or symlink, `os.link(a, b)`, gives 2 records for one inode
- `Song000.flac` and `song000.flac` on a case insensitive volume, which is
  APFS default and the platform this product targets, because
  `location_to_path` normalizes Unicode composition and NOT case

The second record stores adoption's own value, `Adopted Bucket`, as the
original. Revert then behaves differently depending on **the sort order of two
sha256 path digests**. In the bad ordering it restores the real genre, then
refuses on the bogus record with *"its bytes are not the ones adoption left
there"*, an accusation of tampering caused by its own previous line. The user
does what the message instructs, `force=(path, 'genre')`, which writes
`Adopted Bucket` on as the original, reports `restored`, and empties the
ledger. **The user's real genre is then in no file and no record.**

The fix is at identity, not comparison: `(st_dev, st_ino)`. **Do not lowercase
the path.** Case insensitivity is a property of the volume, not the path
string, and lowercasing collapses two genuinely different files on a case
sensitive volume, which is the same bug pointed the other way.

Second U23 finding: `_changed_since_adoption` calls `digest_of` with no
timeout while holding the ledger's exclusive lock. Driven with a FIFO at the
recorded path, `open()` never returns and every other apply and revert in the
library blocks behind it. R-25 documents the cost as bandwidth only and is
wrong about the severity.

### U32, a rehearsal that passes and a run that destroys

`restore.py:1631`. Round 5's "never overwrite a staged companion" refusal went
on the PERFORMING path and not the preflight. With two companions present and
the second's resting name occupied, `run()` moves `master.db-wal` out of the
live tree and THEN refuses, aborting with the write ahead log gone and the
database never replaced. That is verbatim the state the docstring says the
staging exists to prevent. **`dry_run=True` reports all 8 steps performed and
refuses nothing.** A rehearsal that passes followed by a run that destroys is
the most misleading shape this module can have.

The refusal also emits `remedy=report-defect, retryable=False` while a fresh
plan demonstrably succeeds, and its only assertion is `reason ==
"internal-error"`, the eleventh use of that slug in the file.

### U34, and the finding nobody was looking for

`test_reports.py:1769`. The read only guard resolves a receiver only from the
import table, so `alias = config` then `alias.save(cfg)` writes the config
file with both structural guards green. Two lines, in a module that already
imports `config`. Eight more bindings miss the same way.

The one nobody asked for: **the guard has live FALSE POSITIVES today.**
`def f(config): return config.load` is reported as a write, because an
unresolvable receiver falls back to being treated as a module named after the
variable. A guard that fires on ordinary code is one the next author weakens.

### U24, the largest report of the wave

32 of 78 mutations kill zero. Eleven findings. **The closed vocabulary round 4
added cannot be repaired by adding words.** 24 of its 27 entries delete
individually with the suite green, and emptying all 27 kills only 8 tests.
`mix`, the commonest version word in the library, is unpinned because the tests
needing it use `Extended Mix` and `extended` covers it, and the reverse.

It fails in both directions at once. 56 of 75 genuine version designations read
as NOT a version, including `Acappella` (the list carries only the misspelling
`acapella`), `Vocal`, `Refix`, `Dubplate`, `Intro`, `Nightcore`, `Sped Up`,
`12 Inch`, and every non English spelling: `Ao Vivo`, `Versión`, `Mezcla`,
`ライブ`, `Живая`. Meanwhile 15 of 42 ordinary ID3 `TIT3` values read AS a
version, including `Original Motion Picture Soundtrack`, which is the commonest
real TIT3 value there is, plus the labels `Club Sweat` and `Toolroom Club` and
the artists `Radio Slave` and `Cut Chemist`.

**The error costs are asymmetric and the whitelist has them backwards.** A
false negative leaves a bare title, so two versions collide onto one identity
and deleting one suppresses the other, losing a track the user did not delete.
A false positive writes a tombstone that matches no provider spelling and
simply fails to suppress. The safe default is to believe the version column,
not to whitelist it.

Deeper than the vocabulary: **every tombstone written from `RemixerName` is
unmatchable by the consulter, and the docstring already says so.** The column
holds a bare artist name, so `Strobe` + `Michael Woods` records
`strobe (michael woods)` while every provider spells it
`strobe (michael woods remix)`. `tombstone.py:170-174` states this defect
verbatim and closes it only for the branch where the title already carries the
bracket. Every remix the user deletes gets re-downloaded.

And five data safety findings that outrank all of the above, because this unit
trashes files: a hand moved file retires the removal permanently with nothing
trashed and no tombstone; `categorize` caches anchors and never asks
`changed()`, so a volume ejecting mid walk marks a whole removal history as
dealt with; the playlist membership read has no completeness assertion and is
the only thing protecting a track a playlist still points at; and the refusal
that stops `recover` overwriting a re-occupied original path is pinned by
nothing.

### U12, and a refinement to the technique

`_PROBE_REAP_SECONDS` drops from 1.0 to 0.001 with the suite green, run 12
times to rule out a flake. The verifier did not stop at the zero row. It built
a child whose SIGTERM handler takes measurable time and showed the
consequence: at a 50 ms unwind or longer, the millisecond budget SIGKILLs a
child the one second budget unwinds cleanly.

**Then it found why the mutation survives, and this is the generalizable
part.** Both fixture children exit via `os._exit()` inside the signal handler.
That is a zero millisecond unwind, so no fixture in the suite can express the
difference between a one second budget and a one millisecond one.

**When a constant survives mutation, the fault is often in the FIXTURE, not
the guard.** Pinning the constant without fixing the fixture produces a green
row that proves nothing. Add this to the method: for any zero death row on a
timing or sizing constant, ask first whether any fixture could distinguish the
two values at all.

U12 also caught round 3 reproducing a defect it had itself diagnosed one
function later. Its commit message diagnoses quiet degradation for
`except OSError` at `pool.py:461`, and then the malformed cgroup line guard 40
lines down does the same thing: reverting it turns a public function that
promises a number into a `ValueError`, which `plan_pool` swallows into
"this machine's memory is unreadable" and one worker.

### U16, and the third pattern in its purest form

Round 4 was told to fix a machine dependent `match_id`, and it did. `match_id`
is now genuinely a function of the list line alone. **But the identity that
`review export` and `review import` actually move is a different one, and that
one is still library dependent.**

`match.py:1508` derives the review item identity from
`wanted.question(about_the_key=self.asks_about_key)`, and `asks_about_key` is
set at `:1772` by whichever branch the LIBRARY chose. Driven end to end: one
list line gives item `rv_5b77...` on a machine holding the track at `03A` and
`rv_0efa...` on a machine holding only `Extended`, while `match_id` is
identical on both. A answers and exports, B imports with no conflict, and B's
next `adjudicate` re-asks the same question under the other identity. The
answer is imported and ignored. Reverting the line kills ONE test.

The fix was correct. It landed on the wrong object. The docstring and R-24
both assert a property the code now has for `match_id` and does not have for
the thing that travels.

Second U16 finding, and the reason it matters more than it looks: finding (a)
was closed on two readers and left open on the third. A Tidal row carrying its
version in its own field discards the listing's credit BEFORE the new
precondition can check it, so the check is vacuously true. Result is
`SUPPRESSED / TOMBSTONED`, exit zero, **acquisition silently skipping a track
nobody deleted.** Every test pinning it drives `read_text_lines` only. A fix
verified on one reader out of three is how this defect came back after being
fixed once already.

### A merge instruction that was wrong, now corrected

The 08-03 snapshot said U24 and U16 collapse into `match.TOMBSTONE_KIND` and
`match.version_identity`. Neither symbol exists. **The real names are
`cratekit.core.tombstone.KIND_VERSION` and
`cratekit.core.tombstone.version_identity`**, and `tests/_pending.py:109`
registers the module obligation. `KIND_VERSION`, not `TOMBSTONE_KIND`. A merge
instruction naming a symbol that does not exist gets followed literally, so
this one is worth more than its size.

### U38, and a fourth pattern: a fix justified by a fixture, not the tree

Round 4's entire justification was that round 3's wide key set over fired,
"27 of 28 ordinary constructs reported". **That number came from a hand
written fixture. It was never measured against the repository.**

Measured against all 60 plus real package modules under round 3's rule:
**ZERO offenders** outside the two declared table owners. On the fixture that
actually ships it is 18 of 18 under the wide rule, and the 28 construct set is
not in the repository at all.

So round 4 traded real coverage away to fix an over fire that does not occur
here. The coverage traded is not small: across 15 realistic second
reservation table shapes keyed on registry only slugs, 15 of 15 were caught
under round 3's rule and **0 of 15 under the tiers.**

Two compounding findings. **R-19 is factually wrong about the rule it
documents**, claiming tier 2 accepts a conversion wrapped round an `ExitCode`
when it does not, and the fixture round 4 itself added to drive that case is
only ever run with a tier 1 key. And **the alternative round 4 rejected was
rejected on a property the shipped scheme also lacks**: it declined to narrow
to the 18 live integers because that would "blind the guard to a new module
inventing 33", and `{"tree-registry-unusable": 33}` is not reported by what
shipped.

Worst of the twelve, and the smallest: **R-15's headline fix, the whole point
of the round, ships with zero tests holding it.** Reverting the repaired
import walk to the exact pre fix expression kills 0. No fixture anywhere in
`tests/` contains `from .review import` or `from . import review`. The defect
is repaired in the file whose entire thesis is that a guard answering "no"
instead of "wrong" is the defect.

**Name the fourth pattern: a fix justified by a measurement taken on a
fixture rather than on the real system.** It is more dangerous than the other
three because it produces a confident number, a defensible argument, and a
green suite, and the number describes something that was written to make the
argument. Ask of every justifying measurement: was this taken on the tree, or
on something authored alongside the fix?

### A process failure that is mine, not the agents'

U38's verifier could not compare round 4's mutation table row by row, because
**the row descriptions existed nowhere.** Not in the worktree, not in the
repo, not in any file. Only the claimed counts survived, in a chat message.

A mutation table is the primary evidence a round produces, and this wave has
been generating it into a medium that does not persist. Every table so far is
recoverable only from a session transcript. **Standing correction: a fix round
writes its table into the repository, with full row descriptions and not only
counts.** A table that cannot be checked by the next person is a claim, not a
result.

### A technique addition: argue a zero row with a COMPOSITE, not a paragraph

U12's round 4 solved a problem this wave kept hitting. Some assertions cannot
die alone, and saying so has until now been indistinguishable from excusing a
hole.

**An assertion that TIGHTENS a bound cannot die alone, because the shipped
constant satisfies the loose bound too.** Reverting it changes nothing while
the constant is still correct. Round 4's answer is to pair it with a mutation
of the constant it guards and report both:

    M64 reap margin assertion removed   alone 0   with the budget at 0.5:  0
    M64                                 alone 0   with the budget at 0.25: 1
    M65 fixture release 0.4 to 0.0      alone 0   with the budget at 0.25: 0
    M65                                 alone 0   with the budget at 0.001:0

The last two rows are the point: they REPRODUCE the original blind spot on
demand, proving the fixture fix was necessary rather than asserting it.

**Standing rule: a zero death row is acceptable only when a composite shows
what it does hold.** A prose argument is not evidence. This replaces the
weaker convention of declaring a row redundant and moving on.

U12 round 4 also found a THIRD instance of its own quiet degradation shape.
`_cgroup_text` claimed every failure arrives as `OSError`. Two do not:
non-UTF-8 bytes raise `UnicodeDecodeError`, and a path field with an embedded
null byte raises a bare `ValueError` out of the open. Both escaped and landed
as `MEMORY_UNREADABLE`, so a parse bug in our own reader reported as the
machine's memory being unreadable.

### U27, where the hole has now moved three times

Sites four, five and six of R-18 item 3. **Site by site guarding has failed
three consecutive rounds**, so round 6 is directed to fix the CLASSIFICATION
instead: an `OSError` whose errno is `EACCES` or `EPERM`, raised anywhere
under setup or doctor, is a permission the user can grant, decided once at the
dispatcher so an unguarded site still comes out right.

The worst is not a bad message, it is a dead verb. **`crate setup` cannot
complete at all** on a machine where rekordbox's own settings name a database
this interpreter cannot stat, which is a library on an external SSD or under
`~/Documents` without Full Disk Access. The path is not one the user supplied,
so there is no way around it, and the wizard dies before asking anything.

Instance seven of absence read as absence: a mount slot this account cannot
stat reads as a slot with nothing mounted in it, so with the drive attached
and mounted the tool tells the user to attach the drive.

And the reason it keeps coming back: **the suite PINS the wrong behaviour.**
Mutating the remedy to `GRANT_PATH_ACCESS` kills two tests. The defect is
enshrined, and it got that way because those tests raise a synthetic
`PermissionError` instead of hitting a real permission. That is the fourth
pattern, found one round after it was named.

### The sharpest form of the fourth pattern: an explanation written instead of measured

U34's round 4 declared a counting discrepancy against the previous verifier and
explained it: "this table counts failing tests from the suite summary while the
earlier verifier counted parametrized cases individually."

**That mechanism does not exist.** Two independent refutations: pytest's
summary already counts parametrized cases individually, so the two descriptions
are the same number; and measured against round 3's own file at `HEAD~1`, the
six rows give exactly the counts round 4 reported.

The conclusion was correct. Every row did still bite. The REASON was invented.

This is the fourth pattern in its most dangerous form, because it arrives
attached to a true conclusion and therefore survives review. A fixture based
justification at least describes something that was run. A written explanation
describes nothing at all, and the only tell is that it is plausible.

**Standing rule: for every number in a report, either it was measured or the
report says it was not.** No mechanism may be offered for a discrepancy without
a measurement showing that mechanism operating.

### U34's other lesson: a guard that fires on ordinary code

Round 3 was found firing on correct code. Round 4 replaced the receiver's
RESOLUTION and left the binding table's SCOPE untouched, so the false positive
came back respelled. Ten ordinary shapes fail today against the real
`aging.py`, including `for config in rows:`, a comprehension target, a `with`
target, an `except` target, and, worst, `self.config = config` where `config`
is the constructor's own parameter, which binds `self.config` to the module for
the entire file. Constructor injection is the commonest spelling there is.

The tree measures 0 offenders across the governed modules. **That zero is not
safety.** It holds only because no governed module has yet been written in any
of the ten shapes.

A line worth keeping from that report, on the reflective writer hole: **round 2
lost the four token wrapper, round 3 lost it one token longer, round 4 loses it
one LINE longer.** Three rounds, each closing the previous spelling and none
closing the shape.

### What these findings have in common

All three are the wave's two named patterns, again. U23 and U34 are IDENTITY
THAT IS NOT UNIQUE. U23's lock hang, and U32's dangling symlink reading as a
free name, are ABSENCE READ AS EVIDENCE OF ABSENCE. Neither pattern has been
exhausted by five rounds of fixing.

A third pattern is now firm enough to name: **a fix round that lands on the
performing path instead of the checking path.** U32 put its refusal after the
destructive step. U23 put its fix at byte comparison when the defect was at
identity. Both fixes were correct in isolation and both left the hole open.

## Open decisions for Phillip

1. ~~**Board drift on #52 and #53.**~~ **RESOLVED 2026-08-04, no decision
   needed.** The U36 merge added a third drift item, #36 still showing In
   Progress after its issue had closed, which made this routine rather than
   optional: a merged unit reading as unmerged is the state the board exists to
   prevent. Ran `board.py sync`. It corrected five items, the #36 status plus
   adding #52 and #53 to the board as Ready. **`board.py audit` now exits 0 and
   reports "The board matches the repository."** Note for the next session:
   audit on `main` was exit 1 the whole time, never exit 2. The exit 2
   contradiction over `cratekit.write.rebuild` is real but lives only on the
   U32 branch, which re-adds a register key for a module U36 already shipped.
2. **The merge exit criterion.** The standing order is merge nothing until a
   branch verifies clean. Sixteen verifications, sixteen blocking. The severity
   has fallen sharply, from live data destroying defects to tests that cannot
   see what they claim, but it has not reached zero and each round legitimately
   finds something smaller. The alternative is merging on zero BLOCKING with
   the rest recorded as residuals, which is what U36 got and how R-1 through
   R-17 already exist.
3. **Whether the parked conformance branch comes into scope** once the eight
   units clear. Its metadata defect is live on main today.
