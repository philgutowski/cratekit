---
title: Sync still reaches core.held_plan, a module off the named interface, because its file is another card's
found: at the build of #861, U304, 2026-11-22.
issue: no
---

**The mechanism.** `tests/ratchets/imports/sync.txt` keeps one line, `off-interface cratekit.core.held_plan`. Sync is the only feature package that holds a plan across its gates, through `core/held_plan.py`, which is not on `CORE_INTERFACE` in `tests/test_import_rules.py`. U304 owns neither file: `core/held_plan.py` was #857's (U300), which landed without moving it, and the interface list is the import rules test's, capped at 25, which admits a module only when another leaves.

**Measured cost.** None to a person. Point 4 of #847 asks for every package's allowance empty.

**Closes when:** the final audit (#872) or a later core card either puts `held_plan` behind a module on the interface (`session`, which owns the write path the plan feeds, is the natural home) or trades it onto the list, and sync's line is pruned. Ledger only.
