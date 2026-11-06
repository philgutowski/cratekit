---
title: A removal's read back whose declared count or videos cannot be read now stops the mirror apply as a possibly wrong track
found: at round one's review of #558, R-1308, 2026-11-06.
issue: no
---

**The mechanism.** Before R-1308 a read back whose count or video count could
not be read, or declared a video, was refused `positions-unknown` at
`Scope.SOURCE`, which the mirror's apply keeps as "nothing was taken off it"
and carries on past, although the removal had been sent. R-1308's read back
refuses it at `Scope.RUN` as `read-back-differs`, "a track other than the
asked ones may have come off", which stops the apply.

**Measured cost.** The new answer is the more conservative and the old one
was false; no provider was driven that changes its declared counts' shape
between the first reading and the read back.

**Closes when:** a provider is seen to do so; ledger only, a seam note.
