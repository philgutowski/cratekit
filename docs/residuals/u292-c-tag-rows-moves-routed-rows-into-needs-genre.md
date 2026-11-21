---
title: tag rows writes a genre word no folder takes over a routed row, moving it into needs genre, and the backlog campaign runs it first
found: at the review of #849, U292, 2026-11-21.
issue: no
---

**The mechanism.** `tag rows` reads every disagreement as the row lagging its file (`tagging/rows.py`). A row adoption files today, say Melodic House, whose file carries a word no folder takes, say Indie Tech, is written that word, and adoption then files it nowhere. Round one drove two such rows: the backlog projected 0 left after the campaign and the census read 2. The backlog now counts them (`Backlog.joining`), adds them back into its projection and warns `backlog-rows-joining`, naming them; it writes nothing itself.

**Measured cost.** Running the printed campaign moves the named rows into needs genre unless each is held out with `tag rows --leave`. The backlog names them before the step runs.

**Closes when:** U294 (#851) holds every joining row out of its `tag rows` step, or `tag rows` stops writing a word adoption files nowhere over one it files. Ledger only.
