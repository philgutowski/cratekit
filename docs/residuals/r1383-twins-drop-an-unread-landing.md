---
title: sync twins still reads a landing record the session log cannot read as no landing, and reports the track it brought in as not owned
found: at the build of #599, R-1383, 2026-11-07.
issue: no
---

**The mechanism.** `twins.read_library` in `src/cratekit/sync/twins.py` unpacks `pair_cli.landed_inbox_playlists` and drops its unread half by its own policy, said in a comment there. So a twin's track that only an unreadable landing record brought in is a miss named `not owned`, and the twin is made without it, where a sync pair now names the record and holds the track.

**Measured cost.** Not driven through the backfill. The backfill holds a miss and queues nothing, so the cost is a held track whose reason says not owned when the record that would say otherwise could not be read; the next `sync pair` of the twin names the record and holds the track rather than queue it.

**Closes when:** the backfill names an unread landing record beside its misses, or a miss whose code an unread record may hold says so. Ledger only: nothing is written or queued from it, and `sync pair` holds the track.
