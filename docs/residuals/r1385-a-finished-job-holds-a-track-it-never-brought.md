---
title: Another pair's finished job holds a track it never brought in, so no pair queues that track again
found: at the review of #600, R-1385, 2026-11-07.
issue: no
---

**The mechanism.** Since R-1385, `_Reader.held_by_jobs` in `src/cratekit/sync/pair_cli.py` reads every `sync pair` intake job on the library that did not fail or cancel, a SUCCEEDED or BLOCKED one included, as holding its tracks for every pair. A pair's own jobs were read that way before, so a finished job whose report left a track neither owned nor landed (missing, offered, suppressed, or a landed file deleted since) names it `awaiting` on every later sync, now for every pair listing it, and nothing queues it again.

**Measured cost.** Driven by round one's review with the job's reports stubbed: a SUCCEEDED job of another pair reporting `t40` missing kept `t40` awaiting "queued for Another" on every sync. No real job leaving such a report was produced: the intake handler fails a job whose items fail. Read as the conservative side of the card, since not counting a finished job would download again a track it left waiting to land.

**Closes when:** a pair job's track is read as held only while the job is unfinished or its report says the track was downloaded and waits to land. Ledger only: the warning names every such track, and `crate job cancel` on the job frees it.
