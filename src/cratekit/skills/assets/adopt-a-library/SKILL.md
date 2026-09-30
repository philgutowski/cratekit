---
name: adopt-a-library
description: Map a library somebody already has into the declared taxonomy. Use when a person says they already have a library and want this tool to take it over, when the census or the apply refuses, when an approval is reported stale against a plan that moved, or when a queued adoption job is parked on a decision nobody has answered. Covers the read-only scan, the two questions it puts in the review queue, the explicit approval gate, and the tag write nothing puts back.
---

# Adopting a library you already have

Taking a collection that predates this tool and filing it into the taxonomy the
active template declares.

Nothing here is required. Both verbs run from the command line with no skill
installed, and this exists so the order and the two refusals are not something a
person has to work out under pressure.

## The two verbs are not in the same position

They look like a pair and they are not. The scan reads, declares no gate, and
writes nothing anywhere. The apply writes a genre tag onto the person's own audio
files, which is the one operation in this product that no snapshot holds and no
re-import puts back.

```bash
crate adopt scan
crate adopt apply
```

Treat the first as free and repeatable. Treat the second as the one that needs a
person present.

## The scan is total, and that is the requirement

Every row the census is handed comes back in exactly one named category, so a
file that is missing, unreadable, online-only, recorded under a prefix this
installation maps nothing for, or recorded as something that is not a path at all
is REPORTED rather than quietly absent from the plan. A track that is neither in
the plan nor in a named category is a track nobody decided about, and the person
who ran the scan cannot tell that apart from a track the plan had nothing to say
about.

Alongside the category sits adoption's own disposition for the track, which says
what it intends to do: route it, ask about its genre, exclude it because the file
is not usable on this machine, or hold it because nothing declares where it goes.
A track whose genre is blank, or is one of the strings the template declares too
coarse to be a source, is never filed under the router's fallback tier here. That
tier is a legitimate answer everywhere else in the product and it is not one
here, because accepting it would file thousands of tracks into one folder and
report a complete adoption.

## Both verbs queue rather than run in the shell

A census walks a whole collection and stats every file in it, which is long work
by any definition, so it is queued under a job and driven by the engine. That is
what gives it a record, a resume, and an answer to "what is it doing" from a
session other than the one that started it.

```bash
crate job list --state running
crate job show JOB-ID
crate job resume JOB-ID
crate job cancel JOB-ID
```

`--job` on either verb continues the work already queued under that identifier
rather than queueing a second record for one piece of work. It is how a resume
re-invokes the verb, and it is worth knowing so a stalled census is not answered
by starting a fresh one beside it.

```bash
crate adopt scan --job JOB-ID
crate adopt apply --job JOB-ID
```

There is no argument naming a tree. A taxonomy declares exactly one routing tree
by stable identifier, so a flag could only hold that identifier or a mistake.

## The plan has exactly two open questions

They go in the review queue rather than into a file, because a plan approved
thirty percent through and resumed next week needs verdicts that outlive the
process that collected them. One kind is a per track genre question, the other is
a folder collision, a declared destination whose folder already exists holding
rows this plan does not name.

```bash
crate review list --queue adoption
crate review list --queue adoption --kind adoption-collision
crate review show ITEM-ID
crate review resolve ITEM-ID --verdict accepted --option adopt-existing --actor operator
crate review clear ITEM-ID --actor operator
```

A collision has two answers and only two: write into the folder that is already
there, or leave it alone and place nothing in it. The decision is keyed on the
library's own identifier for that folder rather than on its name, so renaming the
folder does not orphan the answer into looking unanswered.

The excluded tracks are deliberately not offered here. An unreadable or
online-only file is a fact about the machine rather than a question for a person,
and a thousand of them in the queue would bury the two questions that need
answering. They stay in the plan carrying the category that names them.

## The approval is an act, and no flag stands in for it

There is no `--approve` and no `--yes`, in this verb or anywhere in the package.
The first invocation builds the plan, offers the gate the plan's digest, records
the run, and exits asking for a decision. Answering happens against that run, as
a separate recorded act naming who made it, and then the verb is re-invoked
against the same run.

```bash
crate adopt apply
crate run show RUN-ID
crate run decide RUN-ID adopt.apply.approve approve --actor operator
crate --run RUN-ID adopt apply
```

`run show` is the verb that names which gate is open and which options it takes,
which matters because the apply declares a second one. If the cloud sync state
cannot be read, the guarded writer raises its own explicit gate mid run, answered
the same way against the same run.

```bash
crate run decide RUN-ID write.cloudsync.unreadable proceed --actor operator
```

An empty plan still asks. "Nothing to adopt" is a plan a person can still abort,
and skipping the question when the plan is empty would make the library whose
census has not run the one library that is never asked.

## An approval names one plan, not the verb

The gate is digested against the plan, so an approval given for one plan is
refused against a plan that has since moved rather than honoured against it. The
plan is rebuilt from the library on every run, which means an approval, then an
edit to the library, then an apply, is a stale decision and is reported as one.
That is not hypothetical. It is the ordinary shape of somebody approving in the
evening and applying the next morning.

When it refuses as stale, read the plan again and decide again. Do not reach for
a way around it; there is not one, and the digest is the only thing standing
between an approval and a library it was never given for.

## What the apply asserts before it touches a file

The whole loop runs inside one destructive session, opened once around every
entry rather than per entry. That session asserts the volume identity still
matches, that a backup has been acknowledged, and that rekordbox is closed, and
it holds a lock for the whole run so two concurrent applies meet the lock instead
of meeting one file twice. Close rekordbox before starting, and expect a refusal
rather than a partial write if the drive that answers is not the drive that was
recorded.

```bash
crate doctor
crate status
```

Queueing itself opens no session, deliberately. A session opened to do zero work
would refuse on a machine that has not acknowledged a backup, which would make
the verb unreachable on exactly the machine adoption exists for.

## The tag write is the one thing restore does not cover

A restore puts back the database and the state coupled to it. It does not put
back a value this tool wrote into a file on disk. So adoption records what each
file's tag held BEFORE it wrote, in a ledger of its own, and that ledger is the
only surviving copy of those values.

```bash
crate restore list
```

Two consequences worth stating plainly. Losing the state directory loses the
undo, not just a log. And an apply is safe to resume because progress lives in
the applied ledger rather than in the plan: entry identifiers hash the
destination together with the track, so a taxonomy edit that moves a track
produces a new entry that comes back as work, while everything that did not move
keeps its identifier and stays skipped.

## Moving a track the plan withheld

The apply withholds a track that already sits in one energy or style sub while
its own file reads another, lists it, and moves nothing. A third verb acts on
that list. It adds the track to the sub its file names and then removes it from
the one it held, and it is the only verb in the product that removes a
membership.

```bash
crate adopt move
crate run decide RUN-ID adopt.move.approve approve --actor operator
crate --run RUN-ID adopt move
```

It reads the backup acknowledgment before it asks, so acknowledge a backup
first. The gate lists every move with what it adds, what it removes and the
reading that decides it, and lists beside them every track it leaves where it
is: a file with no reading, a genre that names no style, and a sub held through
a playlist that was renamed. A sub class such as the vocal sub is never moved
out of.

The additions are committed before any removal is attempted. A run that stops
between the two leaves a track in both subs and never in neither, says which
tracks, and finishes on a resume. The removal marks the row the way rekordbox
marks a removed row and deletes nothing, and the snapshot taken before the
first write restores all of it.

## Reading a result of zero

The collection reader has not landed in this build. The census the apply rebuilds
is therefore empty, the plan it digests is the empty plan, and nothing is
outstanding. A report of zero entries against a library full of tracks is a
missing input rather than a refusal or a broken machine, and the gate, the
session, and the lock around it are all real and driven.

## Checking what adoption actually landed

Ask the library rather than trusting the report. Convergence compares declared
membership against the database per governed tree, coverage names tracks the
governed trees do not cover, and the unplaced report finds rows nothing places.

```bash
crate converge
crate audit coverage --limit 200 /path/to/collection.xml
crate route unplaced
crate report library /path/to/collection.xml
```

A disagreement between the first two is the interesting one. Convergence answers
whether the tree holds what the declaration says, and coverage answers whether
the declaration reaches the whole collection, which are different questions that
a single "did it work" reading collapses into one.
