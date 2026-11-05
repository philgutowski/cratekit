---
title: A made account playlist moved out of its folder between a stop and its continue is moved back
found: at the review of #500, U210, 2026-11-05.
issue: no
---

**The mechanism.** A ceiling stop between making a discovered playlist's
account side and putting it in its folder leaves it at the account root. The
continue (`_made` with `resumed`, `sync/pair_cli.py`) moves it into the folder
the plan named, since the move asks for one fixed place, and does not read
where the playlist is now. A playlist the author moved elsewhere in that
window, into Archive say, is moved back.

**Measured cost.** Driven at round one (S2): the continue moved it back and
answered OK. The playlist is empty in that window (it is filled after the
move), nothing is lost, and moving it again lets the archive rule release it.

**Closes when:** the continue reads the made playlist's folder first and
refuses stale when it sits in a folder other than the root or its own. Ledger
only.
