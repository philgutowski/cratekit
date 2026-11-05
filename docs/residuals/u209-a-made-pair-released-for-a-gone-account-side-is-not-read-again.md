---
title: A made pair released because its account playlist was not listed is released at the write even when the account lists it again
found: at round two of the review of #499, U209, 2026-11-05.
issue: no
---

**The mechanism.** U209's check reads again, before the write, that a made
pair let go for its rekordbox side is still let go, and skips an unpaired
pair whose gone side is the account (`if lost.gone != REKORDBOX_SIDE:
continue`). A made pair the plan unpaired because the account did not list
its playlist is released at the write, its rekordbox side recorded as
released for good, even when the account lists the playlist again by then.
A custom playlist twin takes the same path and is forgotten.

**Measured cost.** Round two drove it in the fake by removing the playlist
and restoring it under the same identifier between the plan and the write:
the pair was released and the next sync said its account playlist was
deleted while the account listed it. Whether the real account can list a
playlist absent at the plan and present at the write is unmeasured, so no
live producer is known.

**Closes when:** the check lists the author's playlists once when the plan
unpairs any for a gone account side, and refuses stale naming one that is
back. Ledger only until a live producer is found.
