---
title: A removal from a playlist whose read lags the removal is refused as not done, though it landed
found: at round one's review of #543, U220, 2026-11-05.
issue: yes
---

**The mechanism.** `TidalAccount.remove_tracks` reads the playlist back once
after each removal by position and refuses at once when the reading is not
the playlist with exactly those positions gone. U220 measured on Sitting 62
that the provider's read can lag a write it accepted, and taught
`order_tracks` to read again after a pause; `remove_tracks` has the same
shape and no reread. Driven on a stand in whose read lags one write:
removing `b` from `[a, b, c, d]` landed, leaving `[a, c, d]`, and was refused
either "declares 3 track(s) ... nothing was taken off it" (the count current,
the tracks lagging) or "a track other than the asked ones may have come off"
(both lagging).

**Measured cost.** The product says a removal did not happen, or may have
taken the wrong track, when it took exactly the asked one; the person checks
by hand and the sync stops. The lag itself is measured live for a move
(Sitting 62), not yet for a removal.

**Closes when:** `remove_tracks` reads back through the same bounded reread
`order_tracks` uses (a reading equal to the playlist before the removal is
read again after a pause; anything else refuses at once), with a test over a
provider whose read lags one write. It meets the board bar under (b).
