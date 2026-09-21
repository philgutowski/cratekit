---
title: "A printed install command has one home, the modules layer, and a pipx reinstall drops the extras already chosen"
date: 2026-09-21
category: integration-issues
module: "src/cratekit/modules/extras.py, src/cratekit/cli/registry.py, src/cratekit/analysis/cli.py, src/cratekit/analysis/vocals.py"
problem_type: integration_issue
component: install_hint
severity: medium
root_cause: wrong_layer_and_incomplete_command
resolution_type: code_fix
applies_when:
  - "A user facing command string must be emitted by both the CLI and a feature module"
  - "A message tells the person how to install a missing extra under pipx"
tags: [pipx, extras, layering, install-command, R-395]
---

# A printed install command has one home, the modules layer, and a pipx reinstall drops the extras already chosen

## Problem

The missing extra message printed a bare `pip install 'cratekit[analysis]'`. Under pipx that pip is not the one in Cratekit's private environment, so the command failed or installed where `crate` never reads. Fixing it looked like a one line change in `cli/render.py`.

## Cause

Two rules sit on either side of the obvious home.

- The layering guard forbids a modules layer file from importing `cratekit.cli`, so the analysis and vocals modules cannot call `cli/render.py`.
- The D2 guard forbids any layer below modules from spelling a package manager line, so core cannot hold it either.

The modules layer is the only place both the CLI and a feature module can reach. The command therefore lives in `modules/extras.py`, and `cli.registry` re-exports the distribution name from it.

Second trap. `pipx install --force` reinstalls from exactly the spec given. A printed command naming only the missing extra silently removes extras already installed. The recorded extras in the environment's `pipx_metadata.json` have to be merged back into the command.

## What to do next time

- Put any user facing command string that both layers emit in `modules/extras.py`. Do not add a second quoting helper.
- When printing a pipx reinstall, read the recorded source and extras from `pipx_metadata.json` and keep them. Test with an extra already present, not only an empty environment.
- Detect pipx by `pipx_metadata.json` in `sys.prefix`, not by where pipx lives.
- Neighbour: R-646 in `docs/residual-findings.md`, filed from this work.
