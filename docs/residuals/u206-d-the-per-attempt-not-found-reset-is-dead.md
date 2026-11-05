---
title: The per attempt reset of what an ISRC lookup said kills no test at either seam and guards a state neither can reach
found: at the second review of #496, U206, 2026-11-05.
issue: no
---

**The mechanism.** `TidalAccount._isrc_tracks` in
`src/cratekit/modules/outbound/tidal_account.py` resets `last["said_not_found"]`
at the start of every attempt, so a not found on an attempt the ladder retried
past is not read as the settling answer. But `_call` returns `_ABSENT` on the
same attempt for every failure `isrc_cache.said_not_found` accepts, so no
attempt that set the flag is ever retried past.

The catalogue's `answered.clear()` in `TidalCatalogue.tracks_for_isrc`
(`src/cratekit/label/tidal_catalogue.py`) is the same shape: a not found returns
the empty answer on the attempt that raised it, so no retried attempt follows
one that appended.

**Measured cost.** None. Removing the account's reset passed all 57 tests in
`tests/test_isrc_cache.py` (Fable round two), and rows M15 and M19 of
`docs/mutation/u206.md` measure zero over the full suite for both seams.

**Closes when:** both resets are removed with a comment saying why, or a seam
starts retrying past a said not found and a test drives it. Ledger only.
