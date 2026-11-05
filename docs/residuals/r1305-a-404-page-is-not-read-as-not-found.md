---
title: A 404 whose body is not JSON is read as an outage, not as not found, by the account, the catalogue and the ISRC cache
found: at the review of #557, R-1305, 2026-11-05.
issue: yes
---

**The mechanism.** R-1305's shape on a different status. The provider client
decodes an error answer's body inside its own handler of the HTTP error, so a
404 whose body is a page never becomes `ObjectNotFound`: it surfaces as the
decode error with the 404 three context links down. Four readers of a not
found read the failure itself or its declared causes only:
`modules/outbound/tidal_account._not_found`, `acquire/isrc_cache.said_not_found`,
`label/tidal_catalogue`'s 404 reader, and `acquire/adapter.classify_unavailable`.

**Measured cost.** Driven over the installed client (tidalapi 0.8.11) with a
canned answer: a 404 page is read as not found by none of the four, a 404 in
JSON by all four. A track or release the provider has nothing for is then
retried, failed as `unavailable-transient` and asked again every run, never
remembered as gone, the R-380 shape `tidal_catalogue`'s docstring names. Whether
the provider answers 404 with a page is unmeasured.

**Closes when:** each of the four readers also reads a 404 status reached as
context, through `provider_session.failure_links` or a walk with its limits,
with a test per reader raising the failure through the client's own handler
(`tests/provider_answers.client_failure`). Earns an issue: the product says an
outage where the provider said gone (board bar b), and it is buildable in the
cloud as R-1305 was.
