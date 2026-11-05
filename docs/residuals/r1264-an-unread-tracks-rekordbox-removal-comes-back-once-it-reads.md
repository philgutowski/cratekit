---
title: A rekordbox removal of a pair's track the account lists unreadably is undone once the account lists it readably
found: at the build of #532, R-1264, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_cli.py` `plan_pair` never takes an unread track
off either side, as the card's approach says. When the person removes, in
rekordbox, the row a pair linked to such a track, rekordbox loses it and the
account keeps it, and the snapshot moves with the account holding it and
rekordbox not. Once the provider lists that track with its title and artist
again, the merge reads it as held on the account since the last sync and never
in rekordbox, so it is added back to rekordbox.

**Measured cost.** Not driven. It needs an unread track the library holds and
links, removed in rekordbox while unread, and then read again later; each step
is reachable on the twins world, the last only if the provider fixes the row.

**Closes when:** a rekordbox removal of a row linked to an unread track is
carried to the account as a removal by id, or the base keeps the unread track
out of the account's snapshot until it reads. Ledger only: it needs a provider
correcting its own row, whose reachability is unmeasured.
