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

## Sitting 42, 2026-10-15, 04:53 to 13:12, unattended, the `/board-up` session under the overnight authority

Phillip, 2026-10-14 23:10, going to bed: "If there is more than one halt or
something gets refused, fix it, don't stop it. Continue until you get this
right. Don't stop and don't ask me any questions." The night's cards, #322
(R-1016), #323 (R-1017), #324 (U145), #325 (U146) and #326 (U147), were built
by the feeder and landed and pushed by the watcher between 23:35 and 04:50
(`9c95a916`, residuals numbered as `a8d81f0a`); #322 halted once on a mounted
installer image the operator ejected and was landed by hand, #324 halted once
on a pre flight the watcher's own residual step dirtied. The feeder was then
kept up for U148 (#327), the `board.py` item limit the watcher found when the
audit could not reach 0 on a 316 item project. Every live step below ran with
rekordbox closed, from the installed copy rebuilt at `9c95a916`, the backup
run first (files 4,330 s, 2,240 of 96,885 files sent; database at 10:05Z),
and the acknowledgment minted as `session` at 06:08 (both ages under five
days, valid to 22:08Z). Every database write was rehearsed on a copy
(`copy_setup.sh`: the database cloned to `copyrun/`, `.cratekit` to
`.cratekit-copyrun`, the installation state and the acknowledgment copied,
the config derived from the live one) and then driven live through
`live_gate.sh` as `session`. The live database read `4d3fd29eeeef77af` before
the first write, `213db969cbf3953d` after the backfill, `1be9cdbbbe735f53`
after rekordbox quit and `1ac2b01bd15fb18d` after the refresh. The live pace was
lowered from 0.5 s to 0.25 s at 05:17 for the mirror's first build
(`config.toml.bak-2026-10-15-before-s42-pacing`), on the 2026-10-14 probe
that drew no rate limit at ten calls a second.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| R-1016, #322, the listing cost | live, read, `listing.account_playlists` through the product's gate with requests counted by path | **613 playlists in 7.1 s, 14 requests**, every one `GET users/<id>/playlistsAndFavoritePlaylists`, no fetch per playlist; 637 calls and 640 s on 2026-10-14 | read |
| R-1017, #323, `export set --rename 2026-10-10T14:59:24Z-a4b0` | live, digest `fe01189f92d3f699`, approved as session | **account playlist `ed84daca` renamed `10_10_26 ...` to `3_25_26 Public Service NYC Live at Signal 2-26`**, the job's name frozen, the ledger rekeyed, 5 calls | live |
| `export set`, the twin check | live, act 1 read then aborted | count 0, nothing to write; five INSPIRATION playlists listed as left for a later sitting because no succeeded set job names them | read |
| `organize --only sets` | report in 2 s (the listing cost fixed), live on digest `0204d59c2da1fcb4` | **the Signal set prefixed where it is, in `Downloaded Sets 2026`**, proven by its INSPIRATION playlist; 8 calls | live |
| U145, `favorites split` | rehearsed on the copy, live on an equal digest `62b043f103ce91dd` | **11 quarter playlists (191 members) split into 21 month playlists**, 2024-06 to 2026-10, plus Undated 7 (no date on any job or on the account; the account listed 9 hearts short, withheld), every quarter retired; second run NO_OP | live |
| U146, `favorites backfill` | rehearsed on the copy `3e1f7f3107cf97d8`, live `05e4ed0aa6960120`; every one of the 58 items and every count equal, the difference the month playlist row ids made separately on each side, approved as session under the 2026-10-09 rule | **58 owned hearts placed, 109 memberships**, 58 into All Favorites and the rest into 2024-06 1, 2024-07 5, 2025-07 1, 2026-02 1, 2026-07 32, 2026-08 1, 2026-09 4, 2026-10 13; 177 already placed; every playlist read back; second run plans 0 with 235 already placed but still opens its gate (residual below) | live |
| U146, a fresh heart on an owned track | one heart added on the account by the session, `Okonkolo - Elegua` (113042695, ISRC QZ2L61800050, from the Signal set's playlist) | the backfill plans nothing for it, by design: it places hearts a hearts job has listed, and a new heart reaches the library through a sync pass, which downloads unowned hearts and needs the acquisition tail; **left for the next real sync pass**, which is the brief's R4 | account |
| U147, `organize --only mirror`, the first build, three attempts | first attempt 05:18 to 08:41: plan 12,305 requests in 7,548 s at 0.25 s (digest `41f2b4ff074ce2fa`, 23 folders, 6,525 adds), approved, then the apply's own pass refused `decision-stale` because the split and backfill had changed the Favorites folder between the two reads; second attempt 08:42 to 10:33 at 0.1 s: plan 12,307 requests in 3,166 s (`ab7e101bb9347599`, 6,624 adds, 6,245 unmatched), apply wrote 22 root folders and 170 playlists then failed `unavailable-transient` on House / Funky House / Disco (a 412 on a 100 track add, 31,009 calls, none rate limited); resume 10:33 to 11:40: plan 7,215 requests in 2,001 s (`28cca4f0f914c121`), 21 folders already equal, House's 4 playlists and 400 tracks written, one swap in Nu Disco / Indie Dance (the session's heart on `Okonkolo - Elegua` tipping a tie to the hearted release) | **22 genre folders at the root, each with its playlists named `<Folder> <Playlist>`, 174 mirror playlists, Favorites adopted with All Favorites, 20 months and Undated beside the seven old `DOWNLOADED` quarters**; 6,624 tracks on the account, 6,245 rows unmatched: 4,213 on an ISRC tie between agreeing releases with no album tag, 1,873 with no ISRC, 91 the tie with an album tag, 66 with no provider track (residual below); about 88,000 provider calls across the three attempts, none rate limited | live |
| `favorites refresh` | rehearsed on the copy, live on an equal digest `382ea3da3d7cfcb4` | **56 memberships added across the 22 genre Favorites**, 1 playlist created, 0 removed, every folder read back | live |
| U147, the run after the refresh | 12:07 to 13:11, plan 7,219 requests in 1,930 s, digest `f53800c585e5c697`, approved as session | **the plan held exactly the refresh's consequences and nothing else: 51 adds across 14 genre Favorites (51 of the 56 refreshed memberships matched on the account) and one playlist created, `Techno Favorites`, 0 removes, 9 folders with nothing to do**; applied, 18,219 calls, none rate limited | live |
| rekordbox, desktop control | opened 12:02 after the last database write, both processes confirmed gone after `cmd+q` at 12:06 (Phillip's call ran over, so the session waited while Zoom was in front) | **All Favorites 241**; the Favorites folder reads 2024-06 7, 2024-07 15, 2024-08 1, 2024-10 2, 2024-12 4, 2025-02 2, 2025-05 1, 2025-06 1, 2025-07 2, 2025-08 2, 2025-09 1, 2026-01 4, 2026-02 4, 2026-04 2, 2026-05 2, 2026-06 10, 2026-07 103, 2026-08 5, 2026-09 37, 2026-10 30, Undated 6, **no quarter playlist**; the genre Favorites as before the refresh (Deep House 17, Tech House 17, House 17, Minimal 5, Progressive 9, R&B 5, Hip-Hop 1, Soul 5) | live |
| the account, read back | through the product's listing, 12:40; the TIDAL desktop app is blocked for computer use by policy and the Chrome extension refused to connect (signed into another claude.ai account than this login), so no screen read | 52 root folders, the 22 genre folders and Favorites among them, every genre folder holding its full playlist set (Afro House 7, Chill / Ambient 2, Hip-Hop 5, Jazz 4, NonElectronic 12, Favorites 29) | read |
| U148, #327, the mutation table the relay task could not measure | driven on main at 11:43 with no live verb running | **17 rows, 17 killed**, committed as `04a1b896` | main |

**What the sitting leaves.** The genre tree and the Favorites folder are on
the account and the ledger links every matched row, so a refresh plans in
about half an hour and writes only the differences. The heart on `Okonkolo -
Elegua` stands on the account for the next sync pass to place (U146's R4 by
the sync path was not driven: it downloads unowned hearts and needs the
acquisition tail). The copy run was removed from the volume. The live pace
stays at 0.1 s, set in three steps (0.25 at 05:17, 0.15 at 06:51, 0.1 at
08:42) with no rate limit answer in about 100,000 calls; the backup of the
config before the first step is `config.toml.bak-2026-10-15-before-s42-pacing`.
The `attended` plan branch (`aeb36f19`, the 2026-10-14 brainstorm) was merged
into main as `4add803d`. The month playlist 2026-07 reads 103 where the split
placed 78 and the backfill named 32 for it: the backfill adds a month
membership only where the member lacks one, 109 memberships for 58 hearts, so
seven of its 32 were already there from the split, and Undated reads 6 against
the split's 7 named, unexplained and left for the next sitting to read.

**Residuals of the sitting, filed unnumbered under `docs/residuals/`:** the
mirror plans the whole account twice per run and a library write between the
passes stales the decision (`s42-the-mirror-plans-twice...`); two thirds of
the mirror's unmatched rows are a tie between agreeing releases the matcher
refuses (`s42-the-mirror-leaves...`); the backfill opens its gate with nothing
to place where the split ends NO_OP (`s42-the-backfill-asks...`).

## What blocks a full sync cycle, stated plainly

**Nothing on the board, as of sitting 15.** #212 closed on 2026-09-29: the
routing tree is database native and adoption has written it. Sitting 10's
finding stands for every tree still on the xml bridge, `inbox` and
`record_labels`: an import lands a playlist at the root (R-687) and sets
attributes only on rows it creates (R-688). Line 4 of #178, the full sync
cycle, is next and is attended.

## Sitting 43, 2026-10-16, the operator session, U153's live colour backfill

Phillip asked why his recent favourites imported without the pink colour.
They did: until U153 the product filed a heart into All Favorites and left
the row uncoloured, and Pink is the standing favourite signal the sweep reads.
U153 was built, reviewed, merged and pushed (`main` at `aa97f32d`, issue
#334), then this sitting coloured the library live.

Rehearsed on a disposable copy of the live database
(`~/.local/state/cratekit/copyrun`, removed after): `crate favorites backfill`
planned 0 memberships to add, 138 All Favorites members to colour Pink, 0
held, digest `78433db65e4f0879`, and the copy apply coloured all 138 and read
them back. Live, the ack was minted as `session` (both backups 1 day old,
under five), the digest equalled the rehearsal, approved as `session`, and the
verb coloured 138 rows Pink, read every one back from the database, and left
the collection unchanged. A second live run planned 0 rows to colour, which is
the idempotence check and the independent re-read: no grey member of All
Favorites remains. Undo is a restore of the landing's session. The library's
master.db is SQLCipher encrypted, so the binding's read-back is the only
direct read; a visual check in rekordbox is the one belt-and-braces step not
taken, and Phillip will see the pink dots on next open.

## Sitting 44, 2026-10-26, the attended session, U154's live shelve

Phillip asked why his batch folders had piled up under `Music` beside the
`Processed_Tracks` tree he kept by hand. The landing put each batch at
`Music/<batch>` and nothing moved it on. U154 was filed, built, reviewed,
merged and pushed (`main` at `ec944239`, issue #335), then this sitting filed
the batches live.

Backup first: both ages were 11 days, over the five day rule, so `backup run`
ran before anything, 2 of 2 settled, 198 files sent, both ages 0 days.
Rehearsed on a disposable copy (`.cratekit` cloned to `.cratekit-copyrun` on
the volume with `cp -Rpc`, the database copied into it, config and state dirs
redirected, doctor reading the scratch registry): `intake shelve --report
--all` planned 14 batches and 447 rows, digest `87b1a90cb27e56e5`, equal on
the copy and live. Two batches left with their reasons: `rekordbox_djoid` has
no date shape, and `2026-10-01-labels-1pct` holds 36 files of 186 with no
row in the collection, so it is not wholly imported. The copy apply shelved
the one file batch `2026-09-29-favorites` and read the row back under the
recorded base drive, the one `location_prefix_map`'s rule names, which is
where this library stores its paths,
file id and analysis path unchanged; the real folder was renamed back by hand
before the live plan, and the live report digest was the same after.

Live, the ack was minted as `session` (both ages under two hours), the live
gate's digest equalled the rehearsal's, approved as `session`, and the verb
moved 14 folders into `Processed_Tracks/2026/` and rewrote 447 rows, every
one read back at its planned path, session `2026-10-27T02:29:15Z-f964`.
Doctor afterwards reads the same 167 rows resolving to no file as before, so
no moved row was lost. The two run identifier batches filed as `09_23_26
Downloads` and `09_23_26 Downloads 2`, since nothing says what they came
from; renaming them is Phillip's. Undo is a restore of the shelve's session.
The 14 GB clone `.cratekit-copyrun` is left on the volume for Phillip to
remove, since the session's permission check refuses a removal at a volume's
top level.

## Sitting 45, 2026-10-27, the attended session, the labels batch shelved and the 36 settled

Phillip asked for sitting 44's leftovers to be finished with rekordbox driven
on his desktop. No desktop control tool was present in the session, so
rekordbox was not opened; everything below ran from the shell against the
database, and the rekordbox side is read through `doctor` and a file by file
comparison of the filed tree with the collection instead. Sitting 44's clone
was removed first. A second clone made for this sitting's rehearsal was
refused at the volume's top level, so its four subfolders were removed by full
path and the empty `.cratekit-copyrun` shell was removed with `rmdir` once
Phillip had finished his hand step, which the check allows.
A second session that afternoon reached the desktop control tool: outside the
desktop app the `computer-use` server is off per project until it is enabled
once from `/mcp`, and the work config directory had never had it enabled for
Cratekit while the personal one had. The three rekordbox rows below are that
session's, on the live library.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| The 36 files of `2026-10-01-labels-1pct` with no row | read | All 186 rows were in the collection on 2026-10-01 (the 12:47Z snapshot holds 186) and the 36 were gone by the 2026-10-02 20:36Z snapshot: sitting 29's removal of the label test's non dance tracks through rekordbox's own dialog, ten Torr, ten Metanoia, eight Deodato, two Robsoul and six others. The live database holds no row for any of them, active or soft deleted, and no file of theirs sits elsewhere. They are rejections, not a failed import, and importing them again would undo sitting 29. | read |
| `crate delete review`, answered abort | refused before the gate | `deletion-reference-set-incomplete`: 153 active rows under no prefix rule, the streamed tracks and tombstones of R-675, so nothing is offered. It could not have offered the 36 anyway, since the pass reads the soft delete marker and these rows are gone outright. R-1037. | refused |
| The 36 to the Trash through `deletion.trash` | refused | The session's permission check refused the move as a deletion. Not retried. | not done |
| The 36 out of the batch | yes | A plain rename, each file to `Removed_from_collection/2026-10-01-labels-1pct` at the volume root, 919 MB, nothing deleted. The batch folder then held 150 files, every one with a row. Phillip dragged that folder to the volume's Trash the same day, read back there by the session. | live |
| `intake shelve --report 2026-10-01-labels-1pct` | copy and live | 1 batch, 150 rows, digest `42b3168abd3f6e00` on both. | measured |
| The copy apply | yes | Run `2026-10-27T11:31:20Z-ec82`, approved as `session`: 150 rows read back under the base drive at `Processed_Tracks/2026/10_01_26 labels-1pct`, none under the old path, file id and analysis path equal to the live rows'. The real folder was renamed back by hand and the live report's digest was unchanged after. | rehearsed |
| The live apply | yes | Sitting 44's backup acknowledgment was still valid, until 14:28Z. Run `2026-10-27T11:32:04Z-6ff1`, the gate's digest equal to the rehearsal's, approved as `session`, 150 rows rewritten, session `2026-10-27T11:32:42Z-b2a8`. Doctor reads 167 rows resolving to no file, as before. `Music` holds `Processed_Tracks`, `Set_Recordings`, `rekordbox_djoid` and the search results file, and no active row records a path under `Music` outside those three folders. | live |
| Every folder under `Processed_Tracks/2026` against the collection | read | The fifteen folders Cratekit filed match file for file, 597 rows. One name in `09_23_26 Downloads` differs in composition form only, the row composed and the file decomposed, and the row's path opens on disk. The hand filed folders carry their old shapes: playlist files and `already_in_library.txt` beside tracks, a few files with no row, a few rows spelled in the other form, subfolders the comparison did not descend into, none of it made here and the rowless files counted nowhere by doctor. | read |
| rekordbox, desktop control | opened 14:38 after `pgrep` showed nothing, the job list read empty and `doctor` read both backup ages at 0 days; quit with `cmd+q` at 14:45, both processes confirmed gone | The collection shows 10,384 tracks against 10,535 active rows, the 151 streaming rows as at sitting 17. The labels batch read by search: `Are You Feeling Lonely` (Coss) and `Toy Carousel (Kadosh Remix)` (Zakir), each one row with preview waveform and artwork and no missing marker, dragged to decks 1 and 2, each loading with its full waveform, Coss 1A 105.00, Zakir 12B 120.00 against the 96 in its file name. Monologue's transparent window refused the first drag, as at sitting 20, and was granted for the session. | read |
| Sitting 44's folders, two spot checks | by search and drag | `Same Girl (with Usher)` from `09_29_26 favorites` and `Bottled Up` from `10_08_26 Labels` each loaded to a deck with a full waveform; Same Girl reads 2B 140.00 against the 03B 144 in its name. The Bottled Up search listed three Afriqua rows, the two dubs beside it, all with previews. | read |
| Missing files, rekordbox's own list | File, Display All Missing Files, closed with OK, nothing relocated or deleted | **8 tracks**, every one a rekordbox demo track (`House 1` to `House 4`, `Breaks 1` to `Breaks 3`, `Techno 1`, artist `rekordbox`, album `GROOVE CIRCUIT`) under the rekordbox folder of another user account's home on this machine. Nothing under `Processed_Tracks`, so none of the 150 shelved today and none of sitting 44's 447 rows is missing to rekordbox. Doctor's 167 rows resolving to no file are a different count: 153 are rows under no prefix rule, the streamed tracks and tombstones of R-675, and how the remaining 14 relate to these 8 was not read. | read |

The two run identifier batches are now known: `09_23_26 Downloads` is
sitting 8's 54 account favourites, run `4773`, and `09_23_26 Downloads 2` is
the 7 tracks acquired for the account playlist of job `673e`, run `d66b`. No
verb renames a filed folder and a rename in Finder breaks 61 rows, so they
keep their names until a unit gives shelve a rename.

## Sitting 46, 2026-10-27, the attended session, the first Bandcamp batch, PULS

Phillip asked for a command line tool that batch downloads his Bandcamp
purchases and for those files to go through the intake chain. The tool
chosen is `bandcampsync` 0.8.0 (meeb/bandcampsync, pipx), which syncs the
account's purchases into `Artist/Album/` folders, tracks what it has fetched
by an ignore file of item ids and a checkpoint, and downloads FLAC by
default. It signs in with the browser's cookie copied by hand from the
Network tab, kept at `~/.config/bandcampsync/cookies.txt` (mode 600, outside
every repository), since Bandcamp's login form has a CAPTCHA. Nothing of
this is in the product yet: the download, the flatten and the ownership
check ran as shell steps, the verbs took over from `tag folder` on.

The account holds 102 purchases. A dry run listed them; a name match of each
release against the 10,581 audio files on the volume read 49 as already
owned, spread from the 3rd purchase to the 101st, so no date cutoff separates
owned from new and the ignore file is the instrument. Phillip then scoped
the batch to one seller: the collection endpoint's `item_url` names the
seller's account, and 55 of the 102 are `pulsromania.bandcamp.com`, 10 of
them owned by the title match. An ignore file of 57 ids (the 47 other
sellers and those 10) left 45 releases, 97 FLAC, 5.5 GB, every file with
cover art embedded and artist, title, album, album artist, year and track
number tags, no genre and no label tag (PULS appears only as a comment
reading `Visit https://pulsromania.bandcamp.com`). A track level check of
the 97 against the volume found one duplicate, LRNT `Dumbellz` on
*Deep Rollers Compilation*, already in the library from *Wavy Attitude VA*
(`Processed_Tracks/2026/bandcamp_2_3_26`); it was left in the Bandcamp tree
and not staged. The real run appended the 45 ids below the ignore file's
delimiter and wrote the checkpoint, so later runs look at newer purchases
only: a release skipped today comes back only if its line is removed and
`.bandcampsync-state.json` deleted.

Another Cratekit session was live on this machine the whole sitting, driving
its own batch of 116 in `Downloads` through `analyze run` and holding a
native land plan at its gate. The two sessions coordinated by message: this
one staged beside `Downloads` rather than in it, told the other before
taking the rehearsal copy and before opening rekordbox, and the other held
every verb until told rekordbox was closed. The product's locks (the write
session lock, the per batch landing lock, the job lock) would have
serialised the database writes either way; what they do not prevent is two
sessions sweeping one folder, which is why the staging folder was separate.

Phillip's two decisions for the batch: every PULS track is `Rominimal`, and
PULS gets a label folder. `Rominimal` reaches `minimal_deep_tech` by the
`minimal` fuzzy rule today, so the tag was written on the files; its own
place under Minimal / Deep Tech cannot be declared, since a bucket that
routes by source genre never consults energy (`routing.py`'s
`sub_by_source` branch, `taxonomy._band_names`), and a Rominimal sub would
take the three energy bands off every track in the bucket. Phillip chose to
card it rather than make Rominimal a top level bucket: **U155, #336**. The
label folder cannot be filed by a native landing (R-771: `--manifest` is
refused, and the Record Labels tree has no database writer), so it was built
by hand in rekordbox below and carded as **U156, #337**, which closes R-771.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `bandcampsync --dry-run`, then the seller split | read | 102 purchases, 24 sellers; 55 PULS. Owned by title match: 49 of 102, 10 of the 55. | read |
| `bandcampsync` into the volume's `Bandcamp` folder with the ignore file | yes, 3m24s | 45 releases, 97 FLAC, 5.5 GB; 42 releases of two tracks, one of three, two of five. No tag, name or art problem; longest name 76 bytes, no two alike. | live |
| The flatten and the duplicate | by hand | 96 files moved flat into a staging folder with `mv -n`; the one `Dumbellz` left behind. First staged at `Bandcamp-staging/2026-10-27 PULS` beside `Downloads`, which the landing refused (`intake-list-unusable`: inside the library and outside download staging, so already owned), then moved to `Downloads/2026-10-27 PULS`, which it took. The other session's sweep of `Downloads` had finished by then. | live |
| `tag folder` | job `2026-10-27T20:06:04Z-2ce2` | 96 of 96 settled, 96 untagged: Traxsource and Bandcamp blocked on all 96 (as every sitting since 32), Deezer not asked for want of an ISRC, Beatport no hit. Art present on all, so none fetched. | live |
| `GENRE=Rominimal` on the 96 | by hand, mutagen, verified | every other tag and the picture block unchanged on every file. | live |
| `analyze run`, `analyze restamp` | jobs `2026-10-27T20:15:29Z-e818`, `2026-10-27T20:54:48Z-9d61` | 96 of 96 each; `initialkey`, `energylevel`, `voxlevel` and the vox gender fields written. The restamp's `db-metadata-not-written` warning as always. | live |
| `name apply --root` | run `2026-10-27T21:01:08Z-d7e1`, answered abort | **0 renames, 0 held**: a Bandcamp file is named `Artist - Album - NN Title` by the seller's zip, a stem carrying text, which the verb carries as it is (R-168), and `analyze run` had already renamed every file to its key and tempo head (`01A - 127 - Bernar - ilustratii 008 - 02 Black Woman Experience.flac`), so nothing was left to rename. Corrected after the commit: this row first said the head was absent on this batch, which the landed names contradict. | no_op |
| `intake land --name "2026-10-27 PULS"`, native, rehearsal | on the copy (`copy_setup.sh`, state redirected, doctor reading the scratch registry), run `2026-10-27T21:05:15Z-5ef7`, applied | digest `ddeb6620b2dc2056`, 96 adds, 0 present, content link 2950670, 1 vox My Tag at the other session's new cut of 3. The 96 files moved back by the plan's own mapping and the empty batch folder removed. | rehearsed |
| `intake land`, native, live | run `2026-10-27T21:06:02Z-77d5`, the live database's sha256 `a865f4bc` unchanged since the copy, digest `215aba93d37bc186` against the rehearsal's, the only differing lines the digest and the database path (R-922), approved as `session` | **96 rows into `Music/2026-10-27 PULS`, the playlist `INBOX / 2026-10-27 PULS`**, staging left empty, each row with the ten columns rekordbox derives left empty. Doctor clean after, no new open session. | live |
| rekordbox, desktop control | opened 17:11 after `pgrep` showed no crate process and both rekordbox processes gone, once the other session had released the desktop control lock at Phillip's word; every `screenshot` call failed, so the session drove it from `screencapture` images (the learning filed with this record); quit from the application menu at 17:35, both processes confirmed gone | **Analyze Tracks on the 96** with BPM/Grid, high precision and Phrase on and KEY off (sitting 45's settings), about eleven minutes for 96, read as done when the analysis store held 96 new `ANLZ0000.DAT`; **Reload Tags** filled key, year, artist and the `Rominimal` genre on all 96. The Year column read 0 on every landed row before the reload, so the native landing carries no year. **`Record Labels / PULS` built by hand**, `PULS 2018` and `PULS 2020` to `PULS 2026`: 3, 16, 26, 2, 10, 8, 6 and 25 tracks, filed by sorting the INBOX playlist on the Year column and dragging each run, every count equal to the files' date tags, 96 in all. Two rekordbox rules paid for on the way: a folder or playlist cannot be made while the tree's search filter is set (`Playlist cannot be edited or deleted while searching`), and the Playlist menu's Create New Playlist creates nothing while a playlist rather than its folder is selected, with the typed name going to the tree's type ahead instead. | live |
| `board.py sync` and `audit` after the two cards | yes | #336 and #337 Ready; 159 units, 153 done, 5 ready, 1 blocked; the board matches the repository. | measured |

The desktop control lock was held by the other session, idle since its
acquisition, and it had no tool to release it; Phillip had its lock file
deleted. Every `screenshot` call then failed in this session while the
clicks worked, so the sitting was driven from `screencapture` images read
by the session, with the capture's own pixels as the click coordinates. The
learning is filed with this record.

Left for Phillip: the rehearsal's scratch copy at the volume root, `copyrun`
and `.cratekit-copyrun`, since the session's recursive removal was refused
by its permission check; the next backup mirrors them until removed. The
`Bandcamp` tree on the volume holds the 45 album folders with their
`cover.jpg`, `bandcamp_item_id.txt` and the one unstaged `Dumbellz`, plus
the ignore file and checkpoint, and is the folder the next sync writes into.

## Sitting 47, 2026-10-27, the attended session, a sync pass landed and both of the day's batches reanalysed

Phillip asked what a sync includes, then for `crate sync all`, and took the
pass through to rekordbox. This session ran beside sitting 46's, which held
the rehearsal copy and rekordbox in turn; the two coordinated by message and
neither ran a verb while the other held the library.

The pass went out of order first. The download was landed straight after
`acquire download`, skipping `tag folder`, `analyze run`, `analyze restamp`
and `name apply`, and the first land plan showed it: 116 rows named by
provider id and no vox score on any. That plan was aborted, the four steps
were run, and the land replanned. Phillip set the vocal cut from 5 to 3 by
hand after reading the scores (`crate analyze calibrate --vocal-cut 3`,
run `ad54`), which holds library wide from now on.

**The analysis settings sittings 45 and 46 recorded are not Phillip's
standard.** Both rows above say BPM/Grid, high precision and Phrase on and
KEY off, which is the state the dialog remembered, with Analysis Mode on
Dynamic. Phillip's standard, stated here: **Analysis Mode Normal, high
precision off, BPM/Grid, Phrase and KEY on, Reload Tags before Analyze
Tracks** (Reload Tags reads the file's key tag and would overwrite
rekordbox's detected key if run after). KEY is on because the Key column is
rekordbox's key and the title head is Cratekit's, and a disagreement between
them is information for the DJ. Dynamic is for tracks whose tempo really
moves, which U157 will mark.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `sync all` | run `2026-10-27T19:07:06Z-21c7` | Playlists: 3 intake jobs. Favourites inbound: 1 job, 265 hearts listed of 274 declared, 9 withheld by the provider. Favourites outbound not queued, no export named. Labels left to `label sync`. 36 provider calls. | queued |
| The four intake jobs | `job resume`, each a detached worker | `9309`, `9d5f`, `f74c`, `6dd9`: 1, 18, 99 and 265 settled, none failed. `intake missing --run 21c7`: **117 missing**, 262 owned, 1 offered for review. | live |
| `acquire download` | job `2026-10-27T19:24:31Z-75b0` | **116 landed in staging; Calvin Harris `Satisfy` `lossy-refused`** (offered lossy only, as at sitting 15). 699 provider calls, no rate limit. | live |
| `intake land`, first plan | run `2026-10-27T19:43:33Z-571e`, not answered | 116 adds named `<id>.flac`, vox 0 of 116, every file unscored: the chain had been skipped. Superseded. | aborted by replan |
| `analyze run`, `name apply`, `tag folder`, `analyze restamp` | jobs `add0`, run `8a40`, job `6167`, job `8b6f` | 116 analysed. `name apply --root Downloads` from the repository checkout planned 0; the absolute path planned and applied **116 renames**, none held. `tag folder`: 87 given a genre, 2 left for unread sources, one `Latin Electronic` outside the taxonomy, Traxsource and Bandcamp blocked on 24. Restamp energy only, its `db-metadata-not-written` warning as always. | live |
| The vocal cut | `analyze calibrate --vocal-cut 3` | 5 to 3, set by hand. Of the 116: 80 score 0, 10 under 2, 14 from 2 to under 5, 12 at 5 or more; **19 tagged at 3**. | live |
| The backup acknowledgment | `session ack`, the gate answered with `run decide` | Both ages about 19 hours. The answer was recorded without `--actor session`, so it took the default actor `cli` and the terminal rule, and the verb refused with no controlling terminal (`backup-acknowledgment-no-terminal`). Minted under `script -q /dev/null`, recorded `decided_by: cli`, `rule: terminal`. The session's error, not U138's: answering as `session` takes the session rule with no terminal. | live |
| `intake land`, native, rehearsal | on the copy (`copy_setup.sh` rebuilt over sitting 46's, live and copy sha256 `baf3db37`), run `2026-10-27T21:54:27Z-0d57`, applied as `session` | digest `7fe79a59192ac844`, 116 adds, 19 vox, 8 hearts Pink into All Favorites and 2026-10. Copy read back: 10,631 to **10,747** active rows, the 116 with no BPM and not analysed, integrity ok. The 116 files moved back to staging by the plan's mapping and the empty folder removed; the live database's hash unchanged. | rehearsed |
| `intake land`, native, live | run `2026-10-27T21:55:36Z-5f8e`, approved as `session` | digest `4cf4cc4d41ec79b9`; against the rehearsal the only differing lines the run, the database path and the digest (R-922). **116 rows into `Music/2026-10-27 Tidal playlists and Favorites`**, batch playlist 5, Lisa_10_27_26 1, Idris precise beats 92 new of 98, The LIVING room 18. 10,747 active rows, integrity ok. Isolée `you are` left out of Idris precise beats: owned on disk, no row for its file. | live |
| rekordbox, first analysis | desktop control, the dialog as it opened: Dynamic, high precision on, KEY off | **All 116 grids variable**, 69 spanning more than 10 BPM inside one track (Feater 89 to 179, Floating Points 79 to 167, Shed 94 to 137). The 96 PULS rows of sitting 46 measured the same way: **96 of 96 variable**, a median span of 1.2 BPM. A random 40 of the older library: 6 variable, all live or orchestral. Every Cratekit batch analysed from 2026-09-29 to 2026-10-16: constant grids but 3 on 2026-10-15. | superseded |
| rekordbox, second analysis | the 92 Idris rows, Dynamic, high precision off | still variable, about 0.4 BPM drift. Phillip had it stopped: rekordbox quit mid run, both processes gone. | stopped |
| rekordbox, the standard | reopened; Reload Tags on the 116 (PULS had it at sitting 46), then Analyze Tracks on **all 212**, Normal, high precision off, BPM/Grid, Phrase and KEY on | **212 of 212 single tempo grids.** Key column filled on all 212. Quit, both processes gone; integrity ok. | live |
| Key agreement | read from the database | Title key against rekordbox's Key column: **98 equal, 114 differ, 23 of those one Camelot step**. Consistent with `_HEAD_AGREEMENT`'s 158 of 299 measured on 2026-09-30, not a regression. Carded as **U158, #341**. | measured |
| Cards | filed | **U157, #338**: a `dyn` My Tag on variable tempo rows so Analyze runs Normal and Dynamic on the right sets; the evidence above added to it. **U158, #341**: the key estimator. | Ready |
| `board.py sync` and `audit` | yes | 163 units, 153 done, 8 ready, 2 blocked; the board matches the repository. | measured |

Two desktop control facts. The lock passed back to this session by deleting
its file again, and `screenshot` failed again while clicks worked, so the
shell capture learning of sitting 46 held a second time; a clean `/mcp`
release is still untested. **The Analysis Mode control opens only while the
mouse is held down on it**: a click does nothing, so a drive presses, moves
to the item, and releases.

Left for Phillip: `crate intake shelve` for `2026-10-27 Tidal playlists and
Favorites` and `2026-10-27 PULS`, with `--report` first; the scratch copy
`copyrun` and `.cratekit-copyrun` at the volume root; `Satisfy` from another
source; a genre on the 29 rows `tag folder` could not give one; a taxonomy
alias for `Latin Electronic`; the one review item.

## Sitting 48, 2026-10-28, the attended session, the account side of two passes marked and filed

Phillip noticed the playlists sitting 47 landed still sat at the account root
under their own names. Nothing had failed: sitting 47 stopped at the
rekordbox analysis, and `sync mark` and `organize --only file` are separate
verbs that no sync driver runs (#333, U152, scopes `sync mark` out). Neither
verb writes the database, so no rehearsal or backup gate applies; rekordbox
stayed closed and no job was running throughout.

**There was no 2026-10-14 sync.** `Aa-Phil 10-14-26` was landed by the pass
`2026-10-15T234532Z-9c32_synced` (landing session `2026-10-16T00:38:54Z-ef36`),
the only native landing between 2026-10-09 and 2026-10-27 in the session log.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `sync mark --pass 2026-10-27T190706Z-21c7_synced` | run `2026-10-28T14:43:39Z-dbcc`, approved as `session` | **3 renamed**: `Lisa_10_27_26`, `Idris precise beats`, `The LIVING room`, each to `DOWNLOADED <name>`; left alone none. Idris counts Isolée `you are` as owned (on disk, no row), so it marks. 47 provider calls. | live |
| `organize --only root --report` | run `2026-10-28T14:44:47Z-4f25`, report only | Would move 53 playlists out of `2026 Custom Playlists` (52 `DOWNLOADED`, plus `lisa_7/16`) into the 2026 folder and remove the emptied folder on a later run. **Phillip said no**: `2026 Custom Playlists` stays as he arranged it. The root step does not file newly marked playlists; `--only file` does. | declined |
| `sync mark --pass 2026-10-15T234532Z-9c32_synced` | run `2026-10-28T14:51:09Z-58b3`, approved as `session` after Phillip read the gate | **2 renamed**: `Aa-Phil 10-14-26` and `lisa_10_11_26`. The gate takes both or neither, since `sync mark` has no per playlist narrowing. 44 provider calls. | live |
| `organize --only file` | run `2026-10-28T14:55:10Z-8273`, approved as `session` after Phillip read the report (digest `f8e834767a89e3c1`) | **5 moved from the root** into the existing 2026 folder: the five `DOWNLOADED` playlists above. None came from a folder, so `lisa_10_11_26` was not taken out of a hand filed place. 0 folders created. A report after it planned nothing. 154 provider calls. | live |

## Sitting 49, 2026-10-28, the attended session, the first release cut and installed

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `release.py plan` | on `main` at 75205bb0 | Proposed minor, v0.1.0 to v0.2.0, nothing marked breaking. Read and agreed. | read |
| `release.py cut --bump minor --mac-battery`, A47 (#375) | on the Mac | The full macOS battery (ruff, pytest, `scan_repo.py`) clean on the cut commit; release commit 40addf24, tag `v0.2.0` pushed with `main` atomically, release published: https://github.com/philgutowski/cratekit/releases/tag/v0.2.0 | live |
| A40 (#364), the macOS battery | the same run | The cut's battery is A40's three commands on `main` at the release. It covers R-1031, U161, U152, U176, U156, U158 and U159, all landed by then. **U166 had not landed** (#347 open), so its macOS run is owed by its own landing. | clean |
| The upgrade, A39 (#363) | `pipx install --force "cratekit[analysis] @ git+https://github.com/philgutowski/cratekit@v0.2.0"` | The old copy was 0.1.0 from a local checkout with librosa injected by hand; the `analysis` extra replaces the injection (librosa, numpy, scipy import). No vocals or web extra was installed before, none after. `crate --version` 0.2.0; `crate doctor` `install.release`: **this copy is 0.2.0, and the latest release is v0.2.0.** | live |

## Sitting 50, 2026-10-28, the attended session, the first `crate sync land`, with nothing to land

From the installed v0.2.0, rekordbox closed, both backup ages 1 day. A43 (#367) stays open: the pass had nothing to land, so no landing gate was reached, and A42 (#366) waits on the same gate.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `crate sync land` | run `2026-10-28T15:55:17Z-edca`, no answer asked | Steps 1 to 5 of 10 ran in order and stopped: preflight ok; `sync all` queued 1 job (favourites inbound, 268 hearts listed of 277 declared, 9 withheld by the provider); the job succeeded; **1 missing**, Calvin Harris `Satisfy`; the download refused it `lossy-refused`, as at sittings 15 and 47. `no_op`, 28 provider calls. Every playlist marked at sitting 48 had nothing missing. | no landing |
| Open intake jobs | named by the same run | **17 intake jobs from 2026-09-17 are still open** (`2026-09-17T16:44:44Z-3ea9` and 16 more), each holding its playlist out of every pass; the verb names `crate sync land --pass-run 2026-09-17T16:43:08Z-c92f` to continue them. Not run: left for Phillip to decide. | found |

## Sitting 51, 2026-10-30, the attended session, a sync pass landed natively on an equal digest

From the installed v0.3.0, rekordbox closed. Written up at sitting 52 from the
sitting's run files, its session record and the plan screens it saved, since
the sitting itself left the record in a comment on A48 (#376). Times are UTC,
so the runs carry 2026-10-31.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `crate sync land`, the first pass | run `2026-10-31T01:19:10Z-6dc3`, pass `2026-10-31T01:19:11Z-d351`, no answer asked | Steps 1 to 5 and stopped, as at sitting 50: one job (favourites inbound, 278 hearts listed of 287 declared, 9 withheld by the provider), **1 missing**, Calvin Harris `Satisfy`, refused `lossy-refused`; `no_op`, 30 provider calls. **17 intake jobs from 2026-09-17 still open**, the finding sitting 50 left for Phillip. | live |
| The 17 stale intake jobs | `crate job cancel` on each, at Phillip's word to clear them if still relevant | Judged by `job show`, which names tracks and a config drift warning but not the playlist: all 17 queued, six weeks old, frozen against an older configuration, five of them copies of one 144 track list and five of one 197 track list. All 17 cancelled, `job list` then showing none open. **They had been holding six playlists out of every pass**: the next pass queued 7 jobs where the first had queued 1, and found the 20 missing tracks below. Carded as **U182, #379**. | live |
| `crate sync land` | run `2026-10-31T01:24:02Z-5f08`, then continued as run `2026-10-31T01:39:41Z-65f2` over the pass `2026-10-31T012402Z-a951_synced` | **7 intake jobs** succeeded over the INBOX playlists and the favourites; **20 missing**, 19 downloaded, 1 refused `lossy-refused`; `tag folder` (Traxsource and Bandcamp blocked on every search), `analyze run`, `analyze restamp` (its `db-metadata-not-written` warning as always) and `name apply` ran in order. Step 10 stopped `PENDING_HUMAN` on the backup acknowledgment, which the verb never mints. A first continue named the wrong run and failed `job-unknown`, carded as **U183, #380**. | live |
| Vocal scores | `crate analyze vocals` from the development checkout | The installed copy carries `analysis` and not `vocals`, so the tail's `analyze run` wrote no `voxlevel`, and a second run skipped all 19 as done. Scored by hand and the rehearsal redone, about forty minutes. Carded as **U181, #378**. | live |
| `crate session ack` | run `2026-10-31T01:49:02Z-8648`, as `session` | Both backup ages under five days. Carded as **U184, #381**, one command for the session's ack. | live |
| `intake land`, native, rehearsal | on the copy in `copyrun` on the library volume, run `2026-10-31T02:00:02Z-db2a`, applied as `session` | digest **`b6744643eade55fe`**: 19 adds, 0 already present, 1 vox My Tag at cut 3, INBOX / Analyze made, 0 left in staging, 12 owned hearts into All Favorites and 2026-10 and coloured Pink, one account track left out (Alex Kaminski `Mana`, neither owned nor landed). | rehearsed |
| `intake land`, native, live | run `2026-10-31T02:00:59Z-99ba`, approved as `session` (run `2026-10-31T02:01:18Z-2e99`), session `2026-10-31T02:01:27Z-1031` | digest **`b6744643eade55fe`, equal to the rehearsal's**. The two plan screens differ only in the run id and the "reads and writes" path. Committed: 19 rows into `djmdContent`, 49 INBOX memberships, 24 favourites memberships and 12 rows coloured, 1 vocals association. 10,747 to 10,766 active rows, integrity ok, **INBOX / Analyze holds exactly 19**, files in `Music/2026-10-30 Tidal playlists and Favorites`, staging empty. | live |
| INBOX before the landing | read from the database | No playlist named `Analyze` directly under INBOX, the first check A48 (#376) owes. | read |
| Cards | filed | U181 to U184, #378 to #381, from the sitting's friction review. **U186, #394**, filed after it: two local sessions drove `crate inbox analyzed` at once (sitting 52's runs `2026-10-31T10:23:06Z-34c0` and an unanswered plan `2026-10-31T10:27:29Z-8f60`), and nothing told either that the other existed. | Ready |

**A42 (#366) is met here.** A native landing rehearsed on a disposable copy
and planned live gave the same digest, the case R-922 said could never occur
while the digest carried the database path. R-922 closes on this sitting.
**A43 (#367) reached its landing gate** through `crate sync land`'s own step
10, answered and applied as the session; it closes when the rekordbox visit
below is recorded. Still owed from this sitting: the rekordbox visit over
INBOX / Analyze (Reload Tags, then Analyze Tracks) and `crate inbox analyzed`,
which A48 (#376) carries.

## Sitting 52, 2026-10-31, the attended session, sitting 51's rows analysed and cleared from INBOX / Analyze

From the installed v0.3.0. Both backup ages 4 days, so no backup ran first.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| rekordbox, the analysis visit | by Phillip's hand, INBOX / Analyze only | Reload Tags on the 19 rows, then Analyze Tracks: Normal, high precision off, BPM/Grid, Phrase and KEY on, and Vocal on as well (rekordbox's own vocal position marks on the waveform, which Cratekit does not read). Completed; rekordbox quit, and `rekordbox` and `rekordboxAgent` both confirmed gone before any verb ran. | live |
| `crate inbox analyzed`, live plan | run `2026-10-31T10:23:06Z-34c0` | **clears 19** rows rekordbox analysed, **keeps 0**; writes the memberships of INBOX / Analyze only. digest **`792e43d7c999931f`**. | planned |
| `crate inbox analyzed`, rehearsal | on a fresh copy (`copy_setup.sh`, live sha256 `5cb744998d362700`), run `2026-10-31T10:28:50Z-48f8`, applied as `session` | The same digest, `792e43d7c999931f`; the two screens differ only in the run id. Applied: 19 cleared, INBOX / Analyze holds 0, read back. The copy's backup acknowledgment came from a terminal, since a copy has no recorded backup ages. **The setup script left the copy's library state with only `local/`**, so the first plan refused `tree-unconverged`; copying `coupled/` in by hand fixed it. | rehearsed |
| `crate inbox analyzed`, live | run `2026-10-31T10:23:06Z-34c0`, approved as `session` on the equal digest, session `2026-10-31T10:29:27Z-5d96` | **19 analysed rows left INBOX / Analyze, which now holds 0**, read back from the database; every track stays in the collection and its other playlists. The live database's sha256 was still `5cb744998d362700` just before the apply, so the rehearsal left it unchanged. | live |

**A48 (#376) and A43 (#367) are met.** A48: no stray `Analyze` playlist
before the landing (sitting 51), the landing put exactly 19 rows in the queue,
rekordbox analysed them, and the clear took out every analysed row and left
none. Its macOS battery passed inside the v0.3.0 cut (`release.py cut
--mac-battery`). A43: the landing `crate sync land` reached at sitting 51 is
now analysed in rekordbox.

## Sitting 53, 2026-11-03, the attended session, v0.5.0 cut and the vocal frames measured

From the installed v0.4.0 until the upgrade below. Both backup ages 7 days at the start, so `crate backup run` ran first.

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `release.py cut --bump minor --mac-battery`, first run | on the Mac at d8633c17 | Refused, red. Ruff refused one import block only on this venv's 0.16.1, while CI's 0.17.3 passes it; the venv moved to 0.17.3, no source changed. One test failed, `test_every_moved_paragraph_is_in_a_fragment_byte_for_byte`, 1 failed, 15976 passed, 1 skipped: U195 reworded a moved record. Carded as U199, built in the cloud and merged at 2568d7f6. | refused |
| `release.py cut --bump minor --mac-battery`, second run | on the Mac at 1631ed99 | The full macOS battery (ruff, pytest, `scan_repo.py`) clean on the cut commit; release commit 632a0fd0, tag `v0.5.0` pushed with `main` atomically, release published at https://github.com/philgutowski/cratekit/releases/tag/v0.5.0. | live |
| The macOS battery owed | the same run | **The cut's battery is the macOS battery every unit landed since v0.4.0 owed**, 41 merges, U188 through U199, named in the release notes. | live |
| A64 (#432), the vocal frames | read only, over `Music/2026-10-27 Tidal playlists and Favorites` and ten known vocal tracks | Distribution reproduces sitting 47 exactly: 80 at 0, 10 under 2, 14 from 2 to under 5, 12 at 5 or more. None undecodable, chunks match length. Donna Summer "I Feel Love", a sung lead, scored exactly 0. Tables on U171 (#352). | live |
| Stale branches | by Phillip's second session, on the local session's checks | Eleven remote branches deleted, ten `cloud/` and one fully merged `claude/`. `cloud/release-v0.2.0` held only the abandoned commit 673c64c4. | live |

## Sitting 54, 2026-11-04, the attended session, A83 (#492): U198's live run, 101 playlists made on the account

From the installed v0.6.0, which carries U198. Both backup ages about 1.4 and 1.1 days (files and database), so no backup ran first; `crate session ack --as session` minted the acknowledgment (run `2026-11-04T23:28:28Z-d87a`, valid 12 hours). rekordbox and rekordboxAgent were not running at any point and were never opened. The sitting ran past midnight UTC, so the later runs carry 2026-11-05. **The in-app read of rekordbox and the two hand changes were not done**: the session had no desktop control tools, and Phillip chose to restart with them. They are listed as OWED below.

A copy rehearsal was set up by hand, since `copy_setup.sh` no longer exists in any place a session can read: the database copied to `copyrun-u198/db/master.db` on the library volume, the volume's `.cratekit` copied to `.cratekit-copyrun` (coupled, local and history without the 14 GB of snapshots), `library.state_dirname` pointed at the copy, installation state and config redirected to a scratch directory, the live backup acknowledgment copied into the copy's `local/`. `crate doctor` on the copy read `tree.registry` at `.cratekit-copyrun/coupled/`. Both scratch directories were deleted from the volume afterwards. The live database read sha256 `85a86cfb0c94bf82` before the rehearsal and after the last run: **no rekordbox write happened** (see the table).

| Workflow | Ran | Observed | State |
|---|---|---|---|
| `crate sync pair`, rehearsal, first try | on the copy, run `2026-11-04T23:28:43Z-bdf0` | Stopped `REFUSED_BY_POLICY` after 500 calls to the provider, the default ceiling for one command (`[provider] calls_per_command`). A first discovery plan needs `--calls`; all later runs here used it. | rehearsed |
| `crate --calls 5000 sync pair`, rehearsal | on the copy, run `2026-11-04T23:31:43Z-55ac`, 8m00s, 4165 calls | Both gates read. **101 pairs found, 92 skipped, digest `ab30bca7046b28eb`, count 1637**, identical on both gates. Both gates answered `skip` as `session` (see why below); nothing written. | rehearsed |
| What the rehearsal gate listed | the same plan | **101 new pairs, one account playlist each**, in 7 account root folders: GIG READY 44 (new folder), MOODS 20 (new), Genre Trivia! 18 (the account already held that root folder, adopted), WIP 9 (new, the folder is named `WIP ` with a trailing space in rekordbox and the account folder takes the same name), TOOLBOX 6 (new), Bandcamp Purchases 2 (new), Playlists 2 (the rekordbox root, new). **868 tracks to add to the account, 576 rekordbox rows unmatched and left in rekordbox** (167 with no ISRC, 21 the account has no track for, and about 388 where the ISRC names several provider tracks that all agree and none was chosen, since the file carries no album tag). **92 skipped, all under ARCHIVE**; none was smart, shared-title or already on the account. No removals, no rekordbox-side change, no acquisition job (every new pair is a first sync, additions only). | rehearsed |
| `crate sync pair`, live, plan and both gates | live, run `2026-11-04T23:51:39Z-0964`, 7m53s plan, 4165 calls | **digest `ab30bca7046b28eb`, count 1637, equal to the rehearsal's**, 101 pairs, 92 skipped. The two plan screens differ in one line only: the provider's count of tracks for ISRC FR22F1701790 (Mi Gente) read 9 on the rehearsal and 10 live, inside a reason text that is not in the digest; no item written differs. The gate after the first answer replanned (4069 calls, 8m49s), digest unchanged. Both gates approved as `session`. | live |
| the account write | the same run, third command, 10m32s | **Stopped on the provider-call ceiling at 5000** (set with `--calls 5000`): the replan took 4069 calls and the writes the rest. By then 94 of the 101 account playlists were made, filled and marked in `playlist_pairs.json`, one (WIP Lisa lisa_spring_2026) made but not yet filled. What it did was kept, as the stop message says. The database read `85a86cfb0c94bf82` still. A continue with `--calls 10000` answered `DECISION_STALE` (run `0964` is spent), since the 94 written pairs had changed the plan. | live, partial |
| `crate sync pair`, live, the rest | live, run `2026-11-05T00:25:00Z-11b8`, `--calls 10000` | New plan: **digest `d136cd26e0ff017c`, count 761**, 101 pairs. Read before approving: 7 new pairs (all WIP) whose add and unmatched counts equal the rehearsal's for the same pairs (7+7, 8+7, 26+21, 5+5, 2+6, 16+22, 8+1), one half written pair (WIP Lisa lisa_spring_2026, 14 adds, 21 unmatched, as the rehearsal had it), **86 adds in all and nothing else**: no removal, no rekordbox-side item, nothing new for the other 93 pairs. The difference from the rehearsal digest is the 94 pairs already written, not what is written. Both gates approved as `session`. The gate-sibling-run warning named run `0964`'s earlier answer. Result: `sync.pair: ok`, **101 pairs synced, 7 account playlists made in this run, 0 added and 0 taken off in rekordbox, 86 added and 0 taken off on the account, 0 acquisition jobs queued**; 3027 calls, 7m06s. | live |
| Whole run totals | the two live runs | **101 account playlists made, 868 tracks added, 0 removed, 0 written in rekordbox**, in about 53 minutes from 23:51 to 00:45 UTC and **about 24,300 calls** to the provider across seven commands (4165, 4069, 5000, 2671, 2671, 2671, 3027), none answered with a rate limit. Every command replans the whole account side, so a run with two gates costs three plans. | live |
| Read back, the plan again | `crate --calls 10000 sync pair`, run `2026-11-05T00:44:58Z-b817`, 5m26s, 2495 calls | **digest `46e19bed5b02ec66`, count 668, 101 pairs, 92 skipped**: 576 unmatched rows and 92 skipped lines, **no add, no removal and no order change on either side**, so the account and rekordbox hold the same lists for every pair, as the last sync recorded them. Answered `skip` at the gate (run `94d9` is the decision), nothing written. | live |
| Read back, the pairs document | `history/playlist_pairs.json` on the volume | 101 pairs, all made and marked, 868 account tracks; per folder: GIG READY 44 pairs, 388 account tracks of 664 rekordbox rows; WIP 9 pairs, 111 of 241; MOODS 20; Genre Trivia! 18 (folder reused, `created: false`); TOOLBOX 6; Bandcamp Purchases 2; Playlists 2. **No ARCHIVE folder and no ARCHIVE playlist is in it**, and the 92 skipped lines are all ARCHIVE. | read |
| Why the rehearsal answered skip | judgment | An applied account gate on the copy would have made 101 playlists on the real account, which a copy cannot be isolated from, and the live run would then have found every title held. So the rehearsal read both gates and skipped both. The digest bound to the plan is what the copy proves, and it was equal. | rehearsed |
| config.toml and the library | checked | `~/Library/Application Support/Cratekit/config.toml` unchanged (sha256 `9e545aa4977367916d2a8f4fbd81d309d8afc7b84631751e8035cdf6e4389d89`, modified 2026-10-15). The live database sha256 `85a86cfb0c94bf82` before and after. The 21 runs at a gate and 8 open sessions from earlier work were not touched. | checked |
| macOS battery on the merged head | cited | The v0.6.0 cut ran it clean on the cut commit 40a501d8, which is the head this sitting ran on; main has not moved. | cited |

**A83 (#492) is half met.** Met: the live run landed with its count and duration recorded, the plan reads equal on both sides after it, and nothing under ARCHIVE was made. **OWED, for a later session with desktop control, in this order:**

1. **GIG READY and WIP read in rekordbox.** Open rekordbox in the attended session only (`rekordbox` and `rekordboxAgent` both confirmed gone before and after, no Cratekit job running first, `crate doctor` backup ages under five days). Compare to the account: `GIG READY Phil Sets Classic Soul Intro` (rekordbox 10 rows, account 4, six unmatched and left in rekordbox) and `WIP Lisa lisa sandbox` (rekordbox 47 rows, account 26), then two more of each folder. The account's tracks must appear in rekordbox in the same relative order as on the account, with the unmatched rows between them; the account's root folders read `GIG READY` and `WIP ` (check whether the Tidal app shows the trailing space or trims it, and whether `crate sync pair` still reads the folder as the same one afterwards). The baseline plan to compare against: the read-back run `2026-11-05T00:44:58Z-b817`, digest `46e19bed5b02ec66`, count 668.
2. **One hand change in rekordbox.** In a playlist under GIG READY or WIP, add or remove one track the account carries (a matched row), quit rekordbox, confirm both processes gone, then run `crate --calls 10000 sync pair`. The plan must show that one change as an account-side item for that pair and nothing else. Answer both gates as the session on a rehearsal that matches (a copy rehearsal needs the setup described at the top of this sitting), and read the result in the Tidal app.
3. **One hand change on the account, by Phillip.** In the Tidal app, add one track the library owns to, or remove one track from, a different playlist inside a `GIG READY` or `WIP ` root folder. Then `crate --calls 10000 sync pair` must show it as a rekordbox-side item, and applying it must land it in rekordbox (an owned track), or queue it for acquisition once (a track the library does not own). Read both back.
4. Then close #492 with a comment naming this record and the follow-up's.

Friction found this sitting, for the file-card skill, not filed: (a) every gate costs a full replan of 2,500 to 4,200 provider calls and about 5 to 9 minutes, and a run with two gates plans three times; even the read back plan, with every pair marked and every miss remembered, still made 2,495 calls (the cause was not traced), and the account write shares the same command's call ceiling, so the default 500 and even `--calls 5000` stopped it. (b) A stop on the call ceiling during the account write leaves the run `DECISION_STALE` on continue, so the recovery is a fresh run. (c) About 388 of 576 unmatched rows are ISRC matches the matcher refuses as ambiguous (several provider tracks agree, no album tag); a rule that prefers the track already hearted or the one the playlist's neighbours share would carry more of GIG READY. (d) The rekordbox folder `WIP ` has a trailing space.

### Sitting 54, continued, 2026-11-05: the OWED list, by a session with desktop control

From the same v0.6.0, main at 29a83b87, both backup ages about one day, the session acknowledgment `2026-11-04T23:28:28Z-d87a` still valid. No Cratekit job ran while rekordbox was open; `rekordbox` and `rekordboxAgent` were confirmed gone after the quit and before every verb. The TIDAL desktop app is refused to the session's desktop control by policy and the browser extension was not connected, so **the account side was read and changed through the product's own account client** (`cratekit.modules.outbound.tidal_account.open_account`, the installed copy): `playlist_tracks` to read, `add_to_playlist` for the one hand change. That is the same call the Tidal app's add makes, with the product's provider gate; nothing else on the account was touched.

| Step | Ran | Observed | State |
|---|---|---|---|
| 1. In-app read, rekordbox | rekordbox opened, tree search per playlist, read by `#` order | **GIG READY Phil Sets Classic Soul Intro**: 10 rows, the account's 4 at positions 1, 3, 4 and 8, the six unmatched between them, exactly as `playlist_pairs.json` records. **WIP Lisa lisa sandbox**: 47 rows in the recorded order, the account's 26 among them in the account's order. Two more of each folder, all equal to the record row for row: GIG READY `MAISON 2 / Peak time - for kids!` (10 of 10 on the account), `tech_house_hits - Phil (25 minutes)` (9, 5 on the account), WIP `lisa_downtempo` (10, 5), `lisaphil_transition_duncan_bday` (8, 2). A copy of the live database read before opening (sha256 `85a86cfb0c94bf82`) gave the same order for all six. | read |
| 1. Account read | product client, `playlist_tracks` | All six account playlists, and `WIP Phil feelings wip`, hold exactly the recorded tracks in the recorded order. **The account keeps the folder name `WIP ` with its trailing space**; the folders listing returns `'WIP '` for `ea281c95`, and every later `sync pair` read it as the same folder (no new folder, no new pair). | read |
| 2. Hand change in rekordbox | dragged `05A - 126 - Hyaku (Edit)` (Traumer, a matched row, account 536293808) to the end of `WIP / Phil / feelings wip`, 9 to 10 rows; quit rekordbox | The database moved to `347bd9ca4dc6d365`. | done |
| 2. Rehearsal | copy (`copyrun-492/db`, `.cratekit-copyrun`, config and installation state redirected to scratch, as at the top of this sitting), run `2026-11-05T01:12:05Z-e0f4`, 4m38s, 2497 calls | **digest `a63b36af40c8c464`, count 669**: the baseline's 668 plus one item, `feelings wip`, account, add Hyaku, nothing else. Answered `skip` (an applied account gate on a copy reaches the real account). | rehearsed |
| 2. Live | run `2026-11-05T01:17:14Z-5058`, three commands 5m17s, 4m49s, 5m54s; 2497, 2497 and 2804 calls | digest `a63b36af40c8c464` at both gates, equal to the rehearsal; both approved as `session`. **1 added and 0 taken off on the account, 0 in rekordbox**; database unchanged. Read back: account `feelings wip` 9 tracks, Hyaku last, equal to the record. | live, met |
| 3. Hand change on the account | `add_to_playlist` on `GIG READY Phil Sets Projects New Downtempo Project 110 BPM` (account `e48ad66d`), track 30584278, Island Life by Mark Barrott, which the library owns (content 184774187) | Account playlist 4 to 5 tracks, Island Life last. | done |
| 3. Rehearsal | copy refreshed from the live state, run `2026-11-05T01:34:08Z-7a64`, 5m11s, 2495 calls | **digest `ae2a37ec6c8a40cd`, count 669**: one item, rekordbox side, add Island Life to that pair, nothing else. Both gates applied on the copy (the account side had no item, so nothing reached the account); the copy's playlist read Island Life at row 9; the live database still `347bd9ca4dc6d365`. | rehearsed |
| 3. Live, first try | run `2026-11-05T01:50:16Z-2443` | Both gates read `ae2a37ec6c8a40cd` and were approved, then the account gate's apply **failed `INTERNAL`: `SystemError: <built-in function proc_cmdline> returned a result with an exception set`**. Pioneer's `FwUpdateManagerd` had leaked 356 zombie processes again, and the rekordbox process scan (`core/processes.py`, `psutil.process_iter(["name"])`) met one as it died. The database still read `347bd9ca4dc6d365`: nothing written. The daemon was stopped (`kill 769`), zombies fell to one. | failed, nothing written |
| 3. Live | fresh run `2026-11-05T02:05:49Z-8a25`, 15m36s for the three commands; 2495, 2496 and 2799 calls | digest `ae2a37ec6c8a40cd` at both gates, approved as `session`. **1 added and 0 taken off in rekordbox, 0 on the account.** Database `2e9c67ada8186391`. Read back from a copy: `New Downtempo Project 110 BPM` 9 rows, Island Life last, equal to the record; account 5. | live, met |
| Cleanup | | `copyrun-492` and `.cratekit-copyrun` deleted from the volume; `config.toml` sha256 `9e545aa4977367916d2a8f4fbd81d309` unchanged. The 21 gated runs and 8 open sessions were not touched. | checked |

**A83 (#492) is met**: the live run's count and duration (above), GIG READY and WIP equal on both sides, nothing under ARCHIVE on the account, and both hand changes crossed. The one difference from the brief: the account side was read and changed through the product's account client rather than in the Tidal app, which this session cannot drive. Both hand changes stay in Phillip's playlists (Hyaku at the end of `feelings wip`, Island Life at the end of `New Downtempo Project 110 BPM`); remove them by hand if unwanted, and the next `sync pair` carries the removal.

For the file-card skill: a process the rekordbox scan cannot read turns a gated write into `INTERNAL` after both gates were answered, costing a whole fresh run (three plans, about 15 minutes, 7,800 calls). Each run here cost 2,495 to 2,800 calls per command even with nothing to change, as (a) above says.

## Sitting 55, 2026-11-05, the attended session, A70 (#443): one /crate-sync pass from a cold start

From the installed v0.6.0 (`install.release` reads it as the latest), run by the project's `crate-sync` skill with no step improvised, its visit by the `rekordbox-visit` skill. **Started 02:23:02 UTC, filed on the account at 02:38:23: 15 minutes 21 seconds, and 0 messages from Phillip during the pass** (his one message this session, telling the session to drive unattended, came before it), against sitting 47's 25 messages and about three hours. The acknowledgment `2026-11-04T23:28:28Z-d87a` was still valid, so none was minted. `crate organize --only root` never ran.

| Step | Ran | Observed | State |
|---|---|---|---|
| Preflight | `crate sync land --help`, `crate analyze check --help`, `crate job list --state running`, `crate doctor` | Both verbs answer; no job running; both backup ages 1 day; `rekordbox.closed` ok. | ok |
| The pass | `crate --output json sync land`, run `2026-11-05T02:23:14Z-5d57`, pass run `2026-11-05T02:23:15Z-910b`, 70 provider calls | Hearts and playlists queued 2 intake jobs, both succeeded; 7 missing listed; download job `2026-11-05T02:23:42Z-fc7a` landed 6, refused 1 (`lossy-refused`, item 522418193); tag folder ok; **stopped `PRECONDITION`, `rename-incomplete`**: 4 renamed, 2 not, each because its name was taken by a file already in Downloads. The favorites listing came back short, 304 declared, 294 listed, 10 withheld by the provider. | stopped |
| Why it stopped | read | The two unrenamed downloads (`01A - 118 - 568233691.flac`, `08A - 118 - 568233693.flac`) decode to the same audio, by `ffmpeg -f md5`, as two Yours tracks staged on 2026-10-31 by a pass that never landed (its gate, `2026-10-31T12:22:58Z-8f87`, still open). The missing list asked for them again because staged is not owned. The two new copies were moved to `Downloads_duplicates_2026-11-05` on the volume, nothing deleted; the named copies stayed. | resolved by hand |
| The pass, continued | `crate sync land --pass-run 2026-11-05T02:23:15Z-910b`, the command the refusal printed (A77) | analyze run, rescore (every file already carried a voxlevel, none owed), restamp, name (nothing left to rename), then **stopped at `intake.land.native`**, gate run `2026-11-05T02:29:24Z-dfb5`, pass `2026-11-05T022315Z-910b_synced`, 14 files staged (5 of this pass, 9 of the 2026-10-31 one). Tag guess: 14 of 14 carried a genre before and after, 0 written, 0 left. | gate |
| Landing rehearsal | `crate intake land ... --rehearse` (A49), run `2026-11-05T02:29:38Z-4141` | **digest `bcd859fa7930f91e`**; added 14, active rows 10766 to 10780, integrity ok, area removed, landed rows gridless, refused 0. No hand copy. | rehearsed |
| Landing, live | `crate --run 2026-11-05T02:29:24Z-dfb5 intake land ...`, then `crate run decide ... intake.land.native apply --actor session --continue` | Gate screen: `rehearsal` reads "digest bcd859fa7930f91e, equal to this plan's"; `lands in` `Music/Processed_Tracks/2026/11_04_26 Tidal playlists and Favorites`, every `FolderPath` under it (A52); `files after landing` 14 rows into genre_energy (A51); the gate screen named `--continue` beside the answer (A53). Applied: **14 added, filed 14, 26 filing memberships, 26 hearts placed (13 into All Favorites, the rest into 2026-10 and 2026-11, made), 13 coloured Pink, 12 vox tagged, 1 dyn tagged**, one custom playlist twin `Custom Playlists 2026 / Welcoming vibe`. No `landing-filed-differently` or `landing-not-filed` warning. | live |
| On disk | `ls` | 14 files under that Processed_Tracks folder; Downloads holds no audio. | read |
| Visit pre check | `crate --output json analyze check`, exit 12 | scope `analyze`, batch 14, not analysed 14, dyn 1. | ok |
| Visit, Normal | INBOX / Analyze, 14 tracks, all selected, Analyze Tracks | Read back before OK: Normal, high precision off, BPM / Grid on, Phrase on, KEY on, Vocal off, CUE off. **Wait done, 14 of 14 in 42 s.** | done |
| Visit, Dynamic | the one dyn row selected alone by a click (row 10, My Tag `vox / dyn`, `08B - 97 - What A Difference A Day Made`), the context menu read singular "Analyze Track", rather than the My Tag filter the skill names | Read back: Dynamic, every other field as above. **Wait done, 1 of 1 in 21 s.** Its BPM read 128.88 after the Normal run and 129.20 after, against 97 in the title. | done |
| Quit | rekordbox menu, Quit | `rekordbox` and `rekordboxAgent` gone within 10 s. | checked |
| Check | `crate analyze check`, **exit 0** | 14 analysed, grids 13 constant and 1 variable (the dyn row), keys 8 equal, 3 one step, 3 far. | done |
| Clear | rehearsed on a hand copy (`copyrun-492`, `.cratekit-copyrun`, config redirected), run `2026-11-05T02:33:52Z-cddf`; live run `2026-11-05T02:34:03Z-39f2` | **digest `b5ed051de5b4d707`, count 14, equal**; applied as `session`: 14 rows left INBOX / Analyze, which reads back 0. | live |
| Marks | `crate organize --only marks`, run `2026-11-05T02:36:23Z-c9d8`, digest `8d4697bf673dbb27` | Six passes read. **Marked 6**: this pass's `Welcoming vibe`, and five the 2026-10-31 pass had left unmarked (`lisa_7/16`, `Minimal`, `David Hohlme`, `lisa_7/31/26`, `lisa_9/18_2026`). Left: `Alex Kaminski` (1 track outstanding), `Phil 9-30-26` (2), `New York Fever Vol. 1` (19 missing); the rest already marked. | live |
| Filing | `crate organize --only file`, run `2026-11-05T02:37:36Z-b3cb`, digest `bc2be87311b7c7f0` | 5 moved into the account's existing `2026` folder: `DOWNLOADED David Hohlme`, `Minimal`, `lisa_7/31/26`, `lisa_9/18_2026`, `Welcoming vibe`; read back in that folder. `lisa_7/16` was marked and not in the filing plan. | live |
| Read in rekordbox | a second, read only visit, quit and both processes confirmed gone after | INBOX holds `2026-11-04 Tidal playlists and Favorites` (14) and **`Welcoming vibe 2026-11-04` (6), the date at the end** (A78's rekordbox half). The batch shows artist and genre on all 14 with no missing file mark; one row's Info panel reads album `Twentysomething (Special Edition)` and year 2004, before any Reload Tags (A50). `BY GENRE + ENERGY / Jazz / with vox` and `/ Favorites` hold that row as the gate screen said (A51); the database places all 14 as planned. | read |

**Met by this sitting:** A70 (#443), A77 (#462, continued with the printed `--pass-run`), A74 (#450, `install.extras` ok, no `sync.land.without-vocals` stop, 12 vox tags from real scores, no `vox-mostly-unscored`; the rescore row scored nothing because every file already carried a voxlevel), A53 (#398, the screens name `--continue` and every gate here was answered with it; no acknowledgment was owed, so the acknowledgment half was not exercised), A61 (#425, the one difference the dyn selection noted above), A49 (#384), A50 (#386), A51 (#388), A52 (#390). **Not met:** A78 (#468), the rekordbox half read but the account mirror under an INBOX folder not, since no organize step in a pass makes it and the account has no INBOX folder; A59 (#421), no label sync ran; A60 (#423), the three verbs ran inside `sync land`, not typed alone. The macOS battery these cards owe is cited from the v0.6.0 cut on 40a501d8, as at sitting 54.

**For the file-card skill:** (a) a pass downloads again a track already staged by an earlier pass that never landed, and then stops at the name step on the collision; the missing list should count staged files. (b) The dyn row's 129 BPM against 97 in its title is worth a look by whoever reads the check's key and tempo agreement. The two duplicates in `Downloads_duplicates_2026-11-05` and the rehearsal copies `copyrun-492` and `.cratekit-copyrun` on the volume are Phillip's to delete; a safety check stopped the session removing folders at the volume's top level.

A68 (#439) is met in part by the same pass: the gate's `dyn My Tag` line read 1 of 14 (10 files with no drift reading, no tag), the visit ran Normal on all 14 and Dynamic on the one `dyn` row, and `crate analyze check` read 13 single tempo grids and the one variable grid on the `dyn` row. Owed: whether that row (`What A Difference A Day Made`, a jazz ballad titled 97 that rekordbox reads 129.20) was the right call by ear, which is Phillip's; and the `rows-await-analysis` warning named the one playlist and its count of 14, not two selections.

## Sitting 56, 2026-11-05, the attended session, A73 (#449) and A46 (#370): the Favorites folder newest first

From v0.6.0. Backup ages one day, no job running, rekordbox closed.

| Step | Ran | Observed | State |
|---|---|---|---|
| Rehearsal | `crate favorites order` on the hand copy (`copyrun-492`, `.cratekit-copyrun`, refreshed from the live state after sitting 55), run `2026-11-05T02:43:50Z-aaf2` | **digest `c4d701c06309c598`, count 23, 20 playlists to move.** Order now: All Favorites, 2026-11 (made by sitting 55's landing directly under All Favorites), then 2024-06 up to 2026-10, Undated. Order after: All Favorites, the months 2026-11 down to 2024-06, Undated. Approved on the copy; read back in that order, no membership changed. | rehearsed |
| Live | run `2026-11-05T02:44:03Z-4615`, `crate run decide --actor session --continue ... favorites.order.approve approve` | digest `c4d701c06309c598`, equal; **20 moved**, read back from the database in the order above, no membership changed. | live |
| Second run | `crate favorites order` | `no_op`, `favorites-in-order`, no gate. | checked |
| In rekordbox | opened, Favorites expanded, quit, both processes gone in 10 s | All Favorites (289), 2026-11 (7), 2026-10 (71), 2026-09 (37), 2026-08, 2026-07, 2026-06, 2026-05, 2026-04, 2026-02, 2026-01, 2025-09, 2025-08, 2025-07 and on down, as the verb read back. The new month from a landing sits directly under All Favorites. | read |

**A73 (#449) and A46 (#370) are met.** The macOS battery is cited from the v0.6.0 cut on 40a501d8.

## Sitting 57, 2026-11-05, the attended session, A66 (#435): the custom playlist twins backfill, stopped before its gate

| Step | Ran | Observed | State |
|---|---|---|---|
| Rehearsal | `crate sync twins` on the hand copy, run `2026-11-05T02:45:53Z-014b`, 85 calls | **Refused `PRECONDITION`, `intake-list-unusable`**: "track 5 names no title". Nothing planned, nothing written. | stopped |
| Live plan | `crate sync twins`, live | The same refusal before any gate, source account playlist `2974f8ca-f511-43b8-a881-686f3067a515`, read through the product's account client as `DOWNLOADED 12-24-25`, whose fifth track is Glass Animals' `[Premade Sandwiches]`: a title written wholly in brackets, which the title reader strips to nothing. One track refuses the whole backfill. | stopped |

**A66 (#435) is not met** and now depends on #507 (U213), filed with this finding. Nothing was written by either run.

## Sitting 58, 2026-11-05, the attended session, the account mirror: A63 (#429), A41 (#365), A56 (#414), and the macOS battery

From v0.6.0. Backup ages one day, no job running, rekordbox closed throughout. The mirror writes only the account, so no copy rehearsal applies; each gate was read and answered as `session`.

| Step | Ran | Observed | State |
|---|---|---|---|
| macOS battery | local `main` after `git pull --no-rebase origin main`, merge `0d89bd44` (carries every merge to 2026-11-05 03:00 UTC, U198 and the units these cards owe) | `ruff` clean; **16,251 passed, 1 skipped** in 209.6 s (the mirror was planning at the same time); `scan_repo.py` clean. `config.toml` unchanged. | clean |
| Report | `crate --calls 20000 organize --report --only mirror`, run `2026-11-05T02:47:23Z-3c1d`, 36m18s | **3,972 account requests in 2,177 s, 18,632 provider calls**, no rate limit. 24 folders: the 22 genre buckets, Favorites (create 1), and **INBOX (create the root folder, create 22 playlists)**. Unmatched rows summed over the steps: **2,118**, against about 6,245 before R-1032 and the 1,939 the brief expects as the floor. | read |
| Plan, live | `crate --calls 40000 organize --only mirror`, run `2026-11-05T03:24:05Z-a842`, 35m41s, 18,234 calls | Gate `organize.account.apply`, **digest `7e38a08a7022d8f7`, count 24**. The same shape as the report, but several counts moved between two plans over the same library and account half an hour apart: Dance / Pop 353 adds and 129 unmatched in the report, 254 and 228 here; Electronica / Other 462 and 222, then 456 and 228; NonElectronic 197 and 103, then 191 and 109; INBOX 439 and 104, then 433 and 110. Summed unmatched here **2,240**. The cause was not traced. | gate |
| Between the acts | `crate sync favorites` | Refused `outbound-export-required` (it needs a rekordbox export), so **no write happened between the plan and the apply**; A41's stale-plan half was not exercised. | not run |
| Apply | `crate run decide --actor session --continue ... organize.account.apply apply`, 2m51s | **`mirror plan frozen: rebuilt from the plan frozen on run 2026-11-05T03:24:05Z-a842`, 192 account requests in 70 s, 1,369 provider calls, no `decision-stale`.** Every step `applied`: **4,654 tracks added, 3 removed** (Melodic House 2, Soul 1), 2 playlists created (Jazz, Favorites), the INBOX root folder and its 22 playlists created. | live |
| Refresh | `crate organize --report --only mirror`, run `2026-11-05T04:03:36Z-965b`, 2m30s | **217 account requests in 150 s, 677 provider calls**; `mirror misses remembered: 1797 row(s) ... not asked again`; every folder `nothing to write`, each playlist equal to its rekordbox playlist's account tracks, the unmatched counts as the plan had them. | read |
| INBOX read back | the product's account client, folder `INBOX` (`41efef92`) | **22 playlists, none for Old**, one per live batch, each `INBOX <batch>`: `2026-11-04 Tidal playlists and Favorites` 13, `Welcoming vibe 2026-11-04` 6, `Phil 9-30-26` 160, `Idris precise beats` 95, `New York Fever Vol. 1` 39 and the rest. **`INBOX 2026-10-27 PULS` holds 0 tracks**, its 96 rows each named unmatched because "the row carries no ISRC, in the database or in its file" (the batch landed before U150 recorded each label row's provider track). **rekordbox's `2026-10-08 Labels` batch (36 rows) has no account playlist and no line in the plan**: `rotate.live_batches` (`organize/account_mirror.py`, `_inbox`) did not offer it, and the plan says nothing about why. No Defected batch is in INBOX, so the brief's Defected read could not be made. | read |
| Downloader (A82, #482) | `crate doctor`; `~/.config` | `adapter.contract` names `vendored`. Both `~/.config/cratekit-downloader` (since 2026-10-09) and the old `~/.config/tidal_dl_ng` existed before; the new one is in use (its `settings.json` and `token.json` written at sitting 55's download, which landed 6 tracks through `vendored`); the old one is left, to delete by hand. The login step was not run, since the state directory was already resolved. | met |

**A63 (#429)**: met for the counts and the refresh (matched rows up by the tie releases, unmatched 2,118 to 2,240 against about 6,245 before, the refresh back to 217 account requests with nothing planned). Not run: the hearts check (`crate sync favorites` needs an export) and the release hearted afterwards, which is Phillip's on the account. **A41 (#365)**: the frozen plan applied with no `decision-stale` and 192 account requests, and the refresh named 1,797 remembered misses; the landing between the acts was not made, so the stale case is unproven. **A56 (#414)**: the first half met; the retirement half waits for the next `crate inbox rotate`; the PULS and Labels findings above are for the file-card skill. **A82 (#482)**: met. The battery above covers every card in this session that owes one.


## Sitting 59, 2026-11-05, the attended session on v0.7.0: A84 (#502), A93 (#525), and a sync pair rehearsal held for U216

From the installed v0.7.0, `main` at `d4232416`. Both backup ages one day; the acknowledgment had expired, so `crate session ack --as session` minted one after reading them (valid to 2026-11-06T01:18Z). No job running, rekordbox closed throughout. `credential.catalogue` reads not recorded, so every lookup here went on the account; A87 (#511) and A89 (#517) wait on Phillip registering the app.

| Step | Ran | Observed | State |
|---|---|---|---|
| macOS battery (A84) | `main` at `d4232416`, carrying U203 (`6a401b23`) and U206 (`1effd75a`); `pip install -e '.[dev]'` first | `ruff` clean; **16,611 passed, 1 skipped** in 219 s, no failure in `test_isrc_cache.py`, `test_sync_pair.py` or `test_intake_missing_isrc.py`; `scan_repo.py` clean; `config.toml` unchanged. `board.py cloud`: three lanes held (#506, #507, #526), #529 ready, #341 set aside; no state that disagrees with its last comment. | met |
| Mirror report (A93) | `crate --calls 40000 organize --report --only mirror`, 679 calls, 217 account requests in 79 s | The INBOX step: 22 playlists equal, 110 unmatched, **"3 node(s) in INBOX not mirrored: 2026-10-08 Labels (36 row(s)), not recognised as a batch; Analyze (0 row(s)), the Analyze playlist; Old, the Old folder"**. 22 mirrored and 3 named account for all 25 direct children rekordbox showed at sitting 55. `mirror edits made on the account: no mirrored playlist was changed`. | met |
| Rotate plan (A93) | `crate inbox rotate` to its gate, three runs (`2e23`, `a70b`, `b76c`), each answered `abort` as `session` | Digest `e59100a117e5413e`, count 46. `2026-10-08 Labels` left alone with "no landing record names it, its name does not end _inboxed, and no batch folder under the music folder carries its name", 36 tracks; Analyze and Old with their own reasons; the same reason on 14 hand made playlists inside Old. Nothing moved. | met |
| Sync pair rehearsal | `crate --calls 20000 sync pair` on a hand copy now one level down (`scratch/copyrun` on the volume, `state_dirname = "scratch/copyrun/state"`), run `2026-11-05T13:25:05Z-3507`, 4m00s | **2,074 calls** for the plan (103 ISRC answers from the cache, 276 asked); the gate's new `provider calls` line: "the command that writes is expected to make about 2893, 240 to check the lists and 2653 to write". **digest `f553e0cd4817ded5`, count 862, 120 pairs** (102 live plus 18 new). Items: 378 account adds (the tie rows, each `tied=yes`), 66 account order, 198 account unmatched (Sitting 54 left 576), 105 rekordbox adds, **18 rekordbox `create`**, 4 `acquire`, 1 `ambiguous`, 92 skipped under ARCHIVE. | rehearsed |
| What the 18 are | read | Every `create` is a `DOWNLOADED <genre>` playlist inside the account's `Genre Trivia!` root folder, which U198 adopted (`created: false`) with them already inside: the account's old download copies of genre playlists rekordbox already pairs under their plain names. Applying would duplicate them in rekordbox, add 105 rows to them, and queue Ahmed Spins, Flux Pavilion, Benny Benassi and Hernan Cattaneo for download. U202 was meant for a playlist made after the sync. | finding |
| Gate answers on the copy | `run decide ... sync.pair.rekordbox skip --continue`, then `sync.pair.account skip --continue` | **The rekordbox gate's answer took 0.4 s and made no plan call** (U209); the account gate showed the same digest and forecast; both skipped, `no_op`. | rehearsed |

**Held:** the live `crate sync pair` was not run, so A88 (#514), A91 (#521), A92 (#523) and A86 (#509) now depend on #530 (U216), filed with this finding. The tie count the rehearsal reads, 378 account adds against Sitting 54's 388 tie rows left out, and the forecast line are recorded above for when the live run comes. **A84 (#502) and A93 (#525) are met.**


## Sitting 60, 2026-11-05, the attended session on v0.7.0: the label cards A58 (#418), A81 (#476), A76 (#459), and the drift cut A67 (#438)

From v0.7.0, no job running, rekordbox closed. Every provider call went on the account (no app credentials).

| Step | Ran | Observed | State |
|---|---|---|---|
| One label alone (A58) | `crate label sync --next --label defected`, run `2026-11-05T13:30:59Z-439b`, 60 s | Stopped at **500 calls**, `provider-call-ceiling`, printing `crate --calls 1000 label sync --next --label defected`. | stopped |
| Its continue | the printed command, run `13:32:03Z-f922`, 1m51s | Stopped at **1,000**, printing `--calls 2000`. | stopped |
| Its continue | the printed command, run `13:33:58Z-30ed`, 3m27s | `no_op`: "Defected: nothing new since it was last asked; 11887 release(s) past this run's window". **1,800 calls**: each continue read the listing again from the start. The report named Defected only. | ok |
| Again | the same command, run `13:37:31Z-e221`, 3m30s | The same answer, **1,800 calls again**, where U189's proof expects none. | finding |
| Ceiling (A81) | `crate label playlists Defected`, run `13:41:06Z-15da`, 54 s | **Stopped at exactly 500**, outcome blocked, `provider-call-ceiling`, printing `crate --calls 1000 label playlists Defected`, before its crawl gate (the listing alone is about 1,790 calls). | as briefed |
| Its continue | the printed command, run `13:42:05Z-43f3` | Stopped at 1,000, printing `--calls 2000`: it **started the listing again rather than continuing from the kept reads**. | finding |
| Crawl gate (A76) | `crate --calls 2000 label playlists Defected`, run `13:44:00Z-73b3`, 3m21s | **The listing took 1,790 calls.** Gate: 11,989 releases, at least 23,978 calls, about 40 min; the new `call ceiling` line names `--calls 25900`. | gate |
| Crawl, stopped part way | `run decide ... crawl --continue` with `--calls 3000` | **Stopped by the provider's breaker**: rate limited 6 calls in a row, 9 of 2,823 calls answered rate limited, every call refused until 14:08:16Z. | stopped |
| Resume (A76) | after the cooldown, `crate --calls 2500 label playlists Defected`, run `14:09:05Z-96e1`, 1,790 calls | The crawl screen: **"506 of them read by an earlier run within the last 7 day(s), so reading the other 11483 is at least 22966"**, `kept reads: 506 ... the oldest 21 minute(s) old`. Answered `abort`: the full crawl to the build gate (about 23,000 calls) was not run after the rate limit. | resumed, aborted |
| Drift (A67) | 20 files of the 2026-10-27 batch copied to a local scratch folder; `crate analyze run` settled them in 0.5 s without measuring (they were analysed before U157), so `detect.analyse_file` with the configured cut was called on each copy directly, reading only | Programmed house and techno: John Tejada 0.10, Omar-S 0.10, Pangaea 0.35, **Shed 1.18**, Overmono 0.14 and 0.41, Anunaku and DJ Plead 0.04, Move D 0.21, Pearson Sound 0.14, Roman Flügel 0.07. Live band recordings: **Mocky 0.89, L'Eclair and The Mauskovic Dance Band 1.22, K.O.G and The Zongo Brigade 5.35** (the only `variable`). Edits and remixes of live material: Tony Allen (Motor City Drum Ensemble remix) 0.39, Tabu Ley Rochereau (re-edit) 0.39, Quantic 0.58, Khruangbin and Quantic (Cut a Rug Mix) 0.07, David Walters 0.28, Voilaaa 0.18, Dan Kye 0.14. The kind of each is the session's reading from the artist and the version, not by ear. No older library tracks were added. | measured |

**A67 (#438) is met**: the kinds overlap from 0.89 to 1.22, leaning to Normal keeps the cut above 1.22, so **the cut stays 1.5** and R-1136 is closed on its entry. **A81 (#476)**: the stop at exactly 500 with its printed continue is met; the continue started again rather than from kept reads, which is #533 (U217). **A76 (#459)**: the listing's call count and the resume that asks only the rest are met; the build gate's `release reads` line was not reached. **A58 (#418)**: the one label report and its time are read; the second run's zero calls failed, filed as #533. The macOS battery is sitting 59's on `d4232416`.


## Sitting 61, 2026-11-05, the attended session on v0.7.0: A69 (#440), the Rominimal genre sub, stopped at the rehearsal

| Step | Ran | Observed | State |
|---|---|---|---|
| Hand edit | the library's `coupled/taxonomy.toml`, a copy kept first in the session's scratch folder | `schema_version` 4 to 5, `"Rominimal"` added to Minimal / Deep Tech's `aliases`, and the `[[bucket.genre_sub]]` table (`id = "rominimal"`, `display = "Rominimal"`, `sources = ["Rominimal"]`), as the shipped template has it. `crate doctor`: `taxonomy.active` and `taxonomy.schema` ok. | done, then undone |
| Rehearsal | `crate route resort` on the hand copy (`scratch/copyrun`, refreshed after the edit), run `2026-11-05T14:13:39Z-d3ca`, then its job `2026-11-05T14:13:39Z-725e` driven, 1m42s | The verb queued a job and the job applied with **no gate**. Read from the copy's database: **`BY GENRE + ENERGY / Minimal / Deep Tech / Rominimal` made with the 96 rows tagged Rominimal** beside the bands, as the brief expects. **It also made a folder `INBOX / Minimal / Deep Tech`** (row 112869439, under INBOX 2705010179) with High Energy 119, Low Energy 129, Med Energy 178, Rominimal 96 and with vox 8. The live INBOX holds no genre folder. The job also warned that 448 memberships the declaration does not place stay in the tree, and that `genre_energy` still differs in 452 places. | stopped |
| Undo | the kept copy put back over `coupled/taxonomy.toml` | `diff` empty; doctor reads schema 4 again. Nothing live was written: the live resort was not run. | done |

**A69 (#440) is not met** and depends on #537 (U218), filed with this finding. The edited taxonomy is kept in the session scratch folder as `taxonomy.toml.2026-11-05-with-rominimal` for whoever retakes the card; the shipped template's text is the same edit.


## Sitting 62, 2026-11-05, the attended session on v0.8.0: one sync pair for A86 (#509), A88 (#514), A91 (#521) and A92 (#523), stopped part way by the account's reorder

From v0.8.0 (U212, U213, U215, U216 in it; U217 and the resort fix #537 not). Backup ages one and two days, the acknowledgment of sitting 59 valid, no job running, rekordbox closed throughout. #440 still waits: the U218 that landed is the board sharing card; the resort fix is #537, now titled U219 and open.

| Step | Ran | Observed | State |
|---|---|---|---|
| The playlist (A86) | the product's account client: `create_playlist('GIG READY A86 proof')`, moved into the account's `GIG READY` folder, three tracks the library owns added (`When Doves Cry (Sir Reel Mix)`, `2000 & Universe`, `Island Life`) | Account playlist `28a6a344-bb8f-46b7-a673-2a3292abeba6`, in the folder, the three tracks in that order. | done |
| Rehearsal | `crate --output json --calls 20000 sync pair` on the hand copy (`scratch/copyrun`, refreshed), run `2026-11-05T17:40:21Z-77dd`, 1m02s | **348 calls** (379 ISRC answers from the copy's cache). **digest `679288bae9ddcb85`, count 756, 103 pairs.** U216 holds: the 18 `DOWNLOADED <genre>` playlists of Genre Trivia! are `account-discovery before` items, named on the gate "not made in rekordbox: 18 account playlist(s)". One `create`, `GIG READY / A86 proof`, with its three tracks in the account's order. **378 account adds, every one `tied`** (Sitting 54 left 388 such rows out), 66 order items, **198 unmatched** (576 at Sitting 54). Forecast: "the command that writes is expected to make about 2859, 206 to check the lists and 2653 to write". On the copy: the rekordbox gate's answer in its own command, **0.56 s, no plan call**; the account gate answered `skip`, and the write made the A86 playlist with 3 rows on the copy, nothing on the account, **314 calls**. | rehearsed |
| Live plan | the same live, run `2026-11-05T17:42:49Z-5ddd`, 4m36s | **2,024 calls** (103 from the live cache, 276 ISRC asked); **digest `679288bae9ddcb85`, equal.** | gate |
| Rekordbox gate (A91) | `run decide ... sync.pair.rekordbox apply --continue`, its own command | **0.83 s, no provider call**; the account gate showed the same digest. | answered |
| Account gate and write (A92) | `run decide ... sync.pair.account apply --continue` | **Failed `unavailable-transient`** after **330 calls** (forecast 2,859): a 412 from the provider while putting `GIG READY Phil Sets Classic Soul Intro` (`0372d822`) in order, the first pair written. Its six tie adds had landed; nothing else was written, on the account or in rekordbox. | stopped |
| Continue (A92) | `crate --calls 20000 --run 2026-11-05T17:42:49Z-5ddd sync pair`, twice | No new plan and no gate asked again, **322 and 327 calls**; each refused `outbound-remove-refused`, "read back after a move is not what it held with that track moved to the end". Each made one or two moves before refusing: the playlist now holds all 10 tracks in an order matching neither side (`Island Life, Hyaku, Inner City Blues, Cheer Up, Hopeless, A Break In The Clouds, When Doves Cry, 2000 & Universe, Lujon, Moonsmith`). Stopped there rather than move it further. | stopped |
| Read back | a copy of the live database; `playlist_pairs.json` | No `A86 proof` playlist in rekordbox and no pair recorded for it: the write stops at the first account order item, before the rekordbox side. | read |

**None of the four is met.** A91's per phase counts are recorded above (plan 2,024; rekordbox answer none; account answer 330 before its stop). A92's forecast against the live count could not be read on a finished write, and its continue resumed without a new plan but could not finish. A88's tie count reads 378 on both plans; GIG READY's account count after the apply and the quiet sync wait on a finished write. All four now depend on #543 (U220), filed with this finding. **Left on the account for the next sync:** `GIG READY A86 proof` (three tracks), and Classic Soul Intro out of order; the next finished `sync pair` puts its order back to rekordbox's.


## Sitting 63, 2026-11-05, the attended session on v0.8.0: A66 (#435), the custom playlist twins backfill

U213 (#507) is in v0.8.0. No job running, rekordbox closed before each verb.

| Step | Ran | Observed | State |
|---|---|---|---|
| Rehearsal | `crate sync twins` on the hand copy (`scratch/copyrun`, refreshed after sitting 62), run `2026-11-05T17:52:05Z-5b44`, 267 calls | **digest `db28910589c68d0b`, count 689**: 77 twins to make, 66 into a new `Custom Playlists 2025` folder and 11 into `Custom Playlists 2026`, each named as its account playlist less `DOWNLOADED `; **612 missing tracks, each named** with its reason (most "the library holds no row for it", some "more than one library row carries it, so none was chosen"); 1 already paired. `12-24-25`, the playlist whose bracketed title refused at sitting 57, now plans with 8 tracks and none missing. Approved on the copy: 77 twins, 1,493 tracks, read back. | rehearsed |
| Live | run `2026-11-05T17:53:35Z-e68d` | digest `db28910589c68d0b`, equal; approved as `session`: **77 twins made and paired, 1,493 tracks, 1 new folder** (`Custom Playlists 2025`), session `2026-11-05T17:54:45Z-764d`. | live |
| Second run | `crate sync twins` | `no_op`, "no downloaded custom playlist in a year folder lacks its twin (78 already paired)", 29 calls, no gate. | checked |
| In rekordbox | opened, tree filtered to `12-24-25` | `Custom Playlists 2025 / 12-24-25` shows 8 tracks, as on the account. The Monologue overlay then covered the tree again, so no other twin was read in the app; rekordbox quit from its menu, both processes gone in 10 s. | read in part |

**A66 (#435) is met in part**: the backfill, its missing tracks named, and the NO_OP second run. **Owed:** the twins read against the account in rekordbox beyond one; the pair check (a track added each side, then `crate sync pair`), which waits on #543 (U220) since a live `sync pair` cannot finish its write; and the next landing's twin. **For Phillip:** the warning says the next `crate sync pair` "adds each one it finds in the library and queues each one the library lacks", so the 612 missing tracks of these 77 old downloaded playlists would be queued for download at the first sync pair that finishes.

**Since U221 (#549, 2026-11-05)** those 612 are held, not queued: the 77 twins were paired before U221 and carry no recorded hold, so `crate sync pair` reads each by time and names every track the account listed before the twin was made as on hold, queueing none, until `crate sync release ACCOUNT_ID` (or `--all`) lets a twin's go. Only once the installed copy carries U221; a build without it still queues them.

## Sitting 64, 2026-11-05, the attended session on v0.8.0: A85 (#504), an edit on Tidal to a mirrored genre playlist carried into the library, then undone

Phillip answered in the session: the session makes the edits through the product's account client on tracks it picks and reverses every one afterwards (the TIDAL app is refused to desktop control and the browser extension was not connected). For #474 he chose the alias `Latin Electronic` to `Organic House`, recorded on that card; its apply runs `crate route resort` and waits on #537. No job running, rekordbox closed throughout.

| Step | Ran | Observed | State |
|---|---|---|---|
| First run | `crate --calls 20000 organize --only mirror-edits --only mirror-downloads --only mirror`, run `2026-11-05T19:06:29Z-9dc3`, 1m34s, 677 calls | `mirror-edits` and `mirror-downloads` plan nothing ("no mirrored playlist was changed on the account since the mirror last finished it"), every mirror step `nothing to write`; both gates answered, `no_op`, the snapshots recorded. | done |
| The edits | account client; removals through the client's own playlist object, since the client refuses to take a track off a playlist it did not make | (1) Chris Luno `Night Thoughts` taken off `Organic House Low` and put in `Downtempo Med`; (2) a track taken off `Organic House Low` into nothing: first Nathan Katz `Parallax`, which the rehearsal **held** ("2 library rows match it, so which one changes is not something the account says"), so it was put back (at the end of the playlist) and Kasbï `Conviction` taken off instead; (3) MONKYMAN `Interest` (Downtempo Low) put in `Organic House with vox`. | done |
| Rehearsal | the same command on the hand copy (`scratch/copyrun`), run `2026-11-05T19:17:26Z-6e5e` | **digest `5ce83beadf438256`**: Night Thoughts `move` Organic House / Low to Downtempo / Med, genre Organic House to Downtempo, energy 2 to 4; Conviction `unfile`, leaves Organic House / Low, joins nothing, with the note that rekordbox's Genre column keeps its word; Interest `folder` Downtempo / Low to Organic House / Low, read as the genre Organic House. **Answered `abort` on the copy**: this step retags the audio files, which a hand copy shares with the live library, so the copy proves the digest only. | rehearsed |
| Live | run `2026-11-05T19:19:07Z-153f`, both gates as `session` | digest `5ce83beadf438256`, equal. `mirror-edits: applied: 1 track(s) moved, 1 given another genre, 1 unfiled`; the account step "3 edit(s) made on the account: 3 taken into the library", every mirror folder equal. | live |
| Read back | a copy of the live database and the files | Night Thoughts: row and file genre Downtempo, in `Downtempo / Med` only. Interest: row and file Organic House, in `Organic House / Low`. Conviction: in no BY GENRE + ENERGY playlist, the file's genre cleared, the row's kept as the plan said, and **listed by `crate route unplaced`** (its JSON items; the human output prints only the count line). On the account all three edits stood. | read |
| Second run | `crate organize --report --only mirror-edits --only mirror` | `no_op`, nothing on either side. | met |
| Undo | account client: Night Thoughts back to `Organic House Low`, Conviction back to `Organic House Low`, Interest off `Organic House with vox`; two passes, each rehearsed on a refreshed copy for its digest (`e859a6b33b135be6`, then `9130ef7f8a3c9b9d`) and applied live on an equal digest | The first pass moved Night Thoughts and Conviction back; Interest needed a second account edit, since the first pass's mirror had already moved it into `Organic House Low` on the account, so it was moved there back to `Downtempo Low`. Read back: all three hold their original genre in row and file and their original BY GENRE + ENERGY playlist; a further report plans nothing. Parallax sits at the end of `Organic House Low` on the account rather than second. | undone |

**A85 (#504) is met**, read from the database rather than in the rekordbox window (the Monologue overlay has covered the tree at both earlier visits today). The macOS battery is sitting 59's.


## Sitting 65, 2026-11-05, the attended session on v0.8.0: A90 (#518), edits on Tidal to Favorites and INBOX carried into the library, then undone

Made and reversed through the product's account client, as Phillip answered at sitting 64; the one queued download cancelled before it fetched, by the same answer. Each live pass was rehearsed on a refreshed hand copy for its digest and answered `abort` there (the step writes the files' colour and tags), then applied live on an equal digest as `session`.

| Step | Ran | Observed | State |
|---|---|---|---|
| The edits | account client | Chris Luno `Night Thoughts`, no favourite, put in `All Favorites`; Skeewiff `Man of Constant Sorrow` moved from `Favorites 2026-10` to `Favorites 2026-09`; Paul Cut `The Joy` taken off `All Favorites`; Mark Barrott `Island Life` put in `INBOX Phil 10_8_26` and Geto Boys `Mind Playing Tricks on Me` taken off it; ANOTR `Unlock`, which the library lacks, put in `Deep House Med`. A read straight after two removals still listed them; a second read five seconds later did not. | done |
| Plan | rehearsal digest `50b77dd04082e110`, live run `2026-11-05T19:47:41Z-773d` equal | Night Thoughts `favourite`, joins All Favorites and 2026-11, colour Pink; Skeewiff `favourite` leaves 2026-10, joins 2026-09; The Joy `unfavourite`, leaves All Favorites and 2026-10, with the note that it stays hearted on the account; Island Life `join`; Geto Boys `leave`; Unlock `held`, "the library holds no track matched to it, so it is queued for download". | gate |
| Live | both gates | `mirror-edits: applied: 2 favourited, 1 unfavourited, 1 joined to and 1 taken off an INBOX batch`; `mirror-downloads: queue 1 track(s)`, job `2026-11-05T19:51:57Z-7e71`, **cancelled** with `crate job cancel` before anything ran. | live |
| Read back | a copy of the live database | Night Thoughts in All Favorites and 2026-11, Pink; Skeewiff in 2026-09 only among the months; The Joy in no Favorites folder playlist, still Pink and still in `BY GENRE + ENERGY / Deep House / Favorites` (it stays hearted); Island Life in INBOX / Phil 10_8_26; Geto Boys in no INBOX batch. A further report planned no edit, but `mirror-downloads` would queue Unlock again while it stood on the account. | read |
| Undo | account edits reversed, then passes `2026-11-05T19:56:50Z-7d67` (`6a9ebe8fb1912c41`), `20:03:47Z-89d5` (`ef1d4b1e3e7f074c`), `20:11:44Z-9c9a` (`3f8b60d3aa5eab16`) | The first pass restored Skeewiff, The Joy's All Favorites, and both INBOX edits, and **kept Night Thoughts as a favourite**: "placed in the favourites in rekordbox since: an addition beats a removal, whose time is never known"; its mirror put it back on the account. Taking it off All Favorites again then read as a true `unfavourite` (it was never hearted on the account). The Joy came back to All Favorites but not to `2026-10`; taking it off and back onto the account's 2026-10 carried it in. Final read: every track in its original Favorites and INBOX playlists; **Night Thoughts keeps the Pink colour the favourite gave it**; Unlock off the account; a further organize `no_op` on both steps. | undone |

**A90 (#518) is met except its download half**: the queued track was cancelled by Phillip's choice rather than landed and filed, so "the download" step is owed, and the read was from the database rather than the rekordbox window. Two small findings, no card: an unfavourite leaves the row's Pink colour; and undoing a favourite on the account loses to rekordbox's newer placement until the mirror has written it back, by the stated rule.


## Sitting 66, 2026-11-05, the attended session on v0.8.0: A68 (#439) judged by measure, A63's (#429) hearts check, A41's (#365) stale case, A96's (#539) notes prepared

| Step | Ran | Observed | State |
|---|---|---|---|
| A68, the dyn call | the file's tags and sitting 55's `crate analyze check` | The by-ear check is replaced by the measured read, since the session cannot listen. `What A Difference A Day Made`: Cratekit's `driftlevel` 2.5 (`drift` variable, cut 1.5); rekordbox's Dynamic grid 664 beats from 127.57 to 130.25, a span of 2.68. Both measures say the tempo moves, so the `dyn` mark was the right call. The title's 97 against rekordbox's 129 is a 4:3 reading (97 × 4/3 ≈ 129.3) of a swung ballad, a separate matter and no card. The untagged 13 rows all read one tempo. | met by measure |
| A63, the hearts check | `crate export collection` to a scratch file (14 rows with no file, 153 unmapped paths, both warned), then `crate sync favorites --export` answered `sync` at its gate twice (the job asked again on its own run), run `2026-11-05T20:21:01Z-1e4f`, job `2026-11-05T20:21:15Z-66f9`, 995 calls, 2m06s | 292 favourites swept, hearts added where matched, never removed; **19 unmatched, 8 of them ties refused with the reason ending "so none was chosen"**, for example The Prodigy `Smack My Bitch Up` (ISRC GBBKS9700073, 4 provider tracks agree, the account hearts 2 of them) and Bob Moses `Time of Your Life` (QM6MZ2589604, 3 agree, 2 hearted). | met |
| A41, the stale case | `crate organize --only mirror` to its gate (run `2026-11-05T20:23:49Z-5868`, digest `b7d48d4cf6fe79b6`, nothing to write); then Island Life put in `INBOX Phil 10_8_26` on the account and a `mirror-edits` pass (rehearsed `8025f47525aa2eba`, applied live, 1 joined); then the first run's gate answered `apply` | **`decision-stale`** after **677 calls** and 1m21s: the apply planned in full and found the decided plan changed. Sitting 58's apply with no write between said "mirror plan frozen"; this one did not. A41 expects no stale with a write between, so it is filed as #552 (U222, `idea`), and the join was undone (rehearsed `ef3fb7da01edfb22`, applied, a further report `no_op`). | not met |
| A96, the notes | `release.py plan --since v0.6.0 --tip v0.7.0` and `--notes` | 12 pull requests, U201 to U211 and U214, none without one, proposing minor, v0.6.0 to v0.7.0; the notes open `Cratekit v0.7.0.`, carry no `Merge branch 'main'` line, and end with the `@v0.7.0` upgrade command. Not yet published: replacing a public release's body waits on Phillip's yes. | prepared |

**Met:** A68 (#439) by measure, and A63 (#429) now that its hearts check is read; A63's "a release you heart afterwards does not swap a mirrored track" is not run, since the client can add a heart but not take one off. **Not met:** A41 (#365), on #552.


## Sitting 67, 2026-11-05, the attended session on v0.8.0: A75 (#454), A65 (#433), and two cards met by earlier sittings, A97 (#541) and A78 (#468)

| Step | Ran | Observed | State |
|---|---|---|---|
| A75, first mint | sitting 59, `crate session ack --as session` from the session's shell, no terminal, no `script` | Both ages one day; `backup.acknowledgment: recorded now, by the session-ages rule, valid until 2026-11-06T01:18:06.468653+00:00`. | done |
| A75, again | `crate session ack --as session`, run `2026-11-05T20:37:43Z-733a` | `no_op`, "already on record, not minted again, by the session-ages rule", the same expiry; `crate run show` on it lists no gate. | done |
| A75, doctor | `crate doctor` | Right after `backup.age.files` (2 days) and `backup.age.database` (1 day): "valid until 2026-11-06T01:18:06+00:00, 4h 40m from now, minted by the session-ages rule". | met |
| A65, status | `crate status` | One line: "runs.old: 18 open gates idle for more than 7 days, from 2026-09-23 to 2026-10-27; crate run retire --older-than 7d answers each one abort after a confirm"; the three gates opened on 2026-10-31 listed one by one. | read |
| A65, retire | `crate run retire --older-than 7d`, run `2026-11-05T20:38:10Z-dc21`, digest `9159f964e3a701ba`, answered `apply --continue` as `session` | Each of the 18 (name.apply 9, intake.land 2, sync.all, sync.favorites, tag.retag, export.prune, session.ack, adopt.apply, favorites.backfill) reads `retired`, answered `abort` as `session`; none kept. | done |
| A65, status again | `crate status` | The `runs.old` line is gone; only the three gates of 2026-10-31 remain. | met |
| A97 | sitting 62 | The live plan named "not made in rekordbox: 18 account playlist(s)" and planned none of the Genre Trivia! `DOWNLOADED` playlists as a create. | met |
| A78 | sittings 55 and 58 | In rekordbox, `Welcoming vibe 2026-11-04` sits directly under INBOX with the date at the end beside the date first batch; on the account, the mirror made `INBOX Welcoming vibe 2026-11-04` in the `INBOX` folder. | met |

The macOS battery these cards owe is sitting 59's on `d4232416`.


## Sitting 68, 2026-11-05, the attended session on v0.8.0, no desktop control: the macOS battery, and A57 (#415) owing its DEADCA7 push

A sub session of the attended run with no desktop control, so it took only steps that need no screen. No job running, rekordbox and rekordboxAgent not running before every verb, both backup ages two days and the acknowledgment of sitting 59 valid (none was needed).

| Step | Ran | Observed | State |
|---|---|---|---|
| macOS battery | `main` at `3c0b3722` (carries every merge to U219, so U172, U178, U185, U191, U192 and R-1056 are all in it) | `ruff` clean; **16,841 tests collected, `pytest` exit 0** in 7m49s, run twice (the second only to keep its log; this repository's `addopts` already carries `-q`, so the session's own `-q` silenced the count line, and the count is from `--collect-only`); `scan_repo.py` clean; `config.toml` unchanged after each. | clean |
| A57, what a push needs | `crate doctor`; `/Applications`; `~/Library/Application Support` | `deadca7.push`: "DEADCA7 is not installed here, so nothing else writes the library beside rekordbox". `DEADCA7.app` is in `/Applications`, but its support folder `~/Library/Application Support/deadca7` does not exist, so the app has never run on this account, and its bundle holds only the GUI binary and its `deadcatalog` resource, no command line. | read |

**A57 (#415) owes its screen step**: the DEADCA7 push into a library copy is made in DEADCA7's own window, which this session cannot drive, and every other step of the card (the report naming the DEADCA7 folder once, the full `organize`, `converge`, the byte for byte read back, `deadca7.push` and the two times) reads that push, so none of them could run without it. The battery it owes is above. Next: an attended session with desktop control launches DEADCA7 once, points its push at a disposable copy with library state redirected, and takes the card from the report on.


## Sitting 69, 2026-11-05, the attended session on v0.8.0, no desktop control: A55 (#412), a PULS batch tagged Rominimal by its label

No PULS batch was staged (sitting 46's 96 landed into `Music/2026-10-27 PULS`, and no new Bandcamp purchase was fetched), so the batch is six copies of those landed files in the session's scratch folder, outside the library: the genre taken off five, and the sixth given `Deep Tech` so a file with its own genre is in the sweep. Every copy carries its cover art, no label tag and no ISRC, as the Bandcamp downloads did.

| Step | Ran | Observed | State |
|---|---|---|---|
| Register | `crate label registry set PULS --genre Rominimal` | Refused `PRECONDITION`, `label-unknown`: PULS was never registered (sitting 46 built its label folder by hand). | refused |
| Register | `crate label registry add PULS --genre Rominimal`, run `2026-11-05T21:35:26Z-f578` | **`labels.puls: puls, genre Rominimal, genre Rominimal routes to Minimal / Deep Tech by the taxonomy's keyword rule 'minimal'`.** No `--bandcamp` was set, since the brief names only the genre. | live |
| Sweep | `crate tag folder a55-puls-staging --label PULS`, job `2026-11-05T21:35:37Z-a55f`, 1.5 s | `succeeded`, 6 of 6 settled. The job's summary (`--output json ... --job`): **`tagged` 5, `tagged_by` `label-genre` 5 and every catalogue 0, `label_genres` `{"PULS": 5}`**, `skipped` `has-genre` 1, `off_taxonomy` empty, every catalogue's answers all 0 (none asked, not even `not-asked`), `art_fetch` `present` 6, `art_repair` `ok` 6. Each item's record reads `source: label-genre`, `label: PULS`, `answers: []`. | live |
| Read back | the six files, by mutagen | Five carry `Rominimal`; the sixth still carries `Deep Tech`; one picture each, no label tag written. | read |
| Calls | `crate doctor`'s provider gate count, before and after | 507,057 before and after: **no provider call**, and no catalogue call. | read |

**A55 (#412) is met**, on copies of a landed PULS batch rather than a newly staged one; the sweep reads files only, so where they sit does not change what it does. The battery it owes is sitting 68's. **PULS is now a followed label**, so a `crate label sync` sweep asks the account about it.


## Sitting 70, 2026-11-05, the attended session on v0.8.0, no desktop control: A54 (#409), the Defected 2026 playlist from the sync's releases

| Step | Ran | Observed | State |
|---|---|---|---|
| Plan | `crate --calls 200 label playlists defected --releases`, run `2026-11-05T21:36:52Z-2f9e`, 6 s | **16 calls.** Gate `label.playlists.confirm`, digest `df874830fdb5d2b4`, count 2: folder `Defected`, "use the one already on the account"; `Defected 2026`, "use the one already in the folder, add 12 of 12"; "catalogue: only the 3 release(s) a label sync took were read, and none of the rest of the catalogue"; releases read **Sorley `Phreaky`, Sam Divine `Paradise`, Yours `What's Mine Is YOURS (Live At Abbey Road)`**; "removes: nothing, ever". No listing, no crawl gate. | gate |
| Against the brief | read | The brief expects two releases and 10 tracks; the plan reads three and 12, the third being Sorley `Phreaky` (two tracks), which a later label sync go took. Both Sorley tracks are owned (`Processed_Tracks/2026/10_08_26 Labels`), as are the other ten, so the add was approved as `session`. | decided |
| Apply | `run decide --actor session --continue ... label.playlists.confirm apply` | `ok`, **20 calls for the run**. | live |
| Read back | the product's account client, read only, folder `e8ce5b95` | The year playlist is **`DOWNLOADED Defected 2026`** (`35e42d16`, made 2026-07-08, so the plan's "Defected 2026" is the marked playlist adopted by its built name), **66 tracks, the last 12 the twelve planned**: Phreaky and its Extended Mix, Paradise and its Extended Mix, and the eight Yours tracks. The other year playlists hold 1 (2005, 2008, 2010, 2015, 2018), 2 (2019, 2022, 2024) and 18 (2025), all made 2026-07-08; the plan named only 2026, and the verb never removes. | read |
| Again | the same command, run `2026-11-05T21:37:18Z-fcf7` | **13 calls**; "Defected 2026: use the one already built, add 0 of 12", **"nothing to write: the account already holds every year and track planned"**, digest `2fa1e0d458bbfa67`. It still opened its gate, answered `abort`. | met |

**A54 (#409) is met**: 90 provider calls in all across the plan, the apply, the second run and the read back, against about 24,700 for a full build. The full build was not started. Two small findings, no card: a plan with nothing to write still asks its gate, and the adopted playlist's account name `DOWNLOADED Defected 2026` is shown by its built name only.


## Sitting 71, 2026-11-05, the attended session on v0.8.0, no desktop control: A79 (#470), the genre guess on sitting 47's untagged tracks, and Discogs

| Step | Ran | Observed | State |
|---|---|---|---|
| Report | `crate --calls 500 --output json tag guess "Music/2026-10-27 Tidal playlists and Favorites" --pass 2026-10-27T190706Z-21c7_synced --report`, 7 s | `no_op`, digest `e682ff4957c2c4c4`, **no provider call** (the gate count did not move). 116 files: **87 have a genre, 29 do not**, which are sitting 47's 29. Playlists voting: `Lisa_10_27_26`, `Idris precise beats`, `The LIVING room`. | read |
| How many a guess would tag | the same report | **28 of 29 guessed, 1 with no votes.** Totals `before` 87, `after` 115. | read |
| Bands | the same report | This build names its bands `high`, `medium`, `split`, `low` (the brief's `strong` and `good` are `high` and `medium`): **high 0, medium 1, split 2, low 25.** The medium one is Youandewan `Be Good To Me Poly` (Deep House, 9.05 against 2.0, four library tracks by the artist). Twenty of the low ones carry nothing but the `Idris precise beats` playlist's mix (Deep House 1.09, House / Funky House / Disco 0.85), so each is guessed Deep House on the playlist alone. Where the artist's library tracks vote `Electronica` higher than anything else (Kelly Lee Owens, Shire T, Romare 2.0; O'Flynn 4.0) the guess takes the second word (Deep House, or Dance / Pop for O'Flynn). | read |
| Splits | `tag-guess-split` | Maajo `Maajo` and Voilaaa, Ayuune Sule `Fighting Slowly`: R&B and Rock tied at 0.75 from `The LIVING room`, written as R&B. | read |
| Off taxonomy | `tag-guess-off-taxonomy` | One word: **`Latin Electronic`**, on Quantic `Atlantic Oscillations` (a file with a genre). | read |
| Without a guess | `tag-guess-no-votes` | **Y traxx `Mystery land`** only. | read |
| Discogs | the Discogs API's database search by artist and track, no token (the site's search page refuses a fetch with 403) | **Y-Traxx `Mystery Land`: 43 releases, all Electronic, style Trance on 40** (Techno 7, Progressive Trance 5), the 1998 master Electronic / Trance; the taxonomy has a `Trance` genre, so Discogs would have tagged it. For the two splits: Maajo is Electronic with House and Deep House (`Maajo Remixes`, 2017) or Afrobeat, Disco, Deep House (`Tropic Of Tulli`, 2016); Voilaaa `Voiciii` (2021) is Funk / Soul with Disco and Afrobeat. Neither is R&B by Discogs. | read |

**A79 (#470) is met** by its done line: the counts, the bands and the Discogs findings. Small findings for the record, no card: the two split ties were broken to R&B where Discogs reads house and disco; and twenty low guesses rest on one playlist's mix alone. The battery is sitting 68's. Its "next sync pass's report read for the guess's before and after" waits for the next `crate sync land` pass, which needs a rekordbox visit.


## Sitting 72, 2026-11-05, the attended session on v0.8.0, no desktop control: A60 (#423), tag folder, analyze run and analyze restamp in one command each, and a Ctrl-C

The installed v0.8.0 carries U192. Two staging folders in the session's scratch folder, outside the library, of copies from `Music/2026-10-27 Tidal playlists and Favorites` with the key and tempo head taken off each name (the head is `analyze run`'s skip marker) and the genre taken off: `a60-x` with two tracks, `a60-y` with five. The interrupt was sent by a small wrapper that starts the command in its own process group and sends SIGINT to the group, as a terminal's Ctrl-C does, since a background command in a non interactive shell starts with SIGINT ignored.

| Step | Ran | Observed | State |
|---|---|---|---|
| Tag | `crate tag folder a60-x`, typed once | **`job: 2026-11-05T21:40:59Z-3381, succeeded`, `items: 2 of 2 settled`, no `drive it with` line**; Traxsource and Bandcamp blocked, as every sitting since 32. | met |
| Analyse | `crate analyze run a60-x`, typed once, 1m03s | **`job: 2026-11-05T21:53:27Z-75a0, succeeded`, `items: 2 of 2 settled`**, no `drive it with` line; both renamed to their heads (`01A - 122 - ...`, `01B - 89 - ...`). | met |
| Restamp | `crate analyze restamp a60-x`, typed once, 9 s | **`job: 2026-11-05T21:54:33Z-c879, succeeded`, `items: 2 of 2 settled`**, no `drive it with` line; the `db-metadata-not-written` warning as always. | met |
| Interrupt | `crate analyze run a60-y`, SIGINT to its group after 45 s | **`analyze.run: cancelled (INTERRUPTED)`**, "job 2026-11-05T21:54:46Z-8e37 was cancelled at stage 'items'", **`resume it with: crate analyze run .../a60-y --job 2026-11-05T21:54:46Z-8e37`**, "the job is queued again with 2 of 5 items settled, and the resume does not redo them". On disk three files carried a head, not two. | as briefed |
| Job | `crate job show 2026-11-05T21:54:46Z-8e37` | **queued**; done 2, pending 3. | as briefed |
| Resume | the printed command, typed, 39 s | Analysed the two untouched tracks and did not analyse the two settled ones again, then **failed `PRECONDITION`, `source-missing`**: "Roman Flügel - Parade D'Amour.flac is no longer a file ... every failure is permanent so resuming this job cannot succeed". That track was the one in flight at the signal: on disk as `08A - 123 - Roman Flügel - Parade D'Amour.flac`, its staged report `0002.json` reading `analyzed` with `renamed_to` set, and **no rename intent** in its staging directory. | failed |
| Why | `src/cratekit/analysis/cli.py` `handle_run`, `src/cratekit/analysis/artifacts.py` | `handle_run` records the rename intent, renames, then returns `artifacts.produced`, whose `staged_path` removes the item's staging directory, the intent with it, in the same attempt. An interrupt after that and before the engine flips the row to done leaves a pending row under the old name and nothing that names the new one, so `_finalized_twin` finds nothing. | traced |
| Queue only | `crate tag folder a60-y --queue-only` | **`job: 2026-11-05T21:56:38Z-7a1e, queued`, `drive it with: crate tag folder .../a60-y --job 2026-11-05T21:56:38Z-7a1e`, `items: 0 of 5 settled`**, as before U192. Driven with that command so nothing was left queued: succeeded, 5 of 5. | met |

**A60 (#423) is not met** and depends on **#555 (U223)**, filed with this finding at P1: the printed resume must finish a job whose interrupt landed between a rename and its row's commit. Every other line of the brief read as written. No provider call. The battery is sitting 68's.


## Sitting 73, 2026-11-05, the attended session on v0.8.0, no desktop control: A71 (#445), held for a native label landing

| Step | Ran | Observed | State |
|---|---|---|---|
| What can be marked | the 78 landing session records under the library's `history/sessions` | **None carries a `labels` entry**: no batch has been landed natively with label filing yet. A45 (#369), the card that lands one, is open. | read |
| The nearest pass | `crate label mark Defected --pass 2026-11-05T022315Z-910b_synced` (sitting 55's landing, which carried the ten Defected tracks), run `2026-11-05T21:41:50Z-5d69` | Gate `label.mark.confirm`, digest `94599ea8fbc7f182`: **"pass: 2026-11-05T022315Z-910b_synced, landed on the database native 'inbox' tree"**, "renamed on the account: none", left alone **"Defected 2026: the landed batch filed no track of this year under the label"**, `undone by: crate sync unmark --pass ...`. The item's `name` reads empty, since the account already calls the playlist `DOWNLOADED Defected 2026`. Answered `abort`; no provider call. | read |

**A71 (#445) is held** and now depends on **#369 (A45)** as well: the proof needs a label batch landed natively with `--label`, and a label batch is downloaded only on Phillip's go per label. The gate's reading of a native pass with nothing filed under the label is recorded above for the retake.


## Sitting 74, 2026-11-05, the attended session on v0.9.0, no desktop control: A81 (#476), the continue after the call ceiling resumes the kept listing

A sub session of the attended run with no desktop control. The installed copy is v0.9.0, which carries U217 (#533). No job running, rekordbox and rekordboxAgent not running before every verb, both backup ages two days; no library write, so no acknowledgment was needed. Before the first run the label crawl cache held Defected's release reads (`reads.json`, sitting 60's) and **no kept listing**, so the first run listed from nothing. Every provider call went on the account; the provider gate's count was 507,147 before.

| Step | Ran | Observed | State |
|---|---|---|---|
| Ceiling | `crate label playlists Defected`, run `2026-11-05T23:08:51Z-402c`, 61 s | **Stopped at exactly 500 calls**, `blocked (REFUSED_BY_POLICY)`, `provider-call-ceiling`, printing **`crate --calls 1000 label playlists Defected`**. The message now reads "the remaining items stay queued; what it read and did not keep is read again when it continues" (U217 dropped "what it did is kept"). Spend line: 500 calls, none rate limited. The kept listing was written on the way out: `label_crawl/defected/listing.json`, 1 named, 84 identified, 80 searched and 167 listed answers. | stopped |
| Its continue | the printed command, exactly, run `2026-11-05T23:10:01Z-f817`, 66 s | **Reached the crawl gate with 542 calls**: "listing: the label's listing continued from an earlier run: 332 answer(s) kept, the oldest 2 minute(s) old, and 331 asked of the provider now". Gate `label.playlists.crawl`, digest `13d2f3c783fd3ccf`: **12,093 releases listed**, 506 kept reads from sitting 60 (9 hours old), the other 11,587 at least 23,174 calls, about 39 min; `call ceiling` names `--calls 23900`. Two roster artists, `3534055` and `3930127`, were reported unavailable. | gate |
| Crawl gate | `crate run decide --actor session 2026-11-05T23:10:01Z-f817 label.playlists.crawl abort` | `ok`, recorded by session. **The crawl was not run**: at least 23,174 calls is over this run's 5,000 call bound for one command, and the card proves the listing's stop and continue, which both happened before the gate. | aborted |

**Calls:** 500 then 542, **1,042 for the whole listing**, where sitting 60 on v0.7.0 paid 500, then 1,000, then 1,790 (3,290) to reach the same gate, and a fresh listing alone was 1,790. The continue is cheaper than even one fresh listing because U217 also reads discovery's listings back from the store rather than paging every discovered artist twice. The gate's count moved 507,147 to 508,189.

**A81 (#476) is met**: the build stopped at exactly 500 with outcome blocked and its printed `--calls 1000` continue, and that continue resumed from the kept answers and finished the listing under its raised ceiling. The macOS battery it owes is sitting 68's on `3c0b3722`, which carries U193.


## Sitting 75, 2026-11-05, the attended session on v0.9.0, no desktop control: A58 (#418), the second ask of one label costs no call

Run straight after sitting 74, on the same conditions. Every provider call went on the account; the gate's count was 508,189 before.

| Step | Ran | Observed | State |
|---|---|---|---|
| Defected, first | `crate label sync --next --label defected`, run `2026-11-05T23:11:26Z-c16a`, 12 s | `no_op`: "Defected: nothing new since it was last asked; 11991 release(s) past this run's window", and **"the label's listing was answered from the one kept by an earlier run, 2 minute(s) old, with no listing call to the provider"**, so `label sync` reads the listing `label playlists` kept. The report names Defected only. **12 calls.** | read |
| Defected, again | the same command, run `2026-11-05T23:11:45Z-4879`, 10 s | The same answer, **12 calls**, where sitting 60 paid 1,800. | finding |
| What the 12 are | the same command once more through the installed interpreter with the HTTP client's request log on, run `2026-11-05T23:12:50Z-d08a`, 12 calls | **None is a listing call**: one session read and one user read, then album and its tracks for five releases (`519880827`, `555140902`, `497841184`, `513897942`, `482701430`), the window's confirmed releases whose ownership the sweep checks by reading their tracks against the library. Those reads are not kept, so a label with nothing new pays them on every ask. | traced |
| A label with something new | `crate label sync --next --label puls`, run `23:13:51Z-db54`, 3 calls | Refused `label-sync-unlisted`: **18 provider artists are named exactly `PULS`**, and the entry sitting 69 added names no seed. | refused |
| Another | `crate label sync --next --label voll-schoen`, run `23:14:08Z-e699`, 83 calls | Refused `label-sync-unlisted`: no artist named exactly `Voll Schön`, no seed, and discovery found nothing. | refused |
| Multinotes, first | `crate label sync --next --label multinotes` (asked 2026-10-07, answered not now), run `2026-11-05T23:14:30Z-1b5f`, **31 s** | `ok`: "the label's listing was read from the provider, since none was kept"; **the question: 2 new releases, 7 tracks, about 310 MB**, Murat Uncuoglu `Just Now` (2020, 3 tracks) and `Trees Of Light` (2019, 4 tracks), with its answer command. The report names Multinotes only. **128 calls**, one label's listing and its question. | question |
| Multinotes, again | the same command, run `2026-11-05T23:15:09Z-c4c7`, under 1 s | **The same question, printed from the saved one, with no provider call**: no spend line, and the gate's count stayed 508,439. | met |

**A58 (#418) is met**: the time (31 s), the one label report with its question, the call count (128, one label's listing), and the second run's zero calls, on Multinotes, a followed label below the first in registry order with something new, which is the case U189's "a saved question is printed again with no provider call" names. Defected, with nothing new, saves no question, so each ask lists again; U217 makes that listing free, and what is left is **12 calls a run**, the session and the ownership reads of the five releases in its window. A small finding, recorded here and no card. The battery it owes is sitting 68's.

**Calls for the sitting:** 250 (Defected 36, PULS 3, Voll Schön 83, Multinotes 128); the gate's count ended at 508,439. **Left for Phillip:** the Multinotes question is saved and waits for his answer (`crate label sync --answer ... --label multinotes`), since label releases are always his call. Two followed labels cannot be listed until their entries carry a seed: **PULS** (18 artists share the name) and **Voll Schön** (no artist by the name; each ask costs about 80 calls of discovery for nothing).


## Sitting 76, 2026-11-06, the attended session on v0.11.0, no desktop control: A60 (#423) retaken, the Ctrl-C landing just after a rename, resumed by the printed command

A sub session of the attended run with no desktop control. The installed copy is v0.11.0, which carries U223 (#555). No job running, rekordbox and rekordboxAgent not running before every verb. As at sitting 72, two staging folders in the session's scratch folder, outside the library, of copies from `Music/2026-10-27 Tidal playlists and Favorites` with the key and tempo head taken off each name and the genre tag taken off (through the installed interpreter's tag library): `a60r-x` with two tracks (Pender Street Steppers `Falling`, Kelly Lee Owens `Bird`), `a60r-y` with five (Floating Points `King Bromeliad`, Lone `Blue Moon Tree`, Overmono `So U Kno`, Pearson Sound `Alien Mode`, Roman Flügel `Juke City`), none of them sitting 72's. The interrupt was sent by a small wrapper that starts the command in its own process group with SIGINT at its default, watches the folder every 5 ms, and sends SIGINT to the group **the moment the third file takes its head**, so the signal lands in the window U223 is about: a track renamed, its row not yet done.

| Step | Ran | Observed | State |
|---|---|---|---|
| Tag | `crate tag folder a60r-x`, typed once, 8 s | **`job: 2026-11-06T01:26:48Z-86c2, succeeded`, `items: 2 of 2 settled`**, no `drive it with` line; `Falling` given its genre back, `Bird` none. | met |
| Analyse | `crate analyze run a60r-x`, typed once, 49 s | **`job: 2026-11-06T01:27:00Z-f0ba, succeeded`, `items: 2 of 2 settled`**, no `drive it with` line; both renamed to their heads (`02B - 118 - ...`, `03A - 110 - ...`). | met |
| Restamp | `crate analyze restamp a60r-x`, typed once, 9 s | **`job: 2026-11-06T01:27:55Z-cab4, succeeded`, `items: 2 of 2 settled`**, no `drive it with` line; the `db-metadata-not-written` warning as always. | met |
| Interrupt | `crate analyze run a60r-y`, SIGINT to its group at 68.8 s, as the third head appeared | Heads appeared at 28.1 s, 51.4 s and 68.8 s; **after the signal a fourth, `07A - 136 - Pearson Sound - Alien Mode.flac`, appeared at 87.1 s, and the command exited at 87.5 s** with **`analyze.run: cancelled (INTERRUPTED)`**, "job 2026-11-06T01:28:16Z-76dc was cancelled at stage 'items'", **`resume it with: crate analyze run .../a60r-y --job 2026-11-06T01:28:16Z-76dc`**, "the job is queued again with 3 of 5 items settled, and the resume does not redo them". On disk four files carried a head, not three: the track in flight at the signal finished and was renamed, its row not done. | as briefed |
| Job | `crate job show 2026-11-06T01:28:16Z-76dc` | **queued**; done 3, pending 2. Item 3's staging directory held its staged report `0003.json` (`analyzed`, `renamed_to` the headed name) **and its `rename-intent.json`**, which sitting 72's had lost. | as briefed |
| Resume | the printed command, typed, 22.5 s | **`job: 2026-11-06T01:28:16Z-76dc, succeeded`, `items: 5 of 5 settled`.** Item 3, Pearson Sound, settled **`skipped-prefixed` with `resumed_after_rename: true`**, its file's modification time unchanged; only Roman Flügel `Juke City` was analysed and renamed. No settled track was analysed again, and no `source-missing`. | met |
| Queue only | `crate tag folder a60r-y --queue-only` | **`job: 2026-11-06T01:30:53Z-74fd, queued`, `drive it with: crate tag folder .../a60r-y --job 2026-11-06T01:30:53Z-74fd`, `items: 0 of 5 settled`**, as before U192. Driven with that command so nothing was left queued: succeeded, 5 of 5. | met |
| macOS battery | local `main` at `7ff92818` (v0.11.0, carrying U192, U222 and U223), run while this sitting's verbs ran | `ruff` clean; **16,980 passed, 1 skipped**, 415.6 s; `scan_repo.py` clean. `config.toml` unchanged. | clean |

**A60 (#423) is met**: the three one command answers, the interrupt's lines, the queued job, the printed resume finishing the job with the interrupted track settled from its record and no track analysed twice, the queue only answer, and the battery. The signal landed in the window sitting 72 hit by chance, here on purpose, and U223's fix held. **No provider call**: the gate's count stayed 508,439.


## Sitting 77, 2026-11-06, the attended session on v0.11.0, no desktop control: A41 (#365) and A102 (#568), the account mirror's frozen plan with a mirror-edits pass between its acts

Run straight after sitting 76, on the same conditions. Both backup ages two days, so the session minted the acknowledgment (`crate session ack --as session`, valid to 2026-11-06T13:40Z) before the first database write. Every live database write was rehearsed on a disposable copy refreshed from the live library (`scratch/copyrun` on the volume, library state cloned to `scratch/copyrun/state`, installation state and config redirected into the session's scratch folder, the ISRC cache left live), the copy's gate answered `abort` (the step retags files the copy shares), then planned live and approved as `session` on an equal digest. The copy area was removed at the end.

| Step | Ran | Observed | State |
|---|---|---|---|
| First act | `crate --calls 2000 organize --only mirror`, run `2026-11-06T01:35:08Z-d48b`, 1m29s, 677 calls | Gate `organize.account.apply`, **digest `b7d48d4cf6fe79b6`** (sitting 66's), every folder `nothing to write`, `mirror plan frozen: frozen on run 2026-11-06T01:35:08Z-d48b`. It also read **"1 edit(s) made on the account: 1 taken into the library by the rekordbox area's mirror-edits step"**: an edit this session did not make. | gate |
| What that edit was | `crate organize --report --only mirror-edits` (536 calls), then the copy's plan (536) | **Kabi (AR) `Rainbow` (content `204810807`) put in `Progressive House Med` on the account**, read as a move from `Progressive House / Low`, genre Progressive House, energy 3 to 4. It was made on the account between sitting 66 (20:25Z, which read no edit) and this sitting, by no recorded session, so it is taken to be Phillip's own edit in the app. | read |
| The staged edit | the product's account client | **Mark Barrott `Island Life` (provider track `30584278`) added to `INBOX Phil 10_8_26`** (`d2dfc5d0`, in INBOX `41efef92`), 6 tracks to 7, at 01:42:58Z: sitting 66's row, an INBOX batch membership and nothing else. | done |
| Between the acts | copy rehearsal run `2026-11-06T01:43:06Z-1dfe`, digest **`44a3168500a69fdd`**; live `crate --calls 1500 organize --only mirror-edits`, run `2026-11-06T01:44:21Z-59fe`, digest **`44a3168500a69fdd`**, equal; approved as `session` | **`mirror-edits: applied: 1 track(s) moved, ... 1 joined to and 0 taken off an INBOX batch`**: Kabi moved Low to Med in the library, Island Life joined `INBOX / Phil 10_8_26`. 536 calls each for the plan and the continue. The session chose to take Kabi's edit with its own rather than wait: the step cannot take one edit without the other, the edit is what the product exists to carry, and Phillip's next sync pass would take it the same way. It is not undone, since it is not this session's. | live |
| Second act | `crate --calls 2000 run decide --actor session --continue 2026-11-06T01:35:08Z-d48b organize.account.apply apply`, 1m21s, **677 calls** | **`organize: no_op`, no `decision-stale`.** Its facts: **"mirror plan: 217 account request(s) in 80.47 s to read the account and rebuild 24 folder(s); mirror plan frozen: rebuilt from the plan frozen on run 2026-11-06T01:35:08Z-d48b"**, and "2 edit(s) made on the account: 2 taken into the library by the rekordbox area's mirror-edits step"; every one of the 24 folders `nothing to write`. Sitting 66's same sequence on v0.8.0 refused `decision-stale` after a full plan. | met |
| Read back | the account client | `INBOX Phil 10_8_26` still holds Island Life (7 tracks): the edit's track was **neither taken off the account nor put back**. Kabi `Rainbow` (`421913435`) is in both `Progressive House Low` and `Med` on the account. | read |
| Refresh | `crate --calls 2000 organize --report --only mirror`, run `2026-11-06T01:48:22Z-7f17`, 677 calls | **`mirror misses remembered: 1797 row(s) the mirror could not match before were not asked again`**; 217 account requests in 76.87 s; every folder equal but **Progressive House: "remove 1"**, Kabi off `Progressive House Low` on the account, the library change the frozen apply left for the next run, as U222's answer (a) states. | read |
| Undo | account client: Island Life taken off `INBOX Phil 10_8_26` (7 to 6, read back 8 s later); copy refreshed, rehearsal run `2026-11-06T01:51:10Z-092f`, digest **`ef3fb7da01edfb22`** (sitting 66's undo digest); live run `2026-11-06T01:52:16Z-2edb`, equal, approved as `session` | `mirror-edits: applied: ... 0 joined to and 1 taken off an INBOX batch`. | undone |
| Final read | `crate --calls 2500 organize --report --only mirror-edits --only mirror`, run `2026-11-06T01:54:34Z-14f5`, 677 calls | `mirror-edits`: "no mirrored playlist was changed on the account since the mirror last finished it"; mirror: every folder equal, INBOX's 22 playlists equal their rekordbox playlists, and the one line **Progressive House "remove 1"** (Kabi, above). | read |
| macOS battery | sitting 76's, on `7ff92818` | 16,980 passed, 1 skipped; and `tests/test_organize_mirror_frozen_u222.py` alone, **15 passed** on the Mac. | clean |

**A41 (#365) is met**: with a library write between the acts, the apply landed with no `decision-stale`, rebuilt from the plan frozen on the gate's run with 217 account requests (the listing's range, as at sittings 58 and 66), and the refresh named its 1,797 remembered misses. **A102 (#568) is met by the same run**: its first act, its INBOX `mirror-edits` pass rehearsed and applied, and its second act quoting the frozen plan fact, with the edit's track neither taken off the account nor put back; no stale refusal was met, so there are no movers to quote; and the U222 test file passes on the Mac.

**Changed and left:** Island Life's join was undone on both sides. **Kabi (AR) `Rainbow` now sits in `Progressive House / Med` in the library (energy 4) rather than Low**, taken from the account edit found waiting; the account still lists it in Low as well until the next mirror apply takes it off there. Undo it, if it was not meant, by taking it off `Progressive House Med` on the account and running a `mirror-edits` pass.

**Calls:** live 5,456 on the account (the gate's count 508,439 to 513,895): the two acts, the refresh and the final read 677 each (2,708), two `mirror-edits` passes of a plan and a continue at 536 each (2,144), the edit report 536, and 68 for the account client's reads and writes. Three copy plans on the redirected gate, 536 each, 1,608. No single command came near 5,000.


## Sitting 78, 2026-11-06, the attended session on v0.11.1, no desktop control: A103 (#571), A100 (#562), A98 (#545) and A56 (#414)

A sub session of the attended run with no desktop control. The installed copy is v0.11.1 (`crate --version`), local `main` at `049c973c`, level with `origin/main`. No Cratekit job running and rekordbox and rekordboxAgent not running before every verb; no library write, so no acknowledgment was minted. The provider gate's count was 513,895 before. The two measurements ran the briefs' scripts exactly, through the checkout's venv, with the answer's URL added to the printed line; the session identifier the URLs carry is left out here.

**A103 (#571), three reads of identifiers that name nothing**, through the stored session and its gate, 7 calls with the login:

| Read | Status | Content type | Body | Client raised |
|---|---|---|---|---|
| `session.album("1")` | 404 | `application/json` | JSON, `{"status":404,"subStatus":2001,"userMessage":"Album [1] not found"}` | `ObjectNotFound`, "Album with id 1 not found" |
| `session.track("1")` | 404 | `application/json` | JSON, `{"status":404,"subStatus":2001,"userMessage":"Track [1] not found"}` | `ObjectNotFound`, "Track with id 1 not found" |
| `session.artist("1")` | 404 | `application/json` | JSON, `{"status":404,"subStatus":2001,"userMessage":"Artist [1] not found"}` | `ObjectNotFound`, "Artist with id 1 not found" |

**`simplejson` installed: False.** Every 404 is JSON, so R-1313's page case is a defence, not the common path, and R-1336 and R-1338 have no producer: noted on all three ledger entries, no card.

**A100 (#562), an invalid token at login and at refresh**, from a throwaway `tidalapi.Session` touching no stored session, keychain entry or library, 2 calls outside the gate:

| Call | Status | Content type | Body | Client raised |
|---|---|---|---|---|
| login, `load_oauth_session("Bearer", "not-a-token", ...)`, `GET /v1/sessions` | 401 | `application/json` | JSON, `{"status":401,"subStatus":11002,"userMessage":"Token has invalid payload"}` | `HTTPError`, "401 Client Error: Unauthorized" |
| refresh, `token_refresh("not-a-refresh-token")`, `POST auth.tidal.com/v1/oauth2/token` | 400 | `application/json` | JSON with `error`, `{"error":"invalid_grant","error_description":"Token has invalid payload","status":400,"sub_status":1005}` | `AuthenticationError`, "invalid_grant: Token has invalid payload" |

The login answer is JSON, so R-1305's page case is a defence, noted on its entry. The refresh answer is JSON naming `error`, the case R-1315 already reads right, so R-1315 earns no card; noted on its entry.

**A98 (#545), Defected's label sync stopped at the ceiling, continued, and asked again:**

| Step | Ran | Observed | State |
|---|---|---|---|
| Before | `label_crawl/defected/listing.json` (sitting 74's kept listing, 5 hours old) moved out of the cache into the session's scratch folder; `reads.json` left | no kept listing | ready |
| Ceiling | `crate label sync --next --label defected`, run `2026-11-06T03:34:27Z-0ee5`, 61 s | **`blocked (REFUSED_BY_POLICY)`, `provider-call-ceiling` at 500 calls**, printing `crate --calls 1000 label sync --next --label defected`; spend line **500 calls**, none rate limited. A new `listing.json` was kept on the way out. | stopped |
| Continue | the printed command, exactly, run `2026-11-06T03:35:31Z-b1c7`, 73 s | `no_op`, "Defected: nothing new since it was last asked; 11991 release(s) past this run's window"; **listing line "the label's listing continued from an earlier run: 334 answer(s) kept, the oldest 2 minute(s) old, and 329 asked of the provider now"**; spend line **550 calls**. Artists `3534055` and `3930127` unavailable, as at sitting 74. | met |
| Second ask | the same command, run `2026-11-06T03:36:48Z-ffe4`, 10 s, within two minutes | `no_op`, the same answer; **listing line "the label's listing was answered from the one kept by an earlier run, 2 minute(s) old, with no listing call to the provider"**; spend line **12 calls**, the session and the window's ownership reads sitting 75 traced. No saved question existed to answer `not-now`: a label with nothing new saves none. | met |

The two runs add to **1,050 calls**, against 1,790 for one fresh listing at sitting 60, and the second ask made no listing call.

**A56 (#414), the INBOX mirror on the live account, first half:**

| Step | Ran | Observed | State |
|---|---|---|---|
| Report | `crate --calls 2000 organize --report --only mirror`, run `2026-11-06T03:37:17Z-3051`, 85 s, 677 calls | `no_op`. **INBOX: "nothing to write: 22 playlist(s) already equal their rekordbox playlists' account tracks, 110 row(s) unmatched, 3 left as they are; 3 node(s) in INBOX not mirrored: 2026-10-08 Labels (36 row(s)), not recognised as a batch; Analyze (0 row(s)), the Analyze playlist; Old, the Old folder"**. Every other folder equal but Progressive House, "remove 1". **No `mirror rows answered by their landing` fact.** | read |
| Apply | `crate --calls 2000 organize --only mirror`, run `2026-11-06T03:39:38Z-0525`, 677 calls; approved as `session`, `run decide --continue`, 685 calls | Gate `organize.account.apply`, digest `8deaa5df5a61431e`, one write: **1 track off `Progressive House Low`, Kabi (AR) `Rainbow` (`421913435`)**, the change sitting 77 left for the next mirror apply. Applied from the frozen plan: `ok`, Progressive House "applied", every other folder nothing to write. | live |
| Read back | the installed copy's account client, read only | The account's root folder `INBOX` (`41efef92`) holds **22 playlists and no subfolder**, `INBOX <batch>` for each of the 22 live batches `crate inbox rotate` names in rekordbox's INBOX, from `Phil 9-30-26` to `Welcoming vibe 2026-11-04`; **none for any of Old's 18 playlists**, none for `2026-10-08 Labels` or Analyze. Kabi is off `Progressive House Low` (63 tracks) and in `Med` (114). | met |
| The Defected batch | the 80 landing session records under `history/sessions` | **None of the 19 native landing records carries `provider_tracks`**, the key U150's landing match reads, so no row could be matched by its landing and the plan has no fact to name. No label batch has been landed natively with `--label`: that is A45 (#369), open, the same hold as A71 at sitting 73. The ten Defected tracks of sitting 55 landed in an ordinary batch. | held |
| Retirement | `crate inbox rotate`, run `2026-11-06T03:42:42Z-34b6`, answered `abort` | Gate `inbox.rotate.approve`, digest `e59100a117e5413e`, as of 2026-11-05: **every batch `keep`**. The oldest live batch is `Phil 9-30-26`, landed 2026-10-08, 28 days; a batch moves after more than 30, so it is first due on **2026-11-08**. | waiting |

**macOS battery**, on `049c973c` (v0.11.1, carrying U217), run while A56's verbs ran: `ruff` clean; **17,079 passed, 1 skipped**; `scan_repo.py` clean; and **`tests/test_label_kept_listing.py` alone, 38 passed** on the Mac. `config.toml` unchanged, sha256 `9e545aa4...`.

**A103 (#571) is met** and **A100 (#562) is met**: their outputs above and the ledger notes on R-1305, R-1313, R-1315, R-1336 and R-1338. **A98 (#545) is met**: the stop at 500, the continue's listing line, 1,050 calls across the two, the second ask's zero listing calls, and the battery below. **A56 (#414) stays open**: the report, the apply and the read back are recorded, with one INBOX playlist per live batch and none for Old; its Defected batch proof now depends on **#369 (A45)**, and its retirement half waits on the next rotate, due 2026-11-08 at the earliest.

**Calls:** 3,125 through the gate (513,895 to 517,020): A103 7, A98 1,062, A56 2,056 (677, 677 and 685 for the three organize runs, 17 for the account client's reads), the rotate plan none; and A100's 2 on a throwaway client outside the gate. No single command came near 5,000.

## Sitting 79, 2026-11-06, the attended session on v0.11.1, with desktop control: A80 (#474), Latin Electronic answered as an alias of Organic House

From the installed v0.11.1, which carries U194 and U219. No Cratekit job running and `rekordbox` and `rekordboxAgent` gone before every verb; both backup ages two days, the acknowledgment of sitting 77 valid. Every live write was rehearsed on a disposable copy (the database copied to `scratch/copyrun/db` on the volume, the library state cloned to `scratch/copyrun/state` without its snapshots, installation state and config redirected into the session's scratch folder, the ISRC cache left live), refreshed before each step, and then planned live and approved as `session` on an equal digest. Phillip's answer is the one recorded on the card: an alias.

| Step | Ran | Observed | State |
|---|---|---|---|
| Alias, rehearsal | `crate taxonomy alias "Latin Electronic" "Organic House"` on the copy, run `2026-11-06T13:28:49Z-8304` | Gate `taxonomy.alias.apply`, **digest `b15249ae87cfc950`, count 4**: one copy edit (`tag_alias`, bucket `organic_house`, word `latin electronic`, add) and three files to retag from `Latin Electronic` to `Organic House`: Quantic `Atlantic Oscillations`, Oraculu `Oraculu (Toribio Remix)`, Dj Babatr `Sunshine Tribe`. Answered `abort` on the copy, since the retag writes audio files the copy shares with the live library. | rehearsed |
| Alias, live | run `2026-11-06T13:29:11Z-40af` | Digest `b15249ae87cfc950`, equal; approved as `session`. `taxonomy-alias-saved`: the copy gained `tag_aliases = ["latin electronic"]` under Organic House and nothing else (a `diff` against the kept copy shows those three lines only), the copy as it was kept beside it as `taxonomy.toml.2026-11-06T082957.bak`; `taxonomy-alias-retagged`: 3 files retagged and read back. | live |
| Tag rows, rehearsal | `crate tag rows` on the refreshed copy, run `2026-11-06T13:30:06Z-f41b` | **digest `c25bb46834652876`, count 4**: 3 writes, row `Latin Electronic` to file `Organic House` for the three tracks, and one row left as `file-too-coarse`; 9,937 agree, 672 blank files, 153 unmapped paths, 14 with no path. Applied on the copy, 3 written and read back. | rehearsed |
| Tag rows, live | run `2026-11-06T13:30:43Z-0d70` | Digest equal; approved as `session`: **3 rows now carry Organic House**, read back, undo session `2026-11-06T13:31:13Z-1759`. | live |
| Resort, rehearsal | `crate route resort` on the refreshed copy, run `2026-11-06T13:31:30Z-01d3`, then its job | Gate `route.resort.apply`, **digest `93a94c01c78a5307`, 1,061 adds**, all into `genre_energy`, and the line **"left alone: INBOX (inbox) ... the taxonomy derives nothing for it"**. The adds are mostly a backlog the alias did not cause: 689 into `with vox` playlists, the rest into energy bands across the buckets; the three tracks into Organic House / High (Quantic, Sunshine Tribe) and Organic House / Med (Oraculu). Applied on the copy; **the copy's INBOX read the same three levels deep before and after, no genre folder in it**. The job warned 450 memberships the declaration does not place stay (adds only), and `resort-again`: 35 favourites came due from its own writes. A second rehearsal plan read **digest `aede29c2da37203f`, 35 adds**, every one into a `Favorites` playlist under a bucket, answered `abort`. | rehearsed |
| Resort, live | run `2026-11-06T13:33:48Z-5b7c`, job `2026-11-06T13:34:27Z-3764`; then run `2026-11-06T13:35:19Z-91f9`, job `2026-11-06T13:35:57Z-7534` | First plan digest `93a94c01c78a5307`, **its item list equal line for line to the rehearsal's**, approved as `session`, job succeeded with the same two warnings. Second plan digest `aede29c2da37203f`, equal, approved, job succeeded. A third plan (`13:36:46Z-cc94`) read **0 adds** and still opened its gate; answered `abort`. | live |
| INBOX untouched, live | a copy of the live database read after the jobs | INBOX's children equal to the pre resort read, no genre folder. BY GENRE + ENERGY / Organic House: Low, Med, High, Candy, Unsorted, with vox, Favorites. | met |
| In rekordbox | opened, tree to `BY GENRE + ENERGY / Organic House`, the list searched per track, quit from its menu; both processes gone in 4 s | **`High`: Quantic `09B - 122 - Atlantic Oscillations` and Dj Babatr `09A - 140 - Sunshine Tribe`; `Med`: Oraculu `03A - 117 - Oraculu (Toribio Remix)`**, its Genre column reading Organic House. rekordbox counts the three playlists 362, 403 and 329, where the database rows number 368, 549 and 330; the difference was there before this resort (the copy read 547 in Med before it ran) and was not traced. | read |
| macOS battery | cited | Sitting 78's on `049c973c`, v0.11.1, the installed copy, which carries U194 and U219: `ruff` clean, 17,079 passed, 1 skipped, `scan_repo.py` clean. | cited |

**A80 (#474) is met**: the alias applied with its one copy edit and its kept copy, the file and the row of each of the three tracks read Organic House, and each track reads in Organic House in rekordbox. The resort also filed the 1,061 adds that had waited since the last resort and the 35 favourites they made due; it never removes, so nothing left any playlist.

## Sitting 80, 2026-11-06, the attended session on v0.11.1, with desktop control: A69 (#440), the Rominimal genre sub, resorted with INBOX left alone

Straight after sitting 79, on its conditions and its copy procedure. The acknowledgment of sitting 77 expired at 13:40Z partway through the rehearsal; both backup ages read two days, so the session minted a new one (`crate session ack --as session`, valid to 2026-11-07T01:41Z).

| Step | Ran | Observed | State |
|---|---|---|---|
| Hand edit | the library's `coupled/taxonomy.toml`, kept first as `taxonomy.toml.2026-11-06-before-rominimal.bak` beside it | `schema_version` 4 to 5, `"Rominimal"` added to Minimal / Deep Tech's `aliases`, and the `[[bucket.genre_sub]]` table (`id = "rominimal"`, `display = "Rominimal"`, `sources = ["Rominimal"]`) after that bucket, as the shipped template has it; `diff` shows those lines only, on top of sitting 79's alias. `crate doctor`: `taxonomy.active` ok, **`taxonomy.schema` ok, schema 5**. | done |
| Rehearsal, first try | `crate route resort` on the refreshed copy, run `2026-11-06T13:39:42Z-368a` | digest `e27b72f5e938d453`, 96 adds; the job **failed `backup-acknowledgment-missing`** on the one item, the acknowledgment having expired seconds before; nothing written. | failed, nothing written |
| Rehearsal | the copy refreshed after the new acknowledgment, run `2026-11-06T13:41:15Z-079f`, job `2026-11-06T13:41:55Z-a9f4` | Gate `route.resort.apply`, **digest `e27b72f5e938d453`, 96 adds, every one into `Minimal / Deep Tech / Rominimal`**, and **"left alone: INBOX (inbox), which holds what the verbs that write it put there and not anything a tag decides"**. Applied: the copy's Minimal / Deep Tech reads Low Energy 141, Med Energy 236, High Energy 129, Candy, Unsorted, with vox, Favorites and **Rominimal 96**; all 96 are rows of `Music/2026-10-27 PULS` with the genre Rominimal, and **each is also in exactly one band** (Low 39, Med 41, High 16). **INBOX read three levels deep before and after: equal, no genre folder.** | rehearsed |
| Live | run `2026-11-06T13:42:51Z-9a7c`, as the brief gives it: `crate run decide RUN route.resort.apply apply --actor session`, then `crate --run RUN route resort` (job `2026-11-06T13:43:33Z-5160`) and its printed drive | Digest `e27b72f5e938d453`, **its items equal line for line to the rehearsal's**. Job succeeded; warnings `tree-not-derived` (INBOX left alone, as quoted above) and `membership-left-behind` (the same 450 as at sitting 79). A copy of the live database read after: Rominimal 96, the same band split, INBOX equal to before. | live |
| In rekordbox | opened, `BY GENRE + ENERGY / Minimal / Deep Tech` expanded, quit from its menu, both processes gone in 8 s | **Rominimal (96) beside Low Energy 141, Med Energy 186, High Energy 127, Candy 21, Unsorted 0, with vox 11, Favorites 18**; the list opens with Bernar `Black Woman Experience`, Alineat `San Chi`, Surrender Dis `Brain Dead`, all added 10/27/26. Bernar's track is in High Energy (#111) and not in Low or Med. rekordbox counts Med Energy 186 where the database holds 236 rows, the same kind of gap sitting 79 found in Organic House. | read |
| macOS battery | cited | Sitting 78's on `049c973c`, v0.11.1, which carries U155 and U219. | cited |

**A69 (#440) is met**: 96 filed into the genre sub, none in the wrong place, each still in its band; the gate answered `apply` as `session` on a digest equal to the rehearsal's; INBOX gained nothing, on the copy and live, and the gate names it as left alone.

## Sitting 81, 2026-11-06, the attended session on v0.11.1, with desktop control: A59 (#421) and A71 (#445) on a Multinotes label go, A45 (#369) waiting on a Bandcamp session

From v0.11.1, which carries U190 and R-1056. No Cratekit job running and `rekordbox` and `rekordboxAgent` gone before every verb; both backup ages two days, the acknowledgment minted at sitting 80.

**A45 (#369) waits on Phillip.** Its batch is a small Bandcamp label purchase landed with `--label`. No Bandcamp purchase is staged (the 36 folders under `Bandcamp` are the PULS releases sitting 46 landed), and `crate acquire bandcamp`, run `2026-11-06T13:46:47Z-f3c6`, refused `UPSTREAM_AUTH`: "no Bandcamp session is recorded, so the account's purchases could not be read". A session is recorded only from the browser's own `Cookie` header, a credential this session does not handle. Owed: Phillip records it with `crate login bandcamp-session --from-file PATH` (and buys a small label release if none waits), then a session runs `crate acquire bandcamp-fetch --seller NAME`, rehearses `crate intake land FOLDER --label NAME --rehearse`, lands it, and reads the label folder in rekordbox.

**Why Multinotes, the session's call.** A59 needs a label answered with something new. Of the followed labels, Multinotes held the one saved question with something new (sitting 75: two releases, seven tracks, about 310 MB); Defected has nothing new, and PULS and Voll Schön cannot be listed. Following a label is the standing wish for its releases, the batch is small and the files can be deleted, and the run Phillip set asks for this go, so the session answered `all` rather than wait. At 2026-10-07 Phillip had answered an earlier Multinotes question "not now"; if these two releases are unwanted, deleting the seven rows and files undoes it.

| Step | Ran | Observed | State |
|---|---|---|---|
| The answer | `crate label sync --next --label multinotes`, then `crate label sync --answer all --label multinotes` | The saved question: Murat Uncuoglu `Just Now` (2020, 3 tracks) and `Trees Of Light` (2019, 4 tracks); "2 of 2 release(s) taken and recorded accepted". | done |
| The go's gate | `crate label sync --go`, run `2026-11-06T13:47:42Z-bdcc` | Gate `label.sync.confirm`, digest `fd87e43e2afd865d`, count 2: 1 label, 2 releases, 7 tracks, 310 MB, about 3 min, nothing else answered since the last go. Answered `crate run decide RUN label.sync.confirm apply --actor session`. | answered |
| **The one command** | `crate --run 2026-11-06T13:47:42Z-bdcc label sync --go`, 6m21s, **50 provider calls** | Downloaded (job `2026-11-06T13:48:06Z-67ea`, 7 of 7), then printed and ran each step itself: `tag folder` (job `785f`), `tag guess` (7 of 7 carried a genre already), `analyze run` (job `fb0c`), `analyze vocals --unscored` (none owed), `analyze restamp` (job `e1db`), `name apply` (7 renamed, 0 collides), and `intake land ... --manifest ... --pass 2026-11-06T134742Z-bdcc`, ending **`pending (PENDING_HUMAN)` at `intake.land.native` under run `2026-11-06T13:54:11Z-8fce`**, naming the decide, the apply, the rekordbox visit and `crate inbox analyzed`. **`label.sync.go.tag`, `.guess`, `.analyze`, `.rescore`, `.restamp` and `.name` all read ok**, `.land` a note naming the wait. | met |
| The count | | **One command typed from the go's gate to the landing's gate** (beside the decide), against five commands plus job drives at the sitting of 2026-10-31. | met |
| Landing, rehearsal | `crate intake land ... --manifest ... --pass ... --rehearse`, run `2026-11-06T13:54:45Z-c8e4` | **digest `aa9dfb01ac794d83`**, count 7: added 7, active rows 10,780 to 10,787, integrity ok, area removed, landed rows gridless, refused 0; three into `Multinotes 2020`, four into `Multinotes 2019`; all into Melodic House bands (six High, one Med); two marked dyn (`Snedmea` drift 22.1, `Trees Of Light`). | rehearsed |
| Landing, live | the go's two printed commands | The gate screen: lands in `Processed_Tracks/2026/11_06_26 Multinotes`, playlist `2026-11-06 Multinotes` under INBOX, labels filed from the manifest under Record Labels, label playlists `Multinotes 2020 (3, added to)` and `Multinotes 2019 (4, added to)`, **"rehearsal: ... digest aa9dfb01ac794d83, equal to this plan's"**. Approved as `session`, applied: `intake.land: ok`, the `rows-await-analysis` warning naming 5 Normal and 2 Dynamic rows. The `gate-sibling-run` warning named the 2026-10-31 landing still open; it was not answered. | live |
| Visit, pre check | `crate --output json analyze check`, exit 12 | scope `analyze`, batch 7, not analysed 7, dyn 2. | ok |
| Visit, Normal | INBOX / Analyze (7), all selected (status line "Selected: 7 Tracks"), Analyze Tracks | The dialog opened on Dynamic; set by the held press and read back: **Normal, high precision off, BPM / Grid on, Phrase on, KEY on, Vocal off, CUE off** (BPM range 78 to 155, as it was). Wait done, **7 of 7**, ended 26 s after OK. | done |
| Visit, Dynamic | the two `dyn` rows selected by a click and a Command click (status line "Selected: 2 Tracks"), Analyze Tracks | Read back: **Dynamic**, every other field as above. Wait done, **2 of 2**, ended 26 s after OK. | done |
| Quit | rekordbox menu, Quit | Both processes gone in 3 s. | checked |
| Check | `crate analyze check`, **exit 0, done** | 7 analysed; grids 5 constant, **2 variable, both on the dyn rows** (119.74 to 120.14, 119.58 to 120.17); keys 7 filled, 5 equal, 2 far (`Only Clouds` head 01A, rekordbox 09A; `Rouge` head 08B, rekordbox 05A). Every row reads 120 BPM in rekordbox, where three heads read 80 and 96, a half and four fifths reading by `analyze run`. | done |
| Clear | rehearsed on the refreshed copy, run `2026-11-06T13:59:05Z-98c0`; live run `2026-11-06T13:59:14Z-5aa8` | **digest `c1e7fe893b6b06b5`, count 7, equal**; applied as `session`: 7 rows left INBOX / Analyze, which reads back 0. | live |
| Filed | a copy of the live database | `INBOX / 2026-11-06 Multinotes` 7; `Record Labels / Multinotes / Multinotes 2020` gained `Snedmea`, `Just Now`, `Only Clouds`, and `Multinotes 2019` the other four. | read |
| A71, first mark | `crate label mark Multinotes --pass 2026-11-06T134742Z-bdcc`, run `2026-11-06T13:59:52Z-5733` | "pass: 2026-11-06T134742Z-bdcc, **landed on the database native 'inbox' tree**", but "nothing to mark: no year playlist was built for this label on this library". Answered `abort`. | read |
| The year playlists | `crate label playlists Multinotes`, run `2026-11-06T14:00:01Z-6604`, 41 calls, then approved as `session`, 35 calls | The account already held a `Multinotes` folder with year playlists 2019 to 2022; the plan adopted all four (adding 7, 7, 1 and 7 tracks the label's 11 confirmed releases carry), digest `68d758f1f3984ece`, "removes: nothing, ever". Applied. | live |
| A71, the mark | the same verb, run `2026-11-06T14:00:17Z-2198`, 5 calls | Gate `label.mark.confirm`: the pass landed native; **renamed on the account: none**; left alone **`DOWNLOADED Multinotes 2019` and `2020`, "its name already carries the prefix"**, and **`2021` and `2022`, "the landed batch filed no track of this year under the label"**. So the plan reads exactly the batch's two years and names why each other year is left. The account had carried the prefix on all four before this sitting, so no rename could be made. Applied: `no_op`. | met, no rename owed |
| A71, unmark | `crate sync unmark --pass 2026-11-06T134742Z-bdcc`, run `2026-11-06T14:00:29Z-5c0b` | "put back on the account: none ... the mark record holds no playlist this pass renamed", which is exactly what the mark did. Answered `abort`. | met |
| macOS battery | cited | Sitting 78's on `049c973c`, v0.11.1, which carries U190 and R-1056. | cited |

**A59 (#421) is met**: the one command from the go's gate to the landing's gate, its report lines and checks, the landing's run `2026-11-06T13:54:11Z-8fce` answered and applied, and the visit. **A71 (#445) is met**: the mark read the pass as native, planned only the batch's years and named the rest; the rename was already on the account, and the unmark planned exactly what the mark did. **A45 (#369) waits on Phillip**, as above. **Calls:** 136 through the gate (50 go, 76 label playlists, 10 mark).

**A correction to sittings 79 and 80.** The counts read there from a copy of the database came from a reader that counted soft-deleted playlist rows too: INBOX / Analyze read 40 rows that way and 0 live. rekordbox's counts (Organic House Low 362, Med 403, High 329; Minimal / Deep Tech Med Energy 186) are the live rows, and the gaps those sittings left untraced are the deleted rows. The INBOX comparisons and the Rominimal band read stand: read again on live rows only, each of the 96 is in exactly one band (39, 41, 16).

## Sitting 82, 2026-11-06, the attended session on v0.11.1, with desktop control: A57 (#415), DEADCA7 installed, its push not aimed at a copy

| Step | Ran | Observed | State |
|---|---|---|---|
| Installed? | `/Applications`, the home folder's `Library` | **`DEADCA7.app` is installed** (0.2.3, build `0345c1db`, its settings read), with `DEADTRAX.app` beside it. It has run: its state is in `Library/Application Support/deadcatalog` (a `runtime/ml-v0.3.3` engine, made 2026-10-26) and its logs in `Library/Logs/deadca7`. There is no `deadca7` support folder and no `rekordbox-backups` folder, so it has never pushed. `crate doctor`'s `deadca7.push` reads "DEADCA7 is not installed here", because it probes the `deadca7` folder only: filed as #576 (U224), P2. | read |
| Where a push would go | launched once, the Catalog, Export and Settings screens read, nothing pressed that writes | No catalog is open; Settings' `Library` section reads "No library" and offers no database chooser. The launch log reads **"rekordbox found" and the live database's path on the library volume**: the app resolves the live database by itself, from the rekordbox agent's settings as the 2026-10-26 assessment read in its source. | read |
| Decision | the session's call | **No push was made.** From its own window a push writes the live database, which the brief forbids. The one way to aim it at a copy is to point the rekordbox agent's own settings at the copy for the push and back afterwards, which also points rekordbox itself there, and a slip writes the live library or leaves rekordbox on the copy. That is not a step for a session nobody is watching. | held |
| After | DEADCA7 quit from its menu | The live database read sha256 `d92feb314cd0a4b4` before the launch and after the quit: nothing written. | checked |

**A57 (#415) waits on Phillip**: a sitting he is present for decides how a DEADCA7 push reaches a disposable copy (the agent settings redirected and put back with him watching, or an app build that takes a library path), then takes the brief from the push on. The doctor's false "not installed" is #576.

## Sitting 83, 2026-11-06, the attended session on v0.11.1, with desktop control: the first Bandcamp run, A44 (#368), A45 (#369) and A62 (#427), with A72 (#446) left nothing to fetch

Phillip recorded the Bandcamp session himself (`crate doctor`: `credential.bandcamp` ok, 14:01Z). Conditions as at sitting 81. The four PULS purchases are releases Phillip bought, so fetching them took no per-label decision; no other label was answered or registered.

| Step | Ran | Observed | State |
|---|---|---|---|
| The account (A44) | `crate acquire bandcamp`, run `2026-11-06T14:04:57Z-088c` | 26 purchases new, 154 owned, 2 held (Dafs `El Capitán's DJ Tools vol.8`); most purchases are listed twice. **13 sellers unregistered**, each named with its `crate label registry add <label name> --bandcamp SELLER` command, among them `pulsromania`. | read |
| Register (A62) | `crate label registry set PULS --bandcamp pulsromania` | ok; `crate acquire bandcamp --seller PULS` then read **5 new (4 releases, `Over Me EP` twice): Space-Time VA, Summer EP, Love EP, Over Me EP**, and "staged under their label: pulsromania as PULS". | live |
| Fetch (A44, A62) | `crate acquire bandcamp-fetch --seller PULS`, job `2026-11-06T14:06:20Z-a5da`, **43 s** | 4 of 4 settled, **8 FLAC files, 357 MB**, into `Downloads/Bandcamp 2026-11-06`; `bandcamp-land-by-label` names the `--label-from-tags` landing. **Every file carries `label` PULS and a `date`** (2021 or 2026), no genre, no ISRC. The verb reports nothing about the download page, the stat answer or the file host, so the first run measures only the count and the time; no surprise met. | live |
| Split | by hand in staging | `Over Me EP` (2 files) moved to `Downloads/Bandcamp 2026-11-06 Over Me`, so A45 lands with `--label` and A62 with `--label-from-tags`, one batch each. | done |
| Tail | per folder: `tag folder`, `analyze run`, `analyze vocals --unscored`, `analyze restamp`, `name apply` | Tagged **Rominimal** on all 8 by PULS's registered genre; analysed and named (`01A - 123 - Cojoc - Over Me EP - 02 Tres Bien.flac` and so on), every job succeeded. | done |
| A45, rehearsal | `crate intake land "<Over Me folder>" --label PULS --rehearse` | First plan digest `cb359bb97d67eccf`, batch named **`2026-11-06 Downloads`**, the staging root's name, not the folder's or the label's; aborted, and planned again with `--name "2026-11-06 Bandcamp PULS Over Me"`: rehearsal `2026-11-06T14:16:21Z-be6b`, **digest `13a7111c1c57b423`**, added 2, integrity ok, refused 0. | rehearsed |
| A45, live | run `2026-11-06T14:16:47Z-cdb8` | The gate: "labels filed from: --label PULS, each file's year from its date tag", label playlists `PULS 2021 (2 file(s), added to)`, rehearsal "equal to this plan's". Approved as `session`: landed. | live |
| A62, rehearsal | `crate intake land "<the six>" --label-from-tags --name "2026-11-06 Bandcamp PULS" --rehearse`, run `2026-11-06T14:17:56Z-258c` | **digest `4b76fc07fbb2b997`**, added 6, integrity ok. | rehearsed |
| A62, live | run `2026-11-06T14:18:19Z-3075` | "labels filed from: each file's own label tag, its year from its date tag", **`PULS 2026 (4 file(s), added to)` and `PULS 2021 (2 file(s), added to)`**, one per release year; equal digest, approved as `session`: landed. | live |
| Label column (A62) | rekordbox, INBOX / Analyze, the Label column shown | **Empty after the landing; after Reload Tags on the 8 rows, `PULS` on every one.** rekordbox reads the Vorbis `label` comment Cratekit writes, so no card moves the field. | read |
| Visit | Normal on all 8, read back (Normal, high precision off, BPM / Grid, Phrase, KEY on, Vocal and CUE off); none marked dyn | Wait done, 8 of 8, ended 26 s after OK; quit, both processes gone in 6 s. `crate analyze check` **exit 0**: 8 constant grids, keys 7 equal and 1 far. Clear rehearsed and live, **digest `d10de34f566cf958`**, equal; INBOX / Analyze reads 0. | done |
| In rekordbox | Record Labels / PULS | `PULS 2021` holds `Tres Bien`, `Walking Over Me` and `Arrival`, `PULS 2026` the Love EP and Summer EP tracks, each with Label PULS. | read |
| Genre sub | `crate route resort`, rehearsed (`2026-11-06T14:22:00Z-d567`) and live (`14:23:00Z-8ef0`), **digest `d9fedc1c16682fc6`, 8 adds**, equal | A landing files a Rominimal row into its band but not into the Rominimal genre sub, which only a resort or a rebuild files. After the resort, Rominimal holds 104, each still in exactly one band. | live |
| A72 | `crate sync bandcamp --seller PULS`, run `2026-11-06T14:24:15Z-bee5` | **`no_op`**, "the account has nothing new to fetch (182 purchase(s), 85 owned, 5 fetched before)": this sitting's fetch took PULS's new purchases, and no other followed label has a seller registered. | waiting |
| macOS battery | cited | Sitting 78's on `049c973c`, v0.11.1, which carries U156, U176, U177 and U179. | cited |

**Met:** A44 (#368), the first Bandcamp run from login to landing; A45 (#369), a label batch landed natively with `--label PULS`; A62 (#427), the seller registered, the batch fetched tagged PULS, landed by its tags into one year playlist per year, and rekordbox's Label column read as `label`. **A72 (#446) waits** on a new purchase from a followed label with its seller registered: Phillip's next PULS purchase, or his registering another label's seller. Small findings, no card: a batch landed with `--label` and no `--name` is named after the staging root, `<date> Downloads`; and a landing does not file the genre sub.

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

The genre work's last item, `crate delete review` over the 36 tracks removed
at sitting 29, closed at sitting 45 another way: the rows are gone outright,
so the pass cannot offer them (the residual filed there), and the files went
to the volume's Trash by Phillip's hand as `Removed_from_collection`.

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
