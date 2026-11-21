---
title: Deleting the night budget's ledger frees a spent night
found: at the review of #850, U293, 2026-11-21, round one finding 8.
issue: no
---

**The mechanism.** `core/night_budget.py` reads a ledger that does not exist as a night that spent nothing, the rule for a fresh installation, so a ledger deleted by hand mid night gives the night its whole budget again. A ledger replaced with one it cannot read refuses.

**Measured cost.** Driven by the reviewer with a hand deletion: a fresh 1,200 calls on the same night. The hour's budget, the night's lowered hour and one command's ceiling still hold every call, so the account sees at most 600 an hour. Nothing in Cratekit deletes the file.

**Closes when:** the ledger's absence is told apart from a fresh installation, for example by the gate's own record of the night's mark.
