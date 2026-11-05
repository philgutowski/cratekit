---
title: board.py cloud reads a card the grok builder holds as ready, since that builder's comments carry no session footer
found: at the review of #536, U218, 2026-11-05.
issue: no
---

**The mechanism.** `cloud_state` in `scripts/board.py` reads only comments
that carry the Claude Code session footer as a hold. The `grok/` builder's
comments carry none (its comments on #309 and #310 of 2026-10-13), so a card
it holds reads `ready, no cloud session has taken it`, and `board.py cloud`
prints no branch names. Driven at review on comments shaped like #310's.

**Measured cost.** No card pays today: the two `grok/` branches on the remote
belong to #309 and #310, both closed. A grok held card offered to a build
thread would put two builders on one card. The same reader takes a comment
of that builder's posted after a cloud thread's `Brainstorm` or `Question for
Phillip` as Phillip's reply (driven at review on a synthetic pair: `answered,
Phillip replied`), so a thread could fold another builder's words into a
brief as his answer; no open card carries that input today. The cloud-unit skill now tells a
thread to look for a `grok/` branch naming the card and that builder's
comment before it posts `Started`.

**Closes when:** `board.py cloud` reads a `grok/` branch or that builder's
comment as a hold, with a test. Ledger only: maintainer facing, and
`board.py` was out of U218's scope.
