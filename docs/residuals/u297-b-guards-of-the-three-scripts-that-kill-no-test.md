---
title: Guards in killset.py, behaviour_compare.py and the stage that kill no test when reverted alone, as the two reviews of U297 left them
found: at the review of #854, U297, rounds one and two, 2026-11-21.
issue: no
---

**The mechanism.** The reviewer reverted 56 guards at round one and 60 fix
round guards at round two, one at a time in a copy of the tree, and ran each
one's test file. 22 and 12 killed nothing. The two fix rounds gave a test to
the ones with a named cost. These stayed at zero, each a line the suite does
not notice when it is reverted alone:

- `scripts/killset.py`: the `isinstance(..., bool)` half of `killed`; the
  suffix filter and the skipped directories in `Tree.holders`; the reading of
  a before table's `head` only when it is a string; the `^{commit}` peel that
  tells a commit from another object in `Commit._read`.
- `scripts/mutate.py`: that the line `main` prints when a resume reuses
  nothing is printed for a replay alone.
- `scripts/behaviour_compare.py`: that only a table's declaration is put in
  one order (an index's or a trigger's with two parenthesised items is
  returned as written, and no test hands it one); the `UnicodeDecodeError`
  arm in `dump_databases`; the longest word first order in `same_but_for`,
  which matters only when one word of a capture is the prefix of another.
- `tests/behaviour/`: the check against the system's temporary directory
  inside `refuse_a_root_outside`, which the check against the scenario's own
  directory covers; the stage fixture's refusal at set up, which the refusal
  before each command covers; the reseeding of the shared `random` generator
  and its restoring.

**Measured cost.** None to a person using the shipped verbs: all three are
maintainer tools, and each guard was seen to work when driven by hand. The
cost is that a later edit can remove one of them with the suite green. The
card's own mutation table, `docs/mutation/u297.md`, measures 25 other rows.

**Closes when:** each has a test that fails with it reverted, or is shown
equivalent and removed. Ledger only.
