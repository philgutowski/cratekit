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

`main` carries U1 to U8, U10, U11, U13, U14, U15, U17, U18, U19, U21, U24, U31,
U34 and U35, plus the W1 through W6 hardening, the A4 whitelist addition, and
U9's verdicts. Pushed to the private remote. Measured after the U24 merge:
**4131 passed, 15 skipped** out of 4146 collected, ruff clean, `scan_repo`
clean. Quote the PASS count here, never the collected total: they differ by the
skips, and an earlier line in this file and one commit trailer both quoted the
collected number as if it were passes.

`main` has since moved to `c114afa` with **3278 passed, 17 skipped**. A trial
merge of that into this branch was run on 2026-08-03 for evidence and then
deleted. Five files conflicted, `docs/HANDOFF.md`,
`docs/residual-findings.md`, `src/cratekit/cli/registry.py`,
`src/cratekit/core/cause.py` and `tests/test_cli_contract.py`, and every one was
two sides appending to the same region rather than two sides changing one thing.

**ONE OF THOSE APPENDS IS A COLLISION AND NOT A CONFLICT, and the real merge has
to settle it by hand.** `main` carries its own `R-16` and `R-17` in
`docs/residual-findings.md`, from U36 and U32, and this branch carries `R-16`,
`R-17`, `R-18`, `R-19` and `R-20`. Keeping both sides, which is what every one of
these five conflicts wants, leaves the merged file with TWO `R-16` headings and
TWO `R-17` headings naming four different findings. Git cannot see that, because
neither side edited the other's line. Whoever merges renumbers this branch's
entries to follow `main`'s highest, and fixes the references to them in
`docs/HANDOFF.md`, `src/cratekit/deletion/candidates.py` and
`tests/test_deletion.py`, which name `R-19` and `R-20` in prose.

**THE MERGED NUMBERS RECORDED HERE AFTER ROUND 3 WERE MEASURED ON THE ROUND 2
TIP, and are corrected rather than adjusted.** They read 3395 passed, 16 skipped
out of 3411 collected, which is exactly nineteen short of the merge of the round
3 tip, nineteen being the number of assertions round 3 added. The merge had been
run before round 3 was committed, so it described a tree that no longer existed
by the time the line was written. The conflict set of five files and the ruff and
`scan_repo` results were and are correct.

MERGED BATTERY, measured on the merge of `c114afa` into the ROUND 4 tip
`49f3c13`, taken after the conflicts above were resolved by keeping both sides:
**3440 passed, 16 skipped** out of 3456 collected, ruff clean, `scan_repo` clean.
The branch was created, measured, reset and deleted, and `main` was not touched.
Re-measure after any further round, since every added assertion moves it, and
measure it on a COMMITTED tip: a merge run before its own round is committed
measures the round before it, which is exactly what went wrong above.

## What U30 changed

**The one unit that modifies the OTHER repository.** All of U30's production
code lives in DJ_tools (branch `unit/u30-overlap-ratchet`, merged to its main),
because the unit's whole point is that R31's ratchet is enforced on both
writers: the old system's lock now resolves to the same library-scoped file
this system flocks, and its XML emission refuses any tree the registry has
flipped. This repository's half is one pinning test and this record.

**What DJ_tools now pins, by path, without importing this package:**

- `.cratekit` as the library state dirname, with `local` and `coupled` beneath
  it. `tests/test_config.py` pins those three names here, because renaming any
  of them before DJ_tools retires would send its overlap guard at paths this
  system no longer uses and the ratchet would disarm silently.
- `local/write.lock`, flocked EX|NB, opened `a+`, never unlinked, dirs 0700 and
  file 0600. Both writers contend on this exact file now, which is the real
  half of AE19.
- `local/session.lock` and its holder JSON shape. A DJ_tools refusal names the
  Cratekit holder from it, rendered the way `Holder.describe` renders it.
- `coupled/tree_registry.json` at schema version 2, with this reader's exact
  refusal semantics ported: absent is the empty registry and default-safe,
  anything untrustworthy refuses, a record with no mode never defaults to xml.
  Bumping the registry schema before DJ_tools retires makes the old system
  REFUSE its governed emissions, by design; that is the safe failure direction,
  not a bug.

DJ_tools' guard maps display names to the stable tree ids `genre_energy`,
`inbox` and `record_labels` in code. A new governed tree cut over in the future
needs that mapping extended in DJ_tools' `DJ_common/tree_guard.py`, or the old
system will not know to refuse it. Its intake guard also reads
`CRATEKIT_DOWNLOAD_STAGING` and `CRATEKIT_CONFIG_DIR` from its own environment
to refuse overlapping intake roots, so an override set only in this system's
shell is invisible to it; the config file is the value both sides can see.

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

`delete.review` genuinely cannot land yet, **and the reason written here on
2026-08-02 is stale.** That note said the wall was R34 and conformance 3: an
explicit gate is answerable only by a separate recorded act, conformance 3 drove
the inline answer and then required exit `OK`, so no explicitly gated verb could
land. It also asserted that a missing database was NOT the problem. Main's
`3269ab1` rewrote conformance 3, and the gate wall is **down**.

Driven rather than argued. On 2026-08-03 the verb was built on a throwaway merge
of `main` and driven through all four acts: it refuses at `delete.review.confirm`
and reports the run resumable; an inline `-d` answer on the same run is refused
and is **not** recorded, which is R34 honoured; `run decide` records it with its
actor; and the resumed invocation carries the answer forward and proceeds past
the gate. Everything R34 asks for works now.

It stops one step later, at exit **22**, `library-directory-missing`. Reading the
collection is what this verb IS, so it cannot exit `OK` on a machine with no
rekordbox database, and the conformance fixture is exactly such a machine. That
is **R-13's original database wall**, unchanged, which closes on a disposable
fixture on the `CRATEKIT_TEST_DB` convention and whose natural owner is U27. The
stale note replaced one wrong reason with another and denied the true one.

`cratekit.deletion.cli` is registered in `tests/_pending.py` against **U24**,
which is where it belongs; an earlier re-point to U27 is reverted, because U27
ships no deletion domain and closes in this same wave, so the re-point moved a
contradiction rather than resolving one. **That entry is what makes a
`Closes #24` trailer return `board.py audit` exit 2 permanently**, and it is a
decision about who owns the database fixture rather than a repair. See R-13 and
R-16 in `docs/residual-findings.md`.

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

**ROUND THREE CLOSED A DATA INTEGRITY DEFECT AND AN IDENTITY THAT NAMED TWO
VERSIONS AT ONCE.** Both had been green through two fix rounds.

A file could reach the Trash with **no tombstone** and stay there forever,
silently. The pre-flight proves the suppression store READABLE, which is not
writable, so a full disk or a volume gone read only reaches the one window where
failing has already destroyed something: the move succeeded and the record did
not. The exception left the gates block with the watermark un-advanced, which
looks safe and is not, because the next run finds the file absent, answers `GONE`,
`GONE` is the one member of `HANDLED`, and the watermark passes over the row. R36
says every completed deletion writes a tombstone and that state made the sentence
false with no trace anywhere. The move is UNDONE now: `run._record_or_put_it_back`
renames the file back, the store's own refusal propagates carrying its remedy, and
re-running completes the deletion. When the undo fails too the refusal is replaced
rather than chained quietly and names both paths, because a store that will not
write is an errand and a file in the Trash with no way back is a fact about
somebody's music.

`version_identity` keyed on artist and title alone while the reader mapped only
`ArtistName` and `Title`, so two remixes of one recording produced **one**
identity whenever rekordbox filed the mix name in its dedicated `RemixerName` or
`Subtitle` column. Deleting the remix reported the ORIGINAL suppressed and never
re-acquired it. The module docstring asserted "the title is what carries the
version", which the schema contradicts by having a Remixer column. The reader
takes the mix name from either column now and `tombstone.version_title` composes
it into the title, so the claim is true rather than assumed, and it keeps the
two-field identity the ISRC argument depends on. **Round 4 narrowed the safety
claim that came with it**, which read "composition can only split one identity
into two, never merge two into one": composing produces a title, and a title is a
string another row may already hold, so `("Everything", "I Do")` and
`("Everything (I Do)", "")` land on one identity. It is true when the second
field really is a mix name, and what keeps it one is the producer, below.

Four smaller ones, each an absence read as evidence. `apply`'s re-check took no
`declined` predicate, so the function whose docstring says it re-runs EVERY
assertion ran one fewer. The revoke read `review-item-unknown` as "the queue does
not hold it" when a wrong derivation produces the same reason, so the derivation
inputs are asserted positively first. `MAX_NAME_ATTEMPTS` could be raised to
`10**9` with the suite green. And a recorded location that is not an absolute path
was excused from the completeness proof on an argument that covers streamed
pseudo-locations only: a drive-letter path or a `file://` location is excused by
the same branch, which on Windows empties the reference set entirely and proves
every removed row unreferenced against nothing. `candidates._unnameable` refuses
those two spellings and NOTHING ELSE, which is round 4's correction: round 3
recognised them with `locations.looks_like_location`, which is `"://" in value`,
so `tidal://`, `spotify://`, `beatport://` and `https://` rows were refused too
and the whole destructive verb went off for any library holding one streamed row
spelled as a URL. Both directions are pinned now. See **R-18** for the half that
belongs to `core.locations` and **R-17** for a folding collision that is recorded
rather than fixed.

**ROUND FOUR FIXED A REGRESSION ROUND THREE INTRODUCED, WIDENED THE UNDO TO THE
INTERRUPTS THAT MISS IT, AND SETTLED WHAT AN IDENTITY IS.** Five blocking
findings and nine more, all driven end to end by an independent verifier.

The regression is the one above: narrowing which excused rows count against the
proof was right, and recognising them by `"://" in value` refused every streamed
row that carries a scheme. That is a destructive verb turning itself off
permanently with a step nobody can perform. Only `file://` names a file, so only
`file://` and a drive letter refuse, and the four other schemes are asserted
excused.

`run._record_or_put_it_back` caught `Exception`, and the failure most likely to
land in that window is not one. The store write takes a sibling lock, which is
the slowest part of the pass, so a Ctrl-C lands there: `KeyboardInterrupt` and
the `SystemExit` a SIGTERM handler raises are both `BaseException` and both
walked past the undo, leaving the file in the Trash with no tombstone and the
next run retiring the row through `GONE`. `trash.move_to_trash` had used
`except BaseException` for the identical window one file over since it shipped.
Both handlers take it now. **`Category.GONE`'s safety argument is corrected
rather than repeated**: no handler catches a SIGKILL or a power loss, so the
guarantee is "every failure this process can observe" and the rest is bounded by
the file being in the Trash rather than unlinked, and by what is lost being the
suppression rather than the music. Recorded as **R-20** with the write-ahead
intent that would actually close it.

**Three findings that were one question: what is an identity.**
`version_title`'s containment short circuit was a plain substring test, so a
version appearing anywhere in the title was dropped from the identity and `Live`
counted as carried by `Lively Up`. Two rows of one recording then shared one
identity and deleting either suppressed both, which is the over-suppression
direction and the exact defect round 3 claimed to close. A version is carried now
only when a BRACKETED group of the title names it at word boundaries, which keeps
`Strobe (Michael Woods Remix)` from composing a second time even though
`RemixerName` holds the bare artist name `Michael Woods`.

And `Subtitle` is not `RemixerName`. `RemixerName` is an association proxy into
`djmdArtist`, so rekordbox's schema says a non-empty value is a remixer, and it
is believed on sight. `Subtitle` is free text mapping to ID3 `TIT3` and holds a
label, a featured credit or a note as readily as a mix name, so believing it on
sight wrote an ordinary track's tombstone under `atlas (anjunadeep)` while the
consulter, which is handed a provider's `Atlas`, answered NOT SUPPRESSED. It is
believed now only when the value reads as a version against a closed vocabulary,
and both directions are pinned. That is also what makes the narrowed composition
claim true in practice: composition is safe because of what is fed to it, not
because of what it does.

Smaller: the `unnameable` tally and the payload's own spelling of the mix name
are pinned rather than merely present, the dead first half of the version guard
is live again under the bracketed test, and R-17's Turkish sentence is deleted
because `str.lower` and `str.casefold` behave identically for the dotless and
dotted i. The Greek final sigma reason is real and the re-keying reason is
decisive on its own, so R-17's decline stands. **R-19** records a square-bracketed
mix name never matching the parenthesised spelling a provider uses.

**ON "THE STALE SENTENCE IS CORRECTED IN ALL FIVE PLACES", written in round 3's
commit body: it is corrected in the four places that can be corrected.** Those
are this file, `src/cratekit/cli/registry.py`, `tests/_pending.py` and
`src/cratekit/deletion/__init__.py`, and each states the reason that is true. The
fifth is `c4f97fb`'s commit body, and a commit body cannot be amended once it is
in the history, so it carries the stale reason and always will. A claim that a
repository has been made uniformly true has to exclude the parts of it that are
immutable, and pointing at the superseding record is the whole of what can be
done about them.

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

## What U23 costs to merge, counted rather than estimated

Round 7 reported a "conflict surface" of 7. That figure is not reproducible, the
term is defined nowhere in this repository, and no grouping of this branch's
changes produces it. **Measured against `main` at merge base `4368171`: the branch
touches 20 files, of which 11 already exist on `main` and 9 are new.** The count
was 11 before round 7 and 11 after; round 7 itself touched 9 files, all of them
already in that set or new.

The 11 that exist on `main`, which is the whole of what a merge has to reconcile:
`docs/HANDOFF.md`, `docs/residual-findings.md`, `src/cratekit/cli/registry.py`,
`src/cratekit/core/cause.py`, `src/cratekit/core/config.py`,
`src/cratekit/core/tags.py`, `tests/_pending.py`, `tests/test_cli_contract.py`,
`tests/test_layering.py`, `tests/test_pending_units.py`,
`tests/test_review_queue.py`.

Reproduce it with:

    for f in $(git diff --name-only 4368171 HEAD); do
      git cat-file -e main:$f 2>/dev/null && echo "ON-MAIN $f" || echo "NEW $f"
    done

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
R-83 with the fix named.

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
record, refused on every retry. Written down as residual R-85 and pinned by a test,
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
whole-file hash on the refusing path, is recorded honestly as R-86 rather than
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

**That last claim was half true and round 6 corrects it.** Three of the refusals
were asserted by their LEADING CLAUSE only, so every word after it could be
reworded and no test moved: `_THE_STAMP_NEVER_LANDED`, `_THE_STAMP_COULD_NOT_BE_READ`
and `_NO_DIGEST_WAS_RECORDED`. Round 5's mutation table credited them one, two and
one death, which is what a WHOLESALE replacement of the constant measures rather
than a nearby rewording. Every message constant is now asserted in full.

**Net:** one acceptance where there were three, and it is the recorded digest
matching the file's bytes. Everything else refuses, names which of the four ways
it is, and names the `(path, field)` pair that overrides it.

**Round 6 found the guard was right and the IDENTITY was wrong, which is a layer
below everything above.** A record was keyed on a digest of the PATH, so two
recorded locations naming one file produced two identities and first-write-wins,
which this module's own docstring calls load bearing, never engaged. The second
record then stored the value adoption had just written as the "original". Three
spellings reach it and none of them is exotic: a hardlink, a case varying
spelling on a case insensitive volume (the APFS default), and a rename between
two runs. Driven end to end, the revert restored the real genre through one
record, refused the other because its own restore had changed the bytes, told the
user their file's bytes were not adoption's, and handed them a `force` key that
wrote `Adopted Bucket` on as the original. The user's genre was then in no file
and no record.

Identity is NOT a lowercased path: case insensitivity is a property of the volume
rather than of the string, and folding two real files into one record is the same
defect pointed the other way.

**AND IT IS NOT `(st_dev, st_ino)` EITHER, which round 6 shipped and round 7 took
out again.** That pair is not unique in either direction and both directions were
measured on real filesystems rather than argued. An inode number is REUSED once
the file holding it is deleted, reproduced on a real MS-DOS FAT image, which is
the format of every rekordbox export drive: adopting the new file found the dead
file's record, REFRESHED the record's path to the new file, stamped the new
file's digest into it, and the revert then wrote the dead file's original onto
the live file and reported the pass clean. The same pair also MOVES for a file
nobody touched, three ways: a FAT remount renumbered the inode, an `os.replace`
save on APFS moved it at the same path on the same volume, which is how every
tagger and this repository's own atomic writer save, and remounting two volumes
in the opposite order moved the device number.

So a record now carries THREE claims about which file it is about, and
`_record_for` requires them to converge: the volume and inode, the path, and a
digest of the bytes adoption left. A disagreement the BYTES can settle is
settled, which is what carries a rename, a remount and a legacy ledger through.
Every other disagreement REFUSES with `RecordCannotBeMatched`, per entry, with
the file untouched. **The recorded path is never rewritten to a different file's
path**, because that one line is what destroyed the evidence. A ledger written by
the old scheme is migrated on the next adoption rather than doubled, and the
ledgers already on disk are covered from the other end too, where two records
resolving to one file refuse as a group, computed over the WHOLE LEDGER rather
than over the records one pass selected, and are deliberately offered no `force`.

**And the guard blocked forever on a file whose bytes cannot be produced, holding
that lock.** Removing the eviction branch left `digest_of` unbounded, and
`revert_tags` holds the ledger's exclusive lock across its whole pass. Driven
with a FIFO at the recorded path: `exists()` True, `stat()` instant, `open()`
never returns, the revert still running at 6 seconds, and a concurrent
`write_tag_with_record` on a different and perfectly readable file waiting behind
it for its whole life. Three fixes, and the permissive choice for evicted files
is kept: the mode is asked before any descriptor is opened, the read has a
deadline that RAISES rather than folding into "unreadable" (`TimeoutError` is an
`OSError`, which is the trap), and the read that would otherwise be a provider
download happens BEFORE the lock is taken.

**What round 7 changed about that last one.** The pre-lock answer used to be
SPENT under the lock whenever `(st_dev, st_ino, st_size, st_mtime_ns)` had not
moved. Those are the four values this module's own docstring says are not
evidence about content, deciding whether evidence about content still applied.
Measured on a real FAT image, whose modification time granularity is one second:
an in-place rewrite of the same length inside one tick left all four identical
while the digest had changed, and the restore ran on the replaced bytes. So the
pre-lock pass now decides NOTHING. It reads to make a provider materialize the
file with no lock held, and the read that decides is taken again under the lock.
That is two reads per refused record and the cost is written down rather than
rounded off. The residual about a revert hashing every file it considers is
corrected rather than re-filed; the residual about inode recycling is CLOSED
rather than accepted; two new ones record what a stalled mount can still do to a
single `read` and what a digest-less record cannot survive.

Round 7's mutation table is `docs/mutation-rows-u23.md`, with every row's exact
substitution beside its count. Fold it into `docs/mutation-rows.md` at merge.



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

One piece of reasoning lives **in this repository**, because it is rekordbox
behaviour rather than that system's paths and it survived the portability guard
once its volume names were stripped:

- `docs/rekordbox-live-fire-2026-08-02.md`, seven findings from repairing 1,357
  collection rows on a real library in one attended session. Four bear on units
  here. Two became R-14 and R-15. The others are knowledge rather than work:
  where analysis files actually live, that rekordbox marks missing files lazily
  so a marker count measures what the application has checked rather than what is
  broken, exactly which columns a relocate writes, and which menu item sits one
  row below `Relocate` and destroys the row.

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

U11 cleared its own entry, which is the countdown firing as designed. The growth
is the mechanism working rather than debt piling up: U11 and U19 between them
added five, each one an obligation that used to live in a docstring. U34 then
cleared its own and added one, because clearing the entry is the required act of
landing and the four verbs it left behind had to land somewhere that a mechanism
reads. See the residual titled "Four report verbs were owed by a unit that was
about to close, and named a module nobody could build", cited by title because
`main` carries a different finding under that number.

**This table is a COPY of `tests/_pending.py`, and the register is the
authority.** It was reconciled against the register on 2026-08-14 and had
drifted: it carried eleven targets across ten rows against the register's ten
keys, because one row named two. Three targets on it were dead, discharged when
their units landed, and are removed here: `cratekit.acquire.match_cli` (U16),
`cratekit.core.restore` (U32) and `cratekit.cli.exit_codes` (U38). Two live keys
were missing entirely and are added: `cratekit.cli.rebuild` (U20) and
`cratekit.session.restore_cli` (U27). One row per key, ten rows, in register
order. Regenerate it from `PENDING` rather than editing it by hand.

**Discharging one of these is three edits in one commit**, and the two files
below say which: the entry, the mirrored key in `EXPECTED_PENDING`, and the
`@requires` decorator on every guard the key gated. See
`docs/solutions/workflow-issues/countdown-entry-discharge-drops-a-whole-test-file.md`.

U23 cleared its own `cratekit.adopt` entry and added `cratekit.adopt.apply_cli`
in its place, which is the same mechanism at a finer grain: the engine landed,
so the engine's countdown expired, and the CLI obligation it left behind now has
a target of its own instead of being owned by a `planned_in` marker on a closing
issue. That last shape is R-13's failure and is live three times over already.

| Unit | Target | Owes |
|---|---|---|
| U37 | `cratekit.intake.collection_xml` | the COLLECTION TRACK emitter that must never emit a `<TEMPO>` element, plus two obligations U19 parked here because U37 owns the pipeline: record each new track's routing intent at the moment the placement is decided, and close a run that deferred a placement through `routing_pass.close_run` rather than `core.session.close_session` |
| U37 | `cratekit.intake` | a path repair proposal offered into the queue U11 declared for it, never applied, and never read back out of a file somebody edited |
| U24 | `cratekit.deletion.cli` | the deletion CLI shell. The re-point to U27 is REVERTED, so this row agrees with `tests/_pending.py`. The wall is R-13's database fixture, not the explicit gate, which main's conformance 3 rewrite took down. It is why a trailer naming this unit's issue returns `board.py audit` exit 2, and its issue stays open by design |
| U27 | `cratekit.cli.doctor` | a database acknowledged outside the library root is reported on every run, so a snapshot that is a copy rather than an atomic commit stays visible long after somebody accepted it |
| U28 | `path:skills` | the shipped operator skills the skills lint runs over |
| U20 | `cratekit.write.routing_cli` | the four `route.*` verbs, each closing through `routing_pass.close_run` rather than the exported `close_session`, and a re-run after a destination rename that CONVERGES by reading U36's `core.convergence.DestinationNode` map rather than building a second one. See R-13: U20 is an inference, not a decision |
| U20 | `cratekit.cli.rebuild` | the rebuild verb, whose operator disposition is an explicit logged act by a named person and never a flag that clears every tree, and which clears a tree's flag only through `write.rebuild.rebuild_tree` handed the convergence check's own difference list |
| U27 | `cratekit.session.restore_cli` | the two restore verbs U32 could not land, and one session held across the whole restore through `core.restore.recovery_session`, passed in as `plan_restore`'s and `run_restore`'s gates, because the default shape takes the library lock twice |
| U27 | `cratekit.cli.reports` | the four report verbs, and the two report engines two of them still have none of. See the residual titled "Four report verbs were owed by a unit that was about to close, and named a module nobody could build": U27 is a judgement, not a decision |
| U27 | `cratekit.adopt.apply_cli` | the apply shell, and the destructive session and library lock `apply_plan` says it does not take. See R-81 for what the wall in front of it actually is, which is not what R-13 says |

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

**A rule's SCOPE is a claim, and a claim stated in prose is a claim nobody drove.**
U34's binding table exempts a veto written inside a branch, because a run that
skipped the branch never cast it. That is right for a NAME and was written as if
it were right for the whole table. It is wrong for an ATTRIBUTE: `class Base`
binds nothing by itself, so a subclass overriding `self.mod` inside an `if`
without calling `super().__init__()` has no path on which the base's binding
exists. Six ordinary branch spellings were reported as writes to the configuration
file for six rounds, with a docstring in two places saying the rule was applied to
the veto only. Drive the scope of a rule the same way you drive its result, on
both halves of whatever the rule ranges over.

**A guard whose coverage is a typed list is a guard that stops covering.** U34's
citation guard named nine files while the branch changed seventeen, and deleting a
report module from the list left the whole suite green. Two of the eight it never
read carry residual citations another unit wrote. Derive the coverage from
something that moves with the branch, and keep a named floor so a silent narrowing
of the derivation has something to get past.

**Do not exempt a guard's own file from that guard.** The same unit skipped the
suite for the "no stray delimiter" check on the grounds that the suite DEFINES the
delimiters. The definitions are assignments and are not delimiter lines, while the
reader honours a delimiter found there exactly as it does anywhere else. An
unclosed marker plus a citation went green in the one file the pair was told not
to look at.

**A classifier with two answers reports the state it could not read as whichever
one it defaults to.** U34's export reader split the playlist tree with "a
playlist, or else a folder". Driven on its own fixture with the `Type` attributes
made unreadable, seven playlists became folders, the intake report rendered a
clean queue over a library it could not read, and the duplicate audit reported a
pair with every placement gone. THE MISREAD NODES SATISFIED THE GUARD WRITTEN TO
CATCH THEIR LOSS, because that guard asks whether the intake folder is present and
the misread nodes are what filled the folder tuple. Give the question its third
answer, decide it once and positively where the document becomes a value, and
refuse there; a second check inside each report is one more site to keep in step
with the first.

**A floor that names files covers the files it names and nothing else.** The same
unit's coverage list was derived from git and floored by nine typed names, so a
narrowing of the derivation was refused on nine files and silent on the other
eight, one of which was the file the same commit created. Check the derivation
against a SECOND derivation composed of different commands, and keep the typed
names only for the failure the two share, which here is one merge base.

**A guard that pins a range has to pin the edge that moves.** The assertion
holding that unit's residual ban list checked that the document still defined 16
and 25 while the range ran to 26, so the top could be narrowed by one with the
suite green. Read the endpoints from the thing the constant describes, in both
directions, rather than writing two numbers next to it.
