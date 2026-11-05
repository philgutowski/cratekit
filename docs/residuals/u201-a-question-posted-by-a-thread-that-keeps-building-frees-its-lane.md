---
title: A Question for Phillip posted by a thread that keeps building reads as waiting on the board, and frees that thread's lane
found: while building #489, U201, 2026-11-05.
issue: no
---

**The mechanism.** The project's rules have a thread post a question on its card
and keep building to the conservative call. `scripts/board.py cloud` reads a
`Question for Phillip` with no reply as `waiting-on-phillip`, whatever the
thread posts after it, so a card still held and being built is counted as no
lane's, and the coordinator may fill that lane while the thread is still
working.

**Measured cost.** Measured on #489: a `Progress` note posted after the question
left the card read `waiting-on-phillip`. No card was taken twice, since a
waiting card is not takeable; the lane count was short by one until the landing.

**Closes when:** `board.py cloud` reads a `Progress` note after a question from
the holding thread as underway, with a test.
