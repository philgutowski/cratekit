# Using Cratekit

How to run Cratekit day to day, in the order you will meet things. It assumes
the install and first run in the README are done and `crate doctor` reports no
failing check.

This guide describes the command line as it is built. When it disagrees with
`crate --help`, the help is right and this file is stale. Which workflows have
actually run on a real library is a separate question, answered by
[`cutover.md`](cutover.md), and the table under "Where it stands" is only a
summary of that file.

## How it works, in one picture

Cratekit touches your rekordbox library in exactly three ways, and the first two
never go near the live database.

```
                         reads only
  rekordbox --(export)--> collection XML file --------> crate reports, audits,
     |                    (a file you make by hand)     favourites sync, playlist export
     |
     |   you import by hand
     +<------------------- importable XML file <-------- crate intake and sync
     |                     (crate writes it, you load it)
     |
     |   guarded write, rekordbox closed, backup acknowledged
     +<------------------- the live database <---------- crate route, rebuild, restore,
                           (through one guarded layer)   metadata --apply
```

- **A collection export** is the XML file rekordbox writes when you export your
  collection (the File menu, Export Collection in xml format). Several verbs read
  one and never the live database. Cratekit records no location for it, so you
  pass the path each time, and a stale export answers every question confidently
  and wrongly. Export a fresh one when the answer matters.
- **An importable file** is what intake and sync produce for new tracks.
  Cratekit does not import it for you. You load it into rekordbox, export the
  collection again, and run `crate intake imported --export` with that export,
  which proves the import happened and puts the importable file away.
- **The guarded write** is the only path to the live database. It refuses unless
  the library volume is mounted and is the volume that was recorded, rekordbox and
  its background agent are both closed, the pinned versions match, and you have
  recorded a backup acknowledgment. It snapshots first and reads the result back
  afterward. Any one of those refusing stops the write.

Four words carry most of the rest.

- **Job.** Long work, such as a playlist intake, a tagging pass or a label
  sweep, is queued and handed back to you as a job identifier. The verb returns
  quickly. `crate job list` shows the queue, `crate job show ID` shows one job
  and why it is in its state, and `crate job resume ID` picks it up without
  repeating finished work.
- **Run.** One invocation's decision state, saved on disk so a decision can be
  answered later, from another terminal, after the process has exited.
- **Gate.** A named question a verb stops at before it writes. There is no
  `--yes` anywhere. A gate is answered by name, and the answer is recorded with
  who gave it.
- **Review item.** A single decision a person has to make, such as "is this
  remix the version I wanted". Verdicts are remembered, so you are never asked
  twice about the same thing.

Two habits follow from that design. Read a refusal instead of retrying it, since
every refusal names a reason and what to do about it. And put root options
before the verb, because they belong to the top level command. `--output json`
gives a machine readable answer, `--decision` answers a gate on the same line, and
`--run` continues a run that stopped at a gate:

```bash
crate --output json doctor
crate --decision route.inbox.apply=apply route inbox
crate --run RUN_ID route inbox
```

## Before every session

Every verb that writes needs the same conditions, so check them once up front.

1. Quit rekordbox, and quit its background agent too. Opening the app is the one
   thing that makes writing verbs refuse.
2. Mount the library volume.
3. Run the health check, and read the `fail` lines first. `note` lines are worth
   knowing and need no action.
4. Run the status verb, which reports open runs, per source sync state and any
   tree whose membership no longer matches the database.

```bash
crate doctor
crate status
```

A source that shows "no clean increment has completed" has simply never synced.

## Where it stands

Summary of [`cutover.md`](cutover.md) as of 2026-09-17. Fixes made after that
date are recorded in `RESTART-cratekit.md`. Treat a fix as unproven on the live
library until `cutover.md` says it was re-run there.

| Workflow | Last live run | State |
|---|---|---|
| Setup and doctor | 2026-09-16 | Live. |
| Backup, `backup run` | 2026-09-16 | Live. A restore rehearsal landed the database byte for byte, then the verb reported failure over a missing side file. Fixed on main, not re-run. |
| Vocal scoring and My Tags | 2026-09-17 | Live for one folder. The verb scores one folder per call, so a full library pass is hundreds of calls. |
| Playlist export, favourites sweep | 2026-09-17 | Live. Both are add only. The favourites listing read a fraction of the account, fixed since, not re-run. |
| Download, `acquire download` | 2026-09-16 | One real track, lossless, proven. Not yet lived on. |
| Playlist intake and harvest | 2026-09-17 | Ran live. Both resolve tracks and report, and neither downloads. |
| Label sweep | 2026-09-17 | 15 of 47 labels swept, 32 refused for want of a seed artist. A discovery fix has merged since and has not been measured live. |
| `sync all` | 2026-09-17 | Queued 18 playlists, 11 of them label debris. A swept playlist is recorded as done once resolved, not once acquired, and is not marked on the account. |
| Routing, tree flip, adopt, remove tracks, analyze, set builder, mastering, naming, tagging, path repair | none recorded | Covered by the test suite and by no live sitting yet. |

For anything in the last row, or anything marked "not re-run", do a small batch
first, confirm your backup is current, and check `crate restore list` afterward
so you know what a rollback would undo.

## Recipes

### Bring music in

Pick the verb by what you are holding.

```bash
crate intake playlist https://tidal.com/playlist/PLAYLIST_UUID
crate intake playlist favorites
crate intake file /path/to/one-track.aiff
crate intake set /path/to/recording.wav
crate intake identify /path/to/recording.wav
crate match run /path/to/tracklist.txt
```

- `intake playlist` reads a streaming playlist and reports each track as owned,
  offered or missing. It queues a job and does not download.
- `intake playlist favorites` does the same for every track hearted on the
  account, which answers whether each heart is in your library. Ownership is
  the same match rule a playlist gets, so a heart you hold in another version
  is offered for review rather than counted owned. Nothing is written to the
  account, no holding playlist is made, and a heart you acquire later simply
  reads owned on the next run. A listing that cannot be read in full refuses
  rather than reporting a short one.
- `intake file` shows a plan by default. It writes only when you also pass
  `--export` with the collection export to splice the track into. It then ends
  waiting on you the way `intake land` does, naming the file to import, and is
  settled the same way, with `crate intake imported`.
- `intake set` takes a recording on this machine, or the web address of a mix.
  An address is fetched with `yt-dlp` into a scratch folder outside the
  library, identified, and removed again, because a mix is input and not
  library material. Without `yt-dlp` it refuses and says how to install it.
  `intake identify` takes an address the same way.
- `intake identify` names the tracks in a recording and stops. It calls a paid
  recognition service, so it refuses before the first call if the recognition
  keys are not recorded.
- `match run` takes lines of `Artist - Title` and sorts each into matched,
  needs review or missing. Needs review means a different version of the track
  exists, such as a remix or an edit, and only you can say if it counts. Those
  become review items.

When a playlist job has finished, turn what it found missing into a list the
download step reads:

```bash
crate intake missing --job JOB_ID
```

It writes `intake-JOB_ID.list.json` into a `lists` folder under download
staging, or into the folder you name with `--out`, and prints the path and the
exact `acquire download` command to run next. Only missing tracks are listed.
Owned tracks, tracks offered for review, and tracks you deleted on purpose are
counted and left out. A job that is still running, failed or was cancelled is
refused rather than listed in part.

A finished `intake set` job lists the same way. A track recognised in a set
carries no provider id, so the verb asks the provider for its ISRC and lists the
track only when exactly one provider track carries that code. A track with no
ISRC, or one the provider files under no track or under several (a single, an
album cut and a compilation often share one), is never guessed at. It is
written to `intake-JOB_ID.unlisted.json` beside the list, with the reason above
each line, and reported as a failing line. If the provider cannot be reached
the verb refuses and writes nothing; run it again later.

That file is a text list, and a text list has its own route to a download:

```bash
crate intake missing --list PATH
```

`PATH` is the unlisted file above, or any tracklist of `Artist - Title` lines
you typed or transcribed from a screenshot. Every line is checked against the
library first, exactly as `match run` checks it, so a track you own is never
searched for. Each line that is still missing is searched for on the provider,
and the search only ever proposes. A line is listed on its own only when exactly
one track the provider returned matches it in artist, title and version. Two
matching tracks, or none with near misses beside it, are offered for review
with each candidate's score, and nothing is ever listed from a score:

```bash
crate review list --queue version-match --kind provider-candidate
crate review resolve ITEM_ID --verdict accepted --option TRACK_ID
```

Run the same `intake missing --list` again after answering, and the candidate
you accepted is listed. A rejected line is not searched for again until you
clear the answer with `crate review clear ITEM_ID`. A line the provider has
nothing for is reported as a failing line, never silently dropped. The list is
written as `NAME-found.list.json`, `NAME` being the input's own name, so it
never lands on the job's list.

A bootleg, a white label or an unreleased promo is not on the provider at all.
For those lines there is a second source search:

```bash
crate acquire fallback PATH
```

It reads the same kind of list, checks it against the library the same way,
and searches SoundCloud and then YouTube for each line still missing. Run
`intake missing --list` first and hand this the lines it could not route: a
line carrying the provider's own id, or with a provider candidate waiting or
accepted in review, is left alone, and a line the provider would list on its
own is not something this verb can see. What it finds is offered for review,
best match first, and nothing is picked or downloaded:

```bash
crate review list --queue fallback-source --kind fallback-candidate
crate review resolve ITEM_ID --verdict accepted --option URL
```

A second run searches nothing it already offered. It needs `yt-dlp`, and says
how to install it when it is missing. If a search fails part way it stops and
names every line it had already offered, and the next run carries on from
there. An accepted upload is reported with its address; downloading it is not
built yet.

A `crate sync all` pass queues one playlist job per new playlist, and its output
ends with the command that lists the whole pass at once:

```bash
crate intake missing --run RUN_ID
```

It writes one list for every playlist job the pass queued on this library,
named for the run, so the pass downloads and lands as one batch. A track two
playlists share is listed once, and the list's manifest names both playlists.
A job still running refuses the whole run. A job that failed or was cancelled
is named and refuses the run too, unless you pass `--skip-failed`, which lists
the rest and reports what it left out as a failing line. The output names the
`--name` to give `intake land`, beside the `--export` it always needs, so the
landed batch carries the run's name.

Downloading is its own step. `crate acquire download LIST` fetches tracks into
the download staging folder through the configured adapter, paced so the account
is not blocked, and `crate acquire audit` reports files that break the lossless
policy. What arrived then needs tagging, naming, landing and filing, in this
order. `tag folder` writes genre and album art to the files only. `name apply`
rebuilds filenames from your template. `intake land` moves the staged files into
your library and writes one importable file naming every one of them, which you
import into rekordbox. `intake imported` reads a collection export taken after
that import and proves it happened. `route inbox` files the intake folder into
your taxonomy, and `route pending` files the landed tracks once a tree has cut
over to the database.

```bash
crate tag folder /path/to/staging
crate name apply --root /path/to/staging
crate intake land --export /path/to/collection-export.xml
crate intake imported --export /path/to/export-taken-after-the-import.xml
crate route inbox
crate route pending
```

`intake land` reads download staging unless you name another folder. The files go
to a new folder under your music folder, named for the run unless you pass
`--name`, and the importable file is written beside the library as
`NAME_inboxed.xml`. It never replaces a file already in the library: a file whose
name is taken stays in staging and the run says so. Two landings under one
`--name` never run at once: the second is refused with nothing moved. If the
first one then lands, the name is taken, so give the second another. Staging has to be on the same
volume as the library, because a move there is a rename and a copy is refused. The
run ends waiting on you, naming the file to import.

Once you have imported it, export your collection again and run
`crate intake imported --export` with that new export. It looks for every landed
file in the export. When they are all there, the import is proven: the importable
file is renamed to `NAME_inboxed.xml.imported`, which you can delete whenever you
like, and the landing stops counting as unfinished. When any are missing it
changes nothing and names them, so an export taken before the import, or an
import that skipped a track, is never mistaken for a finished one. The importable
file itself is refused as the export, since it names every landed track whether or
not rekordbox imported it. Run with no landing waiting, it does nothing, and then
it needs no `--export`. A landing made before this verb existed recorded no
importable file, so its import is proven the same way and the file is yours to
remove once it is.

Until a tree has cut over, `crate route pending` has nothing it can place and
says so. It does not confirm an import.

Tracks you acquired from a label can be filed under that label in the same file.
`crate label approved` writes a manifest beside its list, a file ending in
`.manifest.json` that records which label and year each track came from. Pass it
with `--manifest` and every label track that landed is also listed under
`Record Labels`, in a folder for the label and a playlist for each year:

```bash
crate intake land --export /path/to/collection-export.xml --manifest /path/to/label-approved-NAME.manifest.json
```

The gate screen names the manifest and every label playlist it lists, so you
see what will be filed before you answer. A manifest changed after you read the
plan makes the answer stale, the way a changed folder does.

A landed file is tied to its manifest row by artist, title and version, the same
rule `acquire match` uses. A label track that no file in this landing matches is
named in a warning, and this landing files it under no label. That warning is
expected for a track you landed earlier, which keeps the playlist that landing
gave it, and for a download that never arrived. An export that already holds a
label's folder is added to, never doubled, so landing the rest of a label later
is safe. An export holding the same label folder twice is refused before anything
moves: merge the two in rekordbox and export again.

Once a sync pass has landed, `crate sync mark` tells the streaming account which
playlists it finished, by putting `DOWNLOADED ` in front of their names:

```bash
crate sync mark --xml /path/to/library/RUN_synced_inboxed.xml
```

Give it the importable file `intake land` wrote for the pass, under the name
`intake missing --run` told you to land it as, since the name is how the pass is
found. If you ran `intake imported` first, the file now ends in `.imported`, and
that name works the same. It reads what each playlist's job reported, and plans a rename only for a
playlist whose every track is now in your library, counting a track you have
since deleted on purpose as settled. A playlist with a track still missing, or
one the pass offered you for review and you have not got, is left alone and the
track is named. Nothing is renamed until you answer the gate, a playlist whose name
changed since the plan is skipped, and a playlist already carrying the prefix is
never prefixed twice. If a rename fails part way, the run names the playlists it
had already renamed, and running it again picks up the rest. A rename is a
change to your account that this tool does not undo.

`name apply`, `intake land` and `route inbox` each build a plan and stop at a
gate before they write. Run once to read the plan, then answer the gate. See
"Answering a gate". A plan is bound to the folder as it was, so if a file lands
between reading the plan and answering, the answer is refused as stale and you
plan again.

### Follow record labels

```bash
crate label registry
crate label registry add "Some Label" --match "Some Label Rec"
crate label harvest https://tidal.com/playlist/PLAYLIST_UUID
crate label registry adopt
crate label import "Some Label"
crate sync labels
crate review list --queue label-release
crate review resolve ITEM_ID --verdict accepted --actor YOUR_NAME
crate label approved
```

`label registry` lists who you follow. The registry records nothing about what has
been pulled. A
label's identifier is made once, when you add it, and the record of what has been
pulled hangs off that identifier. To change how a label is displayed, use
`label registry rename`. Removing and re-adding under a new spelling makes the
next sync treat the whole catalogue as new. `harvest` offers the labels behind a
playlist for review and adds and downloads nothing. Accept the ones you want in
review, then `label registry adopt` adds each accepted label the registry does
not already hold, under any spelling of its name, and reports the rest as
already held. Running it again adds nothing new. A sweep proposes releases into the
review queue rather than taking them, and a rejection is remembered until you
clear it.

`label approved` is what makes an accepted release acquirable. It reads every
release you accepted, asks the provider for its tracks again, and writes the
ones your library does not hold into a list under the `lists` folder in download
staging, or the folder you name with `--out`. It prints the path and the exact
`acquire download` command to run next. Beside the list it writes a manifest
recording the label, the year and the release each track came from. Tracks you
own are left out, so you can run it after every review sitting and it lists only
what is still owed. Owned means landed in the library, not listed or staged, so
a list you have not downloaded yet is superseded by the next one, which holds
everything the earlier one did. Download the newest and ignore the older, or
you fetch the same tracks twice. A release the provider has withdrawn is reported by name as
a failing line and the other releases are still listed. A track you hold in
another version becomes a review question, and is listed on a later run once you
answer it.

### Sync from streaming

```bash
crate status
crate sync all --export /path/to/collection-export.xml
crate job list --state queued --state blocked
crate job resume JOB_ID
```

`sync all` queues each enabled source's own increment under one shared run and
returns almost at once. That is the design, not a failure. Nothing has run yet.
Resume the jobs it names, and every source appends to one importable file
instead of one per source. Each source keeps a bookmark (its watermark) that
moves only after a pass in which every item finished, so a partial failure is
covered again next time. The favourites source needs the export, because it never
reads the live database, and it asks one gate before anything is queued.

`crate sync favorites` hearts the library's own favourites on the account, and
that is the whole of what it writes. It reads the favourites playlist out of a
collection export, matches each track on the service, and hearts the ones the
account does not already hold. It changes nothing in the library: no colour, no
Favorite tag and no playlist membership is written locally, and the pass that
queues the sweep says so in its own report, before any heart is written. That is
the pass to read it on: a resume runs detached and its own report goes to the
job's log under the queue root rather than to the terminal that started it.
Hearts the library does not own reach it the other way, through
`crate intake playlist favorites`, which queues them for acquisition. Nothing
un-hearts or un-colours, on either side.

### Publish a playlist

```bash
crate --decision export.playlist.confirm=export \
  export playlist PLAYLIST_KEY --export /path/to/collection-export.xml
```

Give the stable identifier of the library playlist, never its title. Export is
add only. Tracks the service cannot match are reported, so read the report and
not just the count. Exporting the same playlist again updates the remote playlist
Cratekit already made instead of creating a second.

### Keep the library tidy

```bash
crate route unplaced
crate audit coverage /path/to/export.xml
crate audit duplicates /path/to/export.xml
crate report library /path/to/export.xml
crate report intake-aging /path/to/export.xml
crate repair paths
crate route resort
crate converge
```

`route unplaced` lists tracks no tree files, and `audit coverage` asks the same
question from an export. `audit duplicates` never deletes. Run `route resort`
after a genre or energy change, and `converge` to check that each tree matches
the database. Reports and audits are read only. `repair paths` proposes a new location for each
row whose file has moved, and you accept or reject each one with
`crate review resolve`. A wrong repair points a row at somebody else's file, so
nothing is inferred. `converge` reports and never repairs. If a tree has fallen
out of step, `crate rebuild --tree TREE_ID --actor YOUR_NAME` is the only way to
clear it.

Removing files is deliberately slow. `crate delete review` offers the files behind
rows you removed in rekordbox, and confirmed ones go to the system Trash and
nowhere else. `crate tombstone list` shows what was removed and lets you lift one
so that version can be acquired again.

### Analyse audio and score vocals

```bash
crate analyze run /path/to/staging
crate analyze vocals /path/to/one-folder
crate metadata mytags-vocals
crate metadata mytags-vocals --apply
```

The first `metadata` line shows the plan only. Adding `--apply` writes, and needs
the backup acknowledgment.

Analysis needs the `analysis` extra and vocals needs the `vocals` extra, both in
the README. Cratekit never writes a beat grid, a tempo element or an average BPM
field, in any container, and no flag turns that on. The vocal scorer takes one
folder per call. `analyze calibrate` and `analyze restamp` fit a threshold and
carry it across the back catalogue.

### Build a set, master a recording

```bash
crate setbuild /path/under/the/library/anchor-track.aiff --count 8 --role after
crate master /path/to/recording.wav --output-dir /path/to/out
```

`setbuild` ranks tracks you own that are compatible in key and energy with the
anchor, and needs no network. `master` levels a set recording and encodes it to
lossless, and never touches the source.

### Back up and restore

```bash
crate backup run --dry-run
crate backup run
crate restore list
crate restore run SESSION_ID --dry-run
crate restore run --from-backup --target /path/to/empty/dir
```

Backup copies the library to the rclone remote named under `[backup]` in the
config, keeps a dated archive of changed files, and snapshots the database. The
database portion refuses while rekordbox or its agent is running, so a backup
taken with the app open covers the music and not the database. Doctor reports each
portion's age separately for that reason. Use `--dry-run` first, since it walks
the whole plan and copies nothing.

A restore puts the database and the state coupled to it back to a recorded write
session. It does not put back values written into audio files, so genre tags
written by an adoption are not undone. It needs its own confirmation, and if it
reaches back past a later session that committed work, you have to name each of
those sessions with `--discard`. `crate restore list` is free and opens no
session.

`--target` rehearses the database half somewhere the live library is not, which
is how you find out a restore works before you need one. It takes the database
from the off-machine snapshot, needs `--from-backup`, rolls no session back, and
refuses a directory that is the library, holds it, sits inside it, or would land
the database on the live file. The gates are the live restore's: the backup
acknowledgment, the library lock, and rekordbox closed.

## Answering a gate

A gated verb exits asking for a decision and prints the gate's name, its options
and a run identifier. Answer it on the same line, or later, from anywhere. On the
same line:

```bash
crate --decision route.inbox.apply=apply route inbox
```

Or afterwards, from any terminal:

```bash
crate run show RUN_ID
crate run decide RUN_ID route.inbox.apply apply --actor YOUR_NAME
crate --run RUN_ID route inbox
```

The last line matters. Starting a fresh invocation mints a new run, which meets
the same gate with nothing recorded and refuses again. Gates you will meet:

| Gate | Go option | Verb |
|---|---|---|
| `route.inbox.apply` | apply | `route inbox` |
| `name.apply.confirm` | apply | `name apply` |
| `intake.land.confirm` | apply | `intake land` |
| `tag.retag.confirm` | apply | `tag retag` |
| `sync.favorites.confirm` | sync | `sync favorites` |
| `sync.all.favorites.confirm` | sync | `sync all` |
| `sync.mark.confirm` | apply | `sync mark` |
| `export.playlist.confirm` | export | `export playlist` |
| `delete.review.confirm` | trash | `delete review` |
| `adopt.apply.approve` | approve | `adopt apply` |
| `restore.run.confirm` | restore | `restore run` |
| `session.ack.backup` | acknowledged | `session ack` |
| `write.cloudsync.unreadable` | proceed | any verb that writes |

Every gate also offers `abort`. An abort is a recorded answer and not a failure,
and the verb returns its plan with a no-op outcome. Read the last gate in the
table before answering it. It fires when Cratekit cannot tell whether a
cloud sync client is also touching the library, and proceeding is a decision about
a second writer. Treat "could not read" as unknown, not as safe.

### The backup acknowledgment

Before any write, Cratekit wants proof that you have a current backup, and the
proof has to come from you. The acknowledgment lasts twelve hours. A session
working for you cannot mint one, and answering a gate is not the same act.
From a terminal you are sitting at:

```bash
crate session ack
crate run decide RUN_ID session.ack.backup acknowledged --actor YOUR_NAME
crate --run RUN_ID session ack
```

The gate asks whether the database and the music files are backed up, so run
`crate doctor` first and read the two backup ages. If a verb refuses because the
acknowledgment is missing or has expired, this is the fix.

## When something refuses or stalls

| Symptom | Ask |
|---|---|
| Any refusal | Read its reason and remedy. Then run `crate doctor`. |
| "Decision required" | `crate run show RUN_ID` names the gate and its options. |
| A job that never moves | `crate job show JOB_ID`. Queued work needs `crate job resume`. |
| A blocked job | `job show` carries the cause, usually a review decision or a credential. |
| A resume that refuses the same way each time | Cancel it with `crate job cancel` and queue a fresh one. |
| A verb the parser has never heard of | `crate profile show`. A module the profile leaves out has no verbs at all. |
| A tree "unconverged" | `crate converge`, then `crate rebuild`, then `crate converge` again. |
| A stale lock from a machine that is gone | `crate session release`, explicitly. |

A cancelled job is its own state and is never counted as a failure.

## Credentials

Credentials live in the operating system keychain (macOS's built in password
store), never in the config file, and `crate doctor` reports which are recorded.
There are three.

- `provider-session` is the streaming account session used to list and download.
- `identify-key` and `identify-signing-key` are the recognition service's access
  key and signing value, used only by identification.

`crate login NAME --from-file PATH` records one. It refuses a value on the
command line, since that would sit in your shell history and in the process list
for every account on the machine.

Signing in to the streaming account is two commands, because obtaining a session
is an act at a browser and the vendored downloader owns that conversation. The
full procedure, and why the session has to be the PKCE kind or every download
quietly comes back lossy, is in [`adapters.md`](adapters.md) under "Authorising
the provider". Delete the plaintext token file once it is in the keychain.

## Where things live

| What | Where |
|---|---|
| Configuration | `~/Library/Application Support/cratekit/config.toml` |
| Library state, active taxonomy, write sessions and snapshots | `.cratekit/` under the library root |
| Credentials | the OS keychain |
| Backups | the rclone remote named in `[backup]` |

You never need to open a run or job record by hand. `crate status`,
`crate run show` and `crate job show` read them for you.

The configuration is TOML (a plain text settings format) with `[library]`,
`[backup]`, `[acquisition]`, `[naming]`, `[profile]`, `[rekordbox]` and
`[taxonomy]` sections. `crate setup` writes it and can be re-run safely. It
keeps every answer you already gave unless you pass a flag to change one, and it
ends by running doctor.

The `[profile]` name decides which verbs exist. `crate profile show` lists what
is on, and `crate profile set slim|full|custom` changes only that.

## Working with an AI assistant

Twelve short guides ship with the package, one per workflow area, covering the
recipes above. They are optional, since every workflow runs from the command line
without them. They exist so an agent working beside you knows the order and the
traps.

The workspace is a folder of your own, outside the Cratekit clone, because that
clone's instructions are about building the product rather than running it. The
repository ships the template. From inside the clone:

```bash
mkdir -p ~/cratekit-work
cp operator/AGENTS.md operator/CLAUDE.md ~/cratekit-work/
crate skills install --into ~/cratekit-work/.claude/skills
```

Start the agent in that folder. `AGENTS.md` points at `CLAUDE.md`, which is the
operator contract, and the split it draws is the one this guide already
describes:

| The agent may | You do |
|---|---|
| run `doctor`, `status`, reports and audits | run anything that writes |
| read a refusal and name the remedy | answer a gate by name |
| propose the verbs and the order | record the backup acknowledgment |
| read back what a run reports it did | quit rekordbox and its agent |

The right column is not a convention anybody agreed to be polite about.
`crate session ack` refuses an acknowledgment from a session working on your
behalf, and every writing verb refuses while rekordbox or its background agent is
running, so neither is a thing an agent can do for you even when asked.

Installing to the default location instead puts the guides where an agent finds
them for every project on the machine, which is worth avoiding if you keep other
skills there:

```bash
crate skills install
```

Run whichever form you chose again after updating Cratekit. Each copy carries the
version that wrote it, so the verb reports which guides were stale and refreshes
them in the same run.

## Going deeper

| For | Read |
|---|---|
| Which workflows have run for real | [`cutover.md`](cutover.md) |
| What is verified right now | `RESTART-cratekit.md` |
| Signing in, switching downloader | [`adapters.md`](adapters.md) |
| A term that means something specific here | `CONCEPTS.md` |
| Known problems, recorded and not yet fixed | [`residual-findings.md`](residual-findings.md) |
| Past problems and their causes | `solutions/` |
| Setting up to work on Cratekit | [`DEVELOPING.md`](DEVELOPING.md) |
| Working on Cratekit itself | [`METHOD.md`](METHOD.md) and [`BOARD.md`](BOARD.md) |
