---
title: A module handed over other than by a top level import is not followed by the import measure
found: at review round one of #980, U331, 2026-11-23.
issue: no
---

**The mechanism.** `scripts/refactor_measure.py` follows a name that is a module into that module, so `tags.art.read` and `from cratekit.core.tags import art` read as uses of `cratekit.core.art`. It follows only what a top level import hands over, through as many modules as pass it on by import. A module bound by an assignment, a star import, `getattr`, a function that returns it, a conditional import or an import inside a `try` is not followed, so a feature package could reach an unlisted module through a listed one under a single counted name.

**Measured cost.** Maintainer facing. Round two scanned the 25 listed modules at runtime and found none holding a module bound any way other than a top level import, so nothing in the tree uses an unfollowed spelling today.

**Closes when:** the measure reads the listed modules' runtime bindings beside their source, or the rules refuse a module attribute on a listed module that is not a top level import. Ledger only.
