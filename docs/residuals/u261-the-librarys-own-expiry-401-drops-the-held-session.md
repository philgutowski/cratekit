---
title: The provider library's own recoverable expired token 401 drops the held session, costing a login and an account adapter rebuild per expiry
found: at the review of #690, U261, 2026-11-12, round one.
issue: no
---

**The mechanism.** `provider_session._watch` drops the process's held
session on any 401 or 403 answered through the shared client. The provider
library answers an expired access token with a 401, refreshes it and asks
again, which the watch cannot tell from a refusal, so the hold is dropped
although the client recovered.

**Measured cost.** Driven by the review (probes P3 and P7): one more login
per token expiry, two paced requests, and the account's held adapter is
rebuilt, so its per process reads are made again (not measured). No wrong
answer: the refreshed token reaches the keychain on the next login, which
`main` never stored.

**Closes when:** the watch tells the library's recoverable expiry from a
refusal, or the cost is judged too small to matter. Ledger only.
