---
title: A landed twin's first pair sync keeps the twin's landing order over a Tidal reorder made since the landing
found: at the review of #620, R-1416, round one, 2026-11-07.
issue: no
---

**The mechanism.** A landing marks each twin's pair with no snapshot (`sync/twins.py`, `pair_landed`), so the pair's next `sync pair` is a first sync. The twin sits under `Custom Playlists <year>`, outside GIG READY, so since R-1416 that first sync is led by rekordbox: the twin keeps the order the landing wrote it in, which was the account's order at the landing. A Tidal reorder made between the landing and that first sync is therefore not taken into the twin, where before R-1416 it was. A short backfill of `sync twins` that records no snapshot reaches the same branch.

**Measured cost.** Driven by the round one reviewer through the dispatcher on the disposable database: a twin of 1, 2, 3, the account reordered to 3, 1, 2 after the landing; on main the first sync wrote the twin 3, 1, 2, on the branch it stays 1, 2, 3, the gate saying the order follows rekordbox's, so nothing false is said and nothing is lost. A later Tidal reorder still brings Tidal's whole order (608-outside-order-1). The brief's out of scope line leaves adopted and discovered pairs to the rule as it falls out; the session kept the rule general, since keeping rekordbox's order writes less into rekordbox.

**Closes when:** Phillip says whether a twin's first sync should follow the account instead (a `twin` check beside `order_kept` in `plan_pair`), or that it stands. Ledger only.
