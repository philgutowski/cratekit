---
title: Under the app credentials a track's streamability is read off availability, a field the provider marks deprecated and due for removal
found: at the plan of #497, U207, 2026-11-05.
issue: no
---

**The mechanism.** `catalogue_api._available` reads a track's `availability` array for `STREAM`, and `tidal_account._streamable` leaves a track that cannot stream out of the choice. The platform's published document (version 1.10.224) marks `availability` deprecated in favour of `usageRules` and says it will be removed. Once it is gone, every app answer reads as `None`, which is streamable, so a withdrawn release becomes a candidate again.

**Measured cost.** Not driven. Nothing today is affected, since the field is still documented and the app is not registered yet. On removal, a heart or a pair could land on a release nobody can play wherever it is the one release that agrees.

**Closes when:** a live probe reads `usageRules` values and `_available` reads them when `availability` is absent. Ledger only.
