---
title: Helper bodies identical as syntax trees escape the identical body reading when an annotation or a blank line differs
found: at review round one of #978, U329, 2026-11-23.
issue: no
---

**The mechanism.** U329's reading of an identical body (`tests/test_duplication.py`,
`identical_bodies`) keys a function on its arguments and its statements as
syntax trees, the rule the card and U298 named, so a parameter annotation
that differs makes two bodies distinct. Three pairs are identical statement
for statement with the arguments set aside: `_planned_over` in
`cli/label_sync.py` and `cli/sync_land.py` (`tail.Attend` against `_Attend`,
which `sync_land.py` binds to `tail.Attend`), `_as_left` in `adopt/apply.py`
and `identity_of` in `analysis/ahead.py`, and `declared_gate` in
`cli/output.py` and `_gate` in `cli/verbs/taxonomy_word.py`. The size is
physical lines per copy, so a two line body beside a twin wrapped to three
is not counted, and `_folder_and_path` in `analysis/cli.py` and
`vocals/cli.py` is an identical two line body today. Round two drove the
other side of that: the floor reads each copy's own blank lines, so the
accessor this card gave one home, copied into a new part with its blank line
deleted, passes 37 of 37 where the same copy with the blank line fails, and a
blank line added to both `_folder_and_path` copies turns the suite red with
no code changed.

**Measured cost.** None to a user, by the review's independent syntax tree
pass with the arguments ignored. The card's title, "no identical helper body
left", reads wider than its rule; the rule is what the guard holds.

**Closes when:** each pair is given one home, or the reading compares bodies
with the annotations dropped and the guard is tightened to it. Ledger only.
