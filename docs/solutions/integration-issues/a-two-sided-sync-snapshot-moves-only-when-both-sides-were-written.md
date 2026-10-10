---
title: "A two sided sync's snapshot moves only when both sides were written, or a skipped side undoes the other side's removal"
date: 2026-10-10
category: integration-issues
module: src/cratekit/sync/pair_cli.py, src/cratekit/modules/outbound/pairs.py
problem_type: integration_issue
component: sync_pair
severity: high
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A sync keeps two stores the same list and merges each against what it held at the last sync"
  - "One side of such a sync can be declined, skipped, fail part way, or be read short"
  - "A per side base is being recorded as soon as that side is written"
symptoms:
  - "A track removed on one side comes back on the next sync"
  - "A withheld or skipped track reads as an addition and beats a real removal"
related_components:
  - "account"
  - "rekordbox"
tags:
  - sync-pair
  - three-way-merge
  - snapshot
  - u130
---

# A two sided sync's snapshot moves only when both sides were written, or a skipped side undoes the other side's removal

## Context

U130's `crate sync pair` keeps an account playlist and a rekordbox playlist one
list. Each sync merges each side against what that side held at the last sync,
and an addition on either side beats a removal. The first build recorded each
side's snapshot as soon as that side was written, on the reasoning that a side
that was not written "has not changed" and keeps its old base.

## What went wrong

That reasoning holds for the side that was not written and breaks the merge as
a whole. The `/code-review` pass on the branch drove three cases to the same
end:

- A first sync with the account side skipped recorded the rekordbox base and no
  account base. The next sync read the missing account base as empty, so every
  account track counted as added, and a track the author had since removed in
  rekordbox was put back.
- A short account listing recorded an account base without the withheld track.
  When the provider served it again it read as added on the account and beat a
  rekordbox removal.
- Patching the first case with "owed removals", which kept a removed track in
  the other side's base, fixed membership. It still consumed an order change
  the skipped side never received.

## The rule

The snapshot moves only when the whole pair was written: both gates applied,
every write landed, and the account listed the whole playlist. Then both sides
are recorded together. Anything less records only the links the plan learned,
and leaves the snapshot where it was. The next sync then merges against the
same last sync, so every change either side made since is still a change, and
it finishes what the short sync did not. A first sync that did not finish is
still a first sync, which only adds.

Replaying from the old base is safe because the merge is a function of what
each side holds now. A side that was written holds the merged list, and those
tracks read as additions that both sides agree on or as removals both sides
agree on. The one case a replay cannot repair, a reorder that failed part way,
changes only order and is a residual.

## How to apply

- Do not record one side's base on its own. Record both, or record neither.
- Treat an incomplete read, such as a provider withholding tracks it counts, as
  an incomplete sync. Do not let the base learn from it, and do not offer the
  unseen tracks back as additions.
- Measure the base on every membership row, duplicates included. A re-add then
  means that none of the old rows survives, not that the first row changed.
