---
title: What a stale cancel says it frees is read from the open jobs alone, so a playlist the sweep leaves out for another reason is still said to queue again
found: at the build of #379, U182, 2026-11-01.
issue: no
---

**The mechanism.** `_frees` says a cancel frees a playlist, "so the next pass queues it again", when no job staying open holds the same playlist. The sweep's exclusion has other reasons before the open job one (`sync.playlists.exclusion`): a playlist the cursor recorded, a swept prefix, a placeholder name, a label or set playlist, an empty one. The cancel reads only the queue, so for such a playlist the sentence promises a queue the next pass will not make.

**Measured cost.** Not driven: no fixture produced an open intake job for a playlist the sweep also excludes for another reason. A job open for a recorded playlist would have to have been queued by hand after the record, which no candidate driven produced.

**Closes when:** the sentence is read through the sweep's own exclusion, or worded as "no open job holds it any longer". Ledger only.
