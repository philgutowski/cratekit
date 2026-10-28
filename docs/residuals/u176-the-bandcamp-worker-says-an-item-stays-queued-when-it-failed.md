---
title: The Bandcamp worker, like the download and fallback workers, says an item stays queued when the item has failed
found: at the first review of #357, U176, 2026-10-28.
issue: no
---

**The mechanism.** A transient failure of one release in
`bandcamp_cli.handle_fetch` is refused with "it stays queued", the wording
`acquire.cli` and `acquire.fallback_cli` use for the same case. The engine
records the item failed and, when nothing else succeeded, the job failed;
`job retry` re-arms it.

**Measured cost.** Driven: the message says queued while the envelope's state
and the exit code say failed. The envelope is right, so nothing is lost; the
sentence is wrong in three workers.

**Closes when:** the three workers say the item failed and can be retried,
with the retry command. Ledger only, a wording fix.
