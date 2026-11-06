---
title: A removal refused as possibly landed under a lagging read is recorded by no caller as taken off
found: at the build of #558, R-1308, 2026-11-06.
issue: no
---

**The mechanism.** When `remove_tracks` refuses with `lagged: yes`, the
removal may have landed, but prune, the mirror, `label heard` and
`sync pair` each record only what a returned removal said, so a removal that
did land is not in their records. A run again plans from a fresh reading of
the playlist and does not ask for it again once the read shows it.

**Measured cost.** Not driven past the adapter. A record of what was taken
off is short by the asked tracks until the next run reads the playlist.

**Closes when:** a caller records a possibly landed removal as such, or the
next run is shown to settle it. Ledger only.
