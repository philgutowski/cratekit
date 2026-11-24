---
title: WIP playlists have two writers on the account, the mirror and a bare sync pair, and the choice between them is Phillip's
found: at the review of #1062, U959, 2026-11-24.
issue: no
---

**The mechanism.** A bare `crate sync pair` (U198) pairs every plain playlist
outside Cratekit's trees, WIP included, into an account root folder named as
the rekordbox top folder, `WIP ` with its trailing space; the 2026-11-05
sitting paired 9 WIP playlists that way, kept two ways. U959 adds the account
mirror's `WIP` folder, one way, its account edits held. Left alone the two
would copy one set twice. U959 takes the recommended option of the question
on the card: the mirror leaves a playlist a pair keeps, and a bare `sync pair`
leaves a WIP playlist the mirror already copies (`pair_discover.mirrored_wip`),
so each set has one copy, the 9 paired ones in `WIP ` and new ones in `WIP`.
The two other options were `sync pair` alone owning WIP, run by the sync pass,
or the mirror adopting the `WIP ` folder.

**Measured cost.** Two WIP folders on the phone, and a new set's edits on
Tidal are held, never taken back into rekordbox, where a paired set's are.
No copy is made twice, driven by `tests/test_sync_pair_discover_wip.py`.

**Closes when:** Phillip answers the card's question; option 1 needs nothing
more, options 2 and 3 are a card each. Ledger only.
