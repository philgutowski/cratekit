# Cutover

The per workflow record U29 asks for. The board says every unit is closed and
the parity table says every Feature Inventory row has a verb. This file says
which workflows have actually run on the live library, what each run observed,
and what still stands between the product and a full sync cycle on Cratekit
alone. It is written by the attended sittings, never by a session, and a
workflow moves to "cut over" only after it has run correctly on the live
library at least once and the author has lived on it.

Standing rule for every sitting: rekordbox and its agent closed, the volume
mounted, `crate doctor` read before anything else, one workflow per sitting.

## Sitting 1, 2026-09-16

Machine state before: no real configuration had ever been written. The state
directory held test debris from a mutation driver run (R-343) and was deleted.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Setup and doctor | yes | Config, taxonomy on the volume, pin 7.2.18.0311 recorded by a typed yes, both ACR keys and the PKCE provider session in the keychain, commit-msg hook installed, Drive trash off on the remote. Doctor reports no failing check after Full Disk Access was granted. | live |
| Backup, R-9 | dry run yes, real run launched | The mirror command listed both sides in 51 minutes and would copy 52 files, archive 1139, delete 0. Real run is job `2026-09-16T16:30:43Z-4c99`. | pending the real run's outcome |
| Download, R-210 | yes | First real track through the adapter found #82 and it is fixed. After it, a 16 bit 44.1 kHz FLAC with full tags and no tempo tag. Device-flow control on the same account and track was served AAC. | proven, not yet lived on |
| Sync cycle | no | Cannot run. See below. | blocked |
| Tree flip, R-131 | no | Not attempted. Needs a sync to have placed tracks first. | blocked behind sync |
| Vocal restamp, R-133 | no | Not attempted this sitting. | open |
| Retirement of DJ_tools | no | | blocked behind everything above |

Defects found by running rather than by testing, all on the ledger: R-343
through R-349. Four are a sitting's worth of small fixes (R-344, R-346, R-347,
R-348), two are product gaps (R-345, R-349), one is a driver question (R-343).

## Sitting 2, 2026-09-16, evening

Machine state before: rekordbox and its agent closed, the volume mounted,
`crate doctor` reporting no failing check and both backup ages at 0 days. No
Relay run held the repository.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Backup, R-9, real run | yes, read back on Drive | Job `2026-09-16T16:30:43Z-4c99` succeeded, 2 of 2 items. The dated archive holds the 1139 objects the dry run predicted, 6.9 GiB, and the snapshot's `master.db` matches the live file in size and time. | live |
| Restore rehearsal, R-9 | yes, to a scratch directory | The database landed byte for byte, MD5 matched, `integrity_check` ok through the product's own opener, 17341 content rows. The verb then reported the restore failed, because it copies a write ahead log the snapshot does not hold (R-367). No shipped verb targets anything but the live root, so the rehearsal was a script calling the engine (R-368). The live database was not touched. | rehearsed once, verb defective |
| Backup acknowledgment | yes | Minted by the author from a Terminal window at 01:11Z, valid twelve hours. A session cannot mint it, and answering the gate is not minting it (R-369). | live until 13:11Z |
| Vocal restamp, R-133 | no | Next sitting, one workflow per sitting. | open |

R-9 is closed on the ledger. Three findings filed, R-367 to R-369.

## Sitting 3, 2026-09-17, morning

Machine state before: rekordbox and its agent closed, the volume mounted,
`crate doctor` reporting no failing check, both backup ages at 0 days, the
backup acknowledgment minted last night by the author and valid until 13:11Z.
Neither the analysis nor the vocals extra was installed in the venv; both were
installed at the start of the sitting, and the checkpoint and label table the
source system uses were already in `~/panns_data`.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Vocal restamp, R-133 | yes, twice, one folder | The shipped loader could not score anything (R-370), fixed in the sitting. First real run over `This Never Happened LIBRARY 2026-07-02`, 36 tracks, 102 seconds, 1.3 GB peak on the 18 GB machine: 35 scored within one point of what DJ_tools stamped, every gender call matching, one failed on a quarter second tail chunk (R-371), fixed in the sitting. Second run: that track scored, the other 35 unchanged. | cut over for one folder, the full library pass is R-376 |
| Vocal cut | carried | DJ_tools' hand set 5.0 written into `.cratekit/local/vocal_calibration.json` by hand, since no verb sets a cut (R-374). | live |
| Location prefix rule | added by hand | The first My Tags plan resolved 0 of 9937 rows and reported ok (R-372). `location_prefix_map` now maps the drive's old volume name to the current mount; 9770 rows resolve, 167 are streaming and home directory rows. | live |
| My Tags, `metadata mytags-vocals` | plan, then apply on the live database | Plan: 1117 tracks, 288 male, 491 female, cut 5.0. Read only comparison before the apply predicted 4 new associations and 1892 already present. Apply inside the ack window: written 4, already 1892, snapshot captured first, read back vox 1141, male vox 296, female vox 502. Forty three associations DJ_tools wrote sit on files with no voxlevel today (R-373). No session record is written for a gated write (R-375). | live |

R-133 is closed on the ledger. Eight findings filed, R-370 to R-377, two of
them fixed in the sitting and one raised by the review of that fix.

## Sitting 4, 2026-09-17, afternoon

Machine state before: rekordbox and its agent closed, the volume mounted,
`crate doctor` reporting no failing check and both backup ages at 0 days. The
night's acknowledgment had expired at 13:11Z and a new one was minted by the
author from a Terminal window at 15:23Z, valid twelve hours. Cratekit's label
registry was empty; all 47 labels from the source system's `favorite_labels.json`
were carried into it at the start of the sitting, with their match needles and
track limits, through the store's own `add` because no verb sets a track limit.
The author exported a fresh collection from rekordbox mid sitting and closed it
again, since both outbound verbs read an export and never the database (R-227).

Six workflows rather than one, at the author's direction, because the three
landed adapters each owed a live run and they share one set of preconditions.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Playlist harvest, U62 | yes | A share sheet link, `https://tidal.com/playlist/<uuid>`, taken unchanged (R-354 observed). Four labels found behind a ten track playlist, six tracks unresolved. The verb printed none of it: the human renderer has no case for its payload (R-378). | live, output defective |
| Playlist intake, U62 | yes | Ten items, all resolved, none acquired, every one reported `missing / not-in-library`, which an independent check of the library confirmed. `sync all` then queued the same playlist again (R-382). | live |
| Label sweep, U62 | yes | 47 labels queued, **15 swept, 32 failed**: 31 `LabelUnresolvable` for want of a seed artist, one unverifiable. 98 releases offered into review from 12 labels. R-352 measured. The job then reported itself transient and resumable over permanent failures (R-380), and every offered row carries a Python object address where the artist belongs (R-379). Two accented labels got mangled identifiers (R-381). | live, and two thirds of the registry refuses |
| `crate sync all`, U64 | yes, favourites answered abort | 599 playlists listed, 18 queued as intake plus one labels job, nothing resumed. **11 of the 18 are source system label debris**, five of them named `Sol Selectas LIBRARY` and four `Colorize LIBRARY`: R-361 observed. `"mark": "unbound"` on every pass, as R-358 says. | live |
| R-355, the ISRC | fixed in the sitting | The rows both outbound verbs build carry no ISRC, so a live run matched nothing. `source.isrc_for` now reads the file's own tag through the prefix map, `isrc` is a field in the one tag table, and an absent library root refuses rather than reading as a library of untagged files. Live: 103 of 109 favourites and 8246 of 9937 collection rows carry one. | fixed, merged with the sitting |
| Playlist export, U63 | yes, twice | Four track playlist, one remote playlist created across a four item job, 2 added, 2 unmatched, and the account read back holds exactly the two reported. The second run created nothing and added nothing. Both unmatched rows are R-356, an ISRC the provider answers with several tracks. | cut over |
| Favourites sweep, U63 | yes, twice | 109 rows: 18 hearted, 41 already, 50 unmatched, 0 coloured, no failed item, and all 18 verified present on the account. The second pass hearted nothing and read all 59 as already. The shipped favourites listing reads 93 of the account's real 197 (R-383), newest first, so an old heart's state is unreliable while a recent one is not. The colour write this verb declares is still unbound. | cut over |

R-355 is closed by fixing it. R-144 is closed outright, both engines driven
twice. R-352, R-354, R-356 and R-361 carry their live measurements. Six
findings filed, R-378 to R-383, of which R-383 is the one with reach beyond this
sitting.

## Sitting 5, 2026-09-23, afternoon

Machine state before: the live configuration had been overwritten on
2026-09-20 at 16:55 with a test fixture configuration, R-343's predicted worst
case, and doctor failed three checks. R-343 was closed on `main` earlier the
same day, so the mutation driver can no longer do it again. The volume mounted,
rekordbox and its agent closed. The pipx `crate` was 736 commits behind pushed
`main`, at the R-368 merge, and was brought to `1d2136f` first, since running
setup off it would have rebuilt the configuration against defects `main` had
already fixed. No backup acknowledgment was minted: nothing in this sitting
writes to the library or the database.

One workflow, the rebuild, and it took three runs of `crate setup`. Every value
was recovered from a record rather than from memory: the volume UUID from
`diskutil`, lowercased on purpose (R-344); the three backup destinations from
`backup_facts.json` under `.cratekit/local` on the volume, the mirror and the
dated archive both named for the volume and the snapshots under
`gdrive:rekordbox_db`, all three present on the Drive; the live database by
size and date, `PIONEER/Master/master.db`,
281 MB, last written at sitting 3's My Tags apply to the minute; the drive's old
name, `BoatRx`, from the source system's own constant and then from the
database's drive registry.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Rebuild, run 1 | refused | `config-unusable`: the fixture file spelled `remote = "remote"`, setup derives the remote only when the file does not spell one, and the destinations named `gdrive`. No flag overrides a spelled remote, so a re-run cannot repair one (R-662). The fixture file was moved out of the state directory, which is what sitting 1 did with the same debris; the queue, run records and credential index stayed. | refused |
| Rebuild, run 2 | wrote the configuration, failed the canary | The path given for the database was `PIONEER/rekordbox/master.db`, a zero byte file dated May 21 one directory over from the live one, the author's error. Setup accepted it, copied it, and reported `no such table: agentRegistry` on the copy (R-663). The pin and the prefix rule were not recorded because the `!` runner passes no terminal and every prompt took its default. | partial |
| Rebuild, run 3 | `setup: ok` | Answers fed on stdin, two yeses. Pin recorded at 7.2.18.0311 by an explicit answer, with no confirmation date yet. The `BoatRx` rule offered off the database's `BaseDBDrive` and `CurrentDBDrive` and recorded, which is R-372's close working live for the first time. The existing taxonomy on the volume, 18 buckets, left alone. Backup ages read back from the volume, 7 and 6 days. | live |
| `crate doctor` | yes | Exit 0, no failing check. 9784 of 9937 active rows resolve under one rule; 153 do not, 137 under `/v4/catalog`, 8 under the home directory, 8 elsewhere, the streaming and home rows sitting 3 also counted. `rekordbox.pins` notes the pin has no date on which it was confirmed against a real write. | live |

Two findings filed, R-662 and R-663, neither on the board bar. The `!` runner
having no terminal is an operator fact for the next sitting, not a product one:
a wizard answer goes in through a pipe from that runner or from a Terminal
window, and the sittings' "typed yes" is still the author's either way.

## Sitting 6, 2026-09-23, afternoon

Machine state before: the volume mounted, rekordbox and its agent closed,
`crate doctor` from the pipx install at `1d2136f` exit 0 with no failing check,
the pin still without a confirmation date, backup ages 7 and 6 days. No backup
acknowledgment was minted: the sitting stopped before anything that writes.

One workflow, A5 line 1, favourites in, and it ran its first two steps. Every
verb was run from the pipx install, never the checkout.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `intake playlist favorites`, the listing | yes | 1.7 seconds. **215 declared, 206 listed, 9 withheld**, said in the `intake-hearts-withheld` warning and the envelope's `shortfall` block. That is R-383's live half, closed: the old rule read 93 of 197 at sitting 4, and the account holds 215 today. The verb queues and returns, and the human renderer prints nothing about the job it queued (R-378's shape); the job identifier was read out of `job list --output json`. | live, R-383 closed |
| `intake playlist favorites --job`, the resolution | yes | 13 seconds, 206 settled: **0 owned, 61 offered, 145 missing.** Sitting 4 had matched 59 of these hearts to library rows by ISRC; this run reported 37 of the 59 missing and 22 offered. Cause: the Title tag of every processed file carries the `KEY - BPM - ` head, the index takes the tag verbatim, so no processed file can match exactly. Re-resolved on the volume with the head stripped from the tag: 96 owned, 27 offered, 83 missing (R-664). | live, output false |
| `intake missing --job` and everything after | not run | The list would have carried at least 96 owned tracks, and the download and landing would have put 96 duplicates into the library. Stopped by the author's decision. Job `2026-09-23T17:21:30Z-0dbf` stays succeeded with its 61 `version-match` review items unanswered, and sitting 4's ten item playlist job `673e` is still queued from that day. | stopped |

One finding filed, R-664, on the board bar, and R-383 closed. Line 1 of #178 is
not ticked: the tick is a pointer to a record of the workflow having run, and it
ran two steps of seven.

## Sitting 7, 2026-09-23, afternoon

Machine state before: the volume mounted, rekordbox and its agent closed, the
pipx install brought from `1d2136f` to `2e30b0d`, the R-664 merge, with its
analysis and vocals extras kept, `crate doctor` exit 0 with no failing check,
backup ages 7 and 7 days. No backup acknowledgment was minted and no gate was
answered: nothing in this sitting wrote to the library, the database or the
account. Started by the author as "Take #178" and run unattended to the first
gate that needs a person, which is the rule for a sitting nobody is watching.

One workflow, A5 line 1, favourites in, resumed at the fresh listing. Every
verb from the pipx install.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `intake playlist favorites`, the listing | yes | 1.8 seconds, **215 declared, 206 listed, 9 withheld**, the same as sitting 6. Job `2026-09-23T18:12:52Z-7caa`, read out of `job list --output json` as before. | live |
| `intake playlist favorites --job`, the resolution | yes | 11.8 seconds, the same 206 rows as `0dbf`: **96 owned, 29 offered, 81 missing**, against sitting 6's measured 96, 27, 83. Of sitting 4's 59 ISRC matched hearts, 37 owned, 9 offered, 13 missing, every one of the 22 with its head read off correctly and failing on the artist alone. R-664 closed on its second condition. | live, R-664 closed |
| The library walked by ISRC tag | yes, a script | 9868 files in 9 seconds, 1691 with no ISRC tag. **26 of the 81 missing rows and 23 of the 29 offered rows are held** under the row's own ISRC, and the match engine never asks (R-667). The rows, with their files, are in `Downloads/lists/intake-2026-09-23T18:12:52Z-7caa.held-by-isrc.json`. | measured, output false over 49 |
| `intake missing --job` | yes | 11 seconds, 81 rows to `intake-2026-09-23T18:12:52Z-7caa.list.json` with its manifest, 96 owned and 29 offered not listed, 0 by ISRC. The 26 held rows were then dropped by hand into `intake-2026-09-23T18:12:52Z-7caa.unheld.list.json`, 55 rows, the list the download read. | live, list over held files |
| `acquire download`, job `2026-09-23T18:17:08Z-6734` | yes | Queued 55 and drove them in 7 minutes 16 seconds: **54 acquired, 1 refused** by the strict lossless policy, `Calvin Harris :: Satisfy`, `GBARL2600687`, offered lossy only, so the job reports failed and the 54 are durable. Every file 16 bit 44.1 kHz FLAC, artist, title and ISRC tagged, no tempo tag, 1.5 GB in the staging root. `--job` alone refuses for want of the list positional (R-668). Sitting 1's smoke file `341726337.flac` sat in the same root, held by ISRC as `Mood ll Swing :: Chicago Blues`, and was moved to the volume's trash so neither the tagging walk nor the landing would take it. | cut over for one batch |
| `tag folder`, job `2026-09-23T18:25:43Z-448a` | yes | 54 in 2 minutes 47 seconds: **40 tagged, 10 no hit, 4 unmapped** (`Electronica`, the taxonomy has no bucket), art present on 54 and the broken picture block repaired on 54. Genres read back off the files: Organic House 6, Afro House 6, Melodic House 5, House / Funky House / Disco 5, Dance / Pop 5, Deep House 4, Tech House 3, and singles. | cut over for one batch |
| `name apply --root Downloads` | to the gate | **The plan is empty: 0 renames, 0 referenced, 0 collisions** over 54 files named `<id>.flac`, because the adapter names by identifier and the verb never composes a body (R-669). The gate screen shows no plan on either output form; the plan was read by answering abort, which renames nothing (R-670). Runs `a653` and `7222` are left blocked at the gate, unanswered. | live, no-op over acquired files |
| `intake land --export Music/9-17-export.xml` | to the gate | The gate shows the plan: 54 files from `Downloads` into `Music/2026-09-23T183118Z-9416`, intake file `2026-09-23T183118Z-9416_inboxed.xml` at the volume root, against sitting 4's export of 2026-09-17. Run `2026-09-23T18:31:18Z-9416` is blocked at `intake.land.confirm`, the author's answer. Nothing moved. | stopped at the gate |
| The rekordbox import | not run | Behind the landing. | blocked |

Four findings filed, R-667 to R-670, two of them on the board bar, R-667 and
R-669, issues owed after this merge. R-664 closed. Line 1 of #178 is not
ticked: it ran five steps of seven and stopped at the first gate.

## Sitting 8, 2026-09-23, evening

Machine state before: the volume mounted, rekordbox and its agent closed,
the pipx install brought from `2e30b0d` to `f4f5e08`, the R-667 merge, with
its extras kept, `crate doctor` exit 0 with no failing check, backup ages 7
and 7 days. The acknowledgment had expired on the 18th and was minted by the
author from a Terminal window at 21:33Z, valid until 09:33Z. Attended
throughout: the author drove every verb from the pipx install and the
session recorded. Every write ran inside the acknowledgment window.

One workflow, A5 line 1, favourites in, resumed at the rename gate the
landing hold left, and it ran to the end.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `name apply --root Downloads`, first run | refused | `collection-row-unmapped`, **582 rows**, before the gate. R-500's guard reads the collection only when a plan would rename something, so sitting 7's empty plan never reached it and this was its first live read. On a disposable copy of the database: 137 active streamed tracks recorded as `/v4/catalog/tracks/<id>/`, 437 tombstones under two folders that are gone, 8 rows on the other account. No honest prefix rule maps any of them (R-675). The author chose to fix the guard in the sitting. | refused, fixed in the sitting |
| R-675, the fix | built, reviewed, merged, pushed | A dark row refuses only when its file name is one the plan would rename and no resolved row holds. Merged to `main` at `93e8f40` with R-523 and R-524 closed, the pipx install rebuilt from it. | fixed, merged with the sitting |
| `name apply --root Downloads`, second run | to the gate, then applied | Run `2026-09-23T22:16:52Z-ab7c`: **renames 54, referenced 0, collides 0, unnamed 0**, every planned name shown on the gate (R-670 live). The plan was read back through the abort answer, its digest equal to the one the gate held, and all 54 names equal the body composed from each file's own artist and title tags. Applied: `name.apply: ok`, 54 files on disk named `Artist - Title.flac`, none still an identifier. R-669's second condition met. | cut over for one batch |
| Fresh export | yes, by hand | `Music/9-23-export.xml`, 9937 entries. The landing verb reached its gate before the file existed and would have refused after the answer with nothing moved (R-677). | live |
| `intake land --export`, run `2026-09-23T22:22:41Z-4773` | to the gate, then applied | 54 files from `Downloads` into `Music/2026-09-23T222241Z-4773`, intake file `2026-09-23T222241Z-4773_inboxed.xml` at the volume root, 9991 entries, the 54 new rows in a playlist of the batch's name under INBOX, each with no tempo element and an average BPM of zero, 39 with a key and 40 with a genre. Staging empty afterwards. | cut over for one batch |
| The rekordbox import | yes, by hand | The intake file set as the rekordbox xml library, the playlist found under INBOX, imported, then `Music/9-23-export-2.xml` exported with 9991 entries and all 54 batch locations. | live |
| `intake imported --export` | yes | `intake.imported: ok`, the intake file retired as `.imported`, run `4773` settled with no gate open. The human form printed nothing about the 54 it proved (R-678). | cut over |
| `intake playlist favorites`, the listing | yes | 215 declared, 206 listed, 9 withheld, job `2026-09-23T22:34:35Z-c645`, the same as sittings 6 and 7. | live |
| `intake playlist favorites --job`, the resolution | yes | 10 seconds, 206 settled: **203 owned, 2 offered, 1 missing.** By reason: 198 `isrc-exact`, 4 `credited-exact`, 1 `exact`, 1 `version-differs`, 1 `title-approximate`, 1 `not-in-library`. **All 49 rows held by ISRC at sitting 7 resolve owned under `isrc-exact`**, R-667's second condition met. All 54 landed files resolve owned by ISRC. No offered row has a file carrying its ISRC, R-674 measured at zero and closed. The 4 credited hits are three Steve Reich movements and one Breaking Beattz row, each in a processed folder with no ISRC tag. The two offered rows, `Above & Beyond :: Fractals` at another version and `Elderbrook :: I'll Find My Way To You` as a title question, are real questions in `crate review list`. The one missing row is `Calvin Harris :: Satisfy`, lossy only, refused by policy. | live, R-667 and R-674 closed |

Line 1 of #178 is ticked: favourites in ran from the listing to the import
proof on the pipx install, and the heart count against the brief's 197 is
215 on the account today, 206 served. Filed R-675 to R-678, R-675 closed in
the sitting; R-676 is the deletion pass's same shape, read and not driven.

## Sitting 9, 2026-09-23, evening, late

Machine state before: the volume mounted, rekordbox and its agent closed,
the pipx install brought from `93e8f40` to `94ad650`, the sitting 8 record
merge, with its extras kept, `crate doctor` exit 0 with no failing check,
backup ages 7 and 7 days, 153 of 9991 active rows under no prefix rule.
The acknowledgment minted by the author at 21:33Z on the 23rd was still
valid, until 09:33Z, and every write ran inside it. Driven differently from
sitting 8, at the author's direction: the session drove every verb from the
pipx install and answered both gates itself, and the author did the two
things only a person can do, the rekordbox import and the export. The
author's review of each gate is the plan printed on it, recorded below.

Before the workflow, the decision the sitting 8 record left open: whether the
190 unresolved review items get a pass first. Measured off a copy of the
queue database, not driven: 98 `label-release` and 4 `harvested-label` from
sitting 4, which are line 5's, and 88 `version-match`, 58 from job `0dbf`,
29 from `7caa` and 1 from `c645`. Joined against `c645`'s 206 rows, **85 of
the 88 ask about a row that resolution now owns**, 81 under `isrc-exact` and
4 under `credited-exact`. Three are live: `Above & Beyond :: Fractals` twice,
once asking the recording and once the version, and `Elderbrook :: I'll Find
My Way To You` once. The sitting 8 note's count, 61, 61 and 46, was wrong.
The verdict vocabulary is `accepted` or `rejected` and `--where` matches a
payload field by equality, so no honest sweep exists. Decided: no pass, the
stale item shape is R-679, line 2 now.

One workflow, A5 line 2, a small playlist through line 1's path. The
playlist is the ten track one sitting 4 ran standalone as `e3f4`, all ten
missing that day, continued here as job `2026-09-17T16:44:44Z-673e`, the
copy the 9-17 `sync all` pass queued and nobody had driven.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `intake playlist <url> --job 673e`, the resolution | yes | 9.6 seconds, a `config-drift` warning naming four keys changed since the job was queued, the job run against its frozen copy. 10 settled: **3 owned, 7 missing**, the 3 under `isrc-exact`, every one a file sitting 8 landed into `4773` (Teak, Dame Un Grrr, Falling Feels Like Flying), so the hearts and this playlist overlap by three and the overlap was found by ISRC. The human form printed `ok` and the counts came from the artifacts (R-678). | live |
| `intake missing --job 673e` | yes | 8.7 seconds, 7 rows to `intake-2026-09-17T16:44:44Z-673e.list.json` with its manifest, 3 owned not listed, 0 offered, 0 by ISRC. This verb's human form names every count and the next command. | live |
| `acquire download <list>`, job `2026-09-23T22:53:38Z-ad05` | yes, twice | The first call queued 7 and returned `ok` in 0.3 seconds with no job identifier printed (R-678's shape, one more verb). The second, `--job`, drove them in 47 seconds: **7 acquired, 0 refused**, every file 16 bit 44.1 kHz FLAC, artist, title and ISRC tagged, 212 MB in staging. | cut over for one batch |
| `tag folder`, job `2026-09-23T22:55:19Z-81b9` | yes, twice | Queue then drive, 17 seconds: **7 tagged, 0 no hit, 0 off taxonomy**, all from Beatport, Deep House 3, Melodic House 2, Organic House 1, Afro House 1, art present on 7 and the picture block repaired on 7. | cut over for one batch |
| `name apply --root Downloads` | to the gate, then applied | Run `2026-09-23T22:56:37Z-3316`, 1.7 seconds with the collection read: **renames 7, referenced 0, collides 0, unnamed 0**, every name composed from the file's own tags, `Artist - Title.flac`, one carrying `(Radio-Edit)` from its title tag. R-675's leaf rule held on its second live plan. The gate was answered `apply` through `crate run decide` and the run continued with the global `--run`, which sits before the verb, not after it. 7 files renamed on disk. | cut over for one batch |
| `intake land --export Music/9-23-export-2.xml`, run `2026-09-23T22:58:04Z-d66b` | to the gate, then applied | Against sitting 8's post import export, 9991 entries, written a minute before rekordbox closed. 7 files from `Downloads` into `Music/2026-09-23T225804Z-d66b`, intake file `2026-09-23T225804Z-d66b_inboxed.xml` at the volume root, **9998 entries**, the 7 new rows in a playlist of the batch's name under INBOX, each with no tempo element and an average BPM of zero, 6 with a key and 7 with a genre. Staging empty afterwards. The run then reported `PENDING_HUMAN` with the three steps a person owes. | cut over for one batch |
| The rekordbox import | yes, by hand | The intake file set as the rekordbox xml library, the playlist found under INBOX, imported, then `Music/9-23-export-3.xml` exported with **9998 entries and all 7 batch locations**, each still with no tempo element and an average BPM of zero. | live |
| `intake imported --export Music/9-23-export-3.xml` | yes | 0.7 seconds, `intake.imported: ok`, the intake file retired as `.imported`, run `d66b` settled with no gate open. The human form again named nothing it proved (R-678). | cut over |
| `crate delete review`, plan only, run `2026-09-23T23:09:32Z-65f0` | to the gate, answered abort | Run by the author from a Terminal window, because this session's permission layer refused the verb as a deletion. The reference set was complete: **baselined, 7404 accepted as history, 0 offered**, no refusal over the 137 streamed rows. R-676 closed on its first arm, nothing moved. | measured, R-676 closed |

Line 2 of #178 is ticked: a small playlist ran from the queued job to the
import proof on the pipx install, three of its ten rows already owned by ISRC
from line 1's batch, seven acquired, tagged, named, landed and imported.
Every verb but the deletion plan was driven by the session, both write gates
answered by it after the plan matched the tags, and nothing needed a second
invocation except to learn a count the human form withheld. Filed R-679.
R-676 closed. R-677 and R-678 were observed again and stand.

## Sitting 10, 2026-09-24, morning

Machine state before: the volume mounted, rekordbox and its agent closed,
the pipx install brought from `0832299` to `40daec7`, the R-658 merge, with
its extras kept, `crate doctor` exit 0 with no failing check, backup ages 7
and 7 days, 153 of 9998 active rows under no prefix rule, three runs from
sitting 7 still holding open gates. The acknowledgment minted at 21:33Z on
the 23rd had expired at 09:33Z and **was not re-minted, by decision**: the
gate that reads it sits on the database, deletion, restore, adopt and backup
paths, and nothing this sitting ran touches one. Both verbs of the sitting
write queue state or a new file beside an export through the explicit gate
alone. Driven as sitting 9 was: the session drove every verb from the pipx
install and answered every gate, the author did the rekordbox work. The
Cratekit Relay feeder was alive and idle and was stopped before the merge.

First, R-679's owed measurement, then A5 line 3, inbox routing.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `intake playlist favorites`, the listing | yes | 2.0 seconds, **216 declared, 207 listed, 9 withheld**, one heart more than sitting 8, job `2026-09-24T11:49:23Z-c3ca`. R-678's rendering names the job, the drive command and the item count, so nothing was read out of JSON. | live, R-678 held |
| `intake playlist favorites --job c3ca`, the resolution | yes | 9.8 seconds, 207 settled: **203 owned, 2 offered, 2 missing, 0 suppressed**, each count printed by the rendering with the next command. By reason, off the artifacts since the rendering has no breakdown (R-682): 198 `isrc-exact`, 4 `credited-exact`, 1 `exact`, 1 `version-differs`, 1 `title-approximate`, 2 `not-in-library`. The offered rows are sitting 8's two; the missing are `Calvin Harris :: Satisfy`, lossy only, and the new heart `R. Kelly :: Same Girl`. | live |
| `review list`, R-679's measurement | yes | Before the resolution, `--limit 500`: 190 unresolved, 98 `label-release`, 88 `version-match`, 4 `harvested-label`, none with a verdict. After: **105 unresolved, the 3 live `version-match` items and the 102 label rows**. `--all` lists 190 with **85 `superseded`, 81 under `isrc-exact` and 4 under `credited-exact`**. The default page is 50 items, so the whole list needs `--limit`. | measured, R-679 CLOSED live |
| `route inbox --export Music/9-23-export-3.xml`, plan only | to the gate, answered abort, three times | The gate `route.inbox.apply` prints the question and no plan, in human and json mode alike, and `run show` holds none, so the plan was read through the abort answer (R-686). 220 items, 1.2 seconds: the 199 tracks under INBOX, every one already filed, 4 ratings on old rows, **21 long tracks for a `Sets and Long Tracks` playlist the active taxonomy does not declare**, because every verb reads the shipped template (R-685), 1 streamed row unreadable. **The 61 rows of the two batches were not in the plan**: both batch playlists sat at the playlist root, where the rekordbox import had put them, not under INBOX (R-687). The author dragged both into INBOX and exported `Music/9-24-export.xml`, 9998 entries. | measured, nothing written |
| `route inbox --export Music/9-24-export.xml`, run `2026-09-24T13:03:35Z-814c` | to the gate, then applied | Read first through an abort on run `de66`, 1.6 seconds: 281 items, 260 under INBOX, 259 with a destination. **All 61 new rows route to their genre's Unsorted sub**, none carrying an energy reading, so none gets a rating or a vocal placement; among the old rows 34 vocal placements already held, 4 ratings, 2 tracks re-filed into an energy sub. 21 long tracks, 0 vocal subs created since all 18 exist. Applied on the second run with the same digest `819c9e8dbee52322`, 4.8 seconds: **inserted 63, rated 4, long added 21**, 61 lengths unreadable at zero, `Music/9-24-export_routed.xml` written. Checked against the export: 84 memberships added across 14 playlists, the 63 and the 21, four `Rating` attributes changed, 481193 tempo elements on both sides, no average BPM moved, no duplicate row made; the four duplicate rows found were already in the export. | cut over for one file |
| The rekordbox import | yes, by hand | 14 playlist nodes imported one at a time, never a folder, per the source system's Invariant 3, then `Music/9-24-export-2.xml`, 9998 entries, 501 playlist paths. **`Sets and Long Tracks` landed at the root with 21.** The 13 nested subs did not: each landed at the root as a new playlist, same names replacing each other, leaving `Unsorted` (8), `High` (184) and `Soul / R&B` (35) as strays and every sub inside `BY GENRE + ENERGY` unchanged (R-687). **All four ratings read 0** after the import (R-688); the screen may have shown a star on one and the author could not say. | one of three landed |
| `route inbox --export Music/9-24-export-2.xml`, the proof | to the gate, answered abort | Plans the same 259 destinations and the same 4 ratings again, and no long track, which is the one thing that landed. Not the "routes, rates and adds nothing" the pending text promises. | measured, nothing written |

Line 3 of #178 is ticked, because its record is this table and not because
the bridge landed it: the routing pass ran correctly on a fresh export, its
file was right byte for byte, and of the three things the line asked to see
in rekordbox the long track playlist landed, the memberships did not and the
ratings did not. **Decided by the author: stop, delete the three stray root
playlists in rekordbox, keep `Sets and Long Tracks`, leave the 61 rows in
their INBOX playlists.** The memberships wait for the tree's database
cutover, `route inbox` without `--export`, which is the mechanism built for
this and U29's per workflow choice. Filed R-685 to R-688, R-679 CLOSED live.
R-678 held on both intake verbs. R-682 read again: the by reason counts still
come off the artifacts.

## Sitting 11, 2026-09-24, evening

Machine state before: the volume mounted, rekordbox and its agent closed by
the author for the whole sitting, the pipx install at `40daec7`, the Cratekit
Relay feeder building #202 to #204. Driven from the attended worktree and the
pipx install, so nothing merged to main until the feeder had left after #204.
No acknowledgment was minted: nothing this sitting wrote the database.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| A4 #177, the Rating scale | yes, on a disposable copy | The live database copied once with its wal and shm, opened through `rb_writer.open_db`. Distinct `Rating` on the 9,998 rows not soft deleted: 0 on 539, 1 on 1,659, 2 on 996, 3 on 2,994, 4 on 1,434, 5 on 2,376. **The database stores stars, 0 to 5.** R-414 narrowed to its planner half, filed for the feeder, with the fold pinned at the database boundary by the author. | read, #177 closes |
| A3 #176, the Name padding count | yes, on a disposable copy | `plan_title_padding` plan only with the naming verb's template: 9,756 headed titles, **13 unpadded**, every change on the key span alone. **Decided by the author:** the thirteen stay as they are for now and the planner is kept. R-165 stays open with the count. | read, #176 closes |
| #212's taxonomy step | yes | `[long_tracks]` appended to the active taxonomy copy on the volume after a dated backup beside it. `core.active_taxonomy.load` reads `LongTracks(over_seconds=1200)` and doctor's `taxonomy.active` is ok. | done |
| A5 line 10, `name apply` plan only | to the gate, answered abort | Run `2026-09-24T21:03:23Z-ee30`, 16 seconds over the library root: **5,205 files, 5,144 referenced and held, 61 renames, 0 collisions, 0 unnamed.** Every rename pads a single digit key on a file the collection does not reference, 27 of them in one sample pack folder. Some held names repeat the title around the artist, `Title - Artist - Title`, read and not measured. | measured, nothing written |
| A7 #213, `sync labels` | yes, job `2026-09-24T20:45:49Z-c519` | 47 labels, **27 swept, 20 failed** on `TooManyRequests` and recorded permanent (R-704). A fresh copy of the review queue after: **55 of the 98 addressed rows now carry the artist's name**, 43 still carry an address, all under five labels the limit cut off, Anjunadeep 33. The sweep also offered **1,701 new releases**, so the unresolved label rows are 1,799 across 28 labels. | partial, #213 stays open |
| A5 line 7, `analyze vocals --recursive` over the library | running | Job `2026-09-24T21:04:27Z-fbe8`, 9,929 tracks at about twenty a minute, left running overnight. The calibration and the filing pass come after it and after #212. | running |
| A5 line 6, the typed tracklist | yes | A screenshot of a 24 line tracklist typed into a text list, `intake missing --list`: **1 listed by search, 2 owned, 13 near misses offered for review, 8 found nothing.** | live |
| A5 line 6, the set | yes, split | A 5 hour 5 minute mix URL refused at 732 calls against the bound of 400, nothing spent (R-706). Fetched, split into two even halves by hand, each identified: Part A job `8c68`, 24 tracks, 366 calls; Part B job `ae42`, 28 tracks, 6 owned, 366 calls. `intake missing --job` on each: 10 and 8 listed by ISRC, 14 and 14 unlisted, most of them an ISRC the provider files under several releases. | live, split by hand |
| A5 line 6, the downloads | yes, twice | First, all 19 failed `the downloader reported no file` on available lossless tracks. The downloader's own lookup, repeated outside it, answered `TooManyRequests`; the tool swallows it (R-703) and the label sweep beside it had spent the allowance (R-705). About ten minutes after the sweep ended the limit cleared and **all 18 unique tracks landed** as FLAC in Downloads; the one track on both lists was refused `output-exists` on its second copy, correctly. | cut over through the download |

Line 6 of #178 is ticked for the set, the typed tracklist and the fallback
search and download; tagging, naming and landing the 18 wait for rekordbox to
be free after the vocal pass. Line 10 is ticked with the plan above. Filed
R-703 to R-706.

## Sitting 12, 2026-09-25, morning

Machine state before: the volume mounted, rekordbox and its agent closed, the
overnight vocal job `fbe8` succeeded, 9,929 settled, 4,153 scored, 5,762
unchanged, 14 inactive, 10 too large and 4 undecodable. The pipx install
brought from `40daec7` to `1fb3132`, so #202's gate and #214's star fold are
in it; `crate doctor` exit 0, backup ages 8 and 8 days. The author deleted the
three stray root playlists, kept `Sets and Long Tracks` and took a fresh
export. No acknowledgment was minted: nothing this sitting wrote the database.
Driven on a disposable copy of `master.db`, taken with rekordbox closed and no
wal beside it, through a temporary config and state directory, the copy's
config carrying `db_outside_root_acknowledged_on` since the copy sits off the
volume.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| #212, `route inbox` plan only | to the gate, answered abort | Run `082e`: intake `<library root>/INBOX`, **0 tracks**, trees none, the no native tree warning. The folder does not exist, and the path files files in a folder, never rows in the rekordbox INBOX playlist, so **the 61 rows are not this verb's** (R-723). A row in the collection no tree places is `route unplaced`'s, after a cutover. | measured, nothing written |
| `route unplaced`, plan only | yes | `no_op`, `no-native-tree`: no tree has cut over. | measured |
| `adopt scan`, the census | yes, job `08c6` | 9,998 rows settled in 25 seconds. | measured |
| `adopt apply` plan only | to the gate, answered abort | Run `b78a`, tree `genre_energy`: 7,773 route, 2,058 need a genre, 167 excluded, 153 unmapped, 14 not a path, no collisions, digest `52efe350cfdf9bb8`. **7,401 of the 7,773 route to their bucket's Unsorted sub, none to an energy sub.** Adoption passes no energy by design, and `tags.read_energy_from_file` over the same 7,773 files reads **7,726 with a reading, 47 without** (R-722). | measured, nothing written |

**Decided by the author: no live write, diagnose, then file.** #212 cannot
run as its brief was written. The database path reaches the 61 rows only
through adoption, then `route unplaced`, and adoption as it stands would add
7,401 tracks to Unsorted beside their energy subs through a one way door.
Filed R-722, on the board bar, and R-723. #212's brief rewritten around
adoption, waiting on R-722.

## Sitting 13, 2026-09-25, afternoon into the night

Machine state before: the volume mounted, rekordbox and its agent closed, the
pipx install brought from `1fb3132` to `6a45398`, so R-722 is in it; `crate
doctor` ok, backup ages 9 and 9 days, two sessions open. No acknowledgment was
minted: nothing this sitting wrote the database. The copy was taken with
rekordbox closed and no wal beside it, its sha256 equal to the live file's,
driven through a temporary config and state directory.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `adopt scan`, the census | yes, on a disposable copy, job `d45b` | 9,998 rows settled in 39 seconds. | measured |
| `adopt apply` plan only | to the gate, answered abort, run `792b` | Tree `genre_energy`: 7,773 route, 2,058 need a genre, 167 excluded, 153 unmapped, 14 not a path, no collisions, digest `5eca58df932496a3`. The plan's energy tally over 9,831 readable files: **9,769 read, 62 absent, 0 unreadable.** Of the 7,773 routed, **45 go to an Unsorted sub**, against 7,401 at sitting 12. 47 routed files carry no reading: the 45, and 2 under `non_electronic`'s `soul_rnb`, a sub chosen by genre. That is sitting 12's 47. R-722 holds live. | measured, nothing written |
| `backup run`, the fresh backup #212 asks for | started, cancelled | Job `2026-09-25T18:10:37Z-7d21`. After 8 hours 40 minutes the mirror had sent 7.9 GB at about 2 MB/s. **4,274 files, 196 GB, changed on the volume since the last backup**, most likely the overnight vocal job's tag writes making rclone upload each whole file again (the count is near its 4,153 scored, not matched by identity). About 26 hours remained. Cancelled by the author's decision with an interrupt to rclone; the job reads cancelled and resumable, both ages stay 9 days. | stopped, resumable |

**Found while preparing the live step, not yet driven.** `adopt apply` writes
memberships only; the verb passes no tag writer, so no audio file changes. But
the membership writer refuses a tree still on the xml bridge through
`tree_registry.anchored_root`, sitting 12 measured that no tree has cut over,
and nothing in `src` calls `tree_registry.flip` or `record_cutover`. So an
approved live adoption may pass the one way door's gate and then refuse every
membership. Drive it before any live approval. **The adoption ledger is
library scoped**, `adoption_ledger.json` under `.cratekit` on the volume, so an
approval on a disposable copy with only the config and state directory
redirected would mark the live library's entries applied. A copy run that
approves needs the library root redirected too.

## Sitting 14, 2026-09-27

Machine state before: the volume mounted, rekordbox and its agent closed.
**rekordbox had been updated to 7.2.19.0342 for a security concern**, so the
sitting opened on a failed `rekordbox.pins`. The pipx install brought from
`6a45398` to `65532c0`, the R-235 merge, with its extras kept. Backup ages 1
and 10 days at the start. The acknowledgment was minted by the author from a
Terminal window at 21:05Z, valid twelve hours. The copy was taken with
rekordbox closed, its sha256 equal to the live file's, driven through a
temporary config and state directory **with library state redirected as
well**, by pointing `library.state_dirname` at a scratch directory on the
volume rather than moving the library root, since a moved root puts every
file outside it. Both gates named the scratch registry and the scratch
database before they were answered.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The 7.2.19 database, read | yes, on a disposable copy | Opened through `rb_writer.read_only_copy`: the key decrypts under pyrekordbox 0.4.4, schema version 6000, `integrity_check` ok, 17,402 content rows, 9,998 active, 577 playlists, 19,236 memberships, library sync off. | measured |
| The re-pin | by hand | `pinned_app_version` set to `7.2.19.0342` in the configuration file, `validated_on` left unset. Doctor ok. No verb does this (R-732). | live |
| `backup run`, job `11b2` | yes | Succeeded, 2 of 2, about 55 minutes. Both ages 0 days. | live |
| #220, the cutover verb | built by Relay | Landed in 1 hour 1 minute. The first launch halted in 54 seconds on `head_equals_remote`, `main` eight documentation commits ahead of the remote, and ran after a push. | merged |
| `tree cutover genre_energy`, on the copy | to the gate, approved | One root found, `BY GENRE + ENERGY`, row 3976565623, all four prechecks passed against `Music/9-25-export.xml`, digest `55075882cc692d3e`. Recorded in the scratch registry. The live registry was not created. The answer after approval is `ok` and a run (R-730). | proven on a copy |
| `adopt scan` then `adopt apply`, on the copy | approved | The plan is sitting 13's to the digit, digest `5eca58df932496a3`, 7,773 routed, energy 9,769 read and 62 absent. The first approval was spent on a missing acknowledgment (R-733). The second ran 4 minutes 24 seconds: **7,073 already present, 700 added**, no playlist created, 577 before and after, Unsorted subs 13 to 58, the plan's 45, every BPM unchanged, `integrity_check` ok. | proven on a copy |
| What the 700 are | measured | **569 tracks gained a second band sub beside the one they held**, 331 Med to High, 215 Med to Low, 19 High to Med, 4 High to Low. 15 gained a second style sub under `NonElectronic`. 107 had no place in the tree and 9 sat beside `with vox` or `Candy` alone. The live database already holds 37 tracks in two bands of one bucket. | measured, R-731 |

**Stopped before the live step.** The cutover verb works and adoption lands
membership through the database, which is what #220 owed. Adoption as it
stands would double file 569 tracks through the one way door, and the gate
does not show it. Filed R-731, on the board bar, and R-732 and R-733. The
live database and the live library state were not written: the live file's
sha256 was the same after the copy run as before it. The scratch state
directory was removed at the end of the sitting.

## Sitting 15, 2026-09-28 and 2026-09-29

Machine state before: the volume mounted, rekordbox and its agent closed,
the pipx install brought from `65532c0` to `7ebb07f`, the R-731 merge, with
its extras kept. The live database's sha256 was the one sitting 14 copied,
unchanged since 2026-09-26, so the database backup of 2026-09-27 was still an
exact copy of it. Acknowledgments minted by the author from a Terminal window
on both days, the second at 17:07Z on the 29th, **before any gate was
answered**. Copy runs isolated library state through `library.state_dirname`
as sitting 14 did. The author answered every live gate from Terminal; the
session drove the verbs and answered the gates on the copy.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The rehearsal, `tree cutover` then `adopt apply` on a copy | approved, 2026-09-28 | Plan digest `e67844ef76b53a36`: 7,188 route, **585 withheld by placement, 569 band and 16 style**, one style more than sitting 14 counted by hand. Applied: **115 added, 7,073 already present, none failed**, no track given a second band sub, 577 playlists before and after, every BPM unchanged, `integrity_check` ok. | proven on a copy, R-731 holds |
| `tree cutover genre_energy`, LIVE | approved by the author, run `c5f9` | Root `BY GENRE + ENERGY`, row 3976565623, all four prechecks passed against `Music/9-25-export.xml`. Doctor: database native, anchored since 2026-09-29. | **cut over** |
| `adopt apply`, LIVE | approved by the author, run `2db1`, job `24e9` | The plan's digest was the rehearsal's, `e67844ef76b53a36`. **115 added, 7,073 already present, none failed.** Read back against the rehearsal copy: every membership, every playlist row and every content row's BPM, rating and path the same. 11,391 memberships under the tree. | **live, the first native write** |
| rekordbox, opened by the author | yes | Opened on 7.2.19 with no warning. The tree read as before, and two of the 115 were found by eye where the plan put them. The author deleted eight empty `CUE Analysis Playlist` rows, rekordbox's own, and a stray root `2026-Q3` whose 40 tracks all sat in `Favorites / 2026-Q3` in the 9-25 export, an import landed at the root (R-687's shape on another tree). 568 playlists after. | read |
| The pin | by hand | `validated_on = "2026-09-29"` recorded, now there is a write to name. | live |
| `route unplaced`, database path | on a copy | A report, not a write: no gate, nothing changed. **184 of 9,998 rows are placed by no governed tree.** 13 are streaming rows, 20 carry no genre, the rest carry one and sit outside what adoption could read. The human rendering is `ok` and a run (R-730's class). | measured |
| The 61 rows of sitting 10 | read | **47 are in the tree**, 40 of the 54 in one batch and all 7 of the other, filed by the adoption. **14 carry no genre** and cannot be routed until they are tagged. | 47 landed, 14 owed a genre |
| `route pending` | on a copy | `no_op`, nothing pending. Doctor reads six recorded sessions, none open. | nothing to do |

**#212 is done.** The routing tree is on the database, the first native write
landed and was read back, and rekordbox opened on it. A revert is now refused
by design. Line 3 of #178 has its memberships through the database. The 585
withheld entries are in the plan of run `2db1` for the author's decision on
which reading is right, the tag or the placement.

## Sitting 16, 2026-09-29, afternoon

Machine state before: as sitting 15 left it, the same day. rekordbox closed
for every verb and opened by the author for the two exports and the import.
The acknowledgment of 17:07Z held throughout.

The 18 downloads of sitting 11, through the whole tail. This is step 4 of the
road map and the first time an acquired file has gone from staging to a
folder in the tree with no xml routing.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `tag folder` over staging | yes, job `0db5` | 18 settled in seconds. **12 given a genre, 6 none**, every file already carrying art. Two genres read wrong to the session, a 1976 soul record under Breaks and two house remixes under Afro House; the author set genres in rekordbox instead. | live |
| `analyze run` | yes, job `33ea` | Key and tempo on all 18, each file renamed with its head, no tempo tag written. **Energy on none: `uncalibrated`** (R-742). | live, energy missing |
| The energy calibration | carried by hand | The source system's, tested first: **59 of 59 sampled library tracks scored equal to their tag**. Written through `save_calibration`. | live |
| `analyze restamp` | yes, job `4604` | Energy stamped on all 18, 1 to 10. The verb warns that its star rating half is not written by this build. | live |
| `name apply --root` staging | two plans, the second applied | The first planned 19, one of them a refused duplicate inside the acquire job's directory (R-741). Aborted, the leftover moved aside, 18 renamed, no collision. | live |
| `intake land` | applied, run `76bb` | 18 moved to `Music/2026-09-29-sitting11-sets`, the intake file written over `Music/9-29-export.xml`, 10,016 entries. The 18 new entries carry no tempo element and no average BPM, and no existing entry's tempo data differs from the export. **Every new Name is bare** (R-740). | live, Name defective |
| The rekordbox import | by the author | One playlist imported, dragged into INBOX, Reload Tags over the 18 to restore the heads, genres set by hand on seven. rekordbox computed its own grids. | done |
| `intake imported` | yes | Proven imported, 18 tracks, the intake file retired. | live |
| `adopt scan` then `adopt apply` | approved by the author, run `0a1b` | 10,016 rows. Plan: 7,205 route, 585 withheld, digest `11be33c33f377e53`. **17 added, 7,188 already present, none failed.** Read back: each of the 17 in the one sub the plan named, the eighteenth, which carries no genre, in none. 11,408 memberships under the tree, `integrity_check` ok. | **live** |

**Step 4 is done.** Found by running: R-740 to R-744. R-740 is on the board
bar. The 9-27 database backup predates today's writes; a backup is owed
before the next sitting.

## Sitting 17, 2026-09-29, evening

Machine state before: rekordbox closed, the pipx install at `7ebb07f`,
backup job `0cb8` finished at about 17:10 local, both ages 0 days. **The
author turned on desktop control for the session and changed the rule**: an
attended session may open, drive and quit rekordbox on the live library, and
approves a database write gate when its digest equals a rehearsal's. `CLAUDE.md`
carries both. The acknowledgment of 17:07Z held. The Relay feeder was
building #222 and #223 throughout, which sitting 17 paid for below.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Desktop control, read | by the session | rekordbox opened in under 20 seconds, the playlist tree and track rows read from a screenshot, quit, both processes gone within 5 seconds. The window shows 9,865 tracks against 10,016 active rows: the 151 are 137 Tidal and 14 SoundCloud streaming rows. | works |
| Desktop control, drag | by the session | An empty playlist dragged into INBOX and back to the root, each on the first attempt. Read back from the database: parent `root`, 569 playlists, 19,346 memberships, integrity ok. A drag is pressed, moved in steps, held, and released once the target is outlined. | works |
| A8, #225, the rehearsal | on copies | Through `commit_guarded`: refused, both rows, rolled back (R-760). Raw, the binding's `add_content`: two rows, gridless, integrity ok, digest `055b509b1b5d7144`, twice. | measured |
| A8, the live insert | run by the author | The session's own attempt was refused by its safety classifier, so the author ran the same script. A copy of the database was kept in library state history first. Digest before commit equal to the rehearsal's. 17,420 to 17,422 content rows. Row A in rekordbox's own not yet analysed shape, row B the binding's default, both stored under the base drive prefix. | live |
| A8, launch 1, Auto Analysis off | by the session | **No dialog.** Both rows shown, 9,867 tracks, BPM 0.00, no waveform. After the quit, both rows unchanged in the database. | clean |
| A8, launch 2, Analyze Tracks from the menu | by the session | Both analysed inside 30 seconds. **124.00 in 7A and 117.00 in 8A, which is what the files' own names say.** `Analysed` 105, the analysis files under `PIONEER/Master/share/PIONEER/USBANLZ` in the folder each row's UUID named, one mixer row and four or five file rows each. Artwork on the file that carries a picture. | clean |
| A8, launch 3 | by the session | No dialog, both rows unchanged, integrity ok. | clean |
| The two rows kept | by the session, at the author's word | Reload Tags gave them their titles, artists and one genre. The spike playlist deleted through its dialog. 10,018 active rows, 569 playlists, 19,346 memberships. | done |

**The verdict of A8 is CLEAN**, by the outcome table of
`DJ_tools/docs/runbooks/2026-08-01-u9-A1-gridless-insert-notes.md`: a row
inserted through the database is accepted by rekordbox 7.2.19, analysed on
request, and stable across three launches. Intake can leave the xml bridge
and #224 is buildable. What the writer must do: store the base drive prefix,
choose the device whose `MasterDBID` is the library's, and ask for analysis,
since with Auto Analysis off rekordbox analyses nothing on its own.

**What the sitting cost.** #223 was refused at its gate on a timing test
while the machine was busy, and then excluded (R-759). It was landed by hand
after two green batteries. **rekordbox and a Relay build do not run at the
same time.** Filed R-757 to R-760.

## Sitting 18, 2026-09-29, evening, unattended to the import

The author authorised Tidal verbs from the session and asked it to continue
without him. rekordbox stayed closed and nothing wrote the database, since
the rule for both is an attended session. The feeder was stopped, by the
lesson of R-759. The pipx install brought to `11c4081`.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `intake playlist favorites` | yes, job `8b37` | **218 declared, 209 listed, 9 withheld.** 8 provider calls, no rate limit. Resolved: 205 owned, 2 offered, 2 missing, 0 suppressed, each with its reasons printed (R-682 holding). | live |
| `intake missing --job` | yes | 2 listed. | live |
| `acquire download` | yes, job `7308` | **1 landed, 1 refused `lossy-refused`**, the provider offers `Calvin Harris :: Satisfy` in a lossy format only, as sitting 10 read. 9 provider calls, no rate limit. The job reads failed, permanently, over one durable success. | live |
| `tag folder`, `analyze run`, `analyze restamp` | yes | One file. No genre found. Key 03B, tempo 144, **energy 4 stamped by `analyze run` itself** now a calibration exists, no tempo tag. | live |
| `name apply --root` | applied | One rename, no collision, nothing left in the acquire staging directory this time. | live |
| `crate export collection`, the first live use | yes | 10,018 active tracks, 76 folders, 493 playlists, 18,761 memberships, 7.5 MB, under a minute. Against the export rekordbox wrote that afternoon: **the same 493 playlist paths, none only in one**, 14 playlists larger by the 17 adopted since, 2 more tracks. No tempo element and no average BPM on any track. | live, #223 proven |
| `intake land` over that export | applied, run `b7f7` | One file to `Music/2026-09-29-favorites`. **The intake file's Name is `03B - 144 - Same Girl (with Usher)`, the head kept**, no tempo data, the batch playlist under INBOX. Ends pending the import. | live, #222 proven |

**Stopped at the import.** Owed to the next attended sitting: import the
batch, `intake imported`, a genre for the track, then `adopt scan` and
`adopt apply` with the two rows sitting 17 kept.

## Sitting 19, 2026-09-29, 19:36 to 19:49, attended, the import through desktop control

Run while #227 built and clear of its gate, with the acknowledgment of
17:07Z still held. The session drove the whole rekordbox side itself, the
first time from the landing to the tree with no hand step but the
acknowledgment.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The import, by desktop control | by the session | Imported Library set through the Browse dialog. The one playlist `2026-09-29-favorites_inboxed` imported from the rekordbox xml view. Analyze Track run. Two genres set in the Info panel. | works |
| The drag into INBOX | by the session, twice | **The first drag landed BESIDE INBOX at the root**, released on an insertion line. The second, released only once INBOX showed a box outline, landed inside. Rule: zoom and see the box before release. | works on the second attempt |
| rekordbox's analysis of the landed file | read from the screen | **140.00 in 2B. Cratekit's head says `03B - 144`.** One more case for R-744. | measured |
| `intake imported` over `crate export collection` | run, then run again on a copy | **Matched nothing, `PENDING_HUMAN`.** The export writes `Location` under `BaseDBDrive`, the base drive's own mount name; rekordbox's own export writes the current drive. Given a copy of the file with the prefix replaced by `sed`: proven imported, 1 track, the intake file retired. | defect, on the board bar |
| `adopt apply`, the rehearsal | on a copy, state redirected | Added 3, already present 7,205, digest `5fbb8e409f42c727`. | measured |
| `adopt apply`, live | approved by the session | Plan digest equal to the rehearsal's. **The session approved the live gate itself, the first time under the rule of 2026-09-29.** Added 3, 7,205 already present, none failed, integrity ok, 19,350 memberships, 570 playlists. | live |

**Landed:** In The Air Tonight to House / Funky House / Disco / High. Didn't
See It Coming to Downtempo / Low. Same Girl to NonElectronic / Soul / R&B.

**Step 5 of the road map is DONE for the favourites source**: account to
tree, one track, no hand step but the acknowledgment.

**Left for the author, and decided by him the same evening.** The inserted
MONKYMAN row duplicates a track already in the library from another folder,
`Processed_Tracks/2025/10_10_25`: two rows, two files, one recording. He
chose to keep the older row and remove the experiment's row `253549430` from
the collection, file kept. A search filter `Amal Nemer` may still be set in
the collection view.

**The defect.** `intake imported` cannot finish over the export this
product writes, which is a workflow a DJ needs, so it is on the board bar.
`write/collection_export.py` takes `FolderPath` as the database holds it and
`_location` encodes it unchanged, so every `Location` carries the base
drive; `intake imported` digests the decoded path and compares it with the
landed file's mounted path, and `library.location_prefix_map`, the one rule
that joins the two spellings, is applied by neither. Filed as R-773, with
its issue.

## Sitting 20, 2026-09-29 evening to 2026-09-30 morning, the decisions of the evening

Meant to run unattended overnight. It did not: at 22:40 the session asked
desktop control for one more application, whose transparent full screen
window was refusing clicks into rekordbox, and that request waited on an
approval dialog until the author clicked it at 08:30. The feeder had been
stopped at 23:08 for the rekordbox step and stayed stopped all night.
Nothing was lost and nothing was built. The lesson is in the record below.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The two version match items of job `8b37` | resolved rejected by the session, 2026-09-29 | Fractals and I'll Find My Way To You, each held in another version. A rejection is a missing row and hands the track to acquisition. | done |
| Calvin Harris, Satisfy, the lossy copy | read, not run | `lossless_policy` is one global switch, `strict` or `allow_lossy_marked`, with no per track exception by design (R21), and `acquire fallback-fetch` refuses under `strict` before it downloads. No verb takes one exception. Left refused. | recorded, not acted on |
| The MONKYMAN duplicate row | by the session in rekordbox, 08:31 | Row `253549430`, the experiment's file under the 10_25_25 folder, created 9/29/26, play count 0, removed from the collection through its dialog. Row `147268321`, play count 8, kept. File kept. 9,867 tracks shown, 10,018 active rows. No search filter was set; none was left. | done |
| The favourites cycle, second pass | by the session, 08:33 to 08:37 | `intake playlist favorites` job `269b`: 218 declared, 209 listed, 9 withheld, **206 owned, 3 missing** (2 by verdict, Satisfy). 8 provider calls. `acquire download` job `c50f`: **2 landed, Satisfy `lossy-refused`**, 15 calls, no rate limit. Tag, `analyze run`, `analyze restamp` (energy stamped), `name apply` (2 renames from the files' own tags, the answered run resumed with `--run`). `crate export collection`: 10,018 rows, 494 playlists, no tempo. `intake land` run `812d`: 2 files into `Music/2026-09-30-favorites`, intake file `2026-09-30-favorites_inboxed.xml`. | landed, pending the import |
| `adopt move`, R-758's verification, the rehearsal | on a copy, state redirected | **618 moves, 605 band and 13 style, 581 memberships added and 618 removed, 4 left** whose genre names no style, digest `a2237b5eff650c14`. Of the 618, 37 already held their target and only lost the stale sub (R-734's shape). Applied in 13 seconds. Read back: 19,349 to 19,311 memberships, 619 rows soft deleted because one pair was held twice, every BPM unchanged, integrity ok, band doubles per bucket **40 down to 6**. | measured |
| `adopt move`, live | approved by the session on an equal digest, 09:00 | Plan digest `a2237b5eff650c14`, every plan row identical to the rehearsal's. Snapshot `2026-09-30T130022Z` first. Read back equal to the copy on every count, the active membership set identical. **The 585 withheld of sitting 15 and the 37 of R-734 are in the sub their file names.** | live, R-758 verified |

**The six doubles the move leaves.** Four are one pair held twice in the
same sub, duplicate rows rekordbox made, not two subs. Two are tracks that
held two band subs before adoption ran and whose reading names one of
them: `adopt apply` counted them already present and withheld nothing, so
`adopt move`, which plans from adoption's withheld list, never sees them.
Nations in Organic House, Med and High. Mumbling Yeah in Minimal / Deep
Tech, Low Energy and Med Energy. Filed as R-780 and R-781.

**Owed.** The import of `2026-09-30-favorites_inboxed` through desktop
control once the feeder is idle, then `intake imported` over a written
export, which R-773 (#229) makes possible without a hand edit, then
`adopt scan` and `adopt apply` for the two rows. rekordbox's own view of
the moved subs, which is R-761's close.

## Sitting 21, 2026-09-30, 12:24 to 12:41, attended, the second favourites batch to the tree

The author freed the screen for the import, with the feeder idle and
stopped. rekordbox opened by the session, driven, quit, both processes
gone before any verb.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The import, by desktop control | by the session | Imported Library set to the day's intake file through Preferences. The one playlist imported from the rekordbox xml view. 9,869 tracks shown, the two rows at the top with BPM 0.00. | works |
| The drag into INBOX | by the session, one attempt | **No box outline appears on a folder the drag has already expanded.** The insertion line above INBOX is the root; the line below it, at the children's indent, is the first place inside. Released there: `2026-09-30-favorites_inboxed` under INBOX at position 1, read back from the database. | works, the rule refined |
| Analyze Tracks, both rows | by the session | Fractals **123.00 in 4A, equal to Cratekit's head**. I'll Find My Way To You **120.00 in 3B against Cratekit's `04B - 117`**, a second case for R-744. Genres already on both from the tagger, no Reload Tags needed since #222. | measured |
| The moved subs, rekordbox's own view | read from the screen | Organic House: Low 359, Med 394, High 318. The database reads 359, 395, 318, every Med row on an active, distinct track. One display count, cause not found. | R-761 closed |
| `crate export collection`, after #229 | yes | 10,020 rows, 495 playlists, no tempo. **9,853 Locations under the mounted root, none under the base drive.** A new warning names the 153 rows no rule maps. | R-773 live |
| `intake imported` over it | yes, no hand edit | **Proven imported, 2 tracks, intake file retired.** The first time on a file this product wrote. | R-773 closed live |
| `adopt scan` then `adopt apply`, the rehearsal | on a copy, state redirected | Route 7,790, withheld 4, digest `2c9e9f90b60aecad`. Applied: 2 added, 19,313 to 19,315, both rows in their bucket's Med sub. | measured |
| `adopt apply`, live | approved by the session on an equal digest | Read back equal to the copy on every count. Fractals in Melodic House / Med, I'll Find My Way To You in Tech House / Med. | live |

**The favourites cycle has run end to end twice**, the second time with no
hand edit and no hand step but the acknowledgment and the screen.

## Sitting 22, 2026-09-30, unattended, the head against rekordbox's own analysis (R-744, issue #232)

No rekordbox opened, no verb run on the live library. Every read was off a
disposable copy of the database through `rb_writer.read_only_copy`, and the
audio was read from the mounted library, nothing written beside it.

**Which rows measure rekordbox.** 9,776 rows carry a head. The back
catalogue's stored tempo is the grid the source system wrote at import,
the same integer its head carries, so those rows agree with themselves:
73.8% equal, 25.3% off by one to three, nothing measured. A stored tempo
with a fraction was computed by rekordbox, since no tool that fed this
library writes one. 1,361 rows are so, 1,345 on disk, 1,325 with a head.
That sample leans to tracks with an unquantised pulse, classical and live
recordings among them, and understates agreement on programmed music. The
22 rows this product headed at sittings 16 to 21 and rekordbox then analysed
are the only clean sample of the intake and are reported beside it.

**The tempo, every 4th of the 1,325, 299 measured.** The detector was run
over each file's stored tempogram, so every estimator below saw the same
autocorrelation.

| estimator | equal | within one | off one to three | half or double | other level |
|---|---|---|---|---|---|
| shipped before this unit, librosa's strongest bin, no window | 39 | 106 | 191 | 10 | 59 |
| window 80 to 160, no prior, strongest bin | 40 | 108 | 180 | 1 | 78 |
| window 80 to 160, no prior, interpolated | 171 | 204 | 55 | 1 | 72 |
| **window 80 to 160, prior at 120 over one octave, interpolated** | **193** | **225** | **54** | **1** | **51** |
| window 70 to 180, prior, interpolated | 188 | 217 | 51 | 9 | 51 |
| window 85 to 170, prior, interpolated | 190 | 220 | 52 | 6 | 51 |
| window 90 to 180, prior, interpolated | 176 | 207 | 56 | 15 | 52 |
| the source system's heads on the same files, for reference | 265 | | 23 | 2 | 6 |

The interpolation is the whole of the off by one to three bucket: a
tempogram bin at this rate and hop is about six beats wide near 128. The
window removes the octave cases. The prior is worth 22 exact agreements
over a flat window. Eight prior widths and centres were tried; none beat
the one librosa defaults to. The shipped estimator after the review's
edge clamp reads **194, 226, 53, 1, 51**, one row moved. On the 22 intake
files: **16 equal, 17 within one, 4 off by one to three, 2 other level**,
against 15, 16 and 3 before.

**The other level bucket is the method's.** 51 of 299, 17%, a pulse read
at three to two or four to three of rekordbox's, 123 against 97.55, 117
against 87.50, 93 against 140.09. No window resolves a ratio inside the
window. It is recorded in the run's answer as the rate.

**The key, the same 299 and the 22.** Four templates against four chroma
profiles, scored offline on profiles stored per file.

| chroma | template | 299 equal | fifth | relative | parallel | other | 22 equal |
|---|---|---|---|---|---|---|---|
| **harmonic mean, as shipped** | **Krumhansl and Kessler** | **158** | 43 | 18 | 22 | 58 | **19** |
| harmonic mean | EDMA | 166 | 51 | 18 | 13 | 51 | 15 |
| harmonic mean | Shaath | 168 | 41 | 18 | 25 | 47 | 16 |
| harmonic mean | Temperley | 118 | 50 | 30 | 11 | 90 | 7 |
| harmonic median | Krumhansl and Kessler | 137 | 49 | 15 | 37 | 61 | 15 |
| raw CQT mean | Krumhansl and Kessler | 137 | 42 | 23 | 31 | 66 | 11 |
| STFT mean | EDMA | 165 | 43 | 23 | 21 | 47 | 10 |

Nothing beats the shipped detector on both samples, so it stays and the
rate is R-784. rekordbox's key names in this library are Camelot in two
paddings, `8A` and `08A`, and the comparison maps either padding and the
classic names to one padded code.

**How it was measured, since the first attempt was lost.** A
`multiprocessing.Pool` over the files hung after three results: workers
died in librosa's beat tracker, a numba segfault, and the pool waited on
their tasks for ever. The measurement was rerun as eight sequential shard
workers under a driver with a hard deadline that terminates them in
`finally`, each appending a line per file so a cut off run resumes. The
beat tracking refinement was dropped from the trial; the interpolation is
the product path. Loading and the tempogram cost about a second a file,
the harmonic separation for the key about twelve.

**What ships.** `analysis.tempo_floor` and `analysis.tempo_ceiling`, 80 and
160, both ends included, refused when empty. The interpolated estimator
held inside the window. `analysis/agreement.py` and
`scripts/head_agreement.py`, which print the four buckets over a
disposable copy and, with `--analyse N`, the detector's own rate. The run's
answer carries the record under `head_agreement` with `applies_to_window`.
Nothing writes a grid, a tempo, an average tempo or a key anywhere.

## Sitting 23, 2026-09-30, afternoon into the evening, the remaining lines driven

The author asked for every remaining line to be driven in order, with no
questions once the feeder drained and rekordbox used as needed. Relay ran
#231 and #232 alongside, both landed. The one question asked before that
rule was the hearts gate, answered sync on his word.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Line 4, `sync all`, the listing | yes, run `58f1` | **635 provider calls per listing**, the label registry sweep inside it, and the session listed twice by mistake to read a gate it had cut off. No rate limit. Sources queued: favourites out, favourites in, labels, four account playlists. The 9 withheld hearts surface on the inbound line as FAIL while its job queues anyway. | measured |
| The hearts, `sync favorites` | approved on the author's word, run `bd52` | **109 tracks hearted**, digest `27568912b4a103e5`, 297 calls, five tracks the provider no longer serves. The verb writes nothing locally. | live |
| Favourites in, job `76ed` | yes | 210 listed, 208 owned, 2 missing, 0 offered. | live |
| `sync labels`, job `2d20` | yes, three launches | Killed twice at the harness's 30 minute background cap, resumed each time from its queue with nothing repeated, the third launch detached. About one provider call a second, paced by the gate, no rate limit. **Still running at the stop, 20:41: 25,662 lifetime calls on the gate, 978 label releases filed into the review queue since 14:00**, left to finish on its own. | live |
| Line 7, `analyze calibrate --recursive`, on a copy | yes, 32 minutes | The vocal cut fitted at **16.0 by Otsu over 9,945 scored tracks, 386 above it**, the same 16.5 the author rejected by ear on 2026-09-17 for 5.0. The energy refit over 500 tracks gave an onset floor of 1.055 against the carried 0.921, validated 59 of 59. **Both fits discarded, the hand cut and the carried calibration stand.** | measured, decided against |
| Line 7, the filing gap | read from the database | 1,141 vox tagged tracks, 1,140 in a bucket, **12 in a bucket without its `with vox` sub**. `adopt apply` has no vocal logic; only `route inbox` files a vocal sub, per batch. | R-788 filed |
| #224's verification, the screenless half, on a copy | yes | `tree cutover inbox` approved on the copy, digest `7621ba1ce3c0eeb0`. `intake land` on a native intake tree, three files from download staging: **3 rows added, every one of the ten analysis columns NULL, no cue, mixer or file rows**, the playlist under INBOX in order, the device chosen by master id, paths under the base drive. A second approved run a no op. A folder inside the library but outside staging is refused as already owned. **`doctor` then fails `tree.registry` and tells the person to revert the record the verb just made.** | proven on the copy, R-787 filed |
| R-757's close, `crate backup run` timed | yes, 17:50 to 18:13 | **Mirror 1,183 seconds, 91,236 files compared, 200 sent.** | live |
| `crate backup run --full`, the same sitting | yes, 18:14 to 19:09 | **Mirror 3,103 seconds, 91,418 files compared, 2 sent.** `doctor` reads `backup.full_comparison` 0 days. | live, R-766 closed |
| Cards | filed on the author's word | #231 (R-780) and #232 (R-744), both landed by Relay the same afternoon. #232's own measurement workers segfaulted three times in librosa's beat tracker through numba; its session sharded and finished. | done |

**The sweep ended at 20:48**: 16 labels swept, 11 failed permanently as
unresolvable, the provider having no artist named exactly for each, 14,296
calls this run. The author had said to run the Tidal work and rekordbox
without asking, so the pass continued past the budget:

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The four playlist jobs | yes | 2 owned; 63 listed, 1 owned, 62 missing; 2 missing; 1 missing. | live |
| `intake missing --run 58f1` | yes | **67 missing as one list**, 211 owned, every job of the run succeeded. | live |
| `acquire download` | detached, 20:49 to 21:03 | **66 landed, Satisfy lossy refused**, 399 calls. | live |
| The tail, one detached script | 21:04 to 21:30 | 66 tagged, analysed, energy stamped; **62 renamed, 4 left with id names** since two pairs render to one name; export written; `intake land` as `2026-09-30-synced`, 66 files, intake file at the root. | live |
| The import, by desktop control | by the session, 21:31 to 21:36 | Imported Library set, the one playlist imported, 9,935 tracks, dragged into INBOX by the child indent line below it, first child, Analyze Tracks on all 66 with the default settings, quit, both processes gone. | works |
| `crate export collection` then `intake imported` | yes | **Proven imported, 66 tracks, no hand edit.** 10,086 active rows, 19,381 memberships, all 66 analysed by rekordbox, integrity ok. | live |
| `sync mark`, the first live one | to the gate, abort; then apply | **The file names the pass.** `intake missing --run` prints the name to land under, `<run>_synced`, and the session cut that line off and landed under its own, so the mark found no pass. A copy of the retired intake file under the pass's name found it: **four account playlists renamed with the DOWNLOADED prefix**, 1,248 calls. | live, line 4 done |

**Line 4 of #178 is done.** The full sync cycle ran from the account to
INBOX with one hand step, the acknowledgment, and the rows of this batch
reach the tree with `adopt apply` on the next one. The 978 label releases
in review are the author's to decide, after which `label approved` and a
download close line 5.

**Not done, and why.** #213's 98 label releases are the author's taste.
Line 8 needs a real player, line 9 a spare drive. A genre on the INBOX
rows without one is a judgment the tagger could not make from a provider
and the session did not make by ear.

## Sitting 24, 2026-10-01, attended, adopt apply for the synced batch

A fresh acknowledgment minted by the author at 09:09Z, valid twelve hours.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `adopt scan` then `adopt apply`, the rehearsal | on a copy, state redirected | Route 7,794, **needs-genre 2,121 (up 62)**, withheld 4, digest `22984f3e4523493f`. Applied: 4 memberships added, 19,381 to 19,385. | measured |
| `adopt apply`, live | approved by the session on an equal digest | Read back equal to the copy: 19,385 memberships, 572 playlists, every BPM unchanged, integrity ok. | live |

**Only 4 of the 66 synced rows reached a bucket.** The other 62 carry no
genre, since the tagger found none for them (live recordings and a catalogue
the provider does not tag), and adoption routes from the genre on the
database row, so they wait in INBOX. This is the genre owed by the author on
the INBOX rows, now 62 larger.

## Sitting 25, 2026-10-01, the newest 1% of each label, end to end

The author asked for the newest 1% of each label as a test, the rest another
day, and the session accepted it in review on that instruction, asking
nothing after that. Relay landed #235 alongside, and rekordbox opened only once it had.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `label approved` | 47 releases accepted by the author's rule, newest by album id per label | **186 tracks downloaded, 1,116 calls, no rate limit.** 12 already owned, 20 held as other versions for review. | live |
| `tag folder` on the 186, the code before #235 | yes | **137 genres written, 74%.** 38 no hit, 11 declined as Electronica, 6 written as Indie Tech, which the taxonomy has no place for. | live |
| `analyze run`, `analyze restamp`, `name apply`, `intake land` | yes, one detached chain | 186 analysed and stamped, 186 renamed with no collision, landed in their own folder with the label manifest. `tag retag` found 0 to correct, which is right: the 49 without a genre carry none, and retag replaces only a coarse genre already on a file. | live |
| Import through desktop control | yes | Collection 9,935 to 10,121. The playlist went into INBOX on a box outline over the expanded folder, as its last child. rekordbox analysed all 186 in about eight minutes. Both processes gone after quit. | live |
| `intake imported` | over a `crate export collection` | 186 proven, intake file retired, no hand edit. | live |
| `adopt apply` | rehearsed on a copy, live on an equal digest `22cdf5a16e947dd4` | **131 memberships added, 0 removed, no new duplicate**, every one a track with no place in the tree before. Route 7,925, needs-genre 2,176 (up 55: the 49 without a genre and the 6 Indie Tech). Live read back equal to the copy. | live |
| R-791's verification, `tag folder` after #235 | on copies of the 49 untagged files, outside the library | **Beatport 11 matched (all Electronica, declined as unmapped) and 38 miss. Traxsource and Bandcamp blocked on all 38 they were asked**, a 403 and a "Client Challenge" page. 38 files reported `sources-unread`, none `no-hit`, and `tag-folder-source-blocked` named both fallbacks. | proven, R-791 closes |

**What the tagger can do for a label download, measured.** On electronic
label releases Beatport alone finds about four in five. The fallbacks add
nothing from this machine because both refuse the client, and the tool will
not try to get past either. What is left needs a genre by hand or a new
catalogue, which is a card for the author to decide, not a fix.

## Sitting 26, 2026-10-01, afternoon, the attended steps of R-796, R-797 and R-798

The author asked the session to run the three cards' attended steps
itself. The build in use is main at the merge of #238, installed fresh.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The active taxonomy takes the new template | by the author, one command | The session's own write to the active copy was refused by its permission check, so the author ran the dated backup and the copy. The active copy equalled the old shipped template in content, read as parsed tables, so the new template whole is the same edit. `doctor` reads 19 buckets. | live |
| `adopt move`, R-797 | rehearsed on a copy with the new taxonomy, live on an equal digest `fc9f6031b9304ce5` | 41 moves: **39 tracks left `NonElectronic / Soul / R&B` for the top level R&B bands, 25 Low, 9 Med, 3 High, 2 Unsorted**, and two tracks holding two bands in a dance bucket lost one. Memberships 19,702 to 19,700, playlists 573 to 578, every BPM unchanged, integrity ok, live read back equal to the copy. | live, R-797 closes |
| `tag folder`, R-796, the 62 untagged playlist tracks | yes, in place | **60 of 62 written, 97%.** The general catalogue matched all 62 by ISRC: Rock 44, R&B 10, NonElectronic 4, Dance / Pop 2. Declined: one Singer & Songwriter, one Electro beside Beatport's Electronica. Traxsource and Bandcamp blocked on all 61 they were asked, named in the summary. | live, R-796 closes |
| `tag folder`, the label test folder | yes, in place | Of the 49 without a genre, the general catalogue matched 49 and **18 were written**: Dance / Pop 8, Hip-Hop 4, Rock 2, NonElectronic 2, House / Funky House / Disco 1, R&B 1. 31 declined as unmapped: Christian 10, Electro beside Electronica 10, Brazilian Music 8, Electro 2, African Music 1. | live |
| Reload Tags through desktop control | both batches | The genres reached the rows. Every BPM unchanged. A reload takes the key from the file, so a row rekordbox had analysed to another key now reads the key in its name. Both processes gone after quit. | live |
| `adopt apply` | rehearsed on a copy, live on an equal digest `e931e312685575b4` | **78 memberships added, none removed**, each a track with no place before: Rock 52, Dance / Pop 10, R&B 11, Hip-Hop 4, House / Funky House / Disco 1. Route 8,003, needs-genre 2,098. R&B holds 50. Live read back equal to the copy. | live |
| R-799, where the broad words landed | read from the database | **Pop is written as Dance / Pop and filed in the Dance / Pop bands**: 7 pop tracks by Torr, one each by Theo Katzman, CR and Magnus Ferrell now sit beside Le Youth. Alternative is written as NonElectronic and filed under Rock, 6 tracks. | measured, R-799 stands |
| `crate report genres` | yes | Two genres at 50 or more with no top level folder: **Progressive / Melodic, 630 tracks, claimed by no folder and falling to the fallback**, and Rock, 132, under NonElectronic. | read |
| `sync labels`, R-798's check | yes, detached, 15:59 to 20:41 | **30 labels swept, 0 releases filed, 0 held, 16,796 provider calls, no rate limit.** Every label's offer window was already full of the releases the sweep of sitting 23 left in review, 2,755 pending, so nothing new reached the gate and the gate was never asked. 17 items failed permanently, the labels the provider cannot resolve. The 36 of sitting 25 are owned now and are not asked about either. | run, **R-798's check still owed** |

**The gate cannot be shown by a sweep while the queue is full, R-815.** A
release already in review takes a place in its label's window and is not
judged again, so the 2,755 filed before the gate existed sit there
unjudged. `label approved` judges an accepted release by kind, which is the
only place the gate can act on them today. No label was marked with a kind:
which followed label is not a dance label is the author's to say.

## Sitting 27, 2026-10-02, overnight, the queue judged and what the session could not do

The author answered four questions on 2026-10-01: Rock stays flat,
Torromusic Recordings is unfollowed, the 36 non dance tracks of the label
test are removed, and Cratekit's key is the one a track keeps. Relay landed
#239, #240 and #241 first. The build in use is main at the merge of #241.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `label registry remove` | Torromusic Recordings | Gone from the followed labels. | live |
| `crate backup run` | yes, 02:11 to 03:12 | Mirror 3,293 seconds, 91,534 files compared, 2,094 sent, then the database folder. `doctor` reads both ages 0 days. | live |
| Removing the 36 from the collection | attempted through desktop control | The playlist filter showed the ten Torr tracks, the remove dialog opened, and **the session's permission check refused the confirming click**. The session cancelled the dialog. 186 rows in the folder before and after, 10,272 in the collection. | **not done, the author's** |
| rekordbox's KEY analysis | unticked in Preferences, Analysis | rekordbox no longer computes a key beside the one the file carries. Both processes gone after quit. | live |
| `crate label judge`, three labels, R-815 and R-798's check | after a copy of the review database off the volume | 406 items, 816 provider calls, 29 minutes. **379 judged, 149 held, 230 passed, 27 not judged.** Crew Love 98 held, rap and Latin releases by an artist of a similar name. Metanoia Music 51 held, rock and metal from the other label of that name, and 224 passed on Dance and Electro. Nite Grooves had nothing queued. | live, **R-798 proven** |
| `crate label judge`, the whole queue | yes, 03:46 to 06:23 | 2,602 items, 4,693 provider calls, no rate limit. **2,553 judged, 190 held, 2,363 passed, 49 not judged**, the catalogue unread for 2. Be One Records 89 held of 97, Nervous Records 33 of 51, Torromusic Recordings 19 of 23, Last Night On Earth 18 of 84, Multinotes 10 of 10, Amselcom 8, ALiVE Recordings 5, six others 8 between them. Anjunadeep 410, This Never Happened 330 and Stil vor Talent 194 passed whole. | live, **R-815 closes** |

**The queue now holds 2,416 releases and 339 are held, none rejected.**
`crate label held` lists each with the words the catalogue gave. Last Night
On Earth's 18 are worth the author's eye: 9 are called Pop, 4 Classical and
4 film scores, which may be the label's own releases under a broad word.

**`crate tag rows` was not rehearsed.** The verb asks for a backup
acknowledgment before it plans, the author's expired at 21:09Z on
2026-10-01, and only he mints one. R-799's run needs the active taxonomy
edited, which the session's permission check also refuses.

## Sitting 28, 2026-10-02, morning, the rows brought to their files

The author ran the taxonomy edit and minted the acknowledgment from his
Terminal that morning. The session's attempt to record it on his word was
refused by its permission check, which is the rule as written.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The active taxonomy takes R-799's template | by the author, after a dated backup | `doctor` reads 19 buckets and the copy carries `[vocabulary.deezer]`. | live |
| `crate tag remap`, R-799 | read at its gate, applied by the session | 78 files recorded from the general catalogue, 62 agree, **16 written and read back**: Dance / Pop to NonElectronic / Pop on 10, NonElectronic to Rock on 5, NonElectronic to Folk on 1. Digest `ec826897c78a99c4`. Files only. | live |
| `crate tag rows`, R-816 | rehearsed on a copy, live on an equal digest `3dbf848be3ab3619` | 10,272 rows: 8,660 agree, **797 written**, 637 file blank, 153 path unmapped, 14 no path, 1 file too coarse, 10 genre unknown. Progressive / Melodic to Melodic House 440 and to Progressive House 183, blank to Melodic House 136, Electronica to a specific word 23, six of the old word to other folders, three blank rows, the 6 remapped rows. On the copy every other column of every row read equal to live, memberships 19,778 and the genre table 106 rows unchanged, integrity ok; live read back equal to the copy. No pair replaced one specific word with another, so nothing needed `--leave`. | live, **R-816 closes** |
| The ten Pop rows | left by the verb | The library has no genre row named NonElectronic / Pop and the verb makes none, so the ten keep Dance / Pop on the row. Eight of the ten are among the 36 the author is removing. | owed, below |
| `crate report genres` | yes | **Progressive / Melodic is no longer named.** Rock, 138, is the one genre at 50 or more with no top level folder, and the author keeps it flat. | read |
| `adopt apply` | rehearsed on a copy, live on an equal digest `d1bb164795c8cb17` | Route 8,783, needs-genre 1,308, down 790. **One membership added**, a Steve Reich recording to Classical; the rest already sat where their genre names. 14 withheld, ten of them tracks in one band whose energy now plans another, left where they are. | live |

## Sitting 29, 2026-10-02, morning, R-799 closed

The author asked the session to make every rekordbox move itself. The
feeder was stopped by its stop file and left at 09:09, with nothing ready.
A Relay run in another repository, IW-597, was building at the time. The
build in use is main at the merge of #241, as at sitting 28.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Removing the 36 from the collection | through desktop control | Torr 10, Metanoia 10, Deodato 8, Robsoul 2, Bautista 1 and Flaco 1 removed, **32 of 36**, the playlist 186 to 154 and the collection 10,272 rows to 10,240. On the fifth removal, James Savage, **the session's permission check refused the click** and the session stopped there. The author then allowed desktop control in the project's permission rules, and the session removed the last four one at a time: James Savage "Better", Nerv "journey", CR "Tal Para Cual" and CR "FANCY". **The playlist reads 150, the collection 10,236 rows**, integrity ok, both processes gone after quit. | **36 done** |
| The genre row, R-818's hand step | in rekordbox's track information | Espresso and Pop Song given `NonElectronic / Pop`. The library now has that genre row. Return in the field reverts it and Tab commits it. BPM 104 and 98 unchanged. | live |
| The two out of their Dance / Pop bands | Remove from Playlist | Espresso out of High, 188 to 187; Pop Song out of Low, 154 to 153. Neither sits in Med, Candy, Unsorted or with vox. | live |
| Quit | menu | Both processes gone after quit. | live |
| `adopt scan` then `adopt apply` | rehearsed on a copy, live on an equal digest `367761445f6c62c9` | Route 8,771, needs-genre 1,289, withheld 13, no collisions, the 8,771 item lines identical between copy and live. **Two memberships added, both to NonElectronic / Pop**, none removed, no content row changed, 578 playlists before and after, 19,581 to 19,583 memberships, integrity ok. Live read back equal to the copy. | live |
| `crate tag remap` | to its gate, answered abort | 78 files, **78 agree, 0 to write**, digest `7c3964d209725f63`. | read |
| Rock and Folk | read from the database | All 123 rows whose genre is Rock sit in NonElectronic / Rock; the Folk rows sit in NonElectronic / Folk. | read, **R-799 closes** |

**The ten Pop rows, accounted for.** The ten files the remap moved to
`NonElectronic / Pop` were seven by Torr, CR's "FANCY", Espresso and Pop
Song. The seven are out of the collection, two are filed under
NonElectronic / Pop, and FANCY, whose row still says Dance / Pop, is one of
the four the author removes. Magnus Ferrell's "Asleep Talking" stays in
Dance / Pop: its file says Dance / Pop and the remap agrees.

## Sitting 30, 2026-10-02, afternoon into the night, unattended, the run of 2026-10-02

The author set the terms and left: land the run's cards through the feeder,
prove each live, read every live write in rekordbox and on the streaming
account. The feeder's stop file went down at 15:15 so the cycle building
#245, #244 and #242 ends with the feeder leaving, and the rekordbox reads
wait for that gap, since rekordbox and a Relay build never run together. The
author waived a fresh backup for the run; both backups were 0 days old at
its start. The build in use is the installed copy, reinstalled at each
landing.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `adopt scan` then `adopt apply`, R-788, #245 | rehearsed on a copy, live on an equal digest `70e700cf69b129ca` | Route 8,767, needs-genre 1,289, withheld 13, no collisions. `vocals: read`, `vocal` add 33, present 912, no-bucket 196, withheld 0. **33 vocal memberships added, none removed**: R&B / with vox 27, made by the apply as the taxonomy declares, Afro House 3, NonElectronic, Melodic House and House / Funky House / Disco one each. Memberships 19,726 to 19,759, playlists 578 to 579, no content row changed, integrity ok, live equal to the copy. | live, **R-788 closes** |
| The vocal subs read from the database | after the apply | Every vox tagged track adoption routes sits in its bucket's vocal sub. Six do not, none routed there: two with no genre on the row and four in a stale second bucket. R-846 filed. | read |
| `crate label artists`, R-840, #244 | live on the review store, no database | 29 open label releases read a provider object address and **29 were given the artist's name**: Anjunadeep 20, Amselcom 6, Last Night On Earth 2, Defected 1. 2,383 already fine, 33 provider calls, no rate limit. A second run reports none. | live, **R-840 closes** |
| The review store read for addresses | read only, before and after | Before: `crate label held`, 339 holds over 14 labels, none reads an address. After: 2,618 review items and 339 holds read straight from the store, none carries one. | read, **R-389 and R-847 close, #213 done** |
| `crate export playlist TOOLBOX/Dancefloor Rescue`, R-834, #242 | live on the account, at its gate, digest `869777719e9f317c` | One playlist created, 8 items settled, 39 provider calls, no rate limit. **Read back at the provider: `public: False`.** The account's web player, read only in the browser, shows Dancefloor Rescue, 4 tracks, the padlock reading Private. Four tracks did not match and the verb said only `ok`, R-850 filed with an issue. | live, **R-834 closes** |
| rekordbox, read only through desktop control | opened after the feeder left, no job running | BY GENRE + ENERGY / R&B reads High 6, Low 27, Med 14, Unsorted 2 and **with vox 27**, the sub the apply made. Quit from the menu, `rekordbox` and `rekordboxAgent` both gone within ten seconds. | read |
| `sync mark` then `sync unmark`, R-838, #243 | live on the account, each gate read, after cycle 39 | `DOWNLOADED Kids`, two tracks, retitled `Kids` through the account adapter. `sync mark` from the 2026-09-30 pass planned only `Kids -> DOWNLOADED Kids` and wrote the mark record. `sync unmark --playlist` planned `DOWNLOADED Kids -> Kids`, applied, **the account read `Kids`**, and a second unmark planned nothing. The title was set back to `DOWNLOADED Kids`. 619 to 1,241 provider calls a listing, no rate limit. | live, **R-838 closes** |
| `export playlist` again, R-850, #249 | live, onto the playlist R-834's run made | `tracks: 0 written, 4 already there or written before, 4 unmatched`, each unmatched track named with its reason, warning `export-tracks-unmatched`, 22 calls. | live, **R-850 closes** |
| #246, U107 | read from the merge | The task hit the model usage limit and exited with no envelope; Relay merged and closed it anyway, with no review, table or record. #246 reopened, R-857 filed. | **owed** |
| U107 reviewed, R-857, #251 | landed after cycle 40 | Two review rounds, nine findings fixed, 25 of 25 mutation rows killed, R-858 to R-861. #246 closed by hand. | **R-857 closes** |
| `crate sync favorites`, R-856, #250 | live on the account at its gate, digest `ad7df9d6bbf83ffc` | 109 favourites: **0 hearted, 97 already hearted, 12 unmatched, each named with its reason**, warning `favorites-hearts-unmatched`. The provider client's own log lines print above it, R-864. | live |
| Cycles 41 and 42 | landed | U108 #247, R-835 #252, R-837 #253, R-878 #255, R-879 #256, U109 #248, each with its review, table and record. Its task left DJ_tools one local docs commit, not pushed. | landed |
| `label playlists metronomo-records` | live, before R-878 | Refused: the folders endpoint ignores `offset`, R-878 filed and carded. | found |
| `export set` over a typed nine track set | live, before R-879 | 1 of 9 matched, every search fills its page: R-879 filed and carded. | found |
| `label playlists` after R-878 | live | Refused again: the declared total counts folders and playlists alike. **R-887 fixed in the sitting** on the gate alone, 4 of 5 mutation rows killed. | fixed |
| `label playlists sudbeat` and `metronomo-records` | live to the gate, answered abort | Sudbeat adopts its folder and eleven `DOWNLOADED ` year playlists and plans one new private 2026 playlist from 24 confirmed releases; Metronomo adopts its folder and reads 0 releases. **Not applied**: Sudbeat would add 32 tracks to year playlists the source system curated, with no genre gate (R-872) and no removal (R-836). | read, **R-878 and R-887 close** |
| `label playlists mango-alley` | live | Refused after 2,378 calls, one artist's listing spends its budget, unmeasured which: R-888. | found |
| `export set` after R-879 | live to the gate, then apply | **5 of 9 matched**, four by the library file's ISRC. The apply refused `credential-missing`, the provider session expired, nothing written: R-888. | read, **R-879 closes** |
| R-836, #254 | landed after cycle 43 | The account protocol's first removal, `remove_tracks`, refused for any playlist the ledger does not record as product made; `crate label prune` and `crate export prune`, each behind a gate listing every track. R-889 to R-894, none on the board bar. | landed |
| The provider session | re-minted by the author | `check_login` true, 221 favourites read. The plaintext token file was deleted. | live |
| `export set`, R-837, #253 | live, applied at digest `82eb82e0dcbcc832` | **`tech_house_hits - Phil` on the account, `public: False`, five tracks**: OMRI., Adam Lance, Dubdogz, Anti Up, Durante; four named as unmatched. 75 calls. | live |
| `export prune`, R-836 | live to the gate, answered abort | Dancefloor Rescue: nothing to take off, and the empty plan still asked. `TOOLBOX/Acapellas & Tools`, never exported: not judged, no remote playlist recorded. | read |
| R-888, #257 | landed after cycle 44 | A label roster is read whole and spends no budget; the refusal over a real listing keeps its wording. | landed |
| `label playlists mango-alley`, R-835 | live, applied at digest `d7cd746d02e19f10` | **A new `Mango Alley` folder on the account, 15 private year playlists, 2009 to 2026, 1,014 tracks**, read back at the provider and in the web player. 334 releases confirmed of a roster of 756 artists. | live, **R-835 and R-888 close** |
| The author's asks of 2026-10-03 | filed | U110 #258 readable INBOX batch names, U111 #259 `inbox rotate`, U112 #260 `crate organize`, which fixes what the product's rules govern and only lists what the author made. | queued |

## Sitting 31, 2026-10-07 evening to 2026-10-08, attended, the author's five asks

The author set the order and left the session to drive: the first guided label
sync, INBOX, the missing genres, the rest of #178 and #29, and a ledger triage,
with full autonomy, no questions, and later a cap of **50 label tracks** for
the download. A fresh backup ran first (files and database 22:06Z, 94 files
sent). The author minted the backup acknowledgment from Terminal at 23:49Z,
valid to 11:49Z. The build in use is the installed copy, reinstalled from local
`main` at the R-777 merge. Another project's Relay feeder ran throughout; no
Cratekit build ran beside rekordbox.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `crate label sync`, the first guided walk | live, one interactive pass fed on standard input by a driver reading each saved question | **46 labels: 28 answered, 22 picks, 7 not now, 0 stop; 7 not listed** (Rebellion, Kompakt, Rhombus, Sueño, LabelUnresolvable on a shared artist name; Colours Audio, Liebe Detail Spezial, Voll Schön, no artist of the name). The rule, the author's delegation: per label, the single newest release dated 2025 or 2026 with three tracks or fewer, while the total stayed under the cap; everything else not now. About six hours of listing, paced, no rate limit. **Open label releases in review: 2,416 to 8.** | live, **#178 line 5** |
| `label sync --next`, before the walk | live | 17 minutes 54 seconds and 1,059 calls to relist two answered labels and reach the third: R-918. | found |
| The go, `label sync --go` | at its gate, answered apply inside the cap | 22 releases, 42 tracks listed, 4 already owned, 2 offered as other versions, **36 downloaded of 36**, 264 calls, no rate limit. | live |
| `tag folder`, `analyze run`, `analyze restamp`, `name apply` | yes | 34 of 36 given a genre, 2 none; two genres outside the taxonomy (`140 / Deep Dubstep / Grime`, `Indie Tech`); Traxsource and Bandcamp blocked as before. 36 analysed, stamped and renamed, no collision. | live |
| `intake land --manifest --pass`, on the bridge | applied | 36 into `Music/2026-10-08 Labels`, batch playlist `2026-10-08 Labels`, the label year playlists named in the intake file. | live |
| Import through desktop control | yes | Imported Library pointed at the intake file, the batch playlist imported alone, collection 10,236 to 10,272, dragged into INBOX on a box outline after the hover had expanded the tree under it. Analyze Tracks with KEY unticked; every tempo equals the file head but `Villa Loop`, head 85, rekordbox 127. | live |
| `intake imported` | over a `crate export collection` | 36 proven, intake file retired. | live |
| `adopt apply` | rehearsed on a copy, live on an equal digest `b87adda1f85b0766` | **35 memberships added, 0 removed**, live memberships and every content row's tempo, rating and path equal to the copy. Route 8,802, needs-genre 1,290. | live |
| Rebellion's seed | `label registry set` | Jonas Rathsman, the artist of the Rebellion release already in the library. The other six left unseeded, no evidence in the library. | set |
| `[intake_old]` in the active taxonomy | written, the prior copy kept as `taxonomy.toml.bak-2026-10-07` | doctor parses it. | **R-902 half** |
| `inbox rotate`, rehearsal | on a copy | Refused first: the intake tree is on the xml bridge. On the copy, `tree cutover inbox` passed all four prechecks, digest `a22bb1d46da3a36e`; the rotation then planned **nothing: 7 product batches kept, all under 30 days, 14 hand made playlists left alone**, applied as a no-op. | rehearsed |
| `tree cutover inbox`, live | to its gate, run `2026-10-08T04:00:47Z-c16b` | Digest `ded0029507c5e5a1`, which differs from the rehearsal only in the three paths it names. Not approved by the session, by the standing rule. **Approved by the author from Terminal on 2026-10-08 and applied**: INBOX database native, anchored to row 2705010179. The export it keeps for a revert is the 04:00Z one, older than the label import, which R-755's existence check passes. Label landings now land natively without record labels filing (R-771). | **cut over** |
| Legacy INBOX playlists | by hand in rekordbox | The two July playlists the product does not own, `lisa_07_10_2026 SYNC 20260715_133430` and `7_10_26_summer_sampler_2021 SYNC 20260715_133430`, moved into `INBOX / Old`. The twelve in Old, February to June, left for the author. | live |
| The missing genres, measured | on a copy of the database | **621 rows have no genre on the row or the file**; adoption's 1,290 also counts genres with no bucket. Artist and folder neighbours suggest a genre at 80 percent agreement over six votes for 60. Two set by hand in rekordbox, Melodic House, about 25 seconds a track. U114, issue #266, scoped from this. | measured |
| R-777, issue #265 | built and merged locally | `sync mark --pass` on a native intake tree, proven by a closed landing that records the pass. | built |
| `crate organize --report` | live, 05:28Z to about 14:00Z | **About eight and a half hours**, R-912's crawl measured on 46 labels. Rekordbox side: adoption nothing to file, rotation refused on the bridge, Record Labels nothing, 11 of the author's top level folders listed. Account side: 9 labels planned whole catalogues into year playlists, **Anjunadeep 5,750 tracks**, Amselcom 1,128, Crosstown Rebels 731, Be One 437, All Day I Dream 369, Crew Love 241, Bar 25 223, Aus 58, Classic 26, Alive 11 (R-913's shape); 13 refused LabelUnresolvable; **from Defected on, 24 refused on a 401 from the account's folder endpoint** while catalogue reads still worked, R-920. One mark pass, nothing to mark. **No area applied**: nothing to write on rekordbox, and the account plan is the author's to choose. | read |
| Ledger triage | six read only passes over 697 open entries | 41 closed with evidence, 19 already closed in wording a search missed, 632 left. Three promoted for daily use, #262 R-572, #263 R-228, #264 R-515, and R-777 carded as owed since 2026-09-30. | done |

**#178 lines 8 and 9 stay open, the author's.** No player is near and no spare
drive is planned.

**#29 is not retired.** Its own brief retires DJ_tools only when every
workflow's replacement has run on the live library and a full sync cycle has
run on Cratekit alone; #178 lines 4, 7, 8 and 9 are not proven. The skills
would be pointed as below when it is.

| Source system skill | What replaces it |
|---|---|
| dj-sync | `crate sync all`, then `crate label sync`; shipped skill `sync-and-publish` |
| dj-label-batch | `crate label sync`, `label import`, `label harvest`; `label-catalogues` |
| dj-label-playlists | `crate label playlists`; `label-catalogues` |
| dj-favorites | `crate sync favorites`, `intake playlist favorites`; `sync-and-publish`. Gap: a pink row outside the playlist is not hearted, #263 |
| dj-pipeline | `crate intake`, `acquire`, `match`, `export set`; `intake-and-name` |
| dj-tagging | `crate tag folder`; `intake-and-name` |
| dj-maintenance | `route inbox`, `adopt`, `inbox rotate`, `organize`, `tag retag`, `repair paths`, `report`, `audit`; `route-the-library`, `library-reports` |
| dj-vocal | `crate analyze vocals`, calibrate, restamp; `analyze-audio`. #178 line 7 unproven |
| dj-backup | `crate backup run`, `restore`; `restore-and-converge`. No shipped skill triggers on "back up" |
| dj-master-set | `crate master`. No shipped skill |
| dj-set-builder | `crate setbuild`. No shipped skill |
| dj-core | the shipped skills' own descriptions route |

## Sitting 32, 2026-10-08 into 2026-10-09, attended, the first native sync cycle

The rest of #178 line 4, on the intake tree sitting 31 cut over. The backup
acknowledgment the author minted at 14:16Z held to 02:16Z. rekordbox was closed
for every verb and both processes confirmed gone after it quit.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `crate sync all` | live, run `2026-10-08T14:16:49Z-d4ce`, the favourites gate answered sync | Four jobs succeeded: favourites hearting, hearts intake, `Phil 9-30-26`, `Dancefloor Rescue`. | live |
| `intake missing --run` | live | 166 tracks to the list `2026-10-08T141649Z-d4ce_synced`, two hearts and 165 of `Phil 9-30-26`. The author chose all 166. | live |
| `acquire download` | live, detached | **165 of 166**, one refused `lossy-refused` (the provider offers it only lossy), 993 calls, no rate limit, about 30 minutes. | live |
| `tag folder`, `analyze run`, `analyze restamp`, `name apply` | yes | 159 tagged, 4 left with a catalogue unread, one `Indie Tech`; Traxsource and Bandcamp blocked. 165 analysed and stamped. **161 renamed, 4 held as two collisions**: Bilal `Soul Sista` and Tweet `Boogie 2Nite` each sit in the playlist twice, the original album and a compilation, and keep their identifier names. | live |
| `intake land --pass`, native, rehearsal | on a copy, state redirected, applied | 165 rows and files, one INBOX playlist `Phil 9-30-26` named for the account's, nothing for a batch playlist. The apply moves the real files, so the session moved the 165 back by the plan's own mapping and removed the empty folder before the live plan. | rehearsed |
| `intake land --pass`, native, live | to its gate, run `2026-10-08T19:57:21Z-ffa2` | Same screen as the copy but the database line, digest `33c8ce60c7cd8595` against `78d6b6880d0f6cdc`: R-922. **Approved by the author from Terminal and applied**: 165 files into `Music/2026-10-08 Tidal playlists and Favorites`, 165 rows. | live |
| `sync mark --pass`, rehearsal | on the copy, after its landing | The native proof read: `Dancefloor Rescue` planned for the prefix, `Phil 9-30-26` left alone with its tracks not yet adopted. | rehearsed |
| rekordbox, desktop control | Analyze Track on `Phil 9-30-26`, KEY unticked | Tempo, waveform and art on all 165. **Artist and key empty on every row**, the native writer sets five columns and no tag: R-921. Reload Tags on the same selection filled artist, album and key on 165, genre on 159. | live |
| `adopt scan` then `adopt apply` | rehearsed on a copy, live on an equal digest `a74ae7c88692d6a0` | Route 8,960, needs-genre 1,297, withheld 13, no collisions, every item line identical. **158 memberships added, 0 removed**: R&B 62, Nu Disco / Indie Dance 38, Dance / Pop 30, Breaks / D&B / Dubstep 13, NonElectronic 12, House / Funky House / Disco 2, Deep House 1. 2,135 playlists before and after, no tempo changed. Live read back equal to the copy. | live |
| `sync mark --pass`, live | at its gate, the same rename as the rehearsal, approved by the session | **`Dancefloor Rescue` renamed `DOWNLOADED Dancefloor Rescue`** on the account, recorded in the library's mark ledger, 1,305 calls, no rate limit. The first mark proven by a native landing. | live, **#178 line 4** |
| The 165 rows on a deck | the author tried, after the mark | **None loads, no dialog.** A bridge imported row of the same day loads at once. Measured on a copy of the database: the native writer sets five columns and the binding leaves twenty one NULL that rekordbox fills on every row it makes, among them `Rating`, `ColorID`, `DJPlayCount`, `DeliveryControl`, `ExtInfo`; of 10,272 live rows the 165 are the only ones with any of them NULL. A8 at sitting 17 proved such a row is accepted and analysed, and never tried a deck. **R-923, issue #267**, the author choosing a code fix over a re-import: the landing sets the defaults, `crate repair rows` fills them in place. Its live run is the row below when it lands. | found, built |
| `inbox rotate --as-of 2026-11-01` | the author asked for INBOX cleaned up; rehearsed on a copy, live on an equal digest `ba9c5d7bd7ceeae7` | Aged as of a date past the 30 day rule so every batch adopted before this week goes: **7 moved into Old** (both 09-23 batches, both 09-29, both 09-30, the 10-01 labels 1 percent), 2 kept (`2026-10-08 Labels`, `Phil 9-30-26`), the 14 hand made playlists in Old left alone, 0 removed, no track left the collection. Live read back equal to the copy. | live, **R-902 closes**; R-903 still unobserved, nothing was removed |

**`Phil 9-30-26` stays unmarked, correctly.** Three of its tracks match a
version the library already holds and wait in review: Sister Sledge `Thinking
of You` (Dimitri from Paris remix), Leela James `Good Time`, Sade `Your Love Is
King`. Once the author answers them, a later pass marks it.

## Sitting 33, 2026-10-09, attended, the second native sync cycle and the repair of the 165

The author asked for the fixes finished, a review, then a sync of his new
custom playlists and favourites with the downloaded ones marked on the
account. R-923 was built and merged first, the installed copy rebuilt from
`main` at `2fb06d8`. rekordbox stayed open for every file verb and was quit
for every database write.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `crate sync all` | live, run `2026-10-09T03:59:14Z-c5e1`, 649 calls | Two new account playlists queued as intake jobs, the 231 hearts as a third (240 declared, 9 withheld by the provider). The outbound half of favourites, hearting the library's pink rows on the account, not queued: it needs a collection export, the #263 gap. Driven one at a time, all three succeeded in under two minutes: every track resolved against the library. | live |
| `intake missing --run` | live | **67 missing**, 221 already owned, 1 held in review, written to `2026-10-09T035914Z-c5e1_synced.list.json`. | live |
| `acquire download`, first job | live | 12 landed, then **blocked `UPSTREAM_AUTH` on track 63466200**, a 401 from `playbackinfopostpaywall`. The remedy named a dead session. The author minted a PKCE session from Terminal at 10:20Z, recorded it, erased the token file; a driver 22 seconds later wrote the file back from the keychain (R-212, measured again). The new session met the same 401 on the same track. | found |
| The cause | a read only probe through the catalogue | The track is one of 58 in the list from the 2016 compilation `New York Fever Vol.1`; the catalogue reads **33 streamable and 25 not**, and both blocking tracks are in the 25. One unlicensed track reads as a dead session and blocks the job: **R-927**, on the board bar. | found |
| `acquire download`, three more jobs | live, lists cut by hand | The 9 outside the compilation, then the 33 streamable: **41 of 67 on disk**, the 25 unlicensed left missing, every "failure" after the first a file already on disk. | live |
| `tag folder`, `analyze run`, `analyze restamp`, `name apply` | yes | 41 tagged (Traxsource and Bandcamp blocked as before), analysed and stamped; 39 renamed, 2 held as one collision, Cameo Culture `Told You So` under two ids. The staging folder held 26 copies the partial jobs left, 25 byte twins of files already in place, deleted, and one track never moved into place, Bonobo `Kiara`, given its own tail in a side folder and moved in: **42 files**. `name apply` walked into the staging folder first (R-741). | live |
| `repair rows`, R-923's live run | rehearsed on a copy, live on an equal digest `73eb5c83fc856970`, the author having made the acknowledgment the session's that morning | Of 10,437 live rows, **315 lacked a default**: the 165 of sitting 32 lacked all twenty one, and 150 older rows rekordbox made lacked text columns only (79 `Reserved1` alone, 60 the seven text fields, 10 those with subtitle and release date, 1 a colour id). Every item line identical between copy and live. **315 written and 315 read back on both**, those columns and no other, each undoable by its session capture. Whether the 165 now load to a deck is read in rekordbox below. | live |
| `intake land --pass`, native | rehearsed on a copy (digest `f206412ef87ea780`, 42 rows, files put back), live at `bc90a176eb68f091`; the author's decision never landed on the run, and he lifted every approval at 13:05Z, so the session decided it | **42 files into `Music/2026-10-09 Tidal playlists and Favorites`, 42 rows**, two INBOX playlists named for the account's, `New York Fever Vol. 1` with 38 and `Phil 10_8_26` with 4, the one heart in the batch playlist. Each row carries rekordbox's defaults from creation, R-923's other half. | live |
| rekordbox | Analyze Track with KEY unticked, then Reload Tags, on the three new playlists; then the deck test on the repaired 165 | 42 analysed and tag reloaded. **The repaired rows still will not load**: `Load` greyed in the playlist and in the Collection view, a drag lands nothing, while a bridge imported row loads; the information panel reads the file whole. A full column diff after the repair leaves only ids, rating and two update counters different. One track, Maxwell `The Urban Theme`, was removed from the collection for a re-import through rekordbox's own panel, and the panel's sheet took no key event from the session, so it was force quit and the track is landed again below. **R-928.** | found |
| `intake land --pass`, Maxwell alone | rehearsed on a copy, live, the session deciding | The track removed for the experiment, landed again from staging under the pass of sitting 32: one row, one file in `Music/2026-10-09 Tidal playlists and Favorites 2`, the INBOX playlist `Phil 9-30-26 2`. The copy rehearsal had moved the file into that folder and the session's put back looked in yesterday's, so the first live plan found staging empty; a second did it. Unloadable like its siblings. | live |
| `adopt scan`, `adopt apply` | rehearsed on a copy, live on an equal digest `8d5967147803042b`, the session approving | **35 memberships added, 0 removed**, no tempo changed: NonElectronic 12, Nu Disco / Indie Dance 6, R&B 4, House / Funky House / Disco 3, Breaks / D&B / Dubstep 3, Dance / Pop 2, Deep House 2, Techno 1, Trance 1; the rest of the 42 sat where their genre names, and the re-landed Maxwell row had no genre yet. 2,140 playlists before and after. Live read back equal to the copy. | live |
| The deck block, found | one native row removed, its file dropped from Finder onto rekordbox | **rekordbox's own row loads at once, unanalysed.** It differs from a native row in the analysis columns and in `rb_file_id` alone: rekordbox allocated 1402671, in sequence after yesterday's 1400905; the binding mints a random nine digit id. The A8 row of 2026-09-29, the binding's, analysed and filed since, does not load either. So the column is the key, allocated from a counter outside `master.db`. A drop of a path already in the collection adds nothing. **U115, issue #272.** Liberian Girl now has rekordbox's row, outside the INBOX playlist, placed by the next adoption. | found |
| `sync mark --pass` | live, the session approving | **`Phil 10_8_26` renamed `DOWNLOADED Phil 10_8_26`** on the account; `New York Fever Vol. 1` left alone, 21 of its tracks still missing, the unlicensed ones; 1,277 calls, no rate limit. The pass's mark is recorded in the library's mark ledger. | live |

## Sitting 34, 2026-10-09, attended, the 207 native rows replaced by rekordbox's own, and the column named

The author needed playable tracks now, and U115 (#272) is the fix for the
landing, not for the rows already landed. So the proven route of sitting 33
was run over every native row in INBOX: remove the row, drop the folder back
from Finder, let rekordbox make its own. The installed copy stayed at
`2fb06d8`. Both backup ages had just passed one day, so `crate backup run`
went first (53 minutes, 1,780 files sent, the database copied), and
rekordbox was opened only after `doctor` read both under a day.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| Remove from Collection | rekordbox, the session driving, five INBOX playlists | `Phil 9-30-26` 163, `New York Fever Vol. 1` 38, `Phil 10_8_26` 3 (its fourth was in the compilation playlist too), `2026-10-09 Tidal playlists and Favorites` 1, `Phil 9-30-26 2` 1: **207 rows, every native row the landing ever made in INBOX**, each confirmed through rekordbox's own dialog. The five playlists were left in place, empty, since the account playlist names they carry are the sync marks' names; the author deletes them or not. | live |
| The drops | three folders dragged from a Finder list window onto the INBOX node, `left_mouse_down`, moves with waits, `left_mouse_up` | Each drop made a playlist named for its folder: **`2026-10-08 Tidal playlists and Favorites` 164**, Liberian Girl's existing row joined it, so a drop does add a path already in the collection to the new playlist, it only makes no new row; **`2026-10-09 Tidal playlists and Favorites` 42**, after rekordbox asked to replace the empty native playlist of the same name and the session said yes; **`2026-10-09 Tidal playlists and Favorites 2` 1**. rekordbox read artist, album, genre and key from the tags on import, no Reload Tags. 207 rows created today, 10,479 active rows, the count unchanged. | live |
| The deck test, before analysis | `Load` on the first new row | **Live at once**, Sade `By Your Side` loaded to deck 1 unanalysed, and rekordbox analysed it on load. | live |
| Analyze Tracks | the session, per playlist, rekordbox's per batch Analysis Setting dialog each time: BPM / Grid and Phrase ticked, KEY unticked, Normal, 78 to 155 | **207 analysed in about six minutes.** | live |
| The deck test, after | one row from each folder | Sade `By Your Side` (2026-10-08) on deck 1, Weval `Easier` (2026-10-09) on deck 1, Maxwell `The Urban Theme` (Favorites 2) on deck 2, each with a waveform and a tempo. rekordbox quit with `cmd+q`, `rekordbox` and `rekordboxAgent` both gone before any verb. | live |
| `adopt scan`, `adopt apply` | rehearsed on a copy (database copied to scratch, `.cratekit` copied to `.cratekit-copyrun` on the volume, config and state dirs redirected), live on an equal digest `61bb3efcc88a5058`, the session approving | Plan text identical between copy and live, 8,998 routed, 1,301 needing a genre, 13 withheld, collisions none. **196 memberships added, 0 removed, no tempo changed**: Med 67, High 60, Low 45, Hip-Hop 11, Pop 8, Rock 3, Jazz 1, Caribbean 1. 588 playlists before and after. The live database read back equal to the copy, 196 ledger entries under the digest on both. The 11 not placed are the rows with no genre on the file. | live |
| The column, named | `stat` against the new rows | **`rb_file_id` is the file's inode number at import.** Sade's file is inode 1402707 and its row carries 1402707; the same for every row rekordbox made today, and for 459 of 459 rows created in October, 1,851 of 1,851 in July, 33 of 33 in April. Rows from the March migration match in 1,757 of 5,603 and June in 750 of 2,108, their files having been copied since (a copy is a new inode), and 1,358 rows carry 0; those rows load, so a stale or zero value is tolerated and a random nine digit one is not. The ids are not a counter: Maxwell's file, moved to another folder, kept its inode and so got 1402651, below Liberian Girl's 1402671 from the day before. Recorded under R-928 and on #272. | found |

What the sitting leaves: the five emptied INBOX playlists; the twelve hand
made playlists in INBOX / Old; the sampler rows and the A8 row of
2026-09-29 (`73894078`, random id, inode 1104075) still carry random ids
and are outside INBOX, untouched here.

## Sitting 35, 2026-10-09, attended, the first set intake end to end on the native tree

A SoundCloud mix of 5 hours 5 minutes, Public Service NYC live at Vonking on
2026-05-03, taken from the address to BY GENRE + ENERGY with the installed
copy at the merge of #260, which predates U115. rekordbox was closed for
every verb and both processes confirmed gone after it quit. The
acknowledgment the author minted at 12:43Z held throughout.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `intake set` on the address | live, detached, paused 30 minutes mid download at the author's ask and resumed | 557 MB fetched in about 7 minutes, 732 recognition calls in two parts over about 19 minutes, **54 tracks** queued. No output for the whole run, R-924; the tracks visible only in the job store, R-925. The run also surfaced the config overwrite, R-926, found and restored by its drift warning. | live |
| The review of the 54 | the session, the author told the lane | 36 keep, 18 drop: one song under several ISRCs five times (Black Coffee, Edwin Starr, Michael Jackson, D'Angelo, The Emotions, Francis Overcast, Afrikan Roots, Soul Central, Merceditas Valdes, ManWomanBoogie), a karaoke cover, a piano cover, a continuous DJ mix, a row with no ISRC. The author stated the library is growing into hip hop, R&B and soul, so those rows are kept on the same footing as house. | decided |
| `intake set --job` | live | 17 owned, 5 offered, 32 missing, 102 provider calls, no rate limit. | live |
| `intake missing --job`, then `--list` over the unlisted keeps | live | 6 listed by ISRC. 26 handed on: 7 drops, 18 keeps of which one ISRC named several releases or none. The text search listed 1 exactly, offered 15 for review, found nothing for 2. Fifteen verdicts recorded by the session, the ISRC match chosen where one existed, the heard mix otherwise. Two resolved by hand from the provider's own rows for the two ISRCs the search skipped: Soul Central's Funky Lowlives Mix, two releases, the single taken; Edwin Starr's King Britt Remix in place of the Extended Mix the provider lacks. **20 listed**, merged into one list by hand. Not on the provider at all: Freyta, Richie Rich, Atix, Xandra. | live |
| `acquire download` | live, one job, 120 calls, no rate limit, about 4 minutes | **20 of 20.** | live |
| `tag folder`, `analyze run`, `analyze restamp`, `name apply` | yes, in one detached chain | 19 of 20 tagged (one `Dance`, unmapped), Traxsource and Bandcamp blocked as before, art repaired on 20; 20 analysed and stamped; 19 renamed. **One pulled before the rename**: Stefan Ringer `SO` is the library's `Sexual Obsession`, so the resolver's title approximate hold was right and the session's rejection of it wrong; the verdict was cleared and the library candidate accepted. The first chain ran nothing, zsh passing each two word verb as one word. | live |
| `intake land --name`, native | rehearsed on a copy, applied there, the 19 files moved back by the plan's mapping; live on the same screen but the database line, `4c8eeef47fd787ee` against `1f2428567691ccb7`, R-922, approved by the session | 19 rows, 19 memberships in `INBOX / 2026-10-09 Set Public Service NYC Live at Vonking 5-3-26`, files in the folder of that name. A `run decide` only answers; the verb resumed under `--run` applies. | live |
| rekordbox, desktop control | the computer use lock was held by cratekit-7e, idle since 2026-10-08 01:17, pid 20715; removed with the author's choice | Analyze Tracks with KEY unticked, about a minute for 19; Reload Tags filled artist, key and genre on 19, one with no genre (Tribal Kings). **A permanent playlist for the set**, decided by the author for every set intake from now on: `INSPIRATION / 10_09_26 Public Service NYC Live at Vonking 5-26`, the source system's name form, holding the 19 landed and the 13 owned identified tracks, **32**, each owned one found through the Collection search. INSPIRATION already held two such playlists from the source system; TOOLBOX / Sets and Long Tracks is the long recordings, a different thing. U121 (#278) makes the landing write it. | live |
| `adopt scan`, `adopt apply` | rehearsed on a fresh copy, live on an equal digest `b23bf7a9b105529a`, the session approving | 9,016 routed, 1,302 needing a genre, 13 withheld, no collisions. **18 memberships added, 8,998 already present**, the same 18 plan ids on copy and live: House / Funky House / Disco 6, R&B 3, Breaks 2, NonElectronic / Hip-Hop 2 (Kendrick Lamar, Q-Tip), Afro House, Dance / Pop, Deep House, Tech House, UK Garage 1 each. `adopt apply --job` without `--run` opens a new run and asks the gate again; the drive carries the approved run. | live |

**What the sitting leaves.** The 19 rows are native rows made before U115
merged, so they carry random `rb_file_id`s and will not load to a deck
until `crate repair rows` runs over them, after the installed copy is
rebuilt at the merge of #272. Tribal Kings sits in INBOX only until a genre
is set. The four tracks the provider lacks are not acquired. The duplicate
pulled from the batch sits in the session's scratch, not in the library.
The INSPIRATION playlist was made by hand and U121 (#278) is the verb.

## Sitting 36, 2026-10-10, morning, attended, the U115 live proof, and it fails

The installed copy was rebuilt from `~/cratekit` at `681ee20`, the head of
`main` that morning, 162 commits past the brief's `fa94b96` and holding
the merge of #272, with no intake job running. The acknowledgment was
minted by the session at 10:50Z, both ages read under a day (files 20.4
hours, database 19.5 hours), and holds to 22:50Z. The Cratekit feeder had
left on its stop file at 06:46 and the Integrel feeder was idle, so nothing
built while rekordbox was open. The computer use lock, held by another
session's pid since 2026-10-09 14:54, did not refuse the access request and
was left alone.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `repair rows` | rehearsed on a copy (database to scratch, `.cratekit` cloned to `.cratekit-copyrun` with `cp -Rpc`, config and state dirs redirected, the live acknowledgment carried in the clone), live on an equal digest `418d3383f4ffac16`, the session approving both; the live verb resumed under `--run` after `run decide` | **20 rows renumbered, not 36 and not 17.** The 19 Vonking rows of sitting 35 and the A8 row `73894078`, now `1104075`, the inode the U115 record named. The bound read `1417181` on the copy, `1417210` at the live gate and `1417213` at the live apply, filesystem `apfs`; the bound is outside the digest, so the plans matched to the digit with the bound the only line that differed. No column fills: the defaults of sitting 33 were already in place. 20 written and 20 read back on copy and live, undo by session capture `2026-10-10T10:52:56Z-c1cf`. An independent read of the live database afterwards found all 20 equal to `os.stat` of their file and 16 rows left above the bound. | live |
| The sixteen "sampler rows" | read on the copy before approving | **They were never the binding's.** They are rekordbox's own GROOVE CIRCUIT preset rows, `4-Floor Breaks Kit`, eight under this account's own rekordbox sampler folder on the boot volume made 2026-05-25 and eight under a second account's, made 2026-08-15, before any landing existed. Their ids are boot volume inodes: `Breaks1.wav` under this account is inode `88852942` and its row carries `88852942`. Above the library volume's bound by size alone, they fall under R-930 and were listed and left, with the reason `the path does not resolve on this machine`, which is the prefix rule talking, since the eight files under this account exist at their literal path. A wording residual at most, below the ledger bar: those rows are not deck tracks and rekordbox made them. The U115 record's population of seventeen was one row, and the live population at the time of the run was twenty. | found |
| rekordbox, desktop control | opened after `doctor` read both backup ages under a day and the processes gone, quit with `cmd+q`, both confirmed gone before any further verb | **A repaired row still does not load.** `Load` greyed on the context menu of `Water No Get Enemy`, of `As` and of `Canto Della Liberta`, and a drag of the first onto deck 1 landed nothing. The control, Maxwell `The Urban Theme (Remastered 2021)`, the row rekordbox made itself on 2026-10-09 with `rb_file_id` `1402651`, had `Load` live, and two more items live that are greyed on every repaired row: `Add To Tag List` and `Export Track`. The repaired ids survived rekordbox's quit, 20 of 20 still their inode. rekordbox wrote nothing outside the volume that keys a track. | **failed** |
| What still differs, read live while rekordbox was open | the repaired row against the control, every `djmdContent` column, and their `contentFile` rows | Beyond the row's own identity (ids, UUID, path, title, artwork and analysis paths, usn, timestamps) and the known `TrackInfoUpdated` and `AnalysisUpdated` pair, **one column**: `ContentLink`. Every one of the 20 binding rows carries `2973454`, and no other row does; 10,292 rows rekordbox made carry `2950670`, every row since 2026-03 but 27 at `2885134` and a handful of 2023 values. pyrekordbox's `add_content` sets it to the TRACK menu item's `rb_local_usn`, which now reads `645482`; rekordbox's own value keys no table in `master.db`, so what it is remains unknown. Both rows hold five `contentFile` rows of the same shape, artwork and four analysis files, with local paths under the volume. | lead |

**What the sitting leaves.** R-928 stays open: `rb_file_id` was a real
difference and a necessary repair, since every row rekordbox makes carries
its inode and the binding's random id was wrong, but it was not the block.
The 20 repaired rows are correct on that column and still unplayable, and
the proven route to a playable row remains sitting 34's, remove the row and
drop the file from Finder. The one named difference left is `ContentLink`,
untested because a one row write to the live database outside a gated verb
is forbidden, and that test wants a unit: write `2950670` onto one repaired
row through a gate, open rekordbox, read `Load`. `Escape` does not close a
context menu in rekordbox from the control tool, so a click meant for the
search field dismissed the menu instead and the typed search went to the
track list as shortcuts; the deck layout switched to compact and nothing
else was seen to change, and the next sitting should click empty space to
dismiss a menu before touching the search field.

## Sitting 37, 2026-10-10, late morning, attended, A32, and a landed row loads

The installed copy was rebuilt from `~/cratekit` checked out at the A32
branch, and the Cratekit feeder had left on its stop file at 06:46. The
acknowledgment of sitting 36 still held, both ages under a day. A sweep of all
78 `djmdContent` columns on a copy asked, for each, whether a binding row's
value or storage shape occurs on any row rekordbox made. Three did not:
`ContentLink` `2973454`, `ISRC` stored NULL where rekordbox stores the empty
text, and `AnalysisUpdated` at 1. Play history then dated the rest: rows with
other ContentLink values were played under rekordbox 7 as late as 2026-07,
NULL ISRC rows last in 2024, and no row at AnalysisUpdated 1 ever.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `repair link`, the probe | rehearsed on a copy (database to scratch, `.cratekit` cloned to `.cratekit-copyrun` with `cp -Rpc`, config and state dirs redirected), live on an equal digest `5f14b61568f192c6`, the session approving both | **8 values on 6 rows, 8 read back.** ContentLink `2950670` on Water No Get Enemy and Strings of Life; ISRC empty on As and Super Rich Kids; both on Canto Della Liberta and Still In Love; Erotic untouched as the control. Undo by session capture `2026-10-10T12:12:34Z-1989`. | live |
| rekordbox, desktop control | opened after the mutation table ended, read by dragging each row to a deck, quit with `cmd+q`, both processes confirmed gone | **Water No Get Enemy and Strings of Life load**, each with ISRC still NULL and AnalysisUpdated still 1. As, ISRC alone, does not; Erotic does not. rekordbox changed nothing on any probed row. A dictation app's window sat over the track list at first and refused clicks there until it was dismissed; the context menu did not appear in screenshots, so the drag is the read. | **passed** |
| `repair link`, the remaining 16 | rehearsed on a copy, live on an equal digest `04e1873ff5f428a6` | ContentLink `2950670` on the 13 other Vonking rows, the A8 row and the two probe rows still carrying the binding's value; 16 written, 16 read back. No live row carries `2973454` now. Undo by session capture `2026-10-10T12:43:04Z-9e6d`. | live |
| rekordbox, the spot check | opened again, two drags, quit, both processes gone | **The A8 row loads**, for the first time since it was made on 2026-09-29, and **Erotic, refused at the first open, loads**: the same row before and after one column. | **passed** |

**What the sitting leaves.** ContentLink is the block on a native row, and
the other two candidates are not needed. All 20 landed rows load to a deck.
R-928 stays open because the landing still lets the binding choose the
value, so the next native landing makes unplayable rows again until a unit
makes it write the library's own value; until then, `crate repair link`
over each landed row is the repair.

## Sitting 38, 2026-10-12, attended, the favourites, the vocal tags and the taxonomy upgrade

The author asked whether the favourites and vocal tags had been synced and
the INBOX cleaned up. None had, and all four were open attended cards filed
2026-10-10 (A34 to A37, #294, #301 to #303). The installed copy was rebuilt
from `main` at `8dcd3796`, 71 commits past the `fbb3aad` it ran, so U127 to
U132 were in it. No feeder, no job and no rekordbox were running. The
acknowledgment was minted by the session at 23:00Z under the five day rule,
both ages reading about 3.3 days, and holds to 2026-10-13T11:00Z. Every
database write was rehearsed on a copy first (database to scratch,
`.cratekit` cloned to `.cratekit-copyrun` with `cp -Rpc`, config and state
dirs redirected, doctor's `tree.registry` read on the scratch name) and
applied live on an equal digest, the session approving. The live database
read `6c28cd29104ce73c` before the first write, `a463cfbf3c5ea580` after the
last, and `961bd08da87358c8` after rekordbox quit.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `metadata mytags-vocals --apply`, A37 step 1 | rehearsed on the copy, live on the same plan | Plan 1,534 tracks at cut 5.0, 1,885 associations already present, **688 written**: 412 `vox`, 66 `male vox`, 210 `female vox`, digest `6dc8085863c73daf` on both. `vox` read back 1,141 to 1,553 on copy and live. The card counted 266 rows since September; the plan also covered 162 older Processed_Tracks rows that had a score and no tag, which the card's date bound left out. | live |
| `adopt scan`, `adopt apply`, A37 step 2 | rehearsed on the copy, live on an equal digest `8acacba7fc51ac7c`, zero lines differing between the two gate screens | Route 9,039, needs-genre 1,308, withheld 13, no collisions; `vocal` add 351, present 945, no-bucket 257. **355 memberships added, 0 removed**: 351 vocal, 4 band. Read back: 1,553 `vox` rows, 1,491 under a `with vox` sub, the 62 others rows with no genre and so no bucket; Angie Stone under `Nu Disco / Indie Dance / with vox`. | live, **#303 closes** |
| `favorites backfill`, A34 | rehearsed on the copy, live on an equal digest `db179784b7e5de25`; the only differing lines a deprecation warning and the call count, 8 on the copy and 6 live | **74 landed hearts, 148 memberships** into All Favorites and their quarters: 2 into 2024-Q3, 55 into 2026-Q3, 17 into **2026-Q4, created**. All Favorites 109 to 183. The four hearts the card names are in Q4. 70 dates asked of the account. | live, **#294 closes** |
| `favorites backfill`, a second time | live, abandoned at its gate | Plans 0 memberships and no playlist, yet opens the gate and asks the account for the same 70 dates. U120's record says a second run asks nothing. **R-993.** | found |
| `taxonomy upgrade`, A36 step 1 | rehearsed on the copy, live on an equal digest `d6012c8ad12d6a35` | Schema 2 to 4, `favorites` added after `with_vox`, **`soul` and `hip_hop` held** because `rnb` still files 'Soul', 'Soul / R&B' and 'soul & funk' and `non_electronic` still files the hip hop words, as doctor's `taxonomy.schema` said. The copy as it was at `taxonomy.toml.2026-10-12T191123.bak`. The live file equals the copy's byte for byte. Letting the two buckets in is U118's attended tail, A38. | live |
| `favorites refresh`, A36 step 2 | rehearsed on the copy, live on an equal digest `5c9f0888a9029088` | 19 folders, **16 Favorites playlists created, 169 memberships added, 0 removed**; Techno, Trance and Chill / Ambient hold no favourite and get no playlist. Read back: 166 distinct favourites across the 16, 3 of them in two folders, the 17 others favourites with no genre. A second run plans 0, 0 and 0 under the same digest and still opens its gate: R-993 again. | live, **#302 closes** |
| `sync pair`, A35 step 1 | on the copy, `Phil 9-30-26` (`a20b28ba`) against the empty rekordbox playlist `196247513` | **Refused**, `sync-pair-out-of-scope`: the playlist sits under INBOX, a tree Cratekit writes, R-906 by design. It listed the account first, **638 calls over ten minutes**, before a precondition the database answers. **R-994.** | found |
| `intake land --pass 2026-10-08T141649Z-d4ce`, A35 | on the copy, staging empty | `no_op`. A later landing of a mirrored pass holds only its new files (U128), so nothing today refills the four empty playlists from their account playlists. The mixed `Tidal playlists and Favorites` playlists stay until something does. **U134 filed; #301 now depends on it.** | found |
| `export set`, no name, U129's backfill | live at its gate, the session approving, 193 calls, no rate limit | **`10_10_26 Public Service NYC Live at Signal 2-26` created on the account, 39 tracks**, digest `080d8a2ebea7b7a4`, resolved by ISRC and by the author's accepted verdicts, repeats folded. Left for a later sitting: Vonking, GOATCHELLA and PEPOFIT, "no succeeded set job names this INSPIRATION playlist". Vonking's job `2026-10-09T03:01:03Z-6ad9` succeeded but predates U121 and its playlist was made by hand, and R-949 says a backfill run on any day but 2026-10-09 makes a twin. Not run. | live |
| `export archive`, no name | live, abandoned at its gate | Nothing to archive. Signal waits on "an intake file that proves its download", which a native landing never writes: R-777's shape, closed for `sync mark` and open here. **R-995.** The playlist stays at the account root, listenable. | found |
| `converge --tree inbox` | read | Reports 20 missing memberships under genre bucket paths (`afro_house/unsorted`, `dance_pop/with_vox`) for `tree.inbox`. Not rebuilt. **R-996.** | found |
| rekordbox, desktop control | opened after the writes with both processes confirmed gone before and after, quit with `cmd+q` | `R&B / with vox` 96 (27 at sitting 32) and `R&B / Favorites` 6; `Favorites / 2026-Q4` 17; `Deep House / Favorites` 17 and `Tech House / Favorites` 17; the Signal set's rows show `male` and `vox` in the My Tag column. INBOX reads exactly as #301 describes, unchanged. | read |

**What the sitting leaves.** #301 waits on U134. The Vonking set has no
account playlist, and R-949 holds it until a flag names the day. Soul and
Hip-Hop are held out of the live taxonomy until A38. The author stated three
rules this sitting, each filed as a unit: Jazz as a genre folder with energy
bands (U133), a set landed in several batches as one playlist in rekordbox
and on the account (U135), and set playlists dated by the day the set went
up on its service rather than the landing day (U136, R-949's neighbour).
The memory saying no live Tidal bulk work until #217 was removed; #217 is
closed.

## Sitting 39, 2026-10-13, 02:14 to 03:15, unattended, the watcher under the overnight authority

Phillip, 2026-10-12 20:50, away for the night: "keep this going, iterate until
it is perfect, do not stop to ask me any questions, automate the desktop, drive
on your own, assume full permissions. I also want Tidal playlists to be
retroactively named and organized into folders." The build cards of the night
(U134, U137, U133, U135, U136, U138, U139) were landed and pushed first
(`265e35e`), the feeder stopped on its stop file at 02:14:11, the installed
copy rebuilt from `main` at `265e35e`, and every live step below ran with
rekordbox closed. The acknowledgment minted at sitting 38 held (valid to
2026-10-13T11:00Z, both backup ages 3 days). Every database write was
rehearsed on a copy first (database copied to a scratch directory on the library volume,
`.cratekit` cloned to `.cratekit-copyrun` with `cp -Rpc`, the installation
state copied, config and state dirs redirected, doctor's `tree.registry` read
on the scratch name), then run live by the installed `crate` through
`live_gate.sh`, which compares the live digest with the rehearsed one and
answers as `session`. The live database read `961bd08da87358c8` before the
first write, `4aa6da955feed64f` after the last verb, and `a42a73a0c8c35bd2`
after rekordbox quit.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `inbox refill --pass 2026-10-08T141649Z-d4ce_synced`, A35 step 1 | rehearsed on the copy, live on an equal digest `acc64ccf25b1c2e0` | **168 memberships added to `Phil 9-30-26`** (168 of 172 owned, 2 left out as neither owned nor landed, 2 repeats), `Dancefloor Rescue` named as having no INBOX playlist; every row read back, no content row | live |
| `inbox refill --pass 2026-10-09T035914Z-c5e1_synced`, A35 step 1 | rehearsed on the copy, live on an equal digest `62861fcdd1f0a38a` | **47 added**: `New York Fever Vol. 1` 41 of 60 (19 left out, named), `Phil 10_8_26` 6 of 6 | live |
| coverage of the three mixed playlists, A35 step 2 | read on a fresh copy | all 207 tracks of `2026-10-08 Tidal playlists and Favorites` (164), `2026-10-09 …` (42) and `… 2` (1) are in a named playlist, All Favorites (183 hearted) or BY GENRE; 0 orphans | read |
| hand edit of the live taxonomy, A38 step 1 | backup beside it, `taxonomy.toml.2026-10-13T021550.hand-edit.bak` | exactly what the hold named: `Soul`, `Soul / R&B`, `soul & funk` out of `rnb`; `Hip-Hop`, `Hip-Hop / R&B`, `Jazz` out of `non_electronic` with its `hip_hop` and `jazz` subs and map rows; the two deezer vocabulary rows (`Rap/Hip Hop`, `Jazz`) out, since the copy does not load with them, and written back after the upgrade | live |
| `taxonomy upgrade`, A38 step 2 and U133's tail | rehearsed on the copy, live on an equal digest `c3dc105053581278` | **`soul`, `hip_hop`, `jazz` added**, schema 4, 22 buckets, doctor clean; the `jazz` keyword rule left pointing partial matches at NonElectronic, as U133 says it would, the author's call | live |
| `adopt scan` | live | 10,527 rows: route 9,052, needs-genre 1,308, excluded 167, unmapped 153 | live |
| `adopt apply`, first pass | rehearsed on the copy, live on an equal digest `a418b4bd4436020d` | 0 added, 8,961 present, 91 withheld by placement (the former places) | live |
| `adopt move`, A38 step 3 | rehearsed on the copy, live on an equal digest `a55a9d498b39f59d` | **86 tracks moved** into their Hip-Hop, Soul and Jazz bands, none held back; 10 left by reason (2 no reading, 4 genre names no style, 4 one sub held by two rows) | live |
| `adopt apply`, second pass | rehearsed on the copy, live on an equal digest `a52788affd81e697` | **34 vocal memberships added** (the moved tracks' `with vox`); Soul and Hip-Hop Favorites playlists made with 6 adds, 1 removal owed | live |
| `favorites refresh` | rehearsed on the copy `dbbe024b278e9d28`, live `38fe1ff234a181cd`; the difference read item by item is only the folder and playlist row ids of hip_hop, jazz and soul, made separately on each side, every count equal, so approved as session under the 2026-10-09 rule | 22 folders, 0 added, **1 removed**, read back | live |
| `converge` | read before and after | both trees `differing`, remedy `rebuild-tree`, the same pre existing `electronica_other` and `tree.inbox` items before and after (R-996's shape); nothing of this sitting changed them | read |
| rekordbox, desktop control | opened after the writes with both processes confirmed gone before and after, quit with `cmd+q` | INSPIRATION `10_10_26 Public Service NYC Live at Signal 2-26` renamed to **`3_25_26 Public Service NYC Live at Signal 2-26`** (U136's tail, the Signal job's `upload_date 20260325`); the three mixed INBOX playlists **deleted** (memberships only); read: Hip-Hop High 10, Low 14, Med 24, with vox 19, Favorites 1; Jazz High 3, Low 10, Med 2, with vox 4; Soul High 2, Low 6, Med 5, Unsorted 2, with vox 11, Favorites 5; INBOX `Phil 9-30-26` 168, `New York Fever Vol. 1` 41, `Phil 10_8_26` 6 | live |
| `organize --only file` (U137), the Tidal filing | report on the copy (22 minutes, 1,304 paced calls), the plan read line by line, then live on an equal digest `02d28addb67b403c`, the session answering `apply` at 02:30, applied by 03:15 (1,347 calls, none rate limited) | **21 root playlists moved into their year, `Mine` or `Exports` folders, 3 folders created, 13 left at the root each with its reason** (two set playlists for the archive, eleven label LIBRARY playlists for the label step); nothing deleted; the account read back afterwards shows 30 root folders with `Mine`, `Exports` and `2026` among them | live |

**What the sitting leaves.** A35 (#301) and A38 (#311) closed. `Phil 9-30-26
2` is empty under INBOX and the root `Untitled Playlist` stands; both are
Phillip's to remove. The Vonking set's job carries no `upload_date`, so its
INSPIRATION playlist keeps `10_09_26`; the account half of U136's rename has
no verb and is filed as U140 (#317). The Tidal filing ran live (above), U137's first
live run; what the label step and the set archive own stays at the root until
they file it. The 10 tracks the move left are named in the run record.

## Sitting 40, 2026-10-13, 20:03 to 20:15, then 06:23 to 06:25 on 2026-10-14, the operator session, Phillip present

Phillip, 20:03: "I want the playlists tonight." The run of the day (U140 #317,
U142 #319, U143 #320, U144 #321) had landed and been pushed by 19:54
(`a06f827`, residuals numbered at `04be3dad`), the feeder was idle, and
U144's record owed exactly this sitting. The feeder was asked to leave on
its stop file at 20:04 (it left at 20:28, at its next wake), the installed copy rebuilt
from `main` at `04be3dad`, rekordbox and its agent confirmed gone before
every verb. Both backup ages read 4.4 days (files 2026-10-09 14:24Z,
database 2026-10-09 15:17Z), so the session minted the acknowledgment
under the five day rule at 00:11Z, valid to 2026-10-14T12:11Z. The write
was rehearsed first on a copy (database cloned to a scratch directory on
the library volume with `cp -c`, `.cratekit` cloned to `.cratekit-copyrun`,
the installation state copied, config and state dirs redirected, its own
acknowledgment minted there at 00:08Z), then run live by the installed
`crate` through `live_gate.sh` on an equal digest, the session answering
`approve`. The copy and its state were removed after the live run.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `organize --only inspiration` (U144), the INSPIRATION backfill | rehearsed on the copy (plan 88 s, 78 provider calls, applied 86 s), live on an equal digest `3a4f66635677099d`, approved 20:13, applied by 20:14 (76 calls, none rate limited) | **16 INSPIRATION playlists created of 165 matched tracks**, every playlist read back by the verb; 2 sets skipped as already in INSPIRATION (`5_28_26 oshe GOATCHELLA Radio Mix 4-26`, `6_16_26 Pepofit PEPOFIT LIB JUNKYARD 5-26`); 1 set written nothing, no track of it matched (`6_17_26 David San (Oficial) DAVID SAN @ Psicodelica Podcast 2-24`, both tracks owned on disk and not in the collection); 4 misses named under their sets, below | live |
| `organize --only inspiration`, second run | live, plan only | 0 to apply, 1 with nothing to do, digest `48b7a6f9a49739ae`; the gate still asked (the `u143-a-clean-run-still-asks` residual) and was answered `abort` | read |
| rekordbox, desktop control | opened after the writes with both processes confirmed gone before and after, quit with `cmd+q` | opened 06:23 the next morning, once the feeder had left and `crate doctor` read both backup ages at 4 days (they cross five at 10:24 that morning); the INSPIRATION folder lists every one of the 16 new playlists under its full name beside the two sets already there and the two Public Service ones, each row count equal to the verb's read back; `6_19_26 Lee Burridge Playground Burning Man 10-24` opened to 12 tracks with artwork, key and BPM resolved, 1 h 15 min, 629.6 MB | read |

**The misses, by set.** `5_29_26 DOTB - Death on the Balcony Frisky Radio NYC
- 3hr Special 3-21`: 28, Pedro Madeira, Long Shadows, no library file
matches it. `5_29_26 DOTB - Death on the Balcony John Digweed 'Transitions'
Radio - Guest Mix 789`: 7, Max Cooper, Volition (Robag Wruhme's Botnax Caal
Remix), owned on disk and not in the collection. `5_29_26 When We Dip Radio
Amonita When We Dip Radio #167 [25.7.20] 7-20`: 5, Divana Project, Kebo
Giro, owned on disk and not in the collection. `6_19_26 Lee Burridge
Playground Burning Man 10-24`: 12, Spiller, Groovejet (If This Ain't Love)
(Purple Disco Machine & Lorenz Rhode Remix), owned on disk and not in the
collection. With the David San set's two, six owned files are on disk with
no collection row; they join a playlist once rekordbox holds them.

**The playlists made, with their rows.** LP Giobbi This Is Femme House Mix
9; Alex Twin opening set for PAWSA 17; DOTB Frisky Radio NYC 27; DOTB John
Digweed Transitions 789 6; Desert in Me Kora Desert In Podcast 15 9; Fulltone
Fusion Festival 7; When We Dip Radio Amonita #167 5; ƒernab verbimmelt #4
Fulltone 4; Atish Never Sleep Again Burning Man 14; OSHE Bonnaroo For Goats
10; Lee Burridge Hotel Humboldt 11; Lee Burridge Playground Burning Man 12;
Sebastien Leger Lost Miracle 093 6; Sebastien Leger Lost Miracle 094 6; DHA
FM Atish & Hoj 3; hoj Hoj b2b Lee Burridge Burning Man 2012 19. Each under
its full account name without the `DOWNLOADED ` prefix.

**What the sitting leaves.** Every downloaded set on the account has its
INSPIRATION playlist except the David San set, which has no matchable row
until its two files are in the collection. The run's JSON is under
`~/.local/state/cratekit/live/inspiration*.json` and `ack-live*.json`.

**A trap for the next sitting.** The feeder's lock file is held with `flock`
on a file that is never removed (`cratekit-board.feeder.lock`, dated
2026-09-20), so a waiter that polls for the file to vanish never fires. Poll
the feeder's pid, or the "leaving" line in its log. The waiter set at 20:04
did neither and the harness ended it at thirty minutes, which is why the
rekordbox read waited for the morning.

## Sitting 41, 2026-10-14, 06:37 to 08:05, Phillip present from 06:50, stopped on his word

Phillip, 06:37, by the restart prompt: run the account steps the last four units
owe (U140's rename, U142's sets archive, U143's root step, twice), read the
root back, then list the pairing candidates for his custom playlists. Then,
by message while it ran: "don't backup today", "proceed without asking me any
questions", "if longer than 20 min, stop and file it for a future run", "is
it reasonable to complete the tidal library playlist and folder reorg in the
next hour?", "I want all the playlists at the root to be filed when this is
done", "if they haven't been downloaded, just delete them" (the ` LIBRARY`
copies), and at 08:02 "just stop here and I will delete and reorg them by
hand". The feeder was idle (pid 39040, nothing Ready but #29) and was left
running, since no card was filed before it. `crate doctor` read clean with
both backup ages at 4 days; the acknowledgment of sitting 40 held to
2026-10-14T12:11Z; rekordbox and its agent were confirmed gone before every
verb and were not opened. No rehearsal copy was made for the account steps:
they write the account only, and the account is not copied, so each live
plan was read at its gate instead. No database write, no backup, no beat
grid. The actor on every gate was `session`.

**The first finding was the clock.** A read of the account root through the
product's own client, folders and every folder's playlists, ran 24 minutes
and was stopped; instrumented, with every request counted by path, the
account's 624 playlists cost 637 calls in 640 seconds and the 31 folders'
playlists 648 calls in 651 seconds, 1,233 of the 1,285 being
`GET /v1/playlists/<id>`, one per playlist parsed, against 53 page requests.
At the gate's default pace of one call a second that is eleven minutes per
listing, and `organize` lists the account when it plans and again when it
applies, which is where sitting 39's 22 minute report and 45 minute apply
went. R-1016, with a card. On Phillip's ask the pace was halved,
`provider.min_interval_s` 1.0 to 0.5 in the live config (backup
`config.toml.bak-2026-10-14-before-pacing`), and stayed there: 5,500 calls
at that pace drew no rate limit answer (`provider_gate.json` reads 0 rate
limited, 0 trips, 166,884 calls lifetime at 07:29).

| Workflow | Ran | Observed | State |
|---|---|---|---|
| read of the account root, instrumented | live, read only, 07:02 to 07:24 | **31 root folders, 13 root playlists**: the Signal set `10_10_26 Public Service NYC Live at Signal 2-26` (38), eleven ` LIBRARY` copies (four Colorize at 144, five Sol Selectas at 197, one Rebellion at 3, one Do Not Sit On The Furniture at 11), `tech_house_hits - Phil` (5); `Downloaded Sets 2026` 19, `2026` 2, `2026 Custom Playlists` 53 (52 `DOWNLOADED` and the unprefixed `lisa_7/16`); the Vonking set is on the account under no name, and `Untitled Playlist` is gone from the root; the probe folder `Cratekit nesting probe A` stood at the root with B and C inside it | read |
| the three `Cratekit nesting probe` folders, step 1 | by hand through the client, the 2026-10-13 cleanup script, 07:25 | **B, C and A removed**, the root read back with none | live |
| `export set --rename 2026-10-10T14:59:24Z-a4b0` (U140), step 2 | live, 07:25, refused before its gate | **`export-set-rename-unresolved`, nothing written**: the ledger records the set under `10_10_26 Public Service NYC Live at Signal 2-26`, the name its landing wrote (session `2026-10-10T16:09:29Z-714e`), and the verb looked only under the INSPIRATION name `3_25_26 Public Service NYC Live at Signal 2-26` and the two names the job's page words give, `… Live @ Signal: 2.16.2026 3-26` on the posted and the queued day. R-1017, with a card. The Signal rename stays owed | refused |
| `organize --only sets` (U142), step 3 | live, 07:25, plan only, the gate answered `abort` | **0 to apply, 2 listed only, digest `a5b6aad2206399f7`**: Signal waiting, no intake file named for it and no INSPIRATION playlist of its recorded name (the rename above is the proof it lacks); `tech_house_hits - Phil` waiting on the same reason. Vonking is in no ledger map and was not planned, as the brief allows. The read back stays 19 plus 0 | read |
| `organize --only root` (U143), step 4, first run | live, planned 07:26 to 07:45 (2,213 calls, none rate limited), the gate answered `apply` at 07:45, the apply ended by hand at 08:03 on Phillip's word, still in its second listing | plan: **remove `Rebellion LIBRARY`** (every track in the label folder), **move 53 playlists out of `2026 Custom Playlists` into `2026`**, leave ten debris copies naming the tracks their label folders lack (Colorize 39 of 144 each, Sol Selectas 29 of 197 each, Do Not Sit On The Furniture 5 of 11), leave the legacy folder for the later run; digest `e0574ae2454744fa`. **Nothing was written**: `2026` reads 2 and `2026 Custom Playlists` 53 after the stop, so the account is as the first read shows it, less the probe folders | planned, not applied |
| `organize --only root`, second run, step 4 | not run | the first apply never emptied the folder | not run |
| rekordbox, step 5 | not opened | the account steps changed nothing in rekordbox and Phillip stopped the sitting before the read | not run |
| the pairing candidates (U130), Phillip's standing wish | both sides listed, read only; rekordbox from a database copy cloned with `cp -c` to a scratch directory on the volume and removed after | account side: `tech_house_hits - Phil` was the one working custom playlist at the root, and Phillip deleted it by hand at 07:50 (its `sets` record outlives it, R-1018); rekordbox side: **204 plain playlists outside Cratekit's trees**, by top folder ARCHIVE 92, GIG READY 43, MOODS 20, Genre Trivia! 18, Favorites 12, WIP 9, TOOLBOX 6, Bandcamp Purchases 2, root 2. No pair was marked and nothing was synced: a first sync writes rekordbox behind the acknowledgment and queues every unmatched track for acquisition, so the pairs are Phillip's to name | read |

**What the sitting leaves.** Phillip is deleting the ten ` LIBRARY` copies
and reorganising the root by hand, his decision of 08:02, which overrides
the plan's leave rule for those copies (their undownloaded tracks are 39, 29
and 5 per copy, named in the run `2026-10-14T11:26:38Z-fe27`). The Signal
set stays at the root under its old name until R-1017 lands, and the
Rebellion copy and the legacy folder stay until he moves them or the root
step runs again. The provider pace is half a second. The run envelopes are
under `~/.local/state/cratekit/live/{rename,sets,root}.act1.json`; the
instrumented read and the candidate list are in the session's scratch
directory and summarised above.

**A trap for the next sitting.** Budget an account step by its listings, not
its writes: at the half second pace a listing is about five and a half
minutes and an organize step pays two, so plan, read and apply is twelve
minutes before the first write, and the old one second pace doubles it.
Run every account step under nohup with a pid waiter.

## What blocks a full sync cycle, stated plainly

**Nothing on the board, as of sitting 15.** #212 closed on 2026-09-29: the
routing tree is database native and adoption has written it. Sitting 10's
finding stands for every tree still on the xml bridge, `inbox` and
`record_labels`: an import lands a playlist at the root (R-687) and sets
attributes only on rows it creates (R-688). Line 4 of #178, the full sync
cycle, is next and is attended.

## Next sitting

**The account root is Phillip's by hand as of sitting 41 (2026-10-14).**
He stopped the root step and is deleting the ten ` LIBRARY` copies and
filing the rest himself. Before the next account step: read the root back
first, since it will not match any plan written here. Owed from sitting 41,
in this order: R-1017 landed, then U140's Signal rename live
(`crate export set --rename 2026-10-10T14:59:24Z-a4b0`, read back as
`3_25_26 Public Service NYC Live at Signal 2-26`, `export set` planning no
twin), then `organize --only sets` archiving it into `Downloaded Sets 2026`
(read back 19 plus 1; Vonking is on the account under no name and in no
ledger map), then `organize --only root` twice over whatever he left. Budget
each by its listings (the trap above). The pairing candidates for U130 are
listed in sitting 41; Phillip names the pairs, and nothing is marked until he
does. R-1016 is the card that makes any of this fast.

**The INBOX account playlists, Soul, Hip-Hop and Jazz are current as of
sitting 39 (2026-10-13), unattended.** A35 and A38 closed; the Signal set is
named for its posted day in rekordbox, the account half waits on U140 (#317);
the account's root playlists are filed by U131's rule (U137's first live run). As of sitting 38 before it,
the favourites, the vocal tags and the taxonomy were current. A34, A36 and A37 closed on equal digests; A35 (#301)
waits on U134, the refill verb. Owed from that sitting: A38, letting Soul and
Hip-Hop into the live taxonomy by hand and moving their tracks; the Vonking
set's account playlist once R-949 or U136 names the day; U136's attended
rename of the two Public Service playlists to their posted dates. U126's
live proof still stands as owed: the first native landing on the rebuilt
copy, one landed row dragged to a deck and recorded here, and
`link-majority-unclear` on its gate is R-969.

One thing is left of the genre work, and it is the author's: `crate delete
review` over the 36 tracks removed from the collection at sitting 29, run
from his Terminal, since the session's permission check refuses that verb.

Owed by the author: the 2,416 label releases in review and a look at the
339 held; a genre on the rows that still carry none, 1,308 by adoption's
count, 637 of them with no genre on the file either; the 20 label tracks
held as other versions.

Owed, the author's: the first `crate label sync` run, label by label, and its
go; one label built with `crate label playlists` and read in the web player,
which label being his call given R-872 and R-836; one label's created year
playlists pruned with `crate label prune` and read back, which closes R-836
and says whether R-894 occurs; the set `tech_house_hits -
Phil`, on the account since sitting 30, archived after its download; the
DJ_tools docs commit #252's task left unpushed.

Owed for R-790, issue #234: follow a new label, sweep it once, and record
here that it filed `labels.offer_per_sweep` releases, ten unless set, and
that `crate review list --queue label-release --group-by label` counts the
rest as `beyond`.
