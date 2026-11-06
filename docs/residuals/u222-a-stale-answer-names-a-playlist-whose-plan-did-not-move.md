---
title: A stale mirror answer can name a playlist whose plan did not move, since each line's digest covers the names the gate shows
found: at the review of #552, U222, 2026-11-05.
issue: no
---

**The mechanism.** `mirror_frozen._lines` digests each playlist's whole gate
item, the removed tracks' names and the kept and unmatched counts among it,
not only what the step's digest covers, so a playlist whose writes are
unchanged but whose shown names changed is named beside the one that moved.

**Measured cost.** Driven on the plain mirror world: a removal planned on
Techno Med, then a track added to Techno Low on the account and the removed
track retitled; the refusal named both playlists. The decision is still
refused correctly; only the naming overreaches. The producer, a retitle on the
account of a track whose removal is planned, was not driven on the provider.

**Closes when:** each line is digested over the fields its playlist's plan
identity carries. Ledger only.
