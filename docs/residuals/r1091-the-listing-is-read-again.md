---
title: A full label playlists build reads the label's listing again on every run, so a breaker trip inside the listing still starts it over
found: at the build of #410, R-1091, 2026-11-01.
issue: no
---

**The mechanism.** R-1091 keeps every release's tracks a full `crate label
playlists LABEL` reads, in `src/cratekit/label/kept_reads.py`, and the build
reads through them in `_grouped` in `src/cratekit/label/playlists_cli.py`. The
brief also asked for the listing to be kept the same way, and it is not:
`list_catalogue` still reads the roster, the discovery searches and every
roster artist's paged listing on each run, the gate run, the apply run and
every resume. A kept listing would hide a release the label put out after it
was read, for as long as the read is kept, and U191's test
`test_the_crawl_gate_is_asked_again_when_the_listing_grows` pins that a grown
listing asks the crawl gate again. So a breaker trip inside the listing itself
keeps nothing of it, as before R-1091.

**Measured cost.** Not measured. The listing is the roster and its pages,
nothing per release, so it is far fewer calls than the two a release that the
kept reads now save; how many it is for a label the size of Defected (12,368
releases listed on 2026-10-31) was never counted apart from the reads. Not
driven live in the cloud.

**Closes when:** the listing's own call count is measured on a large label
at an attended sitting, and either it fits inside one breaker window, which
closes this as measured, or the listing is kept per artist page with an age
short enough that a new release is seen within a day.
