---
title: A continue pays again the artist read and the pages of the one listing a ceiling stopped inside, and a dropped seed discovery credits is read twice
found: at the review of #533, U217, rounds one and two, 2026-11-05.
issue: no
---

**The mechanism.** The kept listing keeps whole answers, and an artist's
listing is one answer however many pages it is, and the provider object of a
kept artist is not kept. So a ceiling that stops inside an artist's paged
listing loses that listing's pages, and the continue reads the artist again by
identifier and pages that one listing from the start. Separately, a kept seed
that the provider dropped and that discovery also credits is read once by
discovery and once more lazily by the roster.

**Measured cost.** Driven by the review over a 101 call fresh listing: a stop
anywhere in the searches continues for exactly the remainder (101 in all), a
stop inside an artist's listing for 102 or 103 in all. The dropped seed costs
one extra call per run. Every count the listing line shows stays true.

**Closes when:** a listing's pages are kept as they arrive, which needs the
paging wrapper in `acquire/listing.py` to hand pages out, and the identified
answer is consulted before a lazy read. Ledger only, calls only.
