---
title: A twin paired before U221 reads a naive account date as UTC, so a track dated before its mark in a zone east of UTC can read as added after it and be queued
found: at the review of #549, U221, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_cli.held_for_choice` reads a twin that recorded
no hold by time: a track is held unless the account dates its addition after
the pair's mark. The dates come through `intake_cli._added_dates`, whose
`hearted_on` reads `user_date_added` with `placeholders.parse_hearted`, and
that reads a date with no zone as UTC (`as_utc`). A wall clock date one hour
before the mark in a zone at +05:00, served with no zone, reads as four hours
after it.

**Measured cost.** Driven on the twins world by round one of U221's review:
with `on_hold` dropped from the pairs document and the track dated as a naive
+05:00 wall clock an hour before the mark, `sync pair` queued it. No live
producer was driven: the provider's client parses `dateAdded` into an aware
datetime, and `tidal_account._added_at` drops naive ones, so the reachability
on the live account is unmeasured. A track queued this way is a download
Phillip did not choose, among sitting 63's twins only.

**Closes when:** the time rule reads a date the account gave with no zone as
unknown, which holds, rather than as UTC. Ledger only while no producer of a
naive date is found.
