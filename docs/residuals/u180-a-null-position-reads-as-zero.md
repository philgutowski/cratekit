---
title: A Favorites playlist with no position reads as position 0, and the order can hand 0 out as a live position
found: at the review of #361, U180, 2026-11-01.
issue: no
---

**The mechanism.** `placement.seq_of` reads a row's `Seq` as `int(Seq or 0)`,
so a playlist under the Favorites folder whose `Seq` is NULL sorts first and
contributes 0 to the slots `placement.slots` gives out. `crate favorites order`
then writes 0 as a live row's position, which the binding's own
`create_playlist` and `move_playlist` refuse as below 1.

**Measured cost.** Driven on a disposable copy with `Seq` set to NULL by SQL:
the verb wrote All Favorites at `Seq 0` and the folder read in the right order
on the copy. What rekordbox shows for a position of 0 was not measured, and one
candidate producer was driven (SQL); no verb and no known rekordbox path writes
a NULL position.

**Closes when:** the slots are floored at 1, or an attended sitting reads a
`Seq 0` row in rekordbox and finds it shown where its neighbours say. Ledger
only.
