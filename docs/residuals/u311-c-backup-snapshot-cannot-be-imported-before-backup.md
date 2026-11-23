---
title: backup_snapshot.py cannot be imported before backup.py, whose names it takes at import
found: at the review of #868, U311, 2026-11-22.
issue: no
---

**The mechanism.** U311 moved the restore side and the database plan out of
`src/cratekit/modules/tools/backup.py` into `backup_snapshot.py`, which
imports the engine's constants and types from `backup`, and `backup` imports
it back at its foot to re-export every moved name. Importing
`cratekit.modules.tools.backup_snapshot` first, with `backup` not yet loaded,
raises `ImportError: cannot import name 'NEWEST_WALK' from partially
initialized module`. The module docstring says it is loaded through `backup`.

**Measured cost.** None reached: no registry entry, `import_module` call or
test imports it first, and `tests/test_cli_contract.py`'s package walk imports
in sorted order, `backup` first. Driven at review.

**Closes when:** the constants and types both files use move to a module
neither imports back, so either can load first, or a test imports the sibling
alone and pins the order. Ledger only.
