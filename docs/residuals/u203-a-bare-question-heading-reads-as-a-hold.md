---
title: A bare Question heading on a card reads as a hold, then a resume, while it waits on Phillip
found: at the plan of #493, U203, 2026-11-05.
issue: no
---

**The mechanism.** `scripts/board.py` knows the question heading only as
`Question for Phillip` (`HEAD_QUESTION`). The Sharing the board section of
`docs/METHOD.md`, on the branch that carries it, and the coordinator's prompt
to its build threads both tell a thread to ask "under a `Brainstorm` or
`Question` heading". A thread that writes `**Question**` or `## Question.`
leaves a heading the reader does not know, so `cloud_state` reads the card as
underway, then after `STALE_HOURS` as resume, and the next thread may retake
it before Phillip answers. It is the shape U203 fixed for punctuation, in
spelling, which U203's brief put out of scope.

**Measured cost.** Not driven on the live board: of the 1,126 comments on the
repository on 2026-11-05, no session comment opens with a bare `Question`
heading, so no card has paid for it yet. Reading `comment_heading("**Question.**")`
returns `question`, which no constant matches; pinned as unknown by
`test_a_heading_whose_words_differ_is_still_a_hold`.

**Closes when:** either the two texts say `Question for Phillip`, or the reader
takes `question` as a second spelling of `HEAD_QUESTION` with a test beside the
U203 ones. Ledger only: maintainer facing, the board bar's four costs are a DJ's.
