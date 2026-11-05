---
title: The released and name taken reasons still say pair it by hand without the rekordbox playlist
found: at the review of #530, U216, 2026-11-05.
issue: no
---

**The mechanism.** U216's fix round made `pair_discover.BY_HAND` say to make
or choose the rekordbox playlist and name `--rekordbox PLAYLIST_ID`, and its
two new reasons use it. The RELEASED reason in `sync/pair_cli._discovered_back`
and in `pair_discover.discover`, and the name taken reason in
`pair_discover.home_of`, keep the older words, and the test that pins the step
lists BEFORE and COPY only.

**Measured cost.** Driven by the review's second round: following the RELEASED
row's step as written, `crate sync pair pl-3`, exits 30 saying the account
playlist is not paired with a rekordbox playlist; the refusal's own steps name
the right form. One dead end command, nothing lost.

**Closes when:** every pair by hand step reads `BY_HAND`, and the test
quantifies over every kind the back direction lists. Ledger only.
