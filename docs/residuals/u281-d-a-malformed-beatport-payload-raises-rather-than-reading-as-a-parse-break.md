---
title: A Beatport payload whose tracks data is null or a list raises a TypeError rather than reading as a parse break
found: at the review of #796, U281, round two, 2026-11-13.
issue: no
---

**The mechanism.** `searchers._beatport_tracks` walks `props.pageProps.
dehydratedState.queries[].state.data.tracks.data` with `.get` on each step and
assumes each is a mapping. A `data` or `tracks` of `null`, or a list where a
mapping is expected, raises `AttributeError` or `TypeError` out of the
searcher, and the item fails as an internal error rather than as Beatport's
parse break. Present on `main` before U281; U281 adds one shape, a challenge
page that also carries a broken `__NEXT_DATA__`, which round one's order read
as blocked and the fixed order crashes on.

**Measured cost.** Driven on a fake page by U281's round two review, with the
same raise from `main`'s searcher. The producer was not driven: no Beatport
page of that shape has been seen, and Cloudflare's interstitial replaces the
page rather than carrying a Next payload.

**Closes when:** `_beatport_tracks` answers None for any payload whose steps
are not the shapes it reads, so the searcher answers a parse break, or
blocked when the page is a challenge. Ledger only: no producer measured.
