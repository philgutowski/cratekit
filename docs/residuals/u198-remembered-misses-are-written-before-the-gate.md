---
title: sync pair records its remembered misses before either gate, so a run with both gates skipped writes the pairs document
found: at the review of #483, U198, 2026-11-04.
issue: no
---

**The mechanism.** `sync_pair` records what the account said of each unmatched row as soon as the plan is made, so the plans the two gates make again ask the provider nothing. A run whose gates are both answered skip has still written those misses to the pairs document.

**Measured cost.** Driven by the review: both gates skipped, and the document then held the miss. No user facing cost: a miss is a fact about a row and the provider, the mirror records its own the same way (R-1031), and nothing in either playlist is written. A rehearsal reading the document as untouched would be wrong.

**Closes when:** the misses ride the run and are recorded only once a gate is applied, or the rule is accepted as the mirror's. Ledger only.
