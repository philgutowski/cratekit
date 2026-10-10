---
title: A new kebab-shaped literal in src moves the reserved cause suite, and a verb's file write belongs inside the row session
date: 2026-10-09
category: workflow-issues
module: "src/cratekit/tagging/suggest_cli.py"
problem_type: workflow_issue
component: cause_vocabulary
severity: medium
tags: [reserved-causes, outcome-word, rows-apply, library-lock, u114]
---

# A new kebab-shaped literal in src moves the reserved cause suite, and a verb's file write belongs inside the row session

## Problem

Building `crate tag suggest` (U114, #266) hit two seams whose rules are not visible in the code.

1. The first outcome word for a row with no votes was spelled `no-evidence`. That string is already a reason in `core/cause.py`, so the new module landed in the named at-risk population of `tests/test_reserved_causes.py`. The outcome became `no-votes`.
2. Every new kebab-shaped literal in `src` moves pinned counts in the same suite, even when it is not a cause.
3. Writing the genre to the file tag before the row engine's session opened skipped the library lock and the volume check.

## Cause

The reserved-cause suite scans `src` for kebab-shaped literals and treats any that equal a known cause slug as a cause use. Outcome words share the namespace by spelling alone. The row engine takes the library lock and checks the volume when its session opens, so a file written earlier is unguarded.

## Next time

- Before naming an outcome word, `git grep` the spelling against `core/cause.py`. Pick a word that is not a cause slug.
- After adding literals, find the newcomers with `git grep` against main and update the pinned counts in `tests/test_reserved_causes.py` deliberately.
- A verb that writes files and rows writes the files inside the session. `rows.apply_rows` now takes a narrow step for this. Do not write files before it.
- The mutation driver writes nothing to its log until it ends. Read `docs/mutation/NAME.json` for progress. See also [[the-reserved-binary-keys-are-remedy-tokens-not-reasons-a-verb-can-refuse-with]].
