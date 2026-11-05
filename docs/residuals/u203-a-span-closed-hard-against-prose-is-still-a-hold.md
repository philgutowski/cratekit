---
title: A bold heading closed hard against the next word, with no space, is still a hold and then a resume
found: at the Fable review of #493, U203, 2026-11-05.
issue: no
---

**The mechanism.** `_OPENING_EMPHASIS` in `scripts/board.py` takes an opening
span only when its closer is followed by the line's end, whitespace or
punctuation, so `**Brainstorms**` stays a word the reader does not know. The
same rule leaves `**Brainstorm.**One question waits` and
`**Question for Phillip.**One of A or B` unread: they give
`brainstorm.**one question waits`, a hold, then a resume after `STALE_HOURS`,
under the old reader and the new one alike.

**Measured cost.** A question card retaken before Phillip answers, the cost
U203 was filed for, driven through `cloud_state` by the review. The producer
was not driven: none of the 1,126 comments on the repository on 2026-11-05
opens this way. Not a regression, and inside the brief's stated contract.

**Closes when:** a closer followed by a capital letter after a stop inside the
span is also read as a span, with a test that `**Brainstorm**s` stays unknown.
Ledger only: maintainer facing.
