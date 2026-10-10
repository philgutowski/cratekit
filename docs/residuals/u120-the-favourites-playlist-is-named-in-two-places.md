---
title: The favourites playlist is named in two places, the taxonomy class and the outbound default, and one chooser picks between them
found: at the build of #277, U120, 2026-10-10.
issue: no
---

**The mechanism.** U119 declared which playlist is the favourites as the
`favorites` class's `signal_playlist`; the outbound sweep names the same
playlist as `source.DEFAULT_FAVORITES_PLAYLIST` and its `--favorites-playlist`
flag. `placement.source_name` reads the class first and falls back to the
default, so the landing and the backfill agree with the refresh on a library
that declares the class and still work on one whose active taxonomy predates
it, which the live library's did on 2026-10-10. An author who renames the
class's playlist has renamed where hearts land and not where the sweep reads
local favourites from, unless the flag follows.

**Measured cost.** Not driven. The two names are equal on the shipped
template and on the live library.

**Closes when:** the outbound sweep reads its default from the class too, or
the class's `signal_playlist` is the one spelling and the outbound default is
removed. Ledger only.
