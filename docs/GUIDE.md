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
  Cratekit does not import it for you. You load it into rekordbox, then run
  `crate route pending` so the tracks get filed once their rows exist.
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
before the verb, because they belong to the top level command:

```bash
crate --output json doctor          # machine readable answer
crate --decision route.inbox.apply=apply route inbox
crate --run RUN_ID route inbox      # continue a run that stopped at a gate
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
crate intake file /path/to/one-track.aiff
crate intake set /path/to/recording.wav
crate intake identify /path/to/recording.wav
crate match run /path/to/tracklist.txt
```

- `intake playlist` reads a streaming playlist and reports each track as owned,
  offered or missing. It queues a job and does not download.
- `intake file` shows a plan by default. It writes only when you also pass
  `--export` with the collection export to splice the track into.
- `intake set` takes a recording on this machine. A mix URL is not fetched by
  this build.
- `intake identify` names the tracks in a recording and stops. It calls a paid
  recognition service, so it refuses before the first call if the recognition
  keys are not recorded.
- `match run` takes lines of `Artist - Title` and sorts each into matched,
  needs review or missing. Needs review means a different version of the track
  exists, such as a remix or an edit, and only you can say if it counts. Those
  become review items.

Downloading is its own step. `crate acquire download LIST` fetches tracks into
the download staging folder through the configured adapter, paced so the account
is not blocked, and `crate acquire audit` reports files that break the lossless
policy. What arrived then needs tagging, naming and filing, in this order.

```bash
crate tag folder /path/to/staging      # genre and album art, files only
crate name apply                       # rebuilds filenames from your template
crate route inbox                      # files the intake folder into your taxonomy
crate route pending                    # after you have imported, files the rest
```

`name apply` and `route inbox` each build a plan and stop at a gate before they
write. Run once to read the plan, then answer the gate. See "Answering a gate".
A plan is bound to the folder as it was, so if a file lands between reading the
plan and answering, the answer is refused as stale and you plan again.

### Follow record labels

```bash
crate label registry                                 # list who you follow
crate label registry add "Some Label" --match "Some Label Rec"
crate label harvest https://tidal.com/playlist/PLAYLIST_UUID
crate label import "Some Label"
crate sync labels
crate review list --queue label-release
crate review resolve ITEM_ID --verdict accepted --actor YOUR_NAME
```

The registry records who you follow and nothing about what has been pulled. A
label's identifier is made once, when you add it, and the record of what has been
pulled hangs off that identifier. To change how a label is displayed, use
`label registry rename`. Removing and re-adding under a new spelling makes the
next sync treat the whole catalogue as new. `harvest` lists the labels behind a
playlist and adds and downloads nothing. A sweep proposes releases into the
review queue rather than taking them, and a rejection is remembered until you
clear it.

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

Favourites are meant to move both ways and never remove. Hearts on the account
become a colour, a Favorite tag and playlist membership locally, and coloured
tracks are hearted back on the account. Nothing un-hearts or un-colours. At the
last live sitting the hearting half worked and the colour write was still
unbound, so read what the run reports it did.

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
crate route unplaced                              # tracks no tree files
crate audit coverage /path/to/export.xml          # same idea, from an export
crate audit duplicates /path/to/export.xml        # never deletes
crate report library /path/to/export.xml
crate report intake-aging /path/to/export.xml
crate repair paths                                # proposes, never applies
crate route resort                                # after a genre or energy change
crate converge                                    # does each tree match the database
```

Reports and audits are read only. `repair paths` proposes a new location for each
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
crate metadata mytags-vocals            # plan only
crate metadata mytags-vocals --apply    # writes, needs the acknowledgment
```

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

## Answering a gate

A gated verb exits asking for a decision and prints the gate's name, its options
and a run identifier. Answer it on the same line, or later, from anywhere.

```bash
# on the invocation
crate --decision route.inbox.apply=apply route inbox

# or afterwards
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
| `tag.retag.confirm` | apply | `tag retag` |
| `sync.favorites.confirm` | sync | `sync favorites` |
| `sync.all.favorites.confirm` | sync | `sync all` |
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

## Operator skills

Twelve short guides ship with the package, covering the workflow areas above.
They are optional, since every workflow runs from the command line without them.
They exist so an AI coding agent working beside you knows the order and the traps.

```bash
crate skills install
```

## Going deeper

| For | Read |
|---|---|
| Which workflows have run for real | [`cutover.md`](cutover.md) |
| What is verified right now | `RESTART-cratekit.md` |
| Signing in, switching downloader | [`adapters.md`](adapters.md) |
| A term that means something specific here | `CONCEPTS.md` |
| Known problems, recorded and not yet fixed | [`residual-findings.md`](residual-findings.md) |
| Past problems and their causes | `solutions/` |
| Working on Cratekit itself | [`METHOD.md`](METHOD.md) and [`BOARD.md`](BOARD.md) |
