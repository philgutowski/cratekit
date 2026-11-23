---
title: The behaviour scenarios cannot run against the survey's commit as written, since they import test modules that import names the refactor made
found: at the build of #872, U315, 2026-11-23.
issue: no
---

**The mechanism.** `scripts/behaviour_compare.py capture --rev ff8e5ec` collects nothing: 22 of the 70 scenario files import fixture builders from test modules (`tests/test_outbound_workers.py`, `tests/test_adoption.py`, `tests/test_favorites_order.py` and others) that import `core.private_store`, `adopt.revert_changed` and `favorites.spine`, which the refactor created, and the autouse fixture `_no_live_launchd` in `tests/conftest.py` imports `cli.schedule` (U295). Every scenario then errors at setup. U315 ran them against `ff8e5ec`'s source with four import only aliases and `config.mkdir_private` added as an alias of `_mkdir_private`, none read by the product, in a scratch clone; 214 scenarios ran both sides, and six whose verbs were born after `ff8e5ec` were taken across the epic's span alone.

**Measured cost.** Maintainer facing: the comparison the audit is asked for needs a hand built overlay, described in `docs/restart/u315.md`, rather than the instrument's own flag.

**Closes when:** a re-audit can compare against `ff8e5ec` with the instrument as it stands, for example by the scenarios importing their builders from a support module that does not import product modules at top level. Ledger only.
