---
title: A long playlist's walk past the unpaged read's first page rests on two unmeasured facts about the provider's version tag
found: at round one of R-1360's review (#585), 2026-11-06.
issue: no
---

**The mechanism.** `acquire.listing.playlist_tracks_unpaged` walks past a
first page short of the declared count, one track back per request, and
takes a later page only while it starts on the last track read, is no
longer than the first page and carries the first page's version tag
(`_etag`, which the installed client overwrites on every response). A
change wholly past the first page leaves the start and length checks
passing, so the tag is the walk's one defence against a stale later page.
Two facts were not measured live. If a stale later page carries the
CURRENT tag, the walk reads the stale tail as whole and the window is
agreed with, as main read every long playlist. If the tag is one per
response rather than the playlist's version, every walk breaks, and since a
first part beside a whole window is now a lag, every paired playlist past
the cap is held on every run (`sync-pair-left-out`, exit 41 when named) and
never syncs, while the guide's "sync again a few minutes later" cannot help.
An empty unpaged read beside a whole window is a lag for the same reason.

**Measured cost.** Driven at round one on three producers each (the U220
stand in, the verb on the discovery world, the installed client with its
HTTP stubbed): a stale page with the current tag took a removal off by its
stale position, t129 for t130, and reported `sync-pair-nothing` over a
stale read; a tag per response held a 150 track playlist nobody changed,
`window-lags` after 4 readings and 7 seconds, and left a five track pair out
of the run. 0 live candidates driven. Writes succeed with the tag the
window read and the unpaged read each leave whatever limit they asked with,
which a tag per response would not allow, but no two pages of one playlist
were compared.

**Closes when:** the attended sitting filed with R-1360's landing reads,
on the longest paired playlist, the tag of `p.tracks()` beside that of
`p.tracks(offset=99)`, before and after a move made past the first hundred
in the Tidal app, and whether that later page is current. Ledger only:
it closes at an attended sitting.
