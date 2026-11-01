---
title: tag guess reads a playlist's owned tracks by the paths their reports recorded, without the prefix map, so on a moved volume they give no vote and nothing says so
found: at the review of #353, U172, 2026-11-01.
issue: no
---

**The mechanism.** `tagging.guess_cli._playlists` reads each owned member's genre from the library file its intake report named, as recorded. `account_playlists.resolve_owned` applies `cfg.resolved_prefix_map()` to the same paths before it looks a row up. A path that needs the map reads as an unreadable file, which `guess.read_member` drops, so the playlist's share is taken over its staged members alone.

**Measured cost.** Read, not driven on a library whose paths need the map; `read_member` on a missing path returning None was driven. On Phillip's machine the reports and the volume name the same paths, so the cost is a weaker playlist vote on another DJ's moved library, unsaid.

**Closes when:** the owned paths go through the prefix map before they are read, or a dropped owned member is counted in the report. Ledger only.
