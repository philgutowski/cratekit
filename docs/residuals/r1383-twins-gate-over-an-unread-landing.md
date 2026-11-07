---
title: sync twins shows its gate over a landing record the session log cannot read, naming the tracks it brought in as having no row, and refuses only after the answer
found: at the review of #599, R-1383, 2026-11-07.
issue: no
---

**The mechanism.** `twins.read_library` in `src/cratekit/sync/twins.py` unpacks `pair_cli.landed_inbox_playlists` and drops its unread half by its own policy. `twins_cli.sync_twins` plans before any session gate, so the backfill's approve gate shows a twin's track that only an unreadable landing record brought in as a miss, "the library holds no row for it", with no warning naming the record. Only `twins.write` enters `session.assert_gates`, which refuses on the unread entry after the person answered approve.

**Measured cost.** Driven by round two's review on a torn record and on one carrying a state this build does not know: the gate showed three misses with no warning, and after approve the write refused with "the session log holds 1 entry this build cannot read". Nothing was written and nothing was queued. Both producers driven were hand edits; a record a later build writes was not driven.

**Closes when:** the backfill names the unread entries beside its misses on the gate, as `sync pair` does since R-1383. Ledger only: the write refuses before anything is written, and the backfill never queues a download.
