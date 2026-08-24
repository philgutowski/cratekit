---
name: library-status
description: Find out what the library and the queue are doing, and answer a decision something is waiting on. Use when a verb exits saying a decision is required, when work seems stuck or queued and nothing is moving, when a job is blocked, failed, or needs resuming or cancelling, or when someone asks what is running, what is open, why nothing finished, or how to say yes to a confirmation the tool refused to take inline.
---

# Library status

Reading the state, and answering the one question a gated verb is parked on.

Nothing here changes the library. Three of these seven verbs report, three move a
job, and one records a decision. None of them writes a track, a playlist, or a
file.

## Two registers, two questions

`status` is about the library. `job list` is about the queue. They are not two
views of one thing, and reaching for the wrong one is why a stuck workflow looks
like nothing is wrong.

```bash
crate status
crate job list
```

`status` reports open runs, per source sync state, and what medium owns each
governed tree. `job list` reports queued work and what happened to it. A run is
one invocation's decision state and it survives the process that created it. A
job is work handed to a driver. They meet when a queued verb declares a gate,
which is the case the last two sections are about.

## The queue, filtered

Six states are declared: `queued`, `running`, `blocked`, `succeeded`, `failed`,
`cancelled`. `--state` is repeatable and refuses a name that is not one of them
rather than matching nothing, because a filter that silently returns an empty
list looks exactly like a queue with nothing in it, and the next conclusion a
person draws is that their job vanished.

```bash
crate job list --state blocked
crate job list --state queued --state running
```

`blocked` always carries a cause saying why. `cancelled` is its own state rather
than a flavour of `failed`, so a job somebody stopped on purpose stays
distinguishable from one that broke.

## One job, and why reading it always succeeds

```bash
crate job show JOB-ID
crate --output json job show JOB-ID
```

`job show` on a broken job exits 0 and carries the job's cause in the payload.
That is deliberate. If the verb's exit status mirrored the job's status, a caller
could not tell "this job failed" from "I could not read this job", which are
different problems with different fixes.

It also warns when the configuration moved since the job was queued. A job runs
against a frozen copy of its inputs, so an edit made afterwards does not reach
it, and the warning names which keys changed. Nothing refuses over this; the
point is that the setting you just edited is not the setting this run is using.

## Resuming and cancelling

```bash
crate job resume JOB-ID
crate job cancel JOB-ID
```

A resume reconciles before it does anything. A stored row that still says
`running` while nobody holds the job's lock describes a driver that was killed,
and believing the row would either refuse the resume for ever or double drive a
job whose lock is genuinely held. Disk truth is the lock, not the row. Completed
work is not repeated.

Cancelling exits 0 and reports the job as cancelled in the payload. A cancel that
exited non zero would be indistinguishable from a cancel that did not work.

## A gate is answered on the run, never inside the invocation

When a verb reaches a declared gate with nothing answering it, it exits 10,
`decision-required`, and the envelope carries the run identifier, the gate's
stable name, and the closed set of options. The run record persists, so the
answer can come later, from another process, another terminal, or another person.

```bash
crate run show RUN-ID
crate run decide RUN-ID restore.run.confirm restore --actor operator
```

`run decide` takes three positionals in this order: the run, the gate name
exactly as `run show` printed it, and one of that gate's declared options. It
refuses an option the gate does not offer, and it refuses a gate the run's verb
does not declare, naming the ones it does.

`--actor` is who is answering, and it is recorded alongside the decision. It
defaults to `cli`, which is honest about an unattended caller and is not what you
want on a destructive confirmation. Name the person.

## Why there is no flag that does this instead

An ordinary gate can be answered inline, by name, on the invocation that meets
it:

```bash
crate --decision profile.set.apply=apply profile set slim
```

An explicit gate cannot. It refuses even when `--decision` names it correctly,
and it refuses the same way on the next attempt, because R34 makes an explicit
assertion a separate deliberate act with a named actor recorded against it.
Answering it inline would reduce "this requires its own explicit assertion" to
typing one more flag on the command that was already running. There is no blanket
affirmative, no configuration key, and no environment variable anywhere in this
product that substitutes for `run decide`, and that absence is the design rather
than a gap somebody has not filled yet.

After deciding, continue the same run instead of starting a fresh one. A new
invocation mints a new run, meets the same gate with nothing recorded against it,
and refuses again.

```bash
crate --run RUN-ID restore run SESSION-ID
```

The flag goes before the verb path because it belongs to the root parser. A run
belongs to the invocation, not to the subcommand. A run also belongs to the verb
that created it, so continuing a different verb under that identifier is refused
rather than applying a decision to a question nobody asked.

## A decision can go stale

Exit 11, `decision-stale`, means the answer was recorded against an artifact that
has since changed. The digest a decision is checked against comes from what the
run offered, never from whoever is answering, because somebody deciding in a
later session cannot quote the identity of something they were shown by a process
that has already exited. Re-run the verb so it makes a fresh offer, read the new
plan, then decide again.

## Pending human action is not a failure

`run show` can exit 12, `pending-human`. The tool finished its half and something
has to happen outside it before the run is complete. That state names the verb
that proves it done, and it names the verbs it blocks, which then refuse until it
is verified. This is why an unfinished off-tool step cannot be quietly overtaken
by the next run.

`status` surfaces the same runs, so the queue and the pending action are visible
from one place without knowing a run identifier first.

## When something is stuck and you do not know where to look

Work outward from the library to the single gate, in this order, and stop at the
first one that answers.

```bash
crate status
crate job list --state blocked
crate job show JOB-ID
crate run show RUN-ID
```

If the answer is an open gate, `run decide` it and then resume the job. A queued
job whose verb declared an explicit gate carries the run its confirmation was
recorded against, so the child the driver spawns finds the decision already
there. A job frozen by an older build carries no such run and returns to the same
refusal rather than crashing, which is a signal to re-queue it rather than to
keep resuming it.

Reach for the JSON form whenever something other than a person is reading the
answer. The human rendering is free to change and the payload is not.

```bash
crate --output json status
crate --output json job list --state failed
```
