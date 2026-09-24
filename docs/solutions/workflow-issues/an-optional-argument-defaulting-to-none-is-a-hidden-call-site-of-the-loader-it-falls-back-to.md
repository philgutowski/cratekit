---
title: "An optional argument that defaults to None is a hidden call site of the loader it falls back to, so a call-site count understates the defect"
date: 2026-09-24
category: workflow-issues
module: "src/cratekit/core/active_taxonomy.py, src/cratekit/write/trees.py, src/cratekit/searchers.py, tests/test_active_taxonomy.py"
problem_type: workflow_issue
component: taxonomy
severity: medium
root_cause: incomplete_scope
applies_when:
  - "A residual or brief counts the direct calls to a function that should be replaced by a new loader"
  - "A helper takes an optional argument whose None default quietly calls the old source"
  - "A guard is written to refuse the old reader"
symptoms:
  - "Every counted call site moves and some verbs still read the shipped template"
  - "A verb passes nothing for the optional argument and gets the fallback without ever naming it"
tags: [taxonomy, active-copy, default-argument, guard, ast, residual, R-685]
---

# An optional argument defaulting to None is a hidden call site

## Problem

R-685 said 34 call sites in 12 modules read `taxonomy.default_taxonomy()`, the shipped
template, instead of the library's active copy on the volume. Moving those 34 was not
enough. Four tree writers in `write/trees.py` and `searchers.for_taxonomy` took an optional
`declared` argument whose `None` default reached for the shipped template, and the landing
verb relied on that default for its catalog tree.

## Cause

A grep for the function name finds only the sites that spell it. A default that calls it
inside a helper is a call site with no spelling at the caller.

## What to do next time

- Remove the optional default and make the argument required, so the caller has to say
  where the taxonomy came from. That, not the 34 edits, is what made every verb read the
  library's copy.
- Point the guard at the shipped text and the parser as well as the default loader, and
  resolve aliased imports, so a new reader cannot bypass it by renaming. See
  `tests/test_active_taxonomy.py`.
- Treat a count in a brief as a lower bound, and search for the fallback's other
  entrances, defaults and re-exports, before trusting it.
