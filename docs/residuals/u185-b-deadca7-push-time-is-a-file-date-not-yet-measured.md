---
title: doctor reads DEADCA7's last push as its newest backup entry's modification time, unmeasured against a real push
found: at the review of #392, U185, 2026-10-31.
issue: no
---

**The mechanism.** `deadca7.push` in `cli/doctor.py` takes the newest entry in DEADCA7's `rekordbox-backups` folder and reads its modification time as when the app last pushed into the database. If the app makes that backup by copying `master.db` with its date kept, the time read is rekordbox's last write before the push, and a push made after this product's last database backup could be reported as one that backup holds.

**Measured cost.** Not driven: it needs a real DEADCA7 push. Dated directory entries, an empty folder, an unreadable entry and an unreadable fact file were driven and answer as written.

**Closes when:** the attended sitting U185 owes pushes once into a disposable copy and compares the newest entry's modification time with the push's own time. If they differ, the check reads the entry's name or its creation time instead. Ledger only, since it closes at an attended sitting.
