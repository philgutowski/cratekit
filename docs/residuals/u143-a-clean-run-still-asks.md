---
title: A clean account root still opens the account gate, though the plan's R17 says no gate
found: at the build of #320, U143, 2026-10-13.
issue: no
---

**The mechanism.** The convention plan (`docs/plans/2026-10-13-1407-feat-tidal-account-convention-plan.md`, R17 and AE8) and the U143 brief say a second run on a clean root plans nothing and opens no gate. U112's pinned rule is that an area with nothing to write says so and still asks, "answering still records the decision" (`organize/steps.py`, `test_an_area_with_nothing_to_do_still_asks`, `test_the_plan_is_empty_and_still_asks_when_the_root_is_clean`). U143 keeps U112's rule: the root step plans nothing and is in state `nothing` on a clean root, and the account area still asks its gate.

**Measured cost.** One question answered on an organize run that writes nothing. No write, no loss. The two rules were not reconciled because changing whether an area asks is U112's decision and changes every area, not only the root step.

**Closes when:** a person decides between the two rules, and either `organize/cli.py` skips the gate of an area that writes nothing (with the two U112 tests rewritten) or the plan's R17 is read as "plans nothing". Ledger only.
