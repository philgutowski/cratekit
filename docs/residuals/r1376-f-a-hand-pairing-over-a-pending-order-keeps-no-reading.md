---
title: A pair made by hand over a pending account order keeps no reading, so it is held until the provider serves the order the moves leave
found: at the review of #597, R-1376, round two, 2026-11-07.
issue: no
---

**The mechanism.** A first sync by hand has no pair record, and U231's pending hold keeps its reading on the record (`PairStore.see` keeps nothing for a pair not marked), so no two readings can ever agree. The pair is held (`sync-pair-account-settling`) until the account shows exactly the order the stopped write's moves leave, the one case `_pending` lets through without agreement.

**Measured cost.** Driven where every move was accepted and the provider caught up: held twice, then finished, nothing written into rekordbox meanwhile. Not driven: a pending write some of whose moves the provider refused, whose end the account never shows; that pair would be held on every sync until released. It needs a U231 pending order, the pair's rekordbox playlist deleted while pending, a hand pairing and a refused move together. Nothing is written wrong.

**Closes when:** a first sync by hand over a pending order can keep its reading somewhere a later run agrees with, or the hold says to wait for the order the moves leave. Ledger only.
