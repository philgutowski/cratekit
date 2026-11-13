---
title: A Cyanite trial killed between asking for a library track and reading the answer loses the track, and its resume pays for it again
found: at the review of #674, U245, round two, 2026-11-13.
issue: no
---

**The mechanism.** `tagging/cyanite.py` writes a file's row, with the
library track Cyanite made, the moment the create's answer is read
(`CyaniteAsker.on_made`), ahead of the analysis wait, so a run ended by an
error, an interrupt or a signal during the wait keeps the track and a
`--resume` asks about it without uploading. A run ended after the create was
sent and before its answer was read has no track id to write: Cyanite has
made the track, the table has no row, and the resume uploads the file again.

**Measured cost.** Driven by the round two reviewer with a recorded seam
raising KeyboardInterrupt after Cyanite registered the track and before its
reply: the resume uploaded the file again. The window is one round trip wide,
so how often a person meets it is unmeasured. The cost is one track paid for
twice.

**Closes when:** a resume looks the file up in Cyanite's library before
uploading it, by the `libraryTracks(filter: { sha256 })` lookup Cyanite
documents for duplicates or by the title the trial sends, and asks about the
track it finds. Ledger only: it is a paid trial's corner, not a shipped verb.
