---
title: A regular file where DEADCA7's push backup folder belongs is said as a backup folder that does not exist
found: at the review of #576, U224, 2026-11-06.
issue: no
---

**The mechanism.** `_folder_presence` answers False for a path that is there and not a folder, and `_check_deadca7_push` words False as "its backup folder does not exist". With a file at `deadca7/rekordbox-backups`, the sub clause is false. Before U224 the same input read "its backup folder holds no entry", false the same way.

**Measured cost.** Driven by the round one review through `crate doctor` with a file at that path: the INFO line's sub clause is false; its claim that no push is recorded holds, since no entry can be read. Nothing known writes a file there; no producer was driven.

**Closes when:** a path that is there and not a folder is worded as such. Ledger only.
