---
title: sync twins still holds a track a landing through another account playlist brought in, which sync pair then adds
found: at the review of #593, U229, 2026-11-06.
issue: no
---

**The mechanism.** The twins backfill in `src/cratekit/sync/twins.py` reads `pair_cli.landed_isrcs` for each account playlist's own INBOX playlists, as `sync pair` did before U229. So a twin's track that the library holds because another account playlist's landing brought it in is recorded as held, and the next `sync pair` finds the row and adds it.

**Measured cost.** Driven by round one's review: the backfill held `t20`, `t21` and `t22` with the twin holding rows 3 and 1, and the sync pair right after held `t20` and `t21` and added row 9 for `t22`. Two verbs tell two stories about one library; nothing is downloaded and the end state is right.

**Closes when:** the backfill reads every landed INBOX playlist as `sync pair` now does. Ledger only: the next sync pair corrects it with no download.
