---
title: A sync removed run in flight writes over a retirement a person recorded while it read the account
found: at the review of #889, U320, round one, 2026-11-21.
issue: no
---

**The mechanism.** `removed_cli._read_synced` reads the record of not found
answers before it asks the account and writes each read's answer, under the
record's lock, after. A `--retire` answered while that run was reading is
overwritten by the run's own answer for the same playlist, computed from the
record as it stood before.

**Measured cost.** Driven by review round one with a retirement written into
the record mid read: the retirement was lost. The side it errs on keeps rows:
the playlist answers not found again and is retired a day later, or is
retired again. Not driven as two processes.

**Closes when:** the write merges each read's answer over the entry as it
stands under the lock, keeping a retirement made since the read. Ledger only.
