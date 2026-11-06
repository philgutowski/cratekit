---
title: The label sweep's 429 reader misses a 429 page under a declared wrapper
found: at round two of #561's review, R-1313, 2026-11-06, the shape one file over.
issue: no
---

**The mechanism.** `label.sweep`'s rate limit reader walks the declared cause
chain and the context chain each on its own (`_linked` over one attribute), so
a 429 whose body is a page, under a wrapper raised from it, sits on a context
link of a declared link and is reached by neither walk. `core.cause.failure_links`
reaches it.

**Measured cost.** Driven by the review: a `RuntimeError` raised from the
installed client's 429 page reads not rate limited, where the raw page and a
wrapped `TooManyRequests` read rate limited. R-704's cost, a label recorded as
permanently failed for a limit a wait would clear, if anything wrapped the
failure; no producer: each of the raise from sites on the sweep's path
(`tidal_catalogue`, `harvest`, `crawl`, `catalogue`, `listing`, `sweep`) hands
the reader the raw failure. Predates R-1305 and R-1313.

**Closes when:** the sweep reads its 429 through `core.cause.failure_links`
in place of the two single attribute walks, with a test raising a rewrapped
page through `tests/provider_answers.client_failure`. Ledger only: no producer.
