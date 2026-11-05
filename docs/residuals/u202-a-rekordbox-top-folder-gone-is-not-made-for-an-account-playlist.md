---
title: An account playlist whose rekordbox top folder is gone is listed rather than made in a new folder
found: at the build of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_discover.home_of` places an account playlist
only in a live rekordbox top folder of its root folder's name. When rekordbox
holds none, because the folder was deleted or renamed there, the playlist is
listed under `sync-pair-not-brought` and nothing is made, the conservative
call: a folder deleted in rekordbox may have been deleted on purpose.

**Measured cost.** Driven by `test_home_of_refuses_each_place_it_cannot_decide`.
A playlist made on the account in that folder waits until the folder is made
in rekordbox by hand.

**Closes when:** Phillip says whether a missing top folder is made. Ledger
only; the question is on the card.
