---
title: The Old check in the rotation's classifier carries a guard that kills no test, because a name is never None
found: at the review of #512, U214, 2026-11-05.
issue: no
---

**The mechanism.** `rotate._classify` tests `old_display is not None and name
== old_display`. A node's name is always text, so the first clause decides
nothing the second does not already decide.

**Measured cost.** None. Removed in a mutation run, every test passed. It
documents the undeclared case and costs nothing.

**Closes when:** the clause is dropped or kept on purpose. Ledger only,
maintainer facing.
