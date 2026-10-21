---
title: The U151 board read is unmeasured on the live board, for want of a token that can see the project
found: at the build of #332, U151, 2026-10-21.
issue: no
---

**The mechanism.** The session that built U151 held a token that reads the
repository but cannot resolve user project 2, so `project_context` refuses and
the live `board.py audit` and `board.py sync` the brief asks for were not run.
The membership query itself ran against the live repository, 324 issues for 2
points, but every membership came back empty to that token.

**Measured cost.** Not driven. The expected no drift sync is about 6 points of
reads and no writes, against roughly 850 before, and that figure is arithmetic,
not a reading.

**Closes when:** a session holding `BOARD_TOKEN` or Phillip's own `gh` login
runs `board.py audit`, then `board.py sync`, reading `rateLimit { remaining }`
before and after, and the audit agrees with the old script's on the same board.
Ledger only.
