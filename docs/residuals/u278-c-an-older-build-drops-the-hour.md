---
title: A build from before U278 that writes the provider gate file drops the hour's count
found: at the review of #741, U278, 2026-11-12.
issue: no
---

**The mechanism.** The hour's count is a new `window` key in
`provider_gate.json`. A build before U278 reads the file into its own state,
which has no such field, and writes it back without it, so every minute the
window held is lost and the next U278 build starts an empty hour.

**Measured cost.** Driven by the round one review: seven calls through the
branch's gate, one through `origin/main`'s on the same file, and the window
read 0. The producer is an installed copy older than U278 beside a newer one,
which lasts until the Mac's installed copy is updated; the attended check of
this unit is owed on an installed copy at U278 or later.

**Closes when:** every installed copy on the machine carries U278. Ledger only.
