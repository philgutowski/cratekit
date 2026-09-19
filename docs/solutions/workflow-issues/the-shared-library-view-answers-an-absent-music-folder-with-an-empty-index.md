---
title: "The shared library view answers an absent music folder with an empty index, so a verb that starts asking the library inherits a false missing"
date: 2026-09-19
category: workflow-issues
module: "src/cratekit/acquire/match.py, src/cratekit/acquire/match_cli.py, src/cratekit/intake/cli.py"
problem_type: workflow_issue
component: seam_design
severity: high
root_cause: absence_read_as_evidence
applies_when:
  - "A verb that did not consult the library is changed to call match_cli.library_view, resolve_list or match.index_library"
  - "The fix for a false report is to ask a shared seam a question, and the seam has a quiet answer for a state it could not read"
  - "The library lives on an external volume, so the music folder not being there is an ordinary state and not a corruption"
  - "The question is asked AFTER a paid or slow step, so a refusal that arrives late has already been paid for"
symptoms:
  - "Every owned track in a list reports missing, at exit zero, with no warning, when the library drive is not plugged in"
  - "A unit closes a residual that said owned tracks report missing, and its own new path reproduces that report by another road"
  - "Three verbs each carry their own copy of a music folder check and the shared view carries none"
related_components:
  - "match"
  - "intake"
  - "recognition"
tags:
  - "absence-as-evidence"
  - "library-view"
  - "unmounted-volume"
  - "shared-seam"
  - "spend"
---
# The shared library view answers an absent music folder with an empty index, so a verb that starts asking the library inherits a false missing

## Context

U103 (card 148) closed R-422: `intake identify` reported every identified track
missing because it never asked the library. The fix was the obvious one. The
body of `match_list` was lifted into `match_cli.resolve_list` and identify calls
it, so an owned track is `matched`.

## What happened

The unit's suite was green and its owned track reported owned. The built in code
review then pointed out that the new path had a second way to produce exactly
the report the unit existed to stop. `match.index_library` guards its walk with
`if root.is_dir()`, and when the music folder is not there it returns an index
holding nothing, with nothing said. `library_view` hands that on. So with the
library drive unplugged, identify would have paid for recognition, asked an
empty index, and reported every owned track missing at exit zero.

Driving the same state on the paths that already used the view showed it was
not new. `match run` over a list whose one track the library holds went from
`[1, 0, 0]` to `[0, 0, 1]`, outcome ok, when the music folder was removed. An
`intake set` job resumed with the folder gone ended `succeeded` with
`owned 0, missing 3`. That is R-512.

## Why the source does not explain it

Nothing at `library_view` or `resolve_list` says the index may be empty because
the folder is absent. The knowledge lives in three verbs that each learned it
separately and each wrote their own check: `intake missing --list`,
`acquire fallback`, and now `intake identify`. Each carries the sentence "an
absent library is not an empty one" in a comment above its own copy. A session
reading `match_cli` to share the resolve step reads none of those files.

## The rule

Until R-512 lands a refusal inside the shared view, **every new caller of
`library_view`, `resolve_list` or `index_library` over the configured library
refuses an absent music folder itself, as `library-volume-unmounted` with
`Remedy.MOUNT_LIBRARY_VOLUME`, and does it before any paid or slow step.** In
identify that is `_library_or_refuse`, called before `pipeline.identify_only`,
because the answer is free at that point and follows a paid step otherwise.

`index_library(batch_dir)` in `intake/landing.py` is a different case: that
caller made the folder it indexes.

## The test that holds it

`test_an_absent_library_is_refused_before_the_spend_and_never_read_as_an_empty_one`
in `tests/intake/test_workers.py` removes the music folder, drives the verb, and
asserts both the refusal and that the fake transport was never asked. Mutation
row C1 in `docs/mutation/u103-b.md` removes the call and that test dies.

## Where else this applies

Any seam here that returns a collection and has an early `if path.is_dir()` or
`if path.exists()` around the walk. The question to ask of it is whether the
caller can tell "walked and found nothing" from "could not walk".

## See also

- `docs/residual-findings.md`, R-512, the two driven producers and the callers not driven.
- `docs/solutions/workflow-issues/a-seam-that-returns-only-rows-reads-absence-as-evidence-of-absence.md`, the same pattern one seam over, in the identifier.
