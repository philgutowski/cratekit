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
  and wrongly. Export a fresh one when the answer matters. With rekordbox closed,
  `crate export collection FILE` writes one from a copy of the database, so
  rekordbox's menu is not the only source. See "Take a collection export" below.
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
  sweep, is queued and handed back to you as a job identifier. Most verbs
  return quickly. `crate job list` shows the queue, one line per job with its
  verb, its state and how many of its items are settled, `crate job show ID` shows
  one job and why it is in its state, and `crate job resume ID` picks it up
  without repeating finished work. Three verbs of the acquisition tail, `tag
  folder`, `analyze run` and `analyze restamp`, queue their job and then work
  through it before they return, so each step is one command. Stop one with
  Ctrl-C and its answer names the `--job` command that finishes the rest; pass
  `--queue-only` to have it queue and return like the others. An intake job
  names the playlist it was made for in both `job list` and `job show`. An
  open intake job holds its playlist out of every sync pass, so an old one
  left queued keeps that playlist's new music out until it is driven or
  cancelled: `crate job cancel --stale-days 30 --dry-run` lists every queued
  intake job queued more than 30 days ago, with its playlist, age, track count
  and what cancelling it frees, and the same command without `--dry-run`
  cancels them. It never touches a running job, and of several open jobs
  holding exactly the same tracks it keeps the newest and says so.
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

Open gates that have sat idle for more than a week are one line rather than one
line each: how many, the dates they span, and the command that retires them,
`crate run retire --older-than 7d`. Newer gates are listed one by one. The week
is `reports.open_gate_stale_days` in the configuration file. Doctor's
`runs.open-gates` note lists each run that has sat at a gate for more than a
day, with its verb, gate and age, and never fails the report.

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

### Take a collection export

```bash
crate export collection /path/to/collection-2026-09-29.xml
```

Quit rekordbox first. The verb copies the database, reads the copy, and writes
the export to the file you name. It never opens the live database and never
writes to it, and it refuses while rekordbox or its background agent is running,
because a copy taken under a live application is missing whatever was mid write.

- It never replaces a file. Name one that does not exist yet.
- A name ending in `_inboxed.xml`, `_synced.xml` or `_favorites.xml` is refused,
  since that is how an importable file is named and the verbs that read an export
  would refuse this one.
- The file is what the verbs that take `--export` read, and it is not a backup.
  It carries no tempo, no beat grid and no cue points. Every track is written
  with the tempo rekordbox uses for a track it has not analysed.
- Smart playlists are left out, because the database stores their rule and not
  their tracks. The report counts them and names them.
- The first line after the XML declaration says Cratekit wrote the file, so it
  can be told from one rekordbox exported.

An export is a picture of the database at the moment it was written. Take a new
one after anything writes the database, an import included.

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
  settled the same way, with `crate intake imported`. Once your intake tree
  has cut over to the database it takes no export and refuses one: it plans
  one collection row for the file where it sits and one playlist under your
  INBOX folder, named for the file, and asks
  `intake.file.native`, which is answered by a separate `crate run decide`.
  The file is not moved, nothing about the audio is written, and the row
  awaits an analysis you ask rekordbox for, as a native landing's rows do. On
  that path the file has to be inside your library, since a row for a file
  outside it could not be matched against the collection again.
- `intake set` takes a recording on this machine, or the web address of a mix.
  An address is fetched with `yt-dlp` into a scratch folder outside the
  library, identified, and removed again, because a mix is input and not
  library material. Without `yt-dlp` it refuses and says how to install it.
  `intake identify` takes an address the same way.
- `intake identify` names the tracks in a recording and stops. It calls a paid
  recognition service, so it refuses before the first call if the recognition
  keys are not recorded.
- A recording longer than one recognition run's bound, about two hours and
  forty minutes, is identified in even parts, up to three, and is still one
  set: one tracklist, one job, one batch. Both verbs say so with a
  `recognition-in-parts` note. The month's bound is checked over the whole
  recording before the first call, and a file longer than three parts is
  refused as not one set.
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
`--pass` to give `intake land`, and says that the landing takes `--export`
while your intake tree is on the xml bridge and no export once it is database
native. The pass names the importable file, which is how `sync mark` later finds
the run, and the batch itself is named for the date and the playlists.

Downloading is its own step. `crate acquire download LIST` fetches tracks into
the download staging folder through the configured adapter, paced so the account
is not blocked, and `crate acquire audit` reports files that break the lossless
policy. A track the policy refuses for good, such as one offered lossy only, or
one the provider no longer has, is skipped and named in an `acquire-refused`
warning, and a download whose only misses are those ends ok; any other failure
still fails it. What arrived then needs tagging, naming, landing and filing, in
this order. `tag folder` writes genre and album art to the files only. `name apply`
rebuilds filenames from your template. `intake land` moves the staged files into
your library and writes one importable file naming every one of them, which you
import into rekordbox. `intake imported` reads a collection export taken after
that import and proves it happened. `route inbox` files the intake folder into
your taxonomy, and `route pending` files the landed tracks once a tree has cut
over to the database.

A `--root` is read against your library root when it is not a full path, so
`--root Downloads` is the library's Downloads folder wherever your shell stands,
and a root with no folder there is refused naming the path it tried.

```bash
crate tag folder /path/to/staging
crate name apply --root /path/to/staging
crate intake land --export /path/to/collection-export.xml
crate intake imported --export /path/to/export-taken-after-the-import.xml
crate route inbox
crate route pending
```

`tag folder` leaves a file with no genre when no catalogue that answers knows
the track, and some never answer here: Traxsource and Bandcamp refuse every
search with a bot check. `crate tag guess` gives each such file a genre from
what sits beside it: the same artist's other tracks, in your library and in
the folder, and, with `--pass`, the playlist on your account the pass
downloaded it for, which the catalogues mostly did tag. The weighing and its
bands are `tag suggest`'s, and a playlist counts as one voice
however long it is, so three tracks by the artist outweigh a long playlist of
another genre. Every guess is written, whatever its band; a tie is written as
the genre the artist's tracks weigh most, then the first by name, and named in
the report so you can check it. A file nothing votes for keeps no genre and is
named. A file that already carries a genre is never changed. The report gives
how many of the folder's files carried a genre before and after, and names any
word on a file your taxonomy has no folder for, offering to save it as an alias
of one of your genres or to make it a genre folder of its own. `--report`
writes nothing and says what a run would write, which is how a folder that has
already landed is measured. The passes below run it for you, right after `tag
folder`.

```bash
crate tag guess /path/to/staging --pass PASS
crate tag guess /path/to/staging --report
```

Each word `tag folder` or `tag guess` names that your taxonomy has no folder for
is answered in one command, either way, save the one kind named below. `crate
taxonomy alias` saves the word as
an alias of one of your genre folders, so a catalogue that gives it again is
tagged as that genre, and retags every audio file under your library root whose
one genre is the word, in any case; `--folder` retags only the files under one
folder. A file carrying the word beside another genre is left and named. Then
`crate tag rows` brings the rows into line and `crate route resort` files the
tracks. `crate taxonomy folder` makes the word a genre folder of its own under
BY GENRE + ENERGY, with energy bands, so the files already carrying it file
there at the next `crate route resort` and nothing is retagged. It takes the
family, tempo window and rating of the folder the word's tracks are filed in
now, or of the one `--like` names. Both edit your taxonomy copy behind an
explicit gate, keep the copy as it was beside it under a dated name, and refuse
a word the taxonomy treats as too coarse to be a genre, such as `Electronic`, a
word it already files, and a genre it does not declare, writing nothing.

One kind of word takes one answer only: a genre folder's own name in another
case, such as `breaks / d&b / dubstep`. Rekordbox folders are matched by their
exact name, so a file carrying it is filed by a keyword or the fallback until
it is retagged. `crate taxonomy alias "breaks / d&b / dubstep" "Breaks / D&B /
Dubstep"` retags those files to the folder's exact name and changes nothing in
your taxonomy, and the warning names that command for you. An alias to any
other folder is refused, since it would retag the files already carrying the
exact name too, and so is a folder of its own. Where the folder's own name does
not file a track by itself, as with `nonelectronic` and the NonElectronic
folder, which files each track by the track's own genre, neither verb takes the
word, and the refusal says to retag each file with the genre it means.

```bash
crate taxonomy alias "Latin Electronic" "Afro House"
crate taxonomy folder "Latin Electronic" --like "Afro House"
```

`intake land` reads download staging unless you name another folder. The files go
to a new folder under your music folder, and the batch playlist under INBOX takes
the same name. Unless you pass `--name`, that name is the landing's date and what
the files came from, read from what was queued rather than typed:

| What the landing is handed | The batch is named |
|---|---|
| a `--manifest` whose label rows name one label | `2026-10-03 Sudbeat` |
| a `--manifest` naming several labels | `2026-10-03 Labels` |
| a `--pass` whose jobs listed account playlists | `2026-10-03 Tidal playlists` |
| a `--pass` whose jobs listed your hearts | `2026-10-03 Favorites` |
| a `--pass` whose jobs listed a set | `2026-10-03 Set` |
| a `--pass` of more than one kind | `2026-10-03 Tidal playlists and Favorites` |
| neither | `2026-10-03 Downloads` |

A second landing on the same day from the same source gets ` 2`, the next ` 3`,
so two batches never share a playlist.

A `--pass` that swept playlists you made on the account also gives each of them
its own playlist under INBOX, beside the batch, named as on the account with the
landing's date at the end: `Lisa_10_27_26 2026-10-27`. INBOX stays flat, and the
date says which pass brought each one. A playlist landed before this rule keeps
the name it had, and `inbox rotate` ages it out as before. The importable file is written beside the
library as `PASS_inboxed.xml` when you pass `--pass`, `NAME_inboxed.xml` when you
pass only `--name`, and is named for the landing's own run otherwise. That name
is what `sync mark`, `label mark` and `export archive` read, so keep the one the
earlier step printed. It never replaces a file already in the library: a file whose
name is taken stays in staging and the run says so. Two landings under one
batch name never run at once: the second is refused with nothing moved. Staging has to be on the same
volume as the library, because a move there is a rename and a copy is refused. The
run ends waiting on you, naming the file to import.

Take the export before you run `intake land`. An export that is not there, or is
not a collection the landed files can be spliced into, is refused before the plan
reaches its gate, and so is an unmounted library or an importable file already
written under that name, so no answer is spent on a landing that could never run.

Once your intake tree has cut over to the database, with `crate tree cutover
inbox --export`, `intake land` needs no export and refuses one. It moves the
files the same way and then adds each one to the collection itself, with a
title from the file's own tags, and puts the batch playlist under your INBOX
folder, through the same guarded database session every database write here
uses: rekordbox and its agent closed, a backup acknowledged first, a capture
taken before the commit. The plan shows every row with every column it will
set, the playlist and its parent, and the database it writes, and its gate,
`intake.land.native`, is answered by a separate `crate run decide` and never
inline. A file already in the collection is reported present and not added
twice. Each row carries the artist, album, album artist, genre and year its
file's tags name, linked to the library's own artist, album and genre entries
where one of that exact name exists and made in the same commit where none
does, and the plan says which for every row. A file with no artist tag lands
with no artist, as rekordbox would show it. **Nothing about the audio is
written**: no tempo, no grid, no key, no waveform, and the run says so.
rekordbox does not analyse a row it did not make until you ask, so open it,
select INBOX / Analyze and run Analyze Tracks; Reload Tags is not needed, and
adoption reads each row's genre from the moment it lands. A row whose tempo
moves, a live drummed track or an edit of two takes, joins carrying the `dyn`
My Tag, written from the drift `analyze run` measured (below), so the visit is
two selections and the run's warning counts each: the rows without `dyn` with
Analysis Mode Normal, high precision off, BPM/Grid, Phrase and KEY on, and the
rows with `dyn` with Analysis Mode Dynamic and the rest the same. A file with
too little pulse to judge lands as steady, and a file analysed before the drift
existed is counted as unscored on the screen and takes Normal, as every row did
before. Once rekordbox and its
agent have quit, `crate analyze check` says whether the visit is done and done
right: every row analysed, every grid one tempo (or moving on a row marked
`dyn`), the Key column filled, and how often the title's key agrees with
rekordbox's. It exits 0 when the visit is done, 12 when rows still wait for
analysis, and 27 when what rekordbox wrote looks wrong, naming the rows; it
reads INBOX / Analyze, or the landing you name with `--pass` or `--session`,
and writes nothing. A row landed before
2026-10-09 also lacks the defaults rekordbox writes on every row it makes, and
will not load to a deck until `crate repair rows` fills them (R-923); a row
landed since carries them from the start. There is no import, no drag and no `intake imported` on this path.

On this path the files go straight to where they live, the folder a shelve
would have filed them in: `Music/Processed_Tracks/<year>/<MM_DD_YY subject>`,
the date and subject read off the batch name (`2026-10-27 Tidal playlists and
Favorites` lands in `Processed_Tracks/2026/10_27_26 Tidal playlists and
Favorites`), and a `--name` with no date filed under the day it landed. A
folder of that name already on disk, or one the collection stores rows under,
is passed over for ` 2`, ` 3` and on. The gate screen's `lands in` line names
the final folder, every row carries its final path from the first commit, and
the INBOX playlist keeps the batch's readable name. Landing into a batch again
by its own `--name` goes back to its folder. So no `crate intake shelve`
follows a native landing: run against such a batch, it says it was already
filed and does nothing. Batches landed before this change, and every batch on
the xml bridge, are still under `Music/<batch>` until you shelve them.

To see a native landing work before you approve it, run the same command with
`--rehearse` first. A rehearsal asks no question and writes nothing live: it
copies the database and the library's state into a scratch folder of its own
(one per run, so two rehearsals never share one), clones the staged files
there, applies the landing to the copy, reads it back, reports the plan's
digest with the rows added and the copy's integrity, and removes the scratch
folder. Your staging folder, your music folder and your database are left
exactly as they were, and rekordbox running refuses it as it refuses the
landing. A library whose drive was renamed since rekordbox made it, so that
rekordbox stores every path under the old drive name, rehearses as any other:
each row's stored path is compared under the name rekordbox recorded. When the
rehearsal fails, the scratch folder is kept and the refusal names it, the
fields that differ, and the spellings it compared. The landing you then run without `--rehearse` names the newest
rehearsal of the same folder and batch on its gate screen and says whether
its plan equals it, printing the lines that differ when it does not.

When your genre tree is database native too, the same landing files its new
rows into BY GENRE + ENERGY under the same answer. Its gate screen shows, for
every file, the bucket and sub adoption will file it in, its vocal sub when it
gets the vox tag, or why it is placed nowhere (a file with no genre lands and
is listed, filed nowhere), and the `files after landing` line counts them.
After the commit the landing plans adoption over the rows it made and files
them only when every one is where the screen said. If any differs, nothing is
filed, the rows stay landed, and the run says which rows differ and to run
`crate adopt apply`. `--land-only` lands without filing, and a genre tree on
the xml bridge files nothing, which the screen names; either way filing the
batch is then `adopt scan` and `adopt apply`.

Once you have imported the landed file, quit rekordbox, take a new export with
`crate export collection` or from rekordbox's own menu, and run
`crate intake imported --export` with that new export. It looks for every landed
file in the export. When they are all there, the import is proven: the importable
file is renamed to `PASS_inboxed.xml.imported`, which you can delete whenever you
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

Give it the importable file `intake land` wrote for the pass, under the
`--pass` `intake missing --run` told you to land it with, since the file's name is
how the pass is found. The batch folder and playlist carry the date instead. If you ran `intake imported` first, the file now ends in `.imported`, and
that name works the same. It reads what each playlist's job reported, and plans a rename only for a
playlist whose every track is now in your library, counting a track you have
since deleted on purpose as settled. A playlist with a track still missing, or
one the pass offered you for review and you have not got, is left alone and the
track is named. Nothing is renamed until you answer the gate, a playlist whose name
changed since the plan is skipped, and a playlist already carrying the prefix is
never prefixed twice. If a rename fails part way, the run names the playlists it
had already renamed, and running it again picks up the rest.

Every rename that lands is recorded under its pass, so a mark made by mistake
can be taken off again with `crate sync unmark`:

```bash
crate sync unmark --pass RUN_synced
```

Give it the pass's name, or the same intake file you gave `sync mark`; the file
does not have to be there any more. It plans to put back the title each
playlist had before the mark, and only where the title on the account is still
exactly what the mark wrote. A playlist you have retitled since, with the
prefix or without it, is listed and left, and so is one the account no longer
lists. It only ever touches playlists that pass marked: `--playlist ID` narrows
the plan to the ones you name, and naming a playlist the pass did not mark is
refused, even when its name carries the prefix. Nothing is renamed until you
answer its gate, and a playlist already put back is skipped, so running it
twice renames nothing the second time. Taking the prefix off does not make the
next `sync all` offer the playlist again: the pass already recorded it as
resolved, which is a separate record.

**Once your intake tree is database native, name the pass instead of the file.**
A native landing writes no importable file, so give `sync mark` the name you
landed the pass with:

```bash
crate sync mark --pass RUN_synced
```

Everything else is the same: a playlist is planned only when every track the
pass did not find is now in your library, and nothing is renamed until you
answer the gate. With no file to say which landing brought a track, each one
your library holds is counted as owned rather than landed. `--pass` on an intake
tree still on the xml bridge is refused and names `--xml`, since there the file
is what proves the pass landed.

To mark only some playlists of a pass, name each with `--playlist` and its
account identifier, as `sync unmark` takes them:

```bash
crate sync mark --pass RUN_synced --playlist ID
```

The plan, the gate and the renames are only those playlists, and an answer to
that narrowed plan is not taken for the whole pass. A playlist the pass does
not hold is refused before the account is read, and one the pass did not
complete, its job unfinished or a track still missing, is refused by name with
the reason. `crate organize --only marks` marks every landed pass whole.

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
crate label sync
crate label sync --next
crate label sync --next --label "Some Label"
crate label sync --answer pick --label "Some Label" --release RELEASE_ID
crate label sync --go
crate review list --queue label-release
crate review resolve ITEM_ID --verdict accepted --actor YOUR_NAME
crate label approved
crate label playlists "Some Label" --releases
crate label playlists "Some Label"
```

`label sync` is the guided way through your labels. It walks them one at a
time and asks, per label, only about the releases that are new since that label
was last asked, showing the release count, the track count and an estimated
size. Four answers: `all` takes every new release, `pick` lets you choose them by
number, `not-now` takes none, and `stop` removes the label from the registry.
Every answer is saved as it is given, so you can `quit` at any label and the next
run picks up at the first label still unanswered. A release answered once is
never asked about again, `not-now` included; a skipped release is still reachable
through `label import`. The genre gate runs before a label is asked, so a release
it would hold never reaches a question, and the first run also offers, once per
label, the releases already waiting in review from earlier sweeps. A taken
release is an accepted review item; nothing is downloaded by the answer itself.
Without a terminal, `--next` prints the next question and `--answer` records one
answer for one label, and both write the same record. To ask about one label
without reaching it through the labels above it, name it: `--next --label "Some
Label"` lists only that label and prints its question, says it has nothing
new, or says its listing failed, and leaves every other label as it was. A
label whose listing failed is a `[FAIL]` line and is never counted as having
nothing new: the closing line names only the labels that were listed, and a
run in which no label could be read at all, each listing having failed or
confirmed nothing, ends refused, exit 30, reason `label-sync-unlisted`, with
every label's line still shown and a line saying what to do about each kind. A newly followed label is
asked about its newest few releases, the `labels.offer_per_sweep` count, not its
whole catalogue.

When every label with something new is answered, the walk ends at one gate,
`label.sync.confirm`, over one summary of every answer saved since the last go:
the labels taking releases, the releases, the tracks, an estimated size and
time, and how many labels were answered not now or stop following. `--go` asks
the same gate over answers already saved. The gate is explicit, so it is
answered on its own with `crate run decide RUN label.sync.confirm apply --actor
YOUR_NAME`, then `crate --run RUN label sync --go` downloads, unattended and
paced through the provider gate. Only releases an `all` or a `pick` took are
downloaded, a track the library holds in another version goes to the match
queue instead, and a rate limit parks the download rather than retrying. A go
that stopped part way is picked up by the next `--go`, which resumes it before
anything new, and a track is never asked for twice. Once the download has
landed its tracks, the same command runs the acquisition tail on the staging
folder the way `crate sync land` does: `tag folder`, `tag guess` (with no
playlist vote, since no playlist on your account asked for a label's tracks),
`analyze run` followed by
`analyze vocals --unscored`, `analyze restamp` and `name apply`, each driven to
the end, then plans `intake land
--manifest ... --pass ...`, which names the batch for the date and the label,
and stops at the landing's own gate. The report names that gate's run and the
two commands that answer and apply it, then the rekordbox visit. A tail step
that fails ends the go there with its reason, plans no landing, keeps the
download, and names the rest of the tail to run once the cause is mended. A
track the download refused for good, one the provider offers only lossy above
all, is named in the report and skipped, and the tail runs on the tracks that
landed, the way `crate sync land` reads the same download. A go that downloaded
nothing, or whose every track was refused, runs no tail and names none. Every
go downloads into the same staging folder, so land each go before the next. The
size and time are estimates: the size from each track's duration at a FLAC rate,
the time from the pacing delay and an assumed transfer rate.

`label registry` lists who you follow. The registry records nothing about what has
been pulled. A
label's identifier is made once, when you add it, and the record of what has been
pulled hangs off that identifier. To change how a label is displayed, use
`label registry rename`. Removing and re-adding under a new spelling makes the
next sync treat the whole catalogue as new. `harvest` offers the labels behind a
playlist for review and adds and downloads nothing. Accept the ones you want in
review, then `label registry adopt` adds each accepted label the registry does
not already hold, under any spelling of its name, and reports the rest as
already held. Running it again adds nothing new.

A label you follow for one style can carry that style as its genre, so its
tracks are tagged with it and none waits for a hand tag:

```bash
crate label registry set PULS --genre Rominimal
crate tag folder /path/to/staging --label PULS
```

The genre is checked against your taxonomy when you set it, and the screen says
which folder it routes to and how. A genre that reaches only the fallback folder
is refused unless you pass `--accept-fallback`, and `--genre default` clears it.
`tag folder` gives the label's genre to every file of the label that has no
genre, without asking any catalogue, and counts those files apart in its report
under `label-genre`. A file's label is its label tag, or `--label` for a file
that carries none. A file that already has a genre keeps it, and a file of the
label with no picture is still searched, for its art only.

A label that sells on Bandcamp from its own account can name that account, so
what you buy from it arrives tagged with the label and lands filed under it:

```bash
crate label registry set PULS --bandcamp pulsromania
crate acquire bandcamp-fetch --seller PULS
crate intake land "/path/to/staging/Bandcamp 2026-11-01" --label-from-tags
```

The account is the name in the address the label's releases are sold from,
`pulsromania` for `pulsromania.bandcamp.com`, and the address itself is taken
too. One account names one label, so a second label naming it is refused with
the label that holds it, and `--bandcamp default` clears it. `acquire bandcamp`
names each purchase's label, and names every seller you would fetch from that no
label names, with the command that registers it. `--seller` takes a label's
name as well as an account. The fetch writes the label's name into the label tag
of every file it stages from that account, and leaves a seller no label names as
it came. `--label-from-tags` then files each landed file under `Record Labels /
<Label> / <Label> <year>` by its own label tag and its date tag's year, so one
batch holding several sellers files each under its own label. A file with no
label tag or no year is named on the screen and lands in INBOX filed under no
label. This works once the intake tree is database native, as `--label` does.

Or take all of it in one command, from your new purchases to the landing's gate:

```bash
crate sync bandcamp --seller PULS
```

It plans your purchases first, so a session that has expired stops there
with the login step before anything downloads. It fetches what you do not
own into `Bandcamp <today's date>` under download staging (or the folder
`--batch` names), runs `tag folder`, `tag guess`, `analyze run`, `analyze restamp` and
`name apply` on it the way `crate sync land` does, rehearses the landing on a
copy, and plans the landing itself, stopping at its gate with the commands
that answer and apply it as the session and the rekordbox visit after. The
batch is named `<date> Bandcamp <Label>` when every file is one label's, and
`<date> Bandcamp` otherwise, and each file is filed under its own label tag.
Leave out `--seller` for every seller. The report names the purchases and
tracks held back as owned with the library file each is, what the fetch
refused, the sellers no label names, and the files left with no genre. If a
step stops, run the same command again with the same `--batch`: what was
fetched is not fetched again, and whatever the folder holds is taken on
through the tail. Nothing new to fetch and nothing staged ends with no
landing. Like the landing it plans, it needs a database native intake tree.

`sync labels` is retired. It queues nothing and names `label sync`, and `sync
all` no longer sweeps labels either. A labels sweep queued before the guided
sync replaced it still runs with `crate sync labels --job JOB_ID`, so a job
already in the queue is never lost. Such a sweep proposes releases into the
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

`label playlists` keeps a label's folder on the streaming account: one
`<Label>` folder holding a private `<Label> <year>` playlist per release year.
It adds and never removes, and asks one explicit gate, `label.playlists.confirm`,
over a plan naming every playlist and how many tracks it adds. After a `label
sync --go`, `--releases` adds only the releases that go took for the label: it
reads just those releases from the provider, two calls each, creates the folder
or a year playlist if either is missing, and leaves every other year alone. A
second run plans nothing. Without `--releases` the build reads the label's
whole catalogue, two calls for every release it lists, which on a label of
thousands of releases is hours of calls. So it counts the listing first, and
when the estimate is over 500 calls it stops at its own explicit gate,
`label.playlists.crawl`, showing the release count, the calls and the time,
and reads nothing more until you answer `crawl`. A full build keeps the
releases it reads for seven days, written every 50 releases and again whenever
it stops, so a build the provider's rate limit stops part way starts again
where it stopped, and the run that applies the plan you
approved reads none of the catalogue again. The estimate counts only the
releases not kept, and both screens say how many reads were reused and how old
the oldest is. The listing itself is read again every run, so a release the
label put out since is never missed. If the kept reads cannot be read the build
refuses with `label-playlists-reads-unusable`; deleting the file it names is
safe and costs only provider calls. If they cannot be written the build still
shows its plan and warns `label-playlists-reads-unkept`, and a later run reads
those releases again.

Once a label batch has landed, `label mark` puts `DOWNLOADED ` in front of the
year playlists that batch filed, so the account stops offering them as unheard:

```bash
crate label mark "Some Label" --xml /path/to/library/RUN_synced_inboxed.xml
crate label mark "Some Label" --pass RUN_synced
```

Give it the intake file the landing wrote while your intake tree is on the xml
bridge, and the pass's name once it is database native, since a native landing
writes no file and its own record says which years it filed. Only a year the
batch filed under that label is renamed, and only while its title is still the
one `label playlists` built it under; every other year is listed and left, and
a batch that filed none of them says so. Nothing is renamed until you answer
its gate, and `crate sync unmark --pass RUN_synced` takes the marks off again.

### Sync from streaming

```bash
crate status
crate sync all --export /path/to/collection-export.xml
crate job list --state queued --state blocked
crate job resume JOB_ID
```

`sync all` queues each enabled source's own increment under one shared run and
returns almost at once. That is the design, not a failure. Nothing has run yet.
Labels are not among the sources it queues: it makes no provider call for them,
and its report names `crate label sync` as the way to take label releases.
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

A heart that comes IN is coloured, which is the inbound half the sync does not
touch. When a landing places a heart into All Favorites and its month, it
colours that track Pink in the same write, because Pink is the standing signal a
track is a favourite and the sweep above reads it. `crate favorites backfill`
does the same for every member of All Favorites that carries no colour, so the
colour and the playlist agree over a library placed before the colour write
existed. A track you coloured otherwise by hand keeps its colour and is named,
never overwritten, and a library whose colour table has no Pink row places the
hearts and says it coloured none, to be run again once Pink is restored.

The Favorites folder reads newest first: All Favorites on top, then the month
playlists from the newest down, then `Undated`, then anything else you keep
there, in the order you left it. A landing, the backfill and the split each make
a new month in its place, directly under All Favorites and any newer month,
rather than at the bottom. A folder made before that reads oldest first, and
`crate favorites order` puts it right once, with rekordbox closed: it shows each
playlist's position now and after, asks one gate, and writes positions and
nothing else, no membership and no name. A folder already in order asks nothing.

### Keep your custom playlists in rekordbox for good

```bash
crate sync twins
crate sync pair
```

A custom playlist you build on the account lands as an INBOX playlist, which
rotates out of rekordbox after thirty and ninety days. Its twin is the copy that
stays: one playlist of the same name, less `DOWNLOADED `, in the top level folder
`Custom Playlists <year>`, holding the tracks the library owns in the account's
order. A landing of an account playlist pass writes the twin of each custom
playlist it lands, beside its INBOX playlist and in the same write, and pairs the
two with no hand step. `crate sync twins` does the same once for every
`DOWNLOADED` playlist the account already holds in a year folder, shows every
twin and every track it will not hold on one gate, and plans nothing the second
time. From then on `crate sync pair` keeps each twin and its account playlist
one list: an addition on either side lands on both, a removal on either side
comes off both, and a track the library lacks is queued once.

A twin is never counted: when its folder already holds a playlist of its name,
the twin is left and named, and you pair the one there by hand with
`crate sync pair ACCOUNT_ID --rekordbox PLAYLIST_ID`. When you delete the
playlist on the account, the next `crate sync pair` unpairs the twin and leaves
it in rekordbox, named.

### Keep every playlist you made in rekordbox on the account

```bash
crate sync pair
```

With no argument, `crate sync pair` also finds every plain playlist you made in
rekordbox and syncs it with a playlist of its own on the account, both ways. A
rekordbox top folder becomes one root folder of the same name on the account,
holding one private playlist per playlist, titled with the folder first:
`GIG READY Opener`, or `GIG READY Halloween Opener` for one in a subfolder. A
playlist at the rekordbox root goes in the root folder `Playlists`. The first
sync makes the account playlist on the account's gate and adds only; after
that an addition or a removal on either side lands on both, and a track added
on the account that the library does not own is queued for download once.

Never paired: Cratekit's own trees, the Favorites folder and the custom
playlist twins, which other verbs keep. Listed on the gate and never written:
a smart playlist, and every playlist under a top folder
`outbound.pair_skip_folders` names, which is `["ARCHIVE"]` unless you change
it. A made pair whose rekordbox playlist you move into such a folder is
unpaired, and its account playlist stays. A track the account cannot carry stays in
rekordbox, counted on the gate, and is not asked about again until its ISRC
changes. Two playlists that would take one account title refuse that title
until you rename one. Delete either side of such a pair and the next sync
unpairs it, leaves the other side where it is, and does not make it again.

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
the database. `route resort` also fills a genre sub, a playlist beside a genre
folder's energy bands for one genre: in the shipped taxonomy, every track
tagged exactly `Rominimal` sits in its Minimal / Deep Tech band and in
`Minimal / Deep Tech / Rominimal` too. A library whose taxonomy copy predates
it gains it by hand, since `crate taxonomy upgrade` adds only whole folders
and classes: add `"Rominimal"` to the Minimal / Deep Tech bucket's `aliases`,
add the `[[bucket.genre_sub]]` table the shipped template carries under it, and
set `schema_version = 5`. A track landed after that reaches the genre sub at
the next `route resort`. Reports and audits are read only. `repair paths` proposes a
shorter name for each audio file whose name is over the path budget or repeats
its own title at the end, which are the names rekordbox rejects on import, and
you accept or reject each one with `crate review resolve`. Nothing is inferred.
`crate repair paths --apply` then renames the files whose proposal you accepted,
behind a confirm gate, and never one the rekordbox collection references, since
that would strand the row. It does not re-point rows or rewrite an export. `converge` reports and never repairs. If a tree has fallen
out of step, `crate rebuild --tree TREE_ID --actor YOUR_NAME` is the only way to
clear it.

To tidy everything the product's rules govern in one pass, on both sides:

```bash
crate organize --report
crate organize
```

`organize` plans two areas and asks one question for each. The rekordbox area
files unfiled tracks into BY GENRE + ENERGY and its `with vox` subs the way
`adopt apply` does, and rotates INBOX the way `inbox rotate` does. It also
gives every downloaded set on the account its INSPIRATION playlist: each
`DOWNLOADED` playlist in a `Downloaded Sets <year>` folder with no INSPIRATION
playlist of its name (the account name without `DOWNLOADED `) gets one, holding
the library tracks its account tracks match, in the set's order, with every
track it could not match named under the set. Nothing is downloaded, a set with
no match gets no playlist, and a set already in INSPIRATION is skipped, so a
second run plans nothing. That write needs rekordbox closed. The account
area builds a folder for every followed label that lacks one or a year, marks
every landed sync pass, and archives every set whose download is proven into
the root folder `Downloaded Sets <year>`, prefixed. A sync pass is found by its
intake file, or, once your intake tree is database native and writes none, by
the landing that committed it, so every pass that landed is planned and not
only the latest; a native landing of no sync pass, a label's or a set's, is
counted on the gate and planned for nothing. Either of two things proves
a set downloaded: an intake file named for the set, or a playlist of the set's
name under the INSPIRATION folder in rekordbox. It also files every playlist at
the account root
that a sync marked downloaded into the root folder named for the year of its
mark, creating that folder once if the account lacks it, and names every other
playlist at the root with why it stays. It also mirrors rekordbox onto the
account: every genre folder of BY GENRE + ENERGY, the Favorites folder and
INBOX each become one root folder of the same name, holding one private
playlist per rekordbox playlist, `Deep House Low` or `INBOX 2026-10-31
Defected`, kept equal to the tracks the account carries. INBOX mirrors only its
live batches, the playlists `inbox rotate` moves, never Old. A label batch,
which no account playlist holds, fills from the provider track each file was
downloaded as. A track whose ISRC names several releases that all agree with
it, a single and its album cut, goes onto the mirror as one of them and stays
on that one; `crate sync favorites` still hearts none of them until you heart
one yourself, since a heart is a choice of release. Approve one area and abort the other
and only the approved one is written. Every other playlist you made yourself,
on either side, is listed with a suggested home where one is obvious, and is
never moved or renamed. Nothing is deleted beyond the expired batch playlists the rotation
removes, a track that left a mirrored playlist's rekordbox playlist, and the
mirrored playlist of a batch that left INBOX, each named on the gate, and never
a track from your library. `--report` prints both plans and asks nothing. The
rekordbox area needs a backup acknowledged under a day old, and like every
database write it is worth rehearsing on a copy first.

To run one kind of step alone, name it with `--only`, as often as you like:

```bash
crate organize --report --only file
crate organize --only file
```

The kinds are `adopt`, `rotate`, `record-labels` and `inspiration` on the rekordbox side,
`labels`, `sets`, `marks`, `file`, `root` and `mirror` on the account, and `yours` on both. An
area with no kind named is not planned and not asked, so `--only file` files
the playlists at the account root into their folders without reading the
database or planning a label's catalogue, and asks only the account's
question. Its plan is only the filing, and an answer given to the full
organize is not taken for it. A word that is not a kind is refused before
anything is read.

New label releases are kept apart from the ones you have already heard. For
each followed label, the account area also plans a dated playlist beside the
year, `<Label> <year> new <YYYY-MM-DD>`, inside the label's folder, holding the
tracks of the releases a `label sync --go` took that day and that the label's
record does not list as heard. The date is the local day the go ran, so a
second go the same day adds to the same playlist and a go on another day makes
its own. The year playlist is left exactly as it was. A dated playlist older
than `labels.new_playlist_age_days`, thirty by default, is listed in the plan
and nothing is moved; merging one into its year is not done yet.

Removing files is deliberately slow. `crate delete review` offers the files behind
rows you removed in rekordbox, and confirmed ones go to the system Trash and
nowhere else. `crate tombstone list` shows what was removed and lets you lift one
so that version can be acquired again.

### Analyse audio and score vocals

```bash
crate analyze run /path/to/staging
crate analyze vocals /path/to/one-folder
crate analyze vocals /path/to/library --recursive
crate metadata mytags-vocals
crate metadata mytags-vocals --apply
```

The first `metadata` line shows the plan only. Adding `--apply` writes, and needs
the backup acknowledgment.

Analysis needs the `analysis` extra and vocals needs the `vocals` extra, both in
the README. Cratekit never writes a beat grid, a tempo element or an average BPM
field, in any container, and no flag turns that on. `analyze calibrate` and
`analyze restamp` fit a threshold and carry it across the back catalogue.

`analyze run` also writes how far each track's tempo moves over its length, a
drift, as two file tags beside the vocal ones: `driftlevel`, the spread of the
tempo between its steady sections as a percent of its middle, and `drift`,
which reads `steady`, `variable` or `unknown` (too little pulse to judge, a
beatless or very short file). Neither is a tempo. A drift at or above
`analysis.drift_cut` in the config file, 1.5 by default, is variable, and a
native landing reads the level against the cut as it is when it lands, so
changing the cut changes which rows the next landing marks `dyn`. The default
leans toward Normal, since a steady track analysed Dynamic comes back with a
wobbling grid, and it has not yet been calibrated against a real library.

Vocal scores need the vocal model to load, and a copy installed without the
`vocals` extra finishes every track with a key and an energy and no `voxlevel`.
`crate doctor` says so on its `install.extras` row and prints the reinstall
command, which keeps the extras the copy already carries. `analyze run` treats
the Camelot head on a name as finished, so a track it finalized with no score is
never scored by it again; `crate analyze vocals --unscored FOLDER` queues
exactly those files, the head and no `voxlevel`, and leaves a scored one alone.
The acquisition tail runs it after `analyze run` whenever the model can score.
`crate sync land` asks before its pass queues anything: when the model cannot
score here it stops at the gate `sync.land.without-vocals`, whose screen names
what is missing and the command that mends it. Install it and run the pass
again, or answer `crate -d sync.land.without-vocals=go sync land` to land rows
with no vocal score, which the summary then says. A landing plan in which more
than half the added rows carry no score carries the warning
`vox-mostly-unscored`. A profile with the vocals module off is never asked.

`analyze vocals` and `analyze restamp` take `--recursive`, which queues every
folder under the one you name as a single resumable job, so a back catalogue
pass is one invocation rather than one per genre folder. A folder that is a
symbolic link is not walked, and the answer says which ones it left alone.
`analyze run` has no such flag, because it renames each track as it finishes and
that resume is keyed to the filename.

`analyze calibrate` takes `--recursive` too, and for it the flag is not a
convenience. A calibration describes the whole library, so the verb fits only
over the library root, or the music folder under it, walked recursively,
`crate analyze calibrate ROOT --recursive`. Any other folder fails its
`calibrate.sample` check with nothing measured and nothing written, and so does
a walk that had to leave out a linked or unreadable folder. `--accept-partial`
fits over what was walked anyway and warns that the numbers are on its scale. The energy half measures an
even stride sample of the walk, 500 tracks unless `--sample N` says otherwise,
so the same library gives the same fit twice. The vocal cut reads every tagged
track.

### Build a set, master a recording

```bash
crate setbuild /path/under/the/library/anchor-track.aiff --count 8 --role after
crate master /path/to/recording.wav --output-dir /path/to/out
crate master /path/to/REC001.wav /path/to/REC002.wav --lufs -16
```

`setbuild` ranks tracks you own that are compatible in key and energy with the
anchor, and needs no network. `master` levels a set recording and encodes it to
lossless, and never touches the source. A recording the player split into
several files is named as every part, in order; the parts are joined in the
order you give, never sorted, the order is printed back when the job is queued,
and the master is named after the first part with `_set` added. `--lufs` sets
the loudness target, minus fourteen by default.

### Back up and restore

```bash
crate backup run --dry-run
crate backup run
crate backup run --full
crate restore list
crate restore run SESSION_ID --dry-run
crate restore run --from-backup --target /path/to/empty/dir
```

Backup copies the library to the rclone remote named under `[backup]` in the
config, keeps a dated archive of changed files, and snapshots the database. The
three destinations, `dest`, `archive_root` and `db_dest_root`, are each written
as an rclone `remote:path`, and setup asks for them when the backup module is
on, or takes them from `--backup-dest`, `--backup-archive-root` and
`--backup-db-dest-root`. A value with no remote before the colon is refused at
load rather than handed to rclone, which would read it as a folder beside the
process running the backup. The `remote` key is derived from the destinations
when you leave it out. The database portion refuses while rekordbox or its
agent is running, so a backup taken with the app open covers the music and not
the database. Doctor reports each portion's age separately for that reason. Use
`--dry-run` first, since it walks the whole plan and copies nothing.

Every backup compares every file on the volume with the remote, by size and
modification time, so a file whose tags were rewritten is sent even when its
length did not change. What differs between the two modes is how the remote is
listed. The ordinary run asks the remote for one recursive listing. `--full`
asks folder by folder, which on a large library is most of an hour against a
few minutes, and does not depend on the recursive listing being complete.
Doctor reports how long ago a full comparison last ran, under
`backup.full_comparison`, and says to run one after thirty days. The answer
to a resumed backup says which mode ran, how long the mirror took, and how many
files it compared and sent. The count sent is never zero after a real run,
because the record of the previous backup lives in the library and travels with
it.

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

When the rekordbox database sits outside the library root, which is where
rekordbox puts it by default, the `share` folder beside it holds every beat grid
and the library mirror never sees it. The database portion of a backup mirrors
that folder to `analysis-share/` under `backup.db_dest_root`, with rekordbox
closed, and keeps what each run replaced in a dated `archive` beside it. A
restore with `--target` copies it back as `share` beside the restored database,
and the totals say `analysis_share`: `pulled`, `absent` for a backup taken before
the share was carried, `withheld`, or `mirrored` when the share is under the
library root and travels with the music. A restore onto the live library
withholds it, because that restore refuses when any analysis file under the
library moves. To put grids back, restore to a target with rekordbox closed and
move `share` into place beside the database yourself.

Each snapshot records the volume identity of the library it was taken from.
`--from-backup` pulls the newest snapshot that is this library's, stepping over
another library's under a shared remote, unless `--snapshot STAMP` names one,
and a named snapshot that records another volume is refused. The confirmation
shows which stamp it resolved, so a backup that lands before you answer makes
the answer stale rather than changing what arrives. A stamp is the dated folder
name a backup wrote, this product's or the one it replaces, and nothing else is
accepted. Two cases need a word from you. A snapshot taken before identities
were recorded is never the default and is pulled only when you name it with
`--snapshot`. And after a drive is replaced, its snapshots name the old volume,
so the refusal prints that identity and you pass it back as
`--snapshot-volume IDENTITY`. It is checked against the snapshot, used for that
one restore, and never written to the config. `--snapshot`, `--snapshot-volume`
and `--include-mirror` are refused without `--from-backup` rather than ignored.

When the drive itself died and its replacement is a new, empty volume, the verb
above cannot help, because every gate it passes was recorded beside the library
that is gone. Mount the replacement and recover onto it:

```bash
crate restore bare-metal --target /path/to/mounted/replacement --accept-replacement --dry-run
crate restore bare-metal --target /path/to/mounted/replacement --accept-replacement
```

It pulls the mirror first and the database second, and reports each half
separately. It refuses while the recorded library can still be read, refuses a
target that is the empty folder the lost volume left behind on the internal
disk, refuses a target that already holds a database, and refuses when nobody is
at a terminal. `--accept-replacement` is the acknowledgment, since the recorded
one was on the drive that died. It asks whether rekordbox is running twice,
before it starts and again before the database lands, so leave the application
closed until the recovery reports.

It rolls no session back. The session log, the captures and the review queue
arrive inside the mirror as the last backup saw them, and the database comes
from a dated snapshot, which is the same moment only if that backup ran with
rekordbox closed. Run `crate converge` on the recovered library to see whether
the two agree. When the database is configured outside the library root, which
is rekordbox's default, it was never on the lost drive, so only the mirror half
runs and the report says where the database is.

A recovery that stops part way is refused when you run it again, because the
target now holds database files and a target holding one is always refused. The
failure says so and gives the step: remove every file ending `.db` under the
target, then run it again. Nothing is lost, since each of those files came from
the mirror or the snapshot and is transferred again, and music that already
arrived is not copied twice.

Afterwards the config still names the drive that died. Run `crate doctor`, which
prints the identity it reads from the new drive, then `crate setup` with
`--library-root` and `--volume-id` to record the recovered library, since setup
keeps a recorded identity until it is told a new one.

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
the same gate with nothing recorded and refuses again. Or answer and continue in
one command: `--continue` records the answer, then runs the verb that owns the
run again with the arguments it was first given and `--run`, and prints that
verb's result.

```bash
crate run decide RUN_ID route.inbox.apply apply --continue
```

With no `--actor`, the answer is recorded as `cli` when you are at a terminal
and as `session` when nothing is, which is how a session working for you is told
apart; the summary says which. An explicit gate still takes no answer on the
verb's own command line, so `--continue` is always the second command.

When a verb that writes the rekordbox database stops at its gate, it also names
every other run of the same verb that holds its gate open or answered it in the
last twelve hours, one `gate-sibling-run` warning per run with its identifier,
who answered, the option and the time. `crate run decide` repeats the warning
when another run already answered the same plan the same way. It refuses
nothing: two runs planned over one library are told about each other, and an
apply over a library that moved underneath it is still refused stale. Gates you
will meet:

| Gate | Go option | Verb |
|---|---|---|
| `route.inbox.apply` | apply | `route inbox` |
| `name.apply.confirm` | apply | `name apply` |
| `intake.land.confirm` | apply | `intake land`, intake tree on the xml bridge |
| `intake.land.native` | apply | `intake land`, intake tree database native; explicit, `crate run decide` only |
| `intake.file.native` | apply | `intake file`, intake tree database native; explicit, `crate run decide` only |
| `tag.retag.confirm` | apply | `tag retag` |
| `tag.remap.confirm` | apply | `tag remap`; explicit, `crate run decide` only |
| `tag.suggest.confirm` | apply | `tag suggest`; explicit, `crate run decide` only |
| `sync.favorites.confirm` | sync | `sync favorites` |
| `sync.all.favorites.confirm` | sync | `sync all` |
| `sync.mark.confirm` | apply | `sync mark` |
| `sync.unmark.confirm` | apply | `sync unmark`; explicit, `crate run decide` only |
| `export.playlist.confirm` | export | `export playlist` |
| `delete.review.confirm` | trash | `delete review` |
| `adopt.apply.approve` | approve | `adopt apply` |
| `adopt.move.approve` | approve | `adopt move` |
| `inbox.rotate.approve` | approve | `inbox rotate`; explicit, `crate run decide` only |
| `inbox.refill.approve` | apply | `inbox refill`; explicit, `crate run decide` only |
| `organize.rekordbox.approve` | approve | `organize`, its rekordbox area; explicit, `crate run decide` only |
| `organize.account.apply` | apply | `organize`, its account area; explicit, `crate run decide` only |
| `restore.run.confirm` | restore | `restore run` |
| `session.ack.backup` | acknowledged | `session ack` |
| `run.retire.confirm` | apply | `run retire` |
| `write.cloudsync.unreadable` | proceed | any verb that writes |

Every gate also offers `abort`. An abort is a recorded answer and not a failure,
and the verb returns its plan with a no-op outcome. Read the last gate in the
table before answering it. It fires when Cratekit cannot tell whether a
cloud sync client is also touching the library, and proceeding is a decision about
a second writer. Treat "could not read" as unknown, not as safe.

### Retiring old gates

A run that stopped at a gate nobody will answer stays open until something
answers it. `crate run retire` answers every open gate idle for longer than the
threshold, a week unless you give `--older-than` or set
`reports.open_gate_stale_days`, and it answers each one `abort` as `session`,
never the go option, explicit gates included. It shows every gate it would
answer and asks once; nothing old means nothing to ask.

```bash
crate run retire --older-than 7d
crate -d run.retire.confirm=apply run retire --older-than 7d
```

A gate is idle from its run's start or its last resume, whichever is later, so a
run you picked up yesterday is not old. A gate whose options have no `abort`, or
whose verb is gone, is kept and named, and stays in the status list. Queued jobs
are not touched; `crate job cancel` is theirs.

### The backup acknowledgment

Before any write, Cratekit wants proof that you have a current backup, and the
proof has to come from you, or from the ages themselves. The acknowledgment
lasts twelve hours. Answering a gate is not the same act as minting it.
From a terminal you are sitting at:

```bash
crate session ack
crate run decide RUN_ID session.ack.backup acknowledged --actor YOUR_NAME
crate --run RUN_ID session ack
```

The gate asks whether the database and the music files are backed up, so run
`crate doctor` first and read the two backup ages. The line after them,
`backup.acknowledgment`, says whether an acknowledgment is on record and when it
expires. If a verb refuses because the acknowledgment is missing or has expired,
this is the fix.

A session working for you may mint it as the actor `session`, with no
terminal, but only on young backups, in one command:

```bash
crate session ack --as session
```

It asks no gate and leaves no run waiting. When an acknowledgment is already
valid it says so, with its expiry, and mints nothing. `--as` takes no value
but `session`. The older two step form still works:

```bash
crate session ack
crate run decide RUN_ID session.ack.backup acknowledged --continue
```

With no terminal the answer is the session's without `--actor`, and
`--continue` mints in the same command; no `script` wrapper is needed.

Either way the verb checks the ages itself and mints only while both portions are
under five days old. An older portion, or one with no completion recorded, is
refused as `backup-acknowledgment-backup-too-old` and named; run a backup, or
acknowledge from a terminal yourself. The acknowledgment records which rule
minted it, `session-ages` or `terminal`, and who answered the gate.

## Using DEADCA7 beside Cratekit

DEADCA7 is a catalog manager and player that can push into rekordbox's
database. Its playlists go into one folder named `DEADCA7` at the top of the
playlist tree, along with its hot cues and its grids and waveforms. Cratekit
shares the library with it and leaves its work alone:

- Nothing Cratekit writes can move, rename, empty or fill that folder or
  anything in it. A write that would is refused, with nothing written.
- `crate organize` names the folder once, as another app's, and never lists it
  among your own playlists or suggests a home for it.
- A playlist DEADCA7 pushed that happens to share your Favorites playlist's
  name is not mistaken for it.
- No tree in your taxonomy may be named `DEADCA7`.
- `crate doctor` says whether DEADCA7 is installed, when it last pushed into
  the database, and warns when that push is newer than your last database
  backup. Run `crate backup run` then.

Both tools refuse while rekordbox is open, so they take turns. Do not push
from DEADCA7 while a Cratekit verb is running: the verb's next commit sees the
push and refuses, which is the safe answer, and running it again carries on.
A folder merely named DEADCA7 somewhere below the top is your own and is
treated like any other.

## When something refuses or stalls

| Symptom | Ask |
|---|---|
| Any refusal | Read its reason and remedy. Then run `crate doctor`. |
| "Decision required" | `crate run show RUN_ID` names the gate and its options. |
| A job that never moves | `crate job show JOB_ID`. Queued work needs `crate job resume`. |
| A blocked job | `job show` carries the cause, usually a review decision or a credential. |
| "provider-call-ceiling" | The command made as many calls to the streaming provider as one command may, 500 unless `[provider] calls_per_command` says otherwise, and stopped with what it did kept. The refusal prints the exact command that continues, with `--calls N` raising the ceiling for that one run; a job continues with `crate --calls N job resume JOB_ID`. The next run is back at the configured ceiling. |
| A resume that refuses the same way each time | Cancel it with `crate job cancel` and queue a fresh one. |
| `sync land` says intake jobs are left open | Its left open row lists them by playlist with their age. Old ones: `crate job cancel --stale-days DAYS --dry-run`, then without `--dry-run`; the next pass queues each freed playlist again. |
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
behalf unless both backup ages are under five days, and every writing verb
refuses while rekordbox or its background agent is running, so neither is a
thing an agent can do for you over old backups or an open rekordbox.

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
