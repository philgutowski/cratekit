---
title: A build older than U254 reads a journal applied ledger as not JSON and says run doctor, not upgrade
found: while building #683, U254, 2026-11-12.
issue: no
---

**The mechanism.** U254 writes the applied adoption ledger as a journal, a
header line and one record per line, at schema 2. A build before U254 parses
the file as one JSON document, fails on the second line, and refuses with
`adoption-ledger-unusable` and the doctor remedy, where a schema it did not
know would have said to upgrade. The refusal is the safe one, never an empty
ledger, so nothing re-applies; only the advice is wrong.

**Measured cost.** Not driven on an installed copy. Reachable when one
library is used from two installations at different versions, or when a
library's ledger was written by a newer build and an older one is run against
it.

**Closes when:** nothing further is needed once every installed copy carries
U254; the attended card U254 files updates them. Ledger only.
