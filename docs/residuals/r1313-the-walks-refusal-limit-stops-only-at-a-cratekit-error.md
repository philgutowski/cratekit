---
title: The walk's refusal limit stops only at a CratekitError, so a failure met while handling a NoFileLanded or an adapter error raised from a 404 page reads as not found
found: at round one of #561's review, R-1313, 2026-11-06.
issue: no
---

**The mechanism.** `core.cause.failure_links` never enters a product refusal
off the declared chain, and a product refusal is a `CratekitError`.
`NoFileLanded` is a `RuntimeError` and the adapter's `AdapterError` family is
plain `Exception`, both raised from the provider failure they carry. A failure
with no status of its own raised while handling one of them, raised from a 404
page, is read through to the 404, so every reader of a not found calls it one:
R-703's rule that a `NoFileLanded` decides nothing by its cause holds for the
failure itself and not one hop out.

**Measured cost.** Driven by the review: a `ValueError` raised while handling
`NoFileLanded(cause=gone)` raised from a 404 page, and the same under
`AdapterBroken`, read `nearest_status` 404 and all four readers true. No
producer: the except handlers of 15 modules (8 of Cratekit's, 7 of the
client's) were grepped with a six line window for a provider call inside a
handler of either, and none was found;
`acquire_with_source` classifies the handled failure itself and
`fetch_with_retry` retries outside its handler.

**Closes when:** the walk's limit also stops at a `NoFileLanded` and an
`AdapterError`, or a test shows no reader is ever handed a failure raised
inside a handler of one. Ledger only: no producer.
