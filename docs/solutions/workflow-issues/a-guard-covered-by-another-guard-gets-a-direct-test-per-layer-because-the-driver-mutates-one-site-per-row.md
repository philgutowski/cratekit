---
title: "A guard covered by another guard gets a direct test per layer, because the driver mutates one site per row"
date: 2026-09-23
category: workflow-issues
module: "scripts/mutate.py, src/cratekit/acquire/match.py"
problem_type: workflow_issue
component: mutation_driver
root_cause: tool_shape_not_visible_in_the_method
resolution_type: test_added
applies_when:
  - "A mutation table row is expected to read zero because a second guard covers the same input"
  - "A composite row would need to revert two sites in two functions at once"
  - "A lookup guards an empty key and the walk that fills the map never writes that key"
symptoms:
  - "The rows file is drafted with a second old and new pair on one row and the driver has no such field"
  - "A zero row on a user facing guard owes a composite that cannot be expressed"
tags:
  - mutation-table
  - mutate-driver
  - composite
  - guard-layers
  - r-667
---

# A guard covered by another guard gets a direct test per layer, because the driver mutates one site per row

## Problem

The ISRC index has two layers over one input, the empty token. The walk in
`index_library` files a file under its ISRC only when it has one, and the
lookup `held_by_isrc` answers nothing to an empty token. Either alone makes
a row with no ISRC hold nothing, so reverting either alone reads zero, and
METHOD's rule is that a zero on a user facing guard is acceptable only with
a composite showing what the pair holds. The composite here is both layers
off at once, and they sit in two functions forty lines apart.

## Cause

`scripts/mutate.py` takes one `old` and one `new` per row and refuses a row
whose `old` is absent or appears twice. That is the right shape: a two site
edit is two chances to mutate the wrong place and hand back a confident
number about an experiment nobody ran. So a composite over two sites cannot
be written as a row, and the rows file drafted with an `also_old` field is a
draft against a driver that does not exist.

## What to do next time

- Give each layer a test that reaches it alone, on a fixture the other layer
  cannot protect. For the lookup, a hand built index carrying the empty key
  the walk never writes. For the walk, an assertion that the empty key is
  absent from the map it built. Each row then kills one test on its own
  merits and no composite is owed.
- When both layers are the same guard spelled twice, remove one, the way the
  unit for R-669 removed the sanitizer the composer already applied. Keep
  both only when each protects a caller the other cannot see, and say which
  caller in the docstring.
- Neighbours: the concept "Composite" in `CONCEPTS.md`, and
  `docs/mutation/r669-notes.md` for the removed layer.
