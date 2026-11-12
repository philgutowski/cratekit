---
title: A title written only inside another title's trailing brackets no longer finds it
found: at the build of #770, R-1631, 2026-11-12.
issue: no
---

**The mechanism.** R-1631 refuses a title whose words sit only inside the
other title's trailing brackets, because "How Does It Feel" against
"Untitled (How Does It Feel)" carries the same evidence as the wrong match
"Intro" against "Sunrise Mood (Intro)". `main` matched both through its
containment between whole titles. Telling them apart needs a list of version
and part words, and every word such a list lacks writes a wrong genre.
Pinned as a known cost by
`test_a_title_written_only_inside_the_rows_trailing_brackets_is_a_known_cost`.

**Measured cost.** A miss, never a wrong genre: the file gets no genre from
that row and the next source is asked. Not measured: how many files carry an
alternate title in brackets on the catalogue side only.

**Closes when:** Phillip answers the question on #770 (keep refusing, the
recommendation, or match an alternate title when the bracket holds no version
word). Ledger only: a miss with no wrong data.
