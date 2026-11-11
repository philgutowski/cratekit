---
title: A track name apply renames to a name the landing does not take reads as an arrival
found: at the review of #665, R-1499, round two, 2026-11-11.
issue: no
---

**The mechanism.** `name apply` renames a track whose artist starts with a dot, `.38 Special`, to a dot leading name, which `intake.landing.listing` does not take, so the count of files a landing would take falls and the arrival check refuses, telling the person to move out what arrived when nothing did. Before this unit the same track was left out of the landing silently.

**Measured cost.** Driven at round two with the tags written directly; a downloader or `tag folder` producing such an artist was not driven.

**Closes when:** `name apply` never gives a staged file a name the landing does not take, or the check says which own file left the listing. Ledger only.
