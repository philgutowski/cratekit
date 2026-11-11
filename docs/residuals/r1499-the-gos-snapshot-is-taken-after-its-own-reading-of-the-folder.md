---
title: The go's tail snapshot is taken after its own reading of the folder, so an arrival between the two is its own
found: at the review of #665, R-1499, round two, 2026-11-11.
issue: no
---

**The mechanism.** `label sync --go` reads the folder in `label/go.py` before it returns its landing, and `cli/label_sync.py` takes the snapshot the arrival check compares against afterwards. A download another process finishes between the two is in the snapshot, renamed by the tail, planned into the go's landing and kept as the go's own. `crate sync land` takes its snapshot inside the same reading and has no such gap.

**Measured cost.** Driven at round two with a hook placing a second process's download in the window: the go's landing took it with no warning. The window measured 0.5 to 0.8 ms over ten runs on the fixture library.

**Closes when:** the go takes its snapshot before its own reading, or `cli/label_sync.py` reads the folder once more after taking it. Ledger only, since the producer needs a concurrent second driver in a sub millisecond window.
