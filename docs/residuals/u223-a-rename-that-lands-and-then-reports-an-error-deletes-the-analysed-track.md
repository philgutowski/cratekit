---
title: A rename that lands and then reports an error makes analyze run delete the analysed track under its new name
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** `_finalize` in `src/cratekit/analysis/cli.py` removes the
claimed target on any `OSError` from `path.rename(target)`, to drop its own
zero byte claim. A filesystem that completes the rename and then reports an
error (the retransmitted rename shape of a network mount) leaves the analysed
file at the target, and that removal deletes it: the folder holds neither
name, and the next attempt refuses `source-missing` over a deleted track.
The removal predates U223; U223 only drops the intent and report beside it.
The same shape sits in `write/naming_cli.py` and `intake/repair_cli.py`.

**Measured cost.** Driven by the round two reviewer with `Path.rename`
patched to rename and then raise EIO: the folder empty, the item
`analysis-write-failed`. Reachability unmeasured: no candidate on a local
disk produces a rename that lands and raises, and no network mount was
driven.

**Closes when:** the error path removes the target only when it is still the
zero byte claim (its size is 0 and the source is still a file), in all three
places. Ledger only until a producer is driven; then it meets the board bar
as lost files.
