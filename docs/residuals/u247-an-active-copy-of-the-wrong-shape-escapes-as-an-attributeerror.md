---
title: An active taxonomy copy whose tables have the wrong shape escapes the loader as an AttributeError, not a config-unusable refusal
found: at the review of #676, U247, 2026-11-12.
issue: no
---

**The mechanism.** `active_taxonomy.load` turns a `TaxonomyError` into the
`config-unusable` refusal with the setup remedy. A copy that is valid TOML but
gives a table the wrong type, `tree = "x"` where a table belongs, reaches
`build_taxonomy`, which calls `.get` on the string and raises
`AttributeError: 'str' object has no attribute 'get'`. The review drove it
twice through `active_taxonomy.load` on a disposable library, and the same
copy raises the same on `main` without U247's memo, so it predates this unit.
The memo did not change it: a raise is never remembered, so it raises on
every call as before.

**Measured cost.** Driven on a disposable copy only. A person who hand edits
their active copy into this shape is shown a traceback, reported as an
internal defect, where the refusal would name the copy and tell them to run
setup. The other shape checks in `build_taxonomy` were not swept.

**Closes when:** `build_taxonomy` checks that each top level key it reads is
the type it reads it as, and reports a wrong type as one of its problems, with
a test that `tree = "x"` refuses `config-unusable` through
`active_taxonomy.load`. Ledger only.
