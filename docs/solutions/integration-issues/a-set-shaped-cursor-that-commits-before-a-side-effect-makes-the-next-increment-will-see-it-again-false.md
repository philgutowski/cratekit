---
title: A set-shaped cursor that commits before a side effect makes "the next increment will see it again" false
date: 2026-09-18
category: integration-issues
module: "src/cratekit/sync/playlists.py"
problem_type: integration_issue
component: sync
root_cause: incorrect_assumption
resolution_type: code_fix
severity: high
symptoms:
  - "A deferred side effect is skipped or refused and is never attempted again"
  - "The engine's docstring promises the next increment will see it, and it does not"
  - "Every test is green, because each drives one pass and the loss needs two"
  - "The retry set is taken from what this pass ADDED to a cursor rather than what the cursor HOLDS"
  - "The cursor was written at the top of the pass, before anything could have acted on it"
applies_when:
  - "A cursor or watermark records what has been handled, and a side effect is deferred until later in the same pass"
  - "The cursor is a SET of identifiers rather than a position in an ordered stream"
  - "Code derives a work set from what the pass newly recorded rather than from the whole record"
  - "A deferred-action engine documents that a skipped item comes back"
related_components:
  - "outbound"
  - "watermarks"
tags:
  - "cursor"
  - "watermark"
  - "deferred-side-effect"
  - "idempotence"
  - "green-suite"
  - "retry"
---

# A set-shaped cursor that commits before a side effect makes "the next increment will see it again" false

## Context

`sync/marks.py` exists so that an irreversible remote mark waits for proof the
local work finished. Its contract is three sentences, and the third is the one
that matters here:

> A failed recheck skips that mark rather than forcing it: the remote item
> changed, and the next increment will see it again.

That sentence is true of a POSITIONAL cursor. A stream reader that has not
advanced past an item reads it again next time, by construction, and the skip
costs nothing.

`sync.playlists` does not have a positional cursor. It has a SET: `reconcile`
reads the jobs this source queued, and writes the identifier of every playlist
whose job SUCCEEDED into a watermark. `plan` calls `reconcile` FIRST, at the top
of the pass, so that a playlist whose job finished since the last pass is
excluded as `recorded` in this one instead of being queued a second time. That
ordering is deliberate and correct for queueing.

It is fatal for a deferred mark. The obvious way to write the mark set is the
wrong way:

```python
pending = [
    marks.PendingMark(target_id=identity, kind=MARK_KIND)
    for identity in sweep.recorded_now          # what THIS pass added
    if listed.get(identity) and not is_swept_name(listed[identity])
]
```

`recorded_now` is the set the cursor gained in this pass. It is non empty
exactly once per playlist, in the pass that records it. By the time the mark
step runs, the cursor already holds that playlist, so the next pass excludes it
as `RECORDED` and reports `recorded_now` empty. If the mark did not land in that
one pass, and there are three ordinary ways it does not, nothing ever offers it
again.

## What it cost

Caught by the built in `/code-review` on the branch that introduced it, before
any caller existed, so the cost paid was a review round rather than an account
left wrong. What it would have cost, driven as a mutation row
(`S1_set_is_the_cursor` in `docs/mutation/r358.md`, 1 kill on the corrected
suite):

Three reachable paths lose the mark permanently.

1. The importable file is missing or empty, so `apply_deferred` refuses
   `sync-marks-blocked`. The cursor has already moved.
2. The recheck does not hold, because the playlist was renamed or removed on the
   account between the plan and the mark.
3. The rename raises, at the provider or part way through a batch.

In every one, the playlist is recorded, excluded as `recorded` for life, and
never carries the prefix. That is precisely the state the residual "A swept
playlist is never marked on the account" exists to remove, reintroduced by the
fix for it.

The suite could not see it. Every test drove ONE pass, and the loss only exists
across two.

## The fix

Take the set from what the cursor HOLDS, not from what the pass added to it, and
let the side effect's own trace be what removes an item from the set:

```python
def pending_marks(sweep: Sweep) -> tuple[marks.PendingMark, ...]:
    listed = sweep.names()
    return tuple(
        marks.PendingMark(target_id=identity, kind=MARK_KIND)
        for identity in sorted(sweep.recorded)   # the WHOLE cursor
        if listed.get(identity) and not is_swept_name(listed[identity])
    )
```

`Sweep` carries `recorded` alongside `recorded_now` so both facts are available
and named apart. A playlist the prefix reached is listed under a swept name, and
a swept name is skipped, so the set shrinks by exactly what landed. A mark that
did not land is an ordinary candidate on the next pass, with no retry ledger, no
second register and nothing to keep in sync.

The general shape: **when a cursor is a set, the thing that ends a retry has to
be observable in the world, not in the cursor.** A positional cursor gets to use
its own position as the retry state because the position and the work are the
same fact. A set cursor does not, and the substitute is a property of the
external system, read back.

## How to recognise it next time

Ask two questions of any deferred side effect near a cursor.

1. **Is the cursor a position or a set?** A set cursor cannot be un-advanced,
   and nothing in its type says so.
2. **What does the work set come from?** If it is the delta the pass just wrote,
   the work set is empty on every pass but one, and a single failure is
   permanent. If it is the whole record minus what the world says is done, a
   failure is an ordinary next-pass candidate.

And one about the engine. An engine promising "the next increment will see it
again" is promising something about its CALLER'S bookkeeping, not about itself.
`apply_deferred` cannot see the cursor and cannot keep that promise alone. The
first caller of an engine owns the engine's unreviewed contract as well as its
unreviewed failure paths.
