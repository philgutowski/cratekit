---
title: Several U204 guards are killed by no test in the touched files
found: at the review of #494, U204, 2026-11-05.
issue: no
---

**The mechanism.** The reviewers' guard sweeps reverted each guard alone over
the touched test files. Pinned after round one: the INBOX latch, the
favourites restore detection, the favourite read back, the quarter refusal, the
queue's second read and a failed job freeing its track. Still killed by no test
after round two: the AGREED clause's `not there_m & away`, the month move's
`pid in held`, the ledger link guard on adoption in `_read_edits`, the matcher's
codes in `_owned`, the folder guard on a title two folders share
(`_read_edits`, `holds_for`), `Applied.wrote` counting a colour and a made
month, the settle keyed by tree, a month already held, and the source at the
playlist root refusal. The second fix round, `Hold.stay` and the finished job
outcomes, was not reviewed, since both rounds were spent; each has a test that
fails without it.

**Measured cost.** None to a user named; the behaviour is unpinned. The
mutation table, `docs/mutation/u204.md`, is the author's measure of the rest.

**Closes when:** each has a test that kills its revert. Ledger only.
