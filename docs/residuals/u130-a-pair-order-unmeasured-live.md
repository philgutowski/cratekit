---
title: A pair's account order and rekordbox numbering are unmeasured on the live account and library
found: at the build of #298, U130, 2026-10-10.
issue: no
---

**The mechanism.** `TidalAccount.order_tracks` moves each track to the end of
the account playlist with the client's `move_by_indices`, reading back after
every move, and `write/playlist_pair.renumber` numbers a pair's live rekordbox
memberships one through N while a soft removed membership keeps the number it
had. Both were driven only on stand ins: the adapter over the prune suite's fake
client, the writer on the disposable database. How the provider reads a move to
the end, and what rekordbox shows when a live membership shares its number with
a soft removed one, were not observed.

**Measured cost.** Not driven against the provider or rekordbox. A move the
provider places elsewhere is refused by the read back after one move, with every
track still on the playlist; a numbering rekordbox reads otherwise would show
the pair out of order and change no membership.

**Closes when:** the attended sitting the brief names syncs one real playlist
edited on both sides, reorders it on each side in turn, and reads the order on
the account and in rekordbox. Ledger only, since it closes at a sitting.
