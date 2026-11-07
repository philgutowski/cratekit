---
title: A Tidal reorder made after a stopped order and before two syncs five minutes apart read the playlist is put back to rekordbox's order
found: at the build of #623, U234, 2026-11-07.
issue: no
---

**The mechanism.** `_moved_since_stop` in `sync/pair_cli.py` reads an
account off the stopped write's path as the person's only once a reading
kept on the pair after the stop has settled (read again in the same order at
least `AGREE_AFTER` later) and a later order differing from it has settled
too. A move the DJ makes on Tidal before the first reading settles, or the
first sync after the stop that applies its gates, cannot be told from the
provider's partial state or from Tidal still serving an older order, so that
sync finishes the stopped order from rekordbox's side and puts the move back.
A hand pairing has no record to keep a reading on, so nothing it reads leads.

**Measured cost.** Driven by the card's own tests: the move is put back, the
gate line naming the account as read where none of the stopped write's moves
leaves it, so the DJ sees it before approving and can skip the account gate.
This is the card's conservative call, which a P1 card about a scrambled set
asked for; how often a DJ reorders a stopped playlist on Tidal before the
next sync is not measured.

**Closes when:** Phillip decides a reorder should be read from something
else, such as the provider's own modification time for the playlist. Ledger
only.
