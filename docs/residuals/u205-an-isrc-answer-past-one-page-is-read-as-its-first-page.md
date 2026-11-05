---
title: An ISRC lookup on the app client reads the first page of the answer and never its next link, as the account's lookup did
found: at the build of #495, U205, 2026-11-05.
issue: no
---

**The mechanism.** `AppCatalogue.get_tracks_by_isrc` in
`acquire/catalogue_api.py` reads `data` off one answer and ignores
`links.next`, as tidalapi 0.8.11's `Session.get_tracks_by_isrc` does on the
account. A code the catalogue files under more releases than one page holds is
answered with the first page's tracks only, so `_among` chooses among fewer
candidates than exist: a hearted release on the second page is not seen, and
one agreeing release can read as the only one.

**Measured cost.** Not driven: no fixture or live answer this container could
reach carries a second page, and the page size of the filter endpoint is
unmeasured. The behaviour is unchanged from before U205.

**Closes when:** #497 (U207) probes the endpoint's page size and batching, and
a lookup either follows `links.next` inside `acquire.listing`'s ladder or
refuses an answer with a next link rather than choosing over part of it.
Ledger only: unmeasured, and no worse than before.
