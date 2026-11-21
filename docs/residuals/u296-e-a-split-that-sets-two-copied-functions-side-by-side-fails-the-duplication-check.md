---
title: A copied block is read across function boundaries, so a split that sets two functions side by side can fail the duplication check for lines nobody copied
found: at the review of #853, U296, round one, 2026-11-21.
issue: no
---

**The mechanism.** A logical line belongs to its file and not to its function,
so a window of six can span the end of one function and the start of the
next. Two functions that each stand in several files, apart, are no copy
until an edit sets them one after the other: then the window across their
boundary stands wherever another file already has them in that order. A plain
split does this. So does a deletion between two stretches of lines, which is
the limit of "removing a copy only shrinks what is found" and is now said in
the suite, the script and the docs. Two overlapping windows in one file are
also two places, as in the survey's instrument, so seven identical statements
in a row read as a copy.

**Measured cost.** The review moved `produced` and `committed` from
`analysis/artifacts.py` into a new module, side by side as
`adopt/artifacts.py`, `modules/outbound/artifacts.py` and
`tagging/artifacts.py` already hold them, and the check failed naming two
windows in `analysis`. The remedy the rule allows is to keep the order the
lines had or to give them one home, which for that family is three other
packages' files. Reach on the tree: 23 of 219,748 ordered pairs of functions
in 8 files would form such a window if set side by side; of 7,733 single
deletions tried in memory (143 blocks and 7,590 functions) none forms one;
and none of the 190 repeated windows today is two overlapping places.
Maintainer facing: an area card meets it during a split and reorders.

**Closes when:** U298 has given the helper families one home, which removes
the pairs, or the final audit of U290 finds the allowances empty. Ledger only.
