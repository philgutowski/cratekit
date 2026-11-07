---
title: The sync pair awaiting warning counts each pair's listing of a track as a track, in two sentences joined like its rows
found: at the review of #600, R-1385, 2026-11-07.
issue: no
---

**The mechanism.** `_warnings` in `src/cratekit/sync/pair_cli.py` counts awaiting rows, one per pair listing the track, and calls them tracks, so two pairs listing `t40` read "2 account track(s)" over one track and one job. Since R-1385 the warning has two sentences, what a job holds and what another pair of this sync is to queue, joined with the same "; " as the rows inside each. And `if here:` before the second sentence kills no test: a warning of only the first kind would otherwise gain an empty second sentence.

**Measured cost.** Driven by round two's review: the count and the join read as above; every sentence is true. The `if here:` mutation passed the sync tests and added no sync failure to the full suite.

**Closes when:** the warning counts distinct tracks, separates its sentences from its rows, and a test pins a warning holding only tracks a job holds. Ledger only.
