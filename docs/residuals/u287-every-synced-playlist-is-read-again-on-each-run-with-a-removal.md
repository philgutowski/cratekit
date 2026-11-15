---
title: sync removed reads every synced playlist again on each run that finds a removal, past the default call ceiling on a large account
found: at the build of #373, U287, 2026-11-15.
issue: no
---

**The mechanism.** "Still on another synced playlist" is a claim about every playlist the cursor, the taken record and the pairs hold, so a run that finds any removal opens and lists each of them, about two calls a playlist. The taken record held 599 playlists when U242 migrated it, so a run on the live account passes `[provider] calls_per_command` (500) and the hour's reading line, and stops as the call ceiling or the hour's budget with nothing offered.

**Measured cost.** Not driven against the live account. It fails closed: the refusal names the ceiling, and `crate --calls N --calls-per-hour M sync removed` finishes it, the way a first `sync pair` plan does. Every run pays the calls again.

**Closes when:** the synced listings are read once per pass and kept, or the playlists a removed track could be on are narrowed by something the account says, or Phillip judges the cost acceptable. Ledger only.
