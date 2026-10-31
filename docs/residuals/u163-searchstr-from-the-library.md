---
title: A minted lookup row's SearchStr follows the library's majority, not a measured rekordbox rule
found: at the build of #344, U163, 2026-10-31.
issue: no
---

**The mechanism.** `native.search_convention` counts what the library's artist
and album rows store in `SearchStr` (their name, the empty string, or NULL) and
a mint follows the majority, NULL on a tie. What rekordbox's own Reload Tags
stores there was never read off a copy, so the library is the nearest witness,
and the screen shows the value per mint.

**Measured cost.** None driven. rekordbox may search a minted artist or album
differently from one it made if its rule differs from the library's majority.

**Closes when:** an attended landing reads what rekordbox stores on a row it
made by Reload Tags beside a minted one, and the rule is set from that. Ledger
only.
