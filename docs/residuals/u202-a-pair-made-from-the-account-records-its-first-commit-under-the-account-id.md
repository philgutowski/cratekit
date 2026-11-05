---
title: A pair made from the account records its first commit under the account playlist's id and every later one under the rekordbox playlist's
found: at the review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_reverse.create` records the commit that makes a
rekordbox playlist for an account playlist under `playlist-pair:<account id>`,
since the rekordbox playlist has no identifier until that commit. Every later
sync of the same pair writes through `write/playlist_pair.apply`, which
records under `playlist-pair:<rekordbox id>`.

**Measured cost.** Read from the diff, not driven. A pair's session history is
split across two source keys, so a reader of one key misses the commit that
made the playlist.

**Closes when:** the first commit records under the rekordbox id, or both
writers record under the pair's account id. Ledger only.
