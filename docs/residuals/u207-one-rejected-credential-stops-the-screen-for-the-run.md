---
title: One rejected app credential on an ISRC batch stops the screening for the run, though the next lookup refetches the token and succeeds
found: at the review of #497, U207, 2026-11-05.
issue: no
---

**The mechanism.** `Screen.screen` stops for the rest of the run on `AppCredentialsRejected`, on the reasoning that every later batch would be refused the same way. The app client drops its token on a 401 or 403, though, and the next request asks for a fresh one, so a token that lapsed inside its margin or was revoked mid run is refused once and then works. The lookups after it succeed, and the screening that would have saved them is off.

**Measured cost.** Driven by the round two review with a fake answering one batch 401: sixty codes the catalogue files nothing under cost 62 app reads, against 3 with no failure and 23 with a 503 on one batch. A real lapse or revocation was not driven against the provider. It costs request budget only: no false answer.

**Closes when:** a rejection on a batch is retried once with a fresh token before the screening stops. Ledger only.
