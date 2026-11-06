---
title: The paced pool's status read takes the failure alone, so a 403 or 429 whose body is not JSON says nothing about pacing
found: at the build of #561, R-1313, 2026-11-06, hunting the class one file over.
issue: no
---

**The mechanism.** `acquire.download.status_of`, which `classify_signal` asks
first, reads a status off the failure itself and none of its links. A provider
answer whose body is not JSON reaches it as the client's decode error with the
HTTP error three context links down (R-704, R-1305, R-1313), so a 403 page
reads as no status, then as text that is the decoder's own, and the pool hears
no account block. A 429 page is the same shape, though the provider gate counts
a rate limit off the raw response at the transport, so only the block is
unheard.

**Measured cost.** Not driven. The pool's one source today is the vendored
tool, which swallows a provider failure and raises `NoFileLanded`, read as no
signal before any status, so a raw client failure reaching `classify_signal`
needs a source that lets one through. The other readers of a status off a
client failure found by a grep of `src` for `status_code` walk the links (the
two of a rejected session, the four of a not found, `_stale_tag` and the label
sweep's 429); this is the one found that still does not.

**Closes when:** `status_of` reads the nearest status through
`core.cause.nearest_status` when the failure carries none of its own, with a
test raising a 403 and a 429 page through `tests/provider_answers.client_failure`.
Ledger only, for the reachability above.
