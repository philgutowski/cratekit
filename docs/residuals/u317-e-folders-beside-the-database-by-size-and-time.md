---
title: The settings folders and the analysis share beside the database are fingerprinted by size and time only, so a rewrite keeping both is called unchanged
found: at the round one review of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** `backup_record.database_fingerprint` hashes the database
set's content and reads the settings folders and an outside analysis share by
size and modification time, since the share can be gigabytes. A file there
rewritten keeping both is not seen, the portion is `unchanged`, and the newest
snapshot holds the older file.

**Measured cost.** Driven with the time put back by hand. rekordbox moves the
time when it writes, so no producer of a rewrite keeping both was driven.

**Closes when:** the small settings folders are hashed whole, with the share
left to size and time. Ledger only.
