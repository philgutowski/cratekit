---
title: A walk that broke on a page carrying an older tag leaves the client holding that tag
found: at the build of R-1360 (#585), 2026-11-06.
issue: no
---

**The mechanism.** The client overwrites its `_etag` on every response, so
after a walk that broke on a later page carrying an older tag the client
holds that older tag, and the adapter's rule that the unpaged read is taken
last, so the next write carries the current tag, no longer holds. Beside a
whole window such a reading lags and nothing is written from it. Beside a
window short of the declared count (R-1362, a track the account cannot
play) it agrees, and a write sent from it carries the older tag.

**Measured cost.** Not driven. A write sent with an older tag is answered
412, which the adapter already reads again and retries (U220), so the cost
is one refused request and a pause, and a removal from such a playlist is
refused `positions-unknown` before anything is sent.

**Closes when:** R-1362 is built, or the walk reads its first page again
after breaking. Ledger only.
