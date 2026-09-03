---
title: The memo write that suppresses retry goes after every write it is a memo about
date: 2026-09-02
category: workflow-issues
module: src/cratekit/adopt/apply_cli.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: missing_workflow_step
resolution_type: code_fix
applies_when:
  - A worker performs two writes against different stores in one handler, one of which is a durable record (a ledger, an applied-flag, a checkpoint) and one of which is the actual effect (a database row, a file, a tag)
  - The durable record's only job is to stop a future run from repeating the work
  - The two writes cannot be wrapped in one transaction, because they target different sessions or different systems
  - A retry or resume path exists that decides what remains outstanding by reading the durable record rather than by re-deriving it from source
symptoms:
  - A re-run reports everything as already done while the target system shows the effect never landed
  - The gap is permanent rather than self-healing on retry, because the thing that would have prompted the retry was itself marked complete
  - A code review of either write alone looks correct; the defect is only visible in the pair and the order between them
related_components:
  - service_layer
  - database
tags:
  - write-ordering
  - idempotency
  - resume
  - r148
  - u55
  - adopt
---

# The memo write that suppresses retry goes after every write it is a memo about

## Context

`U55` (`src/cratekit/adopt/apply_cli.py`, `handle`) landed the write half of
adoption: one worker session writes tree membership rows into the person's
rekordbox database, and a second, separate write marks those entries applied in
`apply.outstanding`'s ledger. The two cannot share a transaction —
`write_tree_membership` (`src/cratekit/write/trees.py`) opens its own session and
refuses a caller-supplied gates factory, and `apply_plan`'s applied-ledger write
runs in a session of its own, opened after the membership session has closed
(`src/cratekit/adopt/apply_cli.py:33`, the module docstring on why sessions never
nest here).

The first draft of `handle` applied the ledger write, then wrote memberships.
Driven against a library whose taxonomy tree had not been cut over yet
(`tree_registry.record_cutover` never called, which is the ordinary case — see
R-235), the membership write did nothing because the tree wasn't eligible, but
the ledger write had already marked every entry as applied. The next run read
the ledger, found nothing outstanding, and queued nothing. The gap was
permanent: nothing about the failure was retryable, because the record that
would have told a future run "this is still outstanding" had already been
overwritten to say the opposite. This is R-148's hazard — a ledger claiming the
library holds something it does not — reappearing in a second shape once the
reader that made the write reachable actually landed. Reading alone did not
surface it; only driving the two-write sequence against an uncut-over library
did (commit `df166b6`).

The code review that followed the fix then found the same hazard in a third
shape: `write_tree_membership` correctly `SURFACES` (returns, not raises) a row
it could not resolve to exactly one active library row, rather than aborting the
whole session over one bad file. The caller was marking every outstanding entry
applied regardless, including the surfaced ones — so a track that never reached
a playlist was recorded as adopted anyway. `_refuse_unplaced` now raises before
anything is marked whenever `membership.skipped` is non-empty, naming the rows,
so a re-run reports the rows that did land as `already_present` and marks only
those (commit `274b36f`).

## Guidance

When one handler makes two writes to different stores, and one of those writes
is purely a memo — its only effect is to make a future run treat the work as
already done — order them so the memo write is last, after every write it is a
memo about:

1. **Perform the recoverable, repeatable write first.** It is safe to redo:
   running it again over rows that already landed is a no-op or reports
   `already_present`, not a duplicate or a corruption.
2. **Perform the memo write last, and only after the recoverable write is
   confirmed.** If the recoverable write skips or fails part of its work,
   refuse before the memo write happens at all — do not mark the parts that did
   land and silently drop the parts that didn't (`_refuse_unplaced` in
   `apply_cli.py` is the pattern: it raises rather than partially marking).
3. **Derive the memo write's content from the durable plan, not from what this
   particular run happened to touch.** `apply_cli.py`'s membership mapping is
   built from `plan_engine`'s plan, not from a running tally the handler
   accumulates — so a kill between the two writes costs exactly one re-run that
   re-derives the same mapping and finds every row already present, rather than
   losing track of what still needs marking.

The general shape: whichever write is the note saying "do not do this again"
goes after every write it is a note about. If the two writes are reversed, a
partial or failed first write still gets marked complete, and no future run has
any signal that work remains.

## Why This Matters

The failure this produces does not look like a crash. Every run reports OK.
Ruff, pytest, and a code review of either write in isolation all pass, because
the defect is not in either write — it's in the pair and the order between
them. It surfaces only when the target write's precondition fails in a way the
handler doesn't already guard against (here: an un-cut-over tree), which is
exactly the kind of state a fixture built to exercise the happy path won't
reach. The cost is silent and permanent data loss in the domain the ledger is
supposed to protect against: a person's rekordbox library ends up missing
memberships the tool believes it already wrote, and nothing about the system
will ever ask again.

## When to Apply

- Reviewing or writing any handler that performs two writes to different
  systems where one is an effect and the other is a completion record for that
  effect.
- Any resume or retry path whose "what's left to do" query reads a durable
  record instead of re-deriving state from the actual target system.
- Particularly relevant to `cratekit`'s job engine handlers
  (`src/cratekit/core/jobs.py`), where a worker's report of `done` is what
  future drives trust; a worker that reports done before its effect is
  confirmed breaks that trust invisibly.

## Examples

Before (the first draft, R-148 reappearing):

```python
# apply_plan() marks the ledger, THEN memberships are written
report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
membership = _write_memberships(cfg, plan, declared)
# a membership write that lands nothing (uncut-over tree) is invisible:
# the ledger above already says every entry is applied
```

After (`src/cratekit/adopt/apply_cli.py`, `handle`, current tree):

```python
membership = _write_memberships(cfg, plan, declared)
_refuse_unplaced(membership, job, cfg)  # raises before anything is marked
                                          # if any row could not be placed
report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
```

`_refuse_unplaced` closes the second shape of the same hazard: it refuses
rather than letting the ledger write mark rows `write_tree_membership` itself
reported as unresolved, so a re-run recovers instead of silently dropping them.
