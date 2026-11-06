---
title: The first reading of a removal is not held to what the same command's writes left, so a mirror apply or a prune's second chunk stops over a lag
found: at round one's review of #558, R-1308, 2026-11-06.
issue: no
---

**The mechanism.** `order_tracks` holds its first reading to what this
adapter's writes left (`_settled`, U220); `remove_tracks` takes its first
reading through `_positions` as it comes. The mirror's apply adds then
removes on one playlist (`mirror.py`, the add before the removal), and
prune takes a playlist's removals off in chunks of 50, one `remove_tracks`
call each, so either can meet a first reading that lags its own earlier
write. Driven on the U220 stand in: add `x` then remove `b` under a whole
lag of one is answered 412 and raised as `unavailable-transient`; under a
tracks only lag it is refused `positions-unknown` at source. A removal
answered 412 changed nothing but is raised rather than read again, which
R-1308's brief kept out of scope.

**Measured cost.** A mirror apply or a prune stops after its adds or its
first chunk landed, with a true message; running it again does the rest.

**Closes when:** the first reading of a removal is held to `_members` when
this adapter wrote the playlist in this process, read again on the order's
pauses as `_settled` does, and a removal answered 412 is read again and
planned afresh as a move answered 412 is. Ledger only: the run again
finishes the workflow.
