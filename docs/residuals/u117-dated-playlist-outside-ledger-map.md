---
title: A dated playlist is not in the outbound ledger's labels map, so the playlists sweep may read it as intake
found: at the review of #274, U117, 2026-10-10.
issue: no
---

**The mechanism.** A dated playlist created by U117 is not named in the
outbound ledger's `labels` map, so `ledger.label_playlist_ids` does not
carry it. The playlists sweep may therefore read it as intake.

**Measured cost.** Its tracks are owned, so owned dedup should drop them;
not driven past that reading. Excluding it would mean editing `ledger.py`
or `sync/playlists.py`.

**Closes when:** the outbound ledger names dated playlists with the year
ones, or the sweep has another way to leave them alone. Ledger only, or
U122 if that card takes the ledger write.
