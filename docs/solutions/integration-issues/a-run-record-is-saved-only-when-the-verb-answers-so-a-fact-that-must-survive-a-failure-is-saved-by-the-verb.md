---
title: A run record is saved only when the verb answers, so a fact that must survive a failure is saved by the verb
date: 2026-11-01
category: integration-issues
module: src/cratekit/cli/__init__.py, src/cratekit/cli/gates.py, src/cratekit/cli/sync_land.py
problem_type: integration_issue
component: dispatcher
severity: medium
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A verb wants its own run id to mean something after it fails or is interrupted"
  - "A verb adds a field to RunState and expects it on disk"
symptoms:
  - "runs/<id>.json is missing, or lacks the new field, after a run that failed at a later step"
tags:
  - run-record
  - dispatcher
  - sync-land
---

# A run record is saved only when the verb answers, so a fact that must survive a failure is saved by the verb

## Context

U183 taught `crate sync land` to continue a pass by the land run's own id, which
needs the land run's record to name the pass it queued. The first reading was
that setting the field on `ctx.run` is enough, since the dispatcher writes the
record.

## What was learned

`_dispatched` in `src/cratekit/cli/__init__.py` calls `gates.save(state)` in two
places only: after the handler returns an envelope, and when a refusal's code is
a gate code. A refusal of any other kind (a failed step, an internal error) and
an interrupt write nothing, so a field set on `ctx.run` before such an ending is
lost, and the run's id continues nothing. That is exactly the run a person most
needs to continue.

A verb that needs a fact on disk whatever happens next saves the record itself,
the moment the fact is known (`sync_land._remember`). The dispatcher's later
save writes the same object again, so the two never disagree.

Two readers also met the record's shape for the first time: `RunState.from_json`
checks only the schema version, so a record that is not an object, or holds a
list where a mapping goes, raises `AttributeError` past every reader that
catches the gates module's refusals. `gates.load` now refuses a non object; a
reader that scans every record (the sync land resolver) also catches
`AttributeError`, and the doctor's run scan and `run retire` still do not,
recorded as a residual.
