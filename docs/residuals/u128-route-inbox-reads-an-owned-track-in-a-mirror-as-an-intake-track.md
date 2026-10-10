---
title: The routing reads an owned track in an account playlist's mirror as a track to route
found: at the built in review of #295, U128, 2026-10-10.
issue: no
---

**The mechanism.** Since U128 an account playlist's INBOX playlist holds the
tracks the library already owned beside the new ones. `route inbox` plans a
placement for every track it finds under the intake folder,
`routing_cli._inbox_keys` on the bridge and the INBOX memberships on the
native medium, and does not ask whether a track was already filed under BY
GENRE. So an owned track is routed again. Where its file's genre still names
the playlist it sits in, the membership writers add nothing, since they add
only what is absent. Where the file's genre moved since it was filed, which
773 database rows show in this library, it gains a second genre placement and
keeps the first. This is the cost R-905 weighed when it chose new tracks only,
and the author's decision of option (b) accepted the mirror knowing it.

**Measured cost.** Not driven. No `route inbox` was run over a landing that
mirrored an owned track, on either medium, so how many owned tracks a real
sync routes a second time, and how many of those land in a second genre, is
unmeasured.

**Closes when:** `route inbox` leaves a track it finds under INBOX alone when
the collection already places it under BY GENRE, or the author reads a routed
mirror and says the second placement is what he wants. Ledger only: it is a
consequence of a choice the author made, and nothing is lost.
