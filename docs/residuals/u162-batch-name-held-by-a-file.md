---
title: A rehearsal reports a landing clean when the music folder holds a file named as the batch, and the live apply then fails as an internal error
found: at the second review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** The rehearsal holds at its area each staged name the live batch folder holds, so the area's move refuses what the live move will. It does not look at the batch folder itself: a plain file in the music folder named as the batch (`--name`) leaves the area's batch folder free, and the rehearsal lands, while the live apply's `target.mkdir` raises `FileExistsError`, reported as `internal-error` with nothing moved. `preflight_native` does not ask either; the live crash predates U162.

**Measured cost.** Driven by the second review with a hand placed file: the rehearsal reports landed 1, the live landing ends `internal-error`, the file stays in staging, nothing is lost. No Cratekit code was found that places such a file (a default batch name skips a taken name through `batch_name.taken`), so the producer is a person or another program.

**Closes when:** `preflight_native` refuses a batch path that exists and is not a folder, by name, which closes the live crash and the rehearsal's silence together. Ledger only.
