---
title: A Discogs release's artist is compared with no fold at all, so a file tagged with an artist's plain spelling misses every release crediting the accented one
found: at the build of #919, U324, 2026-11-21.
issue: no
---

**The mechanism.** `searchers._artist_matches`, which decides whether a
Discogs release or track is credited to the file's artist, compares the
credits after `titles.normalized` alone (NFC, lower case, trimmed), so
neither an accent nor a letter U324's fold spells plain is read past:
`_artist_matches("Ame", "Âme")`, `("Royksopp", "Röyksopp")` and
`("Trentemoller", "Trentemøller")` are each False. U324 made a maker and a
credit inside a title one name across those spellings
(`titles._folded`), but the artist the release is credited to is a separate
reader and is unchanged, as the card's scope (the version check) asked.

**Measured cost.** Not driven on a live sweep. A file whose artist tag is
written plain, "Royksopp", takes no Discogs release credited "Röyksopp",
whatever its tracks, and goes on to Beatport; sitting 102's file is tagged
with the accented spelling Discogs writes, so it is not affected.

**Closes when:** the release artist check reads each credit through the
same name fold (`titles._folded` word by word, or a public reader of it),
held by a differential over the Discogs fixtures that no release credited
to another artist newly matches. Ledger only: a miss, never a wrong genre.
