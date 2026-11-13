---
title: A name the shape or the credit rules do not recognise is still read one way, as on main
found: at the review of #788, R-1646, rounds one and two, 2026-11-13.
issue: no
---

**The mechanism.** R-1646 reads "Artist - X" by its splits only when
`_title_starts` recognises the shape: the first part after the head credits
the searched artist (`_names_the_artist`) and the next ends in a version word
(`_a_tail_to_shed`). Names it does not recognise are read as `main` reads
them:
- a trailing credit hides the version ending: "Bernard Badie - Vocal Mix
  feat. Tide" matches a row "Vocal";
- two artist parts make the title the head: "Bernard Badie - Tide - Sunrise
  Mood Extended Mix", tagged "Bernard Badie & Tide", matches the self titled
  row "Bernard Badie";
- a tag that does not name the first part as written, "DJ Bernard Badie" or
  "Badie", leaves "Bernard Badie feat. Tide - Sunrise Mood" read shed of its
  feature credit, so it matches the self titled row "Bernard Badie".

**Measured cost.** Driven through `_title_matches` on the branch and through
`tag_one` at round two: each writes the wrong genre on `main` and on the
branch alike. No producer of these names was driven; the naming verb writes
"Artist - Title" from the tags, so the third needs a tag that disagrees with
the name.

**Closes when:** the matcher reads a name's parts as typed fields with an
ambiguous outcome (U280, #791), or each
shape gets its own rule. Ledger only: no worse than `main`, and the redesign
card carries it.
