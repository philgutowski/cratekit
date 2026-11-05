---
title: Whether the account's folder listing carries a playlist's creation time is proven on a fixture only
found: at the review of #530, U216, 2026-11-05.
issue: no
---

**The mechanism.** A root folder adopted before U216 has no record of what it
held, so `sync/pair_cli._discovered_back` reads each unpaired playlist there by
when the account says it was made, through
`TidalAccount.folder_playlists_dated`, which takes the `created` the client's
playlist parser reads off each folder item. The test that proves it adds a
`created` field to an item the author wrote. No live sample of a folder item's
data carrying `created` is recorded anywhere in the repository.

**Measured cost.** Not driven, since the live account cannot be read from the
cloud. If the live items carry no time, every unpaired playlist in the live
`Genre Trivia!` folder is named "no creation time" for good, one made on the
account after the sync included: named on the gate and never made, so never a
duplicate, but nothing made there comes back by itself until it is paired by
hand. The card's live check, no create for the 18, passes either way, so the
attended sitting reads the reason on the 18: "not after a sync adopted" means
the time was read, "no creation time" that it was not.

**Closes when:** the attended sitting reads the reason text on the next live
`crate sync pair` plan. Ledger only; it closes at a sitting.
