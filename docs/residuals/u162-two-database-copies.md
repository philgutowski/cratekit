---
title: Each rehearsal holds two full copies of the database on the library volume, its own and its session's capture
found: at the second review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** A rehearsal copies the database file set into its area, and the guarded session its landing runs under takes its own pre write capture of that copy into the area's library state. Both go when the area is removed; a kept area keeps both.

**Measured cost.** Measured on a fixture database only: two times the database's size on the library volume per rehearsal, and the time to copy it twice. On the live library, a few hundred megabytes for the length of a rehearsal. Not a false report.

**Closes when:** the rehearsal's session is told its capture is the area's copy, or a kept area is reported with its size. Ledger only.
