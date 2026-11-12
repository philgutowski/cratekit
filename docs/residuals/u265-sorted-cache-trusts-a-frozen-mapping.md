---
title: LibraryIndex keeps its sorted recordings from the first approximate call, so a by_recording dict changed afterwards is scored stale
found: at the review of #694, U265, 2026-11-12.
issue: no
---

**The mechanism.** `LibraryIndex.sorted_recordings` builds the recordings and their sorted words the first time the approximate pass asks and keeps them for the life of the index. The class is frozen, but `by_recording` is typed `Mapping` and a caller holding the dict it passed in could still add to it; the review added a recording to the dict after a first call and the pass did not offer it, where the shipped call did.

**Measured cost.** None reachable: the one constructor in `src`, `index_paths`, builds a fresh dict and hands it over, and no code in `src` writes to `by_recording` afterwards (zero producers found by grep).

**Closes when:** the index wraps its mappings read only at construction, or the cache checks the mapping's length before use. Ledger only.
