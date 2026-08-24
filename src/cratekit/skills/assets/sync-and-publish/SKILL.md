---
name: sync-and-publish
description: Bring the library current from every enabled source, and publish one library playlist back out to a streaming account. Use when someone says sync, catch up the library, pull what is new, sync my hearted tracks or favourites, or export a playlist, and when a queued sync or export sits at a confirm gate, exits asking for a decision, or refuses the same way on every resume.
---

# Sync and publish

Two directions across one queue. Inward is every enabled source's increment.
Outward is a playlist written to a streaming account, add only, and only after
somebody confirms it.

Nothing here is required to use the product. These verbs run from the command
line without any skill installed, and this exists so the queueing model, the
gates, and the add-only rule are not things a person has to infer from a
refusal.

## Sync queues, it does not run

`crate sync all` freezes the configuration, queues one increment job per source
the active profile enables, and reports what it queued. There is no monolithic
gated run to sit and watch, so the verb returning almost immediately is the
design rather than a failure.

```bash
crate status
crate sync all
```

Run the status verb first. It answers per source sync state, open runs, and
unconverged trees, which is what says whether the last increment finished
cleanly before you queue another one on top of it.

Every job queued by one invocation shares a single run identifier, so all the
sources append to one importable file instead of producing one apiece. That
shared run is the reason an incremental sync never multiplies the hand import,
and it is why queueing sources one at a time by hand costs you an import per
source.

Which sources exist is a property of the profile, not of this verb. A slim
profile queues fewer jobs and reports fewer, and that is the profile answering,
not the sync failing.

## Driving the queue

The queue is the thing to watch after `sync all` returns.

```bash
crate job list --state queued --state running
crate job show JOB-ID
crate job resume JOB-ID
crate job cancel JOB-ID
```

`--state` is repeatable and refuses a state it does not declare rather than
matching nothing, because a filter that silently matches nothing looks exactly
like an empty queue and the next move is to conclude the job vanished. The
declared states are queued, running, blocked, succeeded, failed, and cancelled.
Cancelled is its own state rather than a flavour of failed, so a job somebody
stopped on purpose is never read as one that broke.

`--job` on a sync verb does not start anything. It reconciles the increment
already queued under that identifier, which is what a resume re-invokes.

```bash
crate sync all --job JOB-ID
```

## A cursor advances only on a clean pass

Each source keeps a cursor recording its last clean completion. It advances only
when every item that was in scope finished without error, so a partial failure
leaves it where it was and the next increment covers that ground again. That is
deliberate. The cursor is an audit record of how far a source got, not a floor
the next run filters by, and treating it as a floor is how a failed item becomes
permanently invisible.

A source whose every listing call failed raises rather than recording an empty
pass, because "nothing new" and "could not ask" are different answers and only
one of them should move a cursor.

## Favourites move both ways, and neither way removes

`crate sync favorites` is two halves. Locally it colours, tags, and places the
hearted tracks the library already holds, and acquires the ones it does not into
the same shared intake file. Remotely it hearts the local favourites back on the
account.

```bash
crate sync favorites
crate sync favorites --run-id SHARED-RUN-ID
```

Neither half removes anything, and that is structural rather than a default. The
heart-back engine has no remove path at all, and an argument whose name sounds
like one is recognised and then ignored, so no combination of inputs un-hearts a
track or un-colours a row. The reason is worth carrying: a heart marks a
favourite rather than ownership, un-hearting is a one tap action, and mirroring
a removal would cost a downloaded file for a fingertip.

`--run-id` is this verb's own argument and carries the intake run shared with
the other sources in a sync. It is not the root `--run` flag, which carries the
run a gate decision was recorded against. Two different runs travel with this
verb, and conflating them is how a confirmed sync ends up in the queue with
nothing able to advance it.

## The confirm gates

Favourites sync and playlist export each declare a confirm gate before anything
reaches the account, and both are explicit. Explicit means there is no blanket
affirmative anywhere: no config key, no environment variable, no flag that says
yes to everything. Each gate is answered by name, on one run.

Answer it on the invocation when you are the one running it:

```bash
crate --decision sync.favorites.confirm=sync sync favorites
crate --decision export.playlist.confirm=export export playlist PLAYLIST-KEY
```

Or let it refuse and answer afterwards, which is the case that actually matters:
a detached job parked at a gate, a run that exited hours ago, a second person on
the same library.

```bash
crate run show RUN-ID
crate run decide RUN-ID sync.favorites.confirm sync --actor NAMED-OPERATOR
```

An unanswered gate exits with a decision-required code carrying the gate name,
its options, and the run identifier, so read the refusal rather than guessing
what the gate is called. The answer is recorded with the actor who gave it and
against the digest of the plan that was offered. If the plan moves, the decision
reads as stale and the gate asks again rather than applying yesterday's yes to a
run that has since grown.

## The other gate favourites can reach

Favourites sync writes rekordbox rows, so it can also reach the shared gate
raised when the guarded writer cannot read Cloud Library Sync state. Its options
are proceed and abort, and it is explicit for the same reason the confirms are:
going past a guard that could not rule out a second writer is a per run act by a
named actor, never a setting.

Do not answer that one by reflex. Run the health check, leave the application
closed while these verbs write, and read "could not read the state" as unknown
rather than as safe.

```bash
crate doctor
```

## Export is add only, and it confirms before it writes

`crate export playlist` takes the stable identifier of a library playlist, never
its title, and refuses when the identifier is missing rather than guessing.
Tracks the service cannot match are reported instead of being silently dropped,
so the report is the thing to read afterwards, not the count.

```bash
crate export playlist PLAYLIST-KEY
crate --output json export playlist PLAYLIST-KEY
```

Reach for the JSON form when something other than a person is reading the
result, because the human rendering is free to change and the payload is not.

A re-export of the same local playlist updates the remote playlist this library
already wrote rather than creating a second one, because the outbound ledger
holds the remote identifier. That ledger survives a library rollback on purpose.
The account does not roll back with the library, and a forgotten remote
identifier is exactly how the next export duplicates everything. Each added
track is recorded before the next write, so an interrupted export resumes
without adding anything twice.

## When a resume refuses the same way every time

A resumed export or favourites sync carries the run its confirmation was
recorded against, so the respawned process meets the gate with the decision
already in place. A job frozen by an older build carries no such run, resumes
without it, mints a fresh one, and exits decision-required again, forever. The
symptom is a job that is confirmed and still cannot move.

Cancel it and queue a new one rather than resuming it a fourth time.

```bash
crate job show JOB-ID
crate job cancel JOB-ID
crate sync favorites
```

## What lands locally

A sync run writes one importable file into the staging directory, named for the
run, and every source in that run appends to it. The file is registered when it
is created and counts as intake only once it is marked complete, so debris left
behind by a crash is not picked up by the next run. While the import is still
owed, it surfaces as a pending human action on the run rather than as a line of
output that scrolls away.

```bash
crate run show RUN-ID
crate status
```

Remote marks are held back until that local file exists and is non-empty, and
they are rechecked before they are applied. Marking the account first is how a
crash leaves the service believing the run finished while the library has
nothing to import.
