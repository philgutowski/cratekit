---
title: The behaviour scenarios record the fake account's writes per kind, not its reads or the order across kinds, and no verb reaches a reservation already taken
found: at the review of #866, U309, 2026-11-22.
issue: no
---

**The mechanism.** `tests/behaviour/outbound.py`'s `account_calls` writes `vars(account)` of the suite's fake, which keeps one list per kind of write. Reads (`folders`, `folder_playlists`, `playlist_tracks`, `playlist_listing`) are not recorded, and the order of calls across kinds is not captured, so the card's "the same calls in the same order" is proved by the scenarios for writes within a kind and by the mirror's printed request count, and otherwise by the review's base against branch drives of the account (3,000 trials comparing every request, move, removal and read back). No scenario reaches a reservation already taken through a verb (the rename twin stands in), the INBOX or Favorites mirror, `mirror-downloads`, the inspiration write, a stale answer, or a filing or root failure part way.

**Measured cost.** Not driven: a change of call order across kinds would pass the comparison and be caught only by the suite's own order tests.

**Closes when:** the fake account records every call, reads included, in one ordered log that the capture writes, and a scenario drives a ledger reservation held by another run. Ledger only.
