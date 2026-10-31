---
title: Whether a rehearsal reports landed over a live batch folder the live move cannot write is undriven
found: at the second review of #343, U162, 2026-10-31.
issue: no
---

**The mechanism.** The area is always writable. A live batch folder the live user cannot write would refuse the live move with `path-permission-denied` while the rehearsal lands.

**Measured cost.** Not driven: the cloud container runs as root, which writes any mode, and no Cratekit code changes a folder's mode, so the producer was not driven either.

**Closes when:** driven on a Mac with a folder made read only, and the area mirrors the live batch folder's writability if it holds. Ledger only.
