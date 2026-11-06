---
title: A playlist of more than a hundred tracks is still judged by a window that lags a change past its first hundred
found: at round one of U226's review (#578), 2026-11-06.
issue: yes
---

**The mechanism.** U226 judges every account removal and order, and the
`crate sync pair` plan and check, by the window read beside the client's
unpaged read (`acquire.listing.judge_window`). The unpaged read is taken as
the playlist only when it holds every track the playlist declares. The
client fills the unpaged read's missing limit with its session's
`item_limit`, 1000, and `listing.PAGE_SIZES` records the provider's ceiling
for this shape as 100, so a playlist of more than a hundred tracks is most
likely served its first hundred alone. The judge then reads an unpaged read
that is the window's first part as agreeing, and takes the window as the
playlist, as every read did before U226: a change past the first hundred
that the window lags is not seen.

**Measured cost.** Driven on the stand ins at round one: a person's move in
the tail of a playlist whose unpaged read is capped (members a, b, d, c;
window serving a, b, c, d; unpaged capped at 2) made `order_tracks` move the
wrong track on the account and refuse `read-back-differs`, `lagged: no`;
through the verb, a four track pair whose window served an old order past
the cap wrote that order into rekordbox and recorded it as the snapshot,
with `totals.read_backs` empty. Round two drove the degenerate case: an unpaged read
that comes back empty agrees with any window, so a landed removal behind a
lagging window was refused "may have landed" after 4 readings. No worse than main, which read every
playlist this way. The live cap was not measured: 0 live candidates driven.

**Closes when:** the next attended sitting reads `len(p.tracks())` beside
`p.num_tracks` on the longest paired playlist. If the unpaged read is capped
below a paired playlist's length, the judge reads past its first page the
same way (a walk of the unpaged kind with an offset, or a prefix read as a
lag for the pairs it touches), with a test on a stand in of the measured
cap. Earns an issue: a write path whose guard is blind for every paired
playlist past the cap, board bar (a) and (d).
