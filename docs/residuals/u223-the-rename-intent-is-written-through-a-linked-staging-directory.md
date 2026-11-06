---
title: analyze run writes its rename intent through a linked staging directory that staged_path then refuses
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** `record_rename_intent` in
`src/cratekit/analysis/artifacts.py` makes the item's staging directory and
writes into it without checking for a link, so an ordinal directory that is a
link has the intent written at its far end, after which `staged_path`
refuses the link and the item fails `internal-error` for good. U223 stopped
the discard and the readers following such a link; the writer predates it.

**Measured cost.** Driven by the round two reviewer with a link planted in
the private job store. No verb writes a link there: zero producers.

**Closes when:** the writer refuses a linked staging directory the way
`staged_path` does. Ledger only.
