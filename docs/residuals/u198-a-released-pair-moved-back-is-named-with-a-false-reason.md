---
title: A made pair released by a move under ARCHIVE and moved back is named as a title no pair made
found: at the review of #483, U198, 2026-11-04.
issue: no
---

**The mechanism.** A made pair whose rekordbox playlist moves under a skipped folder is released, and its account playlist stays in its root folder. Moved back out, the rekordbox playlist is found again, and `pair_cli._discovered` meets the account playlist of its title, which no pair now holds, so it lists the rekordbox playlist as taken by "a playlist ... that no pair made for this one".

**Measured cost.** Driven by the review's second round. Wording only: nothing is written, and the steps given, to pair the two by hand, work.

**Closes when:** `_discovered` reads the released account playlists and says the pair was released when it moved, or pairs the two again. Ledger only.
