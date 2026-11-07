---
title: The mark guard on a stopped write kills only its pure tests, since a first sync now reads the stop through first_stop and a later sync's snapshot guard covers it
found: at the review of #597, R-1376, round one, 2026-11-07.
issue: no
---

**The mechanism.** `_Reader.stopped_write` refuses a write that began before the pair was marked (R-1372). Since R-1376 every first sync, one with no pair record or one with no snapshot, reads the stop through `_Reader.first_stop` whatever the mark, and every later sync has a snapshot no earlier than its mark, which the snapshot guard already compares. So the mark guard decides no plan the dispatcher can reach, short of a pairs document holding a snapshot with no sync time.

**Measured cost.** Maintainer facing. The reviewer's row removing the guard killed 2 of 84, both the pure reader tests in `tests/test_sync_pair_stopped.py`; no scenario test dies. Kept, since the card asked that every existing refusal stay.

**Closes when:** the guard is removed with its pure test, or a reachable input it decides is driven and pinned. Ledger only.
