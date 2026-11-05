---
name: route-the-library
description: Filing tracks into the declared routing tree. Use when the intake folder needs emptying, when tracks sit in the collection that no governed tree places, when a genre or energy change means already-filed tracks belong somewhere else, or when a placement was decided before the library held a row for the track. Triggers on route, file these tracks, sort the intake folder, unplaced, resort, re-place, pending placement, and "nothing places this track".
---

# Route the library

Four verbs put tracks where the declared taxonomy says they go. They are not
four spellings of one thing, they answer four different questions, and picking
the wrong one is the usual reason routing appears to do nothing.

```bash
crate route inbox
crate route unplaced
crate route resort
crate route pending
```

The intake folder is `route inbox`. What no governed tree places is
`route unplaced`. Adding tracks that are already filed to where they now
belong, after a genre or an energy band changed under them, is `route resort`. Placing tracks whose
destination was decided before the library had a row to place is
`route pending`, and it is the only one of the four that can close a run.

## Three of them want the same three conditions

Routing writes playlist membership into the library database, so `route inbox`,
`route resort` and `route pending` check that the library is mounted, that
rekordbox is closed, and that the pins they depend on are intact. A refusal
names which of the three failed. Ask the health check rather than opening the
application to look, since opening it is the condition that makes the verb
refuse.

`route unplaced` is the exception. It only reads the database, so it is safe to
run with rekordbox open. It still needs the library mounted and the pins intact,
since the database is read through the same pinned binding. With `--export` it
writes a new file beside the export and opens no database at all.

```bash
crate doctor
```

Membership is the whole of what routing writes. No tempo value, no beat grid,
no BPM field, in any container, ever. If a routing result appears to have
changed a track's analysis, that is a defect and not a feature.

## The intake folder offers a plan, then stops

`route inbox` builds a plan of where each file sitting in the intake folder
goes, the folder and sub-playlist per file and the vocal sub it also files
into, and stops at a named gate before it writes anything. The gate shows that
plan, its counts, the trees the write goes into and any warning, so the answer
is given over what will be written. The gate is `route.inbox.apply`, it offers
`apply` and `abort`, and nothing answers it implicitly. Run it once to read the
plan, then answer:

```bash
crate route inbox
crate --decision route.inbox.apply=apply route inbox
```

Aborting is a recorded answer rather than a failure. The verb returns the same
plan with a no-op outcome, so a caller can tell "the person said no" apart from
"the run broke", which is a distinction a non-zero exit throws away.

The plan carries a digest over its own items, and the decision is bound to that
digest. Drop a file into the intake folder between reading the plan and
recording the answer and the decision is refused as stale, because it was made
against a plan that no longer describes the folder. The remedy is to plan again
and decide again. There is no flag that forces it through, deliberately.

## Answering a gate later, or from somewhere else

A decision passed on the command line only helps somebody sitting in front of
the run. When the run has already exited, the gate is state on the run and is
answered by naming it:

```bash
crate run show RUN_ID
crate run decide RUN_ID route.inbox.apply apply
crate --run RUN_ID route inbox
```

`run show` names the open gate and its declared options, so it is the verb to
reach for when the refusal scrolled past. The three routing verbs that write
also declare `write.cloudsync.unreadable`, which fires when the cloud sync state cannot be
read at all. It is explicit only, meaning it must be answered by name, and it
is worth reading before answering, because proceeding while that state is
unreadable is a decision about somebody else's copy of the library.

## What nothing places

`route unplaced` finds tracks in the collection that no governed tree places.
Run it before believing the library is filed, since a track that was never
placed produces no error anywhere; it simply is not in a folder.

```bash
crate route unplaced
crate --output json route unplaced
crate audit coverage --limit 200 /path/to/collection.xml
crate converge --tree TREE_ID
```

Those last two answer neighbouring questions and are not substitutes. Coverage
reports tracks the governed trees do not cover, a count you can bound. Converge
asks, per tree, whether declared membership matches what the database actually
holds. A library can be fully covered and still unconverged, so read the one
that matches the question you have.

## Reviewing what nothing places, through an export

On a library whose routing tree has not cut over to the database, the report
above compares nothing and says so. The export gives a review of where those
tracks belong, which you file by hand:

```bash
crate route unplaced --export /path/to/collection.xml
```

Every collection track that no playlist under the routing tree holds is routed
by the same decision the intake sweep makes, and the result is written to
`collection_placed.xml` beside the export. The export itself and the database
are never written, so this is safe with rekordbox open and asks no question
first. The file is the review, and nothing in it reaches the library through an
import, as the end of this section says.

A track filed anywhere under the tree is left where it is, even in a sub the
rules would not pick. A bucket with no sub yet gets one, and the answer lists
every sub it created. A missing genre folder is a warning, never invented. A
track whose file is not on this machine is a warning and is not placed. Ratings
are not set here; `route inbox --export` rates the intake.

The run ends ok and owes no import, because the file is a review rather than
something to import, and a `routing-not-landable` warning says so. Every
placement in it is a playlist nested inside the routing tree, and rekordbox
cannot land one from an xml file: a nested playlist imported on its own lands
at the playlist root as a new playlist, and a folder imported whole keeps what
it held and adds a second copy of every playlist inside it, and
`route unplaced` without `--export` only reports. File the tracks the review
names by hand in rekordbox. Until they are filed, the same command plans the
same placements on every fresh export.

`route inbox --export` follows the same rule for the intake. Its routing is
nested too, so it carries the same warning and owes no import. It ends waiting
only when it added tracks to the long track playlist, which sits at the
playlist root and is the one thing its file can land, and the import it names
is that playlist alone. Once that import lands, the next run over a fresh
export owes nothing.

## Resort shows its plan, then queues rather than sweeps

Changing a genre assignment or an energy band changes where already-filed
tracks belong. Before anything is queued, the resort reads the library without
writing and stops at the explicit gate `route.resort.apply`, showing every
track it will add by tree, folder, playlist and file, how many memberships it
will leave where they are, and which native trees it leaves alone. The gate is
answered by a separate recorded act, never inline, and the run is named again
to queue:

```bash
crate route resort
crate run decide RUN_ID route.resort.apply apply --actor NAME
crate --run RUN_ID route resort
```

A plan with nothing to add still asks, and then queues nothing. The answer is
pinned to the database file the plan read, so a rehearsal on a disposable copy
and the live run are compared by their digests. The approved adds are frozen
in the job: if the library or the taxonomy moves before the job is driven and
the resort would add anything else, it refuses with `resort-plan-stale` and
writes nothing, and the answer is to run it again and read the new plan.
A favourite whose track the resort itself files into a new genre folder only
becomes due after that write, so no plan could show it; the resort leaves it,
says so with a `resort-again` warning, and the next resort shows and files it.

The resort files only the routing tree. A native tree the taxonomy names as
something else, the intake flow above all, holds what the verbs that write it
put there, so the resort leaves it alone and says so with a
`tree-not-derived` warning; `crate rebuild` does the same, and refuses that
tree when it is named.

Sweeping the back catalogue is long work, so once approved this verb queues
a job and hands back its identifier instead of running the sweep inline. That
is the point rather than a limitation: an inline sweep that dies halfway leaves
no record of how far it got, and a job does.

```bash
crate job show JOB_ID
crate job resume JOB_ID
```

Queueing is not driving. `job resume` is what puts a queued job into a running
process, and a job nobody resumes sits in the queue indefinitely looking
healthy. Handing the identifier back to the verb reports that job rather than
queueing a second one:

```bash
crate route resort --job JOB_ID
crate job list --state queued --state blocked
crate job cancel JOB_ID
```

The resort adds and never removes. After a genre or a band change the track is
in its new playlist and still in its old one, because nothing in this product
deletes a playlist membership. The driven resort carries a
`membership-left-behind` warning naming each playlist and the file still in it,
so the person can take it out in rekordbox if it no longer belongs there. The
warning names the first twenty, counts the rest, and ends with the directory
the whole list is written in. A resort that failed part way says the same thing
as a step on its refusal. `crate converge` says whether a tree still differs.

`--state` is repeatable and refuses a state it does not recognise instead of
matching nothing, because a filter that silently matches nothing looks exactly
like an empty queue, and the next conclusion is that the job vanished. A
cancelled job reports as cancelled, never as failed.

## Pending is the gap between deciding and writing

Where a new track goes is decided during acquisition, when there is nothing in
the library to place. The row it needs appears later, when a person imports the
intake export, and that import is an act this product does not perform. So the
decision and the write are separated by a human step, and `route pending` is
the verb that closes the gap once the rows exist.

```bash
crate route pending
crate route pending --session SESSION_ID
```

With no `--session` it works every open run. Naming one works that run alone,
which is what you want when a single run is waiting on a person and the others
are not. When a run's outstanding set empties, that run closes, and closing
goes through the two guards that refuse a run still holding a track nowhere or
an export nobody imported.

Run it before the import and it resolves nothing, marks nothing, and says so.
Nothing is opened, no session is taken, and the state tree is left exactly as
it was found. That is fail-safe on purpose, and it is also why the report has
three answers rather than two. A track that reaches no row is waiting on the
import. A track that reaches a row the library has marked removed was deleted
on purpose. A destination the taxonomy no longer declares is a configuration
fix. Only the first is answered by importing again, so read which one you have
before repeating an act that cannot help.

## Reading the result somewhere else

Each of these emits a structured envelope, a plan for three of them and job
state for the resort. Take the JSON form whenever something other than a person
is reading the answer, since the human rendering is free to change and the
payload is not.

```bash
crate --output json route pending
crate status
```

`status` reports open runs and unconverged trees, which answers "is anything
waiting on me" rather than "file this now". It is the right first command when
you have walked back into a library somebody, including you, left mid-run.
