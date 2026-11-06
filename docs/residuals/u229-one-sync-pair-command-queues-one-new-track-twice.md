---
title: One sync pair command queues a track no landing brought in once for each pair listing it, and again beside another pair's job still holding it
found: at the review of #593, U229, 2026-11-06.
issue: yes
---

**The mechanism.** `_queued` in `src/cratekit/sync/pair_cli.py` reads only the jobs this pair queued, and `_owned` reads another pair's job only once it SUCCEEDED and only for an `owned` report. So two plain pairs listing one new track each plan it as `acquire` in one command, and a pair listing a track another pair's pending job already holds plans it again. U229 made a track a landing brought in through any account playlist the library's row; a track not yet landed is outside that brief.

**Measured cost.** Driven by round one's review: two pairs listing `t40` queued two jobs holding `t40` in one command, and a pair listing `t8` beside another pair's pending job holding `t8` queued a second job. Whether the second job downloads a second copy or resolves owned by the first file's ISRC when it runs was not driven.

**Closes when:** a sync pair plans a track any pending or running `sync pair` job on the library holds as `awaiting`, and two pairs in one plan listing one lacking track queue it once. It earns an issue because a second download job for one track is what the card's goal forbids, a day earlier.
