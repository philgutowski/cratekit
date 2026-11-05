---
title: The ISRC lookup's per attempt reset of its not found flag kills no test and guards a state the account cannot reach
found: at the second review of #496, U206, 2026-11-05.
issue: no
---

**The mechanism.** `TidalAccount._isrc_tracks` in
`src/cratekit/modules/outbound/tidal_account.py` resets `last["said_not_found"]`
at the start of every attempt, so a not found on an attempt the ladder retried
past is not read as the settling answer. But `_call` returns `_ABSENT` on the
same attempt for every failure `isrc_cache.said_not_found` accepts, so no
attempt that set the flag is ever retried past.

**Measured cost.** None. Removing the reset passed all 57 tests in
`tests/test_isrc_cache.py` (Fable round two), and row M15 of
`docs/mutation/u206.md` measures the same zero.

**Closes when:** the reset is removed with a comment saying why, or the account
starts retrying past a said not found and a test drives it. Ledger only.
