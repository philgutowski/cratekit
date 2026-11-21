---
title: The Auto Analysis path's wait can reach its count on rows outside INBOX / Analyze and end before the batch is analysed
found: at the review of #887, U319, 2026-11-21.
issue: no
---

**The mechanism.** Auto Analysis analyses every row rekordbox finds not
analysed, not only the batch, and the skill's wait counts every
`ANLZ0000.DAT` newer than the marker. Driven on a simulated store: seven
files for other rows and none for the batch print `done: 7 of 7`. The skill
says the count can pass `expected` and leans on step 7, whose check then
exits 12 and stops the visit, so nothing is cleared wrongly. A related
shape: a row with `Analysed` 1 and no analysis path judges as waiting and is
counted in `data.summary.not_analysed`, which Auto Analysis may leave alone,
so a wait on it stalls one short. One candidate producer driven, a native
landing, which writes `Analysed` 0 and does not produce it.

**Measured cost.** A visit that stops at waiting and is run again, not a
false report. Reachability on the live library unmeasured.

**Closes when:** `crate analyze check` can say before the launch how many
rows of the whole collection wait (its `unanalysed` scope is read today only
when INBOX / Analyze is empty), and the skill waits for that count. Ledger
only: no data is lost and no report is false.
