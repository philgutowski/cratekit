---
title: Under a token service outage the ISRC screen asks for a token once a batch and reports each batch as a request made
found: at the review of #497, U207, 2026-11-05.
issue: no
---

**The mechanism.** `Screen.screen` treats a failed batch as nothing learned and goes on to the next one, unless the failure was a rate limit, a rejected credential or a 4xx. A token service answering 503 fails every batch before its read, so each batch spends one token request. Each one is also counted in the number `screen_isrcs` returns, though no catalogue request was sent.

**Measured cost.** Driven by the round one review: 45 codes with the token endpoint answering 503 cost three token requests, no catalogue request and nothing marked absent. `screen_isrcs` returned 3. The lookups that follow then refuse as they did before U207. That is three wasted calls on the gate, and a request count in the mirror's plan fact that is three high.

**Closes when:** a failure that never reached the catalogue stops the screening for the run, and a batch that sent no read is not counted. Ledger only.
