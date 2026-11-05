---
name: intake-and-name
description: Bring music into the library and get it correctly named. Use when there is a set recording or a mix URL to process, a streaming playlist to import, a single file already on disk to ingest, or a tracklist to resolve against what is already held; also when somebody wants an identification and no download, when a folder of downloads needs genre and album art, when filenames should be rebuilt from the naming template, or when the library holds rows whose files it can no longer find. Trigger words: import, ingest, intake, track ID, identify this mix, tracklist, tag this folder, rename, broken path, missing file, file not found.
---

# Intake and naming

Getting music in, and getting what arrived named the way the library expects.

Placing what arrived into the configured routing tree is a different job with its
own verbs, and it is not covered here. This skill stops once the tracks exist,
are tagged, are named, and point at files that resolve.

## Pick the verb from the shape of the input

Four ways in, and the choice is made by what you are holding rather than by what
you want out of it.

```bash
crate intake set /path/to/recording.wav
crate intake playlist https://example.com/a-playlist
crate intake file /path/to/one-track.aiff
crate intake identify /path/to/recording.wav
```

A set recording or a mix URL goes through the whole pipeline. A streaming
playlist is its own verb because the tracks are already named and there is
nothing to recognise. One file already on this machine has no remote work at all.
Identification stops after it knows what is in the recording and downloads
nothing.

If you already have the tracklist as text, none of the four apply. Resolving a
list against the library is `match run`, below, and turning its missing lines
into a download list is `intake missing --list`, which searches the provider
for each one, lists a line only on exactly one exact match, and offers
everything else to `review list --queue version-match --kind provider-candidate`.
Run it again after answering and the accepted candidate is listed.

## Identification is where money is spent, so it checks first

`intake identify` refuses before the first paid call when the recognition
credential or the carve binary is not recorded on this machine. That refusal is
deliberate and it is the whole design of the verb: reporting the gap up front is
the difference between a refusal and a paid call that cannot finish and is billed
anyway.

```bash
crate doctor
crate intake identify /path/to/recording.wav
crate --output json intake identify /path/to/recording.wav
```

When it refuses, the health check is the verb that says which credential is
missing and how to record it. Do not retry the identification hoping it clears.

The answer comes back on the match surface, the same shape `match run` produces,
so anything that can read one can read the other. Reach for the JSON form when
something other than a person is going to consume it.

## A list you already have goes to match run

```bash
crate match run /path/to/tracklist.txt
crate --output json match run /path/to/tracklist.txt
```

Every line resolves into one of three states, and only one of them is a question.
Matched and missing are results. Needs review means a candidate exists that is a
DIFFERENT version of the recording you asked for, a remix, an edit, a live take,
a clean cut, and no rule over the strings can decide that for you. Those become
items in the version match queue and nothing else does.

```bash
crate review list --queue version-match
crate review show ITEM-ID
crate review resolve ITEM-ID --verdict accepted --option CANDIDATE-ID
```

A version that a tombstone suppresses appears in none of the three arrays and is
reported on the warning channel instead, so it is not silently counted missing
and then re-acquired.

## Long work is a job, one file is a plan

`intake set`, `intake playlist`, and `tag folder` queue a job and hand back its
identifier. They do not hold the terminal. `intake file`, `name apply`, and
`repair paths` answer inline, because a plan over local files needs no worker.

```bash
crate job list --state queued --state running
crate job show JOB-ID
crate job resume JOB-ID
crate job cancel JOB-ID
```

Blocked always carries the cause that blocked it, and cancelled is a state of its
own rather than a flavour of failed, so a job somebody stopped on purpose is
never confused with one that broke.

The `--job` flag on those three verbs is not for you to type. It is how the
driver continues work already queued under that identifier, and typing it by hand
reports the existing job instead of starting new work.

`intake file` plans by default and writes only when you give it the export to
splice into, which is what keeps a look before a write:

```bash
crate intake file /path/to/one-track.aiff
crate intake file /path/to/one-track.aiff --export /path/to/fresh-export.xml
```

Once the intake tree has cut over to the database there is no export to splice
and the second form is refused by name. The first form then plans one collection
row for the file and one playlist under the intake folder, and stops at the
explicit gate `intake.file.native`, which takes a separate `crate run decide`
with an actor. Nothing about the audio is written on either path.

The export comes from rekordbox's File menu, or, with rekordbox closed, from a
copy of the database:

```bash
crate export collection /path/to/fresh-export.xml
```

It never replaces a file, so name one that does not exist yet.

## Tagging a folder

```bash
crate tag folder /path/to/downloads
crate job show JOB-ID
```

Genre and album art, written into the files. It touches no library rows and no
tree membership, so it is safe to run over a staging folder before anything has
been imported.

Nothing here writes a beat grid, a tempo element, or an average tempo field, in
any container. That is absolute across this product, two suites enforce it, and
there is no flag that turns it on. Do not go looking for one.

## Naming is applied from the declared template, never typed

```bash
crate name apply
crate name apply --root /path/to/folder
```

The template is configuration. A name typed by hand disagrees with the one the
next pass computes, and then the two fight over the same file forever, so the
only supported way to rename is to let the verb render it. A field the track does
not carry is left out of the rendered name rather than written as an empty
segment.

A file the rekordbox collection already references is never renamed or
retagged, whatever folder you point the verb at, because rekordbox records a
path once and a rename leaves its row pointing at nothing. Those files appear in
the plan marked `referenced` and are counted under `totals.referenced`. If the
collection cannot be read at all, the verb refuses with `collection-unreadable`
and renames nothing. When there is something to rename, a row recorded outside
the library root, under a volume no rule in `library.location_prefix_map` names,
whose recorded file is not on this machine either, makes the verb refuse with
`collection-row-unmapped` and rename nothing, because it cannot tell which file
that row references. The refusal names how many rows and the first recorded
location, and the remedy is a prefix rule spelled exactly as that location is,
capitals included. There is no flag that overrides any of these.

Two files in one folder that render to the same name are a third held back
class. Neither is renamed, because nothing decides which of them earns the name,
and a file whose rendered name is already taken by a file the verb is not moving
is held the same way. They appear in the plan marked `collides`, carrying the
reason, and are counted under `totals.collides`. Give one of them a name of its
own, or move it out of the folder, and the next pass renames both.

A freshly acquired file is named for its provider identifier, `92654769.flac`,
and that is the one name the verb composes: a stem that is digits and nothing
else is given the body `Artist - Title` from its tags, the version kept inside
the title as tagged. The head is derived the way it is for every file, so a
file with a key tag and no tempo gets no head, and a head the tag already
carries is rendered. A stem carrying anything but digits is carried as it is,
so the verb never rewrites a name a person or the source system chose. An
identifier file whose tags cannot compose a body, no artist tag, no title tag,
or a title that is only a head, is a fourth held back class, marked `unnamed`
with the reason and counted under `totals.unnamed`, and is never renamed to its
title alone. Tag it and the next pass names it. An identifier file the
collection references is held as `referenced` like any other, because no tag
can make it renamable.

The gate screen shows the totals, each planned rename and each held file with
its reason, up to two hundred of each, so the plan is read before it is
answered. A rename that would land on a name other than the one the plan was
approved with, because a tag changed while the gate waited, is not performed
and is named in the report.

The verb answers `rename-incomplete` when it could not carry out every rename
the plan promised, whether that is a collision, a file that left while the gate
waited, a name taken after the plan was approved, a rename the filesystem
refused, or a title tag that could not be written. The renames that could happen
still happened, `totals.renamed` says how many, and the cause names every
outstanding file with the reason it was not renamed. A file held back because
its name is taken by a file carrying the same ISRC is said to be a second copy
of one recording, and carries that ISRC: keep one copy and move the other out
of the folder. It is not a refusal and it
is not ok: a sweep reported as ok over a rename that never happened is a library
nobody knows is out of convention.

`name apply` builds the full plan, then stops at its confirm gate and exits
asking for a decision. Answer it on the invocation, or later from anywhere:

```bash
crate --decision name.apply.confirm=apply name apply
crate run show RUN-ID
crate run decide RUN-ID name.apply.confirm apply --actor operator
```

The second pair is the one that matters when the run has already exited or when
somebody else is going to answer. A decision recorded against the run is state,
not an argument to a process that has gone.

There is a second gate on this verb. If the cloud sync state cannot be read, it
asks whether to proceed rather than guessing, because renaming files underneath a
sync client that is mid flight is how two copies of a library disagree.

```bash
crate run decide RUN-ID write.cloudsync.unreadable abort --actor operator
```

## Path repair proposes, and applies only what you accepted

```bash
crate repair paths
crate repair paths --root /path/to/folder
```

Without `--apply` this verb writes nothing to the library. It walks the folder
for audio files whose name is over the path budget or repeats its own title at
the end, which are the names rekordbox rejects on import, proposes a name that
fits, and offers every proposal into the path repair queue. It does not re-point
a library row and it does not rewrite an export. A rename is still a quiet and
expensive kind of wrong when it is the wrong one, so the decision belongs to a
person and is recorded rather than inferred.

```bash
crate review list --queue path-repair --limit 50
crate review show ITEM-ID
crate review resolve ITEM-ID --verdict accepted --option CANDIDATE-ID
crate review resolve ITEM-ID --verdict rejected --actor operator
```

Running the pass again is safe. It is idempotent, so a name that already fits
proposes itself unchanged, and offering the same item twice keeps the verdict it
already has rather than writing a second row. A rejection can be revoked when it
turns out to have been wrong:

```bash
crate review clear ITEM-ID --actor operator
```

Accepting a proposal renames nothing on its own. A second run with `--apply`
reads the queue back and renames the files whose proposal was accepted with the
`accept` option, behind a confirm gate, and leaves every open, rejected and kept
item alone. `--root` narrows it to the accepted files under one folder.

```bash
crate repair paths --apply
crate --decision repair.paths.confirm=apply repair paths --apply
```

A file the rekordbox collection references is never renamed, exactly as in
`name apply`, because rekordbox records a path once and a rename strands the row.
That file, a file whose new name is already taken, and any other accepted rename
that did not happen are each named in the report with the reason, and the run
does not answer ok over them. Clear and reject a proposal that should never be
applied, and it leaves the plan. Locations inside an export are not rewritten.

## When something stops

Read the refusal instead of retrying it. Two exits are worth recognising on
sight. A decision required exit means a gate is open and `run show` will name it
with its options. A pending human action exit means the tool has done its part
and something outside it has to happen next, which for intake is usually an
import a person performs.

```bash
crate status
crate job show JOB-ID
crate run show RUN-ID
```

`status` answers what the library's own state is, open runs and per source sync
state, which is a different question from whether this machine is set up. That
second question belongs to the health check.
