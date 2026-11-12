---
title: A removed rekordbox streaming row holds the deletion watermark below it on every run
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** A row the person removed in rekordbox whose location is the
streaming spelling resolves unmapped in `candidates.categorize`, which U243 did
not change, so it is never handled and the watermark stays below its sequence.
Every later run walks the removals above it again.

**Measured cost.** Driven by the round one review: one removed streaming row at
sequence 45 over a baseline of 40, a completed run, the watermark still 40,
`unresolved: 0`, and no warning. Nothing is trashed wrongly; the cost is a
re-walk and a watermark that never moves past a streamed removal.

**Closes when:** a removed row that names no local file is handled as settled
absence, with a test over the watermark. Ledger only.
