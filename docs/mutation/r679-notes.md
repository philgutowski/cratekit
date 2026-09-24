# R-679 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/197` at `5ba0da3`, in the foreground under the
Relay session's rule. Every row's subset was the three files that drive the
review store for this unit, `tests/test_review_queue.py`,
`tests/test_match_states.py` and `tests/intake/test_workers.py`, 626 tests.
Null control 0 of 10090 on both, no collect drift, every restore verified
against `git show HEAD`.

**`r679-a.md`**, 10 rows over `core/review.py` and `cli/review.py`: the
third verdict's writer, its guard, the person's vocabulary, the import route
and the listing. 9 killed, 1 zero.

**`r679-b.md`**, 12 rows over `acquire/match_cli.py`, `acquire/match.py` and
three of the four call sites regated in the fix round. 11 killed, 1 zero with
its composite killing.

22 rows in all, 21 distinct mutations and one composite, under the cap of 25.
Three more were considered and logged as dropped in the rows files: the read
back stamp (A9), which only a race could observe, and the label sweep and
whole list missing gates (D3, D4), the same shape as D2 and held by the same
structural guard.

## The two zeros

- **A2, the read layer of `supersede` alone.** Maintainer facing, one line:
  the read is the efficiency, deciding whether to take a write lock at all,
  and the write's own `verdict IS NULL` is the guard. A1 removes both and
  kills 5; A3 widens both to the reader's predicate and kills 1, the
  unreadable newer verdict test.
- **B4, reading any verdict as an answer, under the reopen layer.** User
  facing, so it carries a composite: B4c removes the reopen and the person's
  vocabulary check together and kills 1, the reopen test, which then reads
  the machine's verdict as a rejection. B3 alone, the reopen removed, kills 1.
  So the two layers are each held and the second is the belt under the first.

## What the kills say

The retirement is held from six directions: never retiring (B1, 6 kills),
retiring under any matched why (B2, 1), the rule not recorded (B5, 4), one
shape only (B6, 6), the credited rule left out (C1, 2) and the reading shape
left out (C2, 1). The writer's guard is held whole (A1, 5) and against the
reader's wider predicate (A3, 1). The one writer rule is held at `resolve`
(A4, 1), at the import (A5, 2), at the empty rule (A6, 2) and at the person's
vocabulary (A7, 2), and the command line's choices (E1, 1). The actor being
the rule is the most tested line in the unit (A8, 10 kills). The three
regated call sites each kill (D1 2, D2 1, D5 1), D5 through the count guard
alone, which is the guard that exists because the missing pass calls twice.
