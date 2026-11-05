---
title: Two processes listing one label each write the kept listing whole, and the last write wins
found: at the review of #533, U217, 2026-11-05.
issue: no
---

**The mechanism.** `KeptListing.flush` writes every answer one process holds,
atomically, over the label's `listing.json`. A `label sync --next` run beside
a sweep job listing the same label each load the document once and flush
their own view, so the answers only the earlier writer asked are dropped.
R-1091's reads store has the same shape.

**Measured cost.** Read, not driven. Provider calls only: the next run asks
again what was dropped. Nothing kept is wrong, since each answer carries its
own instant.

**Closes when:** a flush merges the document on disk under a lock before it
writes, for both stores. Ledger only.
