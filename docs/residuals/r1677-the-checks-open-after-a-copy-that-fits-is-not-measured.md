---
title: The integrity check's open after a throwaway copy that fits makes files the room measure counts only through its headroom
found: at the review of #813, R-1677, 2026-11-13.
issue: no
---

**The mechanism.** `snapshot.assert_room_for_check` measures the file set the
check copies, `rb_writer.file_set`, with the capture's ten percent headroom.
Opening the copy then makes a shared memory index (32 KiB here) and may grow
a log, neither of which is in the file set. When the copy fits and those do
not, `open_db` refuses with a disk input output error, `integrity_ok` answers
False as for any failed open, and the capture is refused as
`snapshot-integrity-failed` with the remedy to report a defect: the card's
symptom one step past the copy. The branch keeps it that way on purpose, so
that no failure after the copy is ever told as a room message
(`test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`).
Separately, `open_db`'s failure path leaks the connection, which holds the
deleted throwaway open, so inside one process the space stays pinned; that
predates this card.

**Measured cost.** Driven by the review on a real tmpfs with the measure
bypassed, at 330 KiB to 352 KiB for a 330 KiB file set: refused as above.
With the measure in place it needs a temporary volume that fills between the
measure and the copy, or a database under about 330 KB, where the headroom is
smaller than the index. A real library is far larger, so the headroom covers
it; no producer with the measure in place was driven.

**Closes when:** the open's own files are counted in the measure (a fixed
allowance for the index and the log), or a failed open on a copy whose volume
reports no free space is told as no room. Ledger only.
