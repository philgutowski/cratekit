---
title: Freezing the snapshot the gate's plan read rather than the one it then recorded kills no test
found: at the review of #552, U222, 2026-11-05.
issue: no
---

**The mechanism.** `account_mirror._record` freezes `reading.recorded`, the
ledger as the gate's plan read it, never the ledger after that plan's own
`record_mirror_agreed`. Freezing the recorded one instead kills zero tests:
in the worlds the suite builds, that record leaves a held track's word as it
was, so the two readings are equal and the test written for the claim cannot
tell them apart.

**Measured cost.** None observed. By `agreed_after`, the two readings decide
the same plan in every case the reviewer and the author constructed; the cost
is an untested claim, not a write.

**Closes when:** a world is found where the gate's own record changes a word
the edit rule reads, and a test pins the frozen one, or the claim is shown to
hold by construction and the docstring says so. Ledger only.
