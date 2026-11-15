---
title: An untagged file's split artist changes which uncredited Traxsource and Bandcamp rows match it
found: at the review of #843, U289, 2026-11-15.
issue: no
---

**The mechanism.** For a file with no tags, main handed every matcher an
empty artist; the branch hands the artist its name reads to. Discogs and
Beatport gate every row on the artist, so an empty artist could never match
there and the split can only add matches. Traxsource and Bandcamp read a row
with no credit by its title alone, and the shared reader lays out a name's
title by the artist it is given, so the verdict on such a row moves both
ways.

**Measured cost.** At round one, a matcher level differential over 5192
names that split: 29820 uncredited row verdicts lost and 27352 gained, for
example row `Bernard Badie` no longer matching `08A - 124 - Bernard Badie -
Sunrise Mood`. No product path reaches either shop: `for_taxonomy` builds
the searcher over `WALK`, Discogs then Beatport, and only an explicit walk
names them. The suite's corpus differential runs with an artist tag only.

**Closes when:** either shop returns to the default walk, at which point the
split's effect on uncredited rows is measured and pinned. Ledger only.
