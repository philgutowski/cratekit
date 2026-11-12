---
title: A name crediting the artist in a way the matcher does not read loses the title after it
found: at the build and review of #781, R-1636, 2026-11-12.
issue: no
---

**The mechanism.** R-1636 reads a file's title from the first dash part after
the head that does not credit the searched artist (`_names_the_artist` in
`tagging/searchers.py`): one of the names the part joins on "&", ",", "/",
";", "+", "x", "vs", "pres" or a feature word must be one of the artist's
names, accents folded and "The" aside, or the part of two words or more a run
of a name with initials. Where the name credits the artist otherwise, the
first part is read as the title and the title after it is not, so each shape
below misses its own row, where `main`, which read every dash part, found it:
- One word of the artist's name, "Badie - Sun Path" for "Bernard Badie", kept
  a title on purpose, since "Badie" is as likely a title.
- A collaboration joined by "and" or "with", "Bernard Badie and Tide - Sun
  Path": both words are in titles, and reading them as joins took "Dancing
  With Bernard Badie" for a credit at round two.
- A file with no artist tag at all, "Bernard Badie - Sun Path".
- A track number glued to the artist after the first part, "Title - 01
  Bernard Badie - Album", which no name writes.
- A title of a number before a name with no key, "1998 - Sun Path"
  (round one's R2; the naming verb never leads with a number).

**Measured cost.** Misses, never a wrong genre: the next source is asked and
the file stays askable. The file with no artist tag is unreachable on the
default walk, `searchers.WALK`, Beatport then Discogs, which both refuse a
file with no artist. The others were found by the build's differential and the
review's drivers; how many files carry such a name was not measured.

**Closes when:** a shape is shown common in a real library, and is then read
by a rule that cannot also take a title for the artist's credit. Ledger only.
