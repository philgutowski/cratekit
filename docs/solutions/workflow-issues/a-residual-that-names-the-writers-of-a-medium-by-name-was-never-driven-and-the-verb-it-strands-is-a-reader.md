---
title: A residual that names the writers of a medium by name was never driven, and the verb a second medium strands is a reader
date: 2026-09-30
category: workflow-issues
module: "src/cratekit/intake/ingest.py, src/cratekit/intake/file_cli.py, src/cratekit/intake/land_cli.py, src/cratekit/sync/mark_cli.py, src/cratekit/core/tree_registry.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: unverified_assumption
resolution_type: workflow_improvement
applies_when:
  - "A brief or a residual lists the verbs a guard refuses, and its measured cost line says it was read off a list or a suffix rather than driven"
  - "A tree, a file or a store gains a second medium, and the unit is scoped as every writer of the first medium"
  - "A refusal has to name a verb, and the guard it replaces lives in the write layer or the core"
symptoms:
  - "The brief names five writers and a grep for the guarded function finds two callers and one verb"
  - "Every named writer is handled and a workflow still cannot finish on the new medium"
  - "A refusal that names a verb is about to be added beside a guard in a layer that names none"
tags:
  - "intake"
  - "tree-registry"
  - "medium"
  - "residual"
  - "reachability"
  - "layering"
  - "R-770"
  - "R-777"
---

# A residual that names writers by name was never driven, and the stranded verb is a reader

## What happened

R-770 said that once the intake tree cuts over, `intake file`, `sync favorites`,
`sync all`, the label batch and every other verb that writes an intake playlist
refuses as a defect, because each goes through `rbxml.insert_intake_playlist`.
Its own measured cost line said the list was read off the emitter guard and the
suffixes `pending_intake_xml` walks.

Driven, the list was one verb long. `git grep insert_intake_playlist -- src`
finds two callers, `ingest.place_files` and the landing's pre-move check, and
one verb besides the landing reaches them, `intake file`. `sync favorites`
hearts on the account. `sync all` queues sources. `sync labels` offers
releases for review. None of them has ever spliced an intake playlist. The
suffixes named files, some of them written only by the source system.

The verb a native intake tree actually strands was not on the list and is not
a writer. `sync mark` reads the intake file a bridge landing writes, to learn
the pass's name and what landed. A native landing writes no such file. That
is R-777.

## Why it was easy to miss

- The residual was filed by the unit that built the second medium, from the
  writer's side: it asked who else writes what it had just stopped writing.
- A second medium removes an ARTIFACT, the intake file. The verbs that break
  are whoever depends on the artifact existing, and a reader depends on it
  as much as a writer does.
- The pending suffix list looks like a list of writers. It is a list of names
  a scan checks for.

## What to do next time

- **Before planning against a list of affected verbs, grep the guarded
  function's callers and walk each up to a verb.** It took three greps here
  and changed the unit from five verbs to one.
- **Then ask the other question: who reads what the old medium produced?**
  Grep for the artifact, here the intake suffix and the verb that proves an
  import, not only for the function that writes it.
- **Write what the drive found into the closing record**, so the ledger stops
  saying five.
- **A refusal that names a verb goes in the first layer that may name one.**
  The emitter guard sits in `write/rbxml.py` and the mode check in
  `core/tree_registry.py`, and neither layer names a verb in any refusal. The
  sentence that names the landing therefore lives in `intake/ingest.py`, in
  `bridge_intake_tree`, the one function every splicer goes through to get a
  tree to hand the emitter. Putting the wording beside the guard would have
  been the shorter diff and the wrong layer.

## Related

- `docs/solutions/workflow-issues/an-optional-argument-defaulting-to-none-is-a-hidden-call-site-of-the-loader-it-falls-back-to.md`,
  the same lesson from the other side: a count in a brief is a lower bound.
  Here it was an upper bound. Either way it was not a measurement.
- `docs/solutions/workflow-issues/the-brief-files-line-is-not-the-landing-path.md`.
