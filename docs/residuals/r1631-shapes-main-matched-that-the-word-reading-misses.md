---
title: Shapes the containment matcher found that the word reading misses
found: at the build and review of #770, R-1631, 2026-11-12.
issue: no
---

**The mechanism.** R-1631 replaced containment with readings of whole words
in `tagging/searchers.py`. Each shape below matched its own row on `main` by
containment and misses now, because nothing in the title tells it from a
wrong match without a list or the artist:
- An unpadded or two digit track number opening a file's name, "12 Sunrise
  Mood", "1 Sunrise Mood", "A1 Sunrise Mood", "1-03 Sunrise Mood"
  (`_TRACK_NUMBER` is zero padded only, so "22 Bullets" is never "Bullets").
- A dash with no spaces, "Aurora Bloom-Sunrise Mood", and a name "Sunrise
  Mood - Aurora Bloom" with no head.
- A tempo with no key after the title, "Sun Path - 124".
- A title that is a Camelot code behind a head, "08A - 124 - 8A" (Beatport's
  top tier still finds it).
- A dash version with a number after it, "Sunrise Mood - Dub 2", "- Mix 1".
- A credit written with "with", "Sunrise Mood with Someone", since "Stay With
  Me" is not "Stay".
- An unbracketed remixer, "Sunrise Mood Kerri Chandler Remix" against plain
  "Sunrise Mood"; a catalogue dash tail the list lacks, "Sunrise Mood -
  Vocal", "- Live At Fabric", "- Tom Rmx"; "Sunrise Mood / Tide".
- An untagged name "Artist - Interlude" against "Interlude", since a tail of
  version words after a title is refused.
- A Discogs single whose release title adds "EP" to the track's, on the
  single fallback only.

**Measured cost.** Misses, never a wrong genre: the next source is asked and
the file stays askable. Found by the review grid and the build's
differential; the untagged shapes need a file with no title tag, whose
producer was not driven.

**Closes when:** a shape is shown common in a real library, and is then read
by a rule that cannot also match another recording. Ledger only.
