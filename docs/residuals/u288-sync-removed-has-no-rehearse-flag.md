---
title: crate sync removed has no rehearsal of its own, so its gate is rehearsed by hand on a copy with library state redirected
found: at the build of #839, U288, 2026-11-21.
issue: no
---

**The mechanism.** CLAUDE.md approves a database write gate only when a
rehearsal matches. `intake land` rehearses itself (`--rehearse`, U162);
`sync removed` does not, so the crate-sync skill's step drives it on a
disposable copy with `CRATEKIT_CONFIG_DIR`, `CRATEKIT_STATE_DIR` and the
library root redirected, by hand, and compares the offered rows with the live
plan's.

**Measured cost.** None driven: a session that skips the copy still meets the
gate, the backup acknowledgment, the confinement and the read back. The hand
procedure is slower and is where a session can get the redirection wrong
(the solutions entry on a disposable database copy).

**Closes when:** `sync removed --rehearse` runs the apply on a
`core.rehearsal` area and the live gate names the rehearsal's digest, as the
landing's does. Ledger only.
