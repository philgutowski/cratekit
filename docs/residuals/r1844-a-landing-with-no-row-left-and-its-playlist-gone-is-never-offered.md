---
title: A landing whose every row is gone and whose playlist was deleted by hand is read as rolled back, so its removals are never offered
found: at the review of #926, R-1844, round one, 2026-11-22.
issue: no
---

**The mechanism.** `deletion.library.landed_absences` reads a landing as standing
when the database holds one of its rows, live or marked, under the UUID the
landing recorded, or every playlist it made. When Phillip deletes the
landing's playlist in rekordbox (deleted outright, A200) and every row of the
landing is also gone, neither fact is left, and the landing reads as rolled
back. That happens in three ways: a landing of one track, the most common case
for A129; a batch cleared to its last track; or siblings taken out by `crate
sync removed`, whose recorded removals prove nothing, since a rollback to
before both leaves the record. A removal already offered on a sibling's proof
is withdrawn once the last sibling goes. A landing into a batch playlist that
was already there (R-1843) behaves the same way when it has a single row.

**Measured cost.** Driven on disposable libraries in
`tests/test_delete_landed_removed.py`: offered 0, the files kept, and the gate
showing `landings read as rolled back: 1` while one of the landing's absent
rows has never been numbered. Nothing goes to the Trash wrongly. Phillip
trashes such files himself.

**Closes when:** a fact no database from before the landing holds, and that a
playlist deletion and a removal both leave, is found for a landing with no row
left (a playlist folder the landing made, a lookup row only it made and
rekordbox does not prune, or another one measured at an attended sitting), and
`landed_absences` reads it. Ledger only: the cost is a kept file, and it is
counted on the gate.
