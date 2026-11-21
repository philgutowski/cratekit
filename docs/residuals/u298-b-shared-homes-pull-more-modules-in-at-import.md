---
title: Three modules load more of the product at import since their helpers moved to a shared home
found: at the review of #855, U298, 2026-11-21.
issue: no
---

**The mechanism.** The review compared what each of the 329 modules loads on import, base against branch. `modules/outbound/tidal_account.py` now loads `cratekit.sync` and `cratekit.favorites` at import, an edge between two toggleable packages that the import rules do not count. `sync/pair_stopped.py`, whose docstring calls it pure, now loads 14 more modules, the shell package and its registry among them. `core/night_budget.py` loads 8 more.

**Measured cost.** None to a run: the top level imports of a toggleable package (54), the lazy ones (111), the verbs left dangling (159) and every allowance line are unchanged, and the behaviour comparison over every verb's help is clean. What it costs is import time and a seam the rules do not see.

**Closes when:** the area cards for the outbound module and sync either import the shared helper lazily or home it lower, and the import rules count an edge between two toggleable packages. Ledger only.
