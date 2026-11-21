---
title: The probe that stands in for a refused walk passes over a folder it cannot list, so an unreadable library can be refused as holding none of its files
found: at the round one review of #893, R-1761, 2026-11-21.
issue: no
---

**The mechanism.** `backup_record.probe` skips a directory whose listing
raises, so what it cannot read is never counted. Where the walk refused and
the library's folders cannot be listed, the root reads as holding none of
its files and the backup refuses with the mount remedy, which is the wrong
fix. It fails closed: nothing is sent or archived.

**Measured cost.** Not driven: the container runs as root, which lists every
directory. A person would be told to mount a mounted volume.

**Closes when:** the probe counts an unlistable folder as unreadable and the
refusal says so. Ledger only.
