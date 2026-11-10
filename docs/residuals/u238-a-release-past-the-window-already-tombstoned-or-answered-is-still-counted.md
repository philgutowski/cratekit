---
title: A release past a label's offer window that is tombstoned, already queued or already answered is still counted as the label's past the window
found: at the review of #646, U238, 2026-11-10.
issue: no
---

**The mechanism.** `sweep._past_window` judges each release past the window
by its copyright line alone. A release a person deleted on purpose
(tombstoned), one already in the review queue, or one a `label sync`
answer already covered is counted as one of the label's releases past the
window, though raising `--offer` would offer none of them: inside the
window a tombstoned one takes no place and an answered or queued one takes
a place without being offered again.

**Measured cost.** Driven by round one's review through `label sync --next`
on a roster whose seven releases past a window of three were tombstoned
in the store directly: the question said "7 more of the label's
release(s) past this run's window", and with the offer raised to ten the
next run said nothing new. An answered release pushed past the window by
a newer one is counted the same way (8 said where 7 were never asked).
The tombstones were written to the store, not by the delete verb, so the
reach through a person's own deletions is unmeasured. The statement is
true (they are the label's releases); it is not the number the person
raises the window against.

**Closes when:** the count past the window leaves out a release the
tombstone reader suppresses and one in the offered set, both answered
locally with no provider call, and `LabelListing.beyond`'s docstring, the
offer window entry in `CONCEPTS.md` and the guide say so. Ledger only: the
card scoped the figure to the label's needle, and the figure says nothing
false.
