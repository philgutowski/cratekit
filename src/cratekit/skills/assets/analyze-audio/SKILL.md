---
name: analyze-audio
description: Analyse audio for key, tempo, and energy, and run the calibration around it. Use when a folder of new tracks carries no key in its filenames, when somebody says analyse, calibrate, validate, restamp, re-rate the energy, or fit the threshold, when an analysis job is sitting in the queue and nothing is moving, or when a recalibration has to be carried across the back catalogue.
---

# Analysing audio

Four verbs. One measures, one fits a threshold, one scores the measuring, and
one carries a new threshold across everything already in the library.

Nothing here is required. Every one of these runs from the command line without
a skill installed, and this exists so the order and the traps are not something
a person has to rediscover.

## What a pass produces, and what it refuses to produce

A pass reads one file and returns a Camelot key, a measured tempo, and an
energy level. The key and the tempo become the head of the filename, and that
head is the whole durable record of the pass. Energy is what the routing verbs
read when they decide where a track belongs.

```bash
crate analyze run /path/to/staging
```

**No beat grid is ever written.** Not a tempo element, not a tempo tag, not an
average tempo field, not an analysis sidecar, in any container, and there is no
flag that changes this. The reason is arithmetic rather than taste: the detector
octave folds, so a confident wrong tempo seeds a grid at half or double time,
and every cue point and every loop already set against that track moves with it.
A wrong grid is worse than no grid. Import gridless and rekordbox derives tempo
and grid from the audio itself, which costs nothing to redo and is right more
often. A number written into a filename is a name, and nothing downstream reads
it as a grid.

## Analysis is a job, and the job is the thing you drive

The verb queues the work and returns. It does not analyse anything inline, and
this is deliberate rather than an omission, because the analysis dependencies
are heavy and the supervising process refuses to import them. Queue, then drive,
then watch.

```bash
crate analyze run /path/to/staging
crate job resume JOB_ID
crate job show JOB_ID
```

The driver is a detached child process, so closing the terminal does not kill
the pass. Re-invoking the verb with the job identifier reports that job rather
than queueing a second one over the same folder, which is the difference between
asking how it is going and starting again.

```bash
crate analyze run /path/to/staging --job JOB_ID
crate job list --state running
crate job list --state queued --state blocked
```

`--state` repeats. A filter naming a state that does not exist refuses instead
of matching nothing, because a silently empty result looks exactly like a queue
that lost your job.

## Resume is the filename, not a sidecar

A file whose name already carries a complete head is skipped on the next pass.
Complete means the key and the tempo both, so a file that got a key while tempo
detection failed counts as unfinished and is picked up again rather than
stranded for ever. That is why a killed driver needs no cleanup and why running
the same folder twice is cheap. The unfinished tail is exactly the set of files
that still have no head.

## Calibrate fits a threshold to this library's own data

Calibration wants a labelled folder to work from, tracks whose right answer you
already know, and it fits the threshold against those rather than against a
number somebody else's library liked.

```bash
crate analyze calibrate /path/to/labelled
crate analyze calibrate
```

It is read only. It writes no file, renames nothing, and touches no database, so
running it costs only time. The folder is optional and running it bare is a
legitimate move: the report comes back as a list of checks, each with its own
status and its own detail, and a check that has not got what it needs says so in
its own row instead of failing the whole verb. That is how you find out what it
wants without guessing.

```bash
crate --output json analyze calibrate /path/to/labelled
```

Reach for the JSON form when something other than a person is going to read the
answer, because the human rendering is free to change and the payload is not.

## Validate asks a different question from calibrate

Calibrate proposes a threshold from labelled data. Validate scores what the
analysers actually produce against labelled ground truth, which is the question
of whether the fitting worked, not the question of what the fit is.

```bash
crate analyze validate /path/to/labelled
```

Run this before spending a restamp on a new threshold. Validate is minutes and
writes nothing. Restamp is hours and writes to the back catalogue, so the cheap
check belongs in front of the expensive one.

## Restamp is the expensive half, and it writes

Restamp re-applies analysed values across tracks that were already analysed
under the old threshold. It queues like a run does, and its preconditions are
stricter because it writes both files and database metadata.

```bash
crate doctor
crate analyze restamp /path/to/library
crate job resume JOB_ID
```

Check the health report first rather than finding out from a driver's log file.
Two of its rows decide whether a restamp can write at all. The library volume
has to be mounted, and the rekordbox application version has to match the pin
that was recorded deliberately. An unset or mismatched pin freezes every
database write by design rather than by breakage, and the health report names
which of the two you are looking at along with the fix.

Stopping one is a first class outcome rather than a failure:

```bash
crate job cancel JOB_ID
crate job show JOB_ID
```

A cancelled job reports as cancelled. It does not masquerade as a job that
broke, so the queue stays readable afterwards.

## When a run stops at a gate

A write can stop and ask a question rather than proceeding. If the guard cannot
read the cloud sync state, the run stops and names the gate, which is
`write.cloudsync.unreadable`, and its two options are proceed and abort.

The answer is a separate, recorded act with a named actor. It is not a flag on
the same invocation that discovered the question, and that is a rule rather than
an oversight, because one blanket affirmative would answer every gate in the
product at once.

```bash
crate run show RUN_ID
crate run decide RUN_ID write.cloudsync.unreadable proceed --actor a-person
```

The decision lives on the run, so the run is what carries it afterwards. The
root `--run` flag is how a later invocation continues a run that already holds
an answer, and a fresh run holds none, which is why re-queueing the same work is
not a way past a gate. Check what is already queued before adding to it.

```bash
crate job list --state queued
```

## After a restamp, the placement is stale

Energy changed, so where a track belongs changed with it. The analysis verbs do
not move anything. Re placing is a separate verb, and it queues a job of its own
for the same reason.

```bash
crate route resort
crate job resume JOB_ID
crate report library /path/to/collection.xml
```

The last one is the read only sanity check, the library's own statistics
including the tempo spread and the gaps, and it answers whether the restamp
moved what you expected it to move.

## Why a verb refuses before it does any work

Analysis is a feature module sitting behind an extras group, so there are two
different ways it can be missing and they look nothing alike.

If the active profile does not switch the analysis module on, the verbs are not
built at all and the shell reports an unknown command. If the module is on but
its dependencies are not installed, the verb is present and refuses with the
name of the extra it needs.

```bash
crate profile show
crate profile set full
crate doctor
```

Changing the profile changes nothing else. It moves no files, migrates nothing,
and does not rewrite the routing tree.
