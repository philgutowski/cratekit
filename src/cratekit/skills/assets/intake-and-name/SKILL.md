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
list against the library is `match run`, below.

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

`name apply` builds the full plan, then stops at its confirm gate and exits
asking for a decision. Answer it on the invocation, or later from anywhere:

```bash
crate name apply --decision name.apply.confirm=apply
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

## Path repair proposes, and never applies

```bash
crate repair paths
crate repair paths --root /path/to/folder
```

This verb writes nothing to the library. It walks for recorded locations that no
longer resolve, proposes what it believes each row now points at, and offers
every proposal into the path repair queue. A wrong answer re-points a library row
at somebody else's file, which is a quiet and expensive kind of wrong, so the
decision belongs to a person and is recorded rather than inferred.

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
