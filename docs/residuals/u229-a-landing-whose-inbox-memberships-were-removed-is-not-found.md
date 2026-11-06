---
title: A track whose landing's INBOX memberships were removed is no longer found by its landing, and a sync pair queues it again
found: at the review of #593, U229, 2026-11-06.
issue: no
---

**The mechanism.** A landed row with no database ISRC is found by `landed_isrcs` in `src/cratekit/sync/pair_cli.py` only through its live membership of the INBOX playlist its landing made. Once those memberships are soft deleted, the row is named by nothing a plan reads, and a track listed on a pair is planned as `acquire`.

**Measured cost.** Driven by round one's review: with the INBOX playlist and its memberships soft deleted the plan queued the track, and with the playlist alone deleted it still found the row. Whether rekordbox or `inbox rotate` ever soft deletes the memberships when an INBOX playlist goes was not measured.

**Closes when:** the landing writes the ISRC into the row, out of U229's scope, or a measurement shows nothing removes the memberships. Ledger only until that is measured.
