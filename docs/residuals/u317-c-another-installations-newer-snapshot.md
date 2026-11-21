---
title: A database fingerprint is trusted after another installation took a newer snapshot, so an unchanged database is not snapshotted again while the default restore takes the other one
found: at the round two review of #877, U317, 2026-11-21.
issue: no
---

**The mechanism.** The database fingerprint record is installation state and
carries no token the library's database fact must hold, unlike the files
record since round one. Installation A snapshots generation one, installation
B snapshots generation two, the database is put back to generation one, and A
finds it unchanged against its own fingerprint, takes no snapshot and resets
the database age. A restore with no stamp named then pulls B's newer snapshot.

**Measured cost.** Driven at the engine with the put back made by a copy.
Generation one stays on the remote under its stamp, so nothing is lost; a
restore that names no stamp gets the other machine's database. `crate restore`
was not driven.

**Closes when:** the database fact carries the fingerprint record's token as
the files fact does, and a fact without it snapshots. Ledger only.
