---
title: A variable row the landing could not tag dyn is counted among the rows the visit runs Normal, while another warning sends it to Dynamic by name
found: at the review of #997, U954, 2026-11-23.
issue: no
---

**The mechanism.** When a landing cannot give a variable row the `dyn` My
Tag (no My Tag category to copy, a removed value, a tag that does not read
back), `dyn-not-written` names it for a Dynamic run by name, before any
Normal run and left out of it. The `rows-await-analysis` warning counts rows
by the tag alone, so it counts that row among "the rows without it" for the
Normal run, and the skill's status line check and wait (the batch less the
`dyn` count) are off by the rows named. With every row such a row, the
awaiting warning tells of a Normal run on rows the other warning says to
leave out.

**Measured cost.** Driven at the review through the landing fixtures, a
library with no My Tag category and a removed `dyn` value; both states are
made by a person in rekordbox and were seeded here, so reachability on the
live library, which carries the category, is unmeasured. The cost is a count
that disagrees by the named rows, and the visit's mode left on Dynamic.

**Closes when:** the awaiting warning counts a variable row the landing could
not tag with the Dynamic rows (or names it apart), and the skill's counts
follow. Ledger only.
