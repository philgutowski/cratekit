---
title: The refusal limit in the provider failure walk names only the product's refusals, not the adapter's own errors
found: at the review of #557, R-1305, 2026-11-05.
issue: no
---

**The mechanism.** `provider_session.failure_links` never enters a
`CratekitError` off the declared chain, so a failure met while handling a
refused session is not read as that refusal. `AdapterAuthFailed`,
`AdapterBroken` and `ProviderUnavailable` are the adapter layer's own errors and
plain `Exception` subclasses (`acquire/adapter.py`), so a provider call made
inside a handler of one of them would be walked into, its 401 cause and all,
and read as a rejected session.

**Measured cost.** Not driven, because nothing produces it: the review read all
13 handlers of those three types in `src` and the job engine's item boundary,
and none makes a provider call inside the handler. 13 candidates driven in
reading and none produces it.

**Closes when:** the limit also names `AdapterError`, with a test raising a
provider failure inside a handler of `AdapterAuthFailed`, or a unit adds such a
handler and pins it. Ledger only, a maintainer facing shape.
