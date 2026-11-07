---
title: A pair's first sync over a short account listing plans an account addition of a withheld track every sync and never records a snapshot
found: at the review of #620, R-1416, round one, 2026-11-07.
issue: no
---

**The mechanism.** On a first sync the account listing comes back short when the provider withholds a track it holds. The withheld track is held in rekordbox, so the merge plans it as an account addition, and since a short listing records no snapshot the pair stays a first sync and plans the same addition at the next run.

**Measured cost.** Driven by the round one reviewer on the fake account: a hand pair at the root with `t2` withheld and rekordbox 3, 1, 2 plans `account add t2` on every run, each run says `sync-pair-written`, and `held.first` stays true. The items are identical on main at 5f08ae57, so it predates R-1416. On a real provider that is an addition of a track the playlist already holds; measured only on the fake, which drops the duplicate, so the real provider's answer is unmeasured.

**Closes when:** a first sync over a short listing plans no account addition of a track the account counts but does not serve, driven on the fake with a provider that keeps duplicates. Ledger only until the real provider's answer is measured.
