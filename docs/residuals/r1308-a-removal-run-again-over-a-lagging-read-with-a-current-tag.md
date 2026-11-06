---
title: A removal run again while the read still lags takes the wrong track off if the lagging listing carries the current version tag
found: at round one's review of #558, R-1308, 2026-11-06.
issue: no
---

**The mechanism.** `TidalAccount.remove_tracks` plans its positions from its
first reading and sends them with the version tag that reading came with. The
safety of a removal run again after R-1308's "may have landed" refusal rests
on the provider answering 412 to a removal whose tag is the one a stale
listing came with; the client takes the tag from the tracks response's own
header, so a lagging body and its tag should come from one response. Driven
on a stand in whose lagging listing keeps the playlist's CURRENT tag instead:
after a refused lagged removal of `b` from `[a, b, c, d]`, a fresh run reads
`[a, b, c, d]` stale, removes position 1, which is now `c`, and its read back,
lagging one write, shows `[a, c, d]`, equal to what it expected, so it
reports `b` taken off while `c` is gone.

**Measured cost.** Not reached on the live provider: the one live observation,
Sitting 62's 412 on a move after adds (U220's record), points to a stale read
carrying a stale tag, under which the same drive is answered 412 and nothing
comes off. Pre existing on main; R-1308's refusal and the GUIDE advise looking
by hand before anything runs again.

**Closes when:** an attended sitting reads a playlist straight after a
removal and compares the listing's tag with the playlist's, or the first
reading of a removal is held to what is known of the playlist (the residual
beside this one). Ledger only, since it closes at an attended sitting.
