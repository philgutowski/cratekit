---
title: U246's forecast pin filters the adds itself, and its growth bound admits a small quadratic term
found: at the review of #675, U246, 2026-11-12.
issue: no
---

**The mechanism.** `test_an_add_is_counted_against_what_the_playlist_holds_after_its_removals`
in `tests/test_sync_pair_calls.py` computes which adds the playlist lacks and
sends only those, where `TidalAccount.add_tracks` makes that decision itself,
so an adapter that began sending an add for a held track would not be seen.
And `tests/test_rebuild_growth.py` holds the count under three times for twice
the tracks; with the measured linear term of three comparisons per track, a
quadratic term under an eighth of a comparison per pair at 24 tracks passes.

**Measured cost.** None. Round two drove the adapter unfiltered over eight
inputs, the two pinned among them, and the request count equalled the
forecast on all eight. No mutant tried lands under the bound: the old shape
grows 3.92 times and a tuple scan 4.03.

**Closes when:** the pin calls `add_tracks` with every add, and the growth test
reads a third size or a tighter coefficient. Ledger only.
