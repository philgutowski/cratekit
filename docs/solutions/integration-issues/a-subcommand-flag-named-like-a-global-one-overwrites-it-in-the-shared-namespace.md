---
title: "A subcommand flag named like a global one overwrites it in the shared namespace"
date: 2026-09-18
category: integration-issues
module: src/cratekit/intake/missing_cli.py
problem_type: integration_issue
component: cli
severity: medium
root_cause: naming_collision
resolution_type: code_fix
applies_when:
  - "A subcommand argument reuses the same flag name as a global argument on the root parser"
  - "The default dest for that name is the global's own dest"
  - "A downstream reader (a gate loader, a resume path) trusts the global's dest for its own meaning"
symptoms:
  - "The dispatcher hands a value meant for the subcommand to code that expects the global's meaning"
  - "A gate or resume loader refuses with 'unknown run', naming a run that was never a gate run"
related_components:
  - argparse
  - dispatcher
tags:
  - argparse
  - dest-collision
  - shared-namespace
  - listdoc
  - manifest-schema
---

# A subcommand flag named like a global one overwrites it in the shared namespace

## Context

U73 added `crate intake missing --run RUN_ID` to select a sync pass's jobs by
run id. `crate`'s root parser already declares a global `--run RUN_ID`
(`src/cratekit/cli/__init__.py:239-243`) that resumes a run stopped at a gate.
argparse subparsers write into the same `Namespace` as the root parser, and an
`add_argument("--run", ...)` on a subparser defaults its `dest` to `run`, the
same dest the global flag uses. The subcommand's value silently overwrote
`args.run`, and the dispatcher handed a sync run id to the gate loader, which
refused it as an unknown gate run.

## What was done

The subcommand flag was given its own dest, `dest="sync_run"`
(`src/cratekit/intake/missing_cli.py:91`), read back as `ctx.args.sync_run`
(`:504-505`). The flag stays spelled `--run` on the command line; only the
namespace attribute changes.

## When to apply

Any new verb flag that reuses a global option's name (`--run`, `--decision`,
`--output`) needs an explicit `dest=` distinct from the global's, checked
against `src/cratekit/cli/__init__.py`'s root parser before the flag is added,
not discovered by a refusal at resume time.

## A second, unrelated trap in the same unit

`listdoc.write` (`src/cratekit/acquire/listdoc.py:390-395`) treats a repeat
write as a no-op by comparing the encoded bytes already on disk to the bytes
about to be written (`_unchanged`, `:355-368`); if they differ at all it
refuses the whole write rather than merging. Adding a new key to every
manifest entry (U73 added `source_ref` per id) means a previously written
manifest for the same name now encodes differently, and a later identical
relisting of that name refuses as "holds something else." A manifest schema
change needs either a fresh name per schema version or an explicit migration
of existing manifests; it cannot land as a field added silently to `manifest()`.
