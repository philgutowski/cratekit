---
title: A sync pair plan reads the tag of every landed row lacking a database ISRC once a lacking track reaches the widened step
found: at the review of #593, U229, 2026-11-06.
issue: no
---

**The mechanism.** `_Reader.landed_anywhere` in `src/cratekit/sync/pair_cli.py` reads the file of each row in every INBOX playlist landed on the library, once per plan, whenever a lacking track carrying an ISRC is left by the four earlier steps. Every native landing leaves its rows without a database ISRC, so the reads grow with what has landed and not with what is asked.

**Measured cost.** Round one measured four tag reads per plan for four landed rows, against none on the base, and none on a resume within the run, which holds the plan. No provider call is added. The live count, over every landing still in rekordbox's INBOX, was not measured.

**Closes when:** the ISRC is written into a landed row at the landing, which the brief leaves out of scope, or the reads are measured on the live library and found small. Ledger only: it costs time, never a wrong answer.
