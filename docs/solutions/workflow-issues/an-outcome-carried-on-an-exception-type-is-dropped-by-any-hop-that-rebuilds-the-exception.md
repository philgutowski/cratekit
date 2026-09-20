---
title: "An outcome carried on an exception type is dropped by any hop that rebuilds the exception"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/core/jobs.py, src/cratekit/core/cause.py, src/cratekit/cli/__init__.py, src/cratekit/tagging/retag_cli.py, src/cratekit/backup/cli.py"
problem_type: workflow_issue
component: cli_dispatcher
root_cause: incomplete_implementation
resolution_type: code_fix
applies_when:
  - "A queued verb's resume is given a new way to end, or jobs gain a new state"
  - "An except CratekitError between a shell and the dispatcher raises a new CratekitError built from the old cause"
  - "A population test drives every verb with one shared fake worker"
  - "A predicate over job state is about to be written in a verb's shell rather than called from core.jobs"
symptoms:
  - "A cherry-pick of a job outcome fix conflicts in a shell that gained a refusal helper since"
  - "A job whose state is blocked leaves its verb with outcome ok and exit 0, the block legible only inside data.cause"
  - "A job whose state is blocked leaves one verb with outcome failed while every other verb says blocked"
  - "A population test over every handler key is green while one verb is wrong"
related_components:
  - job_engine
  - error_handling
tags:
  - queued-verbs
  - job-resume
  - blocked
  - exception-type
  - population-test
  - r-290
  - r-225
---

# An outcome carried on an exception type is dropped by any hop that rebuilds the exception

## Context

R-290: a parked job reported `outcome: ok` and exit 0 in every queued verb.
`jobs.drive` returns normally when a worker raises `jobs.Parked`, and the job it
returns is `blocked`.

## The first trap: `blocked` is an OPEN state

Ten shells carried the same two lines, copied from `backup`:

```python
if not job.is_open() and job.cause is not None:
    raise CratekitError(job.cause)
```

The ledger read this as thirteen shells each forgetting the blocked case. That
is not what happened. `JobState.BLOCKED` is not terminal, a parked job is meant
to be driven again, so `is_open()` is true and the predicate cannot fire. No
copy was wrong when it was written and every copy was wrong afterwards. A rule
about job state that lives in a shell cannot learn about a state added later,
which is why it now lives in `jobs.raise_for_state` and a static test refuses
any condition outside `core/jobs.py` that reads both `is_open` and `cause`.

## The second trap: the bit rides the type

A parked job's cause is the adapter's own, `auth-failed` or
`provider-blocked`, and the same slugs fail single items in jobs that never
parked. Nothing on the cause says "the job is parked". So `raise_for_state`
raises `cause.JobBlocked`, a `CratekitError` subclass, and the dispatcher reads
the TYPE as `Outcome.BLOCKED`. `jobs.Parked` made the same choice for the same
reason one layer down.

The cost of that choice is that the outcome now survives only as long as the
exception object does. `tagging.retag_cli` catches the shell's refusal to append
a remediation step and raised `CratekitError(replace(cause, ...))`. Correct for
the cause, and it silently turned `blocked` into `failed`.

## Why the population test did not see it

The population test drives every key in `handlers.HANDLERS` with one shared
worker that parks on its first item. A worker that parks first has corrected
nothing, and retag only rebuilds its refusal when something WAS corrected, so
the rebuilt path never ran. A population test proves the property over the
population of verbs and says nothing about the branches inside one verb. The
built in review found it by reading the `except`.

## It happened twice, one merge apart

The unit that fixed retag sat unmerged for a day. When it was rebuilt on a later
`main`, `backup` had gained a rehearsal, and with it `_with_rehearsal_step`,
which rebuilds a refusal to add a sentence and built a plain `CratekitError`.
That hop was written by copying retag's, from a `main` where retag had not been
fixed yet. It surfaced only as a merge conflict, and the population test was
green over it for the same reason as before: the job it queues is not a
rehearsal, and a real run is handed back object for object.

A rule stated in a docstring did not survive one merge. So the rebuild has one
owner now, `cause.rebuilt(error, new_cause)`, and a static test in
`tests/test_job_outcome.py` refuses `CratekitError(replace(...))` spelled by
hand anywhere outside `core/cause.py`, and refuses `JobBlocked` or
`JobCancelled` constructed anywhere outside `core/jobs.py`.

## What to do

- A new job ending goes in `jobs.raise_for_state`, never in a shell.
- A refusal reworded on its way out goes through `cause.rebuilt`, never through
  a new `CratekitError`. The static test enforces the spelling it knows. It
  cannot see a rebuild that hand builds a `Cause` field by field, so still read
  the hop.
- `rebuilt` keeps ONLY the two carried types and flattens every other subclass,
  on purpose: eleven of the seventeen `CratekitError` subclasses override
  `__init__` with arguments of their own, so `type(error)(cause)` is not a call
  anything can promise.
- A static guard that matches "the mapping is a plain statement" refuses a verb
  that must word its own exit. The guard takes a `try` holding nothing but the
  mapping, only when every handler ends in a raise or in a call its module
  annotates `NoReturn`. A handler that can fall through is the defect itself.
- Before trusting a green population test, `git grep -n "except CratekitError"`
  in the modules between the shell and the dispatcher and read each one.
- `JobBlocked` is in `core.cause`, not `core.jobs`, because `cli/__init__`
  cannot import `core.jobs`: the engine imports the CLI package for the
  envelope. Do not move it.

Related: `a-queued-verb-has-two-exits-and-an-advisory-on-the-envelope-only-reaches-one.md`,
which is the same seam met from the warnings side.
