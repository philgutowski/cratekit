---
title: The another app's folder half of home_of is reached by no test
found: at the review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `sync/pair_discover.home_of` refuses a top folder that is a
Cratekit tree root or another app's folder in one condition. The tree root
half is pinned by `test_home_of_refuses_each_place_it_cannot_decide`; the
other app's half is reached by no test, so a mutation of it kills nothing.

**Measured cost.** Maintainer facing. U198's discovery never records an
account root folder for another app's folder, so the input needs a person to
rename a recorded rekordbox folder into another app's shape.

**Closes when:** a test drives `home_of` on another app's top folder. Ledger
only.
