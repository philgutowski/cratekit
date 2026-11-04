---
title: A made pair's account playlist whose move into its folder failed stays at the account root
found: at the review of #483, U198, 2026-11-04.
issue: no
---

**The mechanism.** `pair_cli._made` reserves and marks the account playlist in the pairs document, then moves it into its root folder. When the move raises, the run fails with the pair already marked, and no later sync moves it, since only a sync that made the playlist moves it.

**Measured cost.** Driven by the review with `move_to_folder` patched to raise: the second sync is `ok` and the playlist sits at the account root for good. It still syncs both ways; it is in the wrong place, and `crate organize`'s filing may then read it as a root playlist. Nothing is lost.

**Closes when:** the pair records that its playlist was placed, and a sync moves any made pair not yet placed into its recorded folder. Ledger only.
