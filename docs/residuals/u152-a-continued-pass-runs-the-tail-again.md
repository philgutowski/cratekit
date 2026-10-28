---
title: a continued crate sync land pass queues and drives the whole tail again over the staging folder
found: at the review of #333, U152, 2026-10-28.
issue: no
---

**The mechanism.** A continued pass reads every job that already ended (its intake jobs, its download) and does not drive them again, but the tail, `tag folder`, `analyze run` and `analyze restamp`, is queued fresh over the staging folder on every run, since a tail job is frozen against the folder as it stood and a stale one is replaced rather than resumed. A succeeded tail job over the same folder is not read as settled.

**Measured cost.** Driven at the review: tail job counts went from one to two each on a continuation. Time only: the analysis skips a file that already carries its Camelot head, and tagging and restamping again write the same values. The flag's help says the tail runs again.

**Closes when:** a succeeded tail job over the same folder, with no file added since, is read as settled. Ledger only.
