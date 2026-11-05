---
title: A stale access token whose refresh is answered with a page, or with JSON naming no error, is read as the provider being unavailable
found: at the review of #557, R-1305, 2026-11-05.
issue: no
---

**The mechanism.** When the stored access token has expired, tidalapi 0.8.11's
`basic_request` asks `token_refresh`, which decodes the oauth answer's body
before it checks any status (the client's `session.py`, about line 740). An
answer that is not JSON raises the decode error, and JSON with no `error` key
raises a `KeyError`; neither carries a status on any link, so
`provider_session.failure_links` finds nothing for `_rejected` or
`account._session_refused` to read, and the person is told the provider is
unavailable and the held account is kept. R-1305's fix reads a status wherever
the client leaves one; on this path it leaves none.

**Measured cost.** Driven by the review over the installed client with canned
answers: an oauth answer that is a 401 page, and one that is JSON without
`error`, both read `unavailable-transient`. A refresh answered 400
`invalid_grant` in JSON reads right (the client's `AuthenticationError` on the
declared chain), as does a refresh that succeeds and a sessions call then
rejected with a page. Whether the live oauth host ever answers with a page is
unmeasured; this is the path a stale session most often takes, so it is R-1305's
own cost if it does.

**Closes when:** the live oauth answer to a refresh with a revoked refresh
token is measured (the attended card filed with R-1305's landing), and, if it
can be a page, the refresh's decode failure is read as a rejection by a rule
the measurement justifies. Ledger only until then: no status exists to read,
so a fix now would be a guess.
