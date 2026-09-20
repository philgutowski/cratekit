---
title: "A queued verb has two exits, and an advisory attached to the envelope reaches only one of them"
date: 2026-09-20
category: workflow-issues
module: "src/cratekit/tagging/retag_cli.py, src/cratekit/tagging/shell.py, src/cratekit/analysis/cli.py"
problem_type: workflow_issue
component: cli_dispatcher
root_cause: incomplete_implementation
resolution_type: code_fix
applies_when:
  - "A queued verb is given a warning, a next step, or any per run advisory on its resume envelope"
  - "A verb writes part of a folder and something outside the product has to be reconciled afterwards"
  - "A resume path calls shell.advance, adopt.shell.resume, or modules.outbound.shell.resume"
  - "A residual is closed by telling a person what to do rather than by doing it"
symptoms:
  - "The advisory is asserted green in a test that drives a fully successful sweep and never appears on a run that failed part way"
  - "The exact scenario a residual describes, an interrupted run, is the one scenario the fix does not cover"
  - "A refusal envelope carries no warnings at all, and nothing in the suite notices"
  - "A cause arrives at the CLI with a shorter origin trail than the one the queue recorded"
related_components:
  - job_engine
  - error_handling
tags:
  - queued-verbs
  - job-resume
  - warnings
  - remediation-steps
  - r-225
  - partial-failure
  - cause-trail
---

# A queued verb has two exits, and an advisory attached to the envelope reaches only one of them

## Context

`crate tag retag` corrects a genre on a file and does not update the rekordbox
row, because the database half of the verb has no caller. R-185 has recorded that
split since 2026-08-26. The conservative close was to make the verb say the truth
and name the act a person takes, reload the folder's tags in rekordbox, so the
two halves can be reconciled by hand.

The obvious place to put that is a warning on the envelope, which is what
`analyze.restamp` already does for its own deferred half. So the first pass
attached it in `_resume`, beside the summary, gated on the count of files that
were actually corrected.

## The trap

**A queued verb's resume has two exits, and only one of them is an envelope.**

`cratekit.tagging.shell.advance` ends with:

```python
if not job.is_open() and job.cause is not None:
    raise CratekitError(job.cause)
```

That is R-225 and it is correct. A person whose folder was half corrected must
not be handed a normal envelope the dispatcher exits 0 over. The predicate is
deliberately "closed and carrying a cause" rather than "failed", because a run
stopped with a signal closes as CANCELLED.

The consequence is easy to miss and it inverts the whole point of the fix. A
warning attached after that call reaches every run **except** the one that did not
finish. And the run that did not finish is precisely the run R-185 describes: a
sweep interrupted after correcting some files, whose corrected files have stale
rows exactly as a completed sweep's do, and whose folder a second full run will
not select again because the files now look right.

So the fix covered the case that was already the least urgent and missed the case
it was written for, while a green suite agreed with it: every test driving the
advisory drove a sweep that succeeded. The failure path had its own tests, they
asserted item states and written genres, and nothing asked what the refusal told
the person to do next.

The same shape sits behind `cratekit.adopt.shell` and
`cratekit.modules.outbound.shell`, which are the other two copies of this resume,
so anything learned here applies to every queued verb in the repository.

## What to do instead

Decide where the advisory belongs on **both** exits before writing either.

On the success exit it is a warning on the envelope. On the failure exit there
are no warnings, because the non-success envelope's shape is a structured cause,
and what a person does next is what `Remediation.steps` is for. Catch the error,
ask the same question about what actually ran, and extend the cause:

```python
try:
    job, warnings = shell.advance(...)
except CratekitError as failed:
    if not _summary(cfg, ctx.args.job)["corrected"]:
        raise
    raise with_reload_step(failed, folder) from failed
```

Two rules make that extension safe.

**Extend the cause, never rebuild it.** `Cause.origin` is append-only, and a
cause arriving at the CLI with a one-element trail means some hop caught it and
re-created it, losing `inner`, `detail`, `scope` and `retryable` with everything
below. `dataclasses.replace` on the cause and on its remediation carries all of
them through by construction. A hand-built `Cause` with a plausible origin passes
a naive test and destroys the trail.

**Gate both exits on the same measurement, and read it from what ran.** The
committed per item artifacts say what was written; the confirmed plan says what
somebody agreed to look at. A refusal that appended the advisory unconditionally
would send a person to reconcile a library against a sweep that refused on its
first item and wrote nothing.

## How to notice it next time

The assertion that catches this is not about the advisory, it is about the
population of endings. When a verb queues, it has at least three moments a person
can read: the queueing envelope, a resume that finished, and a resume that did
not. Write the case for the third one first, because it is the one the success
path's test will not cover and the one a residual about partial state is usually
about.

A mutation row makes it concrete. Deleting the `except` clause must kill a test;
if it kills nothing, the failure exit has no reader.

And when extending a cause, assert against the cause the queue recorded rather
than against words written in the test:

```python
stored = job_cause(job_id)
assert tuple(refused["cause"]["origin"])[: len(stored.origin)] == stored.origin
assert steps[: len(stored.remediation.steps)] == list(stored.remediation.steps)
```

The first version of that assertion checked only that the trail's first and last
elements differed, which a rebuilt two-element origin satisfies. It measured
zero on the mutation row that rebuilt the cause, which is how the weakness was
found rather than argued.
