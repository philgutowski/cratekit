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
`route unplaced`. Re-placing tracks that are already filed, after a genre or an
energy band changed under them, is `route resort`. Placing tracks whose
destination was decided before the library had a row to place is
`route pending`, and it is the only one of the four that can close a run.

## Three of them want the same three conditions

Routing writes playlist membership into the library database, so `route inbox`,
`route resort` and `route pending` check that the library is mounted, that
rekordbox is closed, and that the pins they depend on are intact. A refusal
names which of the three failed. Ask the health check rather than opening the
application to look, since opening it is the condition that makes the verb
refuse.

`route unplaced` is the exception. It only reads, so it needs the library
mounted and nothing else, and it is safe to run with rekordbox open.

```bash
crate doctor
```

Membership is the whole of what routing writes. No tempo value, no beat grid,
no BPM field, in any container, ever. If a routing result appears to have
changed a track's analysis, that is a defect and not a feature.

## The intake folder offers a plan, then stops

`route inbox` builds a plan of what is sitting in the intake folder and stops
at a named gate before it writes anything. The gate is `route.inbox.apply`, it
offers `apply` and `abort`, and nothing answers it implicitly. Run it once to
read the plan, then answer:

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

## Resort queues rather than sweeps

Changing a genre assignment or an energy band changes where already-filed
tracks belong. Re-placing the back catalogue is long work, so this verb queues
a job and hands back its identifier instead of running the sweep inline. That
is the point rather than a limitation: an inline sweep that dies halfway leaves
no record of how far it got, and a job does.

```bash
crate route resort
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
