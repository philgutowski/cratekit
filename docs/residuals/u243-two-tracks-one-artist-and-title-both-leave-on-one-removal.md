---
title: Two label tracks with one artist and one title both leave their year playlists on one removal
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** `label.tombstoned.Tombstoned` asks the tombstone store by the
version identity, the folded artist and title, which is the identity the
deletion pass writes and acquisition consults. A label catalogue holding two
different tracks under one artist and one title, two releases each carrying
`Label Act - Untitled`, answers both as removed when one was, so `label prune`
takes both off and no build adds either.

**Measured cost.** Driven by the round one review on a fixture: the gate said
two tracks were removed and took both off. A real catalogue holding such a
pair was not driven. The gate names every track it takes off by artist and
title, so the person approving sees both.

**Closes when:** the tombstone carries an identity unique to the recording,
such as the provider track id of a track this product acquired, and the label
side asks by it. Ledger only.
