# A33 (#293): a landing that ends filed

Brainstorm, 2026-10-12, read only against `main` at b43848a9. The card's five hand steps are measured in `docs/cutover.md` (lines 976, 1005, 1026) and the ledger (R-921, R-922, R-816). What follows is what the code says about each question.

## 1. Auto Analysis on

**Known.** A8 (cutover line 485) launched rekordbox 7.2.19 over two binding rows with Auto Analysis off: no dialog, BPM 0.00, no waveform, rows unchanged after quit. Analyze Tracks from the menu analysed both inside 30 seconds. `land_cli.awaiting_analysis` and `docs/GUIDE.md` line 357 state the off case only. **No record anywhere of a launch with Auto Analysis on over a row rekordbox did not import.** Whether it sweeps rows whose `Analysed` is 0 at launch or on selection is unknown.

**The probe is attended, on the live library.** rekordbox opens only the `master.db` its settings name, so a copy cannot answer this; the copy is for the reading. Shape: with a freshly landed batch in INBOX (`Analysed` 0 on every row, read from a copy taken after both processes are gone), turn Auto Analysis on with KEY unticked in its analysis setting, quit, relaunch, wait two minutes, quit, copy and read `Analysed` and `AnalysisDataPath` on the landed rows. Three readings: launch alone, then INBOX selected, then one row selected. Preconditions: no job and no feeder running, both backup ages under five days, the computer use lock free. Yes means step 1 becomes "open once and wait"; no means Analyze Tracks stays. The visit does not go to zero either way (section 5).

## 2. Write the tag fields at landing

**The columns.** On `djmdContent`: `ArtistID` into `djmdArtist.ID`, `AlbumID` into `djmdAlbum.ID` (which carries `AlbumArtistID`), `GenreID` into `djmdGenre.ID`, `KeyID` into `djmdKey.ID`. All four are foreign keys to lookup rows carrying `Name` (or `ScaleName`), the `StatsFull` bookkeeping and, on artist and album, a `SearchStr`. Adoption reads the words through association proxies (`adopt/collection.py` `genre_of` reads `GenreName`).

**What the landing has in hand.** `ingest.file_meta` reads `artist`, `title`, `genre`, `initialkey`, energy and `inizio` from the source and hard codes `album` to an empty string; `tags.TagSpec` already knows `album` (TALB). `native.RowPlan.columns` writes Title, FolderPath, FileNameL, FileSize, FileType, the inode file id and ContentLink; `_vox_plan` reads `voxlevel`.

**What Reload Tags does that a direct write must do itself.** Measured at cutover line 976: artist, album and key on 165 rows, genre on 159. It resolves or mints the three lookup rows with their bookkeeping and `SearchStr`, sets `AlbumArtistID`, and **writes the file's key into `KeyID`, replacing one rekordbox analysed** (cutover line 790). Two rules travel with a landing write: mint and link in one commit, because rekordbox garbage collects an unreferenced lookup row (A4, 43 to 42), and resolve by exact `Name` to the first active row, since there is no unique constraint and tombstoned namesakes sort first (`metadata.resolve_genre_id`). What rekordbox stores in `SearchStr` is unmeasured.

**The guard today.** `PERMITTED_ROW_TABLES` is playlists, memberships, My Tags and `djmdKey`; `ADMITTABLE_ROW_TABLES` is the content table alone, admitted per commit. A landing may link an existing artist or genre row now and cannot mint one. Fields at landing widen the admission to the three lookup tables, by name on the landing's commit only.

**Key is a no, by decision.** `metadata.UNWRITABLE_FIELDS` refuses `KeyID` at registration and `tests/test_metadata_policy.py` pins it: padded Camelot lives in the title head, the key field stays blank so rekordbox's answer stays independent (A4 rescope). Once Reload Tags leaves, the Key column shows empty on landed rows with KEY unticked. Recommendation: accept that, it is the standing rule.

**The beat grid boundary stays.** `GRIDLESS_ON_CREATE_COLUMNS` (BPM, Analysed, AnalysisDataPath, AnalysisUpdated, CueUpdated) plus SampleRate, BitRate, BitDepth, ImagePath and KeyID are refused on creation and read back by `assert_rows_gridless`; `CONTENT_ANALYSIS_TABLES` must own nothing; no ANLZ file is ever written; the tag reader never reads TBPM. Artist, album and genre are not analysis columns, so the content side needs no policy change.

## 3. Adopt from the file

Adoption already reads two of three inputs off the file or tag: energy through `tags.read_energy_checked` (`scan.py` line 435) and vox through `placements.vox_tagged`. Only genre comes from the row, and `genre_of` says why: one source, no second opinion to drift.

**Switching genre to the file is the wrong fix.** It files a track where rekordbox's Genre column disagrees, which is the 773 stale and 1,233 divergent rows R-816 counted, and it recurs whenever `tag retag` or `tag remap` rewrites a file after its row exists. R-816 closed on 2026-10-01: `crate tag rows` writes `GenreID` from the file for every differing row, linking only, 797 rows at sitting 28. The row can always be made right without rekordbox.

**What changes: nothing in adoption.** With section 2 built, a landed row carries its genre from the first commit and `adopt scan` sees it with rekordbox closed. Adoption needs one addition, a scope: `scan_rows` walks the whole collection, and a landing wants the census over its own content ids.

## 4. One verb

`intake land` on a cut over tree is already a composite: rows, ContentLink (U126), the vox tag (U127), account playlists (U113, U128), hearts (U120), the set playlist (U121), one gate, one commit. Fields join that commit. Adoption cannot join the same digest: `AdoptionPlan.digest` hashes entry ids built from content ids that do not exist until the landing commits.

**Shape that gives one approval.** The landing plan predicts each added file's bucket, sub and vocal sub before the row exists, through `ingest.decide_placement` (which `landing._unplaceable` already calls on the staged file), lists it and digests it. After the commit the same run plans adoption over the landed content ids on the same handle, compares to the prediction, and applies memberships and genre Favorites under adoption's own writer and ledger when equal. Two commits, one answer.

**The digest covers** every row's columns with the artist, album and genre words and whether each links or mints, ContentLink and its count, the vox cut and scores, playlists, hearts, set playlist, the predicted placement per file, the taxonomy schema version and the counts. **Not the database path.** R-922 is open: `native.identity` digests `str(plan.database)`, so no copy rehearsal matches and every landing waits on the author. Fix that first or the session can never approve this verb.

**Failure shapes.** Prediction differs after the commit (tree moved, sub undeclared, file retagged): landed and not filed, said plainly with `adopt apply` named, never rolled back. Mint fails mid commit: the whole commit rolls back behind the guard. Two active lookup rows for one word: first active by exact name, the duplicate reported. No genre on the file: predicted `needs-genre`, landed, listed, placed nowhere. The copy rehearsal moves the real files: rehearse on a database copy with library state redirected, move live once.

## 5. What still needs rekordbox

Analysis, and only analysis: tempo, grid, waveform, phrase, artwork, `Analysed`, `AnalysisDataPath`, the ANLZ files, the cue and mixer rows. Forbidden to Cratekit absolutely. One visit per landing, after the verb: open, select INBOX, Analyze Tracks with KEY unticked, quit, confirm both processes gone. Nothing in filing waits on it: a row sits in BY GENRE + ENERGY with BPM 0.00 until the visit. Step 5 of the card (set tie misses) is matching, not rekordbox. The Key column stays empty unless A4 is revisited.

## Units to file

### U<next>: the native landing digest carries the database identity, not its path (R-922)

**Depends on:** none

**Goal.** A copy rehearsal of `intake land` matches the live digest, so the session approves a landing under the 2026-10-09 rule.

**Approach.** Drop `"database": str(plan.database)` from `native.identity`; device and master id already identify the library. Show the path on the gate screen outside the digest, in `land_cli._native_payload` too if it repeats it.

**Key files.** `src/cratekit/intake/native.py`, `src/cratekit/intake/land_cli.py`, `tests/test_intake_native*.py`.

**Test scenarios.** Two plans over the same files against copies at different paths digest equal; the screen names the path; a row or playlist difference still moves the digest.

**Verification.** The next live landing's digest equals its rehearsal; R-922 closed.

**Out of scope.** The cutover gate's same shape (sitting 31).

### U<next+1>: every native landing writes artist, album and genre on the row from the file (R-921)

**Depends on:** U<next>

**Goal.** A landed row reads whole in rekordbox and to adoption before rekordbox opens; Reload Tags leaves the tail.

**Approach.** `RowPlan` gains `artist`, `album`, `genre` from `file_meta` (read `album` through `tags.read_tag`). The plan resolves each word to the first active lookup row by exact `Name` (generalise `metadata.resolve_genre_id`) and plans a mint where none exists; screen and digest show linked against minted per row. `apply_rows` mints and links in the one commit, admitting `djmdArtist`, `djmdAlbum`, `djmdGenre` by name on that commit with the same honesty as `ADMITTABLE_ROW_TABLES`. Album artist links the artist row. `KeyID` untouched. Read back from SQL and through `adopt.collection.genre_of`; refuse a row whose word did not take.

**Key files.** `src/cratekit/intake/native.py`, `src/cratekit/intake/ingest.py`, `src/cratekit/write/metadata.py`, `src/cratekit/core/rb_writer.py`, `src/cratekit/intake/land_cli.py` (screen, `awaiting_analysis` wording), `docs/GUIDE.md` tail.

**Test scenarios.** Word with an active row links it; no row mints and links in one flush; tombstoned namesake skipped; file with no artist leaves rekordbox's empty; creations naming `djmdKey` refused; `assert_rows_gridless` holds; `adopt scan` over the disposable database places the rows with no reload; vox still written.

**Verification.** Live landing, then rekordbox shows artist, album and genre before any reload and `adopt scan` places the rows with rekordbox closed; R-921 closed.

**Out of scope.** Key (A4), rating (`RATING_BACKFILL` has no caller in `src`), rows landed earlier (`tag rows`).

### U<next+2>: `intake land` files its batch, adoption scoped to the landed rows under the one answer

**Depends on:** U<next>, U<next+1>

**Goal.** A set or favourites pass ends in BY GENRE + ENERGY with one `crate run decide`.

**Approach.** `scan_rows` gains a content id scope. The landing plan predicts bucket, sub and vocal sub per added file, lists and digests them. After the commit the run plans adoption over the landed ids on the same handle, applies through `adopt.apply.apply_plan` and its ledger when every placement equals its prediction, otherwise ends `landing-filed-differently` naming `adopt apply`, the landing durable. A land only option keeps today's behaviour.

**Key files.** `src/cratekit/intake/land_cli.py`, `src/cratekit/intake/native.py`, `src/cratekit/adopt/scan.py`, `src/cratekit/adopt/plan.py`, `src/cratekit/adopt/apply.py`, `src/cratekit/intake/landing.py`.

**Test scenarios.** Five files, three with genre, one without, one vox: memberships and favorites read back, the genreless one listed; prediction mismatch leaves rows landed and says so; digest equal on a copy and live; nothing added files nothing.

**Verification.** The next real pass ends filed with one approval and one rekordbox visit; the GUIDE tail reads land, visit, done.

**Out of scope.** Older unfiled rows, the Auto Analysis probe (attended card), set tie misses.

**Residuals, one line:** the Auto Analysis probe is an attended A card, not a unit; the empty Key column is Phillip's call under A4; `SearchStr` and lookup bookkeeping are unmeasured until U<next+1> reads a copy; `RATING_BACKFILL` has no caller.
