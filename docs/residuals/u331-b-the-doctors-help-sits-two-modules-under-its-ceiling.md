---
title: The doctor's help sits two modules under its ceiling, and a top level import of active_taxonomy on its path costs both
found: at the merge of main into #980, U331, 2026-11-24.
issue: no
---

**The mechanism.** `tests/test_cli_lazy.py` holds `crate doctor --help` under a ceiling of cratekit modules, 90 when this card measured it and 95 since U328 put the registry's table in five parts that load at every start. Round one put the foreign tree's names on `core.active_taxonomy`, so every module importing `active_taxonomy` at its top loads `core.foreign_tree` too. With U343 merged the help reached 90 and the test failed. `cli/doctor_state.py` and `core/taxonomy_upgrade.py` now import the loader in the one function that reads it, and the help loaded 88; with U328 merged it loads 93 of 95.

**Measured cost.** Maintainer facing. Two more modules on the doctor's import path, or a top level import of `active_taxonomy` put back in either file, which costs two, fail the test again. The mutation table holds both imports (rows S13 and S14).

**Closes when:** the doctor's help is measured with a margin a unit can spend, or its imports are cut further. Ledger only.
