---
title: "A verb that queues another verb's job must hand it a run that verb owns"
date: 2026-09-10
category: integration-issues
module: src/cratekit/cli/gates.py
problem_type: integration_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - "A verb queues a job under ANOTHER verb's handler key, as a composer does"
  - "The job's own verb declares an explicit gate and its argv builder emits the root --run flag"
  - "A brief says to declare the same gate on the composing verb so a person is asked once"
symptoms:
  - "The composed job queues cleanly and its resume exits decision-unknown-gate on every respawn"
  - "The refusal says the run belongs to one verb, not to another"
related_components:
  - testing_framework
tags:
  - explicit-gate
  - job-resume
  - run-identity
  - composer
  - hand-off
---

# A verb that queues another verb's job must hand it a run that verb owns

## Context

U61 made `crate sync all` a composer. It queues each source's own job under that
source's own handler key, so the workers `sync labels` and `sync favorites`
already had run what it queues. The brief recommended that `sync.all` declare the
favourites confirm on its own entry, so a person running a pass is asked once. It
did not say which run the queued favourites job should carry as its gate run.

The obvious answer is the pass's own run, and it is the one the existing
learning points at:
[a queued verb with an explicit gate must freeze its run](../workflow-issues/an-explicit-gate-makes-a-queued-job-undriveable-without-the-run-id.md).
Freeze `ctx.run.run_id`, emit it as `--run`, done. For a composer that is exactly
wrong.

## Why the obvious answer stalls

`_run_state_for` in `src/cratekit/cli/__init__.py` loads the run named on `--run`
and refuses when the record's `verb` is not the verb being run: "run R belongs to
sync.all, not to sync.favorites". The favourites job's resume is
`sync_favorites_argv`, which emits `--run <gate run> sync favorites --job ...`.
With the composer's run frozen there, the child is refused before it reaches its
gate, every respawn, identically. It is the stall the earlier learning describes,
reached from the other side: there the run was missing, here it is present and
owned by the wrong verb.

A second trap sits beside it. `run decide` resolves the gate against the run's
OWN verb's entry, so a decision for `sync.favorites.confirm` cannot be recorded
on a `sync.all` run at all, and naming the composer's gate `sync.favorites.confirm`
would not help either: `registry.gate(name)` returns the first entry declaring a
name, and `sync.all` is declared before `sync.favorites`.

## What was done

`Gates.hand_off(spec, verb=, gate=)` in `src/cratekit/cli/gates.py`. After the
composer's own explicit gate returns, it mints a new run whose `verb` is the
target verb, copies the recorded decision into it under the target gate's name
with the same option, actor, time and digest, saves it, and returns its id. The
composer freezes THAT id as the job's gate run. The resumed child loads a run it
owns, finds its gate answered, and rebuilds the digest from the frozen payload,
so a plan that moved still meets `DecisionStale`.

It copies an answer and never supplies one. It refuses unless the source gate
holds a recorded decision with a digest, and unless the target verb declares the
target gate offering that option and comparing a digest. Each layer has its own
case in `tests/test_sync_all.py`, including a synthetic gate for the digest
layer, because no real gate offers the option without comparing a digest.

The run owned by the composer keeps its own role: its id is the INTAKE run every
job in the pass carries as `run_id`, so the workers write one intake file (R29).
Two runs per favourites job, on two payload keys, which is the split
`sync_favorites_argv`'s docstring already insists on.

## When to apply

- Any verb that queues work under a handler key other than its own. Ask which run
  the job's resume will load, and who owns that run.
- Drive the queued job through `cli_jobs.argv_for(job)` and the real dispatcher,
  not through the queueing verb. `test_the_jobs_a_pass_queues_run_to_done_through_the_existing_workers`
  does. The mutation that freezes the composer's own run, row G4 in
  `docs/mutation/u61-rows.toml`, is expected to fail there, and that is an
  expectation: the table was not measured (R-329).
- The handed run carries no record that it was handed, which is R-331.
