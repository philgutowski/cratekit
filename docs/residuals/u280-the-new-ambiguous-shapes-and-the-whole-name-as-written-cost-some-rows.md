---
title: The shapes U280 made ambiguous, and the whole name read as written, cost a file some rows main found
found: at the build and review of #791, U280, 2026-11-13.
issue: no
---

**The mechanism.** U280's deliberate changes in `tagging/titles.py` each
refuse some rows main matched, by design:
- the R-1651 shapes now ambiguous, "Artist - Vocal Mix feat. Tide" and
  "Artist - Tide - Sunrise Mood Extended Mix" by "Artist & Tide", match only
  a row writing the same split or the whole name, as R-1646's shape does:
  the file's own row under another mix or with no version is a miss (R-1652's
  cost, wider);
- an ambiguous name whose first part names the artist only as featured,
  "Tide feat. Artist - Vocal Mix", no longer finds a plain "Tide" row, which
  main found by shedding the feature credit across the dash;
- a key read as a title, "8A - Original Mix" against "8A", and a track
  number, "01 - feat" against "01";
- a last part of brackets alone that is no version, a row or a file "Sunrise
  Mood - (Vocal)" or "Sunrise Mood - (Bonus Track)", no longer reads as
  "Sunrise Mood", since a bracket group is shed only from the part carrying
  it (review round two's row 3).

**Measured cost.** Misses, never a wrong genre. The differential against
main (`scripts/title_differential.py`, about 400,000 names of the suite's
corpus in 22 shapes) lost 2,280 pairs to the ambiguous shapes (414 outside
corpus fragments) and 16,091 to the whole name and the bracket rule (1,818
outside fragments), most of them wrong matches main made (a head's words,
"(Intro) - Original Mix" taking an "Original Mix" row, "Artist - (Intro)"
the self titled row). Not measured: how many files or catalogue rows are
written so.

**Closes when:** a catalogue is shown to write "Title - (X)" for a version
of no version word, or Phillip asks for the own row under another mix
(#788's question). Ledger only.
