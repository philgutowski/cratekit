---
title: Guards of U201's account edit rule and its short listing fix that no test reaches
found: at the review of #489, U201, rounds one and two and the mutation table, 2026-11-05.
issue: no
---

**The mechanism.** Each guard below was reverted alone with the suite green.
From the reviews: `PlaylistPlan.unlisted` (a short listing keeps its snapshot's
word on what it did not list; the round two drive S14 kills it), `settled`
recording a short playlist with nothing to write (drive S2 kills it),
`Decision.settle` leaving short playlists out (one extra agreed line after a
move into a short playlist, run 3 of S2), `_later` with two rekordbox places,
a failed listing read as short in `_read_edits`, holds handed only to genre
folders, memberships outside the tree in the step's plan, and two dead
conditions in the round one fix (`gone` in `unlisted`, `not now` in the own
genre held branch). The mutation table, `docs/mutation/u201.md`, adds its own
zero rows: E2 (masked by the still in two bands guard, the composite C1 kills
both), E5 (the composite C2 kills what it narrows), M3 and M4 (the short
listing's settled snapshot), L2 (settle never mints a snapshot; C4 kills what
it narrows) and O4 (a move leaves only routing's playlists; C5 kills what it
narrows). The composite C3 was zero too and is now pinned by a test added
after the table, measured by hand.

**Measured cost.** None on the merged head: every guard was driven working by
the reviewers. A later change that removed one would stay green.

**Closes when:** a test drives each, the reviewers' S14 and S2 sequences first.
