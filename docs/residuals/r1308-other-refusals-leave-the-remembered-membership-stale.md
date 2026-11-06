---
title: An order's refusal and a removal's provider failure leave what the adapter remembers of the playlist as it was before
found: at round two's review of #558, R-1308, 2026-11-06.
issue: no
---

**The mechanism.** R-1308's read back forgets `TidalAccount._members` for
the playlist on every refusal, since what it holds is not known. The same
shape one method over does not: `order_tracks`'s `_read_back` and
`_settled` refuse with the entry holding the last reading `_positions`
took, lagging or not, and `remove_tracks`'s provider failures (a removal
not accepted, or a call that raised) leave the reading from before the
removal. Round two drove what a stale entry does on round one's head: a
later `add_tracks` on the same adapter answered a track as held and added
nothing while the provider did not hold it.

**Measured cost.** None reached: the four callers (prune, the mirror's
apply, `label heard`, `sync pair`) each raise out of the command on these
refusals, read and not driven, so no later call on the same adapter reads
the entry.

**Closes when:** every refusal and failure after a write forgets the entry,
or a caller is found that continues on the same adapter. Ledger only.
