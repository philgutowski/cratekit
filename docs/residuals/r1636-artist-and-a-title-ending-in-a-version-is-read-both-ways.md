---
title: A name crediting the artist before a part ending in a version is read both ways, so a self titled row or a version word row can still write its genre
found: at the review of #781, R-1636, rounds one and two, 2026-11-12.
issue: yes
---

**The mechanism.** Since R-1636 the file's title in `tagging/searchers.py`
(`_title_starts`) starts at the first part after the head that does not
credit the searched artist, and no later part is read alone. One shape is left
that only a list of version words could tell apart: a part crediting the
artist followed by a part ending in a version word. "08A - 124 - Aurora Bloom
- Vocal Mix" is a title "Vocal Mix" by Aurora Bloom, or a self titled track
"Aurora Bloom" and its version; "Aurora Bloom - Sunrise Mood Extended Mix" is
the same shape. Round one of the review drove reading only the second part to
a self titled track losing its own row on page order, so the shape is read
both ways (the artist's part up to that tail, and the tail), as `main` read
it. So the tail is still read as a title where "vocal" is not in
`VERSION_WORDS` (a row "Vocal" writes its genre), and the artist's part is
read where the title merely ends in a version (a self titled row "Aurora
Bloom" writes its genre onto "Aurora Bloom - Sunrise Mood Extended Mix").
Read the same way: "Artist - Artist & Tide", two parts that both credit the
artist, reads the first as a self titled title.

**Measured cost.** Driven through `tag.tag_one` at round one: "08A - 124 -
Bernard Badie - Vocal Mix" took a Beatport "Vocal" row's and a Discogs "Vocal
Mix" track's genre, on `main` and on the branch alike; the file's own row
listed first wins, as on `main`. Not worse than `main` on any input driven,
and narrower: the artist's part is read only before a part that itself ends in
a version (round two). Not measured: how many files carry a title or a name of
this shape.

**Closes when:** the shape is told apart without a list that fails open, or
Phillip decides which reading wins. A wrong genre written onto a file is the
board bar's damaged data.
