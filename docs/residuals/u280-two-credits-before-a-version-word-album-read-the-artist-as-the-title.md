---
title: A name with two parts crediting the artist before a version word album reads the artist's part as the title, as on main
found: at the review of #791, U280, round one, 2026-11-13.
issue: no
---

**The mechanism.** R-1653 named "Tide & Artist - Artist", two parts both
crediting the artist, read both ways (`_title_stretches` in
`tagging/titles.py`, kept by R-1636's tests). U280's review drove it to a
wrong genre one rule over: `_layout` counts a part naming the artist only as
featured as a credit, so "08A - 124 - Sunrise Mood feat. Tide - Bernard
Badie - Summer Mix" tagged "Bernard Badie & Tide" takes the artist's part as a self
titled title, and the row "Bernard Badie" matches. The ambiguity test refuses
a featured only credit among several (`_only_a_list_reads`), but the layout
does not.

**Measured cost.** A wrong genre, driven through `_title_matches`, True on
main and on the branch alike; `tag_one` and the naming verb were not driven,
and a name of this shape needs an album after the artist's part.

**Closes when:** `_layout` reads a featured only credit as the title it
holds, measured by the differential, or R-1653 is decided. Ledger only.
