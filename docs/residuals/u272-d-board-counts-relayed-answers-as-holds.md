---
title: board.py cloud counts a card with a freshly relayed answer as a hold, so its lane alarm fires with lanes free
found: at the start of #701, U272, 2026-11-13.
issue: no
---

**The mechanism.** At 15:59 on 2026-11-13 the orchestrator relayed Phillip's
answers onto #700, #702 and #707 within a minute. `board.py cloud` listed each
as `underway` with "phillip's answer" and counted it toward the five lanes, so
with four sessions holding cards it printed "MORE CARDS ARE HELD THAN THERE
ARE LANES (7 for 5)" and told every later holder, this card's thread among
them, to withdraw. The skill's Orient step tells a thread to obey that line.

**Measured cost.** None here: the coordinator assigned the card and counts
lanes by its own threads, as METHOD says, so the thread built it. A thread
that followed the skill to the letter would have withdrawn a card it was
assigned, and the lane would have sat empty until the next hourly fill.

**Closes when:** the lane count leaves out a card whose latest comment is a
relayed answer with no hold after it, or the skill says the coordinator's
assignment wins over the alarm. Ledger only.
