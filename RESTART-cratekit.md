# Restart: Cratekit

Verified state only. How to work is `docs/METHOD.md`. Why the rules are what
they are is `docs/history/`. **No hash is written here on purpose**, since this
file is part of the commit it would be naming.

**Last merged: U69, issue #114, `relay/114`, 2026-09-18.**
`crate intake missing --job JOB` writes the list document `acquire download`
reads, from a finished intake job, the first verb to call `listdoc.write`. It
is `src/cratekit/intake/missing_cli.py`, registry entry `intake.missing`,
`diagnostic/1`, no write surface, not destructive, no gate. It reads the
job's committed reports with the frozen config and lists only `missing` rows,
so owned, offered and suppressed are counted and left out. The list goes to
`<download_staging>/lists/intake-JOB.list.json` with its manifest, provenance
`playlist` and the job's source, or under `--out`. It refuses, as
`intake-list-unusable`, a job that is not succeeded, a job with no items,
reports that do not cover the items one for one by identifier, a report with
an unreadable state, an `--out` that is a file, and a job whose missing rows
none carry a provider id. A job of another verb is `job-unknown`. A mixed job
with some unlisted rows writes the rest and shows a FAIL check. The human
output names the path and the literal next command, and it is driven through
`cli.run` in the default mode. The written list is queued and downloaded by
the real download verb against `FakeAdapter`. R-400 and R-423 narrowed,
neither closed. **R-431 filed and on the board.** A deleted track whose
tombstone the consult cannot reach, R-69's `UNRECONCILED` shape, is now
listed for download. It is pinned by a test that fails when it closes. Mutation tables
`docs/mutation/u69.md` and `u69-b.md`, 19 of 20 killing. The zero is inert,
because the job queue is installation scoped, and is read in
`docs/mutation/u69-notes.md`. `tests/test_reserved_causes.py` re-pinned to 95
literal holders, measured as a set difference. **Main's highest residual number
is R-431.** Owed to an attended sitting: one real `intake playlist`, `intake
missing`, `acquire download` on a small playlist.

**The session before: U70, issue #115, `relay/115`, 2026-09-18.**
`crate intake playlist favorites` answers "is every heart in my library". The
reserved reference `favorites` is checked in `intake.cli._playlist_rows` before
`playlist_for` could see it, and lists the account's hearts through a sixth
`Catalogue` member, `favourite_tracks`, which `TidalCatalogue` answers through
`listing.favorite_tracks` and refuses when the client exposes no favourites.
The rows go through the same reader, freeze and worker a playlist uses, so each
heart reports owned, offered or missing by the match engine's one rule; a heart
held in another version is offered, not owned. The job is an `intake.playlist`
job whose source is the canonical `favorites`, so the resume argv is unchanged,
with `source_id` favorites. The listing crosses
`label_cli.favourite_tracks_or_refuse`, the playlist boundary's twin, so
`ListingTruncated` refuses whole as `label-playlist-unreadable` and an adapter's
own refusal passes through. No placeholder playlist, no account write, no
cursor: a re-run is idempotent through ownership. `tests/label_fakes.py`
declares six methods and `FakeCatalogue(hearts=...)` answers the sixth; a test
holds the fake's set equal to the protocol's. `intake missing` landed in the
unit after, U69, which drove the hearts through to a download on fakes;
R-423 is narrowed, not closed. R-429 and R-430 filed, neither meeting the board
bar. Mutation table `docs/mutation/u70.md`, 14 of 14 killing, null control 0 of
7751. **Main's highest residual number is R-430.** Owed to an attended sitting:
one live run of `crate intake playlist favorites`, with the heart count
compared against the account's 197.

**The session before: U68, issue #113, `relay/113`, 2026-09-18.**
The product has a writer for the list document `acquire download` reads, which
closes R-400's engine half. `src/cratekit/acquire/listdoc.py` is ONE shared
emitter, not a document per source, and it is pure. `rows_of` takes `Wanted`
tracks or `frozen_tracks` items. `document` builds `{"list": 1, "origin":
"tidal", "tracks": [...]}`, reading every listed row back through
`match.read_row` first, so a row the reader would refuse is refused here by
position as `ListDocRefused` rather than costing the whole list. `write` puts
`<name>.list.json` and a `<name>.manifest.json` provenance sidecar into a
directory through `config.atomic_write_bytes`. Every file check runs before
either write: an absent file is written, an identical one left alone, and a
different one refuses. No listable row writes nothing and returns `None` paths.
First id wins, compared stripped. A row with no provider id, or a `Wanted` from
another service, comes back `unlisted` and is never written. A `Wanted` is
written in the source's own spelling when that re-reads to the same version
token, otherwise as its raw title plus its declared version; writing the split
title instead lost bracketed parts and featured credits, which the unit's
`/code-review` drove and the unit fixed. **Nothing calls `write`
yet**, which is R-400's open verb half and the entrances' units. A frozen
mapping re-reads as the plain record, which is R-428, filed without an issue.
Mutation table `docs/mutation/u68.md`, 23 rows, 20 killing, null control 0 of
7733, the first real table the driver has run under parallel workers, and its
collected counts held at the baseline. Two zeros were equivalent comparisons,
since removed; the third is a maintainer zero, read in
`docs/mutation/u68-notes.md`. **Main's highest residual number is R-428.**
Nothing is owed to an attended sitting. Battery at the branch head: ruff clean,
7,732 passed and 1 skipped, scan clean.

**The session before: U67, issue #112, `relay/112`, 2026-09-18.**
`name apply` never renames or retags a file the rekordbox collection references,
which closes R-407, the one open finding that could lose data library wide.
`write/naming_cli._recorded` reads every row's `FolderPath`, tombstones
included, through `rb_writer.open_db` with `require_closed` False, the
`metadata_cli` pattern, because `tests/test_layering.py` forbids `write` from
importing `adopt.collection`. `_referenced` keys each row as recorded and as
prefix mapped, NFC normalised and casefolded; `_is_referenced` asks a
candidate's absolute and resolved spellings. `_plan_for` marks each item
`"action": "rename"` or `"referenced"`, both in the digest, `totals.count`
stays the rename count and `totals.referenced` is new. `name_apply` reads the
collection AGAIN after the gate and re-checks each item before the rename. Any
failed read refuses as the new slug `collection-unreadable`, exit 25, carrying
the inner cause and its remedy; there is no force flag. **The read is skipped
when nothing would be renamed**, because the conformance suite drives this
verb over a library with no database and the collection cannot change an
empty outcome. Every other test in `tests/test_naming_apply_cli.py` stubs
`_recorded` as a read, empty collection; the U67 tests use a disposable
database. **A library with cloud sync ON now refuses `name apply`**, since the
read open's canary refuses it; kept, recorded as R-425. The at-risk population
re-pin moved 156 to 157 causes and 411 to 412 literals. Mutation tables
`docs/mutation/u67.md` and `docs/mutation/u67-round-2.md`, 21 rows, all killed
after round two added a collision test for the existing target claim, which
had none. New residuals R-425 to R-427. **R-426 meets the board bar**, a row
recorded through a link is unprotected, and its issue is owed after this
merge. **Main's highest residual number is R-427.** Owed to an attended
sitting: one plan only run against the live library to read `referenced`.
Battery at the branch head: ruff clean, 7,698 passed and 1 skipped, scan clean.

**The session before: the battery speed chore and the Phase G plan, `chore/battery-speed`, 2026-09-18.**
Attended, not a board unit. Four things landed together.
**The suite is parallel.** `addopts` carries `-n auto` and the dev extra carries
`pytest-xdist`. Measured on 11 cores at 7,678 tests: 532 seconds serial, 86 at
eight workers, 61 to 67 at auto, green each time including the disk image tests.
A venv older than this merge needs `pip install -e '.[dev]'` once. `-n 0` runs
in process, for a debugger. `scripts/mutate.py` inherits `addopts`, so its
baselines are parallel too. Its reporting plugin now writes from the xdist
controller only and reads the collected count off
`pytest_xdist_node_collection_finished`, and the driver scrubs the inherited
`PYTEST_XDIST_WORKER` identity from its child. Three tests in
`tests/test_mutation_driver.py` drive it against a fixture with `-n 2`. **The
driver has NOT yet run a real table under parallel workers**, so the first unit
to run one should read its null control and collected counts with that in mind.
**A product defect came out of the slowest test.** `listing.fetch_with_retry`
retried a `credential-missing` refusal five times and slept 31 seconds before
re-raising it, per listing. A `CratekitError` whose cause says
`retryable=False` now passes through on the first attempt, and a paired test
holds that a retryable refusal still climbs the ladder. No mutation table was
run over this change, it is two lines behind two new tests.
**The ledger gained R-413 to R-424**, twelve entries from the reads that planned
Phase G: the landing gap R-413, the rating scale hazard R-414, a correction to
R-400's wording R-415, the uncalled export routing writers R-416, six smaller
parity gaps, and the two entries issues 110 and 111 said they were owed, R-423
and R-424.
**METHOD changed.** Native Relay is in the loop and has a section. The
serialized order list is gone, spent. A board bar says which residuals earn an
issue, and a session now files that issue itself. The battery section says the
full suite is the merge gate and not the edit loop.
**The board gained Phase G**, units U67 onward, plus a card for every residual
that met the bar, from `docs/ideation/2026-09-18-parity-to-feature-complete.md`.
The two analysis tests near 30 seconds each spin a real process pool and were
left alone. Battery at the merge: ruff clean, 7,678 passed and 1 skipped, scan
clean.

**Two sessions before: R-358 code half, issue #105, `relay/105`.**
`modules.outbound.service.RemoteAccount` declares a seventh member,
`rename_playlist(playlist_id, name)`, and `TidalAccount` implements it over the
playlist object `add_to_playlist` already edits. A retitle is not a removal, so
the add-only scans still pass. Three refusals: a playlist the session does not
own comes back without an editor, the client answering `False` is a refused
write rather than a raise, and a blank title is `internal-error` at source
scope, spelled here rather than through `provider_failure`, because the client
reads a falsy title as keep the current one and answers True. The retry is kept,
unlike a create's, since a retitle asks for one fixed title.
`sync.playlists.pending_marks` and `mark_swept` are the application.
**The mark set is the WHOLE cursor, `Sweep.recorded`, not `recorded_now`**, and
the recheck is a second fresh listing, not the plan's own read. Both were review
findings; the first is the learning below. `mark_swept` takes an optional
`applied` list appended to as each rename lands, on `queue`'s pattern.
**Production is deliberately unwired.** No sweep writes an importable file, so
nothing calls `mark_swept`, `sync.cli` still reports `"mark": "unbound"`, and a
guard over `sync/cli.py` holds that until the live half is done. The report
block gained a `marked` list, and `"mark"` now separates a step that never ran
from one that ran and marked nothing. The at-risk population re-pin moved 93 to
94: `tidal_account.py` names a cause literal for the first time. Mutation tables
`docs/mutation/r358.md` and `docs/mutation/r358-round-2.md`, 20 rows then 4,
ending 18 of 20 killing, null control 0 of 7672 and 0 of 7674, no collect drift,
every restore verified against `git show HEAD`. The two surviving zeros mutate
test code and are recorded as such. The live mark stays attended and is
Phillip's. New residuals R-397 and R-398. The learning is
`docs/solutions/integration-issues/a-set-shaped-cursor-that-commits-before-a-side-effect-makes-the-next-increment-will-see-it-again-false.md`.
**Main's highest residual number is R-412**, not R-398. A docs merge landed after
this unit: the parity audit against DJ_tools, fourteen findings, R-399 through
R-412. They were numbered 397 through 410 on their branch and each moved up by
two at the merge, because this unit already held 397 and 398. R-400 is their
common cause, the list document `acquire download` reads and nothing produces.

**Three sessions before: R-368, issue #101, `relay/101`.**
`crate restore run` takes `--target DIRECTORY`, a database restore into a
directory that is not the live library, which is how a restore is rehearsed.
Valid only with `--from-backup`. It rolls no session back: a named session
refuses, `--discard` refuses, and the default that means the newest spendable
capture is suppressed. Omitting the flag is the live restore unchanged. Two
destination refusals share `restore-target-is-live-root`, the target being the
library root or holding it or sitting inside it, and the database landing on
the live one, which is the acknowledged outside-root layout that containment
cannot see. The two invocation refusals share `restore-target-invalid`. Both
slugs live in `core.cause.REASONS` and not in the reservation table, which
reserves what a module's refusal enum raises. A target that is not a directory
still raises `restore-target-absent` from `plan_restore`. The target and
`dry_run` are both digested into the offer, the second being a hole this
branch's review found one flag over. The branch's review also found the
guard comparing resolved paths as strings, which accepted a case folded
spelling of the live library on the filesystems this product runs on; both
checks ask `samefile` now. Mutation tables `docs/mutation/r368.md` and
`docs/mutation/r368-round-2.md`, 16 rows then 5, ending 21 of 21 killing, null
control 0 of 7649 and 0 of 7651, no collect drift, every restore verified
against `git show HEAD`. R-368 is closed against its RESTATED close and is not
fully closed: a rehearsal still takes the live library lock and still needs
rekordbox gone, which is R-396. The learning is
`docs/solutions/integration-issues/a-resolved-path-compared-with-equals-is-not-a-same-directory-test.md`.

**Two sessions before, 2026-09-18, R-352, issue #94, `unit/issue94-the-adapter-s-roster-is-narrower-than-th`.**
After own page and seeds, `TidalCatalogue.artist_for` searches the label
name and numbered compilations `001` through `079`, keeps copyright matches
via Cratekit `labels_from_copyright` and `labels_match`, and walks credited
artists through `session.artist` and `listing.artist_releases`. Discovery
runs when the roster is already non empty. An unresolved seed still refuses
first. A rate limited album query skips that query and keeps a resolved own
page. `AuthenticationError` on search still refuses. Catalogue members are
unchanged. The V/A shortfall is R-392. Mutation table
`docs/mutation/r352.md`, 17 of 17 killing, null control 0 of 7633, no
collect drift, every restore verified against `git show HEAD`. R-352 is
closed in place. The learning is
`docs/solutions/workflow-issues/a-search-fake-that-returns-every-album-cannot-catch-numbered-results-being-ignored.md`.
Main's highest residual number is R-394.

**The session before, 2026-09-18, R-351, issue #93, `unit/issue93-a-seed-artist-cannot-be-pinned-by-identi`.**
A seed of the form `id:<digits>` is looked up via `session.artist` with no
search. A name seed stays exact fold and still refuses when two provider
artists carry that name. An identifier seed plus a colliding same name
artist succeeds. A missing identifier refuses the label. A provider outage,
and a KeyError or IndexError, is not read as absence. `ObjectNotFound` is
the live client's missing shape. Bare `LookupError` is the fake's.
Registry `add` stores `id:` seeds. Catalogue members are unchanged.
Discovery landed as issue 94. Mutation
table `docs/mutation/r351.md`, 13 of 13 killing, null control 0 of 7619, no
collect drift, every restore verified against `git show HEAD`. R-351 is
closed in place. The learning is
`docs/solutions/workflow-issues/a-lookuperror-stand-in-cannot-catch-the-clients-object-not-found.md`.
Main's highest residual number is R-391.

**The session before, 2026-09-18, R-380, issue #92, `unit/issue92-a-job-whose-failures-are-permanent-repor`.**
A job whose every item failure is non retryable reports itself non retryable
and does not offer resume-job. When those failures share a reason, that
reason is the job's reason. A mixed job that still has a retryable failure
stays retryable and names both counts. `no-evidence` stays the all failed
slug; its retryable flag follows the items. `jobs.retry` is unchanged, DONE
items stay done. R-266's remaining engine half closed with this. Mutation
table `docs/mutation/r380.md`, 6 of 6 killing, null control 0 of 7608, no
collect drift, every restore verified against `git show HEAD`. R-380 is
closed in place. R-390 and R-391 filed. The learning is
`docs/solutions/workflow-issues/a-job-cause-that-ignores-item-retryable-tells-a-person-to-resume.md`.
Main's highest residual number is R-391.

**The session before, 2026-09-18, R-378, issue #91, `unit/issue91-the-harvest-prints-nothing-a-person-can-`.**
The default human rendering of a harvest names the harvested labels and the
unresolved count. `cli.render.render_review_set` is gated on `review_set/`
the way the diagnostic table is gated on `diagnostic/`. A harvest item's
`name` is its own indented line. Other review_set items keep their own
fields. Tests drive the real dispatcher in the default human mode, because
`tests.cli_drive.drive` always requests json and that is why every harvest
test stayed green over a blank answer. Mutation table
`docs/mutation/r378.md`, 6 of 6 killing, null control 0 of 7603, no collect
drift, every restore verified against `git show HEAD`. R-378 is closed in
place. The learning is
`docs/solutions/workflow-issues/a-json-only-driver-cannot-see-a-blank-human-renderer.md`.
Main's highest residual number is R-389.

**The session before, 2026-09-17, R-379, issue #90, `unit/issue90-every-offered-release-records-its-artist`.**
A label sweep offer records the artist's name, never a provider object's
repr. `_artist_of` reads a string as the name and an object's `name`
attribute otherwise. The suite's stand-ins passed a string, which is why
every green battery missed the address the live sweep wrote. A new test
drives an object whose `str` is a memory address. Mutation table
`docs/mutation/r379.md`, 4 of 4 killing, null control 0 of 7598, no collect
drift, every restore verified against `git show HEAD`. R-379's producer
half is closed. The 98 live rows still carry addresses, filed as R-389.
The learning is
`docs/solutions/workflow-issues/a-string-stand-in-cannot-catch-str-of-a-provider-object.md`.
Main's highest residual number is R-389.

**The session before, 2026-09-17, R-367, issue #87, `unit/issue87-a-restore-from-a-snapshot-taken-with-rek`.**
A restore from a snapshot holding only the database completes and names the
absent write ahead log, rather than failing on a copy the snapshot never
held. `plan_restore` lists the snapshot's database folder and copies only
the sidecars it holds. A listing that fails refuses before anything is
cleared. A failed database copy still refuses. Mutation table
`docs/mutation/r367.md`, 14 of 15 killing, G9 a user facing zero on the
wording with G2 as composite (1 kill), null control 0 of 7596, no collect
drift, every restore verified against `git show HEAD`. R-387 and R-388
filed. R-367 is closed in place. Main's highest residual number is R-388.

**The session before, 2026-09-17, U66, issue #89, `unit/u66-every-guarded-listing-method-has-a-plant`.**
Every member of `acquire.listing.GUARDED_METHODS` now has a planted pagination
loop case in `tests/test_adapter_listing.py`. The planted names live in the test
file and equal the production set, so adding a name arms its own case and
removing one fails that case rather than dropping it. U65's F2, removing
`get_ep_singles`, now kills 2 on the listing file. R-386 is closed in place.
Mutation table `docs/mutation/u66.md`, 6 of 6 killing, null control 0 of 7590,
no collect drift, every restore verified against `git show HEAD`. The learning
is `docs/solutions/workflow-issues/a-parametrize-over-the-live-set-drops-the-case-the-mutation-is-supposed-to-fail.md`:
a parametrize over the live set makes the mutation delete the case that would
have caught it.

**The session before, 2026-09-17, U65, issue #88, `unit/u65-every-listing-declares-its-own-stop-rule`.**
Every provider listing now declares its own stop rule and its own request budget,
in `STOP_RULES` and `PAGE_CAPS` beside the page sizes, and `paginate` takes both
as required keyword arguments so a wrapper that forgets to choose fails to call.

**R-383's code half is done and R-383 is still OPEN**, because its closing
condition is a live read and a live provider call is attended. Two corrections
matter more than the fix itself:

1. **The recorded cause was wrong.** R-383 and its solutions entry both blamed the
   client for dropping unplayable tracks from each page. tidalapi 0.8.11 does no
   such thing: `Favorites.tracks` hands the response to `map_json`, which maps
   every item with no filtering, and the `Track ... is unavailable` line seen
   during the sitting comes from `session.track()`, off the listing path. The
   omission is the API's, and `get_tracks_count` documents it, saying the total
   "also includes track that may not be available for playback". Both records are
   corrected and the measurements are untouched.
2. **The obvious fix is wrong too, and this unit wrote it first.** Stopping on an
   empty page instead of a short one only moves the boundary, because an empty
   page is a page shape as well: a window whose every counted item is unservable
   comes back empty in the MIDDLE of a collection. Reproduced at 300 rows with
   rows 100 to 199 unservable, returning 100 of 200 servable rows silently. The
   unit's own `/code-review` found it.

**No page SHAPE says where a filtered collection ends.** Only a count the provider
publishes for the collection it is serving. `favorite_tracks` ends on
`get_tracks_count` and `playlist_tracks` on the `numberOfTracks` already parsed
onto the object, and neither costs a request, since the count replaces the page
that would have ended the walk. `account_playlists` and `artist_releases` have no
honest count, so they take the weaker empty page rule and carry **R-385** saying
they are narrowed rather than closed. `Favorites.get_playlists_count` is the near
miss and is refused in a docstring: it counts a different collection.

Also in this unit: `max_pages` became a budget of REQUESTS that RAISES
`ListingTruncated` when spent, rather than returning quietly; and a listing that
cannot page now refuses at once instead of being slept on for 31 seconds by the
retry ladder, which was costing this repository's own test file 31 of its 32
seconds and would have cost a 200 artist label crawl over three hours before
reporting a fault it knew about at the first request.

Mutation table `docs/mutation/u65.md`, 25 rows of 27 written, 23 killed, 2 zeros,
both maintainer facing and each given a line, no collect drift, every restore
verified against `git show HEAD`, null control 0. The table was measured at
`42fc8a2` and the file names the two changes that landed after it. Filed: R-384
the request cost, R-385 the two narrowed shapes, R-386 a guarded method name no
test exercises, closed in place by U66. Main's highest residual number is still
R-386. R-383's live half and R-384's live measurement stay attended.

**A METHOD rule could not be followed and needs correcting.** METHOD says run
`scripts/mutate.py` in the foreground. Its fixed overhead on this suite is over
600 seconds, which is the harness tool ceiling, so all three foreground attempts
were killed mid row and two left a partial mutation in
`src/cratekit/acquire/listing.py` that was restored from `git show HEAD:`. The
run that succeeded was a tracked background job, waited on, with nothing else
touching the tree. On this harness foreground is the CONTAMINATING option, which
is the opposite of what the rule assumes.

**Last sitting 2026-09-17, afternoon, attended, six workflows on
`sitting/tidal-runs`.** Not a unit. The three adapters U62, U63 and U64 landed
in September have now each run against the live Tidal account, which is what
`docs/cutover.md` said they owed, and its Sitting 4 table is the record. **R-355
was fixed inside the sitting**: the rows both outbound verbs build carried no
ISRC, so a live export or sweep matched nothing and reported a clean job.
`modules/outbound/source.isrc_for` now resolves each row's `Location` through the
configured prefix map and reads the file's own tag, `isrc` is a field in
`core/tags.py` (`TSRC` in ID3), a value that is not ISRC shaped reads as none,
and an absent library root refuses rather than reading as a library of untagged
files, which the review of the fix found. Live: 103 of 109 favourites and 8246 of
9937 collection rows carry an ISRC where none did before.

With that, `crate export playlist` ran twice on a real four track playlist, one
remote playlist created, 2 added, 2 unmatched, the second run adding nothing, and
`crate sync favorites` ran twice over 109 rows, 18 hearted and verified present on
the account, the second pass hearting nothing and reading all 59 matched rows as
already. **R-144 is CLOSED on the ledger.** Also live: one harvest, one intake
playlist, one 47 label sweep of which 32 labels refused, and one `crate sync all`
that listed 599 playlists and queued 19 jobs, **none of them resumed**, 11 being
source system label debris.

Six findings filed, R-378 to R-383. **R-383 is the one that matters beyond the
sitting**: `listing.paginate` stops at the first short page, and this provider's
favourites listing serves short pages because the client drops unplayable tracks,
so the account's 197 favourites read as 93. Playlists and playlist membership were
measured clean, so it is the filtered listings rather than the helper being wrong
everywhere. Phillip decided it is a unit, not a sitting fix. Mutation table
`docs/mutation/sitting4.md`, 10 rows, 8 killing; `sitting4-notes.md` records that
G9's remeasure was killed by memory pressure and is asserted rather than
measured, and that both driver runs were moved to the background by the harness.
Battery on the committed tree is in the merge commit. Do not take #29.

**The sitting before, 2026-09-17, morning, attended, R-133 on
`sitting/r133-vocal-restamp`.** Not a unit. The vocal restamp ran on the live
library and R-133 is CLOSED on the ledger. It took two fixes, both driven and
both landed in the sitting: R-370, the shipped loader built the clip level
PANNs wrapper against a checkpoint this machine does not hold and the scorer
read the speech columns rather than the singing ones, so no real track could
score; R-371, a tail chunk under a third of a second failed a track. With
them, `crate analyze vocals` over a real 36 track folder completed twice on
the 18 GB machine, 102 and 100 seconds, 1.3 GB peak, every score within one
point of what DJ_tools stamped. `metadata mytags-vocals --apply` then wrote
four associations to the live database inside the acknowledgment window,
1892 already present, after the plan first read clean over 9770 rows it could
not resolve (R-372, the location prefix rule for rekordbox's renamed drive,
added to the config by hand) and after DJ_tools' hand set 5.0 cut was carried
into the calibration state by hand (R-374). Also filed: R-373, R-375, R-376,
and R-377 from the review, which drove ten findings against the fix and
nine are applied.
The analysis and vocals extras are now installed in the venv, which changed
what one slim assumption test drives. `docs/cutover.md` carries the sitting
table. Main's highest residual is R-377. Battery on the committed tree is in
the merge commit. Do not take #29.

**The sitting before, 2026-09-16, evening, attended, R-9 on
`docs/r9-restore-rehearsal`.** Not a unit. The real backup job
`2026-09-16T16:30:43Z-4c99` reports succeeded and was read back on Drive: the
dated archive holds the 1139 objects the dry run predicted and the snapshot's
`master.db` matches the live file. The restore rehearsal ran to a scratch
directory through the engine's `target` seam under the real gates, landed the
database byte for byte, MD5 matched, `integrity_check` ok, and the verb then
reported the restore failed because it copies a write ahead log the snapshot
never holds. R-9 is CLOSED on observation and issue #46 can close back to it.
Three findings filed: R-367, the unconditional sidecar copy, which is a fix
unit; R-368, no verb restores anywhere but the live root; R-369, an
acknowledgment answered from a shell with no terminal cannot be continued
there. The backup acknowledgment is minted, by the author from a Terminal
window, valid until 2026-09-17T13:11Z. The live database was not touched.
`docs/cutover.md` carries the sitting table. Main's highest residual is R-369.
Battery on the committed tree is in the merge commit. Do not take #29.

**The session before, 2026-09-16, #83 on `relay/83`, unattended.** Not a unit. The four
small defects the first attended sitting found are fixed and closed in the
ledger. R-344: `preflight.same_identity` folds the case on both sides of both
identity compares, and setup still records the identity as given, because it is
also the `library_id` jobs and watermarks match exactly. R-346: the prompter
flushes, so setup from a real terminal no longer needs `PYTHONUNBUFFERED=1`.
R-347: an empty secret raises `prompt.NothingEntered` and the credential offer
records it as the INFO note a no gets. R-348: `adapter.raise_if_defect` makes an
`AttributeError`, `TypeError` or `NameError` under an offer or a fetch an
`AdapterBroken` with the adapter's new `report-defect` token, asked before the
vendored token heuristic. Review raised one plausible finding, filed as R-365;
the hunt one file over filed R-366. Mutation tables `docs/mutation/r83.md`, 17
rows, 14 killing, and `r83-round-2.md` after the fold tests moved off an all
digit identity that was its own uppercase, 3 of 3 killing. The two remaining
zeros are maintainer rows, the strip in `normalize_identity` and the sweep's None
guard, which is an equivalent mutation. **Both tables ran in a harness moved
background job.** Each driver call was started in the foreground, outlived the
600 second tool ceiling, and was moved to the background by the harness, and the
session then waited on the output file with nothing edited meanwhile. Every row
reports its restore verified against HEAD and the tree held only the driver's own
output afterwards, which is the same shape
`docs/solutions/workflow-issues/a-relay-task-finished-a-mutation-table-by-backgrounding-the-driver-the-rule-forbids.md`
says is not validated. Phillip may want the tables rerun attended. Main's highest residual was R-366 once
`relay/83` merged. Battery on the committed tree before the record: ruff clean,
`scan_repo.py` exit 0, pytest 7543 passed and 1 skipped in 393 seconds. Do not
take #29.

**The session before, 2026-09-16, U64 (#86) on `relay/86`, unattended.** The playlists
source runs. `crate sync all` lists the account through a fifth `Catalogue` read,
`account_playlists`, which `TidalCatalogue` answers through `listing` and keeps to
playlists whose creator is the logged in user, refusing a client that cannot name
its account. `sync.playlists` excludes, in this order, the `DOWNLOADED ` prefix,
an id in the playlists cursor, a favourites placeholder by
`favorites.placeholders.PLACEHOLDER_NAME` (a dated quarter or the undated
backlog), an open job this source queued, and an empty playlist, then queues each
remaining one through `intake.cli.queue_playlist` under the pass's run id with
`source_id` `playlists`. A plan in `sync/cli.py` now carries every job its source
filed, and the summary gains a `playlists` block. The cursor is a `swept` id list
on the watermark record, written by `WatermarkStore.record_swept`, and
`reconcile` records a playlist at the start of a pass once its job SUCCEEDED, for
this library only. The mark is reported `unbound` every pass, because the account
seam has no rename. Review drove one finding, the undated backlog placeholder.
Mutation table `docs/mutation/u64.md`, 25 rows through the driver's own functions
on subsets, 24 killing, C2's zero closed with a test, C3 a maintainer zero on the
full suite. Three reserved cause population pins moved and are re-pinned with
their sets named. **R-358 and R-359 are the ones to read before the attended
sitting**: a swept playlist is never renamed, and swept means resolved rather than
acquired. R-360 to R-364 are filed beside them. Battery on the recorded tree: ruff clean,
`scan_repo.py` exit 0, pytest 7522 passed and 1 skipped in 392 seconds. Do not
take #29.

**The session before, 2026-09-16, U63 (#85) on `relay/85`, unattended.** The outbound
account seam is bound. `modules.outbound.tidal_account.TidalAccount` implements
the six add only `RemoteAccount` members over U62's `client_session`, imports
nothing vendored, and pages through `acquire.listing`. `account.resolve` refuses
`credential-missing` with no session, logs in ONCE and holds the adapter for the
process, because both workers resolve per item; `account.forget()` drops it, and
a conftest autouse calls it around every test. `bound()` answers whether the
adapter imports, so the queued warning is gone in a shipped build. Matching is an
ISRC naming exactly one track, then an exact provider track URL, else `None`.
`has_heart` answers from one paged favourites read, `add_heart` and
`add_to_playlist` check first, writes retry once, a create never. A provider
failure is an ITEM scoped cause through `account.provider_failure`: 401, 403 or
the client's authentication error is `credential-missing` and drops the held
account, everything else `unavailable-transient`. Review drove four findings: an
add the client answers without the track, a 400 read as a rejected session, the
dead client kept, and `bound()` not importing the client library. Mutation table
`docs/mutation/u63.md`, 25 rows, all killing on subsets, checked by hand for
R-329's reason, three zeros closed with tests. R-226's agent half is closed.
**R-355 is the one to read before the attended sitting: no shipped row carries an
ISRC, so a live sweep or export today matches nothing and writes nothing.** R-356
and R-357 are filed beside it. Next unit is U64 (#86). Do not take #29.

**The session before, 2026-09-16, U62 (#84) on `relay/84`, unattended.** The label
catalogue seam is bound. `acquire.provider_session.client_session` is the one
factory that logs a provider client in from the keychain inside the materialised
scope; U63 is meant to reuse it. `label.tidal_catalogue.TidalCatalogue`
implements the four `Catalogue` reads, pages through `acquire.listing`, imports
nothing vendored, and raises named errors rather than returning `None`.
`catalogue.bound()` answers whether that module imports, so the enqueue warning
is gone in a shipped build. A conftest autouse guard replaces
`provider_session.CLIENT_FACTORY` so no test can reach the live provider; a test
that wants a client sets it. The factory's tests live in
`tests/test_label_tidal_catalogue.py` rather than `tests/test_adapter_contract.py`.
Review drove three findings: an outage is `unavailable-transient` rather than a
new login, the roster lists once at construction, and a name two artists share
refuses. Mutation table `docs/mutation/u62.md`, 24 rows, 23 killed, the one zero
removed as redundant. R-258's agent half is closed; its live half and R-350 to
R-354 are the next attended sitting's, listed in `docs/cutover.md`. Next unit is
U63 (#85). Do not take #29.

**The session before, 2026-09-16, the first attended U29 sitting, on `main` with
Phillip present.** Not a unit. `docs/cutover.md` now exists and is the record.
Setup ran for real against the live library volume, the pin 7.2.18.0311 is
recorded, three credentials are in the keychain, the doctor reports no failing
check, and the commit-msg hook is installed in this checkout so `repo.commit_hook`
is green. **R-210 is CLOSED on observation**: a real FLAC landed with no tempo
tag through the PKCE session, and a fresh device-flow session on the same
account and track was served AAC. The first real download found **#82**, the
adapter handing the vendored tool a function where it calls a logger, fixed and
merged as `8f89efc` with a guard that reads the method set off the vendored
tree. R-9's dry run ran and its real run, job `2026-09-16T16:30:43Z-4c99`,
ended succeeded; the second sitting that evening read it back on Drive, ran
the restore rehearsal and closed R-9. Seven findings are filed, R-343 to R-349.
R-346 is fixed on `relay/83`, so setup from a real terminal no longer needs
`PYTHONUNBUFFERED=1`.

**THE BOARD IS COMPLETE AND THE PRODUCT CANNOT SYNC.** `docs/cutover.md` says
why in one section: R-258 and R-226 are unbound adapter seams and the playlists
source has no listing, so nothing in the product lists Tidal. That was the
remaining build, on the board as U62 (#84), U63 (#85) and U64 (#86), with #29 declared dependent on all three. U62, U63 and U64 have since landed their agent halves, R-355 means the account half matches nothing live yet, and R-358 means a playlist Cratekit sweeps is not marked on the account. R-9 is closed on the ledger; the restore verb's defect is R-367. Do not take #29.

**The session before, 2026-09-11, U25 on `unit/u25-vocal-restamp-and-my-tags-shells`.**
The two remaining vocal CLI shells landed. `cratekit.vocals.cli` queues
`analyze.vocals` and scores files that already carry a Camelot head, which
closes R-277. `analyze.run` still skips a prefixed name. `cratekit.write.metadata_cli`
plans My Tags by default and writes them when apply is requested, through the guarded
writer on the configured database, never the live one. Both `planned_in`
markers are gone, `analyze.vocals` is bound in `HANDLERS`, and
`owed_by_unit()` no longer lists 25. Nineteen landed verbs now queue and
eighteen are bound; `job.resume` remains the unbound exemption. R-133's 18 GB
run stays attended. Do not take #29.

**THE DRIVER RAN.** Twenty five rows in `docs/mutation/u25-rows.toml`,
measured by `scripts/mutate.py` in 6131 seconds, eleven killing, thirteen
zero on the full suite, one refused. Null control 0 of 7401. The zeros
have no composite, which is R-341. A corrupt vocal calibration still
defaults to the 12.0 cut, which is R-342. The reading is
`docs/mutation/u25-notes.md`.

**The session before, 2026-09-11, brief rewrite for U25, not a unit.** #80 is closed.
U25 was not finished. That was the answer R-324 asked for, and the 2026-09-10
reopen of #25 had already taken it. What was still missing was a brief a session
could build against: the issue body still described the DSP port, which is in the
tree. The body then named the two remaining shells, `analyze.vocals` and
`metadata.mytags-vocals`, the engines they sit on, R-277, and R-133 left
attended.

**The session before, 2026-09-11, R-102 on `relay/54`, taken from the board as issue #54
and run as relay task 54.** The twelfth residual issue worked, and the last of
METHOD's guard group. Test work, closed in place, with one piece filed. The
reports allowlist audit in `tests/modules/test_reports.py` now walks the IMPORT
CLOSURE of `ALLOWED_IMPORTS`, not the list: `_admitted_closure` follows import
statements, `__import__` and `importlib.import_module` in one worklist pass and
returns what it cannot follow, which the audit refuses. Driven on the real tree,
`cause` calling a planted `access_probe` reads clean to the one hop walk and red
to the closure. **The closure is eighteen modules and reaches `rb_writer`**
through `rbxml`, `tree_registry` and `session`, so forty nine writers are now
named in `QUALIFIED_MUTATIONS`. **A unit that adds a writer to the write path
will now fail `test_reports.py`**, and the learning is
`docs/solutions/workflow-issues/the-reports-allowlist-audit-reaches-the-write-path-so-a-new-writer-there-fails-test-reports.md`.
The built in review drove three holes in the first version, `import_module`
unread, an unconditional package fallback, and a resolver asking the real tree
for a planted one, and all three are fixed and driven. R-340 is the report side:
a report calling a named writer through another module's attribute is not
caught. Sixteen rows are in `docs/mutation/r-102-rows.toml`, fourteen killing
and two predicted maintainer facing zeros, checked by hand on the one file and
recorded in `docs/mutation/r-102.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-15 on `relay/53`, taken from the board as issue #53
and run as relay task 53.** The eleventh residual issue worked, and the third of
METHOD's guard group. Test work, closed in place, with one piece filed. Measured
before any pin: a sixth permitted table and a bookkeeping column swapped for a
content column killed nothing in the full suite. `tests/test_whitelist_membership.py`
pins `PERMITTED_ROW_TABLES`, `BOOKKEEPING_COLUMNS`, and the content allow list,
which is registry derived here and so is pinned at baseline, per metadata
operation with its ownership mode, and fully enabled. The two deny lists beside
them, `GRIDLESS_ON_CREATE_COLUMNS` and the unwritable metadata fields, are pinned
too, since a removal is their widening. An AST audit holds every
`Rekordbox6Database` call in `src` to an explicit non empty `path=`. The built in
review found that `db_dir` also sets the binding's share directory, and that the
rows file's batch name would have let the driver overwrite the hand record, now
`r-15-driver`. Checking which file the connection opened is R-339. Ten widening
rows are in `docs/mutation/r-15-rows.toml`, all ten checked red by hand on the pin
file and recorded in `docs/mutation/r-15.md`, and unrun by the driver, for R-329's
reason.

**The session before, 2026-09-11, R-14 on `relay/52`, taken from the board as issue #52
and run as relay task 52.** The tenth residual issue worked, and the first of
METHOD's correctness group. A fix, closed in place, with one piece filed. Read
against the tree, nothing in `src` joined `AnalysisDataPath` to anything. What
did exist was seven call sites arming the analysis watch over the library root
alone. With an acknowledged database outside the root, the share and every grid
sit outside it too, so each of those sessions watched nothing. `core.analysis_store`
now owns the join. `share_root` is the directory beside the configured database,
`analysis_file` joins a stored value to it, and `watch_roots` adds the share when it
sits outside the root. The seven sites take `watch_roots`, and an AST guard in
`tests/test_analysis_store.py` refuses a hand listed root. The backup carries the
share only when it sits under the root. Outside it, the plan, the outcome and the
verb's envelope now say `analysis-share-not-carried`, which the built in review
found reached nobody until the envelope asked for it. Carrying the share is R-338.
The kebab literal pin moved 401 to 402. Ten mutation rows are in
`docs/mutation/r-14-rows.toml`, two checked red first by hand and the rest unrun,
for R-329's reason.

**The session before, 2026-09-11, R-11 on `relay/48`, taken from the board as issue #48
and run as relay task 48.** The ninth residual issue worked, and the last of
METHOD's surface group. Two of its four findings closed, two stay on the ledger.
The CRLF absorption was three copies, not the four R-11 counted, since the
catalog writer takes the break after a node rather than before it. The three are
now `rbxml._absorb_lead_break`, and the goldens pass unchanged. The analysis
watch is now driven through the database half:
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session` plants a
real ANLZ file under the library root and asserts the `anlz-modified` refusal.
`apply_rating_changes` stays kept, since the wrapper has grown nothing. The real
label in two fixtures is still the author's decision about D1. Nothing new was
filed. Six mutation rows are in `docs/mutation/r-11-rows.toml`, two checked red
first by hand and the rest unrun, for R-329's reason.

**The session before, 2026-09-11, R-10 on `relay/47`, taken from the board as issue #47
and run as relay task 47.** The eighth residual issue worked, and the second of
METHOD's correctness group. A fix, not a close. `rb_writer.add_memberships`
takes one playlist and many content ids, reads what the playlist holds in one
query, and returns the ids it inserted. `add_membership` is a one id call into
it, so the only when absent rule still lives in one place. `write_tree_membership`
makes one call per playlist instead of one per track, and resolves each folder
once per session instead of once per plan entry. What remains per inserted track
is the binding's own content lookup and track count inside `add_to_playlist`,
which R-10 did not describe. R-10 is closed in place and nothing new was filed.
Eight mutation rows are committed in `docs/mutation/r-10-rows.toml` and unrun,
for R-329's reason.

**The session before, 2026-09-11, R-7 on `relay/44`, taken from the board as issue #44
and run as relay task 44.** The seventh residual issue worked, and the third of
METHOD's surface group. A close, since U27's doctor already reports a trashing
remote with its option unset, and setup runs doctor. Read against rclone
1.74.3's own backend help, two of that check's rows were wrong and are fixed.
Dropbox's row named an option the Dropbox backend does not have, so it failed
every run with a fix nothing could apply. OneDrive's `hard_delete` does nothing
on a personal drive and read green there. `TrashPolicy.applies_when` now gates
it on `drive_type`. R-336 and R-337 are filed. Six mutation rows are committed in
`docs/mutation/r-7-rows.toml` and unrun, for R-329's reason.

**The session before, 2026-09-11, R-6 on `relay/43`, taken from the board as issue #43
and run as relay task 43.** The sixth residual issue worked, and the second of
METHOD's surface group. Another close, measured on the registry: sixty four
entries, sixty two landed, and conformance 1, 2 and 3 parametrise over all
sixty two rather than the four R-6 described. The two markers left are U25's
vocals verbs, which R-324 and the reopened issue already own, so R-6 did not
carry them a second time. The `cratekit.cli.verbs` docstring said the package
held exactly U5's four verbs and it also holds `login`; it is corrected. No guard
changed, so there is no mutation table, and nothing new was filed.

**The session before, 2026-09-10, R-5 on `relay/42`, taken from the board as issue #42
and run as relay task 42.** The fifth residual issue worked, and the one METHOD's
ninth line names first. It was a close, as that line guessed. R-5's closing
condition was already true: U11 and U27 are closed, conformance 4 drives the
review queue and conformance 8 drives the doctor, and neither is an existence
check. What was false was the claim, in R-5 and in the docstrings of conformance
4 and 6, that no adjudicating or destructive verb had landed. Every adjudicating
verb has, and twenty two of twenty four destructive ones. The docstrings are
corrected. The gap they described, that neither assertion drives a landed verb
through the dispatcher, is still real and is R-335. No guard changed, so there is
no mutation table.

**The session before, 2026-09-10, R-4 on `relay/41`, taken from the board as
issue #41 and run as relay task 41.** The fourth residual issue worked, and the first of
METHOD's surface group. R-4's written closing condition was already true: each
of the nine toggles U5 declared gates a landed verb and none carries
`planned_in`. `registry.Entry` now refuses an `extras` group that is not the
verb's own `module_id` or is missing from `EXTRAS_BACKED`, because the stub
prints that field as the install command and nothing tied it to pyproject. A
derived parametrized test drives all thirteen toggles with landed verbs through
the resolver and parser in both directions. R-4 is closed in place, nothing new
was filed, and six mutation rows are committed in `docs/mutation/r-4-rows.toml`
and unrun, for R-329's reason.

**Two sessions back, 2026-09-10, R-3 on `relay/40`, taken from the board as issue #40
and run as relay task 40.** The third residual issue worked, and the second of
METHOD's guard group. `scripts/scan_repo.py` REFUSES a tracked archive now
instead of skipping it, by suffix and by header, so a renamed archive is refused
too. R-3's written closing condition was already true on the tree, since U13
committed the downloader unpacked, and nothing kept it true. R-3 is closed in
place. R-334 is the list still being closed, plus the same silent skip for a
`.db` or `.sqlite` file, and the choice there is Phillip's. Fifteen mutation rows
are committed in `docs/mutation/r-3-rows.toml` and unrun, for R-329's reason.

**Three sessions back, 2026-09-10, R-1 on `relay/38`, taken from the board as
issue #38 and run as relay task 38.** The second residual issue worked rather than a unit,
from the guard group in METHOD's ninth line. `crate doctor`'s `repo.commit_hook`
now reads every hook type `.pre-commit-config.yaml` names and checks each
installed hook, not only `.git/hooks/pre-commit`. R-1 is closed in place, and
R-333 is the one conservative call, a FAIL when PyYAML is not importable.

**THE PRIMARY CHECKOUT FAILS THAT CHECK, AND IT IS RIGHT TO.** It has a
pre-commit hook and no `.git/hooks/commit-msg`, so the board closing hook has
never run locally. Only CI has been judging trailers. The fix is Phillip's,
because it writes into `.git/hooks`:
`pre-commit install --hook-type pre-commit --hook-type commit-msg`. Twenty five
mutation rows, all killing, are in `docs/mutation/r-1.md`. The driver outran
the ten minute foreground ceiling twice, and a polling wait in the foreground
carried it through.

**Four sessions back, 2026-09-10, U61 on `relay/79`, taken from the board as
issue #79 and run as relay task 79.** `crate sync all` is a COMPOSER now. It plans every
enabled source, asks the favourites confirm once, then queues each source through
that source's own `queue_sweep` under that source's own handler key, with one
intake run. Nothing is queued under `sync.all`, so its entry dropped
`long_running` and `argv_builder` and **R-203 CLOSED**: `HANDLERS_NOT_YET_BOUND`
holds only the `job.resume` exemption. Playlists has no worker and is reported as
not built, so a slim pass is a no-op rather than an ok.

**A COMPOSED JOB NEEDS A RUN ITS OWN VERB OWNS.** The dispatcher refuses a `--run`
whose record belongs to another verb, so the favourites job could not carry the
pass's run as its gate run. `Gates.hand_off` copies the recorded answer onto a new
run owned by `sync.favorites`. The learning is
`docs/solutions/integration-issues/a-verb-that-queues-another-verbs-job-must-hand-it-a-run-that-verb-owns.md`.

**U61 HAS NO MUTATION TABLE EITHER, and the reason is now measured.** The null
control is hardcoded to the full suite at `scripts/mutate.py:1002`, so the
driver's preflight is two full runs, about 720 seconds, whatever the rows say.
R-329 carries the correction, `docs/mutation/u61-notes.md` the sampled timing.

**Five sessions back, 2026-09-10, U60 on `relay/78`, taken from the board as
issue #78 and run as relay task 78.** `delete.review` stopped claiming a queue. Its entry
dropped `long_running` and `argv_builder`, `delete_argv` is gone, and the verb
left `HANDLERS_NOT_YET_BOUND`, so R-149 closed in the direction it left open.
R-134 closed too, at a schema cost of zero fields: the first run's baseline rides
the gate's existing context onto the refusal as `cause.detail.shown`, which
`render_gate` prints for a person, and `review_set/1` is untouched.

**A NEW REGISTRY GUARD HOLDS THE CLASS.**
`test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues` parses every
landed long-running verb's module for an `enqueue` call, with `job.resume` exempt
by role. It failed on `main` for `delete.review` alone. Its module-wide bar is
R-328.

**U60 HAS NO MUTATION TABLE, AND THAT IS A MEASURED GAP, NOT A CLEAN ONE.**
`scripts/mutate.py` reruns a six minute full baseline on every call, and a relay
task runs every command in the foreground under a ten minute ceiling, so two
attempts ended in preflight with no row measured. The rows are committed and
ready, `docs/mutation/u60-notes.md` holds the measurements, and R-329 is the gap
with three options, all Phillip's. The learning is
`docs/solutions/workflow-issues/the-mutation-driver-does-not-fit-a-ten-minute-foreground-call.md`.

**Six sessions back, 2026-09-10, R-322 closed on `relay/81`, taken from the
board as issue #81 and run as relay task 81.** The first residual issue to be worked
rather than a unit, and the first work of the ninth line in METHOD's serialized
order. It added SEVEN tests and thirteen lines of `scripts/board.py`, no new
behaviour, and it closed the audit's detector being driven by nothing.

**THE CONTRADICTION DETECTOR HAS A DRIVER NOW.** `contradictions()`,
`units_by_issue_number`'s exclusion of unlabelled unit-shaped titles, the
residual repoint half of the return, the default register read, and
`cmd_audit`'s exit codes are all driven. Both rows R-322 was built out of went
from zero to killing, re-run verbatim from U59's row file so the comparison is
two measurements of one experiment. `docs/mutation/u81-notes.md` is the reading
and it carries one correction to its own first row file.

**THE DOUBLE IS THE `gh` PAYLOAD, NOT THE GRAPH, AND THAT IS THE DECISION R-322
ASKED FOR.** A hand-built graph would type every key `build_graph` derives, so
the producer could drift and the tests would stay green. The fixture is the issue
list JSON, `build_graph` runs on it for real, and the field list is read out of
`load_issues`'s syntax tree and compared against the double's keys. The learning
is filed at
`docs/solutions/workflow-issues/a-double-belongs-at-the-producer-boundary-not-at-the-shape-it-produces.md`
and it carries two traps that cost a round here.

**The pending register is still EMPTY** and nothing in this session touched it,
so no `@requires` decorator exists anywhere.

**U59, the session before this one, built on `relay/77`.** It ran the whole
pipeline in one session: plan, the merge, the built in `/code-review`, a six
finding fix round, a twenty five row mutation table with one composite, and its
record. The merge is what kept the pending register empty: git took `main`'s
empty `PENDING` and only the branch's three-state `module_state` probe, so
nothing was re-armed.

**THE SOFT DELETE DEFECT IS OFF MAIN.** `write/metadata.resolve_genre_id` no
longer defaults the marker. A row that cannot report it refuses with
`soft-delete-marker-unreadable` at run scope rather than reading as active, and
the rule is driven through the SHIPPED reader, `crate tag retag` into
`plan_library` into `plan_genre_retag`, not only through the function's own
rows. R-186 closes.

**THE CONFORMANCE BRANCH IS LANDED AND ITS WORKTREE IS UNTOUCHED.**
`.worktrees/conformance` and `fix/conformance-3-and-soft-delete-reader` are
exactly as they were; the merge was taken on `relay/77` in the primary checkout.
**Two of its eleven commits were already on `main`**, the conformance 3 pair, so
`tests/test_cli_contract.py` is byte identical to `main` and this merge armed
three guards rather than the five the brief names. That is R-326.

**PHASE E'S AGENT HALF IS DONE.** Three verbs stopped reporting work nobody had
done. `route.inbox` applies on the confirmed branch instead of returning the
plan on both. `route.unplaced` reads the library instead of being
`_plan([], ...)`. `rebuild` and `route.resort` queue one item per governed tree
and drive them, and a library that has flipped no tree files no job at all
rather than an empty one. Both workers go through
`rebuild.rebuild_governed_tree`, which is the FIRST CALLER of `rebuild_tree`
anywhere in `src`.

**EVERY QUEUED VERB HAS A WORKER**, with `job.resume` exempt by role. Measured:
eighteen landed verbs queue and seventeen are bound. `delete.review` left the
population in U60 by ceasing to be queued, and `sync.all` left it in U61 by
queueing its work under keys that have workers. R-203 is closed with a note in
place. Its title stays at eighteen on purpose, because the title names what was
true when the entry was written.

**R-131 IS DOWN TO ITS ATTENDED HALF.** Everything in it that a session could do
is done and driven against a disposable database copy. Nothing has run on a live
tree, which is the whole of what the entry now says.

## Main, verify before trusting it

    git status -sb                              # no ahead or behind count
    git status --porcelain                      # empty
    .venv/bin/pytest --tb=no                    # run it; do not trust a count here
    .venv/bin/python scripts/board.py audit     # exit 1 on the In review card, R-265

**Main's highest residual is R-357 once `relay/85` merges**, R-355 to R-357 being
U63's, with R-226's agent half closed in place, no duplicate heading and no
heading moved. U63's full suite before the review round was **7491 passed and 1
skipped** in 400 seconds on a committed tree, and after the review round, the
zero row tests and the record it was **7500 passed and 1 skipped** in 397 seconds.
The nine are six review fix tests and three zero row tests, all in
`tests/test_outbound_tidal_account.py`.

**Main's highest residual was R-342 once U25 merged**, R-341 and R-342
being U25's, with R-277 closed in place, no duplicate heading and no heading
moved. Mutation baseline collected **7401** on a committed tree. The last
full battery before the record was **7399 passed and 1 skipped**, in 374
seconds, then one more test landed (the missing My Tag template through
the dispatcher).

**Main's highest residual was R-340 once `relay/54` merged**, R-340 being that
branch's only filing, with R-102 closed in place, no duplicate heading and no
heading moved. Its suite was **7379 passed and 1 skipped**, in 358 seconds, on
`relay/54` on a committed tree. The eight since R-15's 7371 are this branch's
eight new identifiers in `tests/modules/test_reports.py`: six cases of
`test_the_audit_follows_an_admitted_module_to_the_module_that_writes`,
`test_the_closure_reports_an_import_it_cannot_follow`, and
`test_a_symbol_imported_from_a_package_follows_the_package_initializer`. That is
the new names matched against the delta, not the full collection differenced
against `main`. The R-15 record follows.

R-15's suite was **7371 passed and 1 skipped**, in 356 seconds, on
`relay/53` on a committed tree. The nineteen since R-14's 7352 are all in the new
`tests/test_whitelist_membership.py`: seven membership pins, the tree open audit,
ten audit refusals and one acceptance. The R-14 record follows.

R-14's suite was **7352 passed and 1 skipped**, in 352 seconds, on `relay/52` at
the record commit. The fourteen since R-11's 7338 are this branch's own: eleven in the new
`tests/test_analysis_store.py`, `test_the_analysis_watch_reaches_a_share_outside_the_library_root`
in `tests/test_adopt_apply_cli.py`, and the outside and contained drives in
`tests/test_backup_cli.py`. The R-11 record follows.

The last measured suite was **7338 passed and 1 skipped**, in 352 seconds, taken
on `relay/48` on a committed tree. One of the four since R-7's 7334 is R-11's
`test_a_grid_rewritten_during_a_membership_write_refuses_the_session`; the other
three arrived with R-10, whose own count was not recorded, so that split is not
reconciled by identifier. **Main's highest residual stays R-337 once this branch
merges**, since R-11 filed nothing. The earlier record follows. Against R-6's
7328 the six are R-7's own in
`tests/test_doctor.py`: four cases of
`test_a_onedrive_remote_where_hard_delete_does_nothing_is_a_note` and two of
`test_dropbox_is_not_told_to_set_an_option_rclone_does_not_have`. **Main's
highest residual is R-337 once this branch merges**, R-336 and R-337 being this
branch's, with no duplicate headings and none deleted. R-5 and R-6 changed no
test. Against R-3's 7312 the 16 before those are R-4's
own, reconciled by identifier in `tests/test_cli_contract.py`: two rejection
rows in `test_an_entry_missing_its_metadata_fails_to_register`,
`test_every_live_toggle_is_driven_by_the_toggle_test_below`, and thirteen cases
of `test_a_module_toggle_alone_switches_its_landed_verbs_on_and_off`. **Main's
highest residual stays R-335 once this branch merges**, no duplicate headings, no
heading deleted, and R-6 gained its closing note in place rather than moving.
Append only, and gaps are fine.

**The kebab literal pin in `tests/test_reserved_causes.py` moved 401 to 402** on
R-14, for `analysis-share-not-carried`, a warning code and not a cause. Before
that it moved 391 to 401 for ten git hook type names, differenced as sets
against `main`, none of them a cause.

**THE AUDIT EXITS 1 NOW, NOT 2, AND THE REASON IS A BOARD WRITE NOBODY RECORDED.**
Measured on 2026-09-10 while closing R-322: issue #25 is OPEN with a state reason
of REOPENED, so `contradictions()` returns nothing and the exit 2 U59 predicted
is gone. The registry still owes U25 two modules, which is now the register
working rather than a contradiction, and R-324 and #80 stay open because whether
that is U25's answer is #80's judgement. Do not weaken the check to get a green
audit; **the detector is now driven and softening it fails tests.**

**The one thing the audit does report is R-265, and `sync` is the wrong answer to
it.** `#81 status is In review, should be Ready`. `derive_status` knows five
statuses and the field has six, so every relay card reads as drift for the whole
of its run, and the remedy the audit prints would drag the card back to Ready
mid review. Leave it. Confirmed a second time on #81.

## Read this before touching a write path again

**A GUARD THAT REFUSES AN EMPTY LIST CANNOT SEE A BARREN ONE.** The unit's
learning, filed at
`docs/solutions/integration-issues/a-guard-that-refuses-an-empty-list-cannot-see-a-barren-one.md`.
Both new writes named `root/Music` as their `analysis_roots`, which is one entry
so it passed `write_tree_membership`'s empty-list refusal, and which holds no
ANLZ file, so the beat grid watch fingerprinted nothing and would have reported
a clean session whatever happened to the grids. Every other caller in the
package names the library root. **Judge a new call site's argument against what
the existing call sites pass, not against whether the callee accepted it.**

**THE ITEMS ARE THE DECISION, NOT THE CALL SITE.** Binding a queued verb is one
line at the call site and two real decisions before it: what an item IS, and
what the per item worker does. For these two the item is a TREE, which is what
makes a partial failure recoverable rather than a single collapsed failure.

**A RESUME OWES THREE CHECKS, and the corrected shape is in `intake/cli.py`.**
Refuse a job queued for another verb, because `handlers.run_job` reads the worker
off the JOB ROW and not off the verb somebody typed. Refuse a job with no items,
because every rebuild and resort queued before U53 has none. Re-raise the job's
own cause when it did not end well, which is R-225: `drive` raises only when
EVERY item failed, so a partial failure returns normally and an unconditional OK
exits zero over half a library.

**THE RESORT IS ADDITIVE**, which is R-312. There is no database removal path in
this build, so a genre change leaves the track in its old sub as well as its new
one and the convergence check names the leftovers.

## What U61 left behind

Three residuals, two notes in place, one learning and one learning corrected.

- **R-330.** A job an older build queued under `sync.all` stays in the queue with
  no worker and reads as a defect until somebody cancels it.
- **R-331.** A handed decision carries no record that it was handed, so a run
  record alone cannot tell it from one given directly.
- **R-332.** A pass where every source refused raises the first refusal, so the
  person sees one remedy and meets the other on the next pass.
- **R-329's second option was written on a wrong reading of the driver**, and the
  learning about the ten minute ceiling said the same thing. Both are corrected.

## What U60 left behind

Two residuals and one learning.

- **R-328.** The new queueing guard accepts an `enqueue` call anywhere in a
  verb's module, so two verbs sharing a module pass on one call. Nothing
  exploits it today: every shared-module pair also shares a worker.
- **R-329.** The mutation driver cannot finish a batch inside a relay task's ten
  minute foreground ceiling. U60's twenty rows are committed and unmeasured.
  **Read the learning before an unattended session plans a table**: if the
  battery's full suite is past roughly four minutes, commit the rows, record the
  gap and land, rather than spending ceiling length calls finding out.

## What U59 left behind, beyond the code

Seven residuals, R-320 and R-321 renumbered in from the branch and R-322 through
R-326 filed by this session, plus one learning. Four are worth knowing before
touching the board tooling or a source guard again:

- **R-324.** The registry owes U25 two modules. Its issue was reopened by
  somebody between the U59 merge and 2026-09-10, so the audit no longer exits 2
  and the loud half is discharged while the substantive half is not. The section
  above carries the measurement. #80 is still the decision.
- **R-322. CLOSED on `relay/81`, and the head of this file says what it took.**
  Both zero rows kill now. What replaced it is R-327, the board's WRITE half,
  which is a harder case rather than the same one: `reconcile` reads a user-owned
  project that a repository-scoped token cannot see at all, so there is no local
  payload seam to build an honest double at.
- **R-323.** A trailer names an ISSUE and both registers name a UNIT. Twenty
  four units are mismatched today and none of them is owed a module, which is why
  this was never seen. `audit` resolves the mapping through the issue titles now.
  The network-free hook cannot, so it says that it guessed.
- **R-326.** Two of the parked branch's eleven commits were already on `main`.
  Found by reconciling the collected count BY IDENTIFIER; a total-only check
  showed a healthy rise and would have said nothing.

**A GUARD THAT GOES RED AT A MERGE HAS TWO POSSIBLE CAUSES AND ONLY ONE IS THE
GUARD.** Four went red here and all four were right about their rule and stale
about the tree. Filed at
`docs/solutions/workflow-issues/a-guard-written-against-an-old-tree-goes-red-holding-a-rule-that-is-still-right.md`.
The dangerous reading is the other one: weaken a stale guard to get green, and
the rule it was holding goes with it.

## What U53 left behind, still current

Eight residuals, R-312 through R-319, corrections to R-203 and R-131, and one
learning. Four are worth knowing before touching routing again:

- **R-312.** The resort adds and never removes, so a re-place doubles a track's
  membership until somebody takes the old one out by hand.
- **R-314.** `assert_addressable` kills ZERO tests, and so does the composite
  over the refusal inside it, measured over the full suite twice. Nothing in the
  repository produces a colliding destination set. The extraction into
  `plan_destinations` is what made that measurable; the gap predates it.
- **R-316.** Neither worker derives the vocal dimension and neither reports the
  gap the engine hands them, so a library with vocal playlists declared gets a
  clean job and an unfiled dimension.
- **R-313.** `route.unplaced` declares `writes` and `destructive` and only
  reports, so a person is told to close rekordbox for a read.

## What U57 left behind, still current

**THE RECOGNITION IDENTIFIER IS REAL AND HAS SPENT NOTHING.** The spend is known
BEFORE the first call, not counted after it, and a spend refusal is its own cause
and never a miss. Identifying at the queue is un-resumable spend, R-304, and the
ledger counts attempts the service never received, R-306. No live key is bound,
so the response table has met no real answer, which is R-300.

**A SEAM THAT RETURNS ONLY ROWS READS ABSENCE AS EVIDENCE OF ABSENCE**, filed at
`docs/solutions/workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md`.

**R-308.** `core.artifacts` landed and the four feature copies are not migrated
onto it.

## What U54 and U58 left behind, still current

**R-289**, the acquisition staging tree is a dotfile and `tagging.tag.audio_files`
walks dotfiles. **R-290**, a blocked job reports outcome `ok` and exits 0 in every
queued verb, which is the envelope contract rather than any one verb's line.

**The resume reads a rename intent, never the folder**, filed at
`docs/solutions/workflow-issues/a-worker-that-renames-its-item-owes-the-resume-an-exact-record.md`.
It applies to every remaining R-203 worker that moves files.

**The heavy stack stays behind the extra**, because `cli.jobs.argv_for` imports
the verb module by name to build a resume line.

**A fallback must not fill an absence somebody meant**, filed at
`docs/solutions/workflow-issues/a-remedy-fallback-overwrites-an-absence-somebody-meant.md`.

## What is open

In METHOD's serialized order, which is what picks the work:

| order | issue | unit | state |
|---|---|---|---|
| 7 | | Phase E explanation, Phillip's and not a session's | |
| 8 | #77 | U59, land the conformance branch | DONE on `relay/77` |
| | #78 | U60, the deletion pass | DONE on `relay/78`, no mutation table (R-329) |
| | #79 | U61, `crate sync all` composes the source increments | DONE on `relay/79`, no mutation table (R-329) |
| 9 | #38 | R-1, doctor checks every configured hook type | DONE on `relay/38`, 25 of 25 rows killing. Halted `partial_landing`, repaired by hand 2026-09-11 |
| | #40 | R-3, the scan refuses a tracked archive | DONE on `relay/40`, 15 rows committed and unrun (R-329) |
| | #41 | R-4, extras tied to their module and every toggle driven | DONE on `relay/41`, 6 rows committed and unrun (R-329) |
| | #42 | R-5, conformance 4 and 8 already drive behaviour, closed in place | DONE on `relay/42`, no guard changed, R-335 filed |
| | #43 | R-6, the conformance drives cover sixty two landed verbs, closed in place | DONE on `relay/43`, no guard changed, nothing filed |
| | #44 | R-7, doctor reports a trashing remote, closed in place with two rows fixed | DONE on `relay/44`, 6 rows committed and unrun (R-329), R-336 and R-337 filed |
| | #47 | R-10, one membership call per playlist and one folder lookup per folder | DONE on `relay/47`, 8 rows committed and unrun (R-329) |
| | #48 | R-11, the lead break helper and the watch driven through the database half | DONE on `relay/48`, 6 rows committed and unrun (R-329), two findings still open in the ledger |
| 10 | #25 | U25, vocal restamp and My Tags shells | DONE on `unit/u25-vocal-restamp-and-my-tags-shells` |
| 11 | | Phase F explanation, Phillip's and not a session's | |
| 12 | #29 | U29, cutover | Ready by dependencies, ATTENDED, not a session's to take |

**#38 is the one task in that run that did not verify itself.** It landed at
`d3fe927` with its whole pipeline complete, seven commits through the review
round, the mutation table, the record and the restart, and only the tracker
writes failed, so the record halted `partial_landing`. Repaired by hand on
2026-09-11: the issue was closed with a comment naming `d3fe927`, `relay/38` was
deleted, and `verify` then returned every check green. **Its record still reads
`halted` and always will**, because that manifest is finished and nothing will
start against it again. See the `verify` confirms section below before treating
that as a second repair.

**The board after this merge**: 61 units, 60 done, 1 ready, 0 blocked, once
main is pushed. The one ready is #29, attended and not a session's. METHOD
line 10 is done. Line 11 is Phillip's. Do not take #29.

**Phase E is complete with the U53 merge.** Line 7 is Phillip's, the explainer
over the range from `46d5a4c` to the U53 merge commit. A session does not run
it. Phase F's explainer is line 11, over the U59 merge and the residual
commits plus this one.

#78 and #79 are not in METHOD's list, which was serialized before they existed.
Each was taken as a relay task, which is Phillip placing it.

**#42, R-5 was a close**, read against the tree rather than assumed. Its
successor is R-335, which has no issue.

Residual issues carry the `residual` label. They are the queue after the units,
each done or closed back to the ledger. A2 is attended. **#81, R-322, is the
first of them to be worked and it is done**, which leaves the rest of that label
as the live list; run
`gh issue list --repo philgutowski/cratekit --label residual --state open` rather
than trusting a count written here. R-324 is closed on #80. R-327 has no
issue, which is the normal state for a residual: the ledger holds it until
somebody decides to act on it.

**Every unit in METHOD's serialized list is built except #29, and so
are #78 and #79.** What is left is Phillip's: the two explanations, #46 and
#39, and #29.

## Do this first

1. `CLAUDE.md`, then `docs/METHOD.md`. The pipeline section is the sequence and
   the do-not-touch section binds. Line 10 is done. Line 12 is #29, attended.
2. `board.py next`. It names #29 first by reach. Do not take it. There is no
   unit left that a session may take.
3. Grep `docs/solutions/` for the module you are about to touch. A unit that
   opens a destructive write reads the barren list entry before it names an
   `analysis_roots`; a worker that moves files reads the rename intent entry
   before it binds. Read R-277 before touching `analyze.vocals`.

## The branches

| branch | state |
|---|---|
| `relay/48` | R-11, the branch this record is on; delete after the merge |
| `relay/47` | R-10, merged to `main`; delete if it still exists |
| `relay/44` | R-7, merged to `main`; delete if it still exists |
| `relay/43` | R-6, merged to `main`; delete if it still exists |
| `relay/42` | R-5, merged to `main`; delete if it still exists |
| `relay/41` | R-4, merged to `main`; delete if it still exists |
| `relay/40` | R-3, merged to `main`; delete if it still exists |
| `relay/38` | R-1, merged to `main`; delete if it still exists |
| `relay/79` | U61, merged to `main`; delete if it still exists |
| `relay/78` | U60, merged to `main`; delete if it still exists |
| `relay/81` | R-322, merged to `main`; delete if it still exists |
| `relay/77` | U59, merged to `main`; delete if it still exists |
| `fix/conformance-3-and-soft-delete-reader` | LANDED into `relay/77` by merge. Still in `.worktrees/conformance`, untouched, and now redundant. Deleting it and the worktree is Phillip's call, not a session's, because the merge is not pushed yet |

## When a relay run is cut off mid unit

It has happened three times, all three on a usage limit, and the shape is worth
recognising. The endings differ:

- **The runner had already merged.** Its own verify then refuses to call the
  task landed, `halt_class: partial_landing`, and the tracker issue stays open.
  So `main` carries a unit whose review, table and record never happened. That
  was #72.
- **The runner had not merged.** The task branch holds the work and the tree is
  left dirty, `halt_class: unclean_exit`, and the run stops there whatever
  `on_halt.continue_past_task_halt` says. That was #75.

The state lives in `~/.relay/<run>/state.json`: `tasks.<n>.status`, `halt_class`,
`halt_message`, `findings`, and `transcript_path`. Read the task's last assistant
messages to learn which pipeline step it reached. Finish it on the task's own
branch, merge, and close the issue from there. **Do not re-run the unit from the
board as though nothing had landed.**

**`verify` needs the issue named as `#N`.** After a hand landing, `relay_cli.py
verify <manifest> <task>` reaches a landed verdict only when it can find the
link. It derives one from a default branch commit naming `#N` when the record
carries no `landing_ref`; when the record already carries one, as a
`partial_landing` record does, it instead wants a tracker COMMENT naming that
sha, and one comment is the whole repair. native-relay's own `docs/solutions/`
carries both halves.

**`verify` confirms, it does not promote.** `cmd_verify` computes the verdict,
prints the checks, and returns an exit code; it writes nothing to the record
(`cli.py:395`). A halted record stays halted, reading `partial_landing`, however
green the verdict is. Promotion happens at the NEXT run's startup, where
`startup_reverify` re-runs the full verdict on every halted record and promotes
the ones that now pass. So a repaired task whose manifest is finished keeps a
halted record forever, and that is cosmetic rather than a second repair to chase.
Measured on #38, 2026-09-11: every check green, `38: landed` printed, record
still `halted`.

## Standing decisions

- **The board is the BUILD, the ledger is the LEDGER.** Do not backfill.
- **Residual numbers are APPEND ONLY.** Take numbers above main's highest at
  branch time, and renumber the incoming branch's at the merge, never main's.
- **The pending register is empty.** Re-opening any countdown re-arms it.
- **CI does not run the suite.** A step in the workflow must be able to pass.
- **Use `scripts/mutate.py`**, cap 25 rows, author's table, gap recorded in one
  line. Run `git status --porcelain` after every return; R-256 says why. **Never
  run `git checkout` on a file while a fix is uncommitted**: this session reverted
  one of its own review fixes that way and had to re-apply it, which is METHOD's
  driver rule arriving by hand instead of through a driver.
- **A finding blocks only if its input is REACHABLE and you drove the producer.**
- **Re-pinning a population means naming what moved.** Difference the SETS
  against `main`'s own tree. A count that moved by the right amount is not a
  measurement of what moved, and U59 hit the sharper version: the soft delete
  reader pin went from two members to a DIFFERENT two, so the count did not move
  at all while both members did.
- **A guard that goes red at a merge is usually right and out of date.** Ask
  whether the RULE moved or the TREE did, and drive the answer. Weakening a stale
  guard to get green takes the rule with it. Four of them in U59, all four right.
- **The audit's exit code is a measurement, not a constant.** It exited 2 for
  R-324 until issue #25 was reopened and it exits 1 now for R-265, the `In
  review` card. Read what it printed rather than what a record predicted, and do
  not soften `contradictions()` either way. Softening it now fails tests, which
  is new: R-322 put seven of them behind that function.
- **A double belongs at the PRODUCER's boundary, not at the shape it produces.**
  Hand-build the payload the network returns and let the real derivation run over
  it. Hand-building the derived structure asserts what its author believes the
  producer makes. And making an input injectable moves the undriven path one
  frame UP, to the caller that supplies nothing, so write the row for the default
  branch too.
- **Never write a closing keyword next to an issue number in prose**, not even
  inside backticks and not even to quote one. GitHub reads the text and not the
  intent.
- **Explanations are batched per phase.** No explainer inside a unit.
- **Do not touch** U30's board state, U20, R-9, A1, A2, `.worktrees/conformance`.
  The worktree stays on that list even though its branch has landed, because
  removing it is a cleanup Phillip takes once the merge is pushed.
