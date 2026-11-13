---
title: A name crediting the artist before a part ending in a version finds only a row that writes the same split, so the file's own row under another mix or with no version is a miss
found: at the build of #788, R-1646, and its review round one, 2026-11-12.
issue: no
---

**The mechanism.** Since R-1646 a file's title "[KEY - BPM -] Artist - X",
X ending in a version word, is read in `tagging/searchers.py` by its whole
name and its two splits into a title and a version (`_name_splits`), and a
catalogue row matches it only by writing one of those splits itself
(`_row_splits`, `_beatport_readings`). So these, all found on `main`, are now
a miss:
- "Bernard Badie - Vocal Mix" against its own self titled row listed as
  "Bernard Badie" under another mix or with none;
- "Bernard Badie - Sunrise Mood Extended Mix" against a plain "Sunrise Mood"
  row, or one under another mix, on every source but Beatport's mix field;
  "08A - 124 - Bernard Badie - Sunrise Mood Original Mix" against a Discogs
  "Sunrise Mood" track (review round one);
- either side carrying one more bracket group than the other, "Sunrise Mood
  (Extended Mix) [Remastered]";
- "Bernard Badie - 01 Vocal Mix" against "Bernard Badie (Vocal Mix)", and a
  Beatport name "Sunrise Mood (feat. Tide)" with mix "Extended Mix";
- a Discogs single titled "Bernard Badie" whose tracks are named by their
  versions, "Vocal Mix", "Dub".
Each was found on `main` by the same both ways reading that also wrote a
"Vocal" row's or a self titled row's genre. The card's brief asked for the
first to be found and the self titled row of the second refused, which no
rule but a list of version words tells apart.

**Measured cost.** A miss, never a wrong genre: no catalogue genre is
written and the file is left for another source or hand tagging. The
author's differential of `main` against the branch over 2,336 suite titles,
16 name shapes and 4 artists lost 206,448 of 410 million pairs, most in the
card's shape and most of those in the differential's own synthetic shapes
("Artist - Title Extended Mix"); Beatport's scorer over 2.67 million sampled
pairs lost 7,800, all in the shape. Not measured: how many files in a real
library are named this way.

**Closes when:** Phillip answers the Question for Phillip on #788 (option 1,
this behaviour, recommended); a Discogs single's release title beside its
version named tracks could confirm the self titled split without a list.
Ledger only: a miss loses no data and says nothing false.
