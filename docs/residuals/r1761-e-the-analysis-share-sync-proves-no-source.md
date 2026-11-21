---
title: The analysis share's snapshot is an rclone sync with an archive and no proof of its source, so an emptied or unmounted share moves its whole copy into the dated archive
found: at the round one review of #893, R-1761, 2026-11-21.
issue: no
---

**The mechanism.** `SNAPSHOT_SHARE` in `modules/tools/backup.py` syncs the
analysis share beside a database kept outside the library root to
`analysis-share/` under `db_dest_root` with a backup dir, the same shape the
files mirror had before R-1761, and nothing proves the share folder holds
what it held.

**Measured cost.** Driven at round two with an emptied share folder: 5 of 5
analysis files moved to the share's dated archive. The producer, a share on
a volume that unmounts while the database stays, was not driven, and the
database portion was out of the card's scope.

**Closes when:** the share snapshot is held to the census's rule, or to
`--max-delete 0` when the share holds nothing. Ledger only.
