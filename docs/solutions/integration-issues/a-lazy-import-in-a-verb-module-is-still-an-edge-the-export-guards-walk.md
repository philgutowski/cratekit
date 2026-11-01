---
title: A lazy import in a verb module is still an edge of the import graph the export guards walk
date: 2026-11-01
category: integration-issues
module: src/cratekit/cli/jobs.py, tests/test_match_states.py
problem_type: integration_issue
component: layering
severity: medium
root_cause: wrong_assumption
resolution_type: code_fix
applies_when:
  - "A CLI layer module gains an import of a feature module inside a function"
  - "The feature module is the sync, intake or write side of the product"
symptoms:
  - "tests/test_match_states.py::test_the_match_engine_never_reaches_a_rekordbox_export fails with cratekit.write.rbxml in the reached set"
  - "The mutation driver refuses a red baseline that the touched test files never showed"
tags:
  - layering
  - import-graph
  - match-engine
  - lazy-import
---

# A lazy import in a verb module is still an edge of the import graph the export guards walk

## Context

U182 needed the job verbs to read an intake job's playlist the way the playlists
sweep does, and the first fix imported `cratekit.sync.playlists` inside the one
function that asked, with a `noqa: PLC0415`, the way `cli/sync_land.py` reaches the
intake module. The touched test files stayed green. The mutation driver's baseline,
which runs the whole suite, went red on one test nobody had touched.

## What was learned

**`reaches_an_export_reader` follows every import statement in a source, at any
depth and inside any function.** It reads the text, not what runs, on purpose: a
guard that skipped a function scoped import would pass a module that reads an
export only when one verb runs. The match engine's module reaches the job verbs,
the job verbs now reached `sync.playlists`, and that module imports the intake
CLI, which reaches `cratekit.write.rbxml`. A lazy import is a deferred load, not a
missing edge.

**Before importing a feature module into anything under `cli/`, ask what reaches
that CLI module.** `cli/jobs.py` is reached by the match engine, so it may import
only what reaches no export reader. `cratekit.label.catalogue` is clean; the sync
and intake modules are not. When the logic you need lives in such a module, write
the small reading again over a clean dependency and pin the two to agree in a test,
as `playlist_identity` and `recorded_as` are now.

**Run the full suite, or the mutation driver's baseline, after any new import.**
The touched files cannot see a guard over another module's graph.
