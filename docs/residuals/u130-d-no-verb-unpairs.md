---
title: No verb unpairs a playlist pair
found: at the review of #298, U130, 2026-10-10.
issue: no
---

**The mechanism.** `crate sync pair` marks a pair and nothing removes one. A
pair whose account or rekordbox playlist is gone is left out of a sync of every
pair and named in the answer each time (`sync-pair-left-out`), and pairing
either surviving playlist with another is refused as a conflict.

**Measured cost.** A warning on every sync, and a hand edit of the playlist
pairs document to pair the survivor again. Nothing is written wrongly.

**Closes when:** a gated `sync unpair` drops a pair and its snapshot. Ledger
only until someone wants it.
