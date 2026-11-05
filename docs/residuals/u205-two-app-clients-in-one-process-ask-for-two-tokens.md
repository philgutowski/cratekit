---
title: A process that opens both the outbound account and the label catalogue builds two app clients and asks the token service twice
found: at the review of #495, U205, 2026-11-05.
issue: no
---

**The mechanism.** `tidal_account.open_account` and `tidal_catalogue.open_catalogue`
each call `provider_session.catalogue_client`, which builds its own
`AppCatalogue` with its own token. A verb that opens both in one process
fetches the app's token twice, one gated call more than it needs.

**Measured cost.** Driven by the review with both values recorded: two token
requests for two reads, one extra paced call per process that opens both. No
wrong answer.

**Closes when:** the token, or the client, is held once per process and the
second opener reuses it. Ledger only.
