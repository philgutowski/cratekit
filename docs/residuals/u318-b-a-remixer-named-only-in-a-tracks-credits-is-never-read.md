---
title: A Discogs track whose remixer is named only in its credits is read as no mix, and the miss says the release lacks it
found: at the review of #882, U318, round one, 2026-11-21.
issue: no
---

**The mechanism.** `_discogs_release` reads each track's `title` and
`artists` and never its `extraartists`, so a track "Sunrise Mood (Remix)"
credited Remix: Tide writes no maker, and a file "Sunrise Mood (Tide Remix)"
is refused with a note that the release holds no track with its version,
over a field that was never read.

**Measured cost.** Driven on a hand built release through `tag_one`: main
matched, the branch misses with that note. How often Discogs names a
remixer only in a track's credits is unmeasured.

**Closes when:** the release reader carries each track's remix credits and
`writes_version` reads them. Ledger only: the cost is a miss.
