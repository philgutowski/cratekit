---
title: A composer that drives other verbs' jobs must read the queue, and the queue lists newest first
date: 2026-10-28
category: integration-issues
module: src/cratekit/cli/sync_land.py, src/cratekit/core/jobs.py
problem_type: integration_issue
component: job_engine
severity: high
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A verb drives jobs that other verbs queued and decides what happened from the result"
  - "A verb picks one job out of jobs.list_jobs by a payload field"
  - "A verb asks whether an earlier pass, or a person, left work open"
symptoms:
  - "A continued pass reads an older failed job over the same list and reports nothing landed while a newer job landed every track"
  - "A pass reports clean while an intake job outside its own run sits queued and holds its playlist out of every later pass"
tags:
  - job-engine
  - composer
  - sync-land
  - list-jobs
---

# A composer that drives other verbs' jobs must read the queue, and the queue lists newest first

## Context

U152 built `crate sync land`, which runs the existing verbs through the dispatcher
in process and drives every job they queue through that job's own `--job` command.
Two things it got wrong at first were not visible in the code it called.

## What was learned

**`jobs.list_jobs` is newest first** (`ORDER BY created DESC`). The first version
looked for the download job over a list with `reversed(jobs.list_jobs(store))`,
believing it was walking newest first, and so read the OLDEST job. A pass whose
first download refused every track, followed by a download typed by hand that
landed them, was continued over the old job and reported nothing landed. Take the
first match of `list_jobs` for the newest.

**A command's exit is not the job's state.** A `--job` command can answer without
driving the job at all: a live driver elsewhere holds it, and the command refuses
`job-driver-held` while the row stays `queued` with no cause. Read the job off the
queue after the command, and when it is still open (and not parked), end on the
command's own refusal; `jobs.raise_for_state` over an open row raises nothing, and
the result is an internal error over a row that says nothing.

**`sync all` leaves out what is already in flight, and says so only on an info
row.** A playlist with an open intake job, queued by an earlier pass or by `crate
intake playlist` by hand with no run at all, is excluded from the next pass for as
long as that job is open. A composer that drives only its own run's jobs has to
look at the open intake jobs of the library itself and name each one it leaves,
or that playlist is never acquired and nothing says so.

**A step's gate is not the composer's gate.** Re-raising a child's
`decision-required` or `decision-stale` cause from the composer makes the
dispatcher mark the composer's run resumable over a question it never declared.
Test `cause.code in gates.GATE_CODES` and end the pass for a person, naming the
step's own run.

## When to apply

Any verb that chains other verbs and their jobs. `tests/test_sync_land.py` drives
each of these, and rows R5, R9, R10, R15 and R3 in `docs/mutation/u152-rows.toml`
pin them.
