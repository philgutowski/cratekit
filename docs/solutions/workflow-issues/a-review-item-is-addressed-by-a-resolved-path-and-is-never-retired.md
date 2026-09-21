---
title: A review item is addressed by a resolved path and is never retired, so its consumer checks the world
date: 2026-09-20
category: workflow-issues
module: src/cratekit/intake/repair_cli.py
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: logic_error
resolution_type: code_fix
applies_when:
  - A verb is being written that reads accepted items back out of the review queue and acts on files
  - The producer offered the item with an identity built from path.resolve()
  - The payload holds a value computed from the unresolved path, such as a proposed name
  - The verb will be run a second time over a queue whose accepted items it already carried out
symptoms:
  - A symlinked audio file is scanned by its link name and the apply renames the link's target, outside the library
  - The run after a successful apply reports every item it already carried out as missing or failed
  - A plan calls a rename applied when the source was deleted and an unrelated file holds the target name
  - Accepting the keep option renames the file anyway
related_components:
  - testing_framework
tags:
  - review-queue
  - path-repair
  - identity
  - idempotence
  - symlink
  - repair-paths
---

# A review item is addressed by a resolved path and is never retired

## Problem

U102 built the first consumer of the path repair queue, `repair paths --apply`.
Three of the ten findings the built in review raised came from one seam whose
rules are not written anywhere in `core/review.py`.

## What the seam actually guarantees

1. **An item has no identity field.** `Item` carries a payload and an item id.
   The identity it was offered under is read separately, `review.identity_of`,
   and it is `None` for an item that arrived by `review import`.
2. **The producer decides what the identity is, and `offer_repairs` stores
   `path.resolve()`.** The payload beside it, `recorded` and `proposed`, was
   computed from the path the scan SAW. For a symlinked file the two name
   different files, and the identity is the one a person was never shown.
3. **An accepted verdict is two facts.** The verdict is `accepted` and the
   option says which candidate. `keep` is an accepted verdict, and a verdict may
   be recorded with no option at all.
4. **Nothing retires an item.** There is `resolve` and `clear` and no consumed
   state, so every accepted item is still accepted on the next run, for ever.

## What a consumer therefore has to do

- Read accepted as the verdict AND the option together.
- Treat a missing identity as an item nobody can act on, and hold it.
- Cross check the identity against the payload before touching a file. Here
  that is `Path(identity).name == payload.recorded`, which fails exactly when
  the scanned file was a link.
- Hold any value that comes out of the payload to the shape the producer can
  make, since the store can be imported from an edited document. Here a
  proposed name must be a bare filename with the file's own suffix.
- Be idempotent against the WORLD, and claim only what was observed. Source
  gone with the target present is what an already applied rename looks like. It
  is also what a deleted file beside an unrelated file of that name looks like,
  and nothing can tell them apart, so the plan says which names exist and does
  not call either one applied.

## What is still open

R-625: the identity is the old path alone, so a new file landing there inherits
the verdict. Closing it needs a consumed state on the store or a file identity
in the payload.

## Related

- `a-confirm-gate-does-not-accept-review-items.md`, the same queue from the
  other side: a gate answer is not a verdict.
