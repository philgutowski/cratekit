# An independent fable review of nine landed opus cards

Written 2026-09-19 from an attended check on the Phase G Relay run. Nothing here
is a ledger entry yet. It is the raw material for ledger entries, kept so the
findings outlive the session that produced them.

## Why this exists

Thirty cards into the run, the four cards routed to fable had each reported ten
findings from the in session `/code-review`, and the twenty six opus cards had
reported between none and two. Cost per thousand output tokens was equal, 0.141
against 0.142, so the fable cards cost more only because they did more. To tell
"the fable cards were harder" from "fable reviews better", a fresh fable session
reviewed the merged diff of card 123, which its opus author had passed with two
findings. It returned ten. The same read only pass was then run over the whole
favourites path, cards 112 to 119, because that is the code the first attended
sitting on card 178 exercises against the live library and account.

The comparison changed three things at once, the model, the reviewer's
independence from the author, and an explicit high effort level. It does not say
which of the three did the work. Native Relay issue 27 asks for an independent
review stage per task on the strength of it.

## How to read the findings

Every finding was argued from `git diff` and `git show` alone. **None was driven
by its reviewer.** Two have been driven since, in the attended worktree against
disposable libraries, and they split one each way, so treat the rest as
candidates and drive each before it becomes an R-N entry.

- **Confirmed, card 112 finding 1.** With an empty `location_prefix_map`, a row
  recorded under another volume name protects nothing: the plan read
  `count 2, referenced 0` and the apply renamed the file the row names. The
  author's own config now carries a rule for the renamed drive, so the live
  library is covered. A fresh setup is not, R-372 is the same root cause, and
  the deletion pass refuses on an unmapped row where this verb proceeds.
- **Refuted on current main, card 117 finding 3.** A stub listing passed as
  `--export` refuses `intake-export-is-stub` with both files still in staging
  and no batch folder made. The refusal does arrive only after the gate has been
  answered, which is the smaller point in card 117 finding 6.

Line numbers are at each card's merge, not at current main. "Ledger" notes are
the reviewer's own text search of `docs/residual-findings.md` at the main of
that hour.


## Card 112, U67 name guard, merge `3e25d17`

**112.1** `src/cratekit/write/naming_cli.py` line 196. The guard fails open on rows whose recorded prefix is unmapped. With no matching rule, `_referenced` keys only the old volume spelling, no candidate matches, and the file is planned as a rename with no warning or count.

Scenario. R-372 measured this library at 9937 of 9937 rows under the drive's old volume name, and setup writes `location_prefix_map` empty. On a fresh setup `name apply` over the library root opens the database, matches nothing, reports `totals.referenced` as 0, and renames every imported file. That is the R-407 outcome U67 exists to prevent, and the missing database case refuses while this one proceeds. A rule whose source differs from the recorded volume only in case also lands here, because `_matches_anchored` is case sensitive and only the final key is casefolded. The deletion pass refuses on unmapped rows, this verb does not, and no test covers an unmapped row.

Ledger. Not recorded for `name apply`. R-372 records the empty prefix map for the My Tags plan only, and the R-407 closure note does not mention the unmapped case.

**112.2** `src/cratekit/core/cause.py` line 1499. `collection-unreadable` maps every failed read to `LIBRARY_UNREADABLE`, whose default remedy is `restore-from-snapshot`. An unmounted volume or missing database should exit as `LIBRARY_UNAVAILABLE`, and the wrap also drops the inner cause's scope and retryable flag.

Scenario. The library drive is unplugged, so the inner cause is `library-directory-missing` or `library-database-missing`, which exits as `LIBRARY_UNAVAILABLE` with scope SESSION. `name apply` exits 25 with scope RUN instead. `test_a_missing_database_refuses_and_renames_nothing` pins that code. A driver or Relay battery branching on the exit code treats a detached drive as a corrupt library.

Ledger. Partly. R-425 records the exit code fold for the cloud sync case only. The missing volume and missing database case, and the dropped scope and retryable, are not recorded.

**112.3** `src/cratekit/write/naming_cli.py` line 190. Recorded paths are never link resolved, so a row recorded through a directory link does not match a candidate reached by its real path.

Scenario. The row records `<home>/Music/link/track.flac` where `link` points at `<library>/Tracks`, and the root is given as `<library>/Tracks`. The candidate's absolute and resolved spellings are both the real path, the recorded key is the link path, there is no match, and the file is renamed with its row stranded.

Ledger. Recorded as R-426.

**112.4** `src/cratekit/write/naming_cli.py` line 287. A file that becomes referenced after the plan is skipped with a silent `continue`. The envelope still returns the original plan, the original `totals.count`, and outcome OK.

Scenario. The second read finds a new row for a file planned as a rename. The rename is skipped, the output still lists it as a rename, counts it in `totals.count`, and exits ok. It is the same shape R-172 records for the `claim_target` skip, with a new cause added to the same silent branch.

Ledger. Partly. R-172 records the silent skip for target collisions. The new referenced skip is not named.

**112.5** `src/cratekit/write/naming_cli.py` line 284. The second collection read covers a window that does not exist in process. `gate.require` never blocks, it raises `DecisionRequired` and the process exits, so the wait on a person happens between invocations.

Scenario. Every apply does two database opens, two canaries, two schema checks, and two full ORM loads of about 9937 rows, milliseconds apart in one process. The re-invocation already rebuilds the plan, and `DecisionStale` compares its digest. The real exposure is during the rename loop, which can run for minutes, and the read before the loop does not cover it. `test_a_row_that_appears_after_the_gate_still_protects_its_file` drives the second read with a stub iterator, a sequence production cannot produce, and the code comment at line 281 states a wait that does not occur.

Ledger. Not recorded.

**112.6** `src/cratekit/write/naming_cli.py` line 136. `_recorded` materializes full `DjmdContent` ORM rows to read one column, and the read happens only after the whole tree walk.

Scenario. `handle.get_content()` hydrates every column of every row, twice per apply, where a single column query of `FolderPath` would do. The read runs after `_plan_for` has opened tags on every audio file under the root, which R-169 already calls the slow case. An unmounted or cloud synced database is therefore refused only after minutes of tag reads.

Ledger. Not recorded. R-169 covers repeated file opens, not the collection read or its ordering.

**112.7** `src/cratekit/write/naming_cli.py` line 174. `_referenced` and `_key` are a second private locate. The decode then resolve step duplicates `write/trees._comparable`, which the `RowIndex` docstring in `write/routing_pass.py` names as the single locate.

Scenario. `trees.index_active_rows` and `_comparable` already decode and resolve a recorded path. The `RowIndex` docstring warns that a second normalization is a second locate, and that two locates eventually disagree about which row they mean. The new copy differs by casefolding and by keying the unresolved spelling as well. `name apply` and the membership and routing writers can now disagree about whether a row names a file, and a fix to one will not reach the other. The fix is to lift one keyed locate into trees or locations, with options for tombstones and casefolding.

Ledger. Not recorded. R-280 records other duplicated decode sites and template builders, not this one.

**112.8** `src/cratekit/write/naming_cli.py` line 272. The root still defaults to the library root, where the guard now holds back essentially every file, so the default invocation is a slow no-op.

Scenario. A bare `crate name apply` reads tags across the whole library, then emits a plan of roughly ten thousand `referenced` items with a count near zero, and still asks for a confirm. The rekordbox Name half of the padding convention remains uncalled (R-165). The guard was added at the rename site without moving the verb's default scope to where a rename is legal, such as staging. The alternative is to re-point the row in a guarded session, the second branch of R-407's closing condition.

Ledger. Not recorded. R-407 was closed on its first branch, and the closure note does not say the default root is now inert.


## Card 113, U68 list document emitter, merge `4ec9983`

**113.1** `src/cratekit/acquire/listdoc.py` line 142. _reads_back compares only version_key, so a row that declared its version can be written in the embedded spelling and re-read with an other_reading the source row ruled out.

Scenario. A provider row has title 'Sun Path - Live' and version 'Extended Mix'. The reader sets other_reading to None because a declared version leaves nothing ambiguous, and spelled becomes 'Sun Path - Live (Extended Mix)'. _spellings offers (spelled, '') first. It re-reads to version_key 'extended mix', so it wins, and the document carries the combined title with no version field. read_list then runs split_ambiguous on that title and returns other_reading = ('Sun Path', 'Live Extended Mix'). The written list now asks a reading-unsettled question, or offers a library record 'Sun Path (Live Extended Mix)', where the source listing had one reading. No test covers a declared version row where the first spelling wins. Compare other_reading as well as version_key, or drop the comparison that mutation rows W3 and W5 showed to be unmeasured. Ledger at main: NOT recorded. R-428 covers the frozen mapping only, and main's _reads_back is unchanged.

**113.2** `src/cratekit/acquire/listdoc.py` line 376. A manifest left behind by a crash between the two writes blocks every later write of that name whose content differs at all.

Scenario. write() puts the manifest down first. The list write then fails, for example on ENOSPC or a kill. The playlist gains one track before the retry. _unchanged(manifest_path) sees different bytes and refuses with 'already exists and holds something else', over a list that was never written. The docstring's promise that the next identical write completes the pair holds only for byte identical input. The refusal names the manifest and never says the list is absent. Ledger at main: PARTLY recorded. R-476 records the whole file comparison refusing a repeat run. The orphan manifest shape is not recorded.

**113.3** `src/cratekit/acquire/listdoc.py` line 303. Provenance is looked up by the stripped id while document() applies first occurrence wins to the rows, so a caller's mapping can disagree with the emitter on both rules.

Scenario. (a) Row(ref=' 101 ') with provenance {' 101 ': P}. document() lists '101', provenance.get('101') returns None, and the write refuses 'no provenance was given for listed id 101' even though the caller supplied it. (b) The same id arrives from two sources and the caller builds {row.ref: prov for ...}, which is last wins. The manifest entry then pairs the first occurrence's artist and title with the last occurrence's source and release. The callers at main, approved_cli._provenance and missing_cli, each copy the strip and first-wins rule by hand to avoid this. Altitude fix: carry Provenance on the Row, or pass (Row, Provenance) pairs, so the emitter applies both rules once. Ledger at main: NOT recorded. R-451 records the duplicated reporting tail, not this.

**113.4** `src/cratekit/acquire/listdoc.py` line 264. _checked runs before the duplicate id check, so a broken repeat of an id already listed refuses the whole list even though that row would never be written.

Scenario. The rows are (Row('101', 'Aurora Bloom', 'Sun Path'), Row('101', '', 'Sun Path')). The second row would be dropped as a duplicate and the written document would be fully readable. The write still raises ListDocRefused at position 2, 'would make the whole list unreadable', which is false for the document it would have produced. Move the `if ref in seen: continue` check above _track and _checked. Ledger at main: NOT recorded.

**113.5** `src/cratekit/acquire/listdoc.py` line 282. _encoded can raise UnicodeEncodeError or TypeError, neither of which is ListDocRefused, so a verb catching only ListDocRefused reports an internal error.

Scenario. A provider title holds a lone surrogate, which json.loads produces from '\ud83d'. match.read_row accepts it, so _checked passes. json.dumps with ensure_ascii=False keeps it, and .encode('utf-8') raises UnicodeEncodeError. A Provenance.year that is not an int, or a Provenance value that cannot be serialized, raises TypeError from json.dumps the same way. Nothing is written, but the caller sees an unconverted exception and not a refusal by position. Ledger at main: NOT recorded. R-452 records only the OSError from the write.

**113.6** `src/cratekit/acquire/listdoc.py` line 383. An OSError from atomic_write_bytes escapes write() unconverted, though _unchanged converts read failures.

Scenario. A full disk, or a directory the write cannot create, raises OSError out of write(). It can happen after the manifest is already on disk, and a caller catching ListDocRefused tells the person to report a defect. Ledger at main: RECORDED as R-452. That entry is scoped to `intake missing`, and the label verb converts it on its own. The emitter still converts nothing.

**113.7** `src/cratekit/acquire/listdoc.py` line 173. Each Wanted row goes through match.read_row up to three times, and rows from another service get the spelling search before being unlisted.

Scenario. _row_of_wanted calls _reads_back once or twice per row, and document() calls _checked again on the same track. A row whose origin is not tidal runs the whole spelling search and is then sent to unlisted with no ref, so that work is wasted. The cost is small per row. The cheaper form returns early for non provider rows, and lets the successful _reads_back stand in for _checked on Wanted sourced rows. Ledger at main: NOT recorded. R-451 notes callers building the document twice, which is a different duplication.


## Card 114, U69 intake missing over a job, merge `ab4998e`

**114.1** `src/cratekit/intake/missing_cli.py` line 241. The offered check says offered tracks are "not listed until answered", but the verb only reads committed reports whose state is fixed when the job ran, so answering the review never makes them listable.

Scenario. A playlist job ends with 3 tracks offered. The person runs crate review list and answers all three as not owned. They then rerun crate intake missing on the same job. intake.cli.handle wrote each report's state once, and jobs.retry refuses a SUCCEEDED job, so nothing can update the reports. The rerun still counts 3 offered, produces the same list, and the three tracks never reach acquire download unless the whole playlist is queued again. The message promises a path that does not exist. Ledger: NOT recorded at main. R-449 only notes in passing that the job's reports do not change. main still carries this wording at lines 674 and 989.

**114.2** `src/cratekit/intake/missing_cli.py` line 224. The list comes from a point in time snapshot with no age or ownership recheck, and acquire download does not check the library either, so a rerun hands out a download command for tracks already acquired or since deleted on purpose.

Scenario. The person runs intake missing and then acquire download, and 40 tracks land. Days later they run intake missing on the same job again. The bytes are identical, so listdoc.write is a no-op. The verb still returns Outcome.OK and says "40 missing track(s) written ... next: crate acquire download ...". acquire_download queues every id in the file without asking the library, so all 40 are fetched again. A track tombstoned after the intake is listed the same way, which is exactly what the module docstring says it will not do. Ledger: NOT recorded for this verb. R-431 covers only tombstones the consult cannot reach at intake time. R-449 says intake missing is not the same shape and sets it aside.

**114.3** `src/cratekit/intake/missing_cli.py` line 103. A failed or cancelled job is told to "queue the playlist again", although crate job resume re-arms only the failed items, and the playlist wording is also used for intake.set jobs.

Scenario. An intake.set job fails on 1 of 60 items after a paid identification run. intake missing refuses with the step "queue the playlist again, let it finish, then list that job". For a set that means identifying the recording again and spending the recognition calls again. crate job resume JOB calls jobs.retry, which flips only the failed and claimed items back to pending and keeps the 59 done reports. The same "queue the playlist again" text appears at lines 128, 139 and 150 for set jobs that have no playlist. Ledger: NOT recorded. R-390 is about job resume ignoring retryable, a different defect. main still has it at lines 221, 245, 256 and 267.

**114.4** `src/cratekit/intake/missing_cli.py` line 271. A list that leaves missing tracks out still returns Outcome.OK and exit 0. The only signal is a "fail" check row, so a script or agent reading the exit code or outcome takes a partial list as complete.

Scenario. A job has 5 missing rows and 1 of them cannot be listed, because it has no provider ref or is not a Tidal row. listed is 4 and unlisted is 1. The envelope outcome is ok and the exit code is 0. test_a_missing_row_from_no_provider_is_reported_unlisted_as_a_failing_check pins ExitCode.OK for this case. A driver that gates on the exit code runs the printed download command and reports the playlist done with one track dropped. The file's docstring names this very defect: "A PARTIAL LIST THAT READS AS COMPLETE". doctor returns Outcome.FAILED when a check fails, and this verb does not. Ledger: NOT recorded. main keeps it as "Outcome.OK if listed or unlisted" at line 733.

**114.5** `src/cratekit/intake/missing_cli.py` line 194. Only ListDocRefused is caught around listdoc.write, so an OSError from the mkdir or the atomic write reaches the CLI boundary as internal-error with a report a defect remedy.

Scenario. The person passes --out notes.txt/lists where notes.txt is a file. out.exists() is False, so _out_dir lets it through. config._mkdir_private then raises NotADirectoryError inside atomic_write_bytes. The except Exception at the boundary in cli/__init__.py turns that into internal-error and tells the person to report a defect. A full disk (ENOSPC) or a read only volume does the same. Ledger: RECORDED at main as R-452, driven in label approved but not in this verb. The path under a file variant is not named there, but it is the same class.

**114.6** `src/cratekit/intake/missing_cli.py` line 202. Every ListDocRefused gets the step "move the file aside or name another folder with --out", which is wrong when the refusal is a row the reader would reject or a list name the emitter will not write.

Scenario. A missing report's frozen track thaws to an empty or version only title. That happens with a damaged report, or a job frozen before "spelled" existed whose fallback title and version do not read back. listdoc._checked raises "row 3 would make the whole list unreadable". The person is told to move a file aside or pick another folder. No file is involved, another folder fails the same way, and the refusal never names the item id. The position counts among missing rows, not job items, so it points at nothing the person can look up. Ledger: NOT recorded. R-451 notes that each verb holds its own ListDocRefused translation, but not that the step is wrong.

**114.7** `src/cratekit/intake/missing_cli.py` line 47. PROVENANCE_SOURCE is keyed on handler_key, so a hearts job, which runs under intake.playlist, is recorded in the manifest as source "playlist", and the vocabulary drifts from the "playlists", "labels" and "favorites" sources the emitter's own tests use.

Scenario. The person runs intake playlist favorites and then intake missing. Every manifest row says source "playlist" with source_ref "favorites". The sidecar exists to answer "why is this in the list", and its answer is that a hearted track came from a playlist. A future manifest reader keyed on the sync source names will match neither "playlist", which is singular, nor find any favorites rows. intake.cli already stamps FAVORITES_SOURCE_ID on the job, and is_favorites(source_ref) would tell the two kinds of job apart. Ledger: NOT recorded. main line 99 is unchanged.

**114.8** `src/cratekit/intake/missing_cli.py` line 146. The membership test report.get("state") not in _WORDS raises TypeError when a damaged report carries an unhashable state such as a list or a dict, so the damaged report case this loop exists to refuse ends as an internal error.

Scenario. A report file is hand edited or corrupted to {"state": ["missing"], ...}. It still parses as a dict with the right item_id, so it passes the identifier comparison. ["missing"] in frozenset(...) then raises TypeError: unhashable type. The boundary reports internal-error and report a defect, when the intended result is intake-list-unusable naming the item. An isinstance(state, str) guard closes it. Ledger: NOT recorded.

**114.9** `src/cratekit/intake/missing_cli.py` line 112. Altitude: the verb rebuilds report completeness by identifier to work around artifacts.committed silently skipping unparseable reports, while intake.cli._summary reads the same function with no such check and still reports short counts as if complete.

Scenario. One report file of a finished job cannot be read. intake missing refuses correctly. intake playlist --job and the job summary still print owned, offered and missing counts that add up to one less than the item total, with no warning, because _summary trusts committed(). The fix belongs in committed(): return the ordinals it skipped, or give it a strict mode. Then every reader gets the guarantee and the identifier comparison here is not a special case in one verb. Ledger: NOT recorded, as far as a search for the skip behaviour found.

**114.10** `src/cratekit/intake/missing_cli.py` line 88. Reuse: _finished_or_refuse copies the foreign job refusal from intake.cli._resume nearly word for word, _unusable is a second copy of intake.cli._unusable, _WORDS restates _STATE_WORDS.values() by hand, and the module reaches into the private intake_cli._load.

Scenario. A third intake handler key, or a fifth state word, added in intake/cli.py has to be found again here. If _WORDS falls behind _STATE_WORDS, every job holding the new state becomes unlistable with a "does not say whether the track is missing" refusal. The job-unknown wording now lives in two places that will drift apart. Deriving _WORDS from frozenset(intake_cli._STATE_WORDS.values()), and lifting one intake_job_or_refuse(job, origin) into intake.cli, removes the copies. Ledger: NOT recorded. R-451 records a different duplication, the reporting tail shared with label approved.


## Card 115, U70 favourites in, merge `2998f80`

**115.1** `src/cratekit/intake/cli.py` line 572. One unreadable heart refuses the whole hearts listing on every run, and the refusal tells the person to fix a playlist they cannot edit.

Scenario. An account has 1,400 hearts, and one row has no provider id or no artist (a delisted track with stub metadata). `frozen_rows` or `match.read_tidal_tracks` refuses the whole listing as `intake-list-unusable`. The step says 'fetch the playlist again so every row carries its id' and names a position in a newest-first listing the person cannot see or edit. Every later `crate intake playlist favorites` refuses the same way, so the inbound hearts feature is dead for that account until the heart is found and removed by hand. A playlist can be edited, hearts by position cannot, and the unit took on the all-or-nothing rule without a skip or report path.

Ledger. Partially. R-430 records that the refusal undercounts blank-id hearts and says 'in this playlist'. It does not record that the refusal is permanent, that the remedy cannot be acted on, or the no-artist path.

**115.2** `src/cratekit/label/tidal_catalogue.py` line 470. `favourite_tracks` claims 'this read is complete or it raises', but the provider leaves unservable hearts out of every page, so the result can be silently short.

Scenario. `listing.favorite_tracks` ends on `get_tracks_count`, which counts tracks the provider will not serve, and the pages omit them (the R-383 mechanism). An account declares 197 hearts and 12 are unservable. 185 rows come back with no error, the job reports owned, offered and missing over 185, and the 12 never appear as missing or anything else. The `Catalogue.favourite_tracks` contract ('a short listing would report hearts the library lacks as absent from the account, so no page shape may end it early') is violated by construction. `docs/GUIDE.md` repeats the promise. Nothing compares `len(rows)` with the declared total or warns.

Ledger. Partially. R-383 and its follow-ups record that the provider omits unservable tracks while counting them. No entry records that U70's seam contract and guide promise completeness while the verb silently drops those hearts. R-423 only says the live count against 197 is owed to an attended sitting.

**115.3** `src/cratekit/label/cli.py` line 610. A client with no logged-in account is reported as `label-playlist-unreadable`, with a 'retry' step that can never succeed.

Scenario. `TidalCatalogue.favourite_tracks` raises a plain `LookupError` when `session.user` or `.favorites` is missing. `favourite_tracks_or_refuse` catches every non-Cratekit exception and refuses `label-playlist-unreadable` (exit code `UPSTREAM_UNAVAILABLE`) with the step 'retry once the provider can list this account's favourites', and detail `playlist: favorites`. The real cause is an account or login problem, which the codebase spells `credential-missing` with `REAUTHENTICATE_PROVIDER`. The person retries indefinitely against a session that needs a login. The tests pin only that a `LookupError` is raised, not what the person is told.

Ledger. No.

**115.4** `src/cratekit/intake/cli.py` line 548. `FAVORITES_SOURCE_ID = 'favorites'` is the same value `favorites/cli.py` already stamps on the outbound `sync.favorites` job.

Scenario. The inbound hearts listing (handler `intake.playlist`) and the outbound heart sweep (`sync.favorites`) both carry `source_id` 'favorites'. The constant's comment says it lets 'a later reader tell the job that listed the account's hearts', which only holds if the reader also filters on handler key. A reader that selects by `source_id` alone, as `sync.playlists.source_jobs` would without its handler clause, treats the two directions as one source.

Ledger. Yes, R-429, in full. U74 has since queued hearts from `sync all` under the same value (the R-423 closing note), so the exposure R-429 predicted now exists on `main`. I did not check whether U74's reader filters on handler key, since it is outside this range.

**115.5** `src/cratekit/intake/cli.py` line 553. The reserved word matches only the American spelling, while the product's own messages to the person say 'favourites'.

Scenario. A refusal reads 'the account's favourites could not be listed', and the guide and CONCEPTS prose use 'favourites'. The person types `crate intake playlist favourites`. `is_favorites` is false, the word goes to `playlist_id`, and the person gets "'favourites' is not a playlist URL, a share link, or a playlist identifier", with no hint that the reserved word exists under another spelling. The parametrized test covers case and whitespace only.

Ledger. No.

**115.6** `src/cratekit/intake/cli.py` line 642. Every run queues a whole new job over all hearts, with no check for an open hearts job and no skip for hearts already resolved as owned.

Scenario. 'A re-run needs no cursor' is true for correctness. The cost is that each run on a 1,400-heart account pays a roughly 15-request listing, a 1,400-item job, 1,400 frozen rows in one payload, and 1,400 artifacts, even when two hearts changed. Running the verb twice before resuming leaves two open jobs over the same hearts, and a needs-review heart is asked about from both. U74 later added an open-job hold for the `sync all` pass, but the verb run by hand still has none.

Ledger. No. R-423's narrowing note records the no-cursor choice as a design decision, not its cost or the duplicate open jobs.

**115.7** `src/cratekit/label/cli.py` line 595. `favourite_tracks_or_refuse` is a copy of `playlist_tracks_or_refuse`'s error translation, and it leaves the documentation for the shared reason wrong.

Scenario. Both functions use the same pattern: try the listing, re-raise a CratekitError, and turn any other exception into `label-playlist-unreadable` with `detail={playlist, kind}`. A single helper taking the listing call, the message and the steps would give one place to change the boundary. The docstring at line 542 still says this reason is earned in 'ONE OF THE TWO PLACES' and means 'a BOUND provider was asked something about this playlist', but there are now three sites and one is not about a playlist. `sync.playlists.PER_PLAYLIST_REASONS` treats the reason as naming one playlist, and `detail.playlist` is now 'favorites' for hearts.

Ledger. No.

**115.8** `src/cratekit/intake/cli.py` line 572. The hearts case is wired into the shared `_playlist_rows`, so the public `list_playlist(found, 'favorites')` lists hearts for any caller.

Scenario. `list_playlist` is documented as 'one playlist's tracks' and is public because `sync.playlists` calls it per account playlist. It now returns the account's hearts when given the reserved string. `intake_playlist` has to recompute `is_favorites` at line 642 to set the `source_id`, because the lower layer gives no sign of which listing ran. A cleaner shape is a `list_hearts(found)` beside `list_playlist`, with the verb choosing once. That removes the second `is_favorites` call and keeps the shared seam's meaning unchanged for the sync caller.

Ledger. No.

**115.9** `src/cratekit/intake/cli.py` line 544. Two constants hold the same literal, and the flag is computed twice on the way to one listing.

Scenario. `FAVORITES` and `FAVORITES_SOURCE_ID` are both 'favorites' and both exported in `__all__`. `is_favorites(reference)` runs in `intake_playlist` and again in `_playlist_rows`. If one constant is renamed to fix R-429, the test asserts the literal 'favorites' for both payload fields and gives no signal about which one a reader depends on. One constant, or a constant derived from the other, plus a single dispatch, does the same job.

Ledger. No. R-429 covers the value collision with `sync.favorites`, not the duplication inside this module.

**115.10** `src/cratekit/intake/cli.py` line 569. A docstring uses a colon where a dash would go, which the repo's `CLAUDE.md` forbids.

Scenario. The repository's `CLAUDE.md`, Standing constraints, says: 'No em dashes, en dashes, or double hyphens in any prose, code comment, commit message, or issue body. Do not swap a dash for a colon; favor commas, and keep colons for a genuine list or definition.' The added docstring line is 'a heart the library lacks is not parked in a provider playlist: it is a missing item, queued with its provider identifier'. That colon joins two clauses and introduces neither a list nor a definition. The same pattern appears in `favourite_tracks_or_refuse`'s docstring ('and for the same reasons: a ``CratekitError`` passes through').

Ledger. No.


## Card 116, U71 landing engine, merge `6247e5c`

**116.1** `src/cratekit/intake/landing.py` line 384. A failure after the first move strands the moved files with no intake file, and the engine's own 'already owned' guard then refuses every attempt to land them again.

Scenario. A, B and C are staged. A moves, then os.replace on B raises ENAMETOOLONG, EIO or a uchg permission error, or place_files fails at line 406. apply raises. A sits in Music/<batch> with no COLLECTION row, no intake playlist and no routing intent. Landing Music/<batch> again hits _check_library line 192 ('inside the library ... already owned'), and no other verb splices files already in the library. The refusal names the files but no path gets them into rekordbox. A per file refusal for B that continues and still writes an intake file for what moved, as _occupied already does, would avoid it. Ledger: NOT recorded. R-413's narrowing states the behaviour as design, and R-456 covers only the later label rows.

**116.2** `src/cratekit/intake/landing.py` line 345. _check_export claims every refusal place_files can make is made before the moves, but several are never probed.

Scenario. The unprobed ones are writing destination (destination.parent.mkdir and write_bytes), session.open_session, and the routing ledger write. Take a destination whose parent is unwritable or on a read-only volume, or a state directory that open_session or record_intents cannot write. Every pre-move check passes and all N files move. place_files then raises at ingest.py lines 171, 225 or 231, and the except branch reports N files moved with no intake file. That is the stranding in finding 1 for the whole batch, from a condition one write probe before the first os.replace would catch. Ledger: NOT recorded.

**116.3** `src/cratekit/intake/landing.py` line 375. Only os.replace is inside the try, so an OSError from the second _occupied check mid-loop escapes raw without naming the files already moved.

Scenario. cause.access_refusal's docstring says Path.exists and is_dir re-raise under EPERM, the routine macOS state for an external volume without Full Disk Access. final.exists() raises on the second item after the first has moved. A bare PermissionError leaves apply with no detail['moved'], no _moved_sentence and no batch folder cleanup, breaking the module's promise that the refusal names the moved files. Before any move, target.mkdir at line 368 (target exists as a file, or a batch name exFAT rejects such as one holding ':' or '?', which _check_batch allows) and folder.iterdir also raise raw OSError instead of a refusal. Ledger: NOT recorded.

**116.4** `src/cratekit/intake/landing.py` line 418. The except branch rebuilds the place_files cause instead of extending it, so the origin trail and the inner remediation steps are dropped from the headline.

Scenario. place_files refuses with library-export-unusable carrying steps=('export the collection again from rekordbox ...') and origin ('intake.ingest',). landing calls refuse(exc.cause.reason, ..., origin=_ORIGIN, inner=inner) with no steps, so the outer remediation falls back to the exit code's generic remedy. The origin is the single element ('intake.landing',). Cause's own docstring in core/cause.py calls that 'a defect rather than a style choice' and provides Cause.at(boundary) for this hop. The person is shown the generic remedy instead of 'export again'. Ledger: NOT recorded. R-128 is the same shape at a different site.

**116.5** `src/cratekit/intake/landing.py` line 312. _reason_for is a narrower copy of cause.access_refusal, and it labels every non-permission OSError from a move as intake-list-unusable.

Scenario. os.replace raises EXDEV (a bind mount or firmlink that the st_dev probe read as equal), EIO or ENAMETOOLONG. The refusal reads intake-list-unusable, a precondition about the list, for a failure of the filesystem. An OSError with errno EACCES or EROFS that is not a PermissionError instance also gets the wrong slug until CratekitError.cause reclassifies it. core.cause.classified already does this centrally for every 'raise refuse(...) from exc', so the helper is redundant where it is right and wrong elsewhere. Ledger: NOT recorded. R-452 is the nearest, for intake missing.

**116.6** `src/cratekit/intake/landing.py` line 190. The staging and ownership tests compare resolved paths by exact case, and the target volumes (APFS by default, exFAT) are case-insensitive.

Scenario. Config holds download_staging '<volume>/Library/Downloads' and the person passes '<volume>/library/downloads'. os.path.realpath on macOS does not canonicalise case. in_staging is False while 'owned in source.parents' may or may not match. A staging folder inside the library is then refused as 'already owned'. In the other direction, the 'target is under staging' refusal at line 204 is bypassed and files land inside staging, which a later clean deletes. That is the 2026-06-29 flood shape the module exists to prevent. os.path.samefile or an st_dev and st_ino walk would be exact. ingest.assert_not_staging has the same weakness, so both move together. Ledger: NOT recorded for these sites.

**116.7** `src/cratekit/intake/landing.py` line 109. _digest stats each listed item with no guard, so a file removed between the listing and the stat raises a bare FileNotFoundError instead of decision-stale.

Scenario. A clean or a second landing removes One.flac after _list(plan.folder) at line 326 and before item.stat() inside _digest at line 327. A traceback reaches the person where 'changed after it was planned, so nothing was moved' was meant. The same can happen in plan(). Ledger: the shape is R-485 ('read one path twice with a window between'), but R-485 lists four other sites and not landing.py, so this instance is NOT recorded.

**116.8** `src/cratekit/intake/landing.py` line 258. Every landed file has its tags opened twice, and the export is read and spliced twice.

Scenario. _unplaceable opens each file with mutagen twice (genre, energy). place_files.read_meta then opens it six more times (artist, title, genre, initialkey, energy, inizio). _check_export reads the whole export into a bytearray and runs splice_tracks plus insert_intake_playlist, and place_files does the same again. On an exFAT spinning volume with a 50 MB export and a 200 file batch that roughly doubles the wall time. Cheaper: have place_files expose a validate-only pass, or accept precomputed meta, so one read serves both. Ledger: NOT recorded. R-459 is the neighbour, for the later label index re-read.

**116.9** `src/cratekit/intake/landing.py` line 90. The ACQUIRE_STAGING_DIRNAME clause in _listable is unreachable, and the constant is a hand copy of acquire/cli.py's that no test pins.

Scenario. The name starts with '.', so startswith('.') already returns False. It is also a directory with no audio suffix, so two later clauses reject it too. test_the_listing_is_flat_audio_only_and_skips_dotfiles cannot kill a mutant that deletes the clause, which means the test reads as covering unfinished downloads and covers nothing. The literal '.cratekit-acquire-staging' is duplicated from acquire/cli.py line 168 'rather than imported'. If acquire renames its directory to a name without a dot, landing keeps the old literal silently. Simpler: drop the clause and the constant and keep the dotfile rule, or add one test asserting the two constants are equal. Ledger: NOT recorded.

**116.10** `src/cratekit/intake/landing.py` line 393. apply carries two near-identical 'no file could land' refusal blocks, and plan takes a cfg it never reads.

Scenario. Lines 355 to 365 and 393 to 403 build the same reason, sentence and detail, and differ only in the batch folder cleanup. The next wording change has to be made twice, and the two will drift. One local helper taking the refused list would do. plan(folder, cfg, batch) accepts cfg and ignores it ('the verb's call shape'). A caller can therefore plan under one config and apply under another with nothing noticing, since Plan records neither root nor staging. Either drop the parameter or put the resolved target into Plan and the digest. U72's verb later added target to its own digest, which shows the engine level gap. Ledger: NOT recorded.


## Card 117, U72 intake land verb, merge `6615f8c`

**117.1** `src/cratekit/intake/land_cli.py` line 201. Every successful landing leaves an OPEN intake session (place_files never closes it) plus an _inboxed.xml at the library root, and both make tree_registry.assert_cutover_ready refuse. The only verb that closes that session, route pending, returns early while no tree is database native, which is every library before cutover.

Scenario. Run `crate intake land` once on a library that has not cut over. place_files opens a session and returns with it still OPEN. `route pending` sees no native tree and returns OK before _close_if_settled. The later cutover refuses with `cutover-open-run`, and again with `cutover-xml-pending` until the person hand-deletes the intake file, which no step in the pending action tells them to do. The verb meant to unblock cutover cannot run until cutover has happened. RESIDUALS: not recorded. R-433 records the open session but says 'an open intake record blocks nothing today' and that no reader of OPEN exists outside core/session.py. That is wrong, because assert_cutover_ready reads `not record.terminal`. R-436 covers only the verify_verb half.

**117.2** `src/cratekit/intake/land_cli.py` line 206. The rekordbox_import pending action goes only onto the printed envelope. Nothing assigns it to ctx.run.pending, and the dispatcher's gates.save(state) persists a run record with pending=None. The module and test docstrings say 'the pending action is the run's state, not advice', and it is not.

Scenario. Land a batch and close the terminal. `crate run show <id>` and doctor's run findings both read state.pending, and both show nothing awaiting import. A grep for `state.pending =` and `run.pending =` across src finds no writer. The unimported intake file is remembered only by the scrollback, which is the 'tool says something and forgets' shape the PendingHumanAction docstring says it replaces. session.mark_awaiting_import is not called either, so the intake session is OPEN rather than AWAITING_IMPORT. RESIDUALS: not recorded.

**117.3** `src/cratekit/intake/landing.py` line 215. _check_export claims to make 'every refusal place_files can make about the export' before any move, but it omits the is_stub_listing check, and session.open_session write failures are also missed. With the verb shipped, a stub passed as --export refuses after the files have already moved.

Scenario. `crate intake land --export <run>_synced.xml`. That file is a U22 stub listing, and it sits in staging right beside the batch. The gate is answered, _check_export passes, and every file is os.replace'd into Music/<batch>. Then place_files raises `intake-export-is-stub`. The files are now in the library with no intake file. `intake land` cannot be re-run over them, because _check_library refuses an in-library folder. The only recovery is `intake file` one track at a time. RESIDUALS: not recorded. R-413's narrowing asserts 'every export refusal place_files can make, tried on a copy'. R-456 records the analogous orphaning only for the label tree.

**117.4** `src/cratekit/intake/land_cli.py` line 184. folder and export go into the digest and the payload as the raw argv strings, never resolved. A relative FOLDER or --export therefore names a different place when the answered run is resumed from another working directory, and the digest still matches.

Scenario. `cd /a && crate intake land batch --export fresh.xml`, then decide, then `cd /b && crate --run ID intake land batch --export fresh.xml`, where /b/batch holds a cp -p copy with the same names, sizes and mtimes. The identity strings 'batch' and 'fresh.xml' are equal, so there is no decision-stale, and /b's files land against /b's export under an answer given for /a. This is exactly the case test_an_answer_given_for_one_folder_is_stale_for_another_holding_the_same_names claims to close. The items' from/to values are also relative, while entry.path comparisons depend on the same spelling. RESIDUALS: not recorded.

**117.5** `src/cratekit/intake/land_cli.py` line 99. The digest covers the export's path string but not its content, size or mtime. The answer stays valid when the Fresh Export at that path is replaced between the gate and the apply, even though the module docstring promises staleness if what was shown changed.

Scenario. The person answers the gate, then re-exports from rekordbox over the same fresh.xml, or an older file is copied over it, then resumes with --run. There is no decision-stale. The batch is spliced into a collection the person never confirmed against, and next_track_id is taken from the new file. The files in the folder are fingerprinted by size and mtime, and the export is not. RESIDUALS: not recorded. The U72 closing note says the digest 'covers the export' without saying it covers the path only.

**117.6** `src/cratekit/intake/land_cli.py` line 140. _planned short-circuits an empty folder before landing.plan runs, so _check_batch never sees the batch name. An unusable --name is then a gated no-op exiting OK when the folder is empty, and a refusal when it is not. The first run also validates nothing that can doom the batch (export missing, intake file already exists, folder inside the library), so a person is shown a gate for a plan that can only refuse.

Scenario. `crate intake land --name ../x --export e.xml` on empty staging. The gate screen shows 'lands in <root>/Music/../x' and 'intake file <root>/../x_inboxed.xml', then exits OK no_op. The same command with one file staged refuses intake-list-unusable. Separately, `--export no-such.xml` with files staged gives DECISION_REQUIRED, the person runs `run decide`, and only then sees library-export-unusable. RESIDUALS: not recorded. R-484 records the sibling shape for `sync mark` only.

**117.7** `src/cratekit/intake/landing.py` line 330. target.mkdir(parents=True) sits outside the try that maps OSError to a refusal, and the listing(folder) call in land_cli._planned has the same gap. A permission or filename error surfaces as the dispatcher's generic path, not as `path-permission-denied` with the landing's own sentence. default_name strips colons 'because a colon cannot be in a folder name on exFAT', but --name lets a colon through _check_batch.

Scenario. `crate intake land --name 'fri: set'` on a volume that rejects the character, or a read-only Music folder. mkdir raises a raw OSError after the gate was answered, so none of the 'nothing was moved' wording appears and the _moved_detail the engine builds for every other failure is absent. An unreadable staging folder raises from iterdir before the gate, the same way. RESIDUALS: not recorded for landing. R-452 records the same shape for `intake missing` only.

**117.8** `src/cratekit/cli/registry.py` line 1724. intake.land is declared destructive=True and its handler never enters session.assert_gates. There is no write lock, no backup acknowledgment and no volume identity check, so the conformance 6 properties asserted 'per destructive verb' are not properties of this verb. doctor_checks lists only library.mounted.

Scenario. Two `intake land` runs, or a land running during another destructive session, proceed concurrently because no lock is taken. That is R-432's window made wider. Land on a library whose volume identity does not match the recorded one and the files still move. RESIDUALS: partly recorded. The standing residual 'Conformance 4 and 6 drive the shared surface and not the landed verbs' and R-432 / issue #180 cover the missing lock. Neither names intake.land skipping the acknowledgment or the volume identity gate.

**117.9** `tests/test_cli_contract.py` line 1517. The sample-argument comment says the verb 'refuses from the vocabulary before its gate is reached'. The shipped behaviour is the opposite, and conformance 3 depends on that opposite: library/Music is an empty directory, so the verb reaches its gate and then exits OK as a plan of nothing.

Scenario. Someone 'fixes' _planned so an empty folder refuses, as the comment describes, and conformance 3 fails for intake.land with no hint why. Or a reader trusts the comment and believes conformance 1 and 2 exercise a refusal path, when they exercise the no-op path. The export path `no-such.xml` is never touched for the same reason, so the contract suite drives no export handling at all. RESIDUALS: not recorded. The U72 closing note describes the real behaviour and contradicts this comment.

**117.10** `src/cratekit/intake/land_cli.py` line 163. _pending hand-builds the rekordbox_import PendingHumanAction rather than calling core.session.pending_import, the existing builder for exactly this action. It is also keyed on the run id instead of the intake session place_files opened. The folder is listed three times per apply, in listing, plan and apply, and the tags and the whole export are each read twice, in _unplaceable / _check_export and again in place_files.

Scenario. Cost: there are two spellings of one pending action, so a change to session.pending_import does not reach landings. The pending id `pha_<run>` cannot be joined to the session `route pending --session` takes, because Landed does not carry the session id. For a large batch against a multi-megabyte Fresh Export, each apply parses the export twice and reads every file's tags twice. RESIDUALS: the duplicate reads are recorded for the label path only (R-459). The bypassed helper and the unjoinable id are not recorded. R-436 notes pending_import takes the verb as a parameter and does not note that the verb never calls it.


## Card 118, U73 intake missing over a run, merge `40ee647`

**118.1** `src/cratekit/intake/missing_cli.py` line 287. The second remedy on the failed-job refusal, queue again with sync all and list that run, produces a run that holds only the requeued playlist, so the original run's succeeded jobs never get listed, and the in-place remedy `crate job resume JOB` is never offered.

Scenario. Pass A queues P1 and P2. P1 succeeds with 10 missing tracks and P2 fails. `intake missing --run A` refuses, and the person follows step 2. `sync all` (run B) records P1 in the cursor as swept and requeues only P2. `intake missing --run B` lists P2 alone and reads as the whole pass. Run A keeps refusing unless `--skip-failed` is used, and the text never says that is still needed for P1. P1's 10 tracks are never downloaded, and no later sync offers P1 again (R-359). The same step text sits at line 398. `cli/jobs.py` `resume` calls `jobs.retry` on a failed or cancelled job and keeps it in run A, which is the only remedy that keeps one list, and it is not named. Ledger at main: not recorded. The R-403 closure describes the refusal but not this misdirection.

**118.2** `src/cratekit/intake/missing_cli.py` line 464. The run list has a fixed name, `<run>_synced`, but its contents change when a skipped job is later resumed, so the natural second listing is refused by listdoc's byte comparison.

Scenario. `intake missing --run A --skip-failed` writes `A_synced.list.json` from P1. The person runs `crate job resume` on failed P2 and it succeeds. `intake missing --run A` now builds P1 plus P2 under the same name. `listdoc._unchanged` raises already exists and holds something else, and the verb refuses with move the file aside. P2's tracks cannot be listed until the person moves away a file that may already be half downloaded. R-449 at main says `intake missing` is not this shape because a job's reports do not change, which stopped being true for `--run`. Ledger at main: not recorded for this cause. R-476 records the same fixed-name trap for a changed ISRC answer only.

**118.3** `src/cratekit/intake/missing_cli.py` line 357. Run counts are per report, not per track, so a track shared between playlists inflates `missing`, `owned`, `offered`, `suppressed` and `unlisted`, and no check explains the gap between `missing` and `written`.

Scenario. Two playlists share one missing track. The summary says missing 4, written 3, unlisted 0, and the unlisted check says every missing track is in the list. The unit's own test asserts `(written, missing) == (3, 4)`. To a person or a script this reads as one track silently dropped, the exact defect this file is shaped against. A shared track with no provider id also appears twice in `unlisted_tracks` and counts 2 in the failing check. Ledger at main: not recorded. R-430 covers two hearts folding into one, which is a different thing.

**118.4** `src/cratekit/acquire/listdoc.py` line 346. `source_refs` is written only when it has more than one entry, so a single entry that differs from `source_ref` is dropped.

Scenario. `_provenance` (missing_cli.py line 323) leaves a job with no source ref out of `every[ref]`. If the first job for an id has an empty `SOURCE` payload and the second is playlist pl-b, the entry gets `source_ref=None` and `source_refs=('pl-b',)`. The length is 1, so the key is not written, and the manifest says the track came from nowhere while pl-b is lost. The same happens to any caller passing `Provenance(source_ref='a', source_refs=('b',))`. The docstring's claim that an entry without the key came from its `source_ref` alone is then false. Comparing `source_refs` against `(source_ref,)` instead of the length fixes it and keeps old manifests byte identical. Ledger at main: not recorded.

**118.5** `src/cratekit/intake/missing_cli.py` line 495. The landing hint names the batch for the run, but `intake land` with no FOLDER lands the whole download staging folder, so the `<run>_synced` batch can hold files from other runs or other lists.

Scenario. A person downloads run A's list and an earlier `--job` list, or run B's, before landing anything. They paste `crate intake land --export XML --name A_synced`. `build_land` defaults `folder` to download staging, so every audio file there lands under `A_synced`. Later work keyed on that name treats run B's tracks as run A's, and run B's own landing finds an empty folder. The default `lists/` folder also sits inside staging. The hint skips `tag folder` and `name apply`, which land_cli's own docstring places between download and landing. Ledger at main: not recorded. R-484 covers a mistyped name only.

**118.6** `src/cratekit/sync/cli.py` line 29. The docs say the run list holds every missing track of the pass, but the selection takes intake jobs only, so labels and favourites jobs under the same run are ignored even while open.

Scenario. A full profile pass queues `sync.labels`, `sync.favorites` and `intake.playlist` jobs under one run. `intake missing --run RUN` succeeds while the labels job is still open or has failed. `test_a_job_of_another_verb_in_the_same_run_is_not_listed` pins that. The missing_cli docstring rule that one open job refuses the whole run holds for intake jobs only. A person told the pass downloads and lands as one batch lands `<run>_synced` while the labels half is unresolved, and its list arrives separately from `label approved`. The check text at line 367 is scoped correctly to the N intake jobs, so the overclaim is in the two docstrings and the R-403 closure. Ledger at main: not recorded as a gap. The later U74 closure moves the hearts job under `intake.playlist`, which narrows this to labels.

**118.7** `src/cratekit/intake/missing_cli.py` line 90. The subcommand flag `--run` uses the same spelling as the dispatcher's global `--run` and takes an identifier from the same namespace, with a different meaning depending on its position.

Scenario. `crate intake missing --run X` lists a pass. `crate --run X intake missing` hits argparse's required-group usage error, exit 2, with no structured refusal. `crate --run X intake missing --run X` reaches `gates.load(X)` and refuses `decision-unknown-gate`, saying the run belongs to `sync.all`, not to `intake.missing`. The remedy there is to answer a decision, and no decision exists. The `dest=sync_run` workaround and its comment show the collision was already met in the first build. Favourites and label already spell a shared intake run as `--run-id` with `dest=run_id`, which would have avoided it. Ledger at main: not recorded. `u73-notes.md` mentions the dest collision only as a dropped mutation row.

**118.8** `src/cratekit/intake/missing_cli.py` line 247. Run selection reads every job in the installation's queue and JSON-decodes every payload, each holding a frozen track mapping, then filters in Python.

Scenario. `jobs.list_jobs(store)` runs `SELECT *` with no `WHERE`. After months of passes, every `intake missing --run` parses thousands of whole playlist payloads to find two or three jobs. `handler_key` and `library_id` are columns, so a `WHERE` on those two leaves only the run comparison to Python. `sync/playlists.source_jobs` has the same shape, so a shared filtered query would serve both. Ledger at main: not recorded. R-438 and R-448 are different repeated reads.

**118.9** `src/cratekit/intake/missing_cli.py` line 413. `_listed` works out whether it is listing a run or a job by checking for a `run_id` key in the `subject` dict, and that same dict is spread into refusal details and the summary.

Scenario. The noun in nothing listed: no track in this run/job is missing comes from `'run' if 'run_id' in subject`. `_listed` already takes seven parameters (`subject`, `checks`, `after`, `left_out` and more) to serve two callers. A third caller whose subject carries the run for reference, such as a job listing that reports its run, flips the wording with no error. `**subject` into `_unusable(**detail)` raises `TypeError` the day a subject key is named `out`, `failed` or `unlisted_tracks`. A small subject value holding the noun and the detail dict removes both. Ledger at main: not recorded. R-451 covers the duplicated reporting tail between `label approved` and `intake missing`.


## Card 119, U74 favourites sync, merge `c24712e`

**119.1** `src/cratekit/sync/cli.py` line 493. The in-flight check says the open hearts job is resumed, but `crate sync all` resumes nothing and the row names no resume command. A hearts job left QUEUED blocks every later pass from listing hearts. LEDGER: not recorded. R-361 only notes in passing that sync-queued jobs were left queued and unresumed; R-423's closing note says an open hearts job holds the next pass, as intended behaviour.

Scenario. Pass 1 queues hearts job J. The module doc says the verb declares no argv_builder and has nothing to resume, so no worker drives J. Hearts added to the account later never reach the library. Every later pass takes the IN_FLIGHT branch and prints an info row with remedy None, naming J and claiming it is resumed. `_is_open()` is any non-terminal state, so a BLOCKED job holds the hearts the same way. The person is never told to run `crate intake playlist favorites --job J` or to cancel it.

**119.2** `src/cratekit/sync/cli.py` line 577. The read half is still dropped whenever `ask` raises. The read is queued only after the write's gate returns, so the header's "a read needs no consent" does not hold. LEDGER: not recorded. R-423's closing note claims "whatever the outbound confirmation's answer" and says nothing about an unanswered or refused gate.

Scenario. `ctx.gate.require` can raise DecisionRequired, DecisionStale or UnknownOption, and `hand_off` can raise internal-error. Each leaves `compose` before the ready loop, so `inbound.queue` never runs. Case 1: favourites enabled and an export present, a bare or unattended `crate sync all` always exits DECISION_REQUIRED and the hearts are never listed into the library. `test_the_gate_refusal_queues_no_hearts_listing_either` pins this. Case 2: the person answers, rekordbox re-exports, `--run` resumes, DecisionStale is raised, and the read is dropped with the write. The unit removed this failure shape for abort and missing export only.

**119.3** `src/cratekit/sync/cli.py` line 230. The hearts in-flight check and the enqueue are separate store transactions, and the hearts listing, the labels planner and the whole playlists planner run between them. LEDGER: not recorded for hearts. R-363 records the same race for playlists only.

Scenario. Favourites is planned first. `_plan_inbound` closes the store and lists the hearts over the network. The labels planner then runs, and the playlists planner lists every new account playlist track by track (599 playlists were seen live). Only after that does `compose` reopen the store and enqueue. A `crate intake playlist favorites` by hand, or a second `sync all`, inside that window of minutes gives two open hearts jobs for one library. The by-hand verb makes no in-flight check at all, so the guard is also one-directional.

**119.4** `src/cratekit/sync/cli.py` line 506. `summary.sources` now lists `favorites` as queued when only its read half was filed, while `summary.not_queued` lists `favorites` as declined or `outbound-export-required` in the same report. LEDGER: not recorded.

Scenario. On abort with hearts queued, `queued = [p for p in plans if _filed(p)]` includes favourites. The report then holds `sources == ["favorites"]` and `not_queued["favorites"] == "declined"` together. `test_an_abort_still_queues...` asserts the not_queued side, and `test_a_confirmed_pass_queues_both_halves` asserts the sources side. A machine reader taking `sources` to mean the outbound sweep was queued is wrong. The jobs row carries only `source: favorites`, so the two halves are told apart by handler_key alone, which is R-429's conflation surfaced in the report.

**119.5** `src/cratekit/sync/cli.py` line 271. The hearts are listed from the provider at plan time on every invocation, including the run that only raises DecisionRequired, so each answered pass pays for the full paginated listing twice. LEDGER: not recorded. R-438 covers the double catalogue open inside one pass, not the double listing across the gate.

Scenario. Run 1 lists about 197 hearts, builds `_awaiting`, raises DecisionRequired and discards the listing. Run 2 with `--run` lists them all again before queueing. The first listing feeds only one boolean, `queued_whatever_the_answer`, plus `not_queued`. That boolean is a promise run 2 can break, because its own listing may fail or a job may have opened in between. Cheaper form: on the asking run do only the local in-flight check and the catalogue resolve, and list when the queue is about to run.

**119.6** `src/cratekit/sync/cli.py` line 207. `_hearts_jobs` loads and JSON-parses every job row of every state and library, then keeps only the open ones, although `jobs.list_jobs` already takes a `states=` filter. LEDGER: not recorded.

Scenario. Each hearts or playlist job payload holds its whole frozen track map. The live queue already had 18 playlist jobs with about 1600 tracks. Every `sync all` deserialises all of them, terminal ones included and growing without bound, to answer whether an open hearts job exists. `playlists.source_jobs` needs terminal jobs for its cursor, this caller does not. Pass the open states to `list_jobs`.

**119.7** `src/cratekit/sync/cli.py` line 195. `_hearts_jobs` is a copy of `sync.playlists.source_jobs` with one constant changed. It has the same three-field filter, docstring reasoning and return shape. LEDGER: not recorded. R-364 notes the playlists key filter is kept as defence.

Scenario. Two copies of the "jobs this source owns for this library" rule will drift. One example is a change to how `library_id` is compared when `volume_id` is None. `playlists.source_jobs` with a `source_id` keyword defaulting to SOURCE_ID serves both callers. The favourites planner already imports `cratekit.sync.playlists` for `Excluded`.

**119.8** `src/cratekit/sync/cli.py` line 122. `_Inbound` re-declares `_Plan`'s queue, filed, refused and not_queued fields, and the composer needs a special case at six sites to carry it. LEDGER: not recorded. The sources docstring gives the reason, that PLANNERS is pinned to SPECS, but does not weigh the cost.

Scenario. The six sites are `_filed()`, the three-tuple ready list typed `_Plan | _Inbound`, the refused comprehension, a second warnings block, a second checks loop with its own `_inbound_check`, and the detail merge in `_report`. Any new composer feature must remember both shapes. `_next_step` already had to be patched for this. A planner returning a list of `_Plan`, or a second plan with its own check key, would remove every special case. The next source with a read half repeats all six.

**119.9** `src/cratekit/sync/cli.py` line 238. `_inbound_check` words every plan-time refusal as "the account's hearts were not listed", including a job store failure that happens before any listing is attempted. LEDGER: not recorded.

Scenario. `jobs.open_store()` sits inside the same try as the listing. A locked or unreadable job store raises CratekitError there. `inbound.hearts` stays None, so the fail row reads as a provider listing fault and carries the store's remedy. The code comment on the listed-then-refused branch says it exists to keep exactly this kind of wording from sending a person to the wrong place.

**119.10** `src/cratekit/sync/cli.py` line 238. The hearts half opens its own provider catalogue with `catalogue.resolve(cfg)`, and the playlists planner opens a second one in the same pass. LEDGER: recorded as R-438, filed by this unit, open.

Scenario. A full-profile pass opens two provider sessions where one would serve. This doubles the chance that a transient provider fault refuses one of the two sources. R-438 closes when one pass resolves the catalogue once and hands it to every planner.


## Card 123, U78 set tracks named by ISRC, merge `15b8de8`

**123.1** `src/cratekit/intake/missing_cli.py` line 293. One missing row with a well formed ISRC now makes the whole verb depend on a live provider login, so a missing or rejected session withholds every row, including playlist rows that already carry ids and rows that need no lookup at all.

Scenario. A set job has 10 missing rows: 9 with no ISRC and 1 with an ISRC, and no provider session is stored, which is normal because intake set does not need one. catalogue.resolve refuses credential-missing, so nothing is written. The 9 rows that could have gone to the unlisted text list with no provider call are withheld. In a mixed --run the playlist rows with ids are withheld too, where before U78 they were listed.

**123.2** `src/cratekit/label/tidal_catalogue.py` line 642. A well formed ISRC the provider permanently rejects sleeps the full 31 second retry ladder and then refuses the whole listing, on every run, with the remedy retry later (recorded as R-479, still shipped).

Scenario. A recognised track carries an ISRC of the right 12 character shape that Tidal answers 400 to. tidalapi raises InvalidISRC, the ladder sleeps 1+2+4+8+16 seconds, and the verb refuses unavailable-transient. Every repeat run does the same, so one bad row blocks every other track of the set from ever being listed. The only way out is editing the job's report by hand. A per-code cap (hand the row on as unanswerable after the ladder) would localise it.

**123.3** `src/cratekit/intake/missing_cli.py` line 489. The list bytes now depend on the provider's live answer, and every repeat run re-asks every ISRC before it learns the files are unchanged or conflicting.

Scenario. Run 1 lists row X by its single id. The provider later files a second release under that ISRC. Run 2 spends N lookups and then refuses intake-list-unusable, because list.json differs (R-476). Even the identical repeat case costs N sequential ISRC calls plus one track() call per answer before the write turns out to be a no-op. During an outage that includes the 31 second ladder. The file check could run first for rows that need no lookup.

**123.4** `src/cratekit/intake/missing_cli.py` line 594. When every handed on row is unwritable but something was listed, the failing unlisted check prints 'are in None ... for: None'.

Scenario. 3 rows are listed by id. 1 bare row has an artist containing ' - ', so text_line refuses it. writable is empty and written.unlisted_path is None. The detail reads '1 missing track(s) ... 0 of them are in None with the reason, for: None'. A person is pointed at a file and a command that do not exist.

**123.5** `src/cratekit/cli/registry.py` line 895. The intake.missing registry entry was not updated. It declares no credential.provider doctor check and still says 'adds two new files', while the verb now needs a provider session and writes a third file.

Scenario. crate doctor reports intake.missing ready on an install with no stored provider session, because doctor.py keys off entry.doctor_checks. The verb then refuses credential-missing on the first set job with an ISRC. The 'no write surface, two files' comment is now wrong about <name>.unlisted.json.

**123.6** `src/cratekit/intake/missing_cli.py` line 302. The outage refusal interpolates str(exc), and tidalapi raises a bare InvalidISRC with no message, so the most likely failure renders as 'could not answer for ISRC X ()' and the detail carries no exception type.

Scenario. A server error, a rejected session and a rejected code all surface as 'the streaming provider could not answer for ISRC QZ... ()' with the remedy retry later. A person or script cannot tell an outage from an expired login that needs re-authentication, because type(exc).__name__ is not in the message or detail.

**123.7** `src/cratekit/intake/missing_cli.py` line 498. by_isrc counts rows that document() then drops as duplicate refs, so the 'named by ISRC and listed' check and summary.by_isrc can exceed summary.written.

Scenario. A set plays one track twice, giving two reports with the same ISRC, or a run holds a playlist row with id 9001 plus a recognised row whose ISRC also resolves to 9001. by_isrc is 2 while document() writes the id once. The check says '2 missing track(s) ... named by ISRC and listed' beside written=1. The same overcount applies to in_file when text_document dedupes identical lines.

**123.8** `src/cratekit/acquire/listdoc.py` line 364. Every handed on row is validated twice: the verb calls text_line per row to pre-filter, then text_document calls it again. The second pass's refusal branch is unreachable from the only caller.

Scenario. Each call does a read_row plus a read_text_rows round trip, so the work is doubled per row. The refusal path inside write() is dead for intake missing. If it ever fired it would be translated to 'move the file aside or name another folder with --out', which is the wrong remedy. write() could accept pre-rendered lines, or return the refused rows, so there is one pass and one owner of the rule.

**123.9** `src/cratekit/label/tidal_catalogue.py` line 618. This is the second wrapper over session.get_tracks_by_isrc, with the opposite failure reading to modules/outbound/tidal_account.py match_track. Two copies of the 'exactly one distinct id' rule now exist and disagree on InvalidISRC and on blank ids.

Scenario. Outbound treats InvalidISRC as not found and discards blank ids. The new path retries InvalidISRC and treats a blank id as UNREADABLE. R-477 records the divergence rather than fixing it. One shared ISRC reader on the catalogue seam, used by both, would stop the same client quirk from being handled two ways.

**123.10** `src/cratekit/intake/missing_cli.py` line 268. The one distinct id test ignores whether the provider's track is streamable, and the client silently drops ids whose track() read raises ObjectNotFound, so the 'never a short answer' contract on tracks_for_isrc is not something the adapter can guarantee.

Scenario. The openapi files ids A and B under one ISRC, and the client's per-id track(B) read 404s in this region. The client returns [A], and the row is listed as exactly one id although the ISRC names two releases. Separately, a single id whose track is not streamable is listed and only fails later at acquire download. Two ids where one is unavailable are handed on although only one could be downloaded.
