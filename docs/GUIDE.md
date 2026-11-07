# Using Cratekit

How to run Cratekit day to day. When this file and `crate --help` (or
`crate VERB --help`) disagree, the help is right.

## Install and set up

The [README](../README.md) covers requirements, install, extras and upgrade.

```bash
crate setup
crate doctor
```

- `setup` records the library root, the rekordbox database, the volume's
  identity, download staging, the profile, the taxonomy and the backup
  destinations. It offers to record each credential the profile needs, and
  proposes a rekordbox version pin and any location prefix rule, which only a
  yes adopts. Every other answer is also a flag (`crate setup --help`). Re-running keeps earlier
  answers unless a flag changes one, and ends by running doctor.
- `doctor` writes nothing. Each line is `ok`, `FAIL` (blocks a verb, names the
  fix) or `note` (no action).
- `crate profile show` lists the modules the profile switches on; `crate
  profile set slim|full|custom` changes the preset and nothing else. A verb
  whose module is off does not exist. Adoption is on in every profile.

### Credentials

Credentials live in the OS keychain, never in the config file. Record one
from a file only you can read; a value on the command line is refused:

```bash
crate login NAME --from-file PATH
```

| NAME | What |
|---|---|
| `provider-session` | The streaming account session, used to list and download. Obtaining it is two commands at a browser: see [`adapters.md`](adapters.md). Delete the plaintext token file afterwards, and after a download run, which can write it back. |
| `bandcamp-session` | The browser's bandcamp.com cookie, for the Bandcamp verbs. |
| `identify-key`, `identify-signing-key` | The recognition service's key and signing value, for `intake set` and `intake identify`. |
| `catalogue-app-id`, `catalogue-app-key` | Optional. Cratekit's own app on the provider's developer platform. With both recorded, catalogue lookups go under the app rather than your account; doctor says where lookups go and how many calls each side made. |

A provider that rejects the stored session is reported as rejected, with the
sign in step. A provider that fails or cannot be reached is reported as an
outage to wait out; the session is kept.

## How it works

Cratekit reaches your rekordbox library three ways:

```
                         reads only
  rekordbox --(export)--> collection XML file --------> reports, audits,
     |                                                  favourites sync, playlist export
     |   you import by hand
     +<------------------- importable XML file <-------- intake land (xml bridge)
     |
     |   guarded write: rekordbox closed, backup acknowledged
     +<------------------- the live database <---------- landing (database native),
                                                         route, adopt, organize, restore ...
```

- **A collection export** (a Fresh Export) is a rekordbox XML of the whole
  collection. Verbs that take one never read the live database. A stale export
  answers wrongly and confidently, so take a fresh one when it matters.
- **An importable file** (the intake file, `*_inboxed.xml`) is what a landing
  writes while the intake tree is on the xml bridge. You import it into
  rekordbox.
- **The guarded write** is the only path to the live database. It refuses
  unless the recorded library volume is mounted, rekordbox and
  `rekordboxAgent` are both closed, the pinned versions match and a backup
  acknowledgment is on record. It snapshots first and reads the result back.

Terms:

- **Tree.** A playlist tree the taxonomy governs: INBOX, BY GENRE + ENERGY,
  Record Labels and so on. Each tree is either on the **xml bridge** (written
  through an importable file) or **database native** (written straight to the
  database). `crate tree cutover TREE --export FILE` moves a tree to the
  database; `crate tree revert TREE` puts it back before its first native
  write.
- **Job.** Long work is queued and returns a job id. `crate job list`,
  `job show ID`, `job resume ID` (repeats no finished work) and `job cancel
  ID`. `tag folder`, `analyze run` and `analyze restamp` drive their own job to
  the end; Ctrl-C names the `--job` command that finishes it, and
  `--queue-only` queues and returns.
- **Run.** One invocation's decision state, kept on disk so a gate can be
  answered later from another terminal.
- **Gate.** A named question a verb stops at before it writes. There is no
  `--yes`. See [Answering a gate](#answering-a-gate).
- **Review item.** One decision only a person can make, such as whether a
  remix counts as the track. A verdict is remembered.

Root options go before the verb:

```bash
crate --output json doctor           # one JSON envelope
crate -d route.inbox.apply=apply route inbox   # answer a gate inline
crate --run RUN_ID route inbox       # continue a run stopped at a gate
crate --calls 2000 --run RUN_ID sync pair   # raise the provider call ceiling for one run
```

## Before every session

1. Quit rekordbox and its background agent. Every verb that writes the
   rekordbox database refuses while either runs.
2. Mount the library volume.
3. `crate doctor`; read the `FAIL` lines first.
4. `crate status`: open runs, each source's sync state, and any tree whose
   membership no longer matches the database. Gates idle over a week are
   summarised in one line with the command that retires them.

## Where it stands

Which workflows have run on a real library, and with what result, is recorded
per workflow in [`cutover.md`](cutover.md). For a workflow not recorded there,
run a small batch first, with a current backup, and check `crate restore list`
afterwards.

## Recipes

### Take a collection export

```bash
crate export collection /path/to/collection-export.xml
```

With rekordbox closed, writes a collection export from a copy of the database;
the live file is never opened. It never replaces a file, refuses a name ending
`_inboxed.xml`, `_synced.xml` or `_favorites.xml`, leaves smart playlists out
(counted and named), and carries no tempo, grid or cue points, so it is not a
backup. Take a new one after anything writes the database.

### Run a sync pass

The everyday path from the streaming account to filed rows. It needs a
database native intake tree.

```bash
crate sync land
```

`sync land` takes the pass to its landing gate in one verb: preflight
(rekordbox closed, no backup running), `sync all`, its intake jobs, the
missing list, the download, then the tail in this order: `tag folder`, `tag
guess`, `analyze run`, `analyze vocals --unscored`, `analyze restamp`, `name
apply`. It then plans `intake land` and stops at `intake.land.native`, printing
the two commands that answer and apply it and the rekordbox visit after.

- A tail step that fails ends the pass there; no landing is planned over
  files the tail did not run on.
- A track the download refuses for good (lossy only, gone from the provider)
  is named and skipped. Anything a wait would mend ends the pass.
- A missing track already staged by an earlier unlanded download is not
  downloaded again.
- When the vocal model cannot score here it stops first at
  `sync.land.without-vocals`; install the `vocals` extra, or answer
  `crate -d sync.land.without-vocals=go sync land` to land unscored.
- Two staged files with one ISRC stop `name apply`; keep one, move the other
  out, and continue.
- `crate sync land --pass-run RUN_ID` continues an earlier pass, by either run
  id it printed. Jobs already ended are read, not driven again.

Then, in order:

1. Optionally rehearse: the landing command with `--rehearse` (see [Land a
   batch](#land-a-batch)).
2. Answer and apply the landing with the two printed commands.
3. The rekordbox visit, below.
4. `crate sync mark --pass PASS` to prefix the finished account playlists.

**The rekordbox visit.** Cratekit never analyses inside rekordbox and never
writes a grid. Open rekordbox, select `INBOX / Analyze` and run Analyze Tracks:
rows without the `dyn` My Tag with Analysis Mode Normal, high precision off,
BPM/Grid, Phrase and KEY on; rows with `dyn` with Analysis Mode Dynamic, every
other setting the same. Quit rekordbox and confirm `rekordbox` and
`rekordboxAgent` are gone. Then:

```bash
crate analyze check        # exit 0 done, 12 rows still waiting, 27 suspect
crate inbox analyzed       # take the analysed rows out of INBOX / Analyze
```

`analyze check` reads a copy and writes nothing: every row analysed, every
grid one tempo (or moving on a `dyn` row), Key filled, and how often the
title's key agrees with rekordbox's. `--pass` or `--session` names one
landing.

`sync all` alone queues each enabled source's increment under one run and
returns at once; nothing has run until the jobs are resumed. It sweeps no
labels (`crate label sync` does). The favourites source needs `--export` and
asks `sync.all.favorites.confirm`. A source's watermark moves only after a
pass in which every item finished. An open intake job holds its playlist out
of later passes; `crate job cancel --stale-days 30 --dry-run` lists old ones,
and without `--dry-run` cancels them.

### Bring music in

Pick the verb by what you hold:

```bash
crate intake playlist https://tidal.com/playlist/PLAYLIST_UUID
crate intake playlist favorites          # every heart on the account
crate intake file /path/to/one-track.aiff
crate intake set /path/to/recording.wav  # or a mix URL
crate intake identify /path/to/recording.wav
crate match run /path/to/tracklist.txt
```

- `intake playlist` queues a job that sorts each track into owned, offered
  (another version is held: a review item) or missing. It downloads nothing
  and writes nothing to the account.
- `intake file` plans one file. On the xml bridge it writes only with
  `--export`; once the intake tree is native it takes no export, plans one
  collection row and one INBOX playlist for the file where it sits (it must be
  inside the library), and asks `intake.file.native`.
- `intake set` identifies a recording or a mix URL (fetched with `yt-dlp` to
  scratch, then removed) and resolves its tracks; `intake identify` names the
  tracks and stops. Both call a paid recognition service and refuse before
  the first call without its keys. A recording over one recognition run's
  bound (about 2h45) is identified in up to three even parts, still one set.
- `match run` sorts `Artist - Title` lines into matched, needs review and
  missing.

Turn what is missing into a download list:

```bash
crate intake missing --job JOB_ID     # one finished intake job
crate intake missing --run RUN_ID     # a whole sync all pass, one list
crate intake missing --list PATH      # a text list, searched on the provider
```

- Lists go to `lists/` under download staging, or `--out`. Owned, offered and
  deliberately deleted tracks are left out. A job not finished is refused;
  with `--run`, `--skip-failed` leaves out failed or cancelled jobs.
- A set track has no provider id, so it is listed only when exactly one
  provider track carries its ISRC. The rest go to `intake-JOB_ID.unlisted.json`
  with the reason.
- `--list` checks every line against the library first, then searches the
  provider. A line is listed only on one exact match in artist, title and
  version; otherwise its candidates become review items (`review list --queue
  version-match --kind provider-candidate`). Accept one and run again. The list
  is written as `NAME-found-DIGEST.list.json`, so a run after a review answer
  writes a new list.
- A missing track already sitting in download staging (same ISRC) is counted
  `staged` and not listed.

For bootlegs, white labels and promos the provider lacks:

```bash
crate acquire fallback PATH        # searches SoundCloud, then YouTube; offers review items
crate review list --queue fallback-source --kind fallback-candidate
crate review resolve ITEM_ID --verdict accepted --option URL
crate acquire fallback-fetch PATH  # downloads the accepted ones, marked lossy
```

Download and audit:

```bash
crate acquire download LIST
crate acquire audit                # files that break the lossless policy
```

`acquire download` fetches into download staging through the configured
adapter, paced. A track refused for good is skipped and named in an
`acquire-refused` warning.

Then the tail and the landing, in this order (`sync land`, `label sync --go`
and `sync bandcamp` run it for you):

```bash
crate tag folder /path/to/staging
crate tag guess /path/to/staging --pass PASS
crate analyze run /path/to/staging
crate analyze vocals --unscored /path/to/staging
crate analyze restamp /path/to/staging
crate name apply --root /path/to/staging
crate intake land --pass PASS
crate route pending
```

- `tag folder` writes genre and album art to the files only. A file of a
  registered label with a genre takes that genre with no catalogue asked; any
  other file no catalogue knows keeps no genre.
- `tag guess` gives each file with no genre one from its artist's other
  tracks and, with `--pass`, the account playlist that asked for it. A file
  that has a genre is never changed. `--report` writes nothing. Each genre
  word your taxonomy has no folder for is named, with the `taxonomy alias` or
  `taxonomy folder` command that answers it (see [Keep the library
  tidy](#keep-the-library-tidy)).
- `name apply` renames from your naming template behind
  `name.apply.confirm`. A relative `--root` is read against the library root.
- `route pending` places tracks whose routing was decided before the library
  held a row for them; on the xml bridge it has nothing to place.

### Land a batch

`intake land` moves staged files into the library and adds them as one
batch: a folder and an INBOX playlist of the same name. Staging must be on the
library's volume. A file whose name is taken stays in staging and is named.
Two landings under one batch name never run at once.

The batch name, unless `--name` gives one:

| Handed | Batch |
|---|---|
| `--manifest` naming one label | `2026-10-03 Some Label` |
| `--manifest` naming several | `2026-10-03 Labels` |
| `--pass` of account playlists | `2026-10-03 Tidal playlists` |
| `--pass` of hearts | `2026-10-03 Favorites` |
| `--pass` of a set | `2026-10-03 Set` |
| `--pass` of several kinds | `2026-10-03 Tidal playlists and Favorites` |
| a Bandcamp batch | `2026-10-03 Bandcamp Some Label`, or `2026-10-03 Bandcamp` |
| none | `2026-10-03 Downloads` |

A second batch of the same name the same day gets ` 2`, then ` 3`. A pass
that swept your own account playlists also gives each its own INBOX
playlist, named as on the account with the landing's date at the end.

**On the xml bridge** the landing needs `--export`, takes `intake.land.confirm`,
and writes an importable file beside the library: `PASS_inboxed.xml` with
`--pass`, `NAME_inboxed.xml` with only `--name`. Import it into rekordbox,
quit, take a new export, and prove the import:

```bash
crate intake land --export /path/to/collection-export.xml --pass PASS
crate intake imported --export /path/to/export-after-import.xml
```

`intake imported` renames the file to `*.imported` once every landed file is
in the export, and changes nothing while any is missing. The importable file
itself is refused as the export. Files stay under `Music/<batch>` until
`crate intake shelve BATCH` (or `--all`) files them under the processed
folder by year and date, behind `intake.shelve.native`; `--report` plans only.

**Database native** (`crate tree cutover inbox --export FILE`), the landing
takes no export and refuses one. It writes each row itself, with artist,
album, album artist, genre and year from the file's tags, puts the batch
playlist under INBOX and every row in `INBOX / Analyze`, and asks the explicit
gate `intake.land.native`, answered only by `crate run decide`. Nothing about
the audio is written: no tempo, grid, key or waveform. Files go straight to
`Music/<processed folder>/<year>/<MM_DD_YY subject>` (`Processed_Tracks` by
default), so no shelve follows. A row whose tempo moves (drift from `analyze
run` at or over `analysis.drift_cut`, 1.5 by default) carries the `dyn` My
Tag.

- `--rehearse` copies the database and library state to a scratch folder,
  applies the landing to the copy over clones of the staged files, reports the
  digest and removes the folder. Nothing live changes. The live landing then
  says whether its plan equals the newest rehearsal. A failed rehearsal keeps
  its folder and names it.
- When the genre tree is native too, the same answer files the new rows into
  BY GENRE + ENERGY; the gate shows each row's bucket. If the plan after the
  commit differs, nothing is filed and the run names `crate adopt apply`.
  `--land-only` lands without filing.
- `--manifest` (from `label approved`) files label tracks under `Record Labels
  / <Label> / <Label> <year>`. `--label NAME` files every file under one label;
  `--label-from-tags` files each by its own label tag. Either uses the file's
  date tag for the year; a file without one is named and filed nowhere.
- `--set JOB` also writes the set's permanent playlist under INSPIRATION.
  `crate intake inspiration --job JOB` does the same for a set landed without
  it.
- A row landed by an older version that will not load to a deck is mended by
  `crate repair rows`.

### Mark the account

```bash
crate sync mark --pass PASS                     # database native
crate sync mark --xml /path/to/PASS_inboxed.xml # xml bridge
crate sync mark --pass PASS --playlist ID       # only these playlists
crate sync unmark --pass PASS
```

`sync mark` prefixes `DOWNLOADED ` to each account playlist of the pass whose
every track is now in the library, behind `sync.mark.confirm`. A playlist with
a track still missing is left and the track named; one renamed since the plan
is skipped; none is prefixed twice. A partial failure names what was renamed,
and a rerun does the rest. `sync unmark` restores each title the pass's mark
wrote, only where the title is still exactly what the mark wrote. Unmarking
does not make the next `sync all` offer the playlist again. `crate organize
--only marks` marks every landed pass.

### Follow record labels

```bash
crate label registry                                 # list who you follow
crate label registry add "Some Label" --match "Some Label Rec"
crate label registry set "Some Label" --genre Rominimal --bandcamp somelabel
crate label registry rename "Some Label" --to "New Name"
crate label harvest https://tidal.com/playlist/PLAYLIST_UUID
crate label registry adopt
crate label sync
crate label sync --go
```

- A label's id is made once, at `add`; what has been pulled hangs off it.
  Rename with `registry rename`; removing and re-adding makes the whole
  catalogue new again.
- `registry set` fields: `--match`, `--seed`, `--track-limit`, `--offer`
  (releases kept in review per sweep, `labels.offer_per_sweep` by default),
  `--kind` (for the genre gate), `--genre` (given to the label's files with
  no genre, so no catalogue is asked; one routing only to the fallback folder
  needs `--accept-fallback`) and `--bandcamp` (the seller account). `default`
  clears `--kind`, `--genre` or `--bandcamp`.
- `harvest` offers the labels behind a playlist as review items; `registry
  adopt` adds each accepted one not already held.

`label sync` walks your labels one at a time and asks only about releases new
since that label was last asked, with release and track counts and a size.
Answers: `all`, `pick` (by number), `not-now`, `stop` (unfollow). Each answer is
saved as given; `quit` and the next run resumes at the first unanswered label.
A release answered once is never asked again. The genre gate runs first, so
a release it holds is never asked about. Without a terminal:

```bash
crate label sync --next [--label "Some Label"]
crate label sync --answer pick --label "Some Label" --release RELEASE_ID
```

A label whose listing fails is a `[FAIL]` line, never "nothing new"; a run
where no label could be read ends refused, `label-sync-unlisted`. A label's
listing is kept seven days, so a second ask makes no listing calls; deleting
the file its `listing` line names lists it afresh.

`label sync --go` shows one summary of every answer since the last go at the
explicit gate `label.sync.confirm`. Answer it with `crate run decide RUN
label.sync.confirm apply`, then `crate --run RUN label sync --go` downloads,
paced, and runs the same tail as `sync land`, then plans `intake land
--manifest ... --pass ...` and stops at its gate. A go stopped part way is
resumed by the next `--go`. Every go stages into the same folder, so land
each before the next.

Other label verbs:

| Verb | Does |
|---|---|
| `label approved` | Writes a download list and a `.manifest.json` from accepted label releases, leaving out what you own. Each run supersedes the last unfetched list. |
| `label import NAME` | Brings one label's catalogue in, as a job. |
| `label held [return RELEASE_ID ...]` | Lists releases the genre gate holds back, or returns some to review. |
| `label judge [--label NAME]` | Judges releases waiting in review by the label's kind and holds what the gate would not file. |
| `label artists` | Puts the artist's name on open releases whose artist reads as a provider address. |
| `label playlists LABEL [--releases]` | Keeps the label's account folder of private `<Label> <year>` playlists; adds, never removes. `--releases` reads only what the last go took. A full build over 500 calls stops at `label.playlists.crawl` first. |
| `label mark LABEL --pass PASS` (or `--xml FILE`) | Prefixes `DOWNLOADED ` to the year playlists a landed batch filed. |
| `label prune LABEL` | Takes held or no longer confirmed tracks off the label's year playlists. |
| `label heard LABEL YEAR DATE [--release ID]` | Moves a dated `<Label> <year> new <date>` playlist's tracks into the year playlist and removes the dated one. |

`crate sync labels` is retired; it only resumes a labels sweep queued before
`label sync`, with `--job JOB_ID`.

### Bandcamp

```bash
crate acquire bandcamp [--seller NAME]          # purchases, newest first, with what you own
crate acquire bandcamp-fetch [--seller NAME]    # stage what you do not own
crate sync bandcamp [--seller NAME] [--batch NAME]
```

`bandcamp-fetch` stages into `Bandcamp <today's date>` under download staging
and writes the label's name into the label tag of every file from an account
a registered label names. `sync bandcamp` does the whole run: plans the
purchases (an expired session stops here with the login step), fetches, runs
the tail through `name apply`, rehearses the landing, and plans it, with
`--label-from-tags` when any staged file carries a label tag, stopping at its
gate. Rerun with the same `--batch` to
continue; nothing fetched is fetched again. It needs a native intake tree.

### Sets

```bash
crate intake set https://example.com/mix --dj NAME --set-name NAME
crate export set TRACKLIST [--name NAME]    # a set or typed tracklist as a private account playlist
crate export archive [NAME]                 # file a downloaded set's playlist in Downloaded Sets <year>
```

`export set` lists a row by its provider id, its ISRC, an accepted review
candidate, or one exact catalogue match, never a score; the rest are named on
the gate. With no tracklist it backfills INSPIRATION playlists that have no
account playlist; `--rename JOB` renames one to its INSPIRATION name.
`export archive` with no name archives every recorded set whose download is
proven.

### Keep custom playlists in rekordbox

```bash
crate sync twins
crate sync pair
crate sync release ACCOUNT_ID    # or --all
crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID
```

- A custom account playlist lands as an INBOX playlist, which rotates out.
  Its **twin** is the permanent copy in `Custom Playlists <year>`. A landing
  writes the twin itself; `sync twins` makes one for every `DOWNLOADED`
  playlist already on the account.
- `sync pair` keeps each pair one list both ways: additions and removals on
  either side land on both, and a track the library lacks is queued once,
  however many pairs list it: a pair listing a track another pair's job
  holds names it awaiting. A track a landing brought in through any account playlist is the library's
  and is added, never queued again. When one side added and the other removed between syncs, the later change
  wins; with either time unknown the track stays and is named.
- A twin's missing tracks are held, not downloaded, until `sync release`
  names that twin.
- While a session log record cannot be read (torn, or written by a later
  build), or the log cannot be listed, any landing it holds may have
  brought a track in, so a missing track that carries an ISRC is held and
  named, not downloaded, until the record reads. The warning names each
  record; a track with no ISRC is queued as before.
- With no argument, `sync pair` also pairs every plain playlist you made in
  rekordbox: a top folder becomes a root folder on the account, each playlist
  one private playlist titled folder first (`GIG READY Opener`); a root
  playlist goes in `Playlists`. A playlist you make in such an account folder
  comes into rekordbox at the next sync.
- Never found by a bare `sync pair`: Cratekit's own trees, Favorites, twins
  (a twin is paired with its account playlist when it is made), smart
  playlists, another app's folder, and folders `outbound.pair_skip_folders`
  names (`["ARCHIVE"]` by default).
- It plans once; the rekordbox gate `sync.pair.rekordbox` then the account
  gate `sync.pair.account` (each `apply` or `skip`) reuse the plan. A playlist
  changed before the write refuses as stale. A write stopped by the call
  ceiling names the `crate --calls N --run RUN sync pair` that finishes it.
- After a removal on Tidal it cannot read back, it names the playlist: look
  at it in the Tidal app before running anything again.
- Tidal's order is kept in rekordbox's order only for pairs under GIG READY;
  set `outbound.pair_order_every_pair = true` to keep every pair's. Other
  pairs still sync their tracks both ways and keep rekordbox's order: the
  first sync leaves the rekordbox playlist in the order it stands in, each
  track only Tidal holds going in after the track it follows on Tidal, and a
  reorder you make in rekordbox later stays there until you reorder that
  playlist on Tidal. A Tidal reorder after the first sync is taken into
  rekordbox, and it brings Tidal's whole order, not only the tracks you
  moved. A rekordbox playlist paired while empty takes Tidal's order.
- An order is sent in one go, then read once, about 30 seconds later or
  after the other pairs are written. Not served yet, the pair is pending: the
  run ends ok and names it, every track is on Tidal and rekordbox is
  untouched. The next `sync pair` finishes it when Tidal shows the new order,
  and otherwise leaves the pair out until two readings at least 5 minutes
  apart agree. Nothing is moved again meanwhile, and a continue of a stopped
  run only reads the order. A stopped order records how many moves Tidal
  accepted before it stopped; once two readings agree on an order at or past
  those moves, the rest is sent from that reading, and only while Tidal
  still serves that order when the rest is sent, also when the same sync
  adds or takes off tracks; served older, nothing is moved, the pair is left
  pending and the next sync tries again. A reading from before
  them, or at a move whose landing is not known, leaves the pair out however
  long it agrees, until Tidal shows the moves, you move the playlist by hand
  in the Tidal app, or you release the pair. A run whose plan cannot be kept
  sends no order.
- A fresh `sync pair` after a write that stopped part way through putting a
  Tidal playlist in order finishes that order, from the side that led it,
  rather than reading its half done order as your edit. The gate names the
  run it finishes. A move you made on Tidal since still leads, and so does a
  reorder in rekordbox since. It remembers that stop however long you wait
  before the next sync, until a sync finishes the pair, and also when the
  pair's rekordbox playlist was deleted and you pair the Tidal playlist again
  with `crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID`: that first
  sync finishes the stopped order rather than putting its half done order
  into the new rekordbox playlist.
- Tidal can serve a playlist's old order or tracks to a paged read for
  minutes after a change, while the plain read is current. Where it plans an
  order or checks a write, `sync pair` reads both and takes the plain read
  when it holds every track. If the two disagree and it does not, the pair is
  left out of the run, or the write stops as moved if that starts after the
  plan; sync again a few minutes later. A playlist longer than the plain
  read's first page is read on past it, and is left out the same way when
  that longer read cannot be taken whole while the paged read holds every
  track. The answer's
  `read_backs` say how many readings each write took and how long it waited.

### Publish a playlist

```bash
crate export playlist PLAYLIST_KEY --export /path/to/collection-export.xml
crate export prune PLAYLIST_KEY --export /path/to/collection-export.xml
```

Give the playlist's stable id, never its title. `export playlist` is add only,
behind `export.playlist.confirm`, and updates the playlist it made before
(`--new-playlist` forces a new one); read the unmatched tracks it reports.
`export prune` takes off the remote playlist what the library playlist no
longer holds.

### Favourites

```bash
crate sync favorites --export /path/to/collection-export.xml
crate favorites backfill
crate favorites refresh
crate favorites split
crate favorites order
```

| Verb | Does |
|---|---|
| `sync favorites` | Hearts the library's favourites on the account. Add only; writes nothing locally. |
| `intake playlist favorites` | Queues hearts the library does not own for acquisition. |
| `favorites backfill` | Puts every owned heart into All Favorites and its month playlist, coloured Pink when uncoloured. Adds only. |
| `favorites refresh` | Makes each genre folder's Favorites playlist mirror All Favorites. |
| `favorites split` | Splits quarter playlists into month playlists and retires the emptied quarters. |
| `favorites order` | Orders the folder: All Favorites, months newest first, `Undated`, then the rest as they were. Positions only. |

A landing that places a heart colours it Pink in the same write. A colour you
set by hand is never overwritten. Nothing un-hearts or un-colours.

### Organize

```bash
crate organize --report
crate organize
crate organize --only file
```

One plan per side, one explicit gate each: `organize.rekordbox.approve`, then
`organize.account.apply`. Approve one and abort the other and only the
approved side is written. `--report` asks nothing. `--only KIND`, repeatable,
plans just those steps; a side with no kind named is not asked.

| Side | Kind | Does |
|---|---|---|
| rekordbox | `adopt` | Files unfiled tracks into BY GENRE + ENERGY and its `with vox` subs, as `adopt apply`. |
| rekordbox | `rotate` | Rotates INBOX, as `inbox rotate`. |
| rekordbox | `record-labels` | Listed only; a landing files label batches itself. |
| rekordbox | `inspiration` | Gives each `DOWNLOADED` set in `Downloaded Sets <year>` its INSPIRATION playlist of owned tracks in set order. |
| rekordbox | `mirror-edits` | Carries your edits to mirrored playlists on the account back into the library (genre, energy, favourites, INBOX batches). |
| rekordbox | `mirror-downloads` | Queues once each track you added to a mirrored playlist that the library lacks; the next new `sync land` pass takes the download. |
| account | `labels` | Builds missing label folders and year playlists, and plans each label's dated `<Label> <year> new <date>` playlist of releases a go took that day. |
| account | `sets` | Archives every set whose download is proven into `Downloaded Sets <year>`. |
| account | `marks` | Marks every landed sync pass. |
| account | `file` | Files each `DOWNLOADED` playlist at the root into its `<year>` folder. |
| account | `root` | Removes label debris whose tracks are all downloaded and empty root playlists, and empties legacy `<year> Custom Playlists` folders, each named on the gate. |
| account | `mirror` | Mirrors each BY GENRE + ENERGY genre folder, Favorites and INBOX's live batches to a root folder of private playlists. |
| both | `yours` | Lists playlists you made, with a suggested home; never moves or renames them. |

- An edit on Tidal to a mirrored genre playlist retags the track: moving it
  from `Deep House Low` to `Tech House Med` gives it that genre and an energy
  that files into Med; removing it from every genre playlist clears the
  file's genre and energy tags so `route unplaced` lists it, while
  rekordbox's Genre column keeps the old word until rekordbox reads the file
  again. The first organize after the
  mirror exists reads every difference as rekordbox's.
- A track downloaded for your edit is filed where you put it, though its
  landing first filed it by its tags ("landed for the account's edit"), even
  when the mirror has no snapshot of the playlist you put it in yet; a
  change you make in rekordbox after the landing still wins.
- An answer given on a later run applies the plan you were shown; a change
  on Tidal since refuses as stale.
- `--rematch` asks the provider again about rows the mirror remembers as
  unmatched.
- A dated label playlist older than `labels.new_playlist_age_days` (30) is
  listed; `label heard` merges it.

### Keep the library tidy

```bash
crate route inbox                 # file the intake folder into the taxonomy
crate route unplaced              # tracks no tree places
crate route resort                # after a genre or energy change, additive
crate converge                    # does each tree match the database
crate rebuild --tree TREE_ID --actor YOUR_NAME
crate audit coverage EXPORT
crate audit duplicates EXPORT
crate report library EXPORT
crate report intake-aging EXPORT
crate report genres
crate repair paths
crate inbox rotate
```

- `route inbox` and `route unplaced` take `--export` for a tree still on the
  bridge and write `<name>_routed.xml` or `<name>_placed.xml` beside it.
- `route resort` shows every addition at `route.resort.apply` and files only
  the routing tree; the old membership stays and is named. `crate adopt move`
  moves a track from the sub it holds to the one its file names, adding
  before removing.
- `converge` only reports. `rebuild` is the one repair for an unconverged
  tree; naming INBOX asks `rebuild.accept`.
- Audits and reports are read only. `audit duplicates` never deletes and
  remembers intentional alternates. `report genres` names genres with 50 or
  more tracks and no top level folder.
- `repair paths` proposes a shorter name for each file rekordbox would reject
  (over the path budget, or repeating its title); accept or reject each with
  `review resolve`, then `repair paths --apply` renames the accepted ones,
  never a file the collection references.
- `inbox rotate` moves a batch older than `reports.intake_stale_days` (30)
  into `INBOX / Old` and removes one in Old older than
  `reports.intake_expired_days` (90). Never a track. `inbox refill --pass
  PASS` refills a pass's mirrored INBOX playlists from the account.

**Adopting an existing library.** `crate adopt scan` queues a census; `crate
adopt apply` shows the plan at `adopt.apply.approve` and files tracks and
writes their genre tags.

**Genres.**

| Verb | Does |
|---|---|
| `tag rows [--leave ID]` | Writes each row's genre from its file where they disagree. |
| `tag suggest [--band] [--set ID=GENRE] [--catalogue]` | Suggests a genre for rows with none, from artist, folder and optionally the catalogues; writes file and row. |
| `tag retag FOLDER` | Replaces a genre too coarse to be final. |
| `tag remap` | Rewrites genres a tag job filed by a mapping the taxonomy has since changed. |
| `taxonomy alias WORD GENRE [--folder]` | Saves an unplaced genre word as an alias of a genre folder and retags the files whose one genre is that word. |
| `taxonomy folder WORD [--like GENRE]` | Makes the word a genre folder of its own with energy bands, copying family, tempo window and rating. |
| `taxonomy upgrade` | Adds the classes and buckets the shipped template has and your copy lacks. |

`taxonomy alias` and `taxonomy folder` keep the old copy beside it under a
dated name and refuse a word too coarse to be a genre (such as `Electronic`),
one already filed, or a genre the taxonomy does not declare. A word that is a
genre folder's name in another case takes only `taxonomy alias WORD "Exact
Name"`, which retags without touching the taxonomy. After an alias, run `tag
rows`, then `route resort`.

**Removing tracks.** `crate delete review` offers the files behind rows you
removed in rekordbox; confirmed ones go to the system Trash only. `crate
tombstone list` shows what was removed; `--revoke ID` lets that version be
acquired again.

**Review queue.** `crate review list [--queue Q] [--kind K]`, `review show
ID`, `review resolve ID --verdict accepted|rejected [--option X]` (or
`--where FIELD=VALUE` for many), `review clear ID` to ask again,
`review export PATH` and `review import PATH` (never overwrites a local
verdict).

### Analyse audio and score vocals

```bash
crate analyze run /path/to/folder
crate analyze vocals /path/to/folder [--recursive] [--unscored]
crate analyze restamp /path/to/folder [--recursive]
crate analyze calibrate LIBRARY_ROOT --recursive
crate analyze validate /path/to/labelled-folder
crate metadata mytags-vocals [--apply]
```

- Needs the `analysis` and `vocals` extras. Cratekit never writes a beat
  grid, tempo element or average BPM field, in any container; no flag turns
  that on.
- `analyze run` writes key, energy, vocal scores and a drift to the file's
  tags (`drift` reads `steady`, `variable` or `unknown`; `driftlevel` is the
  spread), then renames the file to the naming template's Camelot head. It
  skips a file already carrying the head, so `analyze vocals --unscored`
  scores the ones it finished with no `voxlevel`. Doctor's `install.extras`
  row says when vocals cannot score.
- `--recursive` queues every folder under the one named as one resumable
  job; linked folders are not walked. `analyze run` has no such flag.
- `analyze calibrate` fits only over the whole library walked recursively;
  anything else fails `calibrate.sample` unless `--accept-partial`. The energy
  fit samples 500 tracks at an even stride (`--sample N`); `--vocal-cut`
  sets the vocal cut by hand. `analyze restamp` carries a new calibration
  across the catalogue.
- `metadata mytags-vocals` plans My Tags from vocal scores; `--apply` writes
  them.

### Build a set, master a recording

```bash
crate setbuild /path/under/the/library/anchor.aiff --count 8 --role after
crate setbuild --named "Artist Title"
crate setbuild --unowned "Some Track" --key 8A --bpm 124
crate master /path/to/REC001.wav /path/to/REC002.wav --lufs -16 --output-dir /path/to/out
```

`setbuild` ranks owned tracks compatible with the anchor in key and energy,
offline. `master` joins a split recording's parts in the order given (named
for the first part plus `_set`), levels it to `--lufs` (-14 by default) and
writes `<name>_mastered.flac` beside it or in `--output-dir`. It never touches
the source and refuses to replace a master without `--overwrite`.

### Back up and restore

```bash
crate backup run --dry-run
crate backup run [--full]
crate restore list
crate restore run [SESSION_ID] --dry-run
crate restore run --from-backup --target /path/to/empty/dir
crate restore bare-metal --target /path/to/replacement --accept-replacement --dry-run
```

**Backup** mirrors the library to the rclone remote, archives changed files
by date and snapshots the database. `[backup]`'s `dest`, `archive_root` and
`db_dest_root` are each an rclone `remote:path`. The database part refuses
while rekordbox or its agent runs, so doctor reports the two ages apart.
Every run compares every file by size and modification time; `--full` lists
the remote folder by folder (most of an hour, independent of the recursive
listing), and doctor's `backup.full_comparison` asks for one every thirty
days. With the database outside the library root, the `share` folder beside
it (rekordbox's analysis files) is mirrored to `analysis-share/` under
`db_dest_root`.

**Restore** puts the database and its coupled state back to a recorded write
session. It does not undo values written into audio files. It asks
`restore.run.confirm`, and reaching past a later session that committed work
needs `--discard SESSION_ID` for each.

- `--from-backup` pulls the newest snapshot of this library's volume;
  `--snapshot STAMP` names one; `--snapshot-volume IDENTITY` accepts a
  snapshot taken before a drive was replaced, for that one restore;
  `--include-mirror` pulls the music too.
- `--target DIR` rehearses the database half elsewhere, rolling nothing back,
  and refuses the library or anything inside it. It puts `share` back beside
  the restored database; a live restore withholds it, so move it into place
  yourself, with rekordbox closed.
- `restore bare-metal` recovers mirror then database onto a new empty volume
  when the drive died. It refuses while the old library is readable, onto a
  target holding a database or the empty mount point the lost drive left, or
  with nobody at a terminal. If it stops in the database half, remove the
  database file and the companions the refusal names, nothing else, and run
  it again; a mirror half that stopped needs nothing removed. Afterwards run `crate doctor` and
  `crate setup --library-root PATH --volume-id ID` to record the new drive,
  then `crate converge`.

## Answering a gate

A gated verb exits with the gate's name, its options and a run id. Most gates
are **explicit**: only a separate `crate run decide` answers them, never `-d`
on the verb's own line.

```bash
crate run show RUN_ID
crate run decide RUN_ID GATE OPTION [--actor YOUR_NAME]
crate --run RUN_ID VERB ...          # continue the same run
crate run decide RUN_ID GATE OPTION --continue   # answer and continue in one
```

A fresh invocation without `--run` mints a new run, which meets the gate again.
Without `--actor` the answer is recorded as `cli` at a terminal and `session`
without one.

- A gate that shows a plan is answered only once its run has shown it. On a
  verb with two gates (organize, sync pair, intake land, export set, label
  playlists), answering the second early is refused as `gate-not-reached`.
- If the plan moves between the answer and the apply, the run refuses as stale
  and writes nothing. When the gate found the move, the refusal shows the new
  plan; an answer recorded after it applies that plan. Otherwise start a fresh
  run.
- A database writer's gate names other runs of the same verb open or answered
  in the last twelve hours (`gate-sibling-run`). It refuses nothing.
- Every gate offers `abort`, a recorded answer that ends the run with no
  further writes, except `sync.land.without-vocals` (`go` or `stop`) and the two
  `sync pair` gates (`apply` or `skip`).

| Gate | Go | Verb |
|---|---|---|
| `route.inbox.apply` * | apply | `route inbox` |
| `name.apply.confirm` * | apply | `name apply` |
| `intake.land.confirm` * | apply | `intake land`, xml bridge |
| `repair.paths.confirm` * | apply | `repair paths --apply` |
| `run.retire.confirm` * | apply | `run retire` |
| `profile.set.apply` * | apply | `profile set` |
| `sync.land.without-vocals` * | go (or stop) | `sync land` |
| `intake.land.native` | apply | `intake land`, database native |
| `intake.file.native` | apply | `intake file`, database native |
| `intake.shelve.native` | apply | `intake shelve` |
| `intake.inspiration.approve` | apply | `intake inspiration` |
| `intake.set.account.confirm` | apply | `intake set` |
| `tag.retag.confirm` | apply | `tag retag` |
| `tag.rows.confirm` | apply | `tag rows` |
| `tag.remap.confirm` | apply | `tag remap` |
| `tag.suggest.confirm` | apply | `tag suggest` |
| `taxonomy.upgrade.apply` | approve | `taxonomy upgrade` |
| `taxonomy.alias.apply` | approve | `taxonomy alias` |
| `taxonomy.folder.apply` | approve | `taxonomy folder` |
| `route.resort.apply` | apply | `route resort` |
| `adopt.apply.approve` | approve | `adopt apply` |
| `adopt.move.approve` | approve | `adopt move` |
| `inbox.rotate.approve` | approve | `inbox rotate` |
| `inbox.refill.approve` | apply | `inbox refill` |
| `inbox.analyzed.approve` | apply | `inbox analyzed` |
| `favorites.backfill.approve` | approve | `favorites backfill` |
| `favorites.refresh.approve` | approve | `favorites refresh` |
| `favorites.split.approve` | approve | `favorites split` |
| `favorites.order.approve` | approve | `favorites order` |
| `organize.rekordbox.approve` | approve | `organize`, rekordbox side |
| `organize.account.apply` | apply | `organize`, account side |
| `sync.all.favorites.confirm` | sync | `sync all` |
| `sync.favorites.confirm` | sync | `sync favorites` |
| `sync.mark.confirm` | apply | `sync mark` |
| `sync.unmark.confirm` | apply | `sync unmark` |
| `sync.pair.rekordbox` | apply (or skip) | `sync pair` |
| `sync.pair.account` | apply (or skip) | `sync pair` |
| `sync.twins.approve` | approve | `sync twins` |
| `sync.release.approve` | approve | `sync release` |
| `label.sync.confirm` | apply | `label sync --go` |
| `label.playlists.confirm` | apply | `label playlists` |
| `label.playlists.crawl` | crawl | `label playlists`, over 500 calls |
| `label.mark.confirm` | apply | `label mark` |
| `label.prune.confirm` | apply | `label prune` |
| `label.heard.confirm` | apply | `label heard` |
| `export.playlist.confirm` | export | `export playlist` |
| `export.prune.confirm` | apply | `export prune` |
| `export.set.confirm` | apply | `export set` |
| `export.set.rename` | apply | `export set --rename` |
| `export.archive.confirm` | apply | `export archive` |
| `delete.review.confirm` | trash | `delete review` |
| `repair.rows.confirm` | apply | `repair rows` |
| `repair.link.confirm` | apply | `repair link` |
| `tree.cutover.approve` | approve | `tree cutover` |
| `tree.revert.approve` | revert | `tree revert` |
| `rebuild.accept` | accept | `rebuild`, INBOX |
| `restore.run.confirm` | restore | `restore run` |
| `session.ack.backup` | acknowledged | `session ack` |
| `session.release.confirm` | release | `session release` |
| `write.cloudsync.unreadable` | proceed | any database writer |

\* Not explicit: also answered inline with `-d GATE=OPTION`.

`write.cloudsync.unreadable` fires when Cratekit cannot tell whether a cloud
sync client is also writing the library. Proceeding is a decision about a
second writer; treat "could not read" as unknown, not safe.

### Retiring old gates

```bash
crate run retire --older-than 7d
crate -d run.retire.confirm=apply run retire --older-than 7d
```

Answers `abort`, as `session`, on every open gate idle longer than the
threshold (`reports.open_gate_stale_days`, 7 by default), after one confirm.
Idle counts from the run's start or last resume. A gate with no `abort`, or
whose verb is gone, is kept and named. Queued jobs are untouched.

### The backup acknowledgment

Every database write needs a backup acknowledgment on record; it lasts twelve
hours. Run `crate doctor` first: it shows both backup ages and, on
`backup.acknowledgment`, whether one is on record and when it expires.

From a terminal:

```bash
crate session ack
crate run decide RUN_ID session.ack.backup acknowledged --actor YOUR_NAME
crate --run RUN_ID session ack
```

A session working for you, with no terminal, in one command:

```bash
crate session ack --as session
```

It mints only while both backup ages are under five days, and refuses
otherwise as `backup-acknowledgment-backup-too-old`; an acknowledgment already
valid is reported, not minted again. The record says which rule minted it,
`session-ages` or `terminal`.

## Safety

- **No beat grid, ever.** No tempo element, BPM tag, average BPM field or
  ANLZ grid, in any container. rekordbox does its own analysis.
- **The live database** is written only through the guarded write (see [How it
  works](#how-it-works)). Verbs that only read take a copy.
- **Files** are trashed only by `delete review`, to the system Trash.
  Renames go through `name apply` and `repair paths --apply`, behind gates,
  and `analyze run`, which renames each file it finishes to its Camelot head.
- **The account** is written behind explicit gates. Exports and label
  playlists add only; removals happen only where a verb names them on its
  gate (`export prune`, `label prune`, `label heard`, `sync pair`, organize's
  `root` and `mirror`).
- **Rollback**: `crate restore list` shows what a restore would undo.

### Using DEADCA7 beside Cratekit

DEADCA7 pushes playlists into one top level `DEADCA7` folder, with its cues,
grids and waveforms. Cratekit never writes into that folder (a write that
would is refused), never offers it a home in `organize`, and refuses a
taxonomy tree of that name. Doctor says whether DEADCA7 is installed, when it
last pushed, and warns when that push is newer than your last database backup:
run `crate backup run` then. Both tools need rekordbox closed; do not push
from DEADCA7 while a verb runs, or the verb's next commit refuses. A folder
named DEADCA7 below the top level is yours.

## When something refuses or stalls

Read the refusal's reason and remedy before retrying, then `crate doctor`.

| Symptom | Do |
|---|---|
| "Decision required" | `crate run show RUN_ID`. |
| A job that never moves | `crate job show JOB_ID`; queued work needs `crate job resume`. |
| A blocked job | `job show` gives the cause, usually a review item or a credential. |
| A resume that refuses the same way | `crate job cancel JOB_ID` and queue a fresh one. |
| `provider-call-ceiling` | The command hit the provider call ceiling (`[provider] calls_per_command`, 500). Run the printed command; `--calls N` raises it for one run, as `crate --calls N job resume JOB_ID`. |
| `rekordbox-absence-unconfirmed` | A process the check could not read, usually one still exiting. Wait, then continue with the printed `crate --run RUN_ID ...`. Inspect with `ps -p PID -o pid,stat,comm`. |
| `backup-acknowledgment-missing` | [The backup acknowledgment](#the-backup-acknowledgment). |
| `sync land` lists intake jobs left open | `crate job cancel --stale-days DAYS --dry-run`, then without `--dry-run`. A queued `crate organize` download is taken by the next new pass. |
| An unknown verb | `crate profile show`: its module is off. |
| A tree "unconverged" | `crate converge`, `crate rebuild`, `crate converge`. |
| A stale lock from a machine that is gone | `crate session release`. |

Exit codes by band:

| Code | Meaning |
|---|---|
| 0 | ok |
| 1, 2 | internal error, usage |
| 10, 11, 12 | decision required, decision stale, waiting on a person |
| 20 to 27 | the library refuses: busy, rekordbox open, unavailable, version pin, unconverged, unreadable, another writer, a missing prerequisite |
| 30, 31, 32 | this install: precondition, module unavailable, acknowledgment required |
| 40, 41, 42 | upstream: auth, unavailable, refused by policy |
| 50 | interrupted |

A cancelled job is its own state, never a failure.

## Where things live

| What | Where |
|---|---|
| Configuration | `config.toml` in the platform config folder (`~/Library/Application Support/cratekit/` on macOS; `CRATEKIT_CONFIG_DIR` overrides) |
| Job queue, provider pacing, ISRC answers | the installation's state folder (`CRATEKIT_STATE_DIR` overrides); doctor's `provider.isrc-cache` line names the ISRC file |
| Library state, active taxonomy, write sessions, snapshots | `.cratekit/` under the library root |
| Credentials | the OS keychain |
| Backups | the rclone remotes in `[backup]` |

The configuration is TOML. `crate setup` writes it. Its sections are
`[library]`, `[paths]`, `[profile]`, `[modules]` (one toggle per module, which
wins over the profile's preset), `[taxonomy]`, `[naming]`, `[acquisition]`,
`[analysis]`, `[rekordbox]`, `[backup]`, `[reports]`, `[outbound]`,
`[recognition]`, `[provider]` and `[labels]`. Every key, with its default
(required keys have none, and setup asks for each):

| Key | Default |
|---|---|
| `schema_version` | required (setup writes it) |
| `library.root` | required, the library folder on the music volume |
| `library.volume_id` | required, the volume's identity, never a mount path |
| `library.db_path` | required, the rekordbox database |
| `library.db_outside_root_acknowledged_on` | unset (the date you accepted a database outside the library root; unset refuses one there) |
| `library.music_dir` | `"Music"` |
| `library.processed_dir` | `"Processed_Tracks"` (where `intake shelve` files a batch) |
| `library.sets_dir` | `"Set_Recordings"` |
| `library.state_dirname` | `".cratekit"` |
| `library.location_prefix_map` | `[]` (setup offers a rule when rekordbox records paths under another base) |
| `paths.download_staging` | required, where downloads land first |
| `profile.name` | required, `slim`, `full` or `custom` |
| `modules.<module>` | unset (the profile decides; `true` or `false` overrides it) |
| `taxonomy.template` | `"default"` |
| `naming.lossy_marker` | `"[MP3]"` |
| `naming.path_budget_bytes` | 250 |
| `naming.filename_max_bytes` | 255 |
| `acquisition.adapter` | `"vendored"` (see [`adapters.md`](adapters.md)) |
| `acquisition.quality` | `"lossless"` |
| `acquisition.pacing_delay_s` | unset (the adapter's own pacing) |
| `acquisition.concurrency` | 1 |
| `acquisition.lossless_policy` | `"strict"` (or `"allow_lossy_marked"`, which marks every lossy file) |
| `analysis.jobs` | unset (probed from memory, never from a CPU count) |
| `analysis.energy_calibration` | `"auto"` (no verb reads it yet) |
| `analysis.tempo_floor` | 80 |
| `analysis.tempo_ceiling` | 160 |
| `analysis.drift_cut` | 1.5 |
| `rekordbox.pinned_pyrekordbox` | `"0.4.4"` |
| `rekordbox.pinned_db_version` | `"6000"` |
| `rekordbox.pinned_app_version` | unset (unset refuses every database write; setup proposes one) |
| `rekordbox.validated_on` | unset (the date the pin was confirmed against a real write) |
| `rekordbox.app_path` | unset |
| `backup.remote` | unset (read from the destinations) |
| `backup.dest` | unset, an rclone `remote:path` |
| `backup.archive_root` | unset, an rclone `remote:path` |
| `backup.db_dest_root` | unset, an rclone `remote:path` |
| `reports.intake_stale_days` | 30 |
| `reports.intake_expired_days` | 90 |
| `reports.open_gate_stale_days` | 7 |
| `outbound.export_stale_days` | 7 (past this age an export's plan says it is old; never a refusal) |
| `outbound.pair_skip_folders` | `["ARCHIVE"]` |
| `outbound.pair_order_every_pair` | false (only GIG READY pairs keep Tidal's order) |
| `recognition.host` | `"identify-us-west-2.acrcloud.com"` |
| `recognition.monthly_calls` | 1000 (a refusal past it, never a warning) |
| `provider.min_interval_s` | 1.0 |
| `provider.cooldown_s` | 900 |
| `provider.calls_per_command` | 500 |
| `provider.isrc_cache_days` | 30 (0 turns the ISRC cache off) |
| `labels.offer_per_sweep` | 10 |
| `labels.new_playlist_age_days` | 30 |

An ISRC answer is shared by every verb, so a rehearsal and the live run pay
for a lookup once. A copy run that redirects `CRATEKIT_STATE_DIR` should point
`CRATEKIT_ISRC_CACHE_DIR` at the live state folder.

## Working with an AI assistant

Twelve operator guides ship with the package, one per workflow area. Keep the
agent's workspace outside the Cratekit clone:

```bash
mkdir -p ~/cratekit-work
cp operator/AGENTS.md operator/CLAUDE.md ~/cratekit-work/
crate skills install --into ~/cratekit-work/.claude/skills
```

`crate skills install` with no `--into` writes to the agent skills folder in
your home directory, shared by every project. Run it again after upgrading;
it refreshes stale copies.

| The agent may | You do |
|---|---|
| run `doctor`, `status`, reports and audits | run anything that writes |
| read a refusal and name the remedy | answer a gate by name |
| propose the verbs and the order | record the backup acknowledgment once either backup is five days old |
| read back what a run reports | quit rekordbox and its agent |

## Going deeper

| For | Read |
|---|---|
| Which workflows have run for real | [`cutover.md`](cutover.md) |
| Signing in, switching downloader | [`adapters.md`](adapters.md) |
| A term that means something specific here | `CONCEPTS.md` |
| Known problems, recorded and not fixed | [`residual-findings.md`](residual-findings.md) |
| Past problems and their causes | `solutions/` |
| Working on Cratekit | [`DEVELOPING.md`](DEVELOPING.md), [`METHOD.md`](METHOD.md) |
