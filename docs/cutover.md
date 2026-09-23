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

## What blocks a full sync cycle, stated plainly

The board is complete and the product cannot yet do its central workflow,
because two seams have no adapter behind them and one source has no listing.
Each was a residual and is a unit on the board since this sitting: U62 (#84) the catalogue, U63 (#85) the account, U64 (#86) the playlists source, with U29 declared dependent on all three.

1. **R-258, the catalogue.** U62 landed its agent half on 2026-09-16:
   `label.catalogue.resolve` now returns `label.tidal_catalogue.TidalCatalogue`
   over the stored session, proven against a fake client only. **Owed to the
   next attended sitting:** one real `crate intake playlist`, one real label
   sweep and one real harvest, plus the observations R-350, R-352, R-353 and
   R-354 close on. Before U62, `label.catalogue.resolve` refused
   `label-catalogue-unbound` on every real invocation once a session existed.
   `intake playlist`, the label sweep and the playlist harvest all end there.
   Consequence for acquisition: `acquire download` refuses a text list and
   needs a provider list document, and nothing in the product can produce one.
   The download smoke test above used a hand written document carrying a
   track id found through the library the adapter sits on.
2. **R-226, the outbound account.** U63 landed its agent half on 2026-09-16:
   `modules.outbound.account.resolve` now returns
   `modules.outbound.tidal_account.TidalAccount` over the stored session, proven
   against a fake client only. **Owed to the next attended sitting:** one real
   `crate export playlist` and one real `crate sync favorites`, which is R-144's
   closing condition. **Read R-355 first**: the rows those verbs build carry no
   ISRC, so a live run today matches nothing and writes nothing until the rows
   gain one. R-356 and R-357 are the observations the same sitting can make.
3. **The playlists source.** U64 landed its agent half on 2026-09-16:
   `crate sync all` lists the account's own playlists through the catalogue's
   new `account_playlists` read, excludes the `DOWNLOADED ` prefixed ones, the
   ids in the playlists cursor, the favourites placeholders, open jobs and empty
   playlists, and queues each remaining one as an `intake.playlist` job under
   the pass's run id. Proven against a fake catalogue only. **Owed to the next
   attended sitting:** one real `crate sync all` on the slim or full profile,
   reading the `playlists` block of its summary against the live account, which
   is what R-361 closes on. **Read R-358 and R-359 first**: a swept playlist is
   not renamed on the account, so DJ_tools sweeps it again while both run, and
   swept means resolved, not acquired.

Until those three land, "the author lives on Cratekit through a full sync
cycle" cannot start, and DJ_tools stays the live system for everything that
lists Tidal. The vendored downloader is the only Tidal facing code that runs.

## Next sitting

The configuration is rebuilt and doctor is clean, so the queue is A5, issue
#178, in its own order, and the next sitting is line 1: favourites in, through
`intake playlist favorites`, `intake missing`, `acquire download`, `tag folder`,
`name apply`, `intake land` and the rekordbox import, with the heart count
compared against the account's 197, which is R-383's live half since U65 landed
its code half. R-361's rule landed on `relay/95`, so the 11 label debris
playlists are excluded before they are queued. The list this section carried
before sitting 5 is superseded by #178.

Anything that writes needs a backup acknowledgment inside its validity window:
`crate session ack` from a Terminal window, answered with `crate run decide`,
continued with `--run`, by the author and never by a session. The full library
vocal pass, R-376, is still a separate attended choice and is still blocked on
nothing.
