---
title: The twins' backfill finds no row a landed track's intake job resolved, where sync pair would
found: at the review of #330, U149, 2026-11-01.
issue: no
---

**The mechanism.** `twins.Library.find` looks for an account track's row by the mirror's link, the database ISRC, the mirror's recorded ISRC and the INBOX playlists landed for that account playlist. `pair_cli._owned` has one more source, the intake jobs the pair queued. A row with no ISRC in the database or its file, landed long enough ago that its INBOX playlist has rotated out, is a miss on the backfill's gate.

**Measured cost.** Not driven. Such a miss is named on the gate and the snapshot records it as an account track the twin lacks, so the next `sync pair` looks again with its own sources and adds it if it finds it; nothing is lost, the twin is short until then.

**Closes when:** the backfill reads the sweep's intake jobs for each account playlist as a source, or the attended backfill shows no such miss. Ledger only.
