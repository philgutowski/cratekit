---
title: The test that a catalogue row's dash tail is a version before it splits the row kills nothing
found: at the mutation table of #788, R-1646, 2026-11-13.
issue: no
---

**The mechanism.** `_row_splits` in `tagging/searchers.py` splits a row
before a dash tail only when the tail reads as a version
(`_a_tail_to_shed`). With the test removed (row M15 of
`docs/mutation/r1646.md`) no test fails. Round one of the review argued it,
and three more of the diff's guards (`_identifies(mix)` in
`_beatport_readings`, the `<` in `_row_splits`, `head in artists` in the
shape), equivalent: a file split's version is never empty and always ends in
a version word.

**Measured cost.** None found. Six candidates were driven against the branch
and the mutant ("Kerri Chandler (Remix 2014)" against "Kerri Chandler Remix
(2014)", "Vocal - Mix", "Sunrise - Mood Extended Mix" and three more) and none
tells them apart: a tail whose words equal a file split's version ends in a
version word itself, or the unshed whole name meets it first. `head in
artists` has a composite (`docs/mutation/r1646-composite.md`).

**Closes when:** the guard is removed or a case it decides is found and
pinned. Ledger only, a maintainer facing guard.
