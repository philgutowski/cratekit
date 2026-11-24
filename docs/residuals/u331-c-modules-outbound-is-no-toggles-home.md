---
title: modules.outbound is no toggle's home, so the rules for a toggleable package no longer read it
found: at the build of #980, U331, decided by 980-toggle-homes-1 on 2026-11-24.
issue: no
---

**The mechanism.** `TOGGLE_HOMES` in `tests/test_import_rules.py` named `cratekit.modules.outbound` as one of `export`'s homes, and the whole `cratekit.favorites` package as `favorites`'. The registry gates one verb with `favorites`, `sync favorites` in `favorites/cli.py`, and the four export verbs with `export`. The rest of the favorites package builds four verbs no toggle gates and part of the landing, and `modules.outbound` is called by organize, sync, label, intake and the favourites sweep. With either toggle off, five ungated verbs could not build: five of the seven dangling lines main allowed. Phillip's decision, option 1, narrowed the table to what the registry gates: `favorites` owns `cratekit.favorites.cli` and `export` owns `cratekit.export`. No source file moved.

**Measured cost.** Maintainer facing. An always on package could import `modules.outbound` at its top level and no test of the import rules would fail, since it is no toggle's package any more. No verb's output changes.

**Closes when:** `modules.outbound` is split into what `export` owns and what every caller uses, and the ungated parts of `cratekit.favorites` move out of it, so each package belongs to one toggle (the decision's option 2, a restructuring card of its own with its own replay). Ledger only.
