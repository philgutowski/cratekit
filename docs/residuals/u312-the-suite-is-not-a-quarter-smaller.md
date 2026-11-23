---
title: The suite ends 4.4 percent smaller, not a quarter, because what is left of it is not restatement
found: at the build of #869, U312, 2026-11-23.
issue: no
---

**The mechanism.** U290's survey set `tests/` at most 249,132 lines, a quarter
under 332,177. The thirteen area cards brought it to 300,722; U312 then cut
nine disjoint slices by the card's own rules (prose to rule and reason, near
identical tests folded into tables with every case kept, repeated setup
shared, slow setup built once, nothing reformatted to win lines) and ended at
about 287,400. Every slice measured why it stopped: test docstrings were
already one line, near duplicate scans (same tree but constants, then names
normalized) found a few dozen lines of foldable tests per slice, and the
helper copies across files were short. The support files reached 20,045
lines against the card's 17,650.

**Measured cost.** None to a person using the verbs. Point 5 of #847's
definition of done stays open on lines, and #872's audit reads the miss.
Reaching the bar would mean deleting tests: 4,728 tests of 51,458 lines on
`1fab8cbd` are named by no recorded kill, and they guard behaviour the
mutation tables never sampled.

**Closes when:** Phillip answers the question on #869 (land with the miss
named, delete unrecorded tests, or lower the bar), or a later card folds the
suite further by a means this card's rules did not allow.
