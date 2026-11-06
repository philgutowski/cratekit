---
title: A landing record the session log cannot read is read as no landing, so a sync pair queues the landed track again with a clean report
found: at the review of #593, U229, 2026-11-06.
issue: yes
---

**The mechanism.** `landed_inbox_playlists` in `src/cratekit/sync/pair_cli.py` takes `session.scan_log`'s records and discards its unreadable list, so a landing whose record does not read (torn, or a state value this build does not know) names no INBOX playlist, and a track only that landing brought in is planned as `acquire`. Since U229 every pair reads every landing this way, so the shape now carries the whole of the card's fix. Pattern one, absence read as evidence of absence.

**Measured cost.** Driven by round one's review on two hand damaged records, one rewritten with an unknown state and one torn: both times the plan queued the landed track and warned only `sync-pair-written`. The natural producers, a record a later build writes or a log directory the account cannot list, were not driven.

**Closes when:** a plan that finds an unreadable landing record names it in a warning and plans no `acquire` for a track it could not rule out, or refuses, as the session log's own gates do. It earns an issue under the board bar's (b), a clean report over state the tool could not read.
