---
title: A twin read by time holds a track the account lists with no date, even one added by hand after the twin was made
found: at the review of #549, U221, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_cli.held_for_choice` reads a twin that recorded
no hold (paired before U221, or made from a short listing) by time, and an
undated track reads as held, the conservative way, since the time rule cannot
tell it from one listed before the mark. So a track Phillip adds to the
account playlist by hand after the twin was made, if the account serves it
with no date, waits for `crate sync release` rather than being queued.

**Measured cost.** Driven on the twins world by round two of U221's review: a
short listing backfill, then t22 appended dated after the mark and t23
appended undated; `sync pair` queued t22 and held t23. `docs/GUIDE.md` says
so. Whether the live account ever serves an undated track is unmeasured. The
cost is a wanted download that waits for one release, never one made unasked.

**Closes when:** the account is shown always to date an addition, or the hold
is recorded for a short listing too, so the time rule is never read for a
twin made since U221. Ledger only.
