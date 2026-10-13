---
title: A track the account cannot play, added to a debris copy after the gate, is not seen by the apply's reread
found: at the review of #320, U143, 2026-10-13.
issue: no
---

**The mechanism.** Before removing a debris playlist, `organize.root.apply` reads its tracks again and keeps the playlist if it holds one the gate was not answered over. The read goes through `playlist_tracks`, which leaves out a track the account cannot play while the provider still counts it (`acquire.listing.playlist_tracks`). The plan compares the read with the listing's declared count and leaves a short read, but the apply has no fresh declared count to compare with, and `remove_root_playlist`'s protocol signature carries none. A track the account cannot play, added in the seconds between the gate's answer and the removal, would be removed with the playlist.

**Measured cost.** Not driven. The window is the time between the run that answers the gate replanning and its apply, and the track is one the account cannot play. Reachability is unmeasured.

**Closes when:** the adapter's removal takes the expected declared count and refuses when the served `num_tracks` differs, or the apply reads the count some other way. Ledger only.
