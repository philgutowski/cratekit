---
title: A stopped order whose last move's landing is not known, and which never landed, holds its pair until the playlist is moved by hand or the pair is released
found: at the build of #604, R-1394, 2026-11-07.
issue: no
---

**The mechanism.** Since R-1394 a pending order records, before each move,
how many moves may have reached the provider (`sent`) and how many it
accepted (`landed`). When a move fails any way but its last 412 (a dropped
connection, a timeout, a crash, a record that could not be written after it
was accepted), its landing is not known, so `_pending` in `sync/pair_cli.py`
holds an agreed reading at `landed` moves rather than finish from it: that
reading may be the provider lagging the move. If the move in fact never
landed, the provider serves that order for good and the pair is held every
run, `sync-pair-account-settling`, until the DJ moves the playlist off the
moves' way in the provider's player or releases the pair.

**Measured cost.** Driven on the fakes by
`test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`:
held across three runs with nothing sent. How often a live move fails with
its landing unknown was not measured. Built with the recommended answer to
the Question for Phillip on the card (hold, never scramble); his other two
options were to finish after the five minute agreement, or after a longer
window.

**Closes when:** Phillip answers the question on #604, or the attended
measure of the provider's lag (A88, A91) sizes a window after which an
agreed reading at `landed` is the truth. Ledger only: the DJ has a named way
out and nothing is damaged.
