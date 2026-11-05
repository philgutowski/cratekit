---
title: A rejected session read from a page quotes the decode error, not the status that decided it
found: at the review of #557, R-1305, 2026-11-05.
issue: no
---

**The mechanism.** `account.provider_failure` and `provider_session.client_session`
put `str(exc)` in the message they raise. For a 401 or 403 whose body is not
JSON, `exc` is the client's decode error, so the person reads "the provider
rejected the stored session (Expecting value: line 1 column 1 (char 0))".

**Measured cost.** Printed by the review through `account.resolve` and
`provider_failure` for a 401 page and a 403 page: the reason and the remedy are
right, and the parenthesis names nothing a person can act on. No false
statement.

**Closes when:** the two messages name the status `failure_links` found (for
example "answered 401") when the failure itself carries none. Ledger only, a
wording fix.
