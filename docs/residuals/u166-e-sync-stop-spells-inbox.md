---
title: The sync land stop spells INBOX / Analyze as a constant, not the adopted intake root's name
found: at the second review of #347, U166, 2026-10-28.
issue: no
---

**The mechanism.** `sync_land.ANALYZE_PLAYLIST` is the literal
`INBOX / Analyze`, held by a test to the shipped taxonomy's intake folder.
The landing's own warning names the playlist under the adopted root's live
name, so a library whose intake folder is called something else would read
one name in the warning and another in the stop.

**Measured cost.** Not driven. Phillip's library uses the shipped name, and
no taxonomy with another intake display was produced.

**Closes when:** the stop reads the name from the landing's own answer or
the active taxonomy. Ledger only.
