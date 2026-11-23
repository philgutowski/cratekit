---
title: A module __getattr__ makes the refactor measure over count one module's outside uses and read its import as lazy
found: at the review of #861, U304, round two, 2026-11-22.
issue: no
---

**The mechanism.** U304 gave `sync/playlists.py` a module `__getattr__` that imports `label.catalogue.AccountPlaylist` on first use, since organize's suite reads that name there. Round two drove `scripts/refactor_measure.py` over it: `_defined_names` answers None for a module with a `__getattr__`, so `outside` counts an attribute of any local variable named `playlists` as a use (one spurious name, `items`, from a keyword argument in `tests/test_organize_mirror.py`), and rule four reads the import inside `__getattr__` as lazy, so a top level `from cratekit.sync.playlists import AccountPlaylist` would hide a labels edge from the static verb check (0 such imports today). The fallback `raise AttributeError` kills no test.

**Measured cost.** None to a person. A later card reading `outside` for that file sees one name too many.

**Closes when:** the measure treats a module `__getattr__` as answering only the names it tests for, or the name moves to a module organize owns. Ledger only.
