---
title: "A field on Wanted that guards a consult has to cross the intake freeze, and its absence has to read as the refusing answer"
date: 2026-09-19
category: integration-issues
module: src/cratekit/intake/cli.py
problem_type: integration_issue
component: intake
severity: high
resolution_type: code_fix
applies_when:
  - "A unit adds a field to match.Wanted that decides whether the engine asks a store something"
  - "The decision is pinned by tests that build the Wanted through a reader and resolve it in the same process"
  - "A guard is written as the absence of something on the Wanted, such as no credit spelled"
tags: [wanted, freeze, thaw, intake, tombstone, companion, suppressed, r-431]
---

# A field on Wanted that guards a consult has to cross the intake freeze

## What happened

R-431 added `Wanted.several_artists`, set by the provider reader, so that a row
billing a guest in its artists list never asks for the companion of a deletion
that credited somebody else. Every engine test passed. The intake path, which
is the one path the residual was about, would have ignored the guard.

## Why

`intake playlist` does not resolve the `Wanted` the reader built. It freezes
each track into the job payload with `intake.cli._frozen`, and the worker, in
another process, resolves the object `thawed` rebuilds. `_frozen` and `thawed`
name every field by hand. A field neither names is silently reset to the
dataclass default on the far side, and the default for a guard like this one is
the permissive answer. So SUPPRESSED would have been decided from a track that
had forgotten its second artist.

Nothing fails. Tests that read a row and call `standing_tombstone` never cross
the freeze, and the one pin of the frozen shape,
`tests/intake/test_workers.py`, compares one literal dict and only fails
because a key was ADDED.

The same session found the other half by review: a guard phrased as "this
listing spelled no credit" is vacuous on a `Wanted` nobody read from a listing.
`match_cli` builds one by hand from a held file, whose title the index has
already taken the credits off, so "no credit in it" meant nobody looked.

## The rule

- A new `Wanted` field goes into `_frozen` and `thawed` in the same commit, with
  a test that round trips it through `intake_cli.frozen` and `intake_cli.thawed`
  and asserts the BEHAVIOUR on the far side, not the key.
- In `thawed`, a payload that lacks the field was frozen by a build that never
  looked. Read its absence as the answer that refuses, here `True`, billed,
  and accept the one missed suppression that costs an older job.
- A guard that reads an absence has to name what makes the absence evidence.
  `uncredited_spellings` requires `spelled`, which only a reader sets.
- `intake.candidates` and the fallback verbs store tracks through the public
  `intake_cli.frozen`, so they inherit the field with no edit.

## Where to look

`src/cratekit/intake/cli.py` `_frozen` and `thawed`,
`src/cratekit/acquire/match.py` `Wanted.uncredited_spellings`, and
`test_a_billed_guest_survives_the_freeze_the_worker_resolves_from` in
`tests/test_intake_missing.py`. Rows B9 and B10 of `docs/mutation/r431-b.md`
are the two mutations that would have shipped green without it.
