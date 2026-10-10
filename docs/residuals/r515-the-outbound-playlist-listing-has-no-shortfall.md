---
title: The outbound account's own playlist listing carries no shortfall
found: at the review of #284, R-515, 2026-10-10.
issue: no
---

**The mechanism.** The outbound account's own `playlist_tracks`, read by
export, prune, sets and folders, still lists without a shortfall, so a
playlist the provider returns short there reads as whole.

**Measured cost.** Not driven. Those verbs act on the served rows of a short
playlist with nothing said.

**Closes when:** that listing carries a `ListingShortfall` and its verbs warn
as the intake, harvest and sweep verbs do. Ledger only; out of the card's
verbs on #264.
